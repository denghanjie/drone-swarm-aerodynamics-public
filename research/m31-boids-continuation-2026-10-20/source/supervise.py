from pathlib import Path
import subprocess,os,json,time,signal,sys
base=Path(__file__).resolve().parent.parent
phase=sys.argv[1]
assert phase in ('storage','native','audit','ui')
with (base/(phase+'-supervisor-launch.lock')).open('x') as f:f.write('one bounded attempt\n')
commands={'storage':[sys.executable,str(base/'source/storage-check.py')],'native':[os.environ.get('M31_NODE','node'),str(base/'source/run.cjs')],'audit':[sys.executable,str(base/'source/audit.py')],'ui':[os.environ.get('M31_NODE','node'),str(base/'source/ui.cjs')]}
limits={'storage':25,'native':1220,'audit':1220,'ui':160}
start=time.monotonic();p=subprocess.Popen(commands[phase],start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);report={}
try:
 out,err=p.communicate(timeout=limits[phase]);report={'returncode':p.returncode,'stdout':out.replace(str(base.parent.parent),'[repository]')[-3000:],'stderr':err.replace(str(base.parent.parent),'[repository]')[-3000:]}
except subprocess.TimeoutExpired:report={'timeout':True}
finally:
 try:os.killpg(p.pid,signal.SIGTERM)
 except ProcessLookupError:pass
 time.sleep(.3)
 try:os.killpg(p.pid,signal.SIGKILL)
 except ProcessLookupError:pass
 p.wait();report['wallSeconds']=time.monotonic()-start
 report['allocationWallPassed']=report['wallSeconds']<={'storage':20,'native':1200,'audit':1200,'ui':150}[phase]
 folder=base/{'native':'results','audit':'audit','ui':'ui','storage':'storage'}[phase]
 report['outputBytes']=sum(x.stat().st_size for x in folder.rglob('*') if x.is_file()) if folder.exists() else 0
 report['outputCapPassed']=report['outputBytes']<={'native':3*1024**3,'audit':64*1024**2,'ui':16*1024**2,'storage':8*1024**2}[phase]
 if not report['outputCapPassed']:report['childReturncode']=report.get('returncode');report['returncode']=1
 with (base/(phase+'-supervisor.json')).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report))
