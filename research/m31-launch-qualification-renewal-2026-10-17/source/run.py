"""One-shot harmless qualification. No scientific code imports."""
import hashlib
import json
import os
import re
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

package = Path(__file__).resolve().parents[1]
root = package.parents[1]
results = package / 'results'
config = json.loads((package / 'source/config.json').read_text())
cutoff = datetime.fromisoformat(config['cutoffUtc'].replace('Z', '+00:00')).timestamp()

def sha(b): return hashlib.sha256(b).hexdigest()
def write(p, obj):
    data = (json.dumps(obj, indent=2, allow_nan=False) + '\n').encode()
    if len(data) > 65536: raise RuntimeError('report-size')
    with p.open('xb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
def pin(p):
    b = p.read_bytes()
    return {'path': p.relative_to(root).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
def gate():
    if time.time() >= cutoff: raise RuntimeError('launch-cutoff')
def clean(s):
    return str(s).replace(str(root), 'REPOSITORY_ROOT').replace(str(Path.home()), 'USER_HOME')[:1024]
def bound():
    total = 0
    for p in results.rglob('*'):
        if p.is_symlink(): raise RuntimeError('symlink-output')
        if p.is_file():
            n = p.stat().st_size; total += n
            cap = 32768 if p.suffix in {'.log', '.jsonl'} else 65536
            if n > cap: raise RuntimeError('file-budget')
    if total > 1048576: raise RuntimeError('output-budget')
def deadline(_s, _f): raise TimeoutError('run-deadline')

class ProbeError(Exception):
    def __init__(self, kind, detail): self.kind, self.detail = kind, detail

def probe(mode=None):
    if mode == 'sampler-nonzero':
        code, out, err = 13, '', 'INJECTED process inspection failure'
    elif mode == 'sampler-malformed':
        code, out, err = 0, 'INJECTED MALFORMED ROW\n', ''
    else:
        try:
            cp = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid=,pgid=,rss='], capture_output=True, text=True, timeout=0.5)
            code, out, err = cp.returncode, cp.stdout, cp.stderr
        except Exception as e:
            raise ProbeError('sampler-exception', {'operation':'process-sample','command':['/bin/ps','-axo','pid=,ppid=,pgid=,rss='],'timeoutSeconds':0.5,'exception': type(e).__name__, 'message': clean(e), 'injected': False})
    detail = {'operation': 'process-sample', 'returnCode': code, 'stderr': clean(err), 'injected': mode is not None}
    if code != 0: raise ProbeError('sampler-nonzero', detail)
    rows = []
    for line in out.splitlines():
        if not line.strip(): continue
        try:
            tokens = line.split()
            if len(tokens) != 4 or any(re.fullmatch(r'[0-9]+', x) is None for x in tokens): raise ValueError('malformed-numeric-row')
            row = tuple(map(int, tokens))
        except ValueError as e:
            detail.update({'exception': 'ValueError', 'offendingRow': clean(line) if mode else '[redacted numeric process row]', 'message': str(e)[:128]})
            raise ProbeError('sampler-malformed', detail)
        rows.append(row)
    return rows

def main():
    gate()
    if not sys.flags.isolated or not sys.dont_write_bytecode: raise RuntimeError('isolated-runtime-required')
    if os.environ.get('RESEARCH_EXECUTION_CONTEXT') != config['executionContext']: raise RuntimeError('execution-context-required')
    exe = Path(sys.executable).resolve(); eb = exe.read_bytes()
    if {'bytes': len(eb), 'sha256': sha(eb)} != config['runtime']: raise RuntimeError('runtime-pin')
    manifest_bytes = (package / 'source-manifest.json').read_bytes(); manifest = json.loads(manifest_bytes)
    publication = json.loads((package / 'source-publication.json').read_text())
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if publication['commit'] != commit or publication['manifestSha256'] != sha(manifest_bytes) or not publication['remoteBytesEqualLocal'] or not publication['committedBytesEqualLocal']: raise RuntimeError('publication-binding')
    for p in manifest['files']:
        b = (root / p['path']).read_bytes()
        if len(b) != p['bytes'] or sha(b) != p['sha256']: raise RuntimeError('source-pin')
    results.mkdir()
    shared = {'supervisorPid':os.getpid(),'supervisorPgid':os.getpgrp(),'configSha256':sha((package/'source/config.json').read_bytes()),'sourceCommit': commit, 'sourceManifestSha256': sha(manifest_bytes), 'runtime': config['runtime'], 'executionContext': config['executionContext'], 'executionContextEvidence': 'Caller attestation via environment variable; tool invocation retained outside package. Not a sandbox detector.'}
    write(results / 'attempt.json', {**shared, 'startedUtc': datetime.now(timezone.utc).isoformat(), 'soleAttempt': True})
    signal.signal(signal.SIGALRM, deadline); signal.alarm(60)
    reports = []; start = time.monotonic(); fatal = None
    try:
        for case in config['cases']:
            gate(); bound()
            if time.monotonic() - start > 58: raise TimeoutError('run-deadline-before-case')
            folder = results / case; folder.mkdir()
            r = {'case': case, **shared, 'firstFailure': None, 'secondaryFailures': [], 'samples': 0, 'peakSampledGroupRssBytes': 0, 'authorization': None, 'events': [], 'closureProbes': [], 'closed': False, 'normalRelease': False}
            t0 = time.monotonic(); r['startedMonotonicNs'] = time.monotonic_ns(); g = None; authorization_time = None; released = False
            def fail(kind, **detail):
                if r['firstFailure'] is None: r['firstFailure'] = {'kind': kind, **detail}
                else: r['secondaryFailures'].append({'kind': kind, **detail})
            try:
                if case == 'capability':
                    rows = probe(); own = [x for x in rows if x[0] == os.getpid()]
                    if len(own) != 1 or own[0][2] != os.getpgrp() or own[0][3] <= 0: raise RuntimeError('capability-own-pid-missing')
                    r['capabilityObservation'] = dict(zip(['pid','ppid','pgid','rssKiB'],own[0]));r['samples'] = 1;r['closed'] = True
                    r['peakSampledGroupRssBytes'] = own[0][3]*1024
                    if r['peakSampledGroupRssBytes'] > 134217728: raise RuntimeError('rss-limit')
                    write(folder / 'inert-output.json', {'case': case, 'capability': True})
                else:
                    with (folder/'stdout.log').open('xb') as out, (folder/'stderr.log').open('xb') as err:
                        g = subprocess.Popen([str(exe),'-I','-B',str(package/'source/guard.py'),case,str(folder)],stdin=subprocess.PIPE,stdout=out,stderr=err,text=True,start_new_session=True)
                        r['guardianPid'] = g.pid
                        while True:
                            if time.monotonic() - start > 58: raise TimeoutError('run-deadline')
                            if time.monotonic() - t0 > 4: raise TimeoutError('case-deadline')
                            bound()
                            ep = folder/'events.jsonl'
                            events = []
                            if ep.exists():
                                for line in ep.read_text().splitlines():
                                    try: events.append(json.loads(line))
                                    except json.JSONDecodeError: pass # May observe a writer's partial final line.
                            r['events'] = events
                            if g.poll() is not None:
                                fail('guardian-exit-before-release', exitCode=g.returncode);break
                            rows = probe(); group = [x for x in rows if x[2] == g.pid]
                            r['samples'] += 1;r['peakSampledGroupRssBytes'] = max(r['peakSampledGroupRssBytes'],sum(x[3]*1024 for x in group))
                            if r['peakSampledGroupRssBytes'] > 134217728: raise RuntimeError('rss-limit')
                            if len(group) > 2: raise RuntimeError('unexpected-group-size')
                            ready = next((e for e in events if e['event'] == 'ready'), None)
                            if ready and r['authorization'] is None:
                                if ready['pid'] != g.pid or ready['pgid'] != g.pid or not any(x[0] == g.pid for x in group): raise RuntimeError('guardian-not-observed')
                                leader = next(x for x in group if x[0] == g.pid)
                                if leader[1] != os.getpid() or leader[3] <= 0: raise RuntimeError('leader-sample-not-qualified')
                                r['leaderObservation'] = {**dict(zip(['pid','ppid','pgid','rssKiB'],leader)), 'monotonicNs':time.monotonic_ns()}
                                if case in {'sampler-nonzero','sampler-malformed'}: probe(case)
                                gate();r['authorization'] = {'guardianPid': g.pid, 'monotonicNs': time.monotonic_ns(), 'leaderSampleObserved': True, 'leaderObservation': r['leaderObservation']}
                                write(folder/'authorization.json',r['authorization']);g.stdin.write('start\n');g.stdin.flush();authorization_time = time.monotonic()
                            if case == 'child-timeout' and authorization_time and time.monotonic()-authorization_time > 0.3:
                                fail('child-timeout', deadlineSeconds=0.3, monotonicNs=time.monotonic_ns());break
                            child_exit = next((e for e in events if e['event'] == 'child-exit'),None)
                            if child_exit:
                                if child_exit['exitCode'] != 0: fail('child-exit', exitCode=child_exit['exitCode'])
                                if any(x[0] != g.pid for x in group): raise RuntimeError('child-still-observed')
                                r['releaseObservation'] = {'monotonicNs':time.monotonic_ns(),'groupRows':[list(x) for x in group]}
                                g.stdin.write('release\n');g.stdin.flush();g.wait(timeout=0.5);released=True;r['normalRelease']=g.returncode==0;break
                            time.sleep(0.01)
            except ProbeError as e: fail(e.kind, **e.detail)
            except Exception as e: fail('supervisor-exception', exception=type(e).__name__, message=clean(e))
            finally:
                if g is not None:
                    try:
                        if g.poll() is None:
                            try: os.killpg(g.pid,signal.SIGTERM)
                            except ProcessLookupError: pass
                            try: g.wait(timeout=0.4)
                            except subprocess.TimeoutExpired:
                                if g.poll() is None: os.killpg(g.pid,signal.SIGKILL)
                                g.wait(timeout=0.5)
                    except Exception as e:
                        r['secondaryFailures'].append({'kind':'cleanup-error','exception':type(e).__name__,'message':clean(e)})
                    r['guardianExitCode']=g.poll()
                    for _ in range(2):
                        try:
                            try: os.killpg(g.pid,0); absent=False
                            except ProcessLookupError: absent=True
                            r['closureProbes'].append({'monotonicNs':time.monotonic_ns(),'absent':absent})
                        except Exception as e:
                            r['secondaryFailures'].append({'kind':'closure-probe-error','exception':type(e).__name__,'message':clean(e)})
                        time.sleep(0.02)
                    r['closed']=len(r['closureProbes'])==2 and all(x['absent'] for x in r['closureProbes']) and r['guardianExitCode'] is not None
                    ep=folder/'events.jsonl'
                    if ep.exists():
                        try: r['events']=[json.loads(line) for line in ep.read_text().splitlines()]
                        except Exception as e: r['secondaryFailures'].append({'kind':'final-event-parse','exception':type(e).__name__})
                if not (folder/'inert-output.json').exists(): r['secondaryFailures'].append({'kind':'missing-inert-output'})
                if not r['closed']: r['secondaryFailures'].append({'kind':'closure-unproven'})
                r['wallSeconds']=time.monotonic()-t0
                if r['wallSeconds'] > 5: r['secondaryFailures'].append({'kind':'case-budget'})
                write(folder/'report.json',r);reports.append(pin(folder/'report.json'))
            if not r['closed']: raise RuntimeError('stop-after-unclosed-case')
    except Exception as e: fatal={'exception':type(e).__name__,'message':clean(e)}
    finally:
        write(results/'index.json', {**shared,'cases':config['cases'],'reports':reports,'fatalFailure':fatal,'wallSeconds':time.monotonic()-start,'files':[pin(x) for x in sorted(results.rglob('*')) if x.is_file()]})
        signal.alarm(0)
    return 0 if fatal is None and len(reports)==8 else 1

if __name__=='__main__': sys.exit(main())
