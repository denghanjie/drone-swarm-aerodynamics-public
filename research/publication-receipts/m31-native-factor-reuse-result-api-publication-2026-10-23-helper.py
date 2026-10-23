"""Prospective result/handoff/receipt Git Data API publisher.

Adapted as source text from the reviewed source API publication recovery helper.
No numerical code is imported. Prepare mode is offline and is permitted only
after the actual commit and applicable allocation boundary exist. Publish mode needs
the separately reviewed exact protocol hash. No Git branch/index/worktree edits.
"""
from pathlib import Path, PurePosixPath
import argparse
import base64
import datetime
import hashlib
import json
import math
import os
import re
import selectors
import signal
import subprocess
import tempfile
import time

ROOT=Path(__file__).resolve().parents[2]
REL='research/m31-native-factor-reuse-2026-10-23'
REPO='denghanjie/drone-swarm-aerodynamics-public'
PARENT='7e6ab5b1d3bb819a7a17178c9a5636bde49ca6f2'
PARENT_TREE='a8e6a60e3e676224ee128562d1babbc559d7352a'
SOURCE_PARENT=PARENT
SOURCE_PARENT_TREE=PARENT_TREE
BRANCH='codex/m31-audit-2026-10-15'
RESTART='research/OVERNIGHT-RESTART.md'
PREFIX='research/publication-receipts/m31-native-factor-reuse-result-api-publication-2026-10-23'
CONTEXT=None
BOUNDS=dict(overallSeconds=1800,secondsPerRequest=180,maxRequests=256,
    maxConcurrentRequests=1,attemptsPerMutation=1,attemptsPerRead=1,
    maxRequestPayloadBytes=512*1024**2,maxSingleRequestBytes=160*1024**2,
    maxCapturedResponseBytes=64*1024**2,maxEvidenceBytes=80*1024**2,
    maxEventBytes=16*1024,maxReceiptBytes=8*1024**2,
    maxBlobBytes=100*1024**2,maxChangedFileBytes=768*1024**2,
    maxGitMetadataBytes=64*1024**2,maxGitOperationSeconds=45,
    finalObservationReserveSeconds=180,closureReserveSeconds=10)
OID=re.compile(r'[0-9a-f]{40}')
SHA=re.compile(r'[0-9a-f]{64}')
ENV={k:v for k,v in os.environ.items() if k not in
    ('GH_DEBUG','DEBUG','GIT_EXTERNAL_DIFF','GIT_DIFF_OPTS','GIT_PAGER','GIT_CONFIG_COUNT')}
ENV.update(GH_PROMPT_DISABLED='1',GH_NO_UPDATE_NOTIFIER='1',
    GH_NO_EXTENSION_UPDATE_NOTIFIER='1',GIT_NO_REPLACE_OBJECTS='1',
    GIT_TERMINAL_PROMPT='0',LC_ALL='C')


def need(value,label):
    if not value:raise AssertionError(label)


def bid(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def git_oid(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def compact(value):return json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()
def parse(raw):
    def pairs(values):
        result={}
        for key,value in values:need(key not in result,'duplicate-json-key');result[key]=value
        return result
    def bad(value):raise ValueError('nonfinite-json:'+value)
    def finite(value):
        result=float(value);need(math.isfinite(result),'finite-json-number');return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad,parse_float=finite)


def relative(name):
    need(type(name) is str and name and '\\' not in name and not any(ord(c)<32 for c in name),'safe-relative-path')
    p=PurePosixPath(name)
    need(not p.is_absolute() and str(p)==name and not any(x in ('','.','..') for x in p.parts),'normalized-relative-path')
    return name


def file_path(name):
    name=relative(name);p=ROOT/name
    need(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(ROOT),'regular-local-file:'+name)
    return p


def pin_file(name):
    path=file_path(name);raw=path.read_bytes();return dict(file=name,**bid(raw))


def checked(pin):
    need(set(pin)=={'file','bytes','sha256'},'complete-file-pin')
    need(type(pin['bytes']) is int and pin['bytes']>=0 and SHA.fullmatch(pin['sha256']),'file-pin-types')
    raw=file_path(pin['file']).read_bytes();need(bid(raw)=={k:pin[k] for k in ('bytes','sha256')},'exact-file-identity:'+pin['file'])
    return raw


def configure(context):
    """Each result or supplemental publication is a separate explicit snapshot."""
    global PARENT,PARENT_TREE,PREFIX,CONTEXT
    need(set(context)=={'kind','publicationId','outputPrefix','protocolPath','parent','parentTree','parentPublicationPin','parentIndependentReviewPin'},'exact-publication-context-fields')
    need(context['kind'] in ('result','handoff','supplemental'),'publication-kind')
    need(re.fullmatch(r'm31-native-factor-reuse-[a-z0-9-]{1,110}',context['publicationId']),'publication-id')
    for field in ('outputPrefix','protocolPath'):
        name=relative(context[field]);need(name.startswith('research/publication-receipts/') and len(PurePosixPath(name).parts)==3,'explicit-administrative-output-location')
    need(context['outputPrefix']!=context['protocolPath'],'distinct-prefix-protocol-path')
    prefix=context['outputPrefix'];protocol=context['protocolPath']
    reserved={prefix+suffix for suffix in ('.json','.writing','-events.jsonl','-launch.lock','-plan.json','-plan-launch.lock','-reachability.json','-manifest.json')}
    need(protocol not in reserved and not protocol.startswith(prefix+'-response-'),'protocol-outside-generated-output-paths')
    need(OID.fullmatch(context['parent']) and OID.fullmatch(context['parentTree']),'explicit-parent-tree-OIDs')
    if context['kind'] in ('result','handoff'):
        need(context['parent']==SOURCE_PARENT and context['parentTree']==SOURCE_PARENT_TREE,'first-result-fixed-published-source-parent')
        need(context['parentPublicationPin'] is None and context['parentIndependentReviewPin'] is None,'result-parent-proved-by-frozen-source-binding')
    else:
        publication=parse(checked(context['parentPublicationPin']));review=parse(checked(context['parentIndependentReviewPin']))
        need(publication['passed'] is True and publication['closed'] is True and publication['commit']==context['parent'] and publication['tree']==context['parentTree'],'supplemental-exact-successfully-published-result-parent')
        need(review['passed'] is True and review['phase']=='result' and review['commit']==context['parent'],'supplemental-parent-independent-result-public-identity')
    PARENT=context['parent'];PARENT_TREE=context['parentTree'];PREFIX=context['outputPrefix'];CONTEXT=context


def clean(value):
    value=str(value).replace(str(ROOT),'[repository]')
    value=re.sub(r'/private/(?:tmp|var/folders)/[^\s\"\']+','[temporary]',value)
    value=re.sub(r'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+','[redacted-token]',value)
    return re.sub(r'(?i)(authorization:\s*bearer\s+)\S+',r'\1[redacted]',value)[:2000]


def redacted(raw):
    raw=re.sub(rb'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+',b'[redacted-token]',raw)
    return re.sub(rb'(?i)(authorization:\s*bearer\s+)\S+',rb'\1[redacted]',raw)


class Budget:
    def __init__(self):self.start=time.monotonic();self.git_bytes=0
    def left(self,reserve=0):
        value=BOUNDS['overallSeconds']-(time.monotonic()-self.start)-reserve
        need(value>0,'overall-administrative-wall-cap');return value
    def git(self,args):
        cap=BOUNDS['maxGitMetadataBytes']-self.git_bytes;need(cap>0,'Git-metadata-byte-cap')
        try:out,err,code=capture(['git','--no-pager',*args],min(BOUNDS['maxGitOperationSeconds'],self.left()),cap)
        except BaseException as error:
            self.git_bytes+=len(getattr(error,'captured_stdout',b''))+len(getattr(error,'captured_stderr',b''));raise
        self.git_bytes+=len(out)+len(err)
        need(code==0,'local-Git-metadata-failure:'+clean(err.decode('utf8','replace')))
        return out


def capture(args,seconds,cap,on_chunk=None):
    """One child, bounded capture; no shell, retries, pager or debug credentials."""
    begin=time.monotonic();out=bytearray();err=bytearray();process=None;selector=selectors.DefaultSelector()
    try:
        process=subprocess.Popen(args,cwd=ROOT,env=ENV,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        for stream,label in ((process.stdout,'stdout'),(process.stderr,'stderr')):
            os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,label)
        while selector.get_map():
            left=seconds-(time.monotonic()-begin);need(left>0,'bounded-child-timeout')
            for key,_ in selector.select(min(left,.2)):
                available=cap-len(out)-len(err);need(available>0,'bounded-child-capture-cap')
                data=os.read(key.fileobj.fileno(),min(65536,available))
                if not data:selector.unregister(key.fileobj);continue
                (out if key.data=='stdout' else err).extend(data)
                if on_chunk:on_chunk(data,key.data)
        code=process.wait(timeout=max(.001,seconds-(time.monotonic()-begin)))
        return bytes(out),bytes(err),code
    except BaseException as error:
        if process and process.poll() is None:
            os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=2)
        error.captured_stdout=bytes(out);error.captured_stderr=bytes(err)
        error.child_returncode=None if process is None else process.returncode
        raise
    finally:
        selector.close()
        if process:process.stdout.close();process.stderr.close()


def tree_entries(budget,oid):
    need(OID.fullmatch(oid),'tree-OID')
    raw=budget.git(['ls-tree','-z',oid]);need(raw.endswith(b'\0') or not raw,'tree-NUL-termination')
    values=[];body=bytearray()
    for token in raw.split(b'\0')[:-1]:
        metadata,name=token.split(b'\t',1);mode,kind,child=metadata.split(b' ')
        need(mode in (b'040000',b'100644',b'100755',b'120000',b'160000'),'tree-mode-domain')
        need(kind=={b'040000':b'tree',b'160000':b'commit'}.get(mode,b'blob'),'tree-mode-type')
        need(OID.fullmatch(child.decode()) and b'/' not in name and name not in (b'',b'.',b'..'),'tree-entry-name-OID')
        text=name.decode('utf8');need(text.encode()==name,'lossless-tree-name')
        values.append(dict(name=text,mode=mode.decode(),type=kind.decode(),oid=child.decode()))
        body.extend(mode.lstrip(b'0')+b' '+name+b'\0'+bytes.fromhex(child.decode()))
    need(git_oid('tree',bytes(body))==oid,'local-tree-Merkle-object-identity')
    return values


def reachable_parent_blobs(budget):
    """OID index from metadata only; reused leaves later get full Merkle paths."""
    raw=budget.git(['ls-tree','-r','-z','--full-tree',PARENT]);need(raw.endswith(b'\0'),'parent-tree-index-terminated')
    by_oid={}
    for token in raw.split(b'\0')[:-1]:
        meta,path=token.split(b'\t',1);mode,kind,oid=meta.decode().split()
        if kind=='blob' and mode in ('100644','100755'):
            name=relative(path.decode('utf8'));by_oid.setdefault(oid,dict(path=name,mode=mode))
    return by_oid


def reuse_proof(budget,witnesses):
    cache={}
    for witness in witnesses:
        current=PARENT_TREE
        for i,name in enumerate(PurePosixPath(witness['path']).parts):
            if current not in cache:cache[current]=tree_entries(budget,current)
            matches=[x for x in cache[current] if x['name']==name];need(len(matches)==1,'unique-reused-blob-tree-path');entry=matches[0]
            last=i==len(PurePosixPath(witness['path']).parts)-1
            if last:need(entry['type']=='blob' and entry['oid']==witness['gitBlobOid'] and entry['mode']==witness['mode'],'reused-blob-exact-parent-leaf')
            else:need(entry['type']=='tree','reused-blob-parent-directory');current=entry['oid']
    return dict(schema='m31-parent-tree-blob-reachability-v1',parent=PARENT,rootTree=PARENT_TREE,
        trees=[dict(oid=oid,entries=cache[oid]) for oid in sorted(cache)],witnesses=witnesses,
        scientificContentParsed=False,originalArchivesDecoded=False)


def commit_identity(budget,commit):
    need(OID.fullmatch(commit) and commit!=PARENT,'actual-new-result-commit')
    raw=budget.git(['cat-file','commit',commit]);need(git_oid('commit',raw)==commit,'exact-local-commit-object')
    header,message=raw.split(b'\n\n',1);rows=header.decode('utf8').split('\n')
    need(len(rows)==4 and rows[0].startswith('tree ') and rows[1]=='parent '+PARENT,'single-exact-parent-unsigned-result-commit')
    tree=rows[0][5:];need(OID.fullmatch(tree),'result-tree-OID')
    def person(text,label):
        match=re.fullmatch(label+r' ([^<>\r\n]+) <([^<>\r\n]+)> ([0-9]+) ([+-][0-9]{4})',text);need(match,'exact-commit-person-metadata')
        name,email,epoch,zone=match.groups();epoch=int(epoch);hours=int(zone[1:3]);minutes=int(zone[3:]);need(hours<=23 and minutes<60,'commit-timezone-domain')
        offset=(hours*60+minutes)*(1 if zone[0]=='+' else -1)
        date=datetime.datetime.fromtimestamp(epoch,datetime.timezone(datetime.timedelta(minutes=offset))).isoformat(timespec='seconds')
        return dict(name=name,email=email,epoch=epoch,timezone=zone,date=date)
    author=person(rows[2],'author');committer=person(rows[3],'committer');text=message.decode('utf8');need(text.encode()==message and text.endswith('\n'),'exact-UTF8-newline-terminated-commit-message')
    expected=(f'tree {tree}\nparent {PARENT}\nauthor {author["name"]} <{author["email"]}> {author["epoch"]} {author["timezone"]}\ncommitter {committer["name"]} <{committer["email"]}> {committer["epoch"]} {committer["timezone"]}\n\n'+text).encode()
    need(expected==raw,'lossless-commit-header-and-message-reconstruction')
    need(budget.git(['rev-parse',PARENT+'^{tree}']).strip().decode()==PARENT_TREE,'exact-published-parent-local-tree')
    return dict(commit=commit,tree=tree,commitObject=bid(raw),author=author,committer=committer,message=text)


def manifest_inputs(manifest_pin,extra_pins):
    manifest=parse(checked(manifest_pin));need(type(manifest['files']) is list,'result-manifest-files')
    pins={}
    for entry in manifest['files']:
        name=relative(entry['path']);need(name not in pins,'unique-result-manifest-path')
        pins[name]=dict(file=name,bytes=entry['bytes'],sha256=entry['sha256'])
    need(manifest_pin['file'] not in pins,'manifest-does-not-self-pin');pins[manifest_pin['file']]=manifest_pin
    for entry in extra_pins:
        need(set(entry)=={'file','bytes','sha256'},'explicit-additional-artifact-pin')
        name=relative(entry['file']);need(name not in pins,'unique-additional-artifact');pins[name]=entry
    return manifest,pins


def allocation_boundary(pins):
    if CONTEXT['kind']=='handoff':
        absent=[]
        for phase in ('producer','audit','finalize','ui'):
            absent.extend([REL+'/'+phase+'-supervisor-launch.lock',REL+'/'+phase+'-supervisor.json',REL+'/'+('results' if phase=='producer' else phase)])
        absent.append(REL+'/viewer/pins.json');need(all(not (ROOT/p).exists() for p in absent),'failure-handoff-requires-all-scientific-display-allocations-unstarted')
        return dict(state='all-unstarted',absentPaths=absent,scientificResultExists=False,administrativeFailureNotPromoted=True)
    closure_name=REL+'/ALLOCATION-CLOSURE.json';need(closure_name in pins,'result-closure-in-manifest')
    closure=parse(checked(pins[closure_name]));need(closure['allClosed'] is True,'all-scientific-display-allocations-closed')
    phases=[]
    for phase in ('producer','audit','finalize','ui'):
        name=REL+'/'+phase+'-supervisor.json';path=ROOT/name
        if path.exists():
            need(name in pins,'closed-supervisor-in-result-manifest');value=parse(checked(pins[name]))
            need(value['closed'] is True and type(value['returncode']) is int,'closed-supervisor-record')
            phases.append(dict(phase=phase,state='closed',pin=pins[name],record=value))
        else:
            absent=[REL+'/'+phase+'-supervisor-launch.lock',name,REL+'/'+('results' if phase=='producer' else phase)]
            need(all(not (ROOT/p).exists() for p in absent),'no-unclosed-or-started-allocation')
            phases.append(dict(phase=phase,state='unstarted',absent=absent))
    need(phases[0]['state']=='closed','actual-result-producer-must-be-closed')
    return dict(closurePin=pins[closure_name],closureRecord=closure,phases=phases,
        operationalSuccessRequired=False,negativeOrFailedResultNotPromoted=True)


def frozen_sources_unchanged(budget,pins):
    name=REL+'/source-manifest.json';need(name in pins,'source-manifest-retained-in-result')
    source=parse(checked(pins[name]));protected=[]
    for entry in source['files']:
        p=relative(entry['path']);pin=dict(file=p,bytes=entry['bytes'],sha256=entry['sha256'])
        checked(pin);protected.append(pin)
    # The source manifest itself must be the same blob at parent and result.
    parent=budget.git(['ls-tree','-z',PARENT,'--',name]);need(parent.endswith(b'\0'),'parent-source-manifest-entry')
    meta,path=parent[:-1].split(b'\t');need(path.decode()==name,'parent-source-manifest-path')
    oid=meta.decode().split()[2];need(git_oid('blob',checked(pins[name]))==oid,'unchanged-parent-source-manifest')
    return protected


def build_plan(budget,commit,manifest_pin,extra_pins):
    metadata=commit_identity(budget,commit);manifest,pins=manifest_inputs(manifest_pin,extra_pins)
    expected_manifest=REL+'/result-manifest.json'
    if CONTEXT['kind']=='handoff':
        need(manifest_pin['file'] in (expected_manifest,CONTEXT['outputPrefix']+'-manifest.json'),'exact-explicit-failure-handoff-manifest-location')
    else:need(manifest_pin['file']==expected_manifest,'exact-new-result-manifest-location')
    boundary=allocation_boundary(pins);protected=frozen_sources_unchanged(budget,pins)
    # Full file identities are opaque-byte bindings, never scientific parsing.
    tree_index={}
    entries=budget.git(['ls-tree','-r','-z','--full-tree',commit]);need(entries.endswith(b'\0'),'result-tree-index-terminated')
    for token in entries.split(b'\0')[:-1]:
        meta,path=token.split(b'\t',1);mode,kind,oid=meta.decode().split();tree_index[path.decode('utf8')]=(mode,kind,oid)
    snapshot=[]
    for name,pin in sorted(pins.items()):
        raw=checked(pin);mode,kind,oid=tree_index[name]
        need(kind=='blob' and mode in ('100644','100755') and git_oid('blob',raw)==oid,'complete-result-manifest-commit-snapshot')
        snapshot.append(dict(**pin,mode=mode,gitBlobOid=oid))
    diff=budget.git(['diff-tree','--no-renames','--no-commit-id','--raw','-z','-r',PARENT,commit]).split(b'\0')
    need(diff[-1]==b'' and len(diff)%2==1 and len(diff)>1,'complete-result-tree-diff')
    parent_blobs=reachable_parent_blobs(budget);objects=[];unique={};total=0
    for i in range(0,len(diff)-1,2):
        meta,path=diff[i],relative(diff[i+1].decode('utf8'));oldmode,newmode,oldoid,newoid,status=meta.decode().split()
        need(oldmode.startswith(':') and status in ('A','M') and newmode in ('100644','100755'),'only-explicit-regular-added-modified-result-files')
        oldmode=oldmode[1:];need(OID.fullmatch(oldoid) and OID.fullmatch(newoid),'diff-object-ids')
        need(path in pins,'changed-file-must-have-prospective-manifest-or-additional-pin')
        raw=checked(pins[path]);need(len(raw)<=BOUNDS['maxBlobBytes'],'individual-result-blob-cap')
        need(git_oid('blob',raw)==newoid,'local-file-exact-result-tree-blob')
        total+=len(raw);need(total<=BOUNDS['maxChangedFileBytes'],'total-local-changed-file-cap')
        obj=dict(path=path,oldMode=oldmode,newMode=newmode,oldOid=oldoid,gitBlobOid=newoid,status=status,**bid(raw))
        if CONTEXT['kind']=='handoff' and path==RESTART:
            need(status=='M' and oldmode in ('100644','100755') and newmode==oldmode,'handoff-restart-existing-regular-file-same-mode')
            original=budget.git(['cat-file','blob',oldoid]);need(git_oid('blob',original)==oldoid,'handoff-restart-exact-source-parent-blob')
            need(raw.endswith(original) and len(raw)>len(original),'handoff-restart-original-history-exact-suffix-with-nonempty-prepended-prefix')
            obj['prependOnlyProof']=dict(sourceParent=PARENT,original=bid(original),prependedPrefix=bid(raw[:len(raw)-len(original)]),originalHistoryPreserved=True)
        if newoid in parent_blobs:obj['reuseWitness']=dict(gitBlobOid=newoid,**parent_blobs[newoid])
        else:obj['reuseWitness']=None
        objects.append(obj)
        if newoid in unique:need(identity_blob(unique[newoid])==identity_blob(obj),'same-Git-blob-identical-SHA256-size')
        else:unique[newoid]=obj
    protected_paths={p['file'] for p in protected}|{REL+'/source-manifest.json'}
    need(not protected_paths.intersection(x['path'] for x in objects),'frozen-source-files-cannot-change')
    if CONTEXT['kind']=='handoff':
        need(all(x['path'].startswith('research/publication-receipts/') or x['path']==RESTART for x in objects),'failure-handoff-administrative-artifacts-and-exact-prepend-only-restart-only')
    if CONTEXT['kind']=='supplemental':
        manifest_paths={entry['path'] for entry in manifest['files']}|{manifest_pin['file']}
        need(not manifest_paths.intersection(x['path'] for x in objects),'supplemental-must-not-change-result-or-source-files')
        need(all(x['path'].startswith('research/publication-receipts/') for x in objects),'supplemental-receipt-artifacts-only')
    objects.sort(key=lambda x:x['path'].encode('utf8'))
    reused=[unique[oid]['reuseWitness'] for oid in sorted(unique) if unique[oid]['reuseWitness'] is not None]
    new=[dict(gitBlobOid=oid,path=unique[oid]['path'],**identity_blob(unique[oid])) for oid in sorted(unique) if unique[oid]['reuseWitness'] is None]
    proof=reuse_proof(budget,reused)
    tree_body=dict(base_tree=PARENT_TREE,tree=[dict(path=x['path'],mode=x['newMode'],type='blob',sha=x['gitBlobOid']) for x in objects])
    api_person=lambda p:{k:p[k] for k in ('name','email','date')}
    commit_body=dict(tree=metadata['tree'],parents=[PARENT],message=metadata['message'],author=api_person(metadata['author']),committer=api_person(metadata['committer']))
    bodies=[dict(operation='blob:'+x['gitBlobOid'],bytes=4*((x['bytes']+2)//3)+len(b'{"content":"","encoding":"base64"}')) for x in new]
    bodies.extend([dict(operation='tree',**bid(compact(tree_body))),dict(operation='commit',**bid(compact(commit_body))),dict(operation='reference',**bid(compact(dict(sha=commit,force=False))))])
    payload=sum(x['bytes'] for x in bodies);requests=len(new)+8
    need(payload<=BOUNDS['maxRequestPayloadBytes'] and all(x['bytes']<=BOUNDS['maxSingleRequestBytes'] for x in bodies),'prospective-exact-request-payload-cap')
    need(requests<=BOUNDS['maxRequests'],'prospective-exact-request-count-cap')
    plan=dict(**metadata,manifest=manifest_pin,additionalArtifactPins=extra_pins,objects=objects,
        changedPathCount=len(objects),changedFileBytes=total,uniqueChangedBlobs=len(unique),
        reusedUniqueBlobs=len(reused),newBlobs=new,allocationBoundary=boundary,
        protectedSourceAndInputPins=protected,manifestSnapshot=snapshot,requestPlan=bodies,exactRequestCount=requests,
        exactRequestPayloadBytes=payload,scientificContentParsed=False)
    return plan,proof,tree_body,commit_body


def identity_blob(obj):return {k:obj[k] for k in ('bytes','sha256')}


def write_new(path,value):
    raw=json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2).encode()+b'\n'
    with path.open('xb') as f:need(f.write(raw)==len(raw),'complete-new-administrative-file')
    return dict(file=path.relative_to(ROOT).as_posix(),**bid(raw))


def prepare(args):
    context=dict(kind=args.kind,publicationId=args.publication_id,outputPrefix=args.output_prefix,protocolPath=args.protocol_output,parent=args.parent,parentTree=args.parent_tree,parentPublicationPin=None if args.parent_publication_receipt is None else pin_file(relative(args.parent_publication_receipt)),parentIndependentReviewPin=None if args.parent_independent_review is None else pin_file(relative(args.parent_independent_review)))
    configure(context)
    budget=Budget();out=ROOT/(PREFIX+'-plan.json');proof_path=ROOT/(PREFIX+'-reachability.json');protocol_path=ROOT/context['protocolPath'];lock=ROOT/(PREFIX+'-plan-launch.lock')
    need(not any(p.exists() for p in (out,proof_path,protocol_path,lock)),'single-use-result-plan-already-started')
    with lock.open('x') as f:f.write('single offline administrative result plan; no network\n')
    report=dict(schema='m31-result-api-offline-plan-closure-v1',closed=False,passed=False,networkCalls=0,nativeQueries=0,archiveDecoded=False)
    try:
        manifest_pin=dict(file=relative(args.manifest),bytes=args.manifest_bytes,sha256=args.manifest_sha256)
        extras=[] if args.additional_pins is None else parse(file_path(args.additional_pins).read_bytes())
        need(type(extras) is list,'explicit-additional-pins-list')
        plan,proof,_,_=build_plan(budget,args.commit,manifest_pin,extras);proof_pin=write_new(proof_path,proof)
        helper=pin_file(Path(__file__).resolve().relative_to(ROOT).as_posix())
        protocol=dict(schema='m31-result-api-prospective-publication-v1',status='awaiting-independent-review',
            operation='single-attempt exact-result-object API publication',repository=REPO,parent=PARENT,parentTree=PARENT_TREE,branch=BRANCH,bounds=BOUNDS,
            context=context,helper=helper,reachabilityProof=proof_pin,plan=plan,independentReviewPin=None,reviewed=False,
            executionPermission='require_escalated',publicIdentityVerificationSeparate=True,
            noScientificOrUiAllocation=True,priorPublicationEvidence=[])
        report.update(passed=True,protocol=write_new(protocol_path,protocol),reachabilityProof=proof_pin,
            commit=args.commit,exactRequestCount=plan['exactRequestCount'],exactRequestPayloadBytes=plan['exactRequestPayloadBytes'])
    except BaseException as error:report['failure']=dict(type=type(error).__name__,detail=clean(error))
    finally:
        report.update(closed=True,wallSeconds=time.monotonic()-budget.start,gitMetadataBytes=budget.git_bytes)
        write_new(out,report)
    need(report['passed'],'offline-result-plan-failed-retained')


class Publisher:
    def __init__(self,protocol_pin):
        self.budget=Budget();self.protocol_pin=protocol_pin;self.protocol_raw=checked(protocol_pin);self.protocol=parse(self.protocol_raw)
        configure(self.protocol['context']);need(protocol_pin['file']==CONTEXT['protocolPath'],'explicit-protocol-location')
        self.requests=0;self.payload_bytes=0;self.captured=0;self.evidence_bytes=0;self.events=[];self.operations=set();self.patch_started=False;self.patch_returned=False;self.network_started=False
        self.out=ROOT/(PREFIX+'.json');self.journal=ROOT/(PREFIX+'-events.jsonl');self.lock=ROOT/(PREFIX+'-launch.lock')
        need(not any(p.exists() for p in (self.out,self.journal,self.lock)),'single-use-result-publication-already-started')
        p=self.protocol;need(p['schema']=='m31-result-api-prospective-publication-v1' and p['status']=='reviewed-ready' and p['reviewed'] is True,'reviewed-exact-protocol-required')
        need(p['operation']=='single-attempt exact-result-object API publication' and p['repository']==REPO and p['parent']==PARENT and p['parentTree']==PARENT_TREE and p['branch']==BRANCH and p['bounds']==BOUNDS,'fixed-parent-repository-branch-bounds')
        need(p['executionPermission']=='require_escalated' and p['publicIdentityVerificationSeparate'] is True and p['noScientificOrUiAllocation'] is True,'administrative-publication-only-permission')
        checked(p['independentReviewPin']);need(p['helper']==pin_file(Path(__file__).resolve().relative_to(ROOT).as_posix()),'reviewed-helper-exact-bytes')
        with self.lock.open('x') as f:f.write('single bounded administrative result publication; one mutation attempt per object\n')
        self.journal.touch(exist_ok=False)
        self.result=dict(schema='m31-result-api-publication-v1',closed=False,passed=False,publicationContext=CONTEXT,protocol=protocol_pin,helper=p['helper'],bounds=BOUNDS,parent=PARENT,parentTree=PARENT_TREE,commit=p['plan']['commit'],tree=p['plan']['tree'],branch=BRANCH,events=self.events,refUpdateAttempted=False,refState='not-attempted',nativeQueries=0,archiveDecoded=False,scientificOrUiAllocationLaunched=False,publicIdentityVerificationExecuted=False)
        self.save()
    def save(self):
        self.result.update(wallSeconds=time.monotonic()-self.budget.start,requests=self.requests,requestPayloadBytes=self.payload_bytes,capturedResponseBytes=self.captured,evidenceFileBytes=self.evidence_bytes,gitMetadataBytes=self.budget.git_bytes)
        raw=json.dumps(self.result,ensure_ascii=False,allow_nan=False,indent=2).encode()+b'\n'
        need(len(raw)<=BOUNDS['maxReceiptBytes'],'bounded-administrative-receipt')
        need(self.evidence_bytes+len(raw)<BOUNDS['maxEvidenceBytes'],'administrative-evidence-cap')
        tmp=self.out.with_suffix('.writing');tmp.write_bytes(raw);os.replace(tmp,self.out)
    def event(self,event):
        value=dict(event=len(self.events)+1,**event);self.events.append(value);raw=compact(value)+b'\n'
        need(len(raw)<=BOUNDS['maxEventBytes'],'individual-event-evidence-cap')
        need(self.evidence_bytes+len(raw)<=BOUNDS['maxEvidenceBytes']-BOUNDS['maxReceiptBytes'],'event-evidence-cap-reserves-closure')
        with self.journal.open('ab') as f:need(f.write(raw)==len(raw),'complete-event-append')
        self.evidence_bytes+=len(raw);self.save();return value
    def capture_file(self,raw,request,label):
        safe=redacted(raw);path=ROOT/(PREFIX+'-response-'+str(request).zfill(4)+'.'+label)
        need(self.evidence_bytes+len(safe)<=BOUNDS['maxEvidenceBytes']-BOUNDS['maxReceiptBytes'],'captured-evidence-cap-reserves-closure')
        with path.open('xb') as f:need(f.write(safe)==len(safe),'complete-response-capture')
        self.evidence_bytes+=len(safe)
        return dict(original=bid(raw),saved=dict(file=path.relative_to(ROOT).as_posix(),**bid(safe)),credentialPatternRedacted=safe!=raw)
    def api(self,operation,method,endpoint,body=None,expected_status=200,final=False):
        need(operation not in self.operations,'no-operation-retry');self.operations.add(operation)
        reserve=BOUNDS['closureReserveSeconds']+(0 if final else BOUNDS['finalObservationReserveSeconds'])
        seconds=min(BOUNDS['secondsPerRequest'],self.budget.left(reserve))
        need(self.requests<self.protocol['plan']['exactRequestCount']<=BOUNDS['maxRequests'],'exact-request-count-cap')
        if not final:need(self.requests<self.protocol['plan']['exactRequestCount']-1,'reserved-final-reference-request')
        raw_body=None if body is None else compact(body);size=0 if raw_body is None else len(raw_body)
        need(size<=BOUNDS['maxSingleRequestBytes'] and self.payload_bytes+size<=self.protocol['plan']['exactRequestPayloadBytes']<=BOUNDS['maxRequestPayloadBytes'],'exact-aggregate-outbound-body-cap')
        self.requests+=1;self.payload_bytes+=size;request=self.requests;mutation=method in ('POST','PATCH')
        intent=self.event(dict(kind='request-intent',request=request,operation=operation,attempt=1,method=method,endpoint='https://api.github.com/repos/'+REPO+endpoint,requestBody=None if raw_body is None else bid(raw_body),authenticated=True,mutation=mutation,dispatchOutcome='pending'))
        start=time.monotonic();out=b'';err=b'';code=None;failure=None;self.network_started=True
        try:
            with tempfile.TemporaryDirectory(prefix='m31-result-api-') as directory:
                command=['/opt/homebrew/bin/gh','api','--hostname','github.com','--method',method,'--include','-H','Accept: application/vnd.github+json','-H','X-GitHub-Api-Version: 2022-11-28','repos/'+REPO+endpoint]
                if raw_body is not None:
                    request_file=Path(directory)/'request.json';request_file.write_bytes(raw_body);command+=['--input',str(request_file)]
                cap=BOUNDS['maxCapturedResponseBytes']-self.captured;need(cap>0,'aggregate-response-capture-cap')
                out,err,code=capture(command,seconds,cap)
        except BaseException as error:
            failure=error;out=getattr(error,'captured_stdout',out);err=getattr(error,'captured_stderr',err);code=getattr(error,'child_returncode',code)
        self.captured+=len(out)+len(err)
        receipt=dict(kind='request-result',request=request,intentEvent=intent['event'],operation=operation,method=method,attempt=1,exitCode=code,capturedStdout=self.capture_file(out,request,'http'),capturedStderr=self.capture_file(err,request,'stderr'),wallSeconds=time.monotonic()-start,diagnostic=clean(err.decode('utf8','replace')),transportPassed=False,mutationOutcome='unknown' if mutation else 'not-applicable')
        status=re.match(rb'HTTP/[^\s]+\s+(\d{3})[^\r\n]*\r?\n',out)
        if status:receipt['httpStatus']=int(status.group(1))
        try:
            if failure:raise failure
            need(code==0 and receipt.get('httpStatus')==expected_status,'API-status-or-exit-failure')
            boundary=re.search(rb'\r?\n\r?\n',out);need(boundary and boundary.end()<=65536,'HTTP-header-boundary')
            payload=out[boundary.end():];value=parse(payload);receipt['responseBody']=bid(payload)
            if isinstance(value,dict):receipt['returnedIdentity']={k:clean(value[k]) for k in ('sha','ref','url') if k in value}
            if isinstance(value,dict) and isinstance(value.get('object'),dict):receipt['returnedObject']={k:clean(value['object'][k]) for k in ('sha','type','url') if k in value['object']}
            receipt.update(transportPassed=True,mutationOutcome='response-received' if mutation else 'not-applicable');self.event(receipt);return value
        except BaseException as error:
            receipt.update(errorType=type(error).__name__,detail=clean(error));self.event(receipt);raise
    def run(self):
        p=self.protocol;plan=p['plan'];phase='local-exact-plan';current_plan=None
        try:
            current_plan,proof,tree_body,commit_body=build_plan(self.budget,plan['commit'],plan['manifest'],plan['additionalArtifactPins'])
            need(current_plan==plan,'complete-prospective-plan-identical');need(parse(checked(p['reachabilityProof']))==proof,'reviewed-parent-Merkle-proof-identical')
            self.result['allocationBoundaryStart']=plan['allocationBoundary'];self.result['reachabilityProof']=p['reachabilityProof'];self.result['blobReuse']=dict(changedPaths=plan['changedPathCount'],uniqueBlobs=plan['uniqueChangedBlobs'],reusedUniqueBlobs=plan['reusedUniqueBlobs'],uploadedUniqueBlobsPlanned=len(plan['newBlobs']),scientificContentsParsed=False)
            self.result['priorPublicationEvidence']=[]
            for pin in p['priorPublicationEvidence']:checked(pin);self.result['priorPublicationEvidence'].append(pin)
            self.save();phase='public-repository';metadata=self.api('repository','GET','')
            need(metadata['full_name']==REPO and metadata['private'] is False and metadata['visibility']=='public','public-repository-identity');self.result['repositoryMetadata']={k:metadata[k] for k in ('full_name','private','visibility','html_url')};self.save()
            phase='initial-reference';ref=self.api('initial-reference','GET','/git/ref/heads/'+BRANCH);self.check_ref(ref,PARENT)
            phase='remote-parent-root';parent=self.api('parent-root','GET','/git/commits/'+PARENT);need(parent['sha']==PARENT and parent['tree']['sha']==PARENT_TREE,'remote-exact-parent-root')
            self.result['remoteReachabilityAnchor']=dict(commit=parent['sha'],tree=parent['tree']['sha']);self.save()
            phase='new-blobs'
            for blob in plan['newBlobs']:
                raw=checked(dict(file=blob['path'],**identity_blob(blob)));need(git_oid('blob',raw)==blob['gitBlobOid'],'unchanged-new-blob-before-upload')
                got=self.api('blob:'+blob['gitBlobOid'],'POST','/git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'),201)
                need(got['sha']==blob['gitBlobOid'],'exact-new-blob-returned-OID')
            phase='result-tree';got=self.api('tree','POST','/git/trees',tree_body,201);self.result['createdTree']=got['sha'];self.save();need(got['sha']==plan['tree'],'exact-local-result-root-before-reference-update')
            phase='result-commit';got=self.api('commit','POST','/git/commits',commit_body,201);self.result['createdCommit']=got['sha'];self.save()
            need(got['sha']==plan['commit'] and got['tree']['sha']==plan['tree'] and [x['sha'] for x in got['parents']]==[PARENT],'exact-local-result-commit-before-reference-update')
            phase='pre-update-reference';ref=self.api('pre-update-reference','GET','/git/ref/heads/'+BRANCH);self.check_ref(ref,PARENT)
            phase='fast-forward-reference';self.patch_started=True;self.result.update(refUpdateAttempted=True,refState='unknown');self.save()
            got=self.api('reference','PATCH','/git/refs/heads/'+BRANCH,dict(sha=plan['commit'],force=False));self.patch_returned=True;self.check_ref(got,plan['commit']);self.result['refState']='target-response-received';self.save()
        except BaseException as error:self.result['failure']=dict(phase=phase,type=type(error).__name__,detail=clean(error))
        finally:
            # One reserved read-only observation even after an earlier failed
            # network operation. No failed/unknown mutation is ever retried.
            if self.network_started:
                try:
                    observed=self.api('final-reference','GET','/git/ref/heads/'+BRANCH,final=True);self.result['finalReference']=observed
                    self.check_ref(observed,None);oid=observed['object']['sha'];self.result['refState']='target' if oid==plan['commit'] else 'parent' if oid==PARENT else 'other'
                    need(oid==plan['commit'],'final-reference-not-target')
                except BaseException as error:self.result['finalReferenceError']=dict(type=type(error).__name__,detail=clean(error))
            try:
                need(checked(self.protocol_pin)==self.protocol_raw,'protocol-unchanged-at-closure');checked(p['helper']);checked(p['independentReviewPin']);checked(p['reachabilityProof'])
                _,pins=manifest_inputs(plan['manifest'],plan['additionalArtifactPins']);self.result['allocationBoundaryEnd']=allocation_boundary(pins);need(self.result['allocationBoundaryEnd']==plan['allocationBoundary'],'unchanged-closed-allocation-boundary')
                for obj in plan['objects']:
                    raw=checked(dict(file=obj['path'],**identity_blob(obj)));need(git_oid('blob',raw)==obj['gitBlobOid'],'result-file-unchanged-at-closure')
                for pin in plan['protectedSourceAndInputPins']:checked(pin)
                for entry in plan['manifestSnapshot']:
                    raw=checked({k:entry[k] for k in ('file','bytes','sha256')});need(git_oid('blob',raw)==entry['gitBlobOid'],'complete-manifest-snapshot-unchanged-at-closure')
                if CONTEXT['kind']=='supplemental':checked(CONTEXT['parentPublicationPin']);checked(CONTEXT['parentIndependentReviewPin'])
                need(commit_identity(self.budget,plan['commit'])=={k:plan[k] for k in ('commit','tree','commitObject','author','committer','message')},'exact-local-commit-retained-at-closure')
            except BaseException as error:self.result['endCheckFailure']=dict(type=type(error).__name__,detail=clean(error))
            self.result['wallCapPassed']=time.monotonic()-self.budget.start<=BOUNDS['overallSeconds']
            self.result['passed']=self.patch_returned and self.result['refState']=='target' and self.result['wallCapPassed'] and not any(k in self.result for k in ('failure','finalReferenceError','endCheckFailure'))
            if self.result['passed'] and not (self.requests==plan['exactRequestCount'] and self.payload_bytes==plan['exactRequestPayloadBytes']):
                self.result['accountingFailure']=dict(detail='successful-exact-request-accounting',expectedRequests=plan['exactRequestCount'],expectedRequestPayloadBytes=plan['exactRequestPayloadBytes'])
                self.result['passed']=False
            self.result['closed']=True;self.result['eventJournal']=pin_file(self.journal.relative_to(ROOT).as_posix());self.save()
        need(self.result['passed'],'result-API-publication-failed-retained')
    def check_ref(self,value,expected):
        need(value['ref']=='refs/heads/'+BRANCH and value['object']['type']=='commit' and OID.fullmatch(value['object']['sha']),'exact-branch-reference-shape')
        if expected is not None:need(value['object']['sha']==expected,'branch-not-exact-expected-commit')


def main():
    parser=argparse.ArgumentParser();commands=parser.add_subparsers(dest='mode',required=True)
    draft=commands.add_parser('prepare');draft.add_argument('--kind',choices=['result','handoff','supplemental'],required=True);draft.add_argument('--publication-id',required=True);draft.add_argument('--output-prefix',required=True);draft.add_argument('--protocol-output',required=True);draft.add_argument('--parent',required=True);draft.add_argument('--parent-tree',required=True);draft.add_argument('--parent-publication-receipt');draft.add_argument('--parent-independent-review');draft.add_argument('--commit',required=True);draft.add_argument('--manifest',required=True);draft.add_argument('--manifest-bytes',type=int,required=True);draft.add_argument('--manifest-sha256',required=True);draft.add_argument('--additional-pins')
    publish=commands.add_parser('publish');publish.add_argument('--protocol',required=True);publish.add_argument('--protocol-sha256',required=True)
    args=parser.parse_args()
    def interrupted(signum,frame):raise InterruptedError('administrative-publication-interrupted:'+str(signum))
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,interrupted)
    if args.mode=='prepare':prepare(args)
    else:
        need(SHA.fullmatch(args.protocol_sha256),'reviewed-protocol-SHA256-required')
        pin=pin_file(relative(args.protocol));need(pin['sha256']==args.protocol_sha256,'reviewed-protocol-byte-identity');Publisher(pin).run()


if __name__=='__main__':main()
