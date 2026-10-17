"""Retained browser group leader; gated before child spawn. No science imports."""
from pathlib import Path
import datetime, hashlib, json, os, select, signal, subprocess, sys, time
package=Path(__file__).resolve().parents[1]
config=json.loads((package/'config.json').read_bytes())
if config.get('executionAllowed') is not True or not config.get('authorization') or not config.get('launchCutoffUtc'):
    raise SystemExit('execution-not-authorized')
if datetime.datetime.now(datetime.timezone.utc)>=datetime.datetime.fromisoformat(config['launchCutoffUtc']):raise SystemExit('launch-cutoff')
attempt=json.loads((package/'results/run-attempt.json').read_bytes())
token=os.environ.get('RESEARCH_RUN_TOKEN','')
if not token or attempt.get('status')!='running' or attempt.get('stages',{}).get('browser',{}).get('status')!='started' or hashlib.sha256(token.encode()).hexdigest()!=attempt.get('runTokenSha256'):raise SystemExit('supervisor-binding')
if len(sys.argv)!=6 or Path(sys.argv[2]).resolve()!=package/'source/controller.cjs' or sys.argv[4]!=attempt['sourceManifestSha256'] or sys.argv[5]!=attempt['sourceCommit']:raise SystemExit('fixed-controller-command')
root=package.parents[1]
manifest_path=package/'source-manifest.json'
manifest_bytes=manifest_path.read_bytes()
if hashlib.sha256(manifest_bytes).hexdigest()!=attempt['sourceManifestSha256']:raise SystemExit('manifest-binding')
manifest=json.loads(manifest_bytes)
for relative in ['config.json','source/group-runner.py','source/controller.cjs']:
    target=package/relative
    pin=next((p for p in manifest['files'] if p['path']==str(target.relative_to(root))),None)
    raw=target.read_bytes()
    if not pin or len(raw)!=pin['bytes'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise SystemExit('guardian-source-pin')
node=Path(sys.argv[1]).resolve()
if node!=Path(os.environ['RESEARCH_NODE']).resolve():raise SystemExit('node-runtime-location')
h=hashlib.sha256();count=0
with node.open('rb') as f:
    for b in iter(lambda:f.read(1024*1024),b''):h.update(b);count+=len(b)
if count!=manifest['runtime']['node']['bytes'] or h.hexdigest()!=manifest['runtime']['node']['sha256']:raise SystemExit('node-runtime-pin')
private=Path(os.environ['RESEARCH_SUPERVISOR_DIR'])
child=subprocess.Popen(sys.argv[1:])
with (private/'child.json').open('x') as f:json.dump({'pid':child.pid,'group':os.getpgrp()},f);f.flush();os.fsync(f.fileno())
recorded=False
while True:
    code=child.poll()
    if code is not None and not recorded:
        with (private/'exit.tmp').open('x') as f:json.dump({'returncode':code},f);f.flush();os.fsync(f.fileno())
        (private/'exit.tmp').rename(private/'exit.json');recorded=True
    ready,_,_=select.select([sys.stdin.buffer],[],[],.1)
    if ready:
        b=os.read(sys.stdin.fileno(),1)
        if b==b'R' and recorded:break
        os.killpg(os.getpgrp(),signal.SIGKILL)
    if time.monotonic_ns()>=int(os.environ['RESEARCH_CHILD_DEADLINE_MONOTONIC_NS']):os.killpg(os.getpgrp(),signal.SIGKILL)
sys.exit(0)
