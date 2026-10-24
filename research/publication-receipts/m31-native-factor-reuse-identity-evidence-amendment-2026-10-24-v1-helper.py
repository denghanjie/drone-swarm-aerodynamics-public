"""Prospective administrative metadata/evidence verifier. Never imports scientific code."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,resource,signal,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[2]
PREFIX='research/publication-receipts/m31-native-factor-reuse-identity-evidence-amendment-2026-10-24-v1'
BASE='research/publication-receipts/m31-native-factor-reuse-source-public-review-2026-10-23'
SSH='research/publication-receipts/m31-native-factor-reuse-source-public-review-2026-10-24-ssh-v1'
COMMIT='7e6ab5b1d3bb819a7a17178c9a5636bde49ca6f2'
ORIGIN='bf064b2c4d54c7ed61a55ae1791fa64bf4e044fe'
REPO='denghanjie/drone-swarm-aerodynamics-public'
START=time.monotonic(); PINS={}; EVENTS=[]; REQUESTS=0; CAPTURED=0; CACHE={}; META=None
ENV=dict(os.environ,GH_PROMPT_DISABLED='1',GH_PAGER='cat',PAGER='cat')
for k in ['GH_DEBUG','DEBUG','GH_FORCE_TTY']:ENV.pop(k,None)
def need(x,m):
    if not x:raise ValueError(m)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def gitid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def same(a,b):return all(a[k]==b[k] for k in ('bytes','sha256'))
def left():
    t=570-(time.monotonic()-START);need(t>0,'helper570s-deadline');return t
def emit(operation,**fields):
    e={'event':len(EVENTS)+1,'operation':operation,'atUtc':now(),**fields};EVENTS.append(e)
    with (ROOT/(PREFIX+'-events.jsonl')).open('a') as f:f.write(json.dumps(e,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
    return e['event']
def checked_path(relative):
    left();p=ROOT/relative
    need(not Path(relative).is_absolute() and '..' not in Path(relative).parts and p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(ROOT),'ordinary-contained-file:'+relative)
    return p
def read(relative):
    p=checked_path(relative)
    with p.open('rb') as f:b=f.read(2097153)
    need(len(b)<=2097152,'administrative-record-size:'+relative);left();return b
def record(relative,expected=None):
    b=read(relative);p={'file':relative,**ident(b),'gitBlobSha1':gitid(b)}
    if expected:need(same(p,expected),'pin-mismatch:'+relative)
    PINS[relative]=p;return b
def load(relative,expected=None):return json.loads(record(relative,expected))
def pinned(pin):return load(pin['file'],pin)
def journal(pin):
    b=record(pin['file'],pin);rows=[json.loads(x) for x in b.splitlines()]
    need([e['event'] for e in rows]==list(range(1,len(rows)+1)),'journal-numbering');return rows
def allocations():
    base=ROOT/'research/m31-native-factor-reuse-2026-10-23';paths=[]
    for phase in ['producer','audit','finalize','ui']:
        paths += [base/(phase+'-supervisor-launch.lock'),base/(phase+'-supervisor.json'),base/('results' if phase=='producer' else phase)]
    paths.append(base/'viewer/pins.json');need(not any(os.path.lexists(p) for p in paths),'allocation-already-started')
    return {'allUnstarted':True,'checkedAtUtc':now(),'absentPaths':[str(p.relative_to(ROOT)) for p in paths]}
def child(args,kind,limit=45):
    global REQUESTS,CAPTURED
    left();ispublic=kind=='metadata'
    if ispublic:
        need(REQUESTS<20,'metadata20GET-cap');REQUESTS+=1
        cap=min(3145728,(16777216-CAPTURED)//2);need(cap>0,'metadata16MiB-cap')
        stem=META/f'{REQUESTS:02d}'
    else:cap=4096;stem=META/'local-current'
    out=Path(str(stem)+'.stdout');err=Path(str(stem)+'.stderr')
    def limits():resource.setrlimit(resource.RLIMIT_FSIZE,(cap,cap))
    event=emit(kind+'-start',args=args if ispublic else ['opaque-local-hash'],secondsLimit=min(limit,left()),captureBytesPerStream=cap)
    started=time.monotonic();reason=None
    with out.open('wb') as fo,err.open('wb') as fe:
        p=subprocess.Popen(args,cwd=ROOT,env=ENV,stdin=subprocess.DEVNULL,stdout=fo,stderr=fe,preexec_fn=limits)
        try:p.wait(timeout=min(limit,left()))
        except subprocess.TimeoutExpired:
            reason='time-limit';p.kill();p.wait(timeout=min(2,left()))
    ob=out.read_bytes();eb=err.read_bytes();need(len(ob)<=cap and len(eb)<=cap,'capture-os-limit')
    if ispublic:CAPTURED+=len(ob)+len(eb)
    emit(kind+'-end',startEvent=event,returncode=p.returncode,reason=reason,stdout=ident(ob),stderr=ident(eb),wallSeconds=time.monotonic()-started,aggregateMetadataBytes=CAPTURED)
    need(reason is None and p.returncode==0,'child-failed:'+kind)
    if not ispublic:out.unlink();err.unlink()
    return ob

def fresh_hash(d):
    p=checked_path(d['path'])
    code="import hashlib,json,sys;size=int(sys.argv[2]);h=hashlib.sha256();g=hashlib.sha1(b'blob '+str(size).encode()+bytes([0]));n=0\nwith open(sys.argv[1],'rb') as f:\n while n<=size:\n  b=f.read(min(1048576,size+1-n))\n  if not b:break\n  n+=len(b);h.update(b);g.update(b)\nprint(json.dumps({'bytes':n,'sha256':h.hexdigest(),'gitBlobSha1':g.hexdigest()}))"
    v=json.loads(child([sys.executable,'-c',code,str(p),str(d['bytes'])],'local-hash'))
    need(same(v,d),'fresh-local-identity:'+d['path'])
    if d.get('gitBlobOid'):need(v['gitBlobSha1']==d['gitBlobOid'],'current-local-git-oid')
    return {'path':d['path'],**v}
def get(endpoint):
    need(endpoint.startswith('/repos/'+REPO) and ('/git/commits/' in endpoint or '/git/trees/' in endpoint or endpoint=='/repos/'+REPO),'metadata-route-only')
    if endpoint in CACHE:return CACHE[endpoint]
    raw=child(['gh','api','--method','GET','--hostname','github.com','-H','Accept: application/vnd.github+json',endpoint],'metadata')
    d=json.loads(raw);need(isinstance(d,dict),'json-object');CACHE[endpoint]=d;return d
def tree_at(ref):
    need(re.fullmatch('[0-9a-f]{40}',ref) is not None,'immutable-commit')
    d=get('/repos/'+REPO+'/git/commits/'+ref);need(d.get('sha')==ref,'commit-response-identity')
    oid=d['tree']['sha'];need(re.fullmatch('[0-9a-f]{40}',oid) is not None,'tree-oid')
    t=get('/repos/'+REPO+'/git/trees/'+oid+'?recursive=1');need(t.get('sha')==oid and t.get('truncated') is False and isinstance(t.get('tree'),list),'complete-tree-response')
    m={e['path']:e for e in t['tree']};need(len(m)==len(t['tree']),'unique-tree-paths')
    emit('fresh-public-commit-tree',commit=ref,tree=oid,entryCount=len(m),httpStatusHeadersObserved=False)
    return m
def bind(tree,ref,path,oid,size):
    v=tree.get(path);need(v and v.get('sha')==oid and v.get('type')=='blob' and v.get('mode') in ['100644','100755'] and v.get('size')==size,'public-tree-path-binding:'+ref+':'+path)
    return {'commit':ref,'path':path,'gitBlobSha1':oid,'bytes':size,'mode':v['mode']}
def validate_retained(v3p,manifest):
    descriptors=manifest['files'];by_path={d['path']:d for d in descriptors}
    need(len(by_path)==len(descriptors)==74 and sum(d.get('kind')=='input' for d in descriptors)==35,'manifest-scope')
    groups=[('original',v3p['originalFailure'],v3p['originalJournal'],24),('v1',v3p['priorRecoveryFailure'],v3p['priorRecoveryJournal'],16),('v2',v3p['v2Failure'],v3p['v2Journal'],6),('v3',{'file':BASE+'-recovery-v3-failure.json','bytes':312688,'sha256':'1fd25299c3f2926f64b5109cfc9218f1f51a76dc20acff95a2070c8c3e918610'},{'file':BASE+'-recovery-v3-events.jsonl','bytes':219814,'sha256':'c084104c44cb129b2038ee5cf97298d54b6047a844b93fe105b8d7133df49a1b'},6)]
    records={};event_maps={};failures=[];proofs=[];covered=set()
    for namespace,rpin,jpin,nfail in groups:
        r=pinned(rpin);j=journal(jpin);need(r['passed'] is False and r['events']==j and r['eventJournal']==jpin,'preserved-failed-acquisition')
        failed=[e for e in j if e.get('stage')=='attempt-end' and e.get('passed') is False] if namespace!='original' else [e for e in j if e.get('passed') is False]
        need(len(failed)==nfail and failed==r['failedAttempts'],'exact-failure-history')
        records[namespace]=r;event_maps[namespace]={e['event']:e for e in j};failures.append({'namespace':namespace,'receipt':rpin,'journal':jpin,'failedEvents':[e['event'] for e in failed]})
    for namespace,count in [('original',66),('v2',5)]:
        r=records[namespace];events=event_maps[namespace];need(len(r['fileProofs'])==count,'retained-proof-count')
        for proof in r['fileProofs']:
            d=proof['descriptor'];path=d['path'];need(d==by_path[path] and path not in covered,'exact-disjoint-descriptor')
            chain=[events[n] for n in proof['events']];ops=['local','source-commit']+(['input-origin-commit'] if d.get('kind')=='input' else [])+(['retrieval-commit'] if namespace=='v2' else [])
            need([e['operation'] for e in chain[:-1]]==ops and all(e['passed'] is True and e['path']==path for e in chain),'retained-chain-shape')
            oid=chain[0]['gitBlobSha1'];need(all(same(d,e) and e['gitBlobSha1']==oid for e in chain[:-1]) and chain[1]['commit']==COMMIT,'retained-local-source-binding')
            need(all(e['localIdentityEvent']==chain[0]['event'] for e in chain[1:-1]),'retained-tree-link')
            if d.get('kind')=='input':need(chain[2]['commit']==d['originCommit'] and oid==d['gitBlobOid'],'retained-origin-binding')
            remote=chain[-1];need(remote['returncode']==0 and remote['httpStatus']==200 and same(d,remote['responseBody']) and same(d,remote['publicIdentity']),'retained-public-byte-identity')
            if namespace=='original':
                need(remote['operation']=='public-contents-api' and remote['authenticated'] is True and remote['commitBinding']==COMMIT and remote['gitBlobSha1']==oid and remote['endpoint']=='https://api.github.com/repos/'+REPO+'/contents/'+path+'?ref='+COMMIT,'original-public-route')
            else:
                route=next(x for x in v3p['priorRetrievals'] if x['descriptor']==d)
                need(remote['operation']=='public-raw-cdn' and remote['authenticated'] is False and remote['sourceCommitBinding']==COMMIT and remote['originCommit']==d['originCommit'] and remote['responseGitBlobSha1']==oid and chain[3]['commit']==remote['retrievalCommit']==route['retrievalCommit'] and remote['endpoint']==route['endpoint'] and remote['freshPublicRead'] is True and remote['historicalPublicProofReused'] is False,'v2-public-route')
            proofs.append({'descriptor':d,'namespace':namespace,'events':proof['events'],'transport':'authenticated-contents-api' if namespace=='original' else 'unauthenticated-historical-ref-cdn'});covered.add(path)
    mp={'path':v3p['manifest']['file'],**{k:v3p['manifest'][k] for k in ('bytes','sha256')}}
    mc=[event_maps['original'][i] for i in [1,2,4]];need(all(e['passed'] is True and e['path']==mp['path'] for e in mc) and all(same(mp,e) for e in mc[:2]) and same(mp,mc[-1]['responseBody']) and same(mp,mc[-1]['publicIdentity']) and mc[1]['commit']==COMMIT and mc[-1]['httpStatus']==200 and mc[-1]['returncode']==0,'manifest-public-proof')
    need(mc[0]['gitBlobSha1']==mc[1]['gitBlobSha1'] and mc[1]['localIdentityEvent']==1 and mc[-1]['commitBinding']==COMMIT and mc[-1]['authenticated'] is True and mc[-1]['endpoint']=='https://api.github.com/repos/'+REPO+'/contents/'+mp['path']+'?ref='+COMMIT,'manifest-proof-bindings')
    metadata=event_maps['original'][3];need(metadata==records['original']['repositoryMetadata'] and metadata['passed'] is True and metadata['httpStatus']==200 and metadata['returncode']==0 and metadata['authenticated'] is True and metadata['endpoint']=='https://api.github.com/repos/'+REPO and metadata['repositoryMetadata']=={'full_name':REPO,'private':False,'visibility':'public','html_url':'https://github.com/'+REPO},'public-repository-metadata')
    return proofs, covered, failures, mp

def validate_historical(protocol,by_path):
    results=[]
    for h in protocol['historicalProofs']:
        d=by_path[h['path']];r=pinned(h['receipt']);need(r['passed'] is True and r['independentReviewPassed'] is True and r['allAllocationsUnstartedAtStartAndEnd'] is True,'historical-pass-review-and-allocation')
        e={x['event']:x for x in r['events']};chain=[e[n] for n in h['events']]
        need([x['operation'] for x in chain[:3]]==['local','source-commit','input-origin-commit'],'historical-chain-shape')
        need(all(x['passed'] is True and x['path']==d['path'] for x in chain),'historical-chain-passed')
        need(all(same(d,x) for x in chain[:3]) and chain[1]['commit']==h['historicalSourceCommit'] and chain[2]['commit']==h['historicalOriginCommit'],'historical-local-source-origin')
        remote=chain[-1];need(remote['httpStatus']==200,'historical-recorded-http200')
        if h['route']=='raw-cdn':
            need(remote['operation']=='public' and remote['commit']==h['publicRef'] and remote['url']=='https://raw.githubusercontent.com/'+REPO+'/'+h['publicRef']+'/'+d['path'] and same(d,remote),'historical-cdn-fullbody')
            need('returncode' not in remote,'historical-cdn-no-invented-returncode')
        else:
            need(remote['operation']=='public-contents-api' and remote['returncode']==0 and remote['authenticated'] is True and remote['accept']=='application/vnd.github.raw+json' and remote['endpoint']=='https://api.github.com/repos/'+REPO+'/contents/'+d['path']+'?ref='+h['publicRef'] and same(d,remote['responseBody']),'historical-api-fullbody')
            need(journal(r['eventJournal'])==r['events'],'historical-phase-journal')
            hp=pinned(r['protocol']);need(same(hp['helper'],protocol['historicalVerifierOriginal']),'historical-verifier-original-provenance-pin')
            need(any(p['descriptor']['path']==d['path'] and p['events']==h['events'] for p in r['fileProofs']),'historical-explicit-proof-chain')
        need(not any('gitBlobSha1' in x or 'gitBlobOid' in x for x in chain),'historical-git-oid-was-not-recorded')
        results.append({'descriptor':d,'receipt':h['receipt'],'events':h['events'],'historicalPublicRef':h['publicRef'],'historicalSourceCommit':h['historicalSourceCommit'],'historicalOriginCommit':h['historicalOriginCommit'],'priorCheckpointProofReused':True,'historicalComputedGitBlobOidRecorded':False,'bodyEvidence':{k:d[k] for k in ['bytes','sha256']}})
    need(len(results)==3,'exact-three-historical-proofs');return results

def main(args):
    global META
    need(os.getsid(0)==os.getpid() and os.getpgrp()==os.getpid(),'outer-created-dedicated-process-group')
    META=ROOT/(PREFIX+'-metadata');META.mkdir()
    for s in ['-events.jsonl','-composite.json','-receipt.json']:need(not (ROOT/(PREFIX+s)).exists(),'single-use-output:'+s)
    start=allocations();emit('start',scientificSourceCommit=COMMIT,scope='Administrative metadata and identity only',originalFreshBodyRuleSatisfied=False)
    protocol=pinned({'file':PREFIX+'-protocol.json','bytes':args.protocol_bytes,'sha256':args.protocol_sha256})
    for pin in protocol['sourceFiles']+protocol['evidencePins']:record(pin['file'],pin)
    review=load(args.review_file);need(PINS[args.review_file]['sha256']==args.review_sha256 and review['passed'] is True,'independent-static-review-pass')
    expected=protocol['sourceFiles']+[{'file':PREFIX+'-protocol.json','bytes':args.protocol_bytes,'sha256':args.protocol_sha256}]
    need(sorted(review['reviewedFiles'],key=lambda x:x['file'])==sorted(expected,key=lambda x:x['file']),'review-exact-source-pins')
    need(args.publication_commit!=COMMIT,'separate-prospective-publication')
    repo=get('/repos/'+REPO);need(repo.get('full_name')==REPO and repo.get('private') is False and repo.get('visibility')=='public','exact-public-repository')
    pub=tree_at(args.publication_commit)
    publication_bindings=[]
    for p in list(PINS.values()):publication_bindings.append(bind(pub,args.publication_commit,p['file'],p['gitBlobSha1'],p['bytes']))
    emit('prospective-publication-and-review-bound',commit=args.publication_commit,records=len(publication_bindings),review= PINS[args.review_file])
    manifest=pinned(protocol['manifest']);descriptors=manifest['files'];by_path={d['path']:d for d in descriptors}
    need(all(d['originCommit']==ORIGIN for d in descriptors if d.get('kind')=='input'),'fixed-current-origin')
    v3p=pinned(protocol['v3Protocol']);proofs,covered,failures,mp=validate_retained(v3p,manifest)
    hist=validate_historical(protocol,by_path);need({p['descriptor']['path'] for p in hist}==set(by_path)-covered,'exact-three-missing-only')
    ss=pinned(protocol['sshReceipt']);sj=journal(protocol['sshJournal']);so=pinned(protocol['sshSupervisor'])
    need(ss['passed'] is False and ss['closed'] is True and ss['proofs']==[] and ss['events']==sj and so['passed'] is False and so['closed'] is True and so['processGroupAbsent'] is True,'preserved-ssh-failure-closure')
    fetch=[e for e in sj if e['operation']=='command-end' and 'fetch' in e.get('args',[])]
    need(len(fetch)==1 and fetch[0]['returncode']!=0 and fetch[0]['reason']=='time-limit' and fetch[0]['args'][-1]==by_path[hist[0]['descriptor']['path']]['gitBlobOid'],'exact-one-failed-ssh-fetch')
    for name,p in [('receipt.json',protocol['sshReceipt']),('events.jsonl',protocol['sshJournal'])]:need(any(x['file']==name and same(x,p) for x in so['privateFilePinsAfterProcessCleanup']),'ssh-sealed-copy')
    frozen=descriptors+[mp];local_start=[fresh_hash(d) for d in frozen];loc={d['path']:d for d in local_start}
    trees={COMMIT:tree_at(COMMIT),ORIGIN:tree_at(ORIGIN)}
    for h in protocol['historicalProofs']:
        if h['publicRef'] not in trees:trees[h['publicRef']]=tree_at(h['publicRef'])
    bindings=[]
    for d in frozen:
        v=loc[d['path']];bindings.append(bind(trees[COMMIT],COMMIT,d['path'],v['gitBlobSha1'],d['bytes']))
        if d.get('kind')=='input':bindings.append(bind(trees[ORIGIN],ORIGIN,d['path'],v['gitBlobSha1'],d['bytes']))
    for h in hist:
        d=h['descriptor'];v=loc[d['path']];h['currentLocalIdentity']=v
        h['freshHistoricalPathBinding']=bind(trees[h['historicalPublicRef']],h['historicalPublicRef'],d['path'],v['gitBlobSha1'],d['bytes'])
        h['bridge']='Historical complete-body length/SHA256 = freshly streamed local length/SHA256; canonical Git blob SHA1 computed now = fresh immutable public tree/path OID. No historical computed Git OID is claimed.'
    local_end=[fresh_hash(d) for d in frozen];need(local_start==local_end and len(local_end)==75,'start-end75-local-closure')
    for p in list(PINS.values()):
        need(same(p,ident(read(p['file']))),'evidence-changed-during-verification')
        if not any(x['path']==p['file'] for x in publication_bindings):publication_bindings.append(bind(pub,args.publication_commit,p['file'],p['gitBlobSha1'],p['bytes']))
    end=allocations();left()
    result={'schema':'m31-native-factor-reuse-prospective-amended-source-evidence-composite-v1','passed':True,'scientificSourceCommit':COMMIT,'amendmentPublicationCommit':args.publication_commit,'originalFreshBodyRuleSatisfied':False,'originalAndAllRecoveryGatesRemainFailed':True,'amendedEvidenceRuleSatisfied':True,'currentCycleFileBodyProofs':71,'priorCheckpointFullBodyProofsReused':3,'currentCycleInputBodyProofs':32,'inputFilePins':35,'additionalCurrentCycleManifestBodyProofs':1,'currentCycleBodyReadsIncludingManifest':72,'currentCycleBodyProofNamespaces':{'originalApi':66,'recoveryV2Cdn':5},'fileProofs':proofs,'reusedHistoricalProofs':hist,'retainedManifestPublicProof':{'namespace':'original','events':[1,2,4]},'priorFailedHttpsAttemptsPreserved':52,'priorFailedSshFetchesPreserved':1,'sshRemainingTargetsUnattempted':2,'failureHistory':failures,'sshFailedEvent':fetch[0]['event'],'evidencePins':list(PINS.values()),'freshPublicationBindings':publication_bindings,'freshScientificPathBindings':bindings,'freshLocalIdentityChecks':{'start':local_start,'end':local_end},'frozenLocalIdentitiesCheckedPerClosure':75,'allocationChecks':{'start':start,'end':end},'metadataRequests':REQUESTS,'metadataCapturedBytes':CAPTURED,'httpStatusHeadersObservedForFreshMetadata':False,'scientificExecution':False,'independentCompositeReviewRequiredBeforeScience':True,'wallSeconds':time.monotonic()-START,'checkedAtUtc':now()}
    with (ROOT/(PREFIX+'-composite.json')).open('x') as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--publication-commit',required=True);parser.add_argument('--protocol-sha256',required=True);parser.add_argument('--protocol-bytes',required=True,type=int);parser.add_argument('--review-file',required=True);parser.add_argument('--review-sha256',required=True);a=parser.parse_args()
    try:
        result=main(a);emit('complete',passed=True);receipt={'passed':True,'closed':True,'wallSeconds':time.monotonic()-START,'metadataRequests':REQUESTS,'metadataCapturedBytes':CAPTURED,'composite':{'file':PREFIX+'-composite.json',**ident((ROOT/(PREFIX+'-composite.json')).read_bytes())}}
    except BaseException as exc:
        receipt={'passed':False,'closed':True,'error':{'type':type(exc).__name__,'detail':str(exc)},'wallSeconds':time.monotonic()-START,'metadataRequests':REQUESTS,'metadataCapturedBytes':CAPTURED,'scientificExecution':False}
        try:emit('failure',**receipt)
        except BaseException:pass
    with (ROOT/(PREFIX+'-receipt.json')).open('x') as f:json.dump(receipt,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(receipt));sys.exit(0 if receipt['passed'] else 1)
