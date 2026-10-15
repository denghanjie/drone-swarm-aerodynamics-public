"""Byte-only terminal science/review sealer. Never imports or evaluates science."""
from pathlib import Path
import hashlib,json,sys,signal,os,math

BASE=Path(__file__).resolve().parents[2]
REPO=BASE.parents[1]
REVIEW=BASE/'review'
SOURCE='e60702197dde11893f01f01496edafbefb4a43de'
FREEZE='aadba212ed2c2006c4a5e8196df21c04f9d9c478bc5714353ddb6bc5415f81fe'
def require(value,message):
 if not value:raise SystemExit(message)
def read(path):
 require(path.is_file() and not path.is_symlink() and path.resolve()==path,'Regular contained file required')
 return path.read_bytes()
def digest(data):return hashlib.sha256(data).hexdigest()
def pin(path,root):
 data=read(path);return {'path':path.relative_to(root).as_posix(),'bytes':len(data),'sha256':digest(data)}
def exclusive(path,value):
 data=(json.dumps(value,indent=2)+'\n').encode()
 # Preserve a partial write as a terminal preparation failure. Never replace it.
 with path.open('xb') as output:output.write(data)
 return {'path':path.relative_to(BASE).as_posix(),'bytes':len(data),'sha256':digest(data)}

def complete_review(exit_text,wall_text):
 """Seal caller-observed process closure only; no numerical checker invocation."""
 signal.signal(signal.SIGALRM,lambda signum,frame:os._exit(124))
 signal.setitimer(signal.ITIMER_REAL,2)
 observed_exit=int(exit_text);observed_wall=float(wall_text)
 require(math.isfinite(observed_wall) and observed_wall>=0,'Finite caller elapsed time required')
 out=REVIEW/'results';target=out/'completion.json'
 require(not target.exists(),'Completion receipt is immutable')
 paths=sorted(out.iterdir());require(all(p.is_file() and not p.is_symlink() for p in paths),'Regular review outputs required')
 existing=[pin(p,BASE) for p in paths];prior_bytes=sum(p['bytes'] for p in existing)
 errors=[];budget={};worker={}
 for name,destination in [('budget.json',budget),('review.json',worker)]:
  try:destination.update(json.loads(read(out/name)))
  except (OSError,ValueError,TypeError):errors.append('Missing or malformed '+name)
 expected={'sole-review.lock','budget.json','stdout.txt','stderr.txt','review.json'}
 if {p.name for p in paths}!=expected:errors.append('Incomplete or unexpected review output inventory')
 if budget.get('outputBytes')!=prior_bytes or budget.get('outputFiles')!=len(paths):errors.append('Pre-completion byte/file accounting mismatch')
 if budget.get('completionReceiptByteReserve')!=4096 or budget.get('observerProvenanceByteReserve')!=16384 or prior_bytes>33554432-4096-16384:errors.append('Completion/observer reserve unavailable')
 review_freeze_bytes=read(REVIEW/'review-freeze.json');review_freeze=json.loads(review_freeze_bytes)
 if digest(review_freeze_bytes)!=budget.get('reviewFreezeSHA256') or review_freeze.get('sourceFreezeSHA256')!=FREEZE or review_freeze.get('sourceCommit')!=SOURCE:errors.append('Review freeze provenance mismatch')
 if review_freeze.get('scienceManifest',{}).get('sha256')!=budget.get('scienceManifestSHA256'):errors.append('Science manifest provenance mismatch')
 if worker.get('sourceCommit')!=SOURCE or worker.get('sourceFreezeSHA256')!=FREEZE:errors.append('Worker source provenance mismatch')
 candidate=(observed_exit==0 and observed_wall<118 and not errors and budget.get('candidateIntegrityVerified') is True and budget.get('integrityVerified') is False and budget.get('requiresSuccessfulSupervisorExit') is True and budget.get('terminal') is True and budget.get('active') is False and budget.get('exitCode')==0 and budget.get('workerCompleted') is True and budget.get('workerIntegrityVerified') is True and budget.get('reviewerChildConfirmedReaped') is True and budget.get('timeout') is False and budget.get('outputCapExceeded') is False and budget.get('withinOutputCap') is True and budget.get('errors')==[] and worker.get('completed') is True and worker.get('integrityVerified') is True and worker.get('terminalFailureVerified') is True and worker.get('decisionVerified') is False and worker.get('qualified') is False)
 receipt={'version':1,'kind':'caller-observed-review-completion','observationSource':'Caller-supplied wrapper exit/time; final acceptance also requires observed completion-process exit, owned-group absence and total chain wall below120s.','observedSupervisorExitCode':observed_exit,'observedSupervisorWallSeconds':observed_wall,'internalLifecycleTimerSeconds':2,'internalTimerScope':'Armed on completion-mode entry; excludes interpreter startup/imports. Outer caller timeout covers the whole process.','terminal':True,'integrityVerified':False,'candidateIntegrityVerified':candidate,'externalCompletionObservationRequired':True,'decisionVerified':False,'qualified':False,'retryPermitted':False,'priorOutputs':existing,'priorOutputBytes':prior_bytes,'receiptByteReserve':4096,'observerProvenanceByteReserve':16384,'receiptBytes':0,'finalOutputBytes':0,'finalOutputFiles':len(paths)+1,'outputByteCap':33554432,'errors':errors,'sourceFreezeSHA256':FREEZE,'reviewFreezeSHA256':digest(review_freeze_bytes)}
 for _ in range(16):
  encoded=(json.dumps(receipt,indent=2)+'\n').encode();n=len(encoded)
  if n==receipt['receiptBytes'] and receipt['finalOutputBytes']==prior_bytes+n:break
  receipt['receiptBytes']=n;receipt['finalOutputBytes']=prior_bytes+n
 require(len(encoded)==receipt['receiptBytes'] and len(encoded)<=4096 and receipt['finalOutputBytes']==prior_bytes+len(encoded) and receipt['finalOutputBytes']+16384<=33554432,'Completion receipt accounting/cap')
 with target.open('xb') as output:output.write(encoded)
 print(json.dumps({'completionSHA256':digest(encoded),'candidateIntegrityVerified':candidate,'integrityVerified':False,'externalCompletionObservationRequired':True,'decisionVerified':False,'qualified':False,'finalOutputBytes':receipt['finalOutputBytes']}))
 raise SystemExit(0 if candidate else 1)

if len(sys.argv)==4 and sys.argv[1]=='--complete-review':complete_review(sys.argv[2],sys.argv[3])
require(len(sys.argv)==1,'Use no arguments to prepare seals, or --complete-review EXIT ELAPSED after caller-observed wrapper termination')

require(not (REVIEW/'science-manifest.json').exists() and not (REVIEW/'review-freeze.json').exists(),'Existing review seal is immutable')
require(not (REVIEW/'results').exists() or not any((REVIEW/'results').iterdir()),'Review already reserved or invoked')
review_files=['review/IMPLEMENTATION.md','review/STATIC-CHALLENGE.md','review/observe-review.py','review/source/review.cjs','review/source/run-once.py','review/source/seal-review.py']
for name in review_files:require(len(read(BASE/name))>0,'Missing review source/static challenge')
freeze_bytes=read(BASE/'freeze.json');require(digest(freeze_bytes)==FREEZE,'Published source freeze mismatch')
freeze=json.loads(freeze_bytes)
require(len(freeze['files'])==50 and len({p['path'] for p in freeze['files']})==50,'Source pin coverage')
for p in freeze['files']:
 path=REPO/p['path'];require(path.is_relative_to(REPO) and '..' not in Path(p['path']).parts,'Source pin containment')
 require(pin(path,REPO)==p,'Frozen source changed')
worker=json.loads(read(BASE/'raw/result.json'));budget=json.loads(read(BASE/'results/budget.json'));started=json.loads(read(BASE/'raw/started.json'))
require(worker['terminal'] is True and worker['status']=='failed' and worker['qualified'] is False,'Expected terminal failed science')
require(budget['terminal'] is True and budget['active'] is False and budget['status']=='closed' and budget['attempts']==1 and budget['exitCode']==1 and budget['retryPermitted'] is False,'Expected terminal supervisor closure')
require(budget['processGroupCleanup']['confirmedAbsent'] is True,'Owned science groups not confirmed absent')
require(started['sourceCommit']==SOURCE and started['freezeSha256']==FREEZE and worker['sourceCommit']==SOURCE,'Recorded source provenance')
require(read(BASE/'raw/result.json')==read(BASE/'results/result.json'),'Worker final copies differ')
terminal=[]
for directory in ['raw','results']:
 children=sorted((BASE/directory).iterdir())
 require(all(p.is_file() and not p.is_symlink() for p in children),'Non-file terminal evidence entry')
 terminal.extend(pin(p,BASE) for p in children)
require(len([p for p in terminal if p['path'].startswith('raw/')])==14 and len([p for p in terminal if p['path'].startswith('results/')])==5,'Unexpected terminal evidence inventory')
require(sum(p['bytes'] for p in terminal if p['path'].startswith('raw/'))==budget['rawBytes'],'Raw size changed after closure')
require(sum(p['bytes'] for p in terminal if p['path'].startswith('results/'))==budget['resultBytes'],'Result size changed after closure')
manifest={'kind':'sealed-terminal-science','sourceCommit':SOURCE,'sourceFreezeSHA256':FREEZE,'scienceStatus':worker['status'],'scientificQualified':False,'externalClosure':'results/budget.json','sourceFiles':freeze['files'],'terminalFiles':terminal,'limits':'Byte inventory only. No scientific check performed by sealer; private exception and process receipts are not included.'}
manifest_pin=exclusive(REVIEW/'science-manifest.json',manifest)
review_freeze={'kind':'frozen-saved-review','sourceCommit':SOURCE,'sourceFreezeSHA256':FREEZE,'invocations':1,'wallSeconds':120,'outputByteCap':33554432,'scienceManifest':manifest_pin,'files':[pin(BASE/name,BASE) for name in review_files],'decision':'Scientific decisionVerified=false and qualified=false. Integrity may pass for the preserved terminal environment failure. No retry after review failure.'}
freeze_pin=exclusive(REVIEW/'review-freeze.json',review_freeze)
print(json.dumps({'scienceManifest':manifest_pin,'reviewFreeze':freeze_pin,'reviewExecuted':False}))
