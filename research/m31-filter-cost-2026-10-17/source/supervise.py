"""One-shot filter-cost supervision with recursive, closed-set output accounting."""
import argparse,hashlib,json,os,re,signal,subprocess,sys,time
from pathlib import Path

WALL_LIMITS={'kernel':600,'checker':600}
GUARDIAN_LIMITS={'kernel':610,'checker':610}
MIB=1024*1024
AGGREGATE_LIMIT=768*MIB
INDEX_LIMIT=8*MIB
JOURNAL_LIMIT=8*MIB
SHARD_LIMIT=128*MIB
SCIENTIFIC_TOTAL_LIMIT=384*MIB
CHECKER_TOTAL_LIMIT=128*MIB
LOG_METADATA_LIMIT=16*MIB
REPORT_LIMIT=65536
RSS_LIMIT=1073741824

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
    wall_limit=WALL_LIMITS[args.stage]
    package=Path(__file__).resolve().parents[1];root=package.parents[1]
    mp=package/'source-manifest.json';mb=mp.read_bytes();manifest=json.loads(mb)
    pubpath=package/'source-publication.json';pubbytes=pubpath.read_bytes();publication=json.loads(pubbytes)
    if publication.get('remoteBytesEqualLocal') is not True or publication.get('committedBytesEqualLocal') is not True or publication.get('manifestSha256')!=sha(mb) or publication.get('manifestBytes')!=len(mb) or not re.fullmatch(r'[0-9a-f]{40}',publication.get('commit','')):raise RuntimeError('Source publication gate failed')
    runtimes=json.loads((package/'runtime-pins.json').read_text());env=os.environ.copy()
    runtime_paths={'node':Path(env['RESEARCH_NODE']).resolve(),'python':Path(sys.executable).resolve()};prior_pins=[];prior_private_pins=[]
    required=['PROTOCOL.md','runtime-pins.json','source/interval.cjs','source/rational.cjs','source/adapter.cjs','source/pair-prepared.cjs','source/boxes.cjs','source/tree.cjs','source/loads.cjs','source/methods.cjs','source/canonical.cjs','source/binary64-interval.cjs','source/zero-filter.cjs','source/run.cjs','source/check.py','source/semantic-reference.py','source/pair-reference.py','source/spec.json','source/result-contract.json','source/guardian.py','source/supervise.py']
    names=[x['path'] for x in manifest['files']]
    if len(names)!=len(set(names)) or any(str((package/n).relative_to(root)) not in names for n in required):raise RuntimeError('Required frozen source missing')
    def identity_check():
        if mp.read_bytes()!=mb or pubpath.read_bytes()!=pubbytes:raise RuntimeError('Publication chain changed')
        for x in manifest['files']:
            if pin(root/x['path'],root)!=x:raise RuntimeError('Frozen source pin mismatch')
        for name,p in runtime_paths.items():
            b=p.read_bytes();expected=runtimes[name]
            if len(b)!=expected['bytes'] or sha(b)!=expected['sha256']:raise RuntimeError('Runtime identity mismatch')
        for x in prior_pins:
            if pin(root/x['path'],root)!=x:raise RuntimeError('Prior stage evidence changed')
        for x in prior_private_pins:
            p=private/x['name'];b=p.read_bytes()
            if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError('Prior private raw log changed')
    identity_check()
    spec=json.loads((package/'source/spec.json').read_text())
    scene_ids=[s['id'] for s in spec['scenes']]
    if len(scene_ids)!=6 or len(set(scene_ids))!=6 or any(not isinstance(s,str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}',s) for s in scene_ids):raise RuntimeError('Declared scene filename set invalid')
    resultdir=package/'results';resultdir.mkdir(exist_ok=True);sync_directory(package)
    if resultdir.is_symlink():raise RuntimeError('Result directory symlink')
    private=Path(env['RESEARCH_PRIVATE_RUN_DIR']);private.mkdir(parents=True,exist_ok=True)
    if private.is_symlink():raise RuntimeError('Private log directory symlink')
    private_identity=sha(str(private.resolve()).encode())
    index_name='timing-index.json';journal_name=index_name+'.jsonl'
    scene_names={'scenes/'+s+'.json' for s in scene_ids}
    anomaly_names={'anomalies/first-mismatch.json'}
    reference_names={'reference-scenes/'+s+'.json' for s in scene_ids}
    scientific_names={index_name,journal_name}|scene_names
    checker_names={'independent-check.json'}|reference_names
    report_names={s+'-supervision.json' for s in WALL_LIMITS}
    metadata_names={s+suffix for s in WALL_LIMITS for suffix in ['-attempt.json','-guardian.jsonl','-stdout.log','-stderr.log','-terminal-error.json']}
    allowed_names=scientific_names|anomaly_names|checker_names|report_names|metadata_names
    raw_names={s+'-'+stream+'.raw' for s in WALL_LIMITS for stream in ['stdout','stderr']}
    allowed_dirs={'scenes','anomalies','reference-scenes'}

    def account_output():
        totals={'aggregateBytes':0,'indexBytes':0,'journalBytes':0,'scientificShardBytes':0,'checkerBytes':0,'logMetadataBytes':0,'reportBytes':0,'unclassifiedBytes':0}
        files=[];violations=[];anomalies=0
        try:
            for p in sorted(resultdir.rglob('*')):
                name=str(p.relative_to(resultdir))
                if p.is_symlink():violations.append('unexpected-output-file');continue
                if p.is_dir():
                    if name not in allowed_dirs:violations.append('unexpected-output-directory')
                    continue
                if not p.is_file():violations.append('unexpected-output-file');continue
                size=p.stat().st_size;totals['aggregateBytes']+=size;files.append({'scope':'results','path':name,'bytes':size})
                if name not in allowed_names:
                    totals['unclassifiedBytes']+=size;violations.append('unexpected-output-file');continue
                if name==index_name:
                    totals['indexBytes']+=size
                    if size>INDEX_LIMIT:violations.append('artifact-output-limit')
                elif name==journal_name:
                    totals['journalBytes']+=size
                    if size>JOURNAL_LIMIT:violations.append('artifact-output-limit')
                elif name in scene_names or name in anomaly_names:
                    totals['scientificShardBytes']+=size
                    if name in anomaly_names:anomalies+=1
                    if size>SHARD_LIMIT:violations.append('artifact-output-limit')
                elif name in checker_names:totals['checkerBytes']+=size
                elif name in report_names:
                    totals['reportBytes']+=size
                    if size>REPORT_LIMIT:violations.append('final-report-budget')
                else:totals['logMetadataBytes']+=size
            # Include all four private raw logs and reject every unallocated private entry.
            for p in sorted(private.iterdir()):
                name=p.name
                if p.is_symlink() or not p.is_file():violations.append('unexpected-private-log');continue
                size=p.stat().st_size;totals['aggregateBytes']+=size;totals['logMetadataBytes']+=size
                files.append({'scope':'private','path':name,'bytes':size})
                if name not in raw_names:violations.append('unexpected-private-log')
            if anomalies>1:violations.append('unexpected-anomaly-count')
            if totals['scientificShardBytes']>SCIENTIFIC_TOTAL_LIMIT:violations.append('scientific-output-limit')
            if totals['checkerBytes']>CHECKER_TOTAL_LIMIT:violations.append('checker-output-limit')
            if totals['logMetadataBytes']>LOG_METADATA_LIMIT:violations.append('log-metadata-limit')
            if totals['aggregateBytes']>AGGREGATE_LIMIT:violations.append('output-limit')
        except OSError:violations.append('output-accounting-failure')
        return {**totals,'anomalyFiles':anomalies,'files':files,'violations':sorted(set(violations))}

    def output_limit_reason(reserve=0):
        accounting=account_output()
        if accounting['violations']:return accounting['violations'][0]
        if accounting['aggregateBytes']+reserve>AGGREGATE_LIMIT:return 'output-limit'
        return None

    initial_reason=output_limit_reason(REPORT_LIMIT)
    if initial_reason:raise RuntimeError(initial_reason)
    if args.stage=='checker':
        if (resultdir/'kernel-terminal-error.json').exists():raise RuntimeError('Kernel finalization failed')
        prev=json.loads((resultdir/'kernel-supervision.json').read_text())
        if prev.get('stage')!='kernel' or any(prev.get(k) is not True for k in ['success','closed','childGroupAbsent','sourceAndRuntimeRechecked','scientificChildAbsentBeforeRelease']) or prev.get('exitCode')!=0 or prev.get('guardianExitCode')!=0 or prev.get('sourceCommit')!=publication['commit'] or prev.get('sourceManifestSha256')!=sha(mb):raise RuntimeError('Kernel not qualified for saved checker')
        if prev.get('privateLogDirectorySha256')!=private_identity:raise RuntimeError('Private log accounting directory changed')
        raw_pins=prev.get('privateRawLogs')
        kernel_raw_names={'kernel-stdout.raw','kernel-stderr.raw'}
        if not isinstance(raw_pins,list) or len(raw_pins)!=2 or {x.get('name') for x in raw_pins}!=kernel_raw_names:raise RuntimeError('Kernel private raw log set incomplete')
        for x in raw_pins:
            p=private/x['name'];b=p.read_bytes()
            if not p.is_file() or p.is_symlink() or len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError('Kernel private raw log changed')
            prior_private_pins.append(x)
        evidence=prev.get('scientificEvidence')
        expected_paths={str((resultdir/n).relative_to(root)) for n in scientific_names}
        if not isinstance(evidence,list) or len(evidence)!=len(expected_paths) or {x.get('path') for x in evidence}!=expected_paths:raise RuntimeError('Kernel scientific evidence set incomplete')
        if any((resultdir/n).exists() for n in anomaly_names):raise RuntimeError('Kernel mismatch anomaly present')
        for x in evidence:
            if pin(root/x['path'],root)!=x:raise RuntimeError('Kernel saved evidence changed')
            prior_pins.append(x)
        kernel_prior_names={'kernel-supervision.json','kernel-attempt.json','kernel-guardian.jsonl','kernel-stdout.log','kernel-stderr.log'}
        if any(not (resultdir/n).is_file() or (resultdir/n).is_symlink() for n in kernel_prior_names):raise RuntimeError('Kernel lifecycle evidence incomplete')
        prior_pins.extend(pin(resultdir/n,root) for n in sorted(kernel_prior_names))
    stage_names=((scientific_names|anomaly_names) if args.stage=='kernel' else checker_names)|{args.stage+suffix for suffix in ['-attempt.json','-guardian.jsonl','-stdout.log','-stderr.log','-supervision.json','-terminal-error.json']}
    if any((resultdir/n).exists() for n in stage_names) or any((private/(args.stage+'-'+stream+'.raw')).exists() for stream in ['stdout','stderr']):raise RuntimeError('Stage allocation already used or output preexists')
    if args.stage=='kernel' and (any(resultdir.iterdir()) or any(private.iterdir())):raise RuntimeError('Kernel requires empty result and private-log directories')
    identity_check()
    dump(resultdir/(args.stage+'-attempt.json'),{'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(mb),'allocation':'sole attempt; existence prevents retry','startedUtc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    output=resultdir/(index_name if args.stage=='kernel' else 'independent-check.json')
    env['RESEARCH_SOURCE_MANIFEST_PATH']=str(mp)
    if args.stage=='kernel':
        command=[str(runtime_paths['node']),str(package/'source/run.cjs')];env['RESEARCH_RESULT_PATH']=str(output);template=['NODE','PACKAGE/source/run.cjs']
    else:
        command=[str(runtime_paths['python']),str(package/'source/check.py'),'--spec',str(package/'source/spec.json'),'--input',str(resultdir/index_name),'--manifest',str(mp),'--output',str(output),'--root',str(root)]
        template=['PYTHON','PACKAGE/source/check.py','--spec','PACKAGE/source/spec.json','--input','PACKAGE/results/timing-index.json','--manifest','PACKAGE/source-manifest.json','--output','PACKAGE/results/independent-check.json','--root','REPOSITORY_ROOT']
    events=resultdir/(args.stage+'-guardian.jsonl');env['RESEARCH_CHILD_COMMAND']=json.dumps(command);env['RESEARCH_GUARD_EVENTS']=str(events)
    env['RESEARCH_SUPERVISION_STAGE']=args.stage
    stdout=private/(args.stage+'-stdout.raw');stderr=private/(args.stage+'-stderr.raw')
    report={'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(mb),'commandTemplate':template,'runtimePins':runtimes,'wallLimitSeconds':wall_limit,'guardianWallLimitSeconds':GUARDIAN_LIMITS[args.stage],'sampledRssLimitBytes':RSS_LIMIT,'outputLimitBytes':AGGREGATE_LIMIT,'artifactLimitBytes':{'timing-index.json':INDEX_LIMIT,'timing-index.json.jsonl':JOURNAL_LIMIT,'eachScientificOrAnomalyShard':SHARD_LIMIT,'allScientificAndAnomalyShards':SCIENTIFIC_TOTAL_LIMIT,'allCheckerOutputs':CHECKER_TOTAL_LIMIT},'logMetadataLimitBytes':LOG_METADATA_LIMIT,'finalReportLimitBytes':REPORT_LIMIT,'nominalSleepSeconds':0.05,'success':False,'closed':False,'samples':0,'peakSampledGroupRssBytes':0,'maxSampleGapSeconds':0,'terminationReason':None,'containmentScope':'Reviewed scientific children spawn no subprocesses. Retained guardian owns process group; sampling is not hostile-code/escaped-descendant isolation.','accountingScope':'Recursive closed-set results plus all four kernel/checker private raw logs and their public copies. Each scene or optional first-mismatch shard has a 128 MiB cap and all such shards share 384 MiB; checker main and references share 128 MiB; index and journal each have an 8 MiB cap; logs/metadata including private raw and public copies share 16 MiB; each supervision report has a 64 KiB cap; aggregate cap is 768 MiB.'}
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
    known_reasons={'wall-limit','rss-limit','output-limit','artifact-output-limit','scientific-output-limit','checker-output-limit','log-metadata-limit','final-report-budget','unexpected-output-file','unexpected-output-directory','unexpected-private-log','unexpected-anomaly-count','output-accounting-failure','unexpected-descendant','escaped-descendant-observed','guardian-failure','guardian-exited-before-release','residual-group-member'}
    try:
        with stdout.open('xb') as out,stderr.open('xb') as err:
            guardian=subprocess.Popen([str(runtime_paths['python']),str(package/'source/guardian.py')],cwd=root,env=env,stdout=out,stderr=err,stdin=subprocess.PIPE,text=True,start_new_session=True)
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
            dest=resultdir/(p.stem+'.log')
            with dest.open('x') as f:f.write(text);f.flush();os.fsync(f.fileno())
            sync_directory(resultdir)
            logs.append({'path':str(dest.relative_to(root)),'rawBytes':len(raw),'rawSha256':sha(raw),'publishedBytes':dest.stat().st_size,'publishedSha256':sha(dest.read_bytes()),'redaction':'machine/runtime path prefixes replaced; raw logs retained privately'})
        report['logs']=logs
        for name,p in [('output',output),('journal',Path(str(output)+'.jsonl'))]:
            if p.exists():report[name]=pin(p,root)
        report['scientificEvidence']=[pin(resultdir/n,root) for n in sorted(scientific_names|anomaly_names) if (resultdir/n).is_file() and not (resultdir/n).is_symlink()]
        report['anomalyEvidence']=[pin(resultdir/n,root) for n in sorted(anomaly_names) if (resultdir/n).is_file() and not (resultdir/n).is_symlink()]
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
        expected_stage=scientific_names if args.stage=='kernel' else checker_names
        if not all((resultdir/n).is_file() and not (resultdir/n).is_symlink() for n in expected_stage):
            if report['terminationReason'] is None:report['terminationReason']='incomplete-stage-evidence'
        if report['anomalyEvidence'] and report['terminationReason'] is None:report['terminationReason']='scientific-anomaly'
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
