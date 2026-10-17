"""One saved-data layout attempt; no scientific or codec imports."""
import time
START=time.monotonic()
from pathlib import Path
import datetime,hashlib,json,os,resource,secrets,subprocess,sys
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1]
NAME='research/m31-tree-witness-layout-2026-10-17'
MIB=1048576;FILE=32*MIB;TOTAL=64*MIB;RESERVE=2*MIB;REPORT=MIB
DEADLINE=START+300
def need(ok,why):
    if not ok:raise ValueError(why)
def guard():need(time.monotonic()<DEADLINE,'total-wall-deadline')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(file):
    h=hashlib.sha256();n=0
    with file.open('rb') as stream:
        for block in iter(lambda:stream.read(MIB),b''):guard();h.update(block);n+=len(block)
    return {'bytes':n,'sha256':h.hexdigest()}
def load(file):
    need(file.stat().st_size<=FILE,'json-file-cap');return json.loads(file.read_bytes())
def safe(relative):
    need(type(relative) is str and relative and not Path(relative).is_absolute() and '..' not in Path(relative).parts,'source-path')
    f=ROOT/relative;need(f.is_file() and not f.is_symlink() and f.resolve()==f,'source-location');return f
def verify(pin):need(identity(safe(pin['path']))=={k:pin[k] for k in ('bytes','sha256')},'source-pin')
def authorize(config):
    need(config['schema']=='m31-tree-witness-layout-supervision-v1' and config['executionAllowed'] is True,'execution-not-authorized')
    a=config['authorization'];need(type(a) is dict and set(a)=={'id','approvedUtc','reviewedSourceManifestSha256'} and type(a['id']) is str and 1<=len(a['id'])<=128,'authorization-fields')
    need(type(a['reviewedSourceManifestSha256']) is str and len(a['reviewedSourceManifestSha256'])==64 and all(c in '0123456789abcdef' for c in a['reviewedSourceManifestSha256']),'reviewed-draft-pin')
    cutoff=datetime.datetime.fromisoformat(config['launchCutoffUtc']);approved=datetime.datetime.fromisoformat(a['approvedUtc']);now=datetime.datetime.now(datetime.timezone.utc)
    need(cutoff==datetime.datetime(2026,10,17,5,6,20,tzinfo=datetime.timezone.utc) and approved.tzinfo is not None and approved<=now<cutoff,'authorization-window');return cutoff
def durable(path,value,first=False):
    data=(json.dumps(value,allow_nan=False,separators=(',',':'))+'\n').encode();need(len(data)<=REPORT,'report-cap')
    temp=path if first else path.with_name(path.name+'.tmp')
    with temp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    if not first:os.replace(temp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
def usage(results,private):
    total=evidence=other=secret=0
    for is_private,base in ((False,results),(True,private)):
        if base is None or not base.exists():continue
        for f in base.rglob('*'):
            guard();need(not f.is_symlink(),'output-symlink')
            if f.is_dir():continue
            need(f.is_file(),'output-file-type');n=f.stat().st_size;need(n<=FILE,'file-cap');total+=n
            if is_private:secret+=n
            elif f.relative_to(base).parts[0] in ('shards','records'):evidence+=n
            elif f.name not in ('run-attempt.json','run-attempt.json.tmp'):other+=n
    need(evidence<=56*MIB and secret<=4*MIB and other<=2*MIB,'output-partition-cap');need(total+RESERVE<=TOTAL,'aggregate-cap');return total
def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(120,121));resource.setrlimit(resource.RLIMIT_FSIZE,(FILE,FILE))
def main(expected,commit):
    global DEADLINE
    need(PACKAGE==ROOT/NAME and len(expected)==64 and len(commit)==40 and all(c in '0123456789abcdef' for c in expected+commit),'arguments')
    config=load(PACKAGE/'config.json');cutoff=authorize(config)
    need((cutoff-datetime.datetime.now(datetime.timezone.utc)).total_seconds()>=300,'full-reservation-unavailable')
    need(config['stageOrder']==['candidate','check'] and config['limits']=={'totalWallSeconds':300,'closureAndOverheadSeconds':60,'perFileBytes':FILE,'combinedOutputLogScratchBytes':TOTAL,'evidenceBytes':56*MIB,'privateBytes':4*MIB,'otherPublicBytes':2*MIB,'finalizationByteAllowance':RESERVE,'chunkBytes':MIB,'pollSeconds':0.1},'fixed-limits')
    for stage,runtime,filename in [('candidate','node','candidate.cjs'),('check','python','check.py')]:
        need(config['stages'][stage]=={'runtime':runtime,'source':NAME+'/source/'+filename,'childWallSeconds':120,'completionAssertions':{'complete':True,'passed':True}},'fixed-stage')
    need(sys.platform=='darwin' and os.environ.get('RESEARCH_EXECUTION_CONTEXT')=='tool-require-escalated' and not os.environ.get('NODE_OPTIONS') and not os.environ.get('NODE_PATH'),'dispatch-context')
    manifest_path=PACKAGE/'source-manifest.json';mid=identity(manifest_path);need(mid['sha256']==expected,'manifest-sha');manifest=load(manifest_path);pins=manifest['files'];by={p['path']:p for p in pins};need(len(by)==len(pins),'duplicate-source-pins')
    for pin in pins:verify(pin)
    for rel in ('config.json','PROTOCOL.md','input-index.json','input-manifest.json','runtime.json','source/source-bundle.json','source/run.py','source/candidate.cjs','source/check.py'):need(NAME+'/'+rel in by,'source-closure')
    need(load(PACKAGE/'config.json')==config,'config-preservation')
    input_manifest=load(PACKAGE/'input-manifest.json');need(input_manifest['schema']=='m31-tree-witness-layout-input-manifest-v1','input-manifest-schema')
    for pin in input_manifest['files']:need(by.get(pin['path'])==pin,'input-source-closure')
    source_bundle=load(PACKAGE/'source/source-bundle.json');need(source_bundle['schema']=='m31-tree-witness-layout-source-closure-v1','source-bundle-schema')
    for pin in source_bundle['sourceFiles']+source_bundle['frozenDecoderFiles']+[source_bundle['inputManifestPin']]:need(by.get(pin['path'])==pin,'bundle-source-closure')
    runtime=load(PACKAGE/'runtime.json')
    for kind in ('node','python'):need(manifest['runtime'][kind]==runtime[kind],'runtime-metadata-binding')
    for kind,file in [('python',Path(sys.executable).resolve()),('node',Path(os.environ['RESEARCH_NODE']).resolve())]:need(identity(file)=={k:manifest['runtime'][kind][k] for k in ('bytes','sha256')},'runtime-'+kind)
    publication_path=PACKAGE/'source-publication.json';publication=load(publication_path)
    need(publication['commit']==commit and publication['manifestSha256']==expected and publication['manifestPath']==NAME+'/source-manifest.json' and publication['manifestBytes']==mid['bytes'] and publication['verifiedFilePins']==len(pins) and publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True and datetime.datetime.fromisoformat(publication['verifiedUtc'])<=datetime.datetime.now(datetime.timezone.utc),'publication-binding')
    results=PACKAGE/'results';private=Path(os.environ['RESEARCH_PRIVATE_LOG_DIR'])
    need(not results.exists() and private.is_absolute() and private.resolve()==private and not private.is_relative_to(ROOT) and not private.exists() and private.parent.is_dir(),'fresh-output-locations')
    authorize(config);guard();need((cutoff-datetime.datetime.now(datetime.timezone.utc)).total_seconds()>=300,'full-reservation-before-marker')
    results.mkdir();private.mkdir();token=secrets.token_hex(32);attempt_path=results/'run-attempt.json'
    attempt={'schema':'m31-tree-witness-layout-attempt-v1','sourceManifestSha256':expected,'sourceCommit':commit,'runTokenSha256':hashlib.sha256(token.encode()).hexdigest(),'startedUtc':utc(),'status':'running','stageOrder':['candidate','check'],'stages':{},'firstFailure':None,'executionRetries':0,'allDescendantsExitClaim':False,'memoryLimitClaim':False}
    durable(attempt_path,attempt,True);protected={NAME+'/source-manifest.json':mid,NAME+'/source-publication.json':identity(publication_path)};prior={};process=None;child_start=None;active=None;child_total=0;code=1
    try:
        for stage in config['stageOrder']:
            authorize(config);guard();need(time.monotonic()-START-child_total<60,'shared-overhead-deadline')
            for pin in pins:verify(pin)
            for rel,pin in {**protected,**prior}.items():need(identity(ROOT/rel)==pin,'prior-preservation')
            output=results/(stage+'.json');need(not output.exists(),'exclusive-stage-output');entry=config['stages'][stage]
            active={'status':'started','startedUtc':utc(),'childWallLimitSeconds':120};attempt['stages'][stage]=active;durable(attempt_path,attempt)
            child_start=time.monotonic();child_deadline=min(DEADLINE,child_start+120)
            env=dict(os.environ);env.update(RESEARCH_STAGE=stage,RESEARCH_RUN_TOKEN=token,RESEARCH_CHILD_BUDGET_MILLISECONDS='120000',RESEARCH_CHILD_DEADLINE_MONOTONIC_NS=str(int(child_deadline*1e9)),RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS=str(int(DEADLINE*1e9)))
            command=([str(Path(sys.executable).resolve()),'-I','-B'] if stage=='check' else [os.environ['RESEARCH_NODE']])+[str(ROOT/entry['source']),str(ROOT),expected,commit]
            log_path=private/(stage+'.log')
            with log_path.open('xb') as log:
                process=subprocess.Popen(command,cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,preexec_fn=limits)
                while True:
                    guard();authorize(config);need(time.monotonic()<child_deadline,'child-wall-deadline');usage(results,private)
                    child_code=process.poll()
                    if child_code is not None:break
                    time.sleep(min(.1,max(0,child_deadline-time.monotonic())))
                need(child_code==0,'child-exit-'+stage);process=None
            elapsed=time.monotonic()-child_start;child_total+=elapsed;child_start=None;need(elapsed<=120,'stage-allocation')
            active.update(wallSeconds=elapsed,exitCode=child_code)
            value=load(output);need(value['complete'] is True and value['passed'] is True and value['sourceManifestSha256']==expected and value['sourceCommit']==commit,'stage-completion')
            active.update(status='completed',finishedUtc=utc(),wallSeconds=elapsed,exitCode=child_code,output=identity(output),privateLog=dict(identity(log_path),published=False))
            for rel,pin in {**protected,**prior}.items():need(identity(ROOT/rel)==pin,'stage-preservation')
            for f in results.rglob('*'):
                if f.is_file() and f!=attempt_path:need(not f.is_symlink(),'result-symlink');prior[str(f.relative_to(ROOT))]=identity(f)
            durable(attempt_path,attempt)
        code=0
    except Exception as error:
        attempt['firstFailure']={'type':type(error).__name__,'code':str(error) if len(str(error))<=120 and str(error).replace('-','').isalnum() else 'supervision-failure'}
        if active is not None and active.get('status')=='started':active.update(status='failed',finishedUtc=utc())
    finally:
        if process is not None:
            try:
                if process.poll() is None:process.kill()
                process.wait(timeout=4);attempt['failedOwnedChildReaped']=True
            except Exception as error:attempt['cleanupFailure']={'type':type(error).__name__};code=1
        if child_start is not None:
            elapsed=time.monotonic()-child_start;child_total+=elapsed
            if active is not None:active.update(status='failed',finishedUtc=utc(),wallSeconds=elapsed)
        try:
            for pin in pins:verify(pin)
            for rel,pin in {**protected,**prior}.items():need(identity(ROOT/rel)==pin,'final-preservation')
            attempt['preservationPassed']=True;attempt['outputLogScratchBytes']=usage(results,private);need(time.monotonic()-START-child_total<=60,'shared-overhead-deadline');guard()
        except Exception as error:attempt['finalizationFailure']={'type':type(error).__name__};code=1
        attempt.update(status='completed' if code==0 and attempt.get('preservationPassed') else 'failed',finishedUtc=utc(),preFinalReportWallSeconds=time.monotonic()-START,stageWallSeconds=child_total,overheadAndClosureSeconds=time.monotonic()-START-child_total,supervisorExitVerified=False,supervisorProcessLifetimePeakRssBytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,peakRssScope='macOS supervisor-process lifetime only; not total memory or a memory limit',timingScope='Pre-final-report timestamps; report write and interpreter exit are outside this timestamp and subject to remaining deadline')
        durable(attempt_path,attempt);need(time.monotonic()<=DEADLINE and datetime.datetime.now(datetime.timezone.utc)<=cutoff,'post-report-deadline')
    return 0 if attempt['status']=='completed' else 1
if __name__=='__main__':
    need(len(sys.argv)==3,'usage-run-MANIFEST-SHA-COMMIT');raise SystemExit(main(*sys.argv[1:]))
