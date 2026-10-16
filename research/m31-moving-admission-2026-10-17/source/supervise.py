"""One-shot moving-admission supervision; source-only until final public source gate."""
import argparse,hashlib,json,os,re,signal,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone

WALL_LIMITS={'kernel':600,'checker':600}
GUARDIAN_LIMITS={'kernel':610,'checker':610}
MIB=1024*1024
SCIENTIFIC_TOTAL_LIMIT=256*MIB
KERNEL_TOTAL_LIMIT=192*MIB
CHECKER_TOTAL_LIMIT=64*MIB
LOG_METADATA_LIMIT=16*MIB
AGGREGATE_LIMIT=SCIENTIFIC_TOTAL_LIMIT+LOG_METADATA_LIMIT
INDEX_LIMIT=2*MIB
JOURNAL_LIMIT=4*MIB
SHARD_LIMIT=32*MIB
GENERATION_LIMIT=8*MIB
CHECK_REPORT_LIMIT=2*MIB
REPORT_LIMIT=65536
RSS_LIMIT=1073741824
LAUNCH_CUTOFF='2026-10-16T23:00:00Z'
CUTOFF_EPOCH=datetime.fromisoformat(LAUNCH_CUTOFF.replace('Z','+00:00')).timestamp()

def launch_gate():
    if time.time()>=CUTOFF_EPOCH:raise RuntimeError('Scientific launch cutoff reached')

def sha(b):return hashlib.sha256(b).hexdigest()
def sync_directory(p):
    fd=os.open(p,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
def dump(p,x):
    with p.open('x') as f:
        json.dump(x,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    sync_directory(p.parent)
def pin(p,root):
    relative=p.relative_to(root)
    if p.resolve()!=p or p.is_symlink() or not p.is_file() or '..' in relative.parts:raise RuntimeError('Noncanonical or nonfile evidence path')
    b=p.read_bytes()
    return {'path':str(relative),'bytes':len(b),'sha256':sha(b)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['kernel','checker']);args=parser.parse_args()
    launch_gate()
    if not sys.flags.isolated:raise RuntimeError('Supervisor requires Python isolated mode (-I)')
    loader_keys=['LD_PRELOAD','LD_LIBRARY_PATH','DYLD_INSERT_LIBRARIES','DYLD_LIBRARY_PATH','DYLD_FRAMEWORK_PATH','DYLD_FALLBACK_LIBRARY_PATH','DYLD_FALLBACK_FRAMEWORK_PATH']
    if any(os.environ.get(k) for k in loader_keys):raise RuntimeError('Dynamic loader injection environment refused')
    wall_limit=WALL_LIMITS[args.stage]
    package=Path(__file__).resolve().parents[1];root=package.parents[1]
    mp=package/'source-manifest.json';mb=mp.read_bytes();manifest=json.loads(mb)
    pubpath=package/'source-publication.json';pubbytes=pubpath.read_bytes();publication=json.loads(pubbytes)
    if publication.get('remoteBytesEqualLocal') is not True or publication.get('committedBytesEqualLocal') is not True or publication.get('manifestSha256')!=sha(mb) or publication.get('manifestBytes')!=len(mb) or publication.get('manifestPath')!=str(mp.relative_to(root)) or publication.get('verifiedFilePins')!=len(manifest.get('files',[])) or not re.fullmatch(r'[0-9a-f]{40}',publication.get('commit','')):raise RuntimeError('Source publication gate failed')
    verified=datetime.fromisoformat(publication['verifiedUtc'].replace('Z','+00:00'))
    if verified.tzinfo is None or verified.timestamp()>time.time() or verified.timestamp()>=CUTOFF_EPOCH:raise RuntimeError('Publication receipt time invalid')
    config_path=package/'source/config.json';config_bytes=config_path.read_bytes();config=json.loads(config_bytes)
    if config.get('id')!='m31-moving-admission-v1' or config.get('launchCutoffUtc')!=LAUNCH_CUTOFF:raise RuntimeError('Wrong frozen allocation')
    declared_limits={'kernelSeconds':600,'checkerSeconds':600,'guardianSeconds':610,'rssBytes':RSS_LIMIT,'outputBytes':SCIENTIFIC_TOTAL_LIMIT,'kernelOutputBytes':KERNEL_TOTAL_LIMIT,'checkerOutputBytes':CHECKER_TOTAL_LIMIT,'combinedOutputBytes':AGGREGATE_LIMIT,'sceneBytes':SHARD_LIMIT,'generationBytesPerRun':GENERATION_LIMIT,'indexBytes':INDEX_LIMIT,'journalBytes':JOURNAL_LIMIT,'checkerReportBytes':CHECK_REPORT_LIMIT,'metadataLogBytes':LOG_METADATA_LIMIT}
    if any(config.get('limits',{}).get(k)!=v for k,v in declared_limits.items()):raise RuntimeError('Resource configuration mismatch')

    runtimes=json.loads((package/'runtime-pins.json').read_text());env=os.environ.copy()
    cleared_keys=['NODE_OPTIONS','NODE_PATH','NODE_V8_COVERAGE','NODE_REDIRECT_WARNINGS','PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','PYTHONUSERBASE','PYTHONINSPECT']+loader_keys
    for key in cleared_keys:env.pop(key,None)
    runtime_paths={'node':Path(env['RESEARCH_NODE']).resolve(),'python':Path(sys.executable).resolve()};prior_pins=[];prior_private_pins=[]
    required=['PROTOCOL.md','RECORD-CONTRACT.md','runtime-pins.json','source/config.json','source/interval.cjs','source/rational.cjs','source/adapter.cjs','source/pair-prepared.cjs','source/boxes.cjs','source/tree.cjs','source/loads.cjs','source/methods.cjs','source/canonical.cjs','source/binary64-interval.cjs','source/zero-filter.cjs','source/run.cjs','source/check.py','source/result-contract.json','source/semantic-reference.py','source/pair-reference.py','source/spec.json','source/guardian.py','source/supervise.py']
    generator_required=['outputs/milestone-31-source/'+n for n in ['sim.cjs','grid.cjs','geometry.cjs','factory.cjs','factory-wide.cjs','wall-filter.cjs']]+['outputs/step02c-source/physics.cjs']

    names=[x['path'] for x in manifest['files']]
    if len(names)!=len(set(names)) or any(str((package/n).relative_to(root)) not in names for n in required) or any(n not in names for n in generator_required):raise RuntimeError('Required frozen source missing')
    def identity_check():
        if mp.read_bytes()!=mb or pubpath.read_bytes()!=pubbytes:raise RuntimeError('Publication chain changed')
        head=subprocess.run(['git','-C',str(root),'rev-parse','--verify','HEAD'],capture_output=True,check=True,timeout=15).stdout.decode().strip()
        if head!=publication['commit']:raise RuntimeError('HEAD differs from published source commit')
        def committed_bytes(path):
            return subprocess.run(['git','-C',str(root),'show',publication['commit']+':'+path],capture_output=True,check=True,timeout=15).stdout
        if committed_bytes(str(mp.relative_to(root)))!=mb:raise RuntimeError('Committed manifest changed')
        for x in manifest['files']:
            if pin(root/x['path'],root)!=x:raise RuntimeError('Frozen source pin mismatch')
            committed=committed_bytes(x['path'])
            if len(committed)!=x['bytes'] or sha(committed)!=x['sha256']:raise RuntimeError('Committed source pin mismatch')
        for name,p in runtime_paths.items():
            b=p.read_bytes();expected=runtimes[name]
            if len(b)!=expected['bytes'] or sha(b)!=expected['sha256']:raise RuntimeError('Runtime identity mismatch')
        for x in prior_pins:
            if pin(root/x['path'],root)!=x:raise RuntimeError('Prior stage evidence changed')
        for x in prior_private_pins:
            p=private/x['name'];b=p.read_bytes()
            if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError('Prior private raw log changed')
    identity_check()
    run_ids=[c['id'] for c in config['cases']];control_ids=[c['id'] for c in config['controls']]
    if run_ids!=['run-a','run-b'] or config['scheduledTimes']!=[0,5,10] or len(control_ids)!=4 or len(set(control_ids))!=4 or any(not isinstance(x,str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}',x) for x in control_ids):raise RuntimeError('Declared filename set invalid')
    scene_ids=[run+'-t'+str(t) for run in run_ids for t in config['scheduledTimes']]
    resultdir=package/'results';resultdir.mkdir(exist_ok=True);sync_directory(package)
    if resultdir.is_symlink():raise RuntimeError('Result directory symlink')
    private=Path(env['RESEARCH_PRIVATE_RUN_DIR']);private.mkdir(parents=True,exist_ok=True)
    if private.is_symlink():raise RuntimeError('Private log directory symlink')
    private_identity=sha(str(private.resolve()).encode())
    index_name='index.json';journal_name='kernel-journal.jsonl'
    scene_names={'scenes/'+x+'.json' for x in scene_ids}
    control_names={'controls/'+x+'.json' for x in control_ids}
    generation_names={'generation/'+x+'.json' for x in run_ids}
    reference_names={'reference/'+x+'.json' for x in control_ids+scene_ids}
    mandatory_kernel_names={index_name,journal_name}|control_names|generation_names
    scientific_names=mandatory_kernel_names|scene_names
    checker_names={'check.json'}|reference_names
    report_names={stage+'-supervision.json' for stage in WALL_LIMITS}
    metadata_names={stage+suffix for stage in WALL_LIMITS for suffix in ['-attempt.json','-guardian.jsonl','-stdout.log','-stderr.log','-terminal-error.json']}
    allowed_names=scientific_names|checker_names|report_names|metadata_names
    raw_names={stage+'-'+stream+'.raw' for stage in WALL_LIMITS for stream in ['stdout','stderr']}
    allowed_dirs={'controls','scenes','generation','reference'}

    def account_output():
        totals={'aggregateBytes':0,'scientificBytes':0,'kernelBytes':0,'checkerBytes':0,'indexBytes':0,'journalBytes':0,'sceneControlReferenceBytes':0,'generationBytes':0,'logMetadataBytes':0,'reportBytes':0,'unclassifiedBytes':0}
        files=[];violations=[]
        try:
            for p in sorted(resultdir.rglob('*')):
                name=str(p.relative_to(resultdir))
                if p.is_symlink():violations.append('unexpected-output-file');continue
                if p.is_dir():
                    if name not in allowed_dirs or (args.stage=='kernel' and name=='reference'):violations.append('unexpected-output-directory')
                    continue
                if not p.is_file():violations.append('unexpected-output-file');continue
                size=p.stat().st_size;totals['aggregateBytes']+=size;files.append({'scope':'results','path':name,'bytes':size})
                if name not in allowed_names or (args.stage=='kernel' and (name in checker_names or name.startswith('checker-'))):
                    totals['unclassifiedBytes']+=size;violations.append('unexpected-output-file');continue
                if name in scientific_names:totals['kernelBytes']+=size;totals['scientificBytes']+=size
                elif name in checker_names:totals['checkerBytes']+=size;totals['scientificBytes']+=size
                else:totals['logMetadataBytes']+=size
                if name==index_name:
                    totals['indexBytes']+=size
                    if size>INDEX_LIMIT:violations.append('artifact-output-limit')
                elif name==journal_name:
                    totals['journalBytes']+=size
                    if size>JOURNAL_LIMIT:violations.append('artifact-output-limit')
                elif name in scene_names|control_names|reference_names:
                    totals['sceneControlReferenceBytes']+=size
                    if size>SHARD_LIMIT:violations.append('artifact-output-limit')
                elif name in generation_names:
                    totals['generationBytes']+=size
                    if size>GENERATION_LIMIT:violations.append('artifact-output-limit')
                elif name=='check.json':
                    if size>CHECK_REPORT_LIMIT:violations.append('artifact-output-limit')
                elif name in report_names:
                    totals['reportBytes']+=size
                    if size>REPORT_LIMIT:violations.append('final-report-budget')
            for p in sorted(private.iterdir()):
                name=p.name
                if p.is_symlink() or not p.is_file():violations.append('unexpected-private-log');continue
                size=p.stat().st_size;totals['aggregateBytes']+=size;totals['logMetadataBytes']+=size
                files.append({'scope':'private','path':name,'bytes':size})
                if name not in raw_names or (args.stage=='kernel' and name.startswith('checker-')):violations.append('unexpected-private-log')
            if totals['kernelBytes']>KERNEL_TOTAL_LIMIT:violations.append('kernel-output-limit')
            if totals['checkerBytes']>CHECKER_TOTAL_LIMIT:violations.append('checker-output-limit')
            if totals['scientificBytes']>SCIENTIFIC_TOTAL_LIMIT:violations.append('scientific-output-limit')
            if totals['logMetadataBytes']>LOG_METADATA_LIMIT:violations.append('log-metadata-limit')
            if totals['aggregateBytes']>AGGREGATE_LIMIT:violations.append('output-limit')
        except OSError:violations.append('output-accounting-failure')
        return {**totals,'files':files,'violations':sorted(set(violations))}

    def output_limit_reason(reserve=0):
        accounting=account_output()
        if accounting['violations']:return accounting['violations'][0]
        if accounting['aggregateBytes']+reserve>AGGREGATE_LIMIT:return 'output-limit'
        if accounting['logMetadataBytes']+reserve>LOG_METADATA_LIMIT:return 'log-metadata-limit'
        return None

    initial_reason=output_limit_reason(REPORT_LIMIT)
    if initial_reason:raise RuntimeError(initial_reason)
    if args.stage=='checker':
        if (resultdir/'kernel-terminal-error.json').exists():raise RuntimeError('Kernel finalization failed')
        prev=json.loads((resultdir/'kernel-supervision.json').read_text())
        if prev.get('stage')!='kernel' or any(prev.get(k) is not True for k in ['success','closed','childGroupAbsent','sourceAndRuntimeRechecked','scientificChildAbsentBeforeRelease']) or prev.get('exitCode')!=0 or prev.get('guardianExitCode')!=0 or prev.get('sourceCommit')!=publication['commit'] or prev.get('sourceManifestSha256')!=sha(mb) or prev.get('configSha256')!=sha(config_bytes):raise RuntimeError('Kernel not qualified for saved checker')
        if prev.get('privateLogDirectorySha256')!=private_identity:raise RuntimeError('Private log accounting directory changed')
        raw_pins=prev.get('privateRawLogs')
        kernel_raw_names={'kernel-stdout.raw','kernel-stderr.raw'}
        if not isinstance(raw_pins,list) or len(raw_pins)!=2 or {x.get('name') for x in raw_pins}!=kernel_raw_names:raise RuntimeError('Kernel private raw log set incomplete')
        for x in raw_pins:
            p=private/x['name'];b=p.read_bytes()
            if not p.is_file() or p.is_symlink() or len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError('Kernel private raw log changed')
            prior_private_pins.append(x)
        evidence=prev.get('scientificEvidence')
        expected_paths={str((resultdir/n).relative_to(root)) for n in scientific_names if (resultdir/n).is_file() and not (resultdir/n).is_symlink()}
        if any(not (resultdir/n).is_file() or (resultdir/n).is_symlink() for n in mandatory_kernel_names):raise RuntimeError('Kernel mandatory evidence incomplete')
        if not isinstance(evidence,list) or len(evidence)!=len(expected_paths) or {x.get('path') for x in evidence}!=expected_paths:raise RuntimeError('Kernel scientific evidence set incomplete')
        for x in evidence:
            if pin(root/x['path'],root)!=x:raise RuntimeError('Kernel saved evidence changed')
            prior_pins.append(x)
        kernel_prior_names={'kernel-supervision.json','kernel-attempt.json','kernel-guardian.jsonl','kernel-stdout.log','kernel-stderr.log'}
        if any(not (resultdir/n).is_file() or (resultdir/n).is_symlink() for n in kernel_prior_names):raise RuntimeError('Kernel lifecycle evidence incomplete')
        prior_pins.extend(pin(resultdir/n,root) for n in sorted(kernel_prior_names))
    stage_names=(scientific_names if args.stage=='kernel' else checker_names)|{args.stage+suffix for suffix in ['-attempt.json','-guardian.jsonl','-stdout.log','-stderr.log','-supervision.json','-terminal-error.json']}
    if any((resultdir/n).exists() for n in stage_names) or any((private/(args.stage+'-'+stream+'.raw')).exists() for stream in ['stdout','stderr']):raise RuntimeError('Stage allocation already used or output preexists')
    if args.stage=='kernel' and (any(resultdir.iterdir()) or any(private.iterdir())):raise RuntimeError('Kernel requires empty result and private-log directories')
    identity_check()
    launch_gate()
    dump(resultdir/(args.stage+'-attempt.json'),{'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(mb),'configSha256':sha(config_bytes),'launchCutoffUtc':LAUNCH_CUTOFF,'allocation':'sole attempt; existence prevents retry','startedUtc':datetime.now(timezone.utc).isoformat()})
    output=resultdir/(index_name if args.stage=='kernel' else 'check.json')
    env['RESEARCH_SOURCE_MANIFEST_PATH']=str(mp)
    env['RESEARCH_EXPECTED_MANIFEST_SHA256']=sha(mb);env['RESEARCH_SOURCE_COMMIT']=publication['commit']
    if args.stage=='kernel':
        command=[str(runtime_paths['node']),str(package/'source/run.cjs'),str(package)];template=['NODE','PACKAGE/source/run.cjs','PACKAGE_ROOT']
    else:
        command=[str(runtime_paths['python']),'-I','-B',str(package/'source/check.py'),'--config',str(config_path),'--input',str(resultdir/index_name),'--manifest',str(mp),'--output',str(output),'--root',str(root)]
        template=['PYTHON','-I','-B','PACKAGE/source/check.py','--config','PACKAGE/source/config.json','--input','PACKAGE/results/index.json','--manifest','PACKAGE/source-manifest.json','--output','PACKAGE/results/check.json','--root','REPOSITORY_ROOT']
    events=resultdir/(args.stage+'-guardian.jsonl');env['RESEARCH_CHILD_COMMAND']=json.dumps(command);env['RESEARCH_GUARD_EVENTS']=str(events)
    env['RESEARCH_SUPERVISION_STAGE']=args.stage
    stdout=private/(args.stage+'-stdout.raw');stderr=private/(args.stage+'-stderr.raw')
    report={'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(mb),'configSha256':sha(config_bytes),'launchCutoffUtc':LAUNCH_CUTOFF,'commandTemplate':template,'runtimePins':runtimes,'runtimeIsolation':{'supervisorPythonIsolated':True,'guardianCheckerPythonIsolated':True,'clearedChildEnvironmentKeys':cleared_keys},'wallLimitSeconds':wall_limit,'guardianWallLimitSeconds':GUARDIAN_LIMITS[args.stage],'sampledRssLimitBytes':RSS_LIMIT,'scientificOutputLimitBytes':SCIENTIFIC_TOTAL_LIMIT,'outputLimitBytes':AGGREGATE_LIMIT,'artifactLimitBytes':{'index.json':INDEX_LIMIT,'kernel-journal.jsonl':JOURNAL_LIMIT,'eachSceneControlReference':SHARD_LIMIT,'eachGenerationRecording':GENERATION_LIMIT,'allKernelScientificOutputs':KERNEL_TOTAL_LIMIT,'allCheckerOutputs':CHECKER_TOTAL_LIMIT,'check.json':CHECK_REPORT_LIMIT},'logMetadataLimitBytes':LOG_METADATA_LIMIT,'finalReportLimitBytes':REPORT_LIMIT,'nominalSleepSeconds':0.05,'success':False,'closed':False,'samples':0,'peakSampledGroupRssBytes':0,'maxSampleGapSeconds':0,'terminationReason':None,'containmentScope':'Reviewed scientific children spawn no subprocesses. Retained guardian owns process group; sampling is not hostile-code/escaped-descendant isolation.','accountingScope':'Recursive closed-set results and all private raw logs. Kernel scientific outputs192 MiB plus checker64 MiB share256 MiB. Controls/scenes/references32 MiB each; generation8 MiB per run; index2 MiB; journal4 MiB; check.json2 MiB. Metadata, supervision reports and private/public logs share16 MiB; combined272 MiB. Supervisor reports64 KiB each. Missing scheduled scene files are allowed only for subsequent independent reached/not-reached validation.'}
    started=time.monotonic();last=started;guardian=None;child_exit=None;child_pid=None
    def sample():
        nonlocal last
        now=time.monotonic();report['maxSampleGapSeconds']=max(report['maxSampleGapSeconds'],now-last);last=now
        table=subprocess.run(['ps','-axo','pid=,ppid=,pgid=,rss='],capture_output=True,text=True,timeout=2,check=True).stdout
        allrows=[tuple(map(int,l.split())) for l in table.splitlines() if len(l.split())==4]
        rows=[r for r in allrows if r[2]==guardian.pid];rss=sum(r[3]*1024 for r in rows)
        report['samples']+=1;report['peakSampledGroupRssBytes']=max(report['peakSampledGroupRssBytes'],rss)
        if rss>RSS_LIMIT:raise RuntimeError('rss-limit')
        if len(rows)>2 or any(r[0]!=guardian.pid and r[1]!=guardian.pid for r in rows):raise RuntimeError('unexpected-descendant')
        if any(r[1] in {guardian.pid,child_pid} and r[2]!=guardian.pid for r in allrows):raise RuntimeError('escaped-descendant-observed')
        return rows
    known_reasons={'wall-limit','rss-limit','output-limit','artifact-output-limit','scientific-output-limit','kernel-output-limit','checker-output-limit','log-metadata-limit','final-report-budget','unexpected-output-file','unexpected-output-directory','unexpected-private-log','output-accounting-failure','unexpected-descendant','escaped-descendant-observed','guardian-failure','guardian-exited-before-release','residual-group-member'}
    try:
        with stdout.open('xb') as out,stderr.open('xb') as err:
            launch_gate()
            guardian=subprocess.Popen([str(runtime_paths['python']),'-I','-B',str(package/'source/guardian.py')],cwd=root,env=env,stdout=out,stderr=err,stdin=subprocess.PIPE,text=True,start_new_session=True)
            report['processGroup']=guardian.pid
            while True:
                if time.monotonic()-started>wall_limit:raise RuntimeError('wall-limit')
                reason=output_limit_reason()
                if reason:raise RuntimeError(reason)
                ev=[]
                if events.exists():
                    for line in events.read_text().splitlines():
                        try:ev.append(json.loads(line))
                        except json.JSONDecodeError:pass
                for e in ev:
                    if e['event']=='child-start':child_pid=e['pid']
                    if e['event']=='child-exit':child_exit=e['exitCode']
                    if e['event']=='guardian-failure':raise RuntimeError('guardian-failure')
                rows=sample()
                if guardian.poll() is not None:raise RuntimeError('guardian-exited-before-release')
                if child_exit is not None:
                    if any(r[0]!=guardian.pid for r in rows):raise RuntimeError('residual-group-member')
                    report['scientificChildAbsentBeforeRelease']=True
                    guardian.stdin.write('release\n');guardian.stdin.flush();guardian.wait(timeout=3);break
                time.sleep(0.05)
            report['exitCode']=child_exit;report['guardianExitCode']=guardian.returncode
    except Exception as e:report['terminationReason']=str(e) if str(e) in known_reasons else 'supervisor-'+type(e).__name__
    finally:
        # Signal only while the owned guardian is alive; never signal a reused exited group ID.
        if guardian is not None:
            if guardian.poll() is None:
                try:os.killpg(guardian.pid,signal.SIGTERM)
                except ProcessLookupError:pass
                try:guardian.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    if guardian.poll() is None:os.killpg(guardian.pid,signal.SIGKILL)
                    guardian.wait(timeout=2)
            absent=True
            for _ in range(2):
                try:os.killpg(guardian.pid,0);absent=False
                except ProcessLookupError:pass
                time.sleep(0.05)
            report['childGroupAbsent']=absent
        else:report['childGroupAbsent']=True
        report['closed']=report['childGroupAbsent'];logs=[]
        for p in [stdout,stderr]:
            if not p.exists():continue
            raw=p.read_bytes();text=raw.decode('utf-8',errors='replace').replace(str(root),'REPOSITORY_ROOT').replace(str(private),'PRIVATE_RUN_DIR')
            for n,q in runtime_paths.items():text=text.replace(str(q),n.upper()+'_EXECUTABLE')
            text=text.replace(str(Path.home()),'USER_HOME')
            text=re.sub(r'/private/var/folders/[^\s\"\']+','PRIVATE_TEMP_PATH',text)
            dest=resultdir/(p.stem+'.log')
            with dest.open('x') as f:f.write(text);f.flush();os.fsync(f.fileno())
            sync_directory(resultdir)
            logs.append({'path':str(dest.relative_to(root)),'rawBytes':len(raw),'rawSha256':sha(raw),'publishedBytes':dest.stat().st_size,'publishedSha256':sha(dest.read_bytes()),'redaction':'machine/runtime path prefixes replaced; raw logs retained privately'})
        report['logs']=logs
        for name,p in [('output',output),('journal',resultdir/journal_name)]:
            if p.exists():report[name]=pin(p,root)
        report['scientificEvidence']=[pin(resultdir/n,root) for n in sorted(scientific_names) if (resultdir/n).is_file() and not (resultdir/n).is_symlink()]
        report['privateLogDirectorySha256']=private_identity
        report['privateRawLogs']=[{'name':n,'bytes':(private/n).stat().st_size,'sha256':sha((private/n).read_bytes())} for n in sorted(raw_names) if (private/n).is_file() and not (private/n).is_symlink()]
        if args.stage=='checker':report['checkerEvidence']=[pin(resultdir/n,root) for n in sorted(checker_names) if (resultdir/n).is_file() and not (resultdir/n).is_symlink()]
        try:identity_check();report['sourceAndRuntimeRechecked']=True
        except Exception:report['sourceAndRuntimeRechecked']=False;report['terminationReason']='postrun-identity-failure'
        report['outputAccountingBeforeReport']=account_output()
        report['finalOutputBytesBeforeReport']=report['outputAccountingBeforeReport']['aggregateBytes']
        reason=output_limit_reason(REPORT_LIMIT)
        report['wallSeconds']=time.monotonic()-started
        if report['wallSeconds']>wall_limit:report['terminationReason']='wall-limit'
        if reason:report['terminationReason']=reason
        expected_stage=mandatory_kernel_names if args.stage=='kernel' else {'check.json'}
        if not all((resultdir/n).is_file() and not (resultdir/n).is_symlink() for n in expected_stage):
            if report['terminationReason'] is None:report['terminationReason']='incomplete-stage-evidence'
        report['success']=report.get('exitCode')==0 and report.get('guardianExitCode')==0 and report['terminationReason'] is None and report['closed'] and output.exists()
        if len((json.dumps(report,indent=2)+'\n').encode())>REPORT_LIMIT:raise RuntimeError('final-report-budget')
        dump(resultdir/(args.stage+'-supervision.json'),report)
        print(json.dumps({k:report[k] for k in ['stage','success','closed','wallSeconds','peakSampledGroupRssBytes','terminationReason']}))
    return 0 if report['success'] else 1

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:
        # Finalization failure cannot leave a successful scientific qualification.
        fallback={'success':False,'closed':False,'terminationReason':'supervisor-terminal-'+type(error).__name__,'closureUnproven':True}
        try:
            if len(sys.argv)==2 and sys.argv[1] in {'kernel','checker'}:
                p=Path(__file__).resolve().parents[1]/'results'/(sys.argv[1]+'-terminal-error.json')
                dump(p,fallback)
        except Exception:pass
        print(json.dumps(fallback));sys.exit(1)
