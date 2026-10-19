from pathlib import Path
import subprocess,os,json,time,signal
base=Path(__file__).resolve().parent.parent
with (base/'ui-v2-supervisor-launch.lock').open('x') as f:f.write('one display attempt\n')
start=time.monotonic();p=subprocess.Popen([os.environ['M31_NODE'],str(base/'source/ui-v2.cjs')],start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
report={}
try:
 out,err=p.communicate(timeout=100);report={'returncode':p.returncode,'stdout':out.replace(str(base.parent.parent),'[repository]')[-2000:],'stderr':err.replace(str(base.parent.parent),'[repository]')[-2000:]}
except subprocess.TimeoutExpired:report={'timeout':True}
finally:
 # Owned group includes any surviving Chromium children even after Node exits.
 try:os.killpg(p.pid,signal.SIGTERM)
 except ProcessLookupError:pass
 # Always allow a short TERM grace and then kill the owned group, even if
 # the Node leader already exited. Browser spawn forces detached=False.
 time.sleep(.3)
 try:os.killpg(p.pid,signal.SIGKILL)
 except ProcessLookupError:pass
 p.wait()
 report['wallSeconds']=time.monotonic()-start
 with (base/'ui-v2-supervisor.json').open('x') as f:json.dump(report,f,indent=2)
 print(json.dumps(report))
