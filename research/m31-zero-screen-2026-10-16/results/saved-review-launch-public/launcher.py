import pathlib,json,time,subprocess,sys,hashlib,os,signal
repo='<REPOSITORY_ROOT>'
lock=pathlib.Path('/tmp/m31-zero-screen-verifier-sole-launch.lock')
with lock.open('x') as f:f.write(str(time.time_ns())+'\n')
a=pathlib.Path('/tmp/m31-zero-screen-verifier-launches')/str(time.time_ns());a.mkdir(parents=True)
checker=pathlib.Path('/tmp/m31-zero-screen-saved-review.py');memo=pathlib.Path('/tmp/m31-zero-screen-saved-review-preparation.md')
assert hashlib.sha256(checker.read_bytes()).hexdigest()=='96c324e62ef554c98ff599f49d338b6830d2a23f6c1e292782f0438bb49e4b67'
assert hashlib.sha256(memo.read_bytes()).hexdigest()=='22309847feb2699f28a479fe4bdcb653f068f6eafdd8ca970c826e31fc6966ec'
for src,name in [(checker,'checker.py'),(memo,'preparation.md'),(pathlib.Path(__file__),'launcher.py')]: (a/name).write_bytes(src.read_bytes())
args=[sys.executable,str(checker),repo,'--source-commit','4717d9b5bb3d82fe2b3d75ea26801de201d124b6','--freeze-sha256','2f1313c8476c09352ae22711be15afce5c7a3d229755a0502b1266201cb41f6a','--authorized-after-science']
(a/'arguments.json').write_text(json.dumps(args,indent=2)+'\n');t=time.perf_counter();status={'authorizedCapSeconds':60,'externalTimeoutSeconds':59,'terminal':True}
with (a/'stdout.txt').open('w') as out,(a/'stderr.txt').open('w') as err:
 try:
  p=subprocess.Popen(args,stdout=out,stderr=err,start_new_session=True)
  try: status['exitCode']=p.wait(timeout=59);status['timeout']=False
  except subprocess.TimeoutExpired:
   os.killpg(p.pid,signal.SIGKILL);p.wait();status.update(exitCode=p.returncode,timeout=True)
 except BaseException as e:status['launchError']=repr(e)
 finally:
  status['wallSeconds']=time.perf_counter()-t;(a/'runtime.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps({'archive':str(a),'runtime':status}))
if pathlib.Path('/tmp/m31-zero-screen-saved-review.json').exists():
 r=json.loads(pathlib.Path('/tmp/m31-zero-screen-saved-review.json').read_text());print(json.dumps({k:r.get(k) for k in ['passed','checkCount','failedCheckCount','failedChecks','exception','retainedCoverage','scientificQualificationCompleted','performanceQualified','verificationWallSecondsBeforeOutput']}))
