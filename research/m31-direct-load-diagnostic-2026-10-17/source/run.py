"""Exclusive bounded oracle-assisted direct-load diagnostic dispatch. No scientific modules imported."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import os
import resource
import signal
import sys
import time

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
LIMIT = 16 * 1024 * 1024


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def write(path, value, exclusive=True):
    payload = (json.dumps(value, separators=(',', ':'), allow_nan=False) + '\n').encode()
    if len(payload) > LIMIT:
        raise ValueError('output-byte-limit')
    target = path if exclusive else path.with_name(path.name + '.final.tmp')
    with target.open('xb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if not exclusive:
        os.replace(target, path)
    descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def timeout(signum, frame):
    raise TimeoutError('registered-time-limit')


def main():
    stage, expected, commit = sys.argv[1:]
    if stage not in ('analyze', 'check') or len(expected) != 64 or len(commit) != 40 or any(c not in '0123456789abcdef' for c in expected + commit):
        raise ValueError('dispatch-arguments')
    result_dir = PACKAGE / 'results'
    result_dir.mkdir(exist_ok=True)
    attempt_path = result_dir / (stage + '-attempt.json')
    attempt = {'schema': 'm31-direct-load-attempt-v1', 'stage': stage,
               'sourceCommit': commit, 'sourceManifestSha256': expected,
               'startedUtc': utc(), 'status': 'started', 'firstFailure': None,
               'dispatchContextAttestation': os.environ.get('RESEARCH_EXECUTION_CONTEXT'),
               'resourceLimits': {'wallSeconds': 180, 'cpuSoftSeconds': 120,
                   'cpuHardSeconds': 121, 'peakRssAcceptanceBytes': 536870912, 'perOutputBytes': LIMIT},
               'resourceScope': 'Single process. CPU/time/output limits enforced. Peak RSS is a post-output acceptance observation, not an enforced memory ceiling; final attempt-report overhead is excluded.'}
    write(attempt_path, attempt)
    start = time.monotonic()
    exit_code = 1
    try:
        if datetime.datetime.now(datetime.timezone.utc) >= datetime.datetime.fromisoformat('2026-10-17T02:00:00+00:00'):
            raise ValueError('launch-cutoff')
        if attempt['dispatchContextAttestation'] != 'tool-require-escalated':
            raise ValueError('explicit-dispatch-attestation-required')
        if sys.platform != 'darwin':
            raise ValueError('registered-platform-requires-darwin-rss-units')
        resource.setrlimit(resource.RLIMIT_CPU, (120, 121))
        resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT, LIMIT))
        signal.signal(signal.SIGALRM, timeout)
        signal.signal(signal.SIGXCPU, timeout)
        signal.alarm(180)
        manifest_bytes = (PACKAGE / 'source-manifest.json').read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != expected:
            raise ValueError('source-manifest-identity')
        manifest = json.loads(manifest_bytes)
        for pin in manifest['files']:
            path = ROOT / pin['path']
            if path.stat().st_size != pin['bytes']:
                raise ValueError('source-pin-size:' + pin['path'])
            if hashlib.sha256(path.read_bytes()).hexdigest() != pin['sha256']:
                raise ValueError('source-pin-digest:' + pin['path'])
        runtime = manifest['runtime']
        runtime_bytes = Path(sys.executable).read_bytes()
        if len(runtime_bytes) != runtime['bytes'] or hashlib.sha256(runtime_bytes).hexdigest() != runtime['sha256']:
            raise ValueError('runtime-identity')
        attempt['verifiedPins'] = len(manifest['files'])
        publication = json.loads((PACKAGE / 'source-publication.json').read_text())
        if (publication.get('commit') != commit or publication.get('manifestSha256') != expected
                or publication.get('manifestPath') != str((PACKAGE / 'source-manifest.json').relative_to(ROOT))
                or publication.get('manifestBytes') != len(manifest_bytes)
                or publication.get('verifiedFilePins') != len(manifest['files'])
                or publication.get('remoteBytesEqualLocal') is not True
                or publication.get('committedBytesEqualLocal') is not True
                or datetime.datetime.fromisoformat(publication['verifiedUtc']) > datetime.datetime.fromisoformat(attempt['startedUtc'])):
            raise ValueError('source-publication-binding')
        if stage == 'check':
            old = json.loads((result_dir / 'analyze-attempt.json').read_text())
            if (old.get('schema') != 'm31-direct-load-attempt-v1' or old.get('stage') != 'analyze'
                    or old.get('status') != 'completed' or old.get('sourceCommit') != commit
                    or old.get('sourceManifestSha256') != expected or old.get('exitCode') != 0
                    or old.get('firstFailure') is not None or old.get('verifiedPins') != len(manifest['files'])):
                raise ValueError('analysis-completion-binding')
            prior_bytes = (result_dir / 'analyze.json').read_bytes()
            if len(prior_bytes) != old.get('outputBytes') or hashlib.sha256(prior_bytes).hexdigest() != old['outputSha256']:
                raise ValueError('analysis-output-binding')
        spec = importlib.util.spec_from_file_location('bounded_' + stage, PACKAGE / 'source' / (stage + '.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        value = module.run(ROOT)
        path = result_dir / (stage + '.json')
        write(path, value)
        attempt.update(status='completed', outputSha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                       outputBytes=path.stat().st_size)
        if stage == 'check' and value.get('passed') is not True:
            raise ValueError('saved-data-check-failed')
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 536870912:
            raise ValueError('observed-peak-rss-acceptance-gate')
        exit_code = 0
    except Exception as exc:
        # Fixed error messages and relative pinned paths; no traceback/private paths.
        attempt['status'] = 'failed'
        message = str(exc).replace(str(ROOT), 'REPOSITORY').replace(str(Path(sys.executable).parent), 'PYTHON_RUNTIME')
        attempt['firstFailure'] = {'type': type(exc).__name__, 'message': message[:512]}
    finally:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        attempt.update(finishedUtc=utc(), wallSeconds=time.monotonic() - start,
                       userSeconds=usage.ru_utime, systemSeconds=usage.ru_stime,
                       peakRssBytes=usage.ru_maxrss, exitCode=exit_code)
        write(attempt_path, attempt, exclusive=False)
        signal.alarm(0)
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
