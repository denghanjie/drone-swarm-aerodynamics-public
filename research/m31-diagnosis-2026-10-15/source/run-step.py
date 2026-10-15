#!/usr/bin/env python3
"""Cumulative bounded executable supervisor. It never retries a recorded job ID."""
import argparse,json,os,subprocess,time,signal,resource,platform
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--timeout',type=float,default=240);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
root=Path(__file__).resolve().parents[1];ledger=root/'results/budget.json';raw=root/'raw';raw.mkdir(exist_ok=True)
cmd=a.command[1:] if a.command and a.command[0]=='--' else a.command
if not cmd:p.error('missing child command')
lock=root/'results/execution.lock';lock.parent.mkdir(exist_ok=True)
fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
child=None;started=None;b=None
def interrupted(signum,frame):raise InterruptedError('supervisor signal')
signal.signal(signal.SIGINT,interrupted);signal.signal(signal.SIGTERM,interrupted)
try:
 b=json.loads(ledger.read_text()) if ledger.exists() else {'wallCapSeconds':1200,'rawByteCap':2147483648,'entries':[],'terminal':False,'platform':{'system':platform.system(),'release':platform.release(),'machine':platform.machine(),'python':platform.python_version()},'scope':'Execution diagnostics only, not a speed benchmark. CPU time is child aggregate; maximum RSS is cumulative child high-water, not simultaneous total memory.'}
 if b.get('active') or b.get('requiresFailureReview') or b['terminal'] or any(x['id']==a.id for x in b['entries']):raise RuntimeError('Terminal campaign or already recorded ID; no automatic retry')
 used=sum(x['wallSeconds'] for x in b['entries']);remaining=b['wallCapSeconds']-used
 if remaining<=0:raise RuntimeError('Cumulative execution cap exhausted')
 limit=min(a.timeout,remaining);b['active']={'id':a.id,'wallLimitSeconds':limit};ledger.write_text(json.dumps(b,indent=2)+'\n');started=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN);reason=None
 # Local execution logs can contain stack paths. They are excluded from the public payload.
 logdir=Path('/tmp/m31-diagnosis-logs');logdir.mkdir(exist_ok=True)
 with (logdir/(a.id+'.log')).open('wb') as log:
  child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  while child.poll() is None:
   elapsed=time.monotonic()-started
   size=sum(x.stat().st_size for x in raw.rglob('*') if x.is_file())
   if elapsed>=max(0,limit-1.1):reason='wall-time cap'
   elif size>=b['rawByteCap']:reason='raw-data cap'
   if reason:
    os.killpg(child.pid,signal.SIGTERM)
    try:child.wait(timeout=1)
    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
    break
   time.sleep(.05)
  code=child.wait()
 elapsed=time.monotonic()-started;after=resource.getrusage(resource.RUSAGE_CHILDREN)
 final_size=sum(x.stat().st_size for x in raw.rglob('*') if x.is_file())
 if elapsed>=limit:reason=reason or 'wall-time cap'
 if final_size>=b['rawByteCap']:reason=reason or 'raw-data cap'
 b['active']=None
 b['entries'].append({'id':a.id,'exitCode':code,'wallSeconds':elapsed,'childCPUSeconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'cumulativeChildMaxRSSPlatformUnits':after.ru_maxrss,'stop':reason,'completeProcess':code==0 and reason is None,'rawBytesAfter':sum(x.stat().st_size for x in raw.rglob('*') if x.is_file())})
 b['terminal']=bool(reason);b['requiresFailureReview']=code!=0
 ledger.write_text(json.dumps(b,indent=2)+'\n');print(json.dumps(b['entries'][-1]));raise SystemExit(1 if reason else code if code>=0 else 1)
except BaseException as exc:
 if b and b.get('active') and started is not None:
  signal.signal(signal.SIGINT,signal.SIG_IGN);signal.signal(signal.SIGTERM,signal.SIG_IGN)
  if child is not None and child.poll() is None:
   os.killpg(child.pid,signal.SIGTERM)
   try:child.wait(timeout=1)
   except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
  b['entries'].append({'id':a.id,'exitCode':child.returncode if child else None,'wallSeconds':time.monotonic()-started,'stop':'supervisor interrupted or failed','failureClass':type(exc).__name__,'completeProcess':False,'rawBytesAfter':sum(x.stat().st_size for x in raw.rglob('*') if x.is_file())})
  b['active']=None;b['terminal']=True;b['requiresFailureReview']=True
  ledger.write_text(json.dumps(b,indent=2)+'\n')
 raise
finally:lock.unlink(missing_ok=True)
