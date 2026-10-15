"""Bounded coordinator observation; no scientific or saved numerical reexecution."""
import time
START=time.monotonic()
from pathlib import Path
import json,os,sys,subprocess,signal,selectors,hashlib

BASE=Path(__file__).resolve().parents[1]
WALL=120;WORK_END=START+117;CLEANUP_END=START+119
CAP=33554432;PROVENANCE_RESERVE=16384;PIPE_CAP=8192;PIPE_TOTAL_CAP=8192
SOURCE='e60702197dde11893f01f01496edafbefb4a43de'
FREEZE='aadba212ed2c2006c4a5e8196df21c04f9d9c478bc5714353ddb6bc5415f81fe'
owned=[]
report={'scope':'One saved-only wrapper and one byte/lifecycle seal; no numerical repeat.','commands':[],'observedIntegrityCandidateVerified':False,'integrityVerified':False,'requiresCallerObservedObserverExit0':True,'decisionVerified':False,'qualified':False,'errors':[],'wallCapSeconds':WALL,'workStopSeconds':117,'cleanupStopSeconds':119,'observerProvenanceByteReserve':PROVENANCE_RESERVE}

def hard_deadline(signum,frame):
 for p,item in owned:
  if not item['ownedProcessGroupAbsent'] and p.poll() is None:
   try:
    if os.getpgid(p.pid)==p.pid:os.killpg(p.pid,signal.SIGKILL)
   except OSError:pass
 os._exit(124)
def soft_deadline(signum,frame):
 report['deadlineReached']=True;report['observedIntegrityCandidateVerified']=False
 signal.signal(signal.SIGALRM,hard_deadline)
 signal.setitimer(signal.ITIMER_REAL,max(.001,START+WALL-time.monotonic()))
 raise TimeoutError('Coordinator work deadline')
signal.signal(signal.SIGALRM,soft_deadline)
signal.setitimer(signal.ITIMER_REAL,max(.001,WORK_END-time.monotonic()))

def require(ok,message):
 if not ok:raise RuntimeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def read(relative,cap=1048576):
 target=BASE/relative
 require(not Path(relative).is_absolute() and '..' not in Path(relative).parts and target.is_file() and not target.is_symlink() and target.resolve()==target,'Contained regular evidence file')
 require(target.stat().st_size<=cap,'Evidence read cap')
 with target.open('rb') as handle:data=handle.read(cap+1)
 require(len(data)<=cap,'Evidence growth cap')
 return data
def load(relative,cap=1048576):return json.loads(read(relative,cap))
def pin(relative):
 data=read(relative);return {'path':relative,'bytes':len(data),'sha256':digest(data)}
def group_absent(p,item):
 if item['ownedProcessGroupAbsent']:return True
 try:os.killpg(p.pid,0)
 except ProcessLookupError:item['ownedProcessGroupAbsent']=True
 return item['ownedProcessGroupAbsent']
def cleanup(p,item,force):
 # Only new-session groups created by this invocation are owned. Never signal a
 # group again once its absence was observed. The fixed checker shares this group.
 if not group_absent(p,item):
  if p.poll() is None:
   try:
    require(os.getpgid(p.pid)==p.pid,'Live owned session leader required')
    os.killpg(p.pid,signal.SIGKILL);item['killSent']=True
   except ProcessLookupError:group_absent(p,item)
  else:
   # Do not signal a possibly reused numeric group after its leader was reaped.
   item['unexpectedLiveGroupAfterCommand']=True
   item['postExitGroupOwnershipUnconfirmed']=True
 remaining=CLEANUP_END-time.monotonic()
 if remaining>0:
  try:p.wait(timeout=min(.5,remaining))
  except subprocess.TimeoutExpired:item['reapTimedOut']=True
 item['exitCode']=p.returncode
 while time.monotonic()<CLEANUP_END and not group_absent(p,item):
  time.sleep(min(.025,max(0,CLEANUP_END-time.monotonic())))
 item['childReaped']=p.returncode is not None

def command(label,args):
 require(time.monotonic()<WORK_END,'No work time remains')
 began=time.monotonic();p=None;selector=None
 item={'command':label,'exitCode':None,'timedOut':False,'outputCapExceeded':False,'ownedByNewSession':True,'ownedProcessGroupAbsent':False,'childReaped':False,'killSent':False,'stdoutBytesObserved':0,'stderrBytesObserved':0,'pipeByteCapEach':PIPE_CAP}
 report['commands'].append(item)
 try:
  p=subprocess.Popen(args,start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  owned.append((p,item));selector=selectors.DefaultSelector()
  for label2,stream in [('stdout',p.stdout),('stderr',p.stderr)]:
   os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,label2)
  while selector.get_map() or p.poll() is None:
   left=WORK_END-time.monotonic()
   if left<=0:item['timedOut']=True;raise TimeoutError('Command work deadline')
   for key,event in selector.select(min(.05,left)):
    field=key.data+'BytesObserved';want=min(4096,PIPE_CAP-item[field]+1)
    try:chunk=os.read(key.fileobj.fileno(),want)
    except BlockingIOError:continue
    if not chunk:selector.unregister(key.fileobj);continue
    item[field]+=len(chunk)
    if item[field]>PIPE_CAP:item['outputCapExceeded']=True;raise RuntimeError('Command output cap')
    if sum(x['stdoutBytesObserved']+x['stderrBytesObserved'] for x in report['commands'])>PIPE_TOTAL_CAP:item['outputCapExceeded']=True;raise RuntimeError('Combined command output cap')
  item['exitCode']=p.wait(timeout=max(.001,min(.25,WORK_END-time.monotonic())))
 finally:
  if selector is not None:selector.close()
  if p is not None:
   try:cleanup(p,item,p.poll() is None)
   finally:
    for stream in [p.stdout,p.stderr]:
     if stream is not None:stream.close()
  item['observedWallSeconds']=time.monotonic()-began
 require(item['ownedProcessGroupAbsent'] and item['childReaped'] and not item.get('unexpectedLiveGroupAfterCommand') and not item.get('reapTimedOut') and not item['timedOut'] and not item['outputCapExceeded'],'Command closure failed')
 return item

try:
 require(len(sys.argv)==2,'Supply the pinned Node executable')
 rb=read('review/review-freeze.json');rf=json.loads(rb)
 expected_sources=sorted(['review/IMPLEMENTATION.md','review/STATIC-CHALLENGE.md','review/observe-review.py','review/source/review.cjs','review/source/run-once.py','review/source/seal-review.py'])
 require(rf['kind']=='frozen-saved-review' and rf['sourceCommit']==SOURCE and rf['sourceFreezeSHA256']==FREEZE and rf['wallSeconds']==120 and rf['outputByteCap']==CAP and rf['invocations']==1,'Review freeze identity')
 require(sorted(p['path'] for p in rf['files'])==expected_sources,'All six review source pins')
 for p in rf['files']:require(pin(p['path'])==p,'Review source pin mismatch')
 report['reviewFreezeSHA256']=digest(rb)
 wrapper=command('saved-review-wrapper',[sys.executable,str(BASE/'review/source/run-once.py'),sys.argv[1]])
 completion=command('byte-only-completion-seal',[sys.executable,str(BASE/'review/source/seal-review.py'),'--complete-review',str(wrapper['exitCode']),str(wrapper['observedWallSeconds'])])
 receipt=load('review/results/completion.json',4096);budget=load('review/results/budget.json',65536);worker=load('review/results/review.json')
 expected_names=sorted(['budget.json','completion.json','review.json','sole-review.lock','stderr.txt','stdout.txt'])
 require(sorted(p.name for p in (BASE/'review/results').iterdir())==expected_names,'Exact six review outputs')
 output_pins=[pin('review/results/'+name) for name in expected_names]
 prior=[p for p in output_pins if not p['path'].endswith('/completion.json')];prior_bytes=sum(p['bytes'] for p in prior);receipt_bytes=len(read('review/results/completion.json',4096));six_bytes=prior_bytes+receipt_bytes
 require(sorted(receipt['priorOutputs'],key=lambda p:p['path'])==prior,'Completion prior output byte pins')
 require(receipt['receiptBytes']==receipt_bytes and receipt['priorOutputBytes']==prior_bytes and receipt['finalOutputBytes']==six_bytes and receipt['finalOutputFiles']==6 and receipt['outputByteCap']==CAP and receipt['receiptByteReserve']==4096,'Completion exact byte/file account')
 require(budget['outputFiles']==5 and budget['outputBytes']==prior_bytes and budget['budgetBytes']==len(read('review/results/budget.json',65536)) and budget['nonBudgetBytes']==prior_bytes-budget['budgetBytes'],'Wrapper exact byte/file account')
 require(budget['completionReceiptByteReserve']==4096 and budget['observerProvenanceByteReserve']==PROVENANCE_RESERVE and receipt['observerProvenanceByteReserve']==PROVENANCE_RESERVE and six_bytes+PROVENANCE_RESERVE<=CAP,'Reserved observer output bytes')
 require(worker.get('completed') is True and worker.get('integrityVerified') is True and worker.get('terminalFailureVerified') is True and worker.get('status')=='terminal-failure-integrity-verified' and worker.get('sourceCommit')==SOURCE and worker.get('sourceFreezeSHA256')==FREEZE,'Worker completion/identity')
 require(budget.get('terminal') is True and budget.get('active') is False and budget.get('candidateIntegrityVerified') is True and budget.get('integrityVerified') is False and budget.get('requiresSuccessfulSupervisorExit') is True and budget.get('exitCode')==0 and budget.get('workerCompleted') is True and budget.get('workerIntegrityVerified') is True and budget.get('reviewerChildConfirmedReaped') is True and budget.get('timeout') is False and budget.get('outputCapExceeded') is False and budget.get('withinOutputCap') is True and budget.get('errors')==[],'Wrapper candidate and closure')
 require(receipt.get('kind')=='caller-observed-review-completion' and receipt.get('terminal') is True and receipt.get('candidateIntegrityVerified') is True and receipt.get('integrityVerified') is False and receipt.get('externalCompletionObservationRequired') is True and receipt.get('errors')==[] and receipt.get('observedSupervisorExitCode')==wrapper['exitCode'] and receipt.get('observedSupervisorWallSeconds')==wrapper['observedWallSeconds'],'Completion conditional status/observation')
 for record in [worker,budget,receipt]:require(record.get('decisionVerified') is False and record.get('qualified') is False,'Failed science must remain unqualified')
 require(receipt.get('sourceFreezeSHA256')==FREEZE and receipt.get('reviewFreezeSHA256')==digest(rb) and budget.get('sourceFreezeSHA256')==FREEZE and budget.get('reviewFreezeSHA256')==digest(rb) and budget.get('scienceManifestSHA256')==rf['scienceManifest']['sha256'],'Lifecycle freeze bindings')
 require(wrapper['exitCode']==0 and completion['exitCode']==0 and all(i['ownedProcessGroupAbsent'] and i['childReaped'] for p,i in owned),'Both actual exits and group closure')
 require(read('review/review-freeze.json')==rb,'Review freeze stable')
 for p in rf['files']:require(pin(p['path'])==p,'Review source stable')
 report['reviewOutputFiles']=6;report['reviewOutputBytes']=six_bytes;report['completionSHA256']=digest(read('review/results/completion.json',4096));report['observedIntegrityCandidateVerified']=True
except BaseException as error:
 report['errors'].append({'type':type(error).__name__,'reason':str(error) if isinstance(error,RuntimeError) else 'Coordinator operation failed'})
 report['observedIntegrityCandidateVerified']=False
finally:
 for p,item in owned:
  if not item['ownedProcessGroupAbsent'] or not item['childReaped']:
   try:cleanup(p,item,True)
   except BaseException as error:report['errors'].append({'type':type(error).__name__,'reason':'Coordinator cleanup failed'})
 if any(not item['ownedProcessGroupAbsent'] or not item['childReaped'] for p,item in owned):report['observedIntegrityCandidateVerified']=False

report['totalObservedWallSecondsBeforeSummary']=time.monotonic()-START
report['withinCombinedWallCap']=report['totalObservedWallSecondsBeforeSummary']<WALL
report['elapsedScope']='Includes wrapper and completion startup/work/writes/closure; sampled before this bounded stdout summary. Caller must observe observer exit0.'
report['observedIntegrityCandidateVerified']=report['observedIntegrityCandidateVerified'] and report['withinCombinedWallCap'] and not report['errors']
report['observedCommandPipeBytes']=sum(x['stdoutBytesObserved']+x['stderrBytesObserved'] for x in report['commands'])
report['commandPipeTotalByteCap']=PIPE_TOTAL_CAP
report['outputAccountingComplete']='reviewOutputBytes' in report
report['observerSummaryBytes']=0;report['accountedTotalOutputBytes']=0 if report['outputAccountingComplete'] else None
for _ in range(16):
 encoded=(json.dumps(report,sort_keys=True)+'\n').encode();total=report['reviewOutputBytes']+report['observedCommandPipeBytes']+len(encoded) if report['outputAccountingComplete'] else None
 if report['observerSummaryBytes']==len(encoded) and report['accountedTotalOutputBytes']==total:break
 report['observerSummaryBytes']=len(encoded);report['accountedTotalOutputBytes']=total
if len(encoded)+report['observedCommandPipeBytes']>PROVENANCE_RESERVE or (report['accountedTotalOutputBytes'] is not None and report['accountedTotalOutputBytes']>CAP) or report['observerSummaryBytes']!=len(encoded):os._exit(125)
# One bounded public observation, retained by the caller as publication provenance;
# it is not a seventh file in review/results. Timers remain armed through exit.
sys.stdout.buffer.write(encoded);sys.stdout.buffer.flush()
raise SystemExit(0 if report['observedIntegrityCandidateVerified'] else 1)
