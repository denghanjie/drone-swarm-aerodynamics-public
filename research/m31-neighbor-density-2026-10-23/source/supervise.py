from pathlib import Path
import subprocess,os,json,time,signal,sys,hashlib
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
base=Path(__file__).resolve().parent.parent;root=base.parent.parent;phase=sys.argv[1];cfg=json.loads((base/'config.json').read_bytes());a=cfg['allocations'][phase]
with (base/(phase+'-supervisor-launch.lock')).open('x') as f:f.write('single bounded attempt\n')
commands={'producer':[sys.executable,str(base/'source/diagnose.py')],'audit':[sys.executable,str(base/'source/audit.py')],'finalize':[sys.executable,str(base/'source/finalize.py')],'ui':[os.environ['M31_NODE'],str(base/'source/ui.cjs')]}
start=time.monotonic();report={};p=None;interrupted=None;folder=base/('results' if phase=='producer' else phase)
def interrupt(signum,frame):
 global interrupted
 interrupted=signum
 raise InterruptedError('supervisor-interrupted')
for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,interrupt)
try:
 env={k:v for k,v in os.environ.items() if k not in ('NODE_OPTIONS','NODE_PATH','PYTHONOPTIMIZE')};env['PYTHONDONTWRITEBYTECODE']='1'
 p=subprocess.Popen([sys.executable,str(base/'source/launch.py'),phase],env=env,start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 while p.poll() is None:
  elapsed=time.monotonic()-start;size=sum(x.stat().st_size for x in folder.rglob('*') if x.is_file()) if folder.exists() else 0
  if elapsed>a['seconds']-2 or size>a['mib']*1024**2:report={'returncode':1,'timeout':elapsed>a['seconds']-2,'evidenceOverflow':size>a['mib']*1024**2};break
  time.sleep(1)
 if not report:
  out,err=p.communicate(timeout=5);report={'returncode':p.returncode,'stdout':out.replace(str(root),'[repository]')[-3000:],'stderr':err.replace(str(root),'[repository]')[-3000:]}
except BaseException as e:report={'returncode':1,'launchError':type(e).__name__,'interruptedSignal':interrupted}
finally:
 for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,signal.SIG_IGN)
 if p:
  for sig in [signal.SIGTERM,signal.SIGKILL]:
   try:os.killpg(p.pid,sig)
   except ProcessLookupError:pass
   if sig==signal.SIGTERM:time.sleep(.3)
  try:p.wait(timeout=2)
  except subprocess.TimeoutExpired:report.update({'returncode':1,'childReapTimeout':True})
 report['wallSeconds']=time.monotonic()-start;report['allocationWallPassed']=report['wallSeconds']<=a['seconds'];report['outputBytes']=sum(x.stat().st_size for x in folder.rglob('*') if x.is_file()) if folder.exists() else 0;report['externalViewerPinBytes']=(base/'viewer/pins.json').stat().st_size if phase=='finalize' and (base/'viewer/pins.json').exists() else 0;report['outputCapPassed']=report['outputBytes']+report['externalViewerPinBytes']<=a['mib']*1024**2;report['closed']=True
 if not report['allocationWallPassed'] or not report['outputCapPassed']:report['childReturncode']=report.get('returncode');report['returncode']=1
 with (base/(phase+'-supervisor.json')).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report));sys.exit(report['returncode'])
