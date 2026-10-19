"""Single-use external time/output supervision; never evaluates model arithmetic."""
import json,os,pathlib,signal,subprocess,sys,time
base=pathlib.Path(__file__).resolve().parents[1];mode=sys.argv[1];assert mode == 'ui'
folder=base/'results-v2';folder.mkdir(exist_ok=True)
with (folder/(mode+'-supervisor.lock')).open('x') as f:f.write('one invocation\n')
t=time.monotonic();cap=(32 if mode=='ui' else 16)*1024**2;limit=False;timeout=False
cmd=[os.environ['M31_NODE'],str(base/'source/ui-v2.cjs')] if mode=='ui' else [sys.executable,'-I','-B',str(base/'source'/ (mode+'.py'))]
with (folder/(mode+'-stdout.txt')).open('xb') as out,(folder/(mode+'-stderr.txt')).open('xb') as err:
 p=subprocess.Popen(cmd,cwd=base,stdout=out,stderr=err,start_new_session=True)
 while p.poll() is None:
  size=sum(x.stat().st_size for directory in [folder,base/'ui-v2'] if directory.exists() for x in directory.rglob('*') if x.is_file())
  timeout=time.monotonic()-t>=60;limit=size>cap-16384
  if timeout or limit:
   os.killpg(p.pid,signal.SIGKILL);p.wait();break
  time.sleep(.025)
 elapsed=time.monotonic()-t;timeout=timeout or elapsed>=60
 result={'mode':mode,'exitCode':p.returncode,'elapsedSeconds':elapsed,'timeout':timeout,'outputLimitExceeded':limit,'outputCapBytes':cap}
 size=sum(x.stat().st_size for directory in [folder,base/'ui-v2'] if directory.exists() for x in directory.rglob('*') if x.is_file());result['savedBytesBeforeSupervisor']=size;result['outputLimitExceeded']=limit or size>cap-16384
(folder/(mode+'-supervisor.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(0 if result['exitCode']==0 and not result['timeout'] and not result['outputLimitExceeded'] else 1)
