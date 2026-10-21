from pathlib import Path
import subprocess,os,json,time,signal,sys
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
base=Path(__file__).resolve().parent.parent;root=base.parent.parent;phase=sys.argv[1]
assert phase in ('producer','audit','finalize','ui')
with (base/(phase+'-supervisor-launch.lock')).open('x') as f:f.write('one bounded attempt\n')
commands={'producer':[os.environ['M31_NODE'],str(base/'source/run.cjs')],'audit':[sys.executable,str(base/'source/audit.py')],'finalize':[sys.executable,str(base/'source/finalize.py')],'ui':[os.environ['M31_NODE'],str(base/'source/ui.cjs')]}
start=time.monotonic();report={};p=None
try:
 p=subprocess.Popen(commands[phase],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 out,err=p.communicate(timeout={'producer':1220,'audit':1220,'finalize':140,'ui':160}[phase]);report={'returncode':p.returncode,'stdout':out.replace(str(root),'[repository]')[-3000:],'stderr':err.replace(str(root),'[repository]')[-3000:]}
except subprocess.TimeoutExpired:report={'timeout':True,'returncode':1}
except Exception as e:report={'returncode':1,'launchError':type(e).__name__}
finally:
 if p:
  for sig in [signal.SIGTERM,signal.SIGKILL]:
   try:os.killpg(p.pid,sig)
   except ProcessLookupError:pass
   if sig==signal.SIGTERM:time.sleep(.3)
  p.wait()
 report['wallSeconds']=time.monotonic()-start;report['allocationWallPassed']=report['wallSeconds']<={'producer':1200,'audit':1200,'finalize':120,'ui':150}[phase]
 folder=base/('results' if phase=='producer' else phase);report['outputBytes']=sum(x.stat().st_size for x in folder.rglob('*') if x.is_file()) if folder.exists() else 0
 report['outputCapPassed']=report['outputBytes']<={'producer':2048,'audit':128,'finalize':2,'ui':16}[phase]*1024**2
 if not report['allocationWallPassed'] or not report['outputCapPassed']:report['childReturncode']=report.get('returncode');report['returncode']=1
 with (base/(phase+'-supervisor.json')).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report))
