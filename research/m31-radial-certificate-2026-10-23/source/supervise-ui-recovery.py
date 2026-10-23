from pathlib import Path
import os, sys, json, hashlib, subprocess, signal, time

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('optimized Python forbidden')
base = Path(__file__).resolve().parent.parent
root = base.parent.parent
with (base / 'ui-recovery-supervisor-launch.lock').open('x') as f:
    f.write('single separately reviewed display recovery attempt\n')
start = time.monotonic()
p = None
report = {}
folder = base / 'ui-recovery'
cap = 16 * 1024**2
def sha(b):
    return hashlib.sha256(b).hexdigest()
def load(p):
    return json.loads(p.read_bytes())
def interrupt(signum, frame):
    raise InterruptedError('supervisor interrupted')
for sig in (signal.SIGTERM, signal.SIGINT):
    signal.signal(sig, interrupt)
try:
    raw = (base / 'display-recovery-manifest.json').read_bytes()
    manifest = json.loads(raw)
    gate = load(base / 'display-recovery-publication.json')
    assert gate['manifestBytes'] == len(raw) and gate['manifestSha256'] == sha(raw)
    assert gate['independentReviewPassed'] and gate['remoteBytesEqualLocal'] and gate['committedBytesEqualLocal']
    assert gate['verifiedFilePins'] == len(manifest['files'])
    assert len({x['path'] for x in manifest['files']}) == len(manifest['files'])
    for pin in manifest['files']:
        data = (root / pin['path']).read_bytes()
        assert len(data) == pin['bytes'] and sha(data) == pin['sha256'], pin['path']
    for phase in ('producer', 'audit', 'finalize'):
        old = load(base / (phase + '-supervisor.json'))
        assert old['closed'] and old['returncode'] == 0 and old['allocationWallPassed'] and old['outputCapPassed']
    old = load(base / 'ui-supervisor.json')
    assert old['closed'] and old['returncode'] == 1
    assert not folder.exists()
    node = Path(os.environ['M31_NODE'])
    runtime = load(base / 'runtime.json')
    data = node.read_bytes()
    assert len(data) == runtime['nodeExecutableBytes'] and sha(data) == runtime['nodeExecutableSha256']
    env = {k:v for k,v in os.environ.items() if k not in ('NODE_OPTIONS', 'NODE_PATH', 'PYTHONOPTIMIZE')}
    env['NODE_PATH'] = str(node.parent.parent / 'node_modules')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    p = subprocess.Popen([str(node), str(base/'source/ui-recovery.cjs')], env=env, start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while p.poll() is None:
        elapsed = time.monotonic() - start
        size = sum(x.stat().st_size for x in folder.rglob('*') if x.is_file()) if folder.exists() else 0
        if elapsed >= 148 or size > cap:
            report = {'returncode':1, 'timeout':elapsed >= 148, 'evidenceOverflow':size > cap}
            break
        time.sleep(.5)
    if not report:
        out, err = p.communicate(timeout=2)
        report = {'returncode':p.returncode, 'stdout':out.replace(str(root),'[repository]')[-3000:], 'stderr':err.replace(str(root),'[repository]')[-3000:]}
except BaseException as e:
    report = {'returncode':1, 'launchError':type(e).__name__, 'message':str(e).replace(str(root),'[repository]')[:1000]}
finally:
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, signal.SIG_IGN)
    if p:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(p.pid, sig)
            except ProcessLookupError:
                pass
            if sig == signal.SIGTERM:
                time.sleep(.3)
        try:
            p.wait(timeout=2)
        except subprocess.TimeoutExpired:
            report.update(returncode=1, childReapTimeout=True)
    report['wallSeconds'] = time.monotonic() - start
    report['outputBytes'] = sum(x.stat().st_size for x in folder.rglob('*') if x.is_file()) if folder.exists() else 0
    report['allocationWallPassed'] = report['wallSeconds'] <= 150
    report['outputCapPassed'] = report['outputBytes'] <= cap
    report['closed'] = True
    if not report['allocationWallPassed'] or not report['outputCapPassed']:
        report['returncode'] = 1
    with (base / 'ui-recovery-supervisor.json').open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps(report))
    sys.exit(report['returncode'])
