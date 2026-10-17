"""Single-use, single-child saved audit supervisor. No scientific imports.

The sole child is the isolated Python audit wrapper. It creates no descendants.
Only its retained Popen handle is waited/killed/reaped; no process-group signals.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import subprocess
import sys
import time

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
NAME = 'research/m31-native-saved-audit-2026-10-17'
FILE_LIMIT = 32 * 1024 * 1024
TOTAL_LIMIT = 96 * 1024 * 1024
ATTEMPT_LIMIT = 1024 * 1024


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def need(value, code):
    if not value:
        raise ValueError(code)


def public_error(error):
    message = str(error).replace(str(ROOT), 'REPOSITORY').replace(str(Path.home()), '[HOME]')
    return {'type': type(error).__name__, 'message': message[:512]}


def identity(path):
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
            size += len(block)
    return {'bytes': size, 'sha256': digest.hexdigest()}


def verify(pin):
    path = (ROOT / pin['path']).resolve()
    need(not Path(pin['path']).is_absolute() and path.is_relative_to(ROOT), 'pin-path')
    need(identity(path) == {k: pin[k] for k in ('bytes', 'sha256')}, 'pin:' + pin['path'])
    return path


def read_json(path):
    need(path.stat().st_size <= FILE_LIMIT, 'json-size')
    return json.loads(path.read_bytes())


def save_attempt(path, value, final=False):
    data = (json.dumps(value, allow_nan=False, separators=(',', ':')) + '\n').encode()
    need(len(data) <= ATTEMPT_LIMIT, 'attempt-byte-limit')
    target = path.with_name(path.name + '.final.tmp') if final else path
    with target.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if final:
        os.replace(target, path)


def child_limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (FILE_LIMIT, FILE_LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 121))


def publication_binding(receipt, commit, manifest_sha, manifest_bytes, manifest_path, count, latest):
    need(receipt['commit'] == commit and receipt['manifestSha256'] == manifest_sha
         and receipt['manifestBytes'] == manifest_bytes and receipt['manifestPath'] == manifest_path
         and receipt['verifiedFilePins'] == count and receipt['remoteBytesEqualLocal'] is True
         and receipt['committedBytesEqualLocal'] is True
         and datetime.datetime.fromisoformat(receipt['verifiedUtc']) <= datetime.datetime.fromisoformat(latest),
         'publication-binding')


def main(expected, commit):
    need(PACKAGE == ROOT / NAME, 'supervisor-location')
    need(len(expected) == 64 and len(commit) == 40 and
         all(c in '0123456789abcdef' for c in expected + commit), 'identity-arguments')
    results = PACKAGE / 'results'
    results.mkdir(exist_ok=True)
    attempt_path = results / 'check-attempt.json'
    attempt = {'schema': 'm31-native-saved-audit-attempt-v1', 'stage': 'saved-check',
               'sourceManifestSha256': expected, 'sourceCommit': commit, 'startedUtc': utc(),
               'status': 'started', 'firstFailure': None, 'originalSupervisorStatus': 'failed',
               'originalSupervisorRepaired': False,
               'scope': 'saved-record numerical consistency only; original launch/cleanup compliance stays failed',
               'resourceScope': 'One Python child; 120 s child wall, 120/121 s child CPU, 32 MiB per child-written file, 96 MiB new evidence/log total; no enforced memory ceiling. Up to 5 s bounded child kill/reap cleanup is separately recorded. Wall deadline requires a live supervisor; per-process CPU/file limits survive parent loss.',
               'dispatchContextAttestation': os.environ.get('RESEARCH_EXECUTION_CONTEXT')}
    # Exclusive acquisition is outside the failure-finalization block. A repeated
    # invocation cannot replace an earlier attempt or create its output files.
    save_attempt(attempt_path, attempt)
    started = time.monotonic()
    process, log_path, pins, config = None, None, [], None
    protected, code = {}, 1
    try:
        need(attempt['dispatchContextAttestation'] == 'tool-require-escalated', 'dispatch-attestation')
        need(sys.platform == 'darwin', 'darwin-runtime')
        cutoff = datetime.datetime.fromisoformat('2026-10-17T03:00:00+00:00')
        need(datetime.datetime.now(datetime.timezone.utc) < cutoff, 'launch-cutoff')
        manifest_path = PACKAGE / 'source-manifest.json'
        manifest_id = identity(manifest_path)
        need(manifest_id['sha256'] == expected, 'source-manifest-sha')
        manifest = read_json(manifest_path)
        pins = manifest['files']
        by_path = {pin['path']: pin for pin in pins}
        need(len(by_path) == len(pins), 'duplicate-source-pin')
        for pin in pins:
            verify(pin)
        for relative in ('source/run.py', 'source/audit.py', 'config.json'):
            need(NAME + '/' + relative in by_path, 'saved-audit-source-closure')
        config = read_json(PACKAGE / 'config.json')
        need(config['schema'] == 'm31-native-saved-audit-config-v1', 'config-schema')
        need(config['limits'] == {'childWallSeconds': 120, 'childCpuSoftSeconds': 120,
             'childCpuHardSeconds': 121, 'perFileBytes': FILE_LIMIT, 'combinedBytes': TOTAL_LIMIT,
             'cleanupWaitSeconds': 5} and config['launchCutoffUtc'] == '2026-10-17T03:00:00+00:00',
             'fixed-resource-contract')
        python_pin = config['runtime']['python']
        need(manifest['runtime']['python'] == python_pin
             and identity(Path(sys.executable).resolve()) == {k: python_pin[k] for k in ('bytes', 'sha256')},
             'pinned-python-runtime')
        for key in ('originalManifest', 'originalPublication', 'originalChecker',
                    'originalBrowserOutput', 'originalFailedAttempt', 'originalJournal'):
            pin = config[key]
            need(by_path.get(pin['path']) == pin, 'saved-input-manifest-binding:' + key)
            verify(pin)
        original = read_json(ROOT / config['originalManifest']['path'])
        for pin in original['files']:
            need(by_path.get(pin['path']) == pin, 'original-full-closure-binding')
            verify(pin)
        need(any(pin == config['originalChecker'] for pin in original['files']), 'original-checker-binding')
        old_attempt = read_json(ROOT / config['originalFailedAttempt']['path'])
        need(old_attempt['status'] == 'failed' and old_attempt['exitCode'] == 1
             and old_attempt['childExitCode'] == 0 and old_attempt['cleanupError'] is True
             and old_attempt['firstFailure']['type'] == 'PermissionError'
             and old_attempt['sourceCommit'] == config['originalSourceCommit']
             and old_attempt['sourceManifestSha256'] == config['originalManifest']['sha256'],
             'original-failed-stage-binding')
        original_receipt = read_json(ROOT / config['originalPublication']['path'])
        publication_binding(original_receipt, config['originalSourceCommit'], config['originalManifest']['sha256'],
                            config['originalManifest']['bytes'], config['originalManifest']['path'],
                            len(original['files']), old_attempt['startedUtc'])
        publication = read_json(PACKAGE / 'source-publication.json')
        publication_binding(publication, commit, expected, manifest_id['bytes'], NAME + '/source-manifest.json',
                            len(manifest['files']), attempt['startedUtc'])
        protected = {NAME + '/source-manifest.json': manifest_id,
                     NAME + '/source-publication.json': identity(PACKAGE / 'source-publication.json')}
        for relative in config['originalMustRemainAbsent']:
            need(not (ROOT / relative).exists(), 'original-checker-already-launched')
        need(not (results / 'check.json').exists(), 'new-audit-output-already-exists')
        attempt.update(verifiedPins=len(pins), originalSourceCommit=config['originalSourceCommit'],
                       originalSourceManifestSha256=config['originalManifest']['sha256'],
                       originalBrowserOutput=config['originalBrowserOutput'],
                       originalFailedAttempt=config['originalFailedAttempt'])
        private = Path(os.environ['RESEARCH_PRIVATE_LOG_DIR'])
        need(private.is_absolute() and not private.resolve().is_relative_to(ROOT), 'private-log-location')
        private.mkdir(parents=True, exist_ok=True)
        log_path = private / 'saved-check.log'
        command = [str(Path(sys.executable).resolve()), '-I', '-B', str(PACKAGE / 'source/audit.py'),
                   str(ROOT), expected, commit]
        environment = {'PATH': os.defpath, 'RESEARCH_EXECUTION_CONTEXT': 'tool-require-escalated'}
        need(datetime.datetime.now(datetime.timezone.utc) < cutoff, 'pre-spawn-launch-cutoff')
        with log_path.open('xb') as log:
            process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log,
                                       stderr=subprocess.STDOUT, env=environment, preexec_fn=child_limits)
            child_started = time.monotonic()
            try:
                child_code = process.wait(timeout=120)
            except subprocess.TimeoutExpired:
                attempt['timedOut'] = True
                attempt['childWallSeconds'] = time.monotonic() - child_started
                cleanup_started = time.monotonic()
                process.kill()  # The specific live Popen child, never a PID group.
                attempt['childExitCode'] = process.wait(timeout=5)
                attempt['cleanupSeconds'] = time.monotonic() - cleanup_started
                attempt['childReaped'] = True
                process = None
                raise TimeoutError('checker-child-wall-deadline')
            attempt['childWallSeconds'] = time.monotonic() - child_started
            attempt['childExitCode'] = child_code
            attempt['childReaped'] = True
            process = None
        need(child_code == 0, 'checker-child-exit')
        output_path = results / 'check.json'
        need(output_path.stat().st_size <= FILE_LIMIT, 'output-byte-limit')
        output = read_json(output_path)
        need(output['schema'] == 'm31-native-load-check-v1' and output['passed'] is True
             and output['decision'] in ('qualified', 'unqualified'), 'checker-report-integrity')
        need([x['id'] for x in output['arithmeticFixtures']] == config['expectedArithmeticFixtureIds']
             and all(x['passed'] is True for x in output['arithmeticFixtures']), 'arithmetic-fixture-pass-assertions')
        need([x['id'] for x in output['corruptionChecks']] == config['expectedCorruptionIds']
             and all(x['passed'] is True for x in output['corruptionChecks']), 'corruption-pass-assertions')
        audit = output['savedEvidenceAudit']
        need(audit['auditSourceCommit'] == commit and audit['auditSourceManifestSha256'] == expected
             and audit['originalSupervisorStatus'] == 'failed' and audit['originalSupervisorRepaired'] is False
             and audit['originalCheckerMainUsedUnchanged'] is True
             and audit['fixtureAssertionsPassed'] is True and audit['corruptionAssertionsPassed'] is True
             and audit['launchCleanupComplianceClaim'] is False, 'saved-audit-provenance')
        attempt.update(outputBytes=output_path.stat().st_size, outputSha256=identity(output_path)['sha256'],
                       recordNumericalDecision=output['decision'])
        code = 0
    except Exception as error:
        attempt['firstFailure'] = public_error(error)
    finally:
        if process is not None:
            cleanup_started = time.monotonic()
            try:
                if process.poll() is None:
                    process.kill()
                attempt['childExitCode'] = process.wait(timeout=5)
                attempt['childReaped'] = True
            except Exception as error:
                attempt['cleanupError'] = type(error).__name__
                code = 1
            attempt['cleanupSeconds'] = time.monotonic() - cleanup_started
        # Preservation is checked on failure too; it never repairs the original
        # failed attempt. Only the new package's result files may be created.
        try:
            for pin in pins:
                verify(pin)
            for relative, expected_pin in protected.items():
                need(identity(ROOT / relative) == expected_pin, 'postrun-protected:' + relative)
            if config is not None:
                for relative in config['originalMustRemainAbsent']:
                    need(not (ROOT / relative).exists(), 'original-checker-artifact-created')
            attempt['preservationPassed'] = bool(pins and protected)
            if log_path is not None and log_path.exists():
                log_id = identity(log_path)
                need(log_id['bytes'] <= FILE_LIMIT, 'private-log-byte-limit')
                attempt['privateLog'] = dict(log_id, published=False)
            # Reserve two 1 MiB attempt copies during atomic finalization; all
            # other new result files and the private child log count in 96 MiB.
            result_bytes = sum(p.stat().st_size for p in results.rglob('*') if p.is_file())
            log_bytes = log_path.stat().st_size if log_path is not None and log_path.exists() else 0
            need(result_bytes + log_bytes + 2 * ATTEMPT_LIMIT <= TOTAL_LIMIT, 'combined-new-evidence-limit')
            attempt['newEvidenceAndLogBytesBeforeFinalization'] = result_bytes + log_bytes
        except Exception as error:
            attempt['preservationOrOutputLimitFailure'] = public_error(error)
            code = 1
        attempt['status'] = 'completed' if code == 0 and attempt.get('preservationPassed') else 'failed'
        if attempt['status'] != 'completed':
            code = 1
        attempt.update(finishedUtc=utc(), wallSeconds=time.monotonic() - started,
                       supervisorPeakRssBytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, exitCode=code)
        save_attempt(attempt_path, attempt, final=True)
    return code


if __name__ == '__main__':
    need(len(sys.argv) == 3, 'usage: run.py AUDIT_MANIFEST_SHA AUDIT_SOURCE_COMMIT')
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
