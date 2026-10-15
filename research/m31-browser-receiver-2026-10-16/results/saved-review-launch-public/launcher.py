from pathlib import Path
import json,hashlib,time,subprocess,os,signal,sys,shutil
root=Path('/tmp');manifest=root/'m31-browser-receiver-saved-review-invocation.json';memo=root/'m31-browser-receiver-saved-review-preparation.md';checker=root/'m31-browser-receiver-saved-review.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(manifest)=='9ffc157bc2cb541e64225d653b995e26b271fd715e442b2e1e11c12b9d7a787d'
assert sha(memo)=='8ba5abe9ab52b5d70fd6901fe031c572fa1e05517f17c711cf2ea3e5c5d16a64'
m=json.loads(manifest.read_text());assert sha(checker)==m['checker']['sha256'];assert sha(Path(m['executable']))==m['pythonExecutable']['sha256']
with (root/'m31-browser-receiver-verifier-launch.lock').open('x') as f:f.write('Permanent sole review launch reservation.\n')
a=root/'m31-browser-receiver-review-launches'/str(time.time_ns());a.mkdir(parents=True)
for src,name in [(manifest,'invocation.json'),(memo,'preparation.md'),(checker,'checker.py'),(Path(__file__),'launcher.py')]:shutil.copyfile(src,a/name)
args=[m['executable']]+m['argv'];(a/'arguments.json').write_text(json.dumps(args,indent=2)+'\n');start=time.perf_counter();p=None;status={'terminal':False,'attempts':1,'authorizedCapSeconds':60,'externalTimeoutSeconds':59,'retryPermitted':False}
try:
 with (a/'stdout.txt').open('x') as out,(a/'stderr.txt').open('x') as err:
  p=subprocess.Popen(args,stdout=out,stderr=err,start_new_session=True)
  try:status['exitCode']=p.wait(timeout=59);status['timeout']=False
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait();status.update(exitCode=p.returncode,timeout=True)
except BaseException as e:
 status['launchError']=repr(e)
 if p and p.poll() is None:os.killpg(p.pid,signal.SIGKILL);p.wait()
finally:
 status['terminal']=True;status['wallSeconds']=time.perf_counter()-start;(a/'runtime.json').write_text(json.dumps(status,indent=2)+'\n');status['checkerUnchangedAfter']=sha(checker)==m['checker']['sha256'];(a/'runtime.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps({'archive':str(a),'runtime':status}))
if Path(m['argv'][m['argv'].index('--output')+1]).exists():
 d=json.loads(Path(m['argv'][m['argv'].index('--output')+1]).read_text());print(json.dumps({k:d.get(k) for k in ['status','reviewPass','fullSuiteQualified','checks','scientificChecks','integrityFailures','scientificFindings','fatal','failureExamples','scientificExamples']}))
sys.exit(0 if status.get('exitCode')==0 and not status.get('timeout') and status['wallSeconds']<60 else 1)
