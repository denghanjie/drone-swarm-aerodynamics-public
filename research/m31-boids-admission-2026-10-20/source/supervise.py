from pathlib import Path
import subprocess,os,json,time,signal,sys
base=Path(__file__).resolve().parent.parent
phase=sys.argv[1]
assert phase in ('native','audit','ui')
with (base/(phase+'-supervisor-launch.lock')).open('x') as f:f.write('one bounded attempt\n')
commands={'native':[os.environ.get('M31_NODE','node'),str(base/'source/run.cjs')],'audit':[sys.executable,str(base/'source/audit.py')],'ui':[os.environ.get('M31_NODE','node'),str(base/'source/ui.cjs')]}
limits={'native':380,'audit':200,'ui':100}
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
 report['allocationWallPassed']=report['wallSeconds']<={'native':360,'audit':180,'ui':90}[phase]
 with (base/(phase+'-supervisor.json')).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report))
