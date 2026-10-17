"""Bounded UI-only QA; scientific source/results never executed or changed."""
from pathlib import Path
import datetime,hashlib,json,os,signal,subprocess,sys,time
start=time.monotonic();out=Path(__file__).resolve().parent
root=Path(os.environ['RESEARCH_ROOT']);private=Path(os.environ['RESEARCH_QA_PRIVATE'])
assert os.environ['RESEARCH_EXECUTION_CONTEXT']=='tool-require-escalated'
assert not (out/'STARTED.json').exists() and not private.exists() and private.resolve()==private
assert (datetime.datetime.fromisoformat('2026-10-17T05:06:20+00:00')-datetime.datetime.now(datetime.timezone.utc)).total_seconds()>90
runtime=json.loads((root/'research/m31-coupled-stage-qualification-2026-10-17/runtime.json').read_bytes())
def identity(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
for p,pin in [(Path(sys.executable).resolve(),runtime['python']),(Path(os.environ['RESEARCH_NODE']).resolve(),runtime['node'])]:assert identity(p)=={k:pin[k] for k in ['bytes','sha256']}
for pin in runtime['chrome']['files']:assert identity(Path(os.environ['RESEARCH_CHROME_CONTENTS'])/pin['appRelativePath'])=={k:pin[k] for k in ['bytes','sha256']}
for pin in runtime['playwright']['files']:assert identity(Path(os.environ['RESEARCH_NODE_MODULES'])/pin['moduleRelativePath'])=={k:pin[k] for k in ['bytes','sha256']}
private.mkdir();os.environ['RESEARCH_QA_DEADLINE_NS']=str(int((start+90)*1e9))
marker={'startedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scientificCalls':0,'budgetSeconds':90,'sourcePins':{p.name:identity(p) for p in out.iterdir() if p.is_file()}}
(out/'STARTED.json').write_text(json.dumps(marker,indent=2)+'\n')
guardian=None;status='failed';failure=None;code=None
try:
    with (private/'controller.log').open('xb') as log:
        guardian=subprocess.Popen([sys.executable,'-I','-B',str(out/'guardian.py'),str(out/'run.cjs')],stdin=subprocess.PIPE,stdout=log,stderr=log,start_new_session=True,env=os.environ.copy(),cwd=root)
        while not (private/'exit.json').exists():
            assert time.monotonic()<start+85,'UI deadline'
            total=0
            for p in private.rglob('*'):
                if p.is_symlink():continue
                if p.is_file():total+=p.stat().st_size
            assert total<128*1024**2,'private bytes'
            assert sum(p.stat().st_size for p in out.iterdir() if p.is_file())<16*1024**2,'QA bytes'
            assert guardian.poll() is None,'guardian stopped early'
            time.sleep(.1)
        code=json.loads((private/'exit.json').read_bytes())['exitCode']
        report=json.loads((out/'report.json').read_bytes())
        assert code==0 and report['passed'] is True and report['cleanup']=={'exit':{'code':0,'signal':None},'close':{'code':0,'signal':None}},'UI failure'
        guardian.stdin.write(b'R');guardian.stdin.flush();guardian.wait(timeout=3);assert guardian.returncode==0
        status='completed'
except Exception as error:
    failure=type(error).__name__+':'+str(error)
finally:
    if guardian is not None and guardian.poll() is None:
        os.killpg(guardian.pid,signal.SIGKILL);guardian.wait(timeout=3)
    assert all(identity(out/p)==pin for p,pin in marker['sourcePins'].items()),'QA source changed'
    result={'status':status,'scientificCalls':0,'controllerExitCode':code,'guardianReaped':guardian is not None and guardian.poll() is not None,'wallSeconds':time.monotonic()-start,'failure':failure,'scope':'Owned root and unreaped guardian group handling; no all-helper OS guarantee or science timing claim.'}
    with (out/'supervision.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result))
sys.exit(0 if status=='completed' else 1)
