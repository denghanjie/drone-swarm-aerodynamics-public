from pathlib import Path
import subprocess,os,json,time,signal,sys
b=Path(__file__).resolve().parent.parent
with (b/'archive-supervisor-launch.lock').open('x') as f:f.write('one lossless packaging attempt\n')
start=time.monotonic();p=subprocess.Popen([sys.executable,str(b/'source/archive.py')],start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
try:
 out,err=p.communicate(timeout=200);report={'returncode':p.returncode,'stdout':out.replace(str(b.parent.parent),'[repository]')[-2000:],'stderr':err.replace(str(b.parent.parent),'[repository]')[-2000:]}
except subprocess.TimeoutExpired:report={'timeout':True}
finally:
 try:os.killpg(p.pid,signal.SIGTERM)
 except ProcessLookupError:pass
 time.sleep(.3)
 try:os.killpg(p.pid,signal.SIGKILL)
 except ProcessLookupError:pass
 p.wait();report['wallSeconds']=time.monotonic()-start;report['allocationWallPassed']=report['wallSeconds']<=180
 with (b/'archive-supervisor.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report))
