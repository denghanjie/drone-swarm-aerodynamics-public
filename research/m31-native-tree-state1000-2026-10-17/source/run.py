"""Single-attempt browser/check supervisor. No scientific imports.
Disabled unless separately reviewed, published, pinned authorization is present.
"""
import time
START = time.monotonic()
from pathlib import Path
import datetime, hashlib, json, os, resource, secrets, signal, subprocess, sys
PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
NAME = 'research/m31-native-tree-state1000-2026-10-17'
STAGES = ('browser', 'check')
FILE_CAP, TOTAL_CAP, ATTEMPT_CAP = 32*1024**2, 256*1024**2, 1024**2
TOTAL_SECONDS, OVERHEAD_SECONDS = 360, 60
DEADLINE = START + TOTAL_SECONDS

def need(value, code):
    if not value: raise ValueError(code)

def wall_guard():
    need(time.monotonic() < DEADLINE, 'total-wall-deadline')

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def identity(path):
    h, n = hashlib.sha256(), 0
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            wall_guard(); h.update(b); n += len(b)
    return {'bytes': n, 'sha256': h.hexdigest()}

def load(path):
    need(path.stat().st_size <= FILE_CAP, 'json-byte-cap')
    return json.loads(path.read_bytes())

def safe(relative):
    need(isinstance(relative,str) and relative and not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'relative-source-path')
    p=ROOT/relative
    need(p.resolve().is_relative_to(ROOT) and p.is_file() and not p.is_symlink(), 'source-location')
    return p

def verify(pin):
    need(identity(safe(pin['path'])) == {k:pin[k] for k in ('bytes','sha256')}, 'pin-identity')

def durable(path, value, first=False):
    raw=(json.dumps(value,allow_nan=False,separators=(',',':'))+'\n').encode()
    need(len(raw)<=ATTEMPT_CAP,'attempt-byte-cap')
    temp=path if first else path.with_name(path.name+'.tmp')
    with temp.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    if not first: os.replace(temp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

def assertions(value, wanted):
    for key, expected in wanted.items():
        found=value
        for part in key.split('.'): found=found[part]
        need(type(found) is type(expected) and found==expected,'completion-assertion:'+key)

def authorize(config):
    need(config['schema']=='m31-native-tree-state1000-supervision-v1' and config['executionAllowed'] is True,'execution-not-authorized')
    a=config['authorization']
    need(isinstance(a,dict) and set(a)=={'id','approvedUtc','reviewedSourceManifestSha256'} and isinstance(a['id'],str) and 1<=len(a['id'])<=128,'authorization-incomplete')
    cutoff=datetime.datetime.fromisoformat(config['launchCutoffUtc'])
    approved=datetime.datetime.fromisoformat(a['approvedUtc'])
    now=datetime.datetime.now(datetime.timezone.utc)
    need(cutoff.tzinfo is not None and approved.tzinfo is not None and approved<=now<cutoff,'authorization-window')
    # reviewedSourceManifestSha256 identifies the reviewed disabled draft. The
    # actual enabled config and authorization are bound by the execution manifest.
    need(len(a['reviewedSourceManifestSha256'])==64 and all(c in '0123456789abcdef' for c in a['reviewedSourceManifestSha256']),'reviewed-draft-pin')
    return cutoff

def usage(paths):
    total=0
    for base_index,base in enumerate(paths):
        base_total=evidence=downstream=0
        if base is None or not base.exists(): continue
        for p in base.rglob('*'):
            wall_guard(); st=p.lstat()
            if p.is_symlink():need(base_index==1,'result-symlink')
            if p.is_symlink() or not p.is_dir():
                need(st.st_size<=FILE_CAP,'per-file-byte-cap');total+=st.st_size;base_total+=st.st_size
                if base_index==0:
                    rel=p.relative_to(base)
                    if rel.parts[0] in ('shards','records','saved-records'):evidence+=st.st_size
                    elif rel.name not in ('run-attempt.json','run-attempt.json.tmp'):downstream+=st.st_size
        if base_index==1:need(base_total<=64*1024**2,'private-output-budget')
        else:need(evidence<=160*1024**2 and downstream<=30*1024**2,'public-output-partitions')
    need(total+2*ATTEMPT_CAP<=TOTAL_CAP,'combined-output-log-scratch-cap')
    return total

def limits(seconds):
    def apply():
        resource.setrlimit(resource.RLIMIT_CPU,(seconds,seconds+1))
        resource.setrlimit(resource.RLIMIT_FSIZE,(FILE_CAP,FILE_CAP))
    return apply

def stop(process, group):
    if group:
        # Guardian is deliberately never polled/reaped before the release.
        need(process.returncode is None,'reaped-group-signal-refused')
        try: os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError: pass
    elif process.poll() is None: process.kill()
    process.wait(timeout=4)

def main(expected,commit):
    global DEADLINE
    need(PACKAGE==ROOT/NAME and len(expected)==64 and len(commit)==40 and all(c in '0123456789abcdef' for c in expected+commit),'arguments')
    # Disabled source exits before attempts, directories or any child spawn.
    config=load(PACKAGE/'config.json'); cutoff=authorize(config)
    remaining=(cutoff-datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    need(remaining>=TOTAL_SECONDS,'full-reservation-unavailable')
    DEADLINE=min(DEADLINE,time.monotonic()+remaining)
    need(config['stageOrder']==list(STAGES),'stage-order')
    need(config['limits']=={'perFileBytes':FILE_CAP,'combinedOutputLogScratchBytes':TOTAL_CAP,'totalWallSeconds':360,'closureAndOverheadSeconds':60,'pollSeconds':0.1,'finalizationByteAllowance':2*ATTEMPT_CAP},'limits')
    need([config['stages'][s]['childWallSeconds'] for s in STAGES]==[120,180],'stage-allocations')
    need(config['preflight']['childWallSeconds']==15 and config['preflight']['runtime']=='python' and config['preflight']['source']==NAME+'/source/validate-saved.py','fixed-saved-preflight')
    need(sys.platform=='darwin' and os.environ.get('RESEARCH_EXECUTION_CONTEXT')=='tool-require-escalated','dispatch-context')
    need(not os.environ.get('NODE_OPTIONS') and not os.environ.get('NODE_PATH'),'node-environment')
    results=PACKAGE/'results'; need(not results.exists(),'fresh-results-directory'); results.mkdir()
    attempt_path=results/'run-attempt.json'
    need(not attempt_path.exists() and not any(results.iterdir()),'single-use-results-no-retry')
    token=secrets.token_hex(32)
    attempt={'schema':'m31-native-tree-state1000-attempt-v1','sourceManifestSha256':expected,'sourceCommit':commit,'runTokenSha256':hashlib.sha256(token.encode()).hexdigest(),'startedUtc':utc(),'status':'running','stageOrder':list(STAGES),'stages':{},'firstFailure':None,'allHelpersExitClaim':False,'memoryLimitClaim':False}
    durable(attempt_path,attempt,True)
    pins=[];protected={};prior={};private=None;process=None;group=False;child_total=0;code=1;child_start=None;active_record=None
    try:
        mf=PACKAGE/'source-manifest.json'; mid=identity(mf);need(mid['sha256']==expected,'manifest-sha')
        manifest=load(mf); pins=manifest['files']; by_path={p['path']:p for p in pins}; need(len(by_path)==len(pins),'duplicate-pins')
        for pin in pins: verify(pin)
        need(load(PACKAGE/'config.json')==config,'config-preservation')
        for rel in ['config.json','source/run.py','source/group-runner.py','source/validate-saved.py','source/transport.cjs','source/transport-store.cjs','prerequisites.json','review/STORAGE-ADMISSION.json']:
            need(NAME+'/'+rel in by_path,'supervisor-source-closure')
        for kind,exe in [('python',Path(sys.executable).resolve()),('node',Path(os.environ['RESEARCH_NODE']).resolve())]:
            need(identity(exe)=={k:manifest['runtime'][kind][k] for k in ('bytes','sha256')},'runtime-'+kind)
        publication_path=PACKAGE/'source-publication.json'; p=load(publication_path)
        need(p['commit']==commit and p['manifestSha256']==expected and p['manifestPath']==NAME+'/source-manifest.json' and p['manifestBytes']==mid['bytes'] and p['verifiedFilePins']==len(pins) and p['remoteBytesEqualLocal'] is True and p['committedBytesEqualLocal'] is True and datetime.datetime.fromisoformat(p['verifiedUtc'])<=datetime.datetime.fromisoformat(attempt['startedUtc']),'publication-binding')
        protected={NAME+'/source-manifest.json':mid,NAME+'/source-publication.json':identity(publication_path)}
        candidate_private=Path(os.environ['RESEARCH_PRIVATE_LOG_DIR']);profile=Path(os.environ['RESEARCH_BROWSER_PROFILE'])
        need(candidate_private.is_absolute() and profile.is_absolute() and not candidate_private.resolve().is_relative_to(ROOT) and profile.resolve()!=candidate_private.resolve() and profile.resolve().is_relative_to(candidate_private.resolve()) and not candidate_private.exists() and not profile.exists(),'fresh-private-locations')
        candidate_private.mkdir(parents=True,exist_ok=False);private=candidate_private
        attempt['privateDirectoryIdentitySha256']=hashlib.sha256(str(private.resolve()).encode()).hexdigest()
        attempt['verifiedPins']=len(pins)
        for stage in ('saved-validation',)+STAGES:
            wall_guard(); authorize(config)
            need(time.monotonic()-START-child_total<OVERHEAD_SECONDS,'shared-overhead-deadline')
            for pin in pins: verify(pin)
            for rel,pin in {**protected,**prior}.items(): need(identity(ROOT/rel)==pin,'prior-artifact-preserved')
            entry=config['preflight'] if stage=='saved-validation' else config['stages'][stage];need(entry['source'] in by_path,'stage-source-pin')
            need(entry['source']==NAME+'/source/'+('controller.cjs' if stage=='browser' else 'validate-saved.py' if stage=='saved-validation' else stage+'.py'),'stage-source')
            output=results/(stage+'.json');need(not output.exists(),'exclusive-stage-output')
            record={'status':'started','startedUtc':utc(),'childWallLimitSeconds':entry['childWallSeconds'],'allocationScope':'shared-overhead' if stage=='saved-validation' else 'stage'};attempt['stages'][stage]=record;active_record=record
            durable(attempt_path,attempt)
            child_start=time.monotonic(); child_deadline=min(DEADLINE,child_start+entry['childWallSeconds'])
            env=dict(os.environ);env.update(RESEARCH_STAGE=stage,RESEARCH_RUN_TOKEN=token,RESEARCH_CHILD_BUDGET_MILLISECONDS=str(entry['childWallSeconds']*1000),RESEARCH_CHILD_DEADLINE_MONOTONIC_NS=str(int(child_deadline*1e9)),RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS=str(int(DEADLINE*1e9)))
            exe=str(Path(sys.executable).resolve()) if entry['runtime']=='python' else os.environ['RESEARCH_NODE']
            command=[exe]+(['-I','-B'] if entry['runtime']=='python' else [])+[str(ROOT/entry['source']),str(ROOT),expected,commit]
            group=stage in ('saved-validation','browser');guard_dir=None
            if group:
                guard_dir=private/(stage+'-supervisor');guard_dir.mkdir()
                env['RESEARCH_SUPERVISOR_DIR']=str(guard_dir)
                command=[str(Path(sys.executable).resolve()),'-I','-B',str(PACKAGE/'source/group-runner.py')]+command
            authorize(config);wall_guard()
            log_path=private/(stage+'.log')
            with log_path.open('xb') as log:
                process=subprocess.Popen(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.PIPE if group else subprocess.DEVNULL,env=env,start_new_session=group,preexec_fn=limits(entry['childWallSeconds']))
                while True:
                    wall_guard();need(time.monotonic()<child_deadline,'child-wall-deadline')
                    usage([results,private])
                    if group:
                        exit_path=guard_dir/'exit.json'
                        if exit_path.exists(): child_code=load(exit_path)['returncode'];break
                    else:
                        child_code=process.poll()
                        if child_code is not None:break
                    time.sleep(min(.1,max(0,child_deadline-time.monotonic())))
                need(child_code==0,'child-exit-'+stage)
                value=load(output);assertions(value,entry['completionAssertions'])
                need(value['sourceCommit']==commit and value['sourceManifestSha256']==expected,'stage-source-binding')
                if group:
                    if stage=='browser': assertions(value,config['browserRootCompletionAssertions'])
                    process.stdin.write(b'R');process.stdin.flush();guardian_code=process.wait(timeout=min(4,max(.01,DEADLINE-time.monotonic())));process=None
                    need(guardian_code==0,'guardian-release')
                    record['guardianReleasedWithoutGroupSignal']=True
                process=None
            child_elapsed=time.monotonic()-child_start
            if stage!='saved-validation': child_total+=child_elapsed
            child_start=None
            need(child_elapsed<=entry['childWallSeconds'],'stage-allocation-exceeded')
            record.update(status='completed',finishedUtc=utc(),wallSeconds=child_elapsed,exitCode=child_code,output=identity(output),privateLog=dict(identity(log_path),published=False))
            for rel,pin in {**protected,**prior}.items():need(identity(ROOT/rel)==pin,'stage-preservation')
            # Includes every sidecar emitted by that stage; later stages may add
            # files but cannot mutate or remove earlier bytes.
            for f in results.rglob('*'):
                if f.is_file() and f!=attempt_path:
                    need(not f.is_symlink(),'result-symlink');prior[str(f.relative_to(ROOT))]=identity(f)
            durable(attempt_path,attempt)
        code=0
    except Exception as error:
        attempt['firstFailure']={'type':type(error).__name__,'code':str(error) if str(error).replace('-','').replace(':','').isalnum() and len(str(error))<=120 else 'supervision-failure'}
    finally:
        if process is not None:
            try: stop(process,group);attempt['failedOwnedChildReaped']=True
            except Exception as error: attempt['cleanupFailure']={'type':type(error).__name__};code=1
        if child_start is not None:
            failed_elapsed=time.monotonic()-child_start
            if active_record is not None and active_record.get('allocationScope')!='shared-overhead':child_total+=failed_elapsed
            if active_record is not None:active_record.update(status='failed',finishedUtc=utc(),wallSeconds=failed_elapsed)
        try:
            for pin in pins:verify(pin)
            for rel,pin in {**protected,**prior}.items():need(identity(ROOT/rel)==pin,'final-preservation')
            attempt['preservationPassed']=bool(pins and protected)
            attempt['outputLogScratchBytes']=usage([results,private])
            need(time.monotonic()-START-child_total<=OVERHEAD_SECONDS,'shared-overhead-deadline')
            wall_guard()
        except Exception as error:attempt['finalizationFailure']={'type':type(error).__name__};code=1
        attempt.update(status='completed' if code==0 and attempt.get('preservationPassed') else 'failed',finishedUtc=utc(),preFinalReportWallSeconds=time.monotonic()-START,stageWallSeconds=child_total,overheadAndClosureSeconds=time.monotonic()-START-child_total,supervisorExitVerified=False,supervisorProcessLifetimePeakRssBytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,peakRssScope='macOS ru_maxrss for this supervisor process lifetime only; not isolated stage, tree aggregate or memory limit',executionRetries=0,timingScope='Entry through pre-final-report timestamp; final durable report write and interpreter exit are outside that timestamp but remain subject to remaining authorization/deadline check; no exact exited-process duration claim')
        durable(attempt_path,attempt)
        need(time.monotonic()<=DEADLINE and datetime.datetime.now(datetime.timezone.utc)<=cutoff,'post-report-total-deadline')
    return 0 if attempt['status']=='completed' else 1

if __name__=='__main__':
    need(len(sys.argv)==3,'usage-run.py-MANIFEST_SHA-SOURCE_COMMIT')
    raise SystemExit(main(*sys.argv[1:]))
