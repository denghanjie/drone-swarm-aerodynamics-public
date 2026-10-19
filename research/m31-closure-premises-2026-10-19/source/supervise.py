"""One display-only allocation; no scientific evaluation."""
import json,os,pathlib,signal,subprocess,sys,time
base=pathlib.Path(__file__).resolve().parents[1];out=base/'ui';out.mkdir()
with (out/'supervisor.lock').open('x') as f:f.write('one display allocation\n')
t=time.monotonic();cap=32*1024**2;timeout=False;breach=False
with (out/'stdout.txt').open('xb') as stdout,(out/'stderr.txt').open('xb') as stderr:
 p=subprocess.Popen([os.environ['M31_NODE'],str(base/'source/ui.cjs')],stdout=stdout,stderr=stderr,cwd=base,start_new_session=True)
 while p.poll() is None:
  timeout=time.monotonic()-t>=60;breach=sum(x.stat().st_size for x in out.rglob('*') if x.is_file())>cap-16384
  if timeout or breach:os.killpg(p.pid,signal.SIGKILL);p.wait();break
  time.sleep(.025)
 elapsed=time.monotonic()-t;size=sum(x.stat().st_size for x in out.rglob('*') if x.is_file());r={'exitCode':p.returncode,'elapsedSeconds':elapsed,'timeout':timeout or elapsed>=60,'outputLimitExceeded':breach or size>cap-16384,'outputCapBytes':cap,'savedBytesBeforeSupervisor':size}
(out/'supervisor.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));sys.exit(0 if r['exitCode']==0 and not r['timeout'] and not r['outputLimitExceeded'] else 1)
