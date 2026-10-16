"""One consumed frozen allocation; exact runtimes; actual child-group closure."""
import datetime
import hashlib
import importlib.metadata
import json
import os
import pathlib
import platform
import signal
import subprocess
import sys
import time

if sys.flags.optimize:
    raise RuntimeError('Nonoptimized Python required')
if len(sys.argv) != 5:
    raise RuntimeError('kind executable verified_manifest_sha published_commit')
p = pathlib.Path(__file__).resolve().parent.parent
repo = p.parent.parent
kind, executable, expected_sha, published_commit = sys.argv[1:]
if kind not in ('candidate', 'review'):
    raise RuntimeError('Unknown allocation')
out = p/'results'
out.mkdir(exist_ok=True)
with (out/(kind+'-invocation.lock')).open('x') as handle:
    handle.write('This sole invocation is consumed. Never remove or repeat.\n')
start = time.monotonic()
limits = dict(candidateWallSeconds=900, reviewWallSeconds=180, rssBytes=1610612736,
              scientificDirectoryBytes=218103808, supervisorLogsBytes=4194304)
cap = limits['candidateWallSeconds'] if kind == 'candidate' else limits['reviewWallSeconds']
rec = dict(kind=kind, sourceCommit=published_commit, sourceManifestSha256=expected_sha,
           startedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           wallCapSeconds=cap, rssCapBytes=limits['rssBytes'], sampledPeakRSSBytes=None,
           rssSamples=0, sampleIntervalSeconds=.1, monitorErrors=[], exitRaces=[],
           signals=[], returncode=None, closed=False, childGroupAbsent=None,
           performanceMeasurement=False, runtimeIdentityVerified=False,
           executionContext='frozen-center-screen-host', closureReserveBytes=1048576)
proc = None
pins = []
protected = {}


def check(ok, label):
    if not ok:
        raise RuntimeError(label)


def digest(file):
    h = hashlib.sha256()
    with file.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def files():
    return sorted(file for name in ('results', 'inputs', 'generation')
                  for file in (p/name).rglob('*') if file.is_file())


def storage():
    listing = files()
    total = sum(file.stat().st_size for file in listing)
    logs = sum(file.stat().st_size for file in listing
               if file.parent == out and file.name.endswith(('-stdout.txt', '-stderr.txt')))
    return total, logs


def guard_storage():
    total, logs = storage()
    check(total <= limits['scientificDirectoryBytes']-rec['closureReserveBytes'], 'scientific-directory-reserve-cap')
    check(logs <= limits['supervisorLogsBytes'], 'aggregate-log-cap')


def identity(file, expected):
    resolved = file.resolve(strict=True)
    return resolved.stat().st_size == expected['bytes'] and digest(resolved) == expected['sha256']


def group_absent():
    try:
        os.killpg(proc.pid, 0)
        return False
    except ProcessLookupError:
        return True


try:
    manifest = p/'source-manifest.json'
    check(digest(manifest) == expected_sha, 'source-manifest-hash')
    check(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, timeout=5).decode().strip() == published_commit, 'source-head')
    pins = json.loads(manifest.read_text())['files']
    required = {str((p/file).relative_to(repo)) for file in ('config.json', 'runtime.json', 'source/run.py', 'source/experiment.cjs', 'source/review.py')}
    check(required.issubset({pin['path'] for pin in pins}), 'critical-source-pins-missing')
    for pin in pins+[dict(path=str(manifest.relative_to(repo)), bytes=manifest.stat().st_size, sha256=expected_sha)]:
        file = repo/pin['path']
        data = file.read_bytes()
        check(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'local-source-pin')
        check(subprocess.check_output(['git', 'show', published_commit+':'+pin['path']], cwd=repo, timeout=5) == data, 'committed-source-pin')
        check(time.monotonic()-start <= cap, 'prelaunch-wall-cap')
    config = json.loads((p/'config.json').read_text())
    runtime = json.loads((p/'runtime.json').read_text())
    check(all(config['limits'].get(key) == value for key, value in limits.items()), 'fixed-supervisor-limits')
    check(sys.platform == runtime['platform'] and platform.machine() == runtime['architecture'], 'platform-identity')
    check(identity(pathlib.Path(sys.executable), runtime['python']) and sys.version == runtime['python']['version'], 'supervisor-python-identity')
    check(not os.environ.get('NODE_OPTIONS') and sys.flags.optimize == runtime['flags']['pythonOptimize'] == 0, 'forbidden-runtime-flags')
    distribution = importlib.metadata.distribution('numpy')
    record = distribution.read_text('RECORD')
    check(distribution.version == runtime['numpy']['version'] and record is not None and hashlib.sha256(record.encode('utf-8')).hexdigest() == runtime['numpy']['distributionRecordSha256'], 'numpy-distribution-identity')
    target = runtime['node'] if kind == 'candidate' else runtime['python']
    check(identity(pathlib.Path(executable), target), 'child-executable-identity')
    if kind == 'candidate':
        check(subprocess.check_output([executable, '--version'], timeout=5, text=True).strip() == target['version'], 'child-node-version')
    else:
        check(pathlib.Path(executable).resolve() == pathlib.Path(sys.executable).resolve(), 'review-python-process-identity')
        previous = json.loads((out/'candidate-run.json').read_text())
        check(previous.get('closed') is True and previous.get('childGroupAbsent') is True, 'candidate-not-closed')
        # Failed science may still be independently inspected; success remains a separate gate.
        rec['candidateSupervisorSuccess'] = previous.get('supervisorSuccess') is True
        protected = {str(file.relative_to(p)): digest(file) for file in files() if file.name != 'review-invocation.lock'}
    rec['runtimeIdentityVerified'] = True
    rec['runtime'] = runtime
    guard_storage()
    script = 'experiment.cjs' if kind == 'candidate' else 'review.py'
    command = [executable, str(p/'source'/script), str(p)]
    if kind == 'review':
        command.append(str(out/'independent-review.json'))
    with (out/(kind+'-stdout.txt')).open('xb') as stdout, (out/(kind+'-stderr.txt')).open('xb') as stderr:
        proc = subprocess.Popen(command, stdout=stdout, stderr=stderr, start_new_session=True)
        while proc.poll() is None:
            check(time.monotonic()-start <= cap, 'wall-cap')
            try:
                rss = int(subprocess.check_output(['/bin/ps', '-o', 'rss=', '-p', str(proc.pid)], stderr=subprocess.DEVNULL, text=True, timeout=2).strip() or 0)*1024
                check(rss > 0, 'nonpositive-rss')
                rec['rssSamples'] += 1
                rec['sampledPeakRSSBytes'] = max(rec['sampledPeakRSSBytes'] or 0, rss)
            except (ValueError, RuntimeError, subprocess.SubprocessError, OSError) as exc:
                if proc.poll() is not None:
                    rec['exitRaces'].append(type(exc).__name__)
                    break
                rec['monitorErrors'].append(type(exc).__name__)
                raise RuntimeError('rss-monitor-failed')
            check(rss <= limits['rssBytes'], 'rss-cap')
            guard_storage()
            time.sleep(.1)
        rec['returncode'] = proc.wait(timeout=3)
except BaseException as exc:
    rec['exception'] = dict(type=type(exc).__name__, reason=str(exc) if isinstance(exc, RuntimeError) else 'details-withheld-to-avoid-private-paths')
finally:
    if proc is None:
        rec['childGroupAbsent'] = True
    else:
        try:
            if proc.poll() is None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                    rec['signals'].append('SIGKILL')
                except ProcessLookupError:
                    rec['exitRaces'].append('kill-after-exit')
            rec['returncode'] = proc.wait(timeout=3)
            if not group_absent():
                os.killpg(proc.pid, signal.SIGKILL)
                rec['signals'].append('SIGKILL-residual-group')
                for _ in range(10):
                    if group_absent():
                        break
                    time.sleep(.05)
            rec['childGroupAbsent'] = group_absent()
        except BaseException as exc:
            rec['cleanupError'] = type(exc).__name__
    try:
        rec['protectedInputsUnchanged'] = bool(pins) and digest(p/'source-manifest.json') == expected_sha and all((repo/f['path']).is_file() and (repo/f['path']).stat().st_size == f['bytes'] and digest(repo/f['path']) == f['sha256'] for f in pins)
        rec['candidateOutputsUnchanged'] = all((p/name).is_file() and digest(p/name) == h for name, h in protected.items())
        rec['scientificBytesBeforeClosure'], rec['logBytes'] = storage()
        rec['artifacts'] = [dict(path=str(file.relative_to(p)), bytes=file.stat().st_size, sha256=digest(file)) for file in files()]
    except BaseException as exc:
        rec['finalizationError'] = type(exc).__name__
    rec['elapsedSeconds'] = time.monotonic()-start
    rec['closed'] = proc is None or (rec['returncode'] is not None and rec['childGroupAbsent'] is True)
    rec['supervisorSuccess'] = rec['returncode'] == 0 and rec['closed'] is True and rec['rssSamples'] > 0 and rec['runtimeIdentityVerified'] is True and not any(rec.get(k) for k in ('exception', 'cleanupError', 'finalizationError', 'monitorErrors', 'signals')) and rec.get('protectedInputsUnchanged') is True and rec.get('candidateOutputsUnchanged') is True and rec['elapsedSeconds'] <= cap and rec.get('logBytes', limits['supervisorLogsBytes']+1) <= limits['supervisorLogsBytes']

    def encode():
        return (json.dumps(rec, indent=2, allow_nan=False)+'\n').encode('utf-8')

    rec['elapsedSeconds'] = time.monotonic()-start
    if rec['elapsedSeconds'] > cap:
        rec['supervisorSuccess'] = False
        rec['finalWallCapExceeded'] = True
    # Re-encode after any status change, then check those exact immutable bytes.
    # An already exhausted cap still gets truthful, unqualified closure evidence.
    while True:
        payload = encode()
        fits = (len(payload) <= rec['closureReserveBytes'] and
                rec.get('scientificBytesBeforeClosure', limits['scientificDirectoryBytes'])+len(payload)
                <= limits['scientificDirectoryBytes'])
        if fits or (rec.get('finalStorageCapExceeded') is True and rec['supervisorSuccess'] is False):
            break
        rec['supervisorSuccess'] = False
        rec['finalStorageCapExceeded'] = True
    with (out/(kind+'-run.json')).open('xb') as handle:
        handle.write(payload)
print(json.dumps({k:rec[k] for k in ('kind', 'supervisorSuccess', 'closed', 'returncode', 'elapsedSeconds', 'sampledPeakRSSBytes', 'childGroupAbsent')}))
sys.exit(0 if rec['supervisorSuccess'] else 1)
