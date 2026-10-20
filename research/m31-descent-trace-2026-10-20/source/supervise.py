import sys,os
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
 raise RuntimeError('optimized-Python-not-permitted')
from pathlib import Path
import subprocess,os,json,time,signal,sys
base=Path(__file__).resolve().parent.parent;root=base.parent.parent;phase=sys.argv[1]
assert phase in ('extract','audit','finalize','ui')
with (base/(phase+'-supervisor-launch.lock')).open('x') as f:f.write('one bounded attempt\n')
commands={phase:([os.environ['M31_NODE'],str(base/'source/ui.cjs')] if phase=='ui' else [sys.executable,str(base/'source'/(phase+'.py'))])}
start=time.monotonic();p=subprocess.Popen(commands[phase],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);report={}
try:
 out,err=p.communicate(timeout=160 if phase=='ui' else 920);report={'returncode':p.returncode,'stdout':out.replace(str(root),'[repository]')[-3000:],'stderr':err.replace(str(root),'[repository]')[-3000:]}
except subprocess.TimeoutExpired:report={'timeout':True,'returncode':1}
finally:
 for sig in [signal.SIGTERM,signal.SIGKILL]:
  try:os.killpg(p.pid,sig)
  except ProcessLookupError:pass
  if sig==signal.SIGTERM:time.sleep(.3)
 p.wait();report['wallSeconds']=time.monotonic()-start;report['allocationWallPassed']=report['wallSeconds']<=(150 if phase=='ui' else 900)
 folder=base/('results' if phase=='extract' else phase);report['outputBytes']=sum(x.stat().st_size for x in folder.rglob('*') if x.is_file()) if folder.exists() else 0
 report['outputCapPassed']=report['outputBytes']<= {'extract':32,'audit':2,'finalize':2,'ui':16}[phase]*1024**2
 if not report['allocationWallPassed'] or not report['outputCapPassed']:report['childReturncode']=report.get('returncode');report['returncode']=1
 with (base/(phase+'-supervisor.json')).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report))
