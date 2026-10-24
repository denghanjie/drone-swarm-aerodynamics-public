"""Unexecuted administrative supervisor draft. One helper session, swept on all exits."""
from pathlib import Path
import sys,os,json,time,signal,subprocess,hashlib,re
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-python-prohibited')
started=time.monotonic();root=Path.cwd()
protocol=Path(sys.argv[1]);helper=Path(sys.argv[2]);expectedProtocol=sys.argv[3];expectedHelper=sys.argv[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=protocol.read_bytes();source=helper.read_bytes()
if sha(raw)!=expectedProtocol or sha(source)!=expectedHelper:raise RuntimeError('exact-source-pin-mismatch')
cfg=json.loads(raw);name=cfg['privateStoreName']
if not re.fullmatch('m31-targeted-ssh-[a-z0-9-]+',name):raise RuntimeError('unsafe-private-directory')
work=Path('/private/tmp')/name;prefix=Path('/private/tmp')/(name+'-supervisor')
with Path(str(prefix)+'.lock').open('x') as f:f.write('one900-second administrative allocation\n')
Path(str(prefix)+'-start.json').write_text(json.dumps({'protocolSha256':expectedProtocol,'helperSha256':expectedHelper,'maxSeconds':900,'noScience':True})+'\n')
env={k:v for k,v in os.environ.items() if k not in ('PYTHONOPTIMIZE','PYTHONPATH')};env['PYTHONDONTWRITEBYTECODE']='1'
p=None;reason=None;groupAbsent=False
out=Path(str(prefix)+'.stdout');err=Path(str(prefix)+'.stderr')
try:
    with out.open('xb') as a,err.open('xb') as b:
        p=subprocess.Popen([sys.executable,str(helper),str(protocol)],cwd=root,env=env,stdout=a,stderr=b,start_new_session=True)
        while p.poll() is None:
            if time.monotonic()-started>=890:reason='outer-timeout';break
            if out.stat().st_size+err.stat().st_size>2*1024**2:reason='outer-output-cap';break
            time.sleep(.1)
except BaseException as e:reason=type(e).__name__
finally:
    if p:
        for sig in (signal.SIGTERM,signal.SIGKILL):
            try:os.killpg(p.pid,sig)
            except ProcessLookupError:pass
            if sig==signal.SIGTERM:time.sleep(.2)
        try:p.wait(timeout=3)
        except subprocess.TimeoutExpired:reason='helper-reap-timeout'
        for _ in range(20):
            try:os.killpg(p.pid,0)
            except ProcessLookupError:groupAbsent=True;break
            time.sleep(.1)
    pins=[];inner=None
    for f in [work/'events.jsonl',work/'receipt.json',out,err]:
        try:
            if f.is_file():
                size=f.stat().st_size
                if size>2*1024**2:reason='closure-file-cap';continue
                data=f.read_bytes();pins.append({'file':f.name,'bytes':len(data),'sha256':sha(data)})
                if f.name=='receipt.json':inner=json.loads(data)
        except (OSError,ValueError):reason='closure-file-unreadable-or-incomplete'
    elapsed=time.monotonic()-started
    report={'closed':True,'passed':bool(not reason and p and p.returncode==0 and groupAbsent and elapsed<=900 and inner and inner['passed']),'returncode':p.returncode if p else None,'reason':reason,'processGroupAbsent':groupAbsent,'wallSeconds':elapsed,'protocolSha256':expectedProtocol,'helperSha256':expectedHelper,'privateFilePinsAfterProcessCleanup':pins,'noScientificExecution':True,'receiptScope':'Administrative isolated SSH acquisition only. Body hashes are in the helper receipt; all helper descendants share one swept session.'}
    Path(str(prefix)+'.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
