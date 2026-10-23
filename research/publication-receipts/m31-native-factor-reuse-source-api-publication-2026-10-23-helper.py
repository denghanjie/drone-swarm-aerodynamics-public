"""Single bounded administrative API publication recovery; no scientific execution."""
from pathlib import Path
import argparse, base64, datetime, hashlib, json, os, re, selectors, signal, subprocess, tempfile, time

ROOT=Path(__file__).resolve().parents[2]
REL='research/m31-native-factor-reuse-2026-10-23'
PREFIX='research/publication-receipts/m31-native-factor-reuse-source-api-publication-2026-10-23'
REPO='denghanjie/drone-swarm-aerodynamics-public'
COMMIT='7e6ab5b1d3bb819a7a17178c9a5636bde49ca6f2'
PARENT='bf064b2c4d54c7ed61a55ae1791fa64bf4e044fe'
PARENT_TREE='53f92a874d8b6df1c11c48f0d53a24db40401eca'
TREE='a8e6a60e3e676224ee128562d1babbc559d7352a'
BRANCH='codex/m31-audit-2026-10-15'
MESSAGE='Freeze reviewed native factor reuse ablation and exact evidence controls\n'
EPOCH=1792758116
IDENTITY={'name':'DHJ','email':'17939962+denghanjie@users.noreply.github.com','date':datetime.datetime.fromtimestamp(EPOCH,datetime.timezone(datetime.timedelta(hours=8))).isoformat()}
MANIFEST={'file':REL+'/source-manifest.json','bytes':21212,'sha256':'858ba637b83da51296ffd8cc9cd4d91556de70ef568275fab144b353273eda4d'}
BOUNDS={'overallSeconds':600,'secondsPerRequest':45,'maxRequests':45,'maxConcurrentRequests':1,'maxCapturedBytes':16777216,'attemptsPerOperation':1,'maxSourceBytes':1048576}
ENV={k:v for k,v in os.environ.items() if k not in ('GH_DEBUG','DEBUG','GIT_EXTERNAL_DIFF','GIT_DIFF_OPTS','GIT_PAGER')}
ENV.update(GH_PROMPT_DISABLED='1',GH_NO_UPDATE_NOTIFIER='1',GH_NO_EXTENSION_UPDATE_NOTIFIER='1',GIT_NO_REPLACE_OBJECTS='1',GIT_TERMINAL_PROMPT='0')
START=time.monotonic();EVENTS=[];CAPTURED=0;REQUESTS=0
OUT=ROOT/(PREFIX+'.json');JOURNAL=ROOT/(PREFIX+'-events.jsonl');LOCK=ROOT/(PREFIX+'-launch.lock');PROTOCOL=ROOT/(PREFIX+'-protocol.json')
RESULT={'schema':'m31-factor-source-api-publication-recovery-v1','sourceCommit':COMMIT,'expectedParent':PARENT,'expectedParentTree':PARENT_TREE,'expectedTree':TREE,'branch':BRANCH,'bounds':BOUNDS,'events':EVENTS,'closed':False,'passed':False,'refUpdateAttempted':False,'refUpdated':False,'allocationLaunched':False,'nativeQueries':0,'archiveDecoded':False,'publicSourceGateExecuted':False}
def interrupted(signum,frame):raise InterruptedError('administrative-publication-interrupted:'+str(signum))
for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,interrupted)

class BudgetFailure(Exception):pass
def bid(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def same(pin,raw):return all(pin[k]==bid(raw)[k] for k in ('bytes','sha256'))
def remaining():
    left=BOUNDS['overallSeconds']-(time.monotonic()-START)
    if left<=0:raise BudgetFailure('overall-wall-cap')
    return left
def clean(value):
    value=str(value).replace(str(ROOT),'[repository]')
    value=re.sub(r'/private/(?:tmp|var/folders)/[^\s\"\']+','[temporary]',value)
    value=re.sub(r'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+','[redacted-token]',value)
    return re.sub(r'(?i)(authorization:\s*bearer\s+)\S+',r'\1[redacted]',value)[:1800]
def save():
    RESULT.update(wallSeconds=time.monotonic()-START,capturedBytes=CAPTURED,requests=REQUESTS)
    temporary=OUT.with_suffix('.writing')
    temporary.write_text(json.dumps(RESULT,indent=2)+'\n');os.replace(temporary,OUT)
def record(event):
    item={'event':len(EVENTS)+1,**event};EVENTS.append(item)
    with JOURNAL.open('a') as f:f.write(json.dumps(item,separators=(',',':'))+'\n')
    save();return item
def parse(raw):
    def unique(pairs):
        out={}
        for k,v in pairs:
            assert k not in out,'duplicate-json-key';out[k]=v
        return out
    def invalid(value):raise ValueError('nonfinite-json:'+value)
    return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid)
def local_git(args):
    return subprocess.check_output(['git',*args],cwd=ROOT,env=ENV,timeout=min(15,remaining()))
def allocation_state():
    absent=[]
    for phase in ('producer','audit','finalize','ui'):
        for name in (phase+'-supervisor-launch.lock',phase+'-supervisor.json','results' if phase=='producer' else phase):
            assert not (ROOT/REL/name).exists(),'allocation-already-started:'+name
            absent.append(name)
    assert not (ROOT/REL/'viewer/pins.json').exists(),'viewer-already-finalized'
    return {'allUnstarted':True,'absentPaths':absent+['viewer/pins.json']}
def api(method,endpoint,body=None,expected_status=200):
    global CAPTURED,REQUESTS
    assert REQUESTS<BOUNDS['maxRequests'],'request-count-cap'
    duration=min(BOUNDS['secondsPerRequest'],remaining());REQUESTS+=1
    raw_body=None if body is None else json.dumps(body,separators=(',',':')).encode()
    event={'request':REQUESTS,'method':method,'endpoint':'https://api.github.com/repos/'+REPO+endpoint,'attempt':1,'requestBody':None if raw_body is None else bid(raw_body),'authenticated':True}
    begin=time.monotonic();out=bytearray();err=bytearray();process=None;selector=selectors.DefaultSelector();failure=None
    try:
        with tempfile.TemporaryDirectory(prefix='m31-factor-api-') as directory:
            args=['/opt/homebrew/bin/gh','api','--hostname','github.com','--method',method,'--include','-H','Accept: application/vnd.github+json','-H','X-GitHub-Api-Version: 2022-11-28','repos/'+REPO+endpoint]
            if raw_body is not None:
                request=Path(directory)/'request.json';request.write_bytes(raw_body);args+=['--input',str(request)]
            process=subprocess.Popen(args,cwd=ROOT,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            for stream,label in ((process.stdout,'stdout'),(process.stderr,'stderr')):
                os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,label)
            while selector.get_map():
                left=duration-(time.monotonic()-begin)
                if left<=0:raise TimeoutError('bounded-request-timeout')
                for key,_ in selector.select(min(left,.2)):
                    available=BOUNDS['maxCapturedBytes']-CAPTURED
                    if available<=0:raise BudgetFailure('aggregate-captured-byte-cap')
                    data=os.read(key.fileobj.fileno(),min(65536,available));CAPTURED+=len(data)
                    if not data:selector.unregister(key.fileobj);continue
                    (out if key.data=='stdout' else err).extend(data)
            returncode=process.wait(timeout=max(.001,duration-(time.monotonic()-begin)))
    except BaseException as exc:
        failure=exc
        if process and process.poll() is None:
            os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=2)
        returncode=None if process is None else process.returncode
    finally:
        selector.close()
        if process:process.stdout.close();process.stderr.close()
    raw=bytes(out);stderr=bytes(err)
    event.update(exitCode=returncode,capturedStdout=bid(raw),capturedStderr=bid(stderr),diagnostic=clean(stderr.decode('utf8','replace')),wallSeconds=time.monotonic()-begin)
    status=re.match(rb'HTTP/[^\s]+\s+(\d{3})[^\r\n]*\r?\n',raw)
    if status:event['httpStatus']=int(status.group(1))
    try:
        if failure:raise failure
        assert returncode==0 and event.get('httpStatus')==expected_status,'API-exit-or-status-failure'
        boundary=re.search(rb'\r?\n\r?\n',raw);assert boundary and boundary.end()<=65536,'HTTP-header-boundary'
        payload=raw[boundary.end():];event['responseBody']=bid(payload);value=parse(payload)
        if isinstance(value,dict):event['returnedIdentity']={k:value[k] for k in ('sha','ref','url') if k in value}
        if isinstance(value,dict) and 'object' in value:event['returnedObject']=value['object']
        event['transportPassed']=True;record(event);return value
    except BaseException as exc:
        event.update(transportPassed=False,errorType=type(exc).__name__,detail=clean(exc));record(event);raise

assert not any(p.exists() for p in (OUT,JOURNAL,LOCK)), 'single-use-recovery-already-started'
parser=argparse.ArgumentParser();parser.add_argument('--protocol-sha256',required=True);args=parser.parse_args()
assert re.fullmatch('[0-9a-f]{64}',args.protocol_sha256),'protocol-hash-required'
protocol_raw=PROTOCOL.read_bytes();protocol=parse(protocol_raw)
assert hashlib.sha256(protocol_raw).hexdigest()==args.protocol_sha256,'reviewed-protocol-identity'
HELPER={'file':Path(__file__).resolve().relative_to(ROOT).as_posix(),**bid(Path(__file__).read_bytes())}
assert protocol['helper']==HELPER and protocol['bounds']==BOUNDS
assert protocol['repository']==REPO
assert protocol['commit']==COMMIT and protocol['parent']==PARENT and protocol['parentTree']==PARENT_TREE and protocol['tree']==TREE and protocol['branch']==BRANCH and protocol['manifest']==MANIFEST
assert protocol['operation']=='single-attempt exact-object API publication recovery' and protocol['executionPermission']=='require_escalated'
assert protocol['author']==protocol['committer']==IDENTITY and protocol['message']==MESSAGE
with LOCK.open('x') as lock:lock.write('single bounded administrative API publication attempt\n')
JOURNAL.touch(exist_ok=False)
RESULT.update(helper=HELPER,protocol={'file':PROTOCOL.relative_to(ROOT).as_posix(),**bid(protocol_raw)})
save();phase='preflight';blobs=[];patch_started=False;patch_returned=False
try:
    RESULT['allocationChecks']={'start':allocation_state()};save()
    history=protocol['failedGitPushReceipt'];history_raw=(ROOT/history['file']).read_bytes();assert same(history,history_raw)
    history_value=parse(history_raw);assert history_value['commit']==COMMIT and len(history_value['events'])==3 and all(e['exitCode']!=0 for e in history_value['events'])
    RESULT['closedPriorGitPush']=history;RESULT['priorGitPushAttemptsExhausted']=3;save()
    original=local_git(['cat-file','commit',COMMIT])
    expected=(f'tree {TREE}\nparent {PARENT}\nauthor {IDENTITY["name"]} <{IDENTITY["email"]}> {EPOCH} +0800\ncommitter {IDENTITY["name"]} <{IDENTITY["email"]}> {EPOCH} +0800\n\n'+MESSAGE).encode()
    assert original==expected and hashlib.sha1(b'commit '+str(len(original)).encode()+b'\0'+original).hexdigest()==COMMIT,'exact-local-commit-metadata'
    assert local_git(['rev-parse',PARENT+'^{tree}']).strip().decode()==PARENT_TREE,'exact-local-parent-tree'
    manifest_raw=(ROOT/MANIFEST['file']).read_bytes();assert same(MANIFEST,manifest_raw)
    manifest=parse(manifest_raw);pins={p['path']:p for p in manifest['files']};pins[MANIFEST['file']]=MANIFEST
    diff=local_git(['diff-tree','--no-commit-id','--raw','-z','-r',PARENT,COMMIT]).split(b'\0')
    assert diff[-1]==b'' and len(diff)==75,'exact37-added-files'
    total=0
    for i in range(0,74,2):
        meta,path=diff[i],diff[i+1].decode();oldmode,mode,oldoid,oid,status=meta.decode().split()
        assert oldmode==':000000' and mode=='100644' and oldoid=='0'*40 and status=='A'
        assert path.startswith(REL+'/') and path in pins and '\\' not in path and '..' not in Path(path).parts
        local=ROOT/path;assert local.is_file() and not local.is_symlink() and local.resolve().is_relative_to(ROOT)
        raw=local.read_bytes();assert same(pins[path],raw) and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid
        total+=len(raw);assert total<=BOUNDS['maxSourceBytes'];blobs.append((path,raw,oid))
    assert {p for p,_,_ in blobs}=={p for p in pins if p.startswith(REL+'/')},'complete-checkpoint-only-upload-set'
    RESULT['sourceBlobs']=[{'path':p,**bid(raw),'gitBlobOid':oid} for p,raw,oid in blobs];RESULT['sourceBytes']=total
    assert protocol['objects']==RESULT['sourceBlobs'] and protocol['sourceBlobCount']==37 and protocol['sourceBlobBytes']==total,'prospective-exact-blob-inventory'
    save()
    phase='public-repository';metadata=api('GET','');assert metadata['full_name']==REPO and metadata['private'] is False and metadata['visibility']=='public'
    RESULT['repositoryMetadata']={k:metadata[k] for k in ('full_name','private','visibility','html_url')};save()
    phase='initial-reference';ref=api('GET','/git/ref/heads/'+BRANCH);assert ref['ref']=='refs/heads/'+BRANCH and ref['object']['type']=='commit' and ref['object']['sha']==PARENT,'initial-branch-not-exact-parent'
    phase='parent-tree';parent=api('GET','/git/commits/'+PARENT);assert parent['sha']==PARENT and parent['tree']['sha']==PARENT_TREE,'remote-parent-tree-mismatch'
    RESULT['parentTreeProof']={'commit':parent['sha'],'tree':parent['tree']['sha']};save()
    entries=[];phase='blobs'
    for path,raw,oid in blobs:
        got=api('POST','/git/blobs',{'content':base64.b64encode(raw).decode(),'encoding':'base64'},201);assert got['sha']==oid,'uploaded-blob-mismatch'
        entries.append({'path':path,'mode':'100644','type':'blob','sha':oid})
    phase='tree';got=api('POST','/git/trees',{'base_tree':PARENT_TREE,'tree':entries},201);RESULT['createdTree']=got['sha'];save();assert got['sha']==TREE,'tree-mismatch-no-ref-update'
    phase='commit';got=api('POST','/git/commits',{'tree':TREE,'parents':[PARENT],'message':MESSAGE,'author':IDENTITY,'committer':IDENTITY},201);RESULT['createdCommit']=got['sha'];save();assert got['sha']==COMMIT,'commit-mismatch-no-ref-update'
    phase='pre-update-reference';ref=api('GET','/git/ref/heads/'+BRANCH);assert ref['ref']=='refs/heads/'+BRANCH and ref['object']['type']=='commit' and ref['object']['sha']==PARENT,'pre-update-branch-not-exact-parent'
    phase='fast-forward';RESULT['refUpdateAttempted']=True;RESULT['refUpdated']='unknown';patch_started=True;save()
    got=api('PATCH','/git/refs/heads/'+BRANCH,{'sha':COMMIT,'force':False});patch_returned=True
    assert got['ref']=='refs/heads/'+BRANCH and got['object']['type']=='commit' and got['object']['sha']==COMMIT,'updated-ref-response-mismatch'
    RESULT['refUpdated']=True
except BaseException as exc:
    RESULT['failure']={'phase':phase,'type':type(exc).__name__,'detail':clean(exc)}
finally:
    # One reserved read-only observation after any attempted PATCH, never a PATCH retry.
    if patch_started:
        try:
            observed=api('GET','/git/ref/heads/'+BRANCH);RESULT['finalReference']=observed
            assert observed['ref']=='refs/heads/'+BRANCH and observed['object']['type']=='commit'
            RESULT['refUpdated']=observed['object']['sha']==COMMIT
            if not RESULT['refUpdated']:raise AssertionError('final-ref-not-exact-commit')
        except BaseException as exc:RESULT['finalReferenceError']={'type':type(exc).__name__,'detail':clean(exc)}
    try:
        RESULT.setdefault('allocationChecks',{})['end']=allocation_state()
        assert PROTOCOL.read_bytes()==protocol_raw,'protocol-changed'
        assert same(HELPER,Path(__file__).read_bytes()),'helper-changed'
        for path,raw,_ in blobs:assert (ROOT/path).read_bytes()==raw,'frozen-source-changed'
    except BaseException as exc:RESULT['endCheckFailure']={'type':type(exc).__name__,'detail':clean(exc)}
    RESULT['acquisitionWallPassed']=time.monotonic()-START<=BOUNDS['overallSeconds']
    RESULT['passed']=patch_returned and RESULT['refUpdated'] is True and RESULT['acquisitionWallPassed'] and not any(k in RESULT for k in ('failure','finalReferenceError','endCheckFailure'))
    RESULT['closed']=True;RESULT['eventJournal']={'file':JOURNAL.relative_to(ROOT).as_posix(),**bid(JOURNAL.read_bytes())};save()
    assert parse(OUT.read_bytes())==RESULT and [parse(x) for x in JOURNAL.read_bytes().splitlines()]==EVENTS
print(json.dumps({k:v for k,v in RESULT.items() if k not in ('events','sourceBlobs','finalReference')},separators=(',',':')))
if not RESULT['passed']:raise SystemExit(1)
