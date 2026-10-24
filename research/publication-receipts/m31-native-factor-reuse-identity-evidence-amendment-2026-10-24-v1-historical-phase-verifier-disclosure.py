"""Administrative identity checks only. Requires frozen commit/manifest CLI pins."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
import argparse, datetime, hashlib, json, os, re, selectors, signal, subprocess, tempfile, threading, time

ROOT=Path(__file__).resolve().parents[2]
REL='research/m31-phase-attribution-2026-10-23'
BASE='research/publication-receipts/m31-phase-attribution-source-public-review-2026-10-23'
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
    value=900-(time.monotonic()-START)
    if value<=0:STOP.set();raise BudgetFailure('overall-900-second-limit')
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
def allocation_state():
    checked=[]
    for phase in ('producer','audit','finalize','ui'):
        for name in (phase+'-supervisor-launch.lock',phase+'-supervisor.json','results' if phase=='producer' else phase):
            assert not (ROOT/REL/name).exists(),'allocation-already-started:'+name
            checked.append(REL+'/'+name)
    assert not (ROOT/REL/'viewer/pins.json').exists(),'finalizer-already-started'
    return {'checkedAtUtc':now(),'allUnstarted':True,'absentPaths':checked+[REL+'/viewer/pins.json']}
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
                if time.monotonic()-START>=900:raise BudgetFailure('overall-900-second-limit')
                raise AttemptTimeout('api-attempt-45-second-limit')
            if STOP.is_set():raise BudgetFailure('verification-stopped')
            for key,_ in selector.select(min(left,.2)):
                with LOCK:
                    available=536870912-CAPTURED
                    if available<=0:raise BudgetFailure('aggregate-captured-512-MiB-limit')
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
def public(path,pin=None,keep=False):
    mode='repository-public-metadata' if pin is None else 'public-contents-api'
    endpoint='repos/'+REPO if pin is None else 'repos/'+REPO+'/contents/'+quote(path,safe='/')+'?ref='+ARGS.commit
    accept='application/vnd.github+json' if pin is None else 'application/vnd.github.raw+json'
    for attempt in (1,2,3):
        event={'operation':mode,'path':path,'attempt':attempt,'endpoint':'https://api.github.com/'+endpoint,'authenticated':True,'accept':accept}
        try:
            raw,stderr,code,failure,wall=capture_gh([GH,'api','--hostname','github.com','--method','GET','--include','-H','Accept: '+accept,'-H','X-GitHub-Api-Version: 2022-11-28',endpoint])
            event.update(returncode=code,capturedStdout=bid(raw),capturedStderr=bid(stderr),wallSeconds=wall)
            match=re.match(rb'HTTP/[^\s]+\s+(\d{3})[^\r\n]*\r?\n',raw)
            if match:event['httpStatus']=int(match.group(1))
            if failure:raise failure
            assert code==0,'gh-api-nonzero-exit'
            assert match is not None and event['httpStatus']==200,'missing-or-non-200-http-status'
            split=re.search(rb'\r?\n\r?\n',raw);assert split is not None and split.end()<=65536,'invalid-http-header-boundary'
            body=raw[split.end():];got=bid(body);event['responseBody']=got
            safe={}
            for line in raw[match.end():split.start()].decode('latin1').splitlines():
                if ':' in line:
                    key,value=line.split(':',1)
                    if key.lower() in ('content-type','content-length','x-github-request-id','x-ratelimit-remaining','x-ratelimit-limit','x-ratelimit-reset'):safe[key.lower()]=value.strip()
            event['safeResponseHeaders']=safe
            if pin is None:
                metadata=json.loads(body);view={k:metadata.get(k) for k in ('full_name','private','visibility','html_url')}
                assert view['full_name']==REPO and view['private'] is False and view['visibility']=='public','repository-not-exactly-public'
                event['repositoryMetadata']=view
            else:assert same(pin,got),'public-body-identity-mismatch'
            numbered=record({**event,'passed':True})
            return (numbered,body) if keep else numbered
        except Exception as error:
            detail=str(error).replace(str(ROOT),'[repository]')[:500]
            record({**event,'passed':False,'errorType':type(error).__name__,'detail':detail})
            if isinstance(error,BudgetFailure):raise
    raise RuntimeError('three-public-attempts-exhausted:'+path)
def identity_read(mode,path,pin,commit=None):
    for attempt in (1,2,3):
        begin=time.monotonic();event={'operation':mode,'path':path,'attempt':attempt}
        if commit:event['commit']=commit
        try:
            if STOP.is_set():raise BudgetFailure('verification-stopped')
            deadline=begin+min(45,remaining())
            if mode=='local':
                candidate=ROOT/path;assert candidate.resolve().is_relative_to(ROOT) and candidate.is_file() and not candidate.is_symlink(),'unsafe-local-path'
                assert all(not (ROOT/parent).is_symlink() for parent in candidate.relative_to(ROOT).parents),'symlinked-parent'
                got=file_id(candidate,deadline)
            else:
                obj=commit+':'+path
                size=subprocess.run(['git','cat-file','-s',obj],cwd=ROOT,env=ENV,capture_output=True,timeout=max(.001,deadline-time.monotonic()),check=True)
                assert int(size.stdout)==pin['bytes'],'git-object-size-mismatch'
                with tempfile.TemporaryFile() as target:
                    subprocess.run(['git','cat-file','blob',obj],cwd=ROOT,env=ENV,stdout=target,stderr=subprocess.PIPE,timeout=max(.001,deadline-time.monotonic()),check=True)
                    target.seek(0);h=hashlib.sha256();n=0
                    for block in iter(lambda:target.read(1048576),b''):
                        if time.monotonic()>deadline:raise AttemptTimeout('git-identity-45-second-limit')
                        remaining();n+=len(block);h.update(block)
                    got={'bytes':n,'sha256':h.hexdigest()}
            assert same(pin,got),'identity-mismatch'
            return record({**event,'passed':True,**got,'wallSeconds':time.monotonic()-begin})
        except Exception as error:
            record({**event,'passed':False,'errorType':type(error).__name__,'detail':str(error).replace(str(ROOT),'[repository]')[:500],'wallSeconds':time.monotonic()-begin})
            if isinstance(error,BudgetFailure):raise
    raise RuntimeError('three-identity-attempts-exhausted:'+mode+':'+path)
def one(index,pin):
    path=pin['path'];proofs=[identity_read('local',path,pin),identity_read('source-commit',path,pin,ARGS.commit)]
    if pin['kind']=='input':proofs.append(identity_read('input-origin-commit',path,pin,pin['originCommit']))
    proofs.append(public(path,pin))
    with LOCK:VERIFIED.append((index,{'descriptor':pin,'events':[e['event'] for e in proofs]}));count=len(VERIFIED)
    if count%10==0:print(json.dumps({'verifiedFilePins':count,'total':ARGS.file_pins}),flush=True)

parser=argparse.ArgumentParser()
parser.add_argument('--commit',required=True);parser.add_argument('--manifest-bytes',type=int,required=True);parser.add_argument('--manifest-sha256',required=True);parser.add_argument('--file-pins',type=int,required=True);parser.add_argument('--protocol-sha256',required=True)
ARGS=parser.parse_args();assert re.fullmatch('[0-9a-f]{40}',ARGS.commit) and re.fullmatch('[0-9a-f]{64}',ARGS.manifest_sha256) and re.fullmatch('[0-9a-f]{64}',ARGS.protocol_sha256)
assert ARGS.manifest_bytes>0 and ARGS.file_pins>29
MANIFEST=REL+'/source-manifest.json';MP={'bytes':ARGS.manifest_bytes,'sha256':ARGS.manifest_sha256}
PROTOCOL=ROOT/(BASE+'-protocol.json');JOURNAL=ROOT/(BASE+'-events.jsonl');OUTPUT=ROOT/(BASE+'.json');MARKDOWN=ROOT/(BASE+'.md');FAILURE=ROOT/(BASE+'-failure.json')
assert not any(p.exists() for p in (JOURNAL,OUTPUT,MARKDOWN,FAILURE))
protocol_raw=PROTOCOL.read_bytes();assert hashlib.sha256(protocol_raw).hexdigest()==ARGS.protocol_sha256
protocol=json.loads(protocol_raw)
assert protocol['commit']==ARGS.commit and protocol['manifest']=={'file':MANIFEST,**MP} and protocol['filePins']==ARGS.file_pins
assert protocol['bounds']=={'maxConcurrentTransfers':2,'attemptsPerIdentity':3,'secondsPerAttempt':45,'overallSeconds':900,'aggregateCapturedPublicBytes':536870912}
assert protocol['executionPermission']=='require_escalated'
initial=allocation_state();JOURNAL.touch(exist_ok=False);pins=[];metadata=None;error=None
try:
    identity_read('local',MANIFEST,MP);identity_read('source-commit',MANIFEST,MP,ARGS.commit)
    metadata=public('repository-metadata')
    _,manifest_body=public(MANIFEST,MP,True);manifest=json.loads(manifest_body);pins=manifest['files']
    assert len(pins)==len({p['path'] for p in pins})==ARGS.file_pins
    inputs=[p for p in pins if p['kind']=='input'];assert len(inputs)==29 and sum(p['bytes'] for p in inputs)==95752652
    assert sum(p['kind']=='source' for p in pins)==ARGS.file_pins-29
    for p in pins:
        assert isinstance(p['path'],str) and not p['path'].startswith('/') and '\\' not in p['path'] and all(x not in ('','.', '..') for x in p['path'].split('/'))
        assert type(p['bytes']) is int and p['bytes']>0 and re.fullmatch('[0-9a-f]{64}',p['sha256'])
        if p['kind']=='input':assert re.fullmatch('[0-9a-f]{40}',p['originCommit'])
    with ThreadPoolExecutor(max_workers=2) as executor:
        tasks={executor.submit(one,i,p):p['path'] for i,p in enumerate(pins)};failures=[]
        for task in as_completed(tasks):
            try:task.result()
            except Exception as exc:failures.append({'path':tasks[task],'errorType':type(exc).__name__,'detail':str(exc)})
        if failures:raise RuntimeError('file-identities-incomplete:'+json.dumps(failures))
    source_inputs=ROOT/REL/'input-pins.json';input_pin=next(p for p in pins if p['path']==REL+'/input-pins.json');assert same(input_pin,file_id(source_inputs))
    declared_inputs=json.loads(source_inputs.read_bytes())['files'];assert len(declared_inputs)==29 and {p['path']:p for p in declared_inputs}=={p['path']:p for p in inputs},'input-descriptor-identity'
    assert len(VERIFIED)==ARGS.file_pins;remaining()
except Exception as exc:error={'errorType':type(exc).__name__,'detail':str(exc).replace(str(ROOT),'[repository]')}
try:final=allocation_state();assert bid(PROTOCOL.read_bytes())==bid(protocol_raw)
except Exception as exc:final={'allUnstarted':False,'detail':str(exc)};error={'errorType':type(exc).__name__,'detail':str(exc)}
passed=error is None
remote=[e for e in EVENTS if e['passed'] and e['operation']=='public-contents-api'];failed=[e for e in EVENTS if not e['passed']]
receipt={'schema':'m31-phase-attribution-independent-public-source-review-v1','passed':passed,'checkedAtUtc':now(),'commit':ARGS.commit,'manifestPath':MANIFEST,'manifestBytes':MP['bytes'],'manifestSha256':MP['sha256'],'verifiedFilePins':len(VERIFIED),'declaredFilePins':ARGS.file_pins,'localBytesEqualPins':passed,'committedBytesEqualLocal':passed,'remoteBytesEqualLocal':passed,'independentReviewPassed':passed,'freshInputOriginGitPins':sum(p['descriptor']['kind']=='input' for _,p in VERIFIED),'freshInputPublicPins':sum(p['descriptor']['kind']=='input' for _,p in VERIFIED),'inputPublicProofsReused':0,'freshPublicReads':len(remote),'freshPublicBytes':sum(e['responseBody']['bytes'] for e in remote),'authentication':'Fresh authenticated GitHub Contents API raw reads at exact source ref, after exact repository public visibility verification; no unauthenticated raw-CDN claim.','repositoryMetadata':metadata,'protocol':{'file':str(PROTOCOL.relative_to(ROOT)),**bid(protocol_raw)},'bounds':protocol['bounds'],'aggregateCapturedPublicBytes':CAPTURED,'wallSeconds':time.monotonic()-START,'allAllocationsUnstartedAtStartAndEnd':initial['allUnstarted'] and final.get('allUnstarted') is True,'allocationChecks':{'start':initial,'end':final},'successfulIdentityOperations':sum(e['passed'] for e in EVENTS),'failedAttempts':failed,'events':EVENTS,'files':[x['descriptor'] for _,x in sorted(VERIFIED)],'fileProofs':[x for _,x in sorted(VERIFIED)],'eventJournal':{'file':str(JOURNAL.relative_to(ROOT)),**bid(JOURNAL.read_bytes())},'error':error,'allocationLaunched':False,'nativeQueries':0,'auditExecuted':False,'uiLaunched':False,'archiveDecompressed':False,'savedStateReaggregated':False,'rawEvidenceTreatedAsOpaqueBytes':True,'verificationScope':'Publication byte identity and administrative unstarted checks only; no scientific source imported or executed.'}
target=OUTPUT if passed else FAILURE
with target.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
assert json.loads(target.read_bytes())==receipt and [json.loads(x) for x in JOURNAL.read_text().splitlines()]==EVENTS
if passed:
    lines=['# Independent public source verification — phase attribution','','Passed. All source and immutable input pins plus the manifest were freshly checked against local/source-Git/public bytes. Every one of the 29 inputs also received a fresh origin-Git read. No prior public proof was reused.','','- Source commit: `'+ARGS.commit+'`.','- Manifest: '+str(MP['bytes'])+' bytes; SHA-256 `'+MP['sha256']+'`.','- Verified file pins: '+str(ARGS.file_pins)+'.','- Fresh public reads including manifest: '+str(len(remote))+'; '+str(receipt['freshPublicBytes'])+' body bytes.','- Route: existing-gh authenticated GitHub Contents API raw response at exact commit, after public repository visibility verification. This is not unauthenticated raw-CDN evidence.','- At most two concurrent transfers, three attempts per identity, 45 seconds per attempt, 900 seconds overall, 512 MiB aggregate captured public bytes.','- Failed attempts: '+str(len(failed))+', individually retained in JSON/journal.','- All four prospective allocations remained unstarted at start/end. No model/analysis/audit/UI execution, native query, archive decoding or reaggregation occurred.','','## Coverage','','| Path | Kind | Bytes | SHA-256 |','| --- | --- | ---: | --- |']
    for p in pins:lines.append('| `'+p['path']+'` | '+p['kind']+' | '+str(p['bytes'])+' | `'+p['sha256']+'` |')
    with MARKDOWN.open('x') as f:f.write('\n'.join(lines)+'\n')
print(json.dumps({'passed':passed,'verifiedFilePins':len(VERIFIED),'freshPublicReads':len(remote),'failedAttempts':len(failed),'aggregateCapturedPublicBytes':CAPTURED,'receipt':{'file':str(target.relative_to(ROOT)),**bid(target.read_bytes())},'markdown':{'file':str(MARKDOWN.relative_to(ROOT)),**bid(MARKDOWN.read_bytes())} if passed else None,'error':error}),flush=True)
if not passed:raise SystemExit(1)
