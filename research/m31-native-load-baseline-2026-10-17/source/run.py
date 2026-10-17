"""Single-use native-load qualification supervisor; no scientific imports.

Source draft. Only explicit execution after source/publication freeze may launch children.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import signal
import subprocess
import sys
import time

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
LIMIT = 32 * 1024 * 1024


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value, final=False):
    data = (json.dumps(value, allow_nan=False, separators=(',', ':')) + '\n').encode()
    if len(data) > LIMIT:
        raise ValueError('metadata-limit')
    target = path.with_name(path.name + '.final.tmp') if final else path
    with target.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if final:
        os.replace(target, path)


def need(condition, code):
    if not condition:
        raise ValueError(code)


def child_limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT, LIMIT))
    # This limits each inherited process, not aggregate browser CPU or memory.
    resource.setrlimit(resource.RLIMIT_CPU, (120, 121))


def terminate_group(process):
    # The retained guardian is not polled/reaped before this cleanup, preventing
    # group-leader PID reuse. The harness forces Chrome detached=False.
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            break
        if sig == signal.SIGTERM:
            time.sleep(0.2)
    process.wait(timeout=5)


def main():
    stage, expected, commit = sys.argv[1:]
    need(stage in ('browser', 'check'), 'stage')
    need(len(expected) == 64 and len(commit) == 40 and
         all(c in '0123456789abcdef' for c in expected + commit), 'identity-arguments')
    result_dir = PACKAGE / 'results'
    result_dir.mkdir(exist_ok=True)
    attempt_path = result_dir / (stage + '-attempt.json')
    attempt = {'schema': 'm31-native-load-attempt-v1', 'stage': stage,
               'sourceManifestSha256': expected, 'sourceCommit': commit,
               'startedUtc': utc(), 'status': 'started', 'firstFailure': None,
               'resourceScope': '120s supervised child wall, 32MiB per file, 120/121s per-process CPU inherited; no enforced aggregate memory ceiling; output totals checked after exit. Browser subprocess memory not measured.',
               'dispatchContextAttestation': os.environ.get('RESEARCH_EXECUTION_CONTEXT')}
    save(attempt_path, attempt)
    start = time.monotonic()
    process = None
    exit_code = 1
    try:
        need(attempt['dispatchContextAttestation'] == 'tool-require-escalated', 'dispatch-attestation')
        need(sys.platform == 'darwin', 'darwin-runtime')
        need(datetime.datetime.now(datetime.timezone.utc) < datetime.datetime.fromisoformat('2026-10-17T03:00:00+00:00'), 'launch-cutoff')
        source = (PACKAGE / 'source-manifest.json').read_bytes()
        need(sha(source) == expected, 'source-manifest-sha')
        manifest = json.loads(source)
        for pin in manifest['files']:
            path = ROOT / pin['path']
            need(path.resolve().is_relative_to(ROOT), 'pin-path')
            data = path.read_bytes()
            need(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'source-pin:' + pin['path'])
        attempt['verifiedPins'] = len(manifest['files'])
        for kind, path in [('python', Path(sys.executable)), ('node', Path(os.environ['RESEARCH_NODE']))]:
            data = path.read_bytes()
            pin = manifest['runtime'][kind]
            need(len(data) == pin['bytes'] and sha(data) == pin['sha256'], kind + '-runtime')
        publication = json.loads((PACKAGE / 'source-publication.json').read_bytes())
        need(publication['commit'] == commit and publication['manifestSha256'] == expected
             and publication['manifestBytes'] == len(source)
             and publication['manifestPath'] == str((PACKAGE / 'source-manifest.json').relative_to(ROOT))
             and publication['verifiedFilePins'] == len(manifest['files'])
             and publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True
             and datetime.datetime.fromisoformat(publication['verifiedUtc']) <= datetime.datetime.fromisoformat(attempt['startedUtc']), 'publication-binding')
        preservation_inputs = [PACKAGE / 'source-manifest.json', PACKAGE / 'source-publication.json']
        if stage == 'check':
            prior = json.loads((result_dir / 'browser-attempt.json').read_bytes())
            data = (result_dir / 'browser.json').read_bytes()
            need(prior['status'] == 'completed' and prior['exitCode'] == 0
                 and prior['sourceCommit'] == commit and prior['sourceManifestSha256'] == expected
                 and prior['outputSha256'] == sha(data) and prior['outputBytes'] == len(data), 'browser-completion')
            preservation_inputs += [result_dir / 'browser-attempt.json', result_dir / 'browser.json',
                                    result_dir / 'browser-journal.jsonl']
        preservation = {str(path.relative_to(ROOT)): {'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())}
                        for path in preservation_inputs}
        attempt['additionalPreservationInputs'] = preservation
        need(not (result_dir / (stage + '.json')).exists(), 'output-already-exists')
        command = ([os.environ['RESEARCH_NODE'], str(PACKAGE / 'source/controller.cjs')] if stage == 'browser'
                   else [sys.executable, '-I', '-B', str(PACKAGE / 'source/check.py')])
        command += [str(ROOT), expected, commit]
        # Keep raw operational stdout/stderr private. Public outputs identify hashes only.
        private = Path(os.environ['RESEARCH_PRIVATE_LOG_DIR'])
        need(private.is_absolute() and not private.resolve().is_relative_to(ROOT), 'private-log-location')
        private.mkdir(parents=True, exist_ok=True)
        log_path = private / (stage + '.log')
        supervisor_dir = private / (stage + '-supervisor')
        supervisor_dir.mkdir(exist_ok=False)
        environment = dict(os.environ, RESEARCH_SUPERVISOR_DIR=str(supervisor_dir))
        guardian = [sys.executable, '-I', '-B', str(PACKAGE / 'source/group-runner.py')]
        with log_path.open('xb') as log:
            process = subprocess.Popen(guardian + command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       stdin=subprocess.PIPE, env=environment,
                                       start_new_session=True, preexec_fn=child_limits)
            child_start = time.monotonic()
            exit_path = supervisor_dir / 'exit.json'
            while not exit_path.exists():
                if time.monotonic() - child_start >= 120:
                    raise TimeoutError('child-wall-deadline')
                time.sleep(0.1)
            child_code = json.loads(exit_path.read_bytes())['returncode']
            attempt['childWallSeconds'] = time.monotonic() - child_start
            attempt['childExitCode'] = child_code
            # Guardian stays alive after the child completes. Do not poll/reap it
            # before the owned-group cleanup, including on successful completion.
            terminate_group(process)
            process = None
            attempt['ownedGroupCleanupIssued'] = True
        log_bytes = log_path.read_bytes()
        attempt['privateLog'] = {'bytes': len(log_bytes), 'sha256': sha(log_bytes), 'published': False}
        need(child_code == 0, 'child-exit')
        output_path = result_dir / (stage + '.json')
        need(output_path.stat().st_size <= LIMIT, 'output-byte-limit')
        data = output_path.read_bytes()
        attempt.update(outputBytes=len(data), outputSha256=sha(data))
        total = sum(p.stat().st_size for p in result_dir.iterdir() if p.is_file())
        need(total <= 96 * 1024 * 1024, 'combined-evidence-limit')
        # Verify original source/input closure again after execution.
        for pin in manifest['files']:
            data = (ROOT / pin['path']).read_bytes()
            need(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'postrun-pin:' + pin['path'])
        for relative, pin in preservation.items():
            data = (ROOT / relative).read_bytes()
            need(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'postrun-generated-input:' + relative)
        attempt['preservationPassed'] = True
        attempt['status'] = 'completed'
        exit_code = 0
    except Exception as exc:
        attempt['status'] = 'failed'
        message = str(exc).replace(str(ROOT), 'REPOSITORY').replace(str(Path.home()), '[HOME]')
        attempt['firstFailure'] = {'type': type(exc).__name__, 'message': message[:512]}
        if process is not None:
            try:
                terminate_group(process)
            except Exception:
                attempt['cleanupError'] = True
    finally:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        attempt.update(finishedUtc=utc(), wallSeconds=time.monotonic() - start,
                       supervisorPeakRssBytes=usage.ru_maxrss, exitCode=exit_code)
        save(attempt_path, attempt, final=True)
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
