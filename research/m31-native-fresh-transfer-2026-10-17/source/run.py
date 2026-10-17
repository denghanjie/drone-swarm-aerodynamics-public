"""Prospective finite four-stage supervisor; no scientific imports.

Single-process stages use retained child handles. Browser stage retains a group
leader until its controller and recorded Chrome root have closed. Successful
browser completion releases the guardian without a group signal. This does not
claim all Chrome helpers exited or hard containment under supervisor loss.
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
NAME = 'research/m31-native-fresh-transfer-2026-10-17'
STAGES = ('generation', 'reference', 'browser', 'check')
FILE_CAP = 32 * 1024 * 1024
TOTAL_CAP = 256 * 1024 * 1024
ATTEMPT_CAP = 1024 * 1024


def need(value, code):
    if not value:
        raise ValueError(code)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def identity(path):
    digest = hashlib.sha256()
    count = 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
            count += len(block)
    return {'bytes': count, 'sha256': digest.hexdigest()}


def verify(pin):
    path = ROOT / pin['path']
    need(not Path(pin['path']).is_absolute() and path.resolve().is_relative_to(ROOT), 'pin-location')
    need(identity(path) == {key: pin[key] for key in ('bytes', 'sha256')}, 'pin:' + pin['path'])


def read_json(path):
    need(path.stat().st_size <= FILE_CAP, 'json-cap')
    return json.loads(path.read_bytes())


def public_error(error):
    message = str(error).replace(str(ROOT), 'REPOSITORY').replace(str(Path.home()), '[HOME]')
    return {'type': type(error).__name__, 'message': message[:512]}


def save(path, value, final=False):
    data = (json.dumps(value, allow_nan=False, separators=(',', ':')) + '\n').encode()
    need(len(data) <= ATTEMPT_CAP, 'attempt-size')
    target = path.with_name(path.name + '.final.tmp') if final else path
    with target.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if final:
        os.replace(target, path)


def assertions(value, expected):
    for dotted, wanted in expected.items():
        actual = value
        for key in dotted.split('.'):
            actual = actual[key]
        need(type(actual) is type(wanted) and actual == wanted, 'output-assertion:' + dotted)


def limits(seconds):
    def apply():
        resource.setrlimit(resource.RLIMIT_CPU, (seconds, seconds + 1))
        resource.setrlimit(resource.RLIMIT_FSIZE, (FILE_CAP, FILE_CAP))
    return apply


def files_under(path):
    return [p for p in path.rglob('*') if p.is_file() and not p.is_symlink()]


def disk_bytes(path):
    # lstat counts symlink/socket metadata without following private profile links.
    if not path.exists():
        return 0
    return sum(p.lstat().st_size for p in path.rglob('*') if not p.is_dir() or p.is_symlink())


def stop_owned(process, group):
    # Group leader has not been polled/reaped. Only browser guardians use group
    # cleanup, and only after a failure/timeout. Normal completion never does.
    if group:
        need(process.returncode is None, 'refuse-group-signal-after-reap')
        os.killpg(process.pid, signal.SIGTERM)
        time.sleep(0.2)
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif process.poll() is None:
        process.kill()
    process.wait(timeout=4)


def main(stage, expected, commit):
    need(stage in STAGES and PACKAGE == ROOT / NAME, 'stage-location')
    need(len(expected) == 64 and len(commit) == 40 and all(c in '0123456789abcdef' for c in expected + commit), 'source-arguments')
    results = PACKAGE / 'results'
    results.mkdir(exist_ok=True)
    attempt_path = results / (stage + '-attempt.json')
    attempt = {'schema': 'm31-native-fresh-attempt-v1', 'stage': stage,
               'sourceManifestSha256': expected, 'sourceCommit': commit,
               'startedUtc': utc(), 'status': 'started', 'firstFailure': None,
               'dispatchContextAttestation': os.environ.get('RESEARCH_EXECUTION_CONTEXT'),
               'scope': 'Finite fresh-state numerical transfer; no benchmark or all-helper cleanup claim.'}
    save(attempt_path, attempt)  # exclusive; occupied attempts cannot be replaced
    start = time.monotonic()
    process, group, code = None, False, 1
    pins, protected, previous_files = [], {}, {}
    private, log_path, config = None, None, None
    previous_wall = 0
    cleanup_started = None
    try:
        need(attempt['dispatchContextAttestation'] == 'tool-require-escalated', 'dispatch-attestation')
        need(sys.platform == 'darwin', 'darwin-runtime')
        cutoff = datetime.datetime.fromisoformat('2026-10-17T03:00:00+00:00')
        need(datetime.datetime.now(datetime.timezone.utc) < cutoff, 'launch-cutoff')
        manifest_path = PACKAGE / 'source-manifest.json'
        manifest_id = identity(manifest_path)
        need(manifest_id['sha256'] == expected, 'manifest-sha')
        manifest = read_json(manifest_path)
        pins = manifest['files']
        by_path = {pin['path']: pin for pin in pins}
        need(len(by_path) == len(pins), 'duplicate-pins')
        for pin in pins:
            verify(pin)
        need(all(NAME + '/' + rel in by_path for rel in ['source/run.py', 'source/group-runner.py', 'config.json']), 'supervisor-source-closure')
        config = read_json(PACKAGE / 'config.json')
        need(config['schema'] == 'm31-native-fresh-config-v1', 'config-schema')
        need(config['stageOrder'] == list(STAGES) and config['launchCutoffUtc'] == '2026-10-17T03:00:00+00:00', 'stage-contract')
        need(config['limits'] == {'perFileBytes': FILE_CAP, 'combinedOutputLogScratchBytes': TOTAL_CAP,
                                 'cumulativeSupervisorSeconds': 1500, 'cleanupSeconds': 10}, 'global-limits')
        entry = config['stages'][stage]
        need([config['stages'][s]['childWallSeconds'] for s in STAGES] == [120, 600, 120, 180], 'fixed-stage-limits')
        for kind, executable in [('python', Path(sys.executable).resolve()), ('node', Path(os.environ['RESEARCH_NODE']).resolve())]:
            pin = manifest['runtime'][kind]
            need(identity(executable) == {k: pin[k] for k in ('bytes', 'sha256')}, 'runtime:' + kind)
        need(not os.environ.get('NODE_OPTIONS') and not os.environ.get('NODE_PATH'), 'node-environment')
        publication_path = PACKAGE / 'source-publication.json'
        receipt = read_json(publication_path)
        need(receipt['commit'] == commit and receipt['manifestSha256'] == expected
             and receipt['manifestPath'] == NAME + '/source-manifest.json'
             and receipt['manifestBytes'] == manifest_id['bytes'] and receipt['verifiedFilePins'] == len(pins)
             and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True
             and datetime.datetime.fromisoformat(receipt['verifiedUtc']) <= datetime.datetime.fromisoformat(attempt['startedUtc']), 'publication-binding')
        protected = {NAME + '/source-manifest.json': manifest_id,
                     NAME + '/source-publication.json': identity(publication_path)}
        private = Path(os.environ['RESEARCH_PRIVATE_LOG_DIR'])
        profile = Path(os.environ['RESEARCH_BROWSER_PROFILE'])
        need(private.is_absolute() and profile.is_absolute()
             and not private.resolve().is_relative_to(ROOT) and profile.resolve().is_relative_to(private.resolve()), 'private-locations')
        private_identity = hashlib.sha256(str(private.resolve()).encode()).hexdigest()
        attempt['privateDirectoryIdentitySha256'] = private_identity
        for prior in STAGES[:STAGES.index(stage)]:
            prior_attempt = read_json(results / (prior + '-attempt.json'))
            prior_path = results / (prior + '.json')
            need(prior_attempt['status'] == 'completed' and prior_attempt['exitCode'] == 0
                 and prior_attempt['sourceCommit'] == commit and prior_attempt['sourceManifestSha256'] == expected
                 and prior_attempt['privateDirectoryIdentitySha256'] == private_identity
                 and identity(prior_path) == {'bytes': prior_attempt['outputBytes'], 'sha256': prior_attempt['outputSha256']}, 'prior-stage:' + prior)
            assertions(read_json(prior_path), config['stages'][prior]['requiredForFollowingStage'])
            previous_wall += prior_attempt['wallSeconds']
        need(previous_wall + entry['childWallSeconds'] + 10 <= 1500, 'remaining-total-time')
        for path in files_under(results):
            if path != attempt_path:
                previous_files[str(path.relative_to(ROOT))] = identity(path)
        output_path = results / (stage + '.json')
        need(not output_path.exists(), 'stage-output-exists')
        private.mkdir(parents=True, exist_ok=True)
        if stage == 'browser':
            need(not profile.exists(), 'fresh-browser-profile')
        attempt.update(verifiedPins=len(pins), priorArtifactsPreserved=len(previous_files),
                       resourceScope='Child wall/CPU/file caps; cumulative supervisor wall and256MiB disk checked at completion. No memory ceiling. Wall supervision requires live parent. Browser-root/controller close only; not all helpers.')
        log_path = private / (stage + '.log')
        executable = str(Path(sys.executable).resolve()) if entry['runtime'] == 'python' else os.environ['RESEARCH_NODE']
        command = [executable] + (['-I', '-B'] if entry['runtime'] == 'python' else [])
        need(entry['source'] in by_path, 'entry-source-pin')
        command += [str(ROOT / entry['source']), str(ROOT), expected, commit]
        environment = dict(os.environ)
        if stage == 'browser':
            group = True
            guard_dir = private / 'browser-supervisor'
            guard_dir.mkdir(exist_ok=False)
            environment['RESEARCH_SUPERVISOR_DIR'] = str(guard_dir)
            command = [str(Path(sys.executable).resolve()), '-I', '-B', str(PACKAGE / 'source/group-runner.py')] + command
        need(datetime.datetime.now(datetime.timezone.utc) < cutoff, 'pre-spawn-cutoff')
        with log_path.open('xb') as log:
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       stdin=subprocess.PIPE if group else subprocess.DEVNULL,
                                       env=environment, start_new_session=group,
                                       preexec_fn=limits(entry['childWallSeconds']))
            child_start = time.monotonic()
            if group:
                exit_path = guard_dir / 'exit.json'
                while not exit_path.exists():
                    need(time.monotonic() - child_start < entry['childWallSeconds'], 'browser-child-wall-deadline')
                    time.sleep(0.1)
                child_code = read_json(exit_path)['returncode']
            else:
                child_code = process.wait(timeout=entry['childWallSeconds'])
            attempt.update(childWallSeconds=time.monotonic() - child_start, childExitCode=child_code)
            need(child_code == 0, 'child-exit')
            output = read_json(output_path)
            assertions(output, entry['completionAssertions'])
            if group:
                # Root event assertions belong in the frozen browser contract.
                # The guardian still owns the session while we verify them.
                assertions(output, config['browserRootCompletionAssertions'])
                release_start = time.monotonic()
                cleanup_started = release_start
                process.stdin.write(b'R')
                process.stdin.flush()
                guard_code = process.wait(timeout=5)
                process = None  # Reaped handle must never reach group cleanup.
                attempt['childReaped'] = True
                need(guard_code == 0, 'guardian-release-exit')
                attempt.update(guardianReleasedWithoutGroupSignal=True, guardianExitCode=guard_code,
                               browserRootAndControllerClosed=True,
                               cleanupSeconds=time.monotonic() - release_start,
                               allHelpersExitClaim=False)
            attempt['childReaped'] = True
            process = None
        output_pin = identity(output_path)
        attempt.update(outputBytes=output_pin['bytes'], outputSha256=output_pin['sha256'])
        code = 0
    except Exception as error:
        attempt['firstFailure'] = public_error(error)
    finally:
        if process is not None:
            cleanup_start = cleanup_started if cleanup_started is not None else time.monotonic()
            try:
                stop_owned(process, group)
                attempt['childReaped'] = True
            except Exception as error:
                attempt['cleanupError'] = public_error(error)
                code = 1
            attempt['cleanupSeconds'] = time.monotonic() - cleanup_start
        try:
            for pin in pins:
                verify(pin)
            for relative, pin in {**protected, **previous_files}.items():
                need(identity(ROOT / relative) == pin, 'preservation:' + relative)
            attempt['preservationPassed'] = bool(pins and protected)
            if log_path is not None and log_path.exists():
                attempt['privateLog'] = dict(identity(log_path), published=False)
            total = disk_bytes(results) + (disk_bytes(private) if private is not None else 0) + 2 * ATTEMPT_CAP
            need(attempt.get('cleanupSeconds', 0) <= 10, 'cleanup-time-cap')
            need(total <= TOTAL_CAP, 'total-evidence-log-scratch-cap')
            attempt['evidenceLogScratchBytesWithFinalizationReserve'] = total
            need(previous_wall + time.monotonic() - start <= 1500, 'total-supervisor-time-cap')
        except Exception as error:
            attempt['preservationOrResourceFailure'] = public_error(error)
            code = 1
        attempt['status'] = 'completed' if code == 0 and attempt.get('preservationPassed') else 'failed'
        if attempt['status'] != 'completed':
            code = 1
        attempt.update(exitCode=code, finishedUtc=utc(), wallSeconds=time.monotonic() - start,
                       cumulativeSupervisorSeconds=previous_wall + time.monotonic() - start,
                       supervisorPeakRssBytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        save(attempt_path, attempt, final=True)
    return code


if __name__ == '__main__':
    need(len(sys.argv) == 4, 'usage: run.py STAGE MANIFEST_SHA SOURCE_COMMIT')
    raise SystemExit(main(*sys.argv[1:]))
