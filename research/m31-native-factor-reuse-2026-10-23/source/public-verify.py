"""Administrative identity checks only. Requires frozen commit/manifest CLI pins."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
import argparse, base64, datetime, hashlib, json, os, re, selectors, signal, subprocess, tempfile, threading, time

ROOT=Path(__file__).resolve().parents[3]
REL='research/m31-native-factor-reuse-2026-10-23'
BASE=None
REPO='denghanjie/drone-swarm-aerodynamics-public'
GH='/opt/homebrew/bin/gh'
START=time.monotonic();LOCK=threading.Lock();STOP=threading.Event();EVENTS=[];CAPTURED=0;VERIFIED=[]
ENV={k:v for k,v in os.environ.items() if k not in ('GH_DEBUG','DEBUG','GIT_EXTERNAL_DIFF','GIT_DIFF_OPTS','GIT_PAGER')}
ENV.update(GH_PROMPT_DISABLED='1',GH_NO_UPDATE_NOTIFIER='1',GH_NO_EXTENSION_UPDATE_NOTIFIER='1',GIT_NO_REPLACE_OBJECTS='1',GIT_TERMINAL_PROMPT='0')
class BudgetFailure(Exception):pass
class AttemptTimeout(Exception):pass
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def bid(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def remaining():
    value=BOUNDS['overallSeconds']-(time.monotonic()-START)
    if value<=0:STOP.set();raise BudgetFailure('overall-'+str(BOUNDS['overallSeconds'])+'-second-limit')
    return value
def file_id(path,deadline=None):
    h=hashlib.sha256();size=0
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):
            if deadline is not None and time.monotonic()>deadline:raise AttemptTimeout('local-identity-45-second-limit')
            remaining();size+=len(block);h.update(block)
    return {'bytes':size,'sha256':h.hexdigest()}
def same(pin,got):return all(pin[k]==got[k] for k in ('bytes','sha256'))
def record(event):
    with LOCK:
        numbered={'event':len(EVENTS)+1,**event};EVENTS.append(numbered)
        with JOURNAL.open('a') as f:f.write(json.dumps(numbered,separators=(',',':'))+'\n')
    return numbered
def capture_gh(args):
    global CAPTURED
    if STOP.is_set():raise BudgetFailure('verification-stopped')
    duration=min(45,remaining());begin=time.monotonic();out=bytearray();err=bytearray();failure=None
    p=subprocess.Popen(args,cwd=ROOT,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    selector=selectors.DefaultSelector()
    for stream,label in ((p.stdout,'stdout'),(p.stderr,'stderr')):
        os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,label)
    try:
        while selector.get_map():
            left=duration-(time.monotonic()-begin)
            if left<=0:
                if time.monotonic()-START>=BOUNDS['overallSeconds']:raise BudgetFailure('overall-'+str(BOUNDS['overallSeconds'])+'-second-limit')
                raise AttemptTimeout('api-attempt-45-second-limit')
            if STOP.is_set():raise BudgetFailure('verification-stopped')
            for key,_ in selector.select(min(left,.2)):
                with LOCK:
                    available=BOUNDS['aggregateCapturedPublicBytes']-CAPTURED
                    if available<=0:raise BudgetFailure('aggregate-captured-'+str(BOUNDS['aggregateCapturedPublicBytes'])+'-byte-limit')
                    data=os.read(key.fileobj.fileno(),min(65536,available));CAPTURED+=len(data)
                if not data:selector.unregister(key.fileobj);continue
                (out if key.data=='stdout' else err).extend(data)
        returncode=p.wait(timeout=max(.001,duration-(time.monotonic()-begin)))
    except BaseException as error:
        failure=error
        if isinstance(error,BudgetFailure):STOP.set()
        if p.poll() is None:os.killpg(p.pid,signal.SIGKILL)
        p.wait(timeout=2);returncode=p.returncode
    finally:selector.close();p.stdout.close();p.stderr.close()
    return bytes(out),bytes(err),returncode,failure,time.monotonic()-begin
def identity_read(mode,path,pin,commit=None,local_proof=None):
    for attempt in (1,2,3):
        begin=time.monotonic();event={'operation':mode,'path':path,'attempt':attempt}
        if commit:event['commit']=commit
        try:
            if STOP.is_set():raise BudgetFailure('verification-stopped')
            deadline=begin+min(45,remaining())
            if mode=='local':
                candidate=ROOT/path;assert candidate.resolve().is_relative_to(ROOT) and candidate.is_file() and not candidate.is_symlink(),'unsafe-local-path'
                assert all(not (ROOT/parent).is_symlink() for parent in candidate.relative_to(ROOT).parents),'symlinked-parent'
                h256=hashlib.sha256();h1=hashlib.sha1(('blob '+str(pin['bytes'])+'\0').encode());n=0
                with candidate.open('rb') as f:
                    for block in iter(lambda:f.read(1048576),b''):
                        if time.monotonic()>deadline:raise AttemptTimeout('local-identity-45-second-limit')
                        remaining();n+=len(block);h256.update(block);h1.update(block)
                got={'bytes':n,'sha256':h256.hexdigest()};event['gitBlobSha1']=h1.hexdigest()
                if pin.get('gitBlobOid'):assert pin['gitBlobOid']==event['gitBlobSha1'],'declared-input-blob-identity'
            else:
                assert local_proof is not None and local_proof['passed'] and local_proof['path']==path and same(pin,local_proof)
                result=subprocess.run(['git','ls-tree','--full-tree','-z',commit,'--',path],cwd=ROOT,env=ENV,capture_output=True,timeout=max(.001,deadline-time.monotonic()),check=True)
                records=result.stdout.split(b'\0');assert len(records)==2 and records[-1]==b'','one-exact-tree-entry-required'
                meta,tree_path=records[0].split(b'\t',1);mode_word,type_word,oid=meta.decode('ascii').split(' ')
                assert tree_path==path.encode('utf8') and type_word=='blob' and mode_word in ('100644','100755'),'exact-ordinary-blob-required'
                assert re.fullmatch('[0-9a-f]{40}',oid) and oid==local_proof['gitBlobSha1'],'local-blob-tree-identity-mismatch'
                if pin.get('gitBlobOid'):assert oid==pin['gitBlobOid'],'declared-input-tree-identity'
                event.update(gitBlobSha1=oid,gitTreeMode=mode_word,treeMetadata=bid(result.stdout),localIdentityEvent=local_proof['event'],binding='Fresh exact-commit tree metadata plus freshly streamed local Git blob SHA-1 and SHA-256; no Git blob extraction.')
                got={'bytes':local_proof['bytes'],'sha256':local_proof['sha256']}
            assert same(pin,got),'identity-mismatch'
            return record({**event,'passed':True,**got,'wallSeconds':time.monotonic()-begin})
        except Exception as error:
            record({**event,'passed':False,'errorType':type(error).__name__,'detail':str(error).replace(str(ROOT),'[repository]')[:500],'wallSeconds':time.monotonic()-begin})
            if isinstance(error,BudgetFailure):raise
    raise RuntimeError('three-identity-attempts-exhausted:'+mode+':'+path)

PHASE_BOUNDS={
 'source':{'maxConcurrentTransfers':2,'attemptsPerIdentity':3,'secondsPerAttempt':45,'overallSeconds':900,'aggregateCapturedPublicBytes':536870912},
 'result':{'maxConcurrentTransfers':4,'attemptsPerIdentity':3,'secondsPerAttempt':45,'overallSeconds':3600,'aggregateCapturedPublicBytes':805306368}
}

def unique(items):
 out={}
 for key,value in items:
  assert key not in out,'duplicate-administrative-json-key'
  out[key]=value
 return out

def invalid_constant(value):raise ValueError('nonfinite-administrative-json:'+value)
def parse_admin(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid_constant)
def admin_file(path,pin=None):
 raw=(ROOT/path).read_bytes()
 if pin is not None:assert same(pin,bid(raw)),'administrative-identity-mismatch:'+path
 return parse_admin(raw)

def route_for(path,pin):
 if pin is None:return 'repository-public-metadata'
 if re.search(r'\.(?:png|jpe?g|gif|webp)$',path,re.I) and pin['bytes']<1048576:return 'public-contents-json-base64'
 if re.search(r'\.(?:png|jpe?g|gif|webp|pdf|zip|gz|bz2|xz|bin|part\d+)$',path,re.I):return 'public-git-blob-json-base64'
 return 'public-contents-api'

def public(path,pin=None,git_blob=None,keep=False):
 mode=route_for(path,pin)
 if mode=='repository-public-metadata':endpoint='repos/'+REPO
 elif mode=='public-git-blob-json-base64':
  assert re.fullmatch('[0-9a-f]{40}',git_blob or ''),'required-git-blob-id'
  endpoint='repos/'+REPO+'/git/blobs/'+git_blob
 else:endpoint='repos/'+REPO+'/contents/'+quote(path,safe='/')+'?ref='+ARGS.commit
 accept='application/vnd.github.raw+json' if mode=='public-contents-api' else 'application/vnd.github+json'
 for attempt in (1,2,3):
  event={'operation':mode,'path':path,'attempt':attempt,'endpoint':'https://api.github.com/'+endpoint,'authenticated':True,'accept':accept,'commitBinding':ARGS.commit}
  if git_blob:event['gitBlobSha1']=git_blob
  try:
   raw,stderr,code,failure,wall=capture_gh([GH,'api','--hostname','github.com','--method','GET','--include','-H','Accept: '+accept,'-H','X-GitHub-Api-Version: 2022-11-28',endpoint])
   diagnostic=stderr.decode('utf8','replace').replace(str(ROOT),'[repository]')[:1000]
   diagnostic=re.sub(r'gh[pousr]_[A-Za-z0-9_]+','[redacted-token]',diagnostic)
   diagnostic=re.sub(r'(?i)(authorization:\s*bearer\s+)\S+',r'\1[redacted]',diagnostic)
   event.update(returncode=code,capturedStdout=bid(raw),capturedStderr=bid(stderr),stderrText=diagnostic,wallSeconds=wall)
   match=re.match(rb'HTTP/[^\s]+\s+(\d{3})[^\r\n]*\r?\n',raw)
   if match:event['httpStatus']=int(match.group(1))
   if failure:raise failure
   assert code==0,'gh-api-nonzero-exit'
   assert match is not None and event['httpStatus']==200,'missing-or-non-200-http-status'
   split=re.search(rb'\r?\n\r?\n',raw);assert split is not None and split.end()<=65536,'invalid-http-header-boundary'
   body=raw[split.end():];event['responseBody']=bid(body)
   safe={}
   for line in raw[match.end():split.start()].decode('latin1').splitlines():
    if ':' in line:
     key,value=line.split(':',1)
     if key.lower() in ('content-type','content-length','x-github-request-id','x-ratelimit-remaining','x-ratelimit-limit','x-ratelimit-reset'):safe[key.lower()]=value.strip()
   event['safeResponseHeaders']=safe
   if pin is None:
    metadata=parse_admin(body);view={k:metadata.get(k) for k in ('full_name','private','visibility','html_url')}
    assert view['full_name']==REPO and view['private'] is False and view['visibility']=='public','repository-not-exactly-public'
    event['repositoryMetadata']=view;payload=body
   elif mode=='public-contents-api':
    assert same(pin,bid(body)),'public-body-identity-mismatch';event['publicIdentity']=bid(body);payload=body
   else:
    envelope=parse_admin(body);assert envelope['encoding']=='base64' and type(envelope['size']) is int and envelope['size']==pin['bytes']
    if mode=='public-contents-json-base64':assert envelope['type']=='file' and envelope['path']==path
    encoded=envelope['content'];assert isinstance(encoded,str) and re.fullmatch(r'[A-Za-z0-9+/=\r\n]*',encoded),'base64-alphabet'
    payload=base64.b64decode(encoded.replace('\r','').replace('\n',''),validate=True)
    assert same(pin,bid(payload)),'decoded-public-identity-mismatch'
    oid=hashlib.sha1(('blob '+str(len(payload))+'\0').encode()+payload).hexdigest()
    assert envelope['sha']==oid and (git_blob is None or oid==git_blob),'decoded-git-blob-identity'
    event['publicIdentity']=bid(payload);event['decodedGitBlobSha1']=oid
    event['binaryTreatment']='Base64 transport decoding only to opaque byte identities; no archive/image parsing, decompression or rendering.'
   numbered=record({**event,'passed':True})
   return (numbered,payload) if keep else numbered
  except Exception as exc:
   record({**event,'passed':False,'errorType':type(exc).__name__,'detail':str(exc).replace(str(ROOT),'[repository]')[:500]})
   if isinstance(exc,BudgetFailure):raise
 raise RuntimeError('three-public-attempts-exhausted:'+path)

def allocation_state(pin_map):
 if ARGS.phase=='source':
  absent=[]
  for phase in ('producer','audit','finalize','ui'):
   for name in (phase+'-supervisor-launch.lock',phase+'-supervisor.json','results' if phase=='producer' else phase):
    assert not (ROOT/REL/name).exists(),'allocation-already-started:'+name
    absent.append(REL+'/'+name)
  assert not (ROOT/REL/'viewer/pins.json').exists(),'finalizer-already-started'
  return {'checkedAtUtc':now(),'allUnstarted':True,'absentPaths':absent+[REL+'/viewer/pins.json']}
 path=REL+'/ALLOCATION-CLOSURE.json';closure=admin_file(path,pin_map[path]);assert closure['allClosed'] is True
 supervisors={}
 for phase in ('producer','audit','finalize','ui'):
  path=REL+'/'+phase+'-supervisor.json';s=admin_file(path,pin_map[path]);assert s['closed'] is True and closure['allocations'][phase]==s
  supervisors[phase]={'pin':pin_map[path],'closed':True,'returncode':s['returncode']}
 return {'checkedAtUtc':now(),'allClosed':True,'closurePin':pin_map[REL+'/ALLOCATION-CLOSURE.json'],'supervisors':supervisors,'scope':'Frozen administrative closure and supervisor records; no execution.'}

def validate_source_proofs(pin_map,manifest):
 old=admin_file(SOURCE_REVIEW['path'],SOURCE_REVIEW)
 assert old['passed'] is True and old['phase']=='source' and old['commit']==ARGS.source_commit
 assert old['allAllocationsUnstartedAtStartAndEnd'] is True and old['inputPublicProofsReused']==0
 assert old['verifiedFilePins']==old['declaredFilePins'] and old['freshInputPublicPins']==ARGS.input_pins and old['inputPins']==ARGS.input_pins and old['inputBytes']==ARGS.input_bytes
 assert manifest['sourceCommit']==ARGS.source_commit and manifest['sourceManifestSha256']==old['manifestSha256']
 assert SOURCE_REVIEW['path'] in pin_map and same(SOURCE_REVIEW,pin_map[SOURCE_REVIEW['path']])
 source_manifest=REL+'/source-manifest.json';assert source_manifest in pin_map and pin_map[source_manifest]['bytes']==old['manifestBytes'] and pin_map[source_manifest]['sha256']==old['manifestSha256']
 for pin in old['files']:assert pin_map.get(pin['path'])==pin,'frozen-source-or-input-descriptor-changed:'+pin['path']
 events=old['events'];assert [e['event'] for e in events]==list(range(1,len(events)+1));by={e['event']:e for e in events};reused={}
 for proof in old['fileProofs']:
  d=proof['descriptor']
  if d.get('kind')!='input':continue
  chain=[by[x] for x in proof['events']]
  assert len(chain)==4 and [x['operation'] for x in chain[:3]]==['local','source-commit','input-origin-commit']
  assert all(e['passed'] is True and e['path']==d['path'] for e in chain)
  assert chain[1]['commit']==ARGS.source_commit and chain[2]['commit']==d['originCommit']
  for e in chain[:3]:assert same(d,e)
  assert chain[1]['gitBlobSha1']==chain[2]['gitBlobSha1']==chain[0]['gitBlobSha1']==d['gitBlobOid']
  remote=chain[3];assert remote['gitBlobSha1']==d['gitBlobOid']
  assert remote['operation'] in ('public-contents-api','public-contents-json-base64','public-git-blob-json-base64')
  assert remote['httpStatus']==200 and remote['authenticated'] is True and same(d,remote['publicIdentity']) and remote['commitBinding']==ARGS.source_commit
  reused[d['path']]={'descriptor':d,'sourceEvent':remote['event'],'sourceOperation':remote['operation'],'sourceEndpoint':remote['endpoint']}
 assert len(reused)==ARGS.input_pins and sum(v['descriptor']['bytes'] for v in reused.values())==ARGS.input_bytes
 return old,reused

def one(index,pin):
 path=pin['path'];local_proof=identity_read('local',path,pin);proofs=[local_proof,identity_read(ARGS.phase+'-commit',path,pin,ARGS.commit,local_proof)]
 if pin.get('kind')=='input':proofs.append(identity_read('input-origin-commit',path,pin,pin['originCommit'],local_proof))
 if ARGS.phase=='result' and pin.get('kind')=='input':
  old=REUSED[path];assert old['descriptor']==pin
  proofs.append(record({'operation':'reused-public-input-proof','path':path,'passed':True,'bytes':pin['bytes'],'sha256':pin['sha256'],'sourceReview':SOURCE_REVIEW,'sourceCommit':ARGS.source_commit,'sourceEvent':old['sourceEvent'],'sourceOperation':old['sourceOperation'],'sourceEndpoint':old['sourceEndpoint'],'freshPublicRead':False}))
 else:proofs.append(public(path,pin,proofs[1]['gitBlobSha1']))
 with LOCK:VERIFIED.append((index,{'descriptor':pin,'events':[e['event'] for e in proofs]}));count=len(VERIFIED)
 if count%20==0:print(json.dumps({'verifiedFilePins':count,'total':ARGS.file_pins}),flush=True)

parser=argparse.ArgumentParser()
parser.add_argument('--phase',choices=['source','result'],required=True);parser.add_argument('--commit',required=True);parser.add_argument('--manifest-bytes',type=int,required=True);parser.add_argument('--manifest-sha256',required=True);parser.add_argument('--file-pins',type=int,required=True);parser.add_argument('--input-pins',type=int,required=True);parser.add_argument('--input-bytes',type=int,required=True);parser.add_argument('--protocol-sha256',required=True)
parser.add_argument('--source-commit');parser.add_argument('--source-review-file');parser.add_argument('--source-review-bytes',type=int);parser.add_argument('--source-review-sha256')
ARGS=parser.parse_args();BOUNDS=PHASE_BOUNDS[ARGS.phase];assert re.fullmatch('[0-9a-f]{40}',ARGS.commit) and re.fullmatch('[0-9a-f]{64}',ARGS.manifest_sha256) and re.fullmatch('[0-9a-f]{64}',ARGS.protocol_sha256)
assert ARGS.manifest_bytes>0 and ARGS.file_pins>ARGS.input_pins>0 and ARGS.input_bytes>0
BASE='research/publication-receipts/m31-native-factor-reuse-'+ARGS.phase+'-public-review-2026-10-23'
MANIFEST=REL+'/'+ARGS.phase+'-manifest.json';MP={'bytes':ARGS.manifest_bytes,'sha256':ARGS.manifest_sha256};SOURCE_REVIEW=None
if ARGS.phase=='result':
 assert re.fullmatch('[0-9a-f]{40}',ARGS.source_commit or '') and re.fullmatch('[0-9a-f]{64}',ARGS.source_review_sha256 or '') and ARGS.source_review_bytes>0
 assert ARGS.source_review_file=='research/publication-receipts/m31-native-factor-reuse-source-public-review-2026-10-23.json'
 SOURCE_REVIEW={'path':ARGS.source_review_file,'bytes':ARGS.source_review_bytes,'sha256':ARGS.source_review_sha256}
PROTOCOL=ROOT/(BASE+'-protocol.json');JOURNAL=ROOT/(BASE+'-events.jsonl');OUT=ROOT/(BASE+'.json');FAIL=ROOT/(BASE+'-failure.json');MD=ROOT/(BASE+'.md')
assert not any(p.exists() for p in (JOURNAL,OUT,FAIL,MD))
protocol_raw=PROTOCOL.read_bytes();assert hashlib.sha256(protocol_raw).hexdigest()==ARGS.protocol_sha256
protocol=parse_admin(protocol_raw);assert protocol['phase']==ARGS.phase and protocol['commit']==ARGS.commit and protocol['manifest']=={'file':MANIFEST,**MP}
assert protocol['filePins']==ARGS.file_pins and protocol['inputPins']==ARGS.input_pins and protocol['inputBytes']==ARGS.input_bytes
assert protocol['bounds']==BOUNDS and protocol['executionPermission']=='require_escalated'
HELPER={'file':str(Path(__file__).resolve().relative_to(ROOT)),**bid(Path(__file__).read_bytes())}
assert protocol['helper']==HELPER,'helper-identity-not-bound'
assert protocol['gitIdentityRoute']=='Fresh exact-commit tree metadata bound to freshly streamed local Git blob SHA1 and SHA256; no Git blob extraction'
assert protocol['binaryRoute']=='Git blob JSON/base64 for binary parts; Contents JSON/base64 for PNG below 1MiB, Git blob JSON/base64 for larger PNG; no raw binary requests'
if ARGS.phase=='result':assert protocol['reusedInputSourceReview']==SOURCE_REVIEW
JOURNAL.touch(exist_ok=False);pins=[];pin_map={};initial=None;final=None;metadata=None;error=None;REUSED={};source_receipt=None
try:
 manifest_local=identity_read('local',MANIFEST,MP);identity_read(ARGS.phase+'-commit',MANIFEST,MP,ARGS.commit,manifest_local)
 manifest=admin_file(MANIFEST,MP);pins=manifest['files'];assert len(pins)==len({p['path'] for p in pins})==ARGS.file_pins
 for pin in pins:
  assert isinstance(pin['path'],str) and not pin['path'].startswith('/') and '\\' not in pin['path'] and all(x not in ('','.', '..') for x in pin['path'].split('/'))
  assert type(pin['bytes']) is int and pin['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',pin['sha256'])
  assert pin.get('kind') in (None,'source','input','result','administrative','evidence','review')
  if pin.get('kind')=='input':assert re.fullmatch('[0-9a-f]{40}',pin['originCommit']) and re.fullmatch('[0-9a-f]{40}',pin['gitBlobOid'])
  if ARGS.phase=='source':assert pin.get('kind') in ('source','input')
 pin_map={p['path']:p for p in pins};inputs=[p for p in pins if p.get('kind')=='input'];assert len(inputs)==ARGS.input_pins and sum(p['bytes'] for p in inputs)==ARGS.input_bytes
 declared=admin_file(REL+'/input-pins.json',pin_map[REL+'/input-pins.json'])['files'];assert len(declared)==len(inputs) and {p['path']:p for p in declared}=={p['path']:p for p in inputs}
 if ARGS.phase=='result':source_receipt,REUSED=validate_source_proofs(pin_map,manifest)
 initial=allocation_state(pin_map)
 metadata=public('repository-metadata')
 _,fresh_manifest=public(MANIFEST,MP,keep=True);assert fresh_manifest==(ROOT/MANIFEST).read_bytes()
 with ThreadPoolExecutor(max_workers=BOUNDS['maxConcurrentTransfers']) as executor:
  jobs={executor.submit(one,i,p):p['path'] for i,p in enumerate(pins)};failures=[]
  for job in as_completed(jobs):
   try:job.result()
   except Exception as exc:failures.append({'path':jobs[job],'errorType':type(exc).__name__,'detail':str(exc)})
  if failures:raise RuntimeError('file-identities-incomplete:'+json.dumps(failures))
 assert len(VERIFIED)==ARGS.file_pins;remaining()
except Exception as exc:error={'errorType':type(exc).__name__,'detail':str(exc).replace(str(ROOT),'[repository]')}
# Administrative end-state checks run after success or failure; never rerun an allocation.
try:
 final=allocation_state(pin_map)
 if initial and ARGS.phase=='result':assert initial['closurePin']==final['closurePin'] and initial['supervisors']==final['supervisors']
 assert bid(PROTOCOL.read_bytes())==bid(protocol_raw)
 if SOURCE_REVIEW:assert same(SOURCE_REVIEW,file_id(ROOT/SOURCE_REVIEW['path']))
except Exception as exc:
 end_error={'errorType':type(exc).__name__,'detail':str(exc).replace(str(ROOT),'[repository]')}
 error=end_error if error is None else {**error,'endCheckError':end_error}
passed=error is None;remote=[e for e in EVENTS if e['passed'] and e['operation'] in ('public-contents-api','public-contents-json-base64','public-git-blob-json-base64')];failed=[e for e in EVENTS if not e['passed']];inputs_verified=sum(x['descriptor'].get('kind')=='input' for _,x in VERIFIED)
receipt={'schema':'m31-native-factor-reuse-independent-public-'+ARGS.phase+'-review-v1','phase':ARGS.phase,'passed':passed,'checkedAtUtc':now(),'commit':ARGS.commit,'manifestPath':MANIFEST,'manifestBytes':MP['bytes'],'manifestSha256':MP['sha256'],'verifiedFilePins':len(VERIFIED),'declaredFilePins':ARGS.file_pins,'inputPins':ARGS.input_pins,'inputBytes':ARGS.input_bytes,'localBytesEqualPins':passed,'committedBytesEqualLocal':passed,'remoteBytesEqualLocal':passed,'independentReviewPassed':passed,'freshInputOriginGitPins':inputs_verified,'freshInputOriginTreePins':inputs_verified,'gitIdentityRoute':protocol['gitIdentityRoute'],'freshInputPublicPins':inputs_verified if ARGS.phase=='source' else 0,'inputPublicProofsReused':inputs_verified if ARGS.phase=='result' else 0,'inputPublicProofSource':SOURCE_REVIEW,'freshPublicReads':len(remote),'freshPublicResponseBodyBytes':sum(e['responseBody']['bytes'] for e in remote),'freshPublicIdentityBytes':sum(e['publicIdentity']['bytes'] for e in remote),'publicRouteCounts':{name:sum(e['operation']==name for e in remote) for name in ('public-contents-api','public-contents-json-base64','public-git-blob-json-base64')},'authentication':'Authenticated GitHub API after exact public repository metadata verification. Text uses exact-ref Contents raw responses; binary transport uses JSON/base64 bound to source/result Git blob SHA-1 and manifest SHA-256. No unauthenticated raw-CDN claim.','repositoryMetadata':metadata,'protocol':{'file':str(PROTOCOL.relative_to(ROOT)),**bid(protocol_raw)},'helper':HELPER,'bounds':BOUNDS,'aggregateCapturedPublicBytes':CAPTURED,'wallSeconds':time.monotonic()-START,'allAllocationsUnstartedAtStartAndEnd':bool(ARGS.phase=='source' and initial and final and initial['allUnstarted'] and final['allUnstarted']),'allAllocationsClosed':bool(ARGS.phase=='result' and initial and final and initial['allClosed'] and final['allClosed']),'allocationChecks':{'start':initial,'end':final},'failedAttempts':failed,'events':EVENTS,'files':[x['descriptor'] for _,x in sorted(VERIFIED)],'fileProofs':[x for _,x in sorted(VERIFIED)],'eventJournal':{'file':str(JOURNAL.relative_to(ROOT)),**bid(JOURNAL.read_bytes())},'error':error,'allocationLaunched':False,'nativeQueries':0,'auditExecuted':False,'uiLaunched':False,'archiveDecompressed':False,'imageRendered':False,'savedStateReaggregated':False,'rawEvidenceTreatedAsOpaqueBytes':True,'verificationScope':'Administrative publication byte identity only. Base64 decoding recovers opaque transport bytes and does not decompress archives, parse image/scientific contents, run models or aggregate logs. Source phase freshly retrieves all file pins and manifest; result phase freshly retrieves all noninputs and manifest and reuses only exact source-gate input public proofs with fresh local SHA1/SHA256 and result/origin Git tree metadata bindings. Git blob bodies are not re-extracted locally. Individual failures and source-preparation history remain retained.'}
target=OUT if passed else FAIL
with target.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
assert parse_admin(target.read_bytes())==receipt and [parse_admin(x.encode()) for x in JOURNAL.read_text().splitlines()]==EVENTS
if passed:
 lines=['# Independent public '+ARGS.phase+' verification — native factor reuse','','Passed for publication byte identity.','','- Commit: `'+ARGS.commit+'`.','- Manifest: '+str(MP['bytes'])+' bytes; SHA-256 `'+MP['sha256']+'`.','- Covered file pins: '+str(ARGS.file_pins)+'.','- Fresh public reads including manifest: '+str(len(remote))+'.','- Input public proofs reused: '+str(receipt['inputPublicProofsReused'])+'.','- Failed attempts: '+str(len(failed))+'; each retained in JSON/journal.','- Git identity uses fresh tree metadata bound to local Git blob SHA-1/SHA-256; no local Git blob extraction.', '- Authenticated exact-ref Contents API for text/PNG or immutable Git-blob JSON/base64 for binary parts. Decoded content is checked as opaque bytes and Git blob identities only.','- Bounds: '+str(BOUNDS['maxConcurrentTransfers'])+' concurrent transfers, three attempts per identity, 45 seconds per attempt, '+str(BOUNDS['overallSeconds'])+' seconds overall, '+str(BOUNDS['aggregateCapturedPublicBytes']//1048576)+' MiB captured public data.','- Administrative start/end state: '+('all four allocations unstarted.' if ARGS.phase=='source' else 'all four frozen allocation records closed and matching.'),'- No archive decompression, image rendering, numerical/model/audit/UI execution or raw-log aggregation occurred.','','## Coverage','','| Path | Kind | Bytes | SHA-256 |','| --- | --- | ---: | --- |']
 for pin in pins:lines.append('| `'+pin['path']+'` | '+str(pin.get('kind','result'))+' | '+str(pin['bytes'])+' | `'+pin['sha256']+'` |')
 with MD.open('x') as f:f.write('\n'.join(lines)+'\n')
print(json.dumps({'passed':passed,'phase':ARGS.phase,'verifiedFilePins':len(VERIFIED),'freshPublicReads':len(remote),'inputPublicProofsReused':receipt['inputPublicProofsReused'],'failedAttempts':len(failed),'aggregateCapturedPublicBytes':CAPTURED,'receipt':{'file':str(target.relative_to(ROOT)),**bid(target.read_bytes())},'markdown':{'file':str(MD.relative_to(ROOT)),**bid(MD.read_bytes())} if passed else None,'error':error}),flush=True)
if not passed:raise SystemExit(1)
