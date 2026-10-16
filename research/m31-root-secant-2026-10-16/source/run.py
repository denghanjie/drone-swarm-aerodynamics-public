"""One bounded serial invocation per kind; no retries or silent repairs."""
import datetime
import hashlib
import json
import os
import pathlib
import signal
import subprocess
import sys
import time

if sys.flags.optimize:
    raise RuntimeError('Nonoptimized Python required')
p = pathlib.Path(__file__).resolve().parent.parent
repo = p.parent.parent
kind, interpreter, expected_sha, published_commit = sys.argv[1:]
if kind not in ('candidate', 'review'):
    raise ValueError('Unknown allocation')
out = p/'results'
out.mkdir(exist_ok=True)
cfg = json.loads((p/'config.json').read_text())
lim = cfg['limits']
phase_results_cap = lim['candidateResultsBytes'] if kind == 'candidate' else lim['resultsBytes']
with (out/(kind+'-invocation.lock')).open('x') as f:
    f.write('This sole invocation is consumed. Never remove or repeat.\n')
start = time.monotonic()
rec = dict(kind=kind, sourceCommit=published_commit, sourceManifestSha256=expected_sha,
           startedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), wallCapSeconds=lim['wallSeconds'], rssCapBytes=lim['rssBytes'],
           sampledPeakRSSBytes=None, rssSamples=0, sampleIntervalSeconds=.1, monitorErrors=[], exitRaces=[], signals=[], returncode=None,
           performanceMeasurement=False, closed=False, childGroupAbsent=None, inheritedInputCopied=False)
proc = None
pins = []
protected = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(path):
    return sorted(f for f in path.rglob('*') if f.is_file())


def total(path):
    return sum(f.stat().st_size for f in files(path))


def check(ok, label):
    if not ok:
        raise RuntimeError(label)


def storage_guard():
    check(total(out) <= phase_results_cap-lim['closureReserveBytes'], 'results-reserve-cap')
    check(total(p) <= lim['packageBytes']-lim['closureReserveBytes'], 'package-reserve-cap')
    check(sum(f.stat().st_size for f in files(out) if f.name.endswith(('-stdout.txt','-stderr.txt'))) <= lim['logsBytes'], 'aggregate-log-cap')


try:
    manifest = p/'source-manifest.json'
    check(digest(manifest) == expected_sha, 'source-manifest-hash')
    check(subprocess.check_output(['git','rev-parse','HEAD'], cwd=repo, timeout=5).decode().strip() == published_commit, 'source-head')
    pins = json.loads(manifest.read_text())['files']
    for pin in pins+[dict(path=str(manifest.relative_to(repo)), bytes=manifest.stat().st_size, sha256=expected_sha)]:
        path = repo/pin['path']
        b = path.read_bytes()
        check(len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256'], 'local-pin')
        check(subprocess.check_output(['git','show',published_commit+':'+pin['path']],cwd=repo,timeout=5) == b, 'committed-pin')
        check(time.monotonic()-start < lim['wallSeconds'], 'prelaunch-wall-cap')
    if kind == 'review':
        previous = json.loads((out/'candidate-run.json').read_text())
        check(previous['supervisorSuccess'] is True and previous['closed'] is True, 'candidate-closure-not-qualified')
        protected = {str(f.relative_to(out)): digest(f) for f in files(out) if not f.name.startswith('review-')}
    storage_guard()
    script = 'candidate.py' if kind == 'candidate' else 'review.py'
    with (out/(kind+'-stdout.txt')).open('xb') as stdout, (out/(kind+'-stderr.txt')).open('xb') as stderr:
        proc = subprocess.Popen([interpreter, str(p/'source'/script), str(p)], stdout=stdout, stderr=stderr, start_new_session=True)
        while proc.poll() is None:
            check(time.monotonic()-start <= lim['wallSeconds'], 'wall-cap')
            try:
                sample = int(subprocess.check_output(['/bin/ps','-o','rss=','-p',str(proc.pid)], stderr=subprocess.DEVNULL, text=True, timeout=2).strip() or 0)*1024
                check(sample > 0, 'nonpositive-rss')
                rec['rssSamples'] += 1
                rec['sampledPeakRSSBytes'] = max(rec['sampledPeakRSSBytes'] or 0, sample)
            except (ValueError, RuntimeError, subprocess.SubprocessError, OSError) as exc:
                if proc.poll() is not None:
                    rec['exitRaces'].append(type(exc).__name__)
                    break
                rec['monitorErrors'].append(type(exc).__name__)
                raise RuntimeError('rss-monitor-failed')
            check(sample <= lim['rssBytes'], 'rss-cap')
            storage_guard()
            time.sleep(.1)
        rec['returncode'] = proc.wait(timeout=3)
except BaseException as exc:
    rec['exception'] = dict(type=type(exc).__name__, reason=str(exc) if isinstance(exc, RuntimeError) else 'details-withheld-to-avoid-private-paths')
finally:
    if proc is not None:
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
                rec['signals'].append('SIGKILL')
            except ProcessLookupError:
                rec['exitRaces'].append('kill-after-exit')
            except BaseException as exc:
                rec['cleanupError'] = type(exc).__name__
        try:
            rec['returncode'] = proc.wait(timeout=3)
            try:
                os.killpg(proc.pid, 0)
                rec['childGroupAbsent'] = False
                os.killpg(proc.pid, signal.SIGKILL)
                rec['signals'].append('SIGKILL-residual-group')
            except ProcessLookupError:
                rec['childGroupAbsent'] = True
        except BaseException as exc:
            rec['cleanupError'] = type(exc).__name__
    else:
        rec['childGroupAbsent'] = True
    rec['artifacts'] = []
    try:
        rec['protectedInputsUnchanged'] = bool(pins) and digest(p/'source-manifest.json') == expected_sha and all((repo/f['path']).is_file() and (repo/f['path']).stat().st_size == f['bytes'] and digest(repo/f['path']) == f['sha256'] for f in pins)
        rec['candidateOutputsUnchanged'] = all((out/s).is_file() and digest(out/s) == h for s,h in protected.items())
        rec['resultsBytesBeforeClosure'] = total(out)
        rec['packageBytesBeforeClosure'] = total(p)
        rec['logBytes'] = sum(f.stat().st_size for f in files(out) if f.name.endswith(('-stdout.txt','-stderr.txt')))
        for f in files(out):
            rec['artifacts'].append(dict(path=str(f.relative_to(p)), bytes=f.stat().st_size, sha256=digest(f)))
    except BaseException as exc:
        rec['finalizationError'] = type(exc).__name__
    rec['elapsedSeconds'] = time.monotonic()-start
    rec['closed'] = True
    rec['supervisorSuccess'] = rec['returncode'] == 0 and rec['childGroupAbsent'] is True and rec['rssSamples'] > 0 and not any(rec.get(k) for k in ('exception','cleanupError','finalizationError','monitorErrors','signals')) and rec.get('protectedInputsUnchanged') is True and rec.get('candidateOutputsUnchanged') is True and rec['elapsedSeconds'] <= lim['wallSeconds'] and rec.get('logBytes', lim['logsBytes']+1) <= lim['logsBytes']
    def encode():
        return (json.dumps(rec, indent=2, allow_nan=False)+'\n').encode()
    payload = encode()
    rec['elapsedSeconds'] = time.monotonic()-start
    if rec['elapsedSeconds'] > lim['wallSeconds']:
        rec['supervisorSuccess'] = False
        rec['finalWallCapExceeded'] = True
    payload = encode()
    if len(payload) > lim['closureReserveBytes'] or rec.get('resultsBytesBeforeClosure',phase_results_cap)+len(payload) > phase_results_cap or rec.get('packageBytesBeforeClosure',lim['packageBytes'])+len(payload) > lim['packageBytes']:
        rec['supervisorSuccess'] = False
        rec['finalStorageCapExceeded'] = True
        payload = encode()
    with (out/(kind+'-run.json')).open('xb') as f:
        f.write(payload)
print(json.dumps({k:rec[k] for k in ('kind','supervisorSuccess','closed','returncode','elapsedSeconds','sampledPeakRSSBytes','childGroupAbsent')}))
sys.exit(0 if rec['supervisorSuccess'] else 1)
