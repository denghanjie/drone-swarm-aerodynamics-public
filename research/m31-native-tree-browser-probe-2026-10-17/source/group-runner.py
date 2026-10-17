"""Retained process-group leader for saved validation and owned Chrome root."""
from pathlib import Path
import datetime,hashlib,json,os,select,signal,subprocess,sys,time
package=Path(__file__).resolve().parents[1]; root=package.parents[1]
config=json.loads((package/'config.json').read_bytes())
def need(ok,why):
    if not ok: raise ValueError(why)
need(config.get('executionAllowed') is True and config.get('authorization') and datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(config['launchCutoffUtc']),'execution-not-authorized')
attempt=json.loads((package/'results/run-attempt.json').read_bytes());token=os.environ.get('RESEARCH_RUN_TOKEN','');stage=os.environ.get('RESEARCH_STAGE')
need(stage in ('saved-validation','browser') and token and attempt['status']=='running' and attempt['stages'][stage]['status']=='started' and hashlib.sha256(token.encode()).hexdigest()==attempt['runTokenSha256'],'supervisor-binding')
command=sys.argv[1:]
if stage=='browser':
    expected=[os.environ['RESEARCH_NODE'],str(package/'source/controller.cjs'),str(root),attempt['sourceManifestSha256'],attempt['sourceCommit']];kind='node'
else:
    expected=[str(Path(sys.executable).resolve()),'-I','-B',str(package/'source/validate-saved.py'),str(root),attempt['sourceManifestSha256'],attempt['sourceCommit']];kind='python'
need(command==expected,'fixed-owned-child-command')
raw=(package/'source-manifest.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==attempt['sourceManifestSha256'],'manifest-binding');manifest=json.loads(raw)
for relative in ['config.json','source/group-runner.py','source/controller.cjs' if stage=='browser' else 'source/validate-saved.py']:
    file=package/relative;pin=next((p for p in manifest['files'] if p['path']==str(file.relative_to(root))),None);b=file.read_bytes()
    need(pin and len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'guardian-source-pin')
h=hashlib.sha256();size=0
with Path(command[0]).open('rb') as stream:
    for block in iter(lambda:stream.read(1048576),b''):h.update(block);size+=len(block)
need(size==manifest['runtime'][kind]['bytes'] and h.hexdigest()==manifest['runtime'][kind]['sha256'],'guardian-runtime-pin')
private=Path(os.environ['RESEARCH_SUPERVISOR_DIR']);child=subprocess.Popen(command)
with (private/'child.json').open('x') as stream:json.dump({'pid':child.pid,'group':os.getpgrp()},stream);stream.flush();os.fsync(stream.fileno())
recorded=False
while True:
    code=child.poll()
    if code is not None and not recorded:
        with (private/'exit.tmp').open('x') as stream:json.dump({'returncode':code},stream);stream.flush();os.fsync(stream.fileno())
        (private/'exit.tmp').rename(private/'exit.json');recorded=True
    ready,_,_=select.select([sys.stdin.buffer],[],[],.1)
    if ready:
        b=os.read(sys.stdin.fileno(),1)
        if b==b'R' and recorded:break
        os.killpg(os.getpgrp(),signal.SIGKILL)
    if time.monotonic_ns()>=int(os.environ['RESEARCH_CHILD_DEADLINE_MONOTONIC_NS']) or datetime.datetime.now(datetime.timezone.utc)>=datetime.datetime.fromisoformat(config['launchCutoffUtc']):os.killpg(os.getpgrp(),signal.SIGKILL)
sys.exit(0)
