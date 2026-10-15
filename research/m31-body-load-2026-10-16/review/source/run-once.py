"""One permanent 120 s / 32 MiB saved-only review reservation and supervisor."""
import time
START=time.monotonic()
from pathlib import Path
import os,sys,json,hashlib,subprocess,signal,resource
BASE=Path(__file__).resolve().parents[2]
REPO=BASE.parents[1]
REVIEW=BASE/'review'
OUT=REVIEW/'results'
CAP=33554432
WALL=120
SOURCE='e60702197dde11893f01f01496edafbefb4a43de'
FREEZE='aadba212ed2c2006c4a5e8196df21c04f9d9c478bc5714353ddb6bc5415f81fe'
record={'version':1,'terminal':False,'active':True,'attempts':1,'wallCapSeconds':WALL,'softStopSeconds':118,'outputByteCap':CAP,'completionReceiptByteReserve':4096,'observerProvenanceByteReserve':16384,'status':'reserved','retryPermitted':False,'decisionVerified':False,'qualified':False,'integrityVerified':False,'candidateIntegrityVerified':False,'requiresSuccessfulSupervisorExit':True,'timeout':False,'outputCapExceeded':False,'exitCode':None,'reviewerChildConfirmedReaped':False,'errors':[]}
p=None
def hard_deadline(signum,frame):
 # No filesystem operations at the hard deadline. A partial/provisional budget
 # is failure evidence; observed supervisor exit 124 can never certify integrity.
 if p is not None and p.returncode is None:
  try:p.kill()
  except OSError:pass
 os._exit(124)
def soft_deadline(signum,frame):
 record['timeout']=True;record['candidateIntegrityVerified']=False
 signal.signal(signal.SIGALRM,hard_deadline)
 signal.setitimer(signal.ITIMER_REAL,max(.001,WALL-(time.monotonic()-START)))
 raise TimeoutError('Whole review soft deadline')
# Armed before any campaign/output I/O; remains armed through interpreter exit.
signal.signal(signal.SIGALRM,soft_deadline)
signal.setitimer(signal.ITIMER_REAL,max(.001,118-(time.monotonic()-START)))
OUT.mkdir(exist_ok=True)
with (OUT/'sole-review.lock').open('x') as lock:lock.write('One saved-only review reserved. Permanent lock; never remove.\n')
ledger=OUT/'budget.json'
with ledger.open('x') as output:output.write(json.dumps(record,indent=2)+'\n')
def require(value,message):
 if not value:raise RuntimeError(message)
def read(path):
 require(path.is_file() and not path.is_symlink() and path.resolve()==path,'Regular contained input required')
 return path.read_bytes()
def digest(data):return hashlib.sha256(data).hexdigest()
def pinned(root,pin):
 relative=Path(pin['path']);require(not relative.is_absolute() and '..' not in relative.parts,'Relative pin path')
 data=read(root/relative);require(len(data)==pin['bytes'] and digest(data)==pin['sha256'],'Pinned byte mismatch');return data
def output_bytes():
 paths=list(OUT.iterdir());require(all(p.is_file() and not p.is_symlink() for p in paths),'Unexpected review output entry');return sum(p.stat().st_size for p in paths)
def child_limit():
 # Expected source writes one <=1 MiB report; stdout and stderr each <=8 MiB.
 # This hard per-file bound plus the fixed file inventory leaves ample cap reserve.
 resource.setrlimit(resource.RLIMIT_FSIZE,(8388608,8388608))

try:
 require(len(sys.argv)==2,'Supply only the pinned Node executable path')
 require(sorted(p.name for p in OUT.iterdir())==['budget.json','sole-review.lock'],'Preexisting review output')
 rb=read(REVIEW/'review-freeze.json');rf=json.loads(rb)
 require(rf['kind']=='frozen-saved-review' and rf['sourceCommit']==SOURCE and rf['sourceFreezeSHA256']==FREEZE and rf['invocations']==1 and rf['wallSeconds']==WALL and rf['outputByteCap']==CAP,'Review freeze contract')
 require(sorted(p['path'] for p in rf['files'])==sorted(['review/IMPLEMENTATION.md','review/STATIC-CHALLENGE.md','review/observe-review.py','review/source/review.cjs','review/source/run-once.py','review/source/seal-review.py']),'Review source inventory')
 for pin in rf['files']:pinned(BASE,pin)
 require(rf['scienceManifest']['path']=='review/science-manifest.json','Manifest path');manifest=json.loads(pinned(BASE,rf['scienceManifest']))
 require(manifest['kind']=='sealed-terminal-science' and manifest['sourceCommit']==SOURCE and manifest['sourceFreezeSHA256']==FREEZE,'Manifest contract')
 fb=read(BASE/'freeze.json');require(digest(fb)==FREEZE,'Source freeze identity');frozen=json.loads(fb)
 require(manifest['sourceFiles']==frozen['files'],'Original source pins retained')
 for pin in frozen['files']:pinned(REPO,pin)
 for pin in manifest['terminalFiles']:pinned(BASE,pin)
 closure=json.loads(read(BASE/'results/budget.json'));require(closure['terminal'] is True and closure['active'] is False and closure['status']=='closed' and closure['processGroupCleanup']['confirmedAbsent'] is True,'Science not terminal/closed')
 node=Path(sys.argv[1]).resolve();runtime=json.loads(read(BASE/'runtime-provenance.json'));node_bytes=read(node);np=runtime['pins'][0];require(len(node_bytes)==np['bytes'] and digest(node_bytes)==np['sha256'],'Node runtime mismatch')
 require(time.monotonic()-START<WALL-2,'Review preflight exhausted wall budget')
 record['reviewFreezeSHA256']=digest(rb);record['scienceManifestSHA256']=rf['scienceManifest']['sha256'];record['sourceFreezeSHA256']=FREEZE
 env=os.environ.copy();env.pop('NODE_OPTIONS',None);env.pop('NODE_PATH',None);env['M31_SAVED_REVIEW_RESERVED']='1'
 # A fixed executable/script pair; no arbitrary checker or scientific command.
 with (OUT/'stdout.txt').open('xb') as stdout,(OUT/'stderr.txt').open('xb') as stderr:
  # Same group as the wrapper: the coordinator owns that group and can stop the
  # whole invocation even if its outer deadline precedes an internal deadline.
  p=subprocess.Popen([str(node),str(REVIEW/'source/review.cjs')],stdout=stdout,stderr=stderr,cwd=REPO,env=env,preexec_fn=child_limit)
  while p.poll() is None:
   elapsed=time.monotonic()-START;total=output_bytes()
   if elapsed>=WALL-1 or total>CAP-65536:
    record['timeout']=elapsed>=WALL-1;record['outputCapExceeded']=total>CAP-65536
    p.kill();p.wait(timeout=.5);break
   try:p.wait(timeout=min(.05,max(.001,WALL-1-elapsed)))
   except subprocess.TimeoutExpired:pass
  record['exitCode']=p.returncode
 # Reconcile the worker result; failed review remains failed and is never retried.
 if (OUT/'review.json').is_file():
  result=json.loads(read(OUT/'review.json'));record['workerCompleted']=result.get('completed') is True;record['workerIntegrityVerified']=result.get('integrityVerified') is True
  require(result.get('decisionVerified') is False and result.get('qualified') is False,'Review must not qualify failed science')
 else:record['workerCompleted']=False;record['workerIntegrityVerified']=False
 require(read(REVIEW/'review-freeze.json')==rb,'Review freeze changed during invocation')
 for pin in rf['files']:pinned(BASE,pin)
 pinned(BASE,rf['scienceManifest'])
 for pin in manifest['terminalFiles']:pinned(BASE,pin)
except BaseException as error:
 # Public diagnostics avoid local paths; no repair invocation follows.
 record['errors'].append({'type':type(error).__name__,'message':str(error) if isinstance(error,RuntimeError) else 'Supervisor operation failed'})
finally:
 if p is not None and p.poll() is None:
  try:p.kill();p.wait(timeout=.5)
  except (OSError,subprocess.SubprocessError) as error:record['errors'].append({'type':type(error).__name__,'message':'Child termination failed'})
 # The frozen reviewer spawns no children. poll/wait reaps this exact child;
 # the coordinator separately confirms the wrapper's whole group has vanished.
 record['reviewerChildConfirmedReaped']=p is None or p.poll() is not None
 if not record['reviewerChildConfirmedReaped']:record['errors'].append({'type':'UnconfirmedClosure','message':'Reviewer child reaping unconfirmed'})
 record.update(terminal=True,active=False,status='closure-record-awaiting-supervisor-exit')
 record['elapsedMeasurement']='Sample immediately before terminal receipt serialization/write; whole invocation including that write remains under the asynchronous 120 s deadline. Successful supervisor exit 0 must be independently observed.'
 try:
  expected={'sole-review.lock','budget.json','stdout.txt','stderr.txt','review.json'}
  require(all(p.name in expected and p.is_file() and not p.is_symlink() for p in OUT.iterdir()),'Unexpected review output file')
  record['outputFiles']=len(list(OUT.iterdir()));record['nonBudgetBytes']=sum(p.stat().st_size for p in OUT.iterdir() if p!=ledger);record['budgetBytes']=0;record['outputBytes']=0;record['withinOutputCap']=False
  record['elapsedAtTerminalReceiptStartSeconds']=time.monotonic()-START
  record['candidateIntegrityVerified']=record.get('exitCode')==0 and record.get('workerCompleted') is True and record.get('workerIntegrityVerified') is True and not record['errors'] and not record['timeout'] and not record['outputCapExceeded'] and record['reviewerChildConfirmedReaped'] and record['elapsedAtTerminalReceiptStartSeconds']<118
  for _ in range(16):
   encoded=(json.dumps(record,indent=2)+'\n').encode();total=record['nonBudgetBytes']+len(encoded);within=total<=CAP-record['completionReceiptByteReserve']-record['observerProvenanceByteReserve']
   if len(encoded)==record['budgetBytes'] and total==record['outputBytes'] and within==record['withinOutputCap']:break
   record['budgetBytes']=len(encoded);record['outputBytes']=total;record['withinOutputCap']=within
   if not within:record['candidateIntegrityVerified']=False
  encoded=(json.dumps(record,indent=2)+'\n').encode();require(len(encoded)==record['budgetBytes'] and record['outputBytes']==record['nonBudgetBytes']+len(encoded),'Review ledger size stabilization')
  ledger.write_bytes(encoded)
 except BaseException:
  record['candidateIntegrityVerified']=False
  # Best-effort final failure receipt; a failure is never a retry authorization.
  record['errors'].append({'type':'FinalizationError','message':'Review output finalization failed'})
  ledger.write_text(json.dumps(record,indent=2)+'\n')

print(json.dumps({'status':record['status'],'candidateIntegrityVerified':record['candidateIntegrityVerified'],'integrityVerified':False,'requiresSuccessfulSupervisorExit':True,'decisionVerified':False,'qualified':False,'elapsedAtExitSummarySeconds':time.monotonic()-START}))
raise SystemExit(0 if record['candidateIntegrityVerified'] else 1)
