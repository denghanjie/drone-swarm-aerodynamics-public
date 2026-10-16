"""One-shot bounded scientific child supervision with retained group ownership."""
import argparse,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):
    with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def pin(p,root):return {'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['kernel','checker']);args=parser.parse_args()
    package=Path(__file__).resolve().parents[1];root=package.parents[1]
    mp=package/'source-manifest.json';mb=mp.read_bytes();manifest=json.loads(mb)
    pubpath=package/'source-publication.json';pubbytes=pubpath.read_bytes();publication=json.loads(pubbytes)
    if publication.get('remoteBytesEqualLocal') is not True or publication.get('manifestSha256')!=sha(mb):raise RuntimeError('Source publication gate failed')
    runtimes=json.loads((package/'runtime-pins.json').read_text());env=os.environ.copy()
    runtime_paths={'node':Path(env['RESEARCH_NODE']).resolve(),'python':Path(sys.executable).resolve()};prior_pins=[]
    required=['PROTOCOL.md','MODEL.md','runtime-pins.json','source/interval.cjs','source/rational.cjs','source/adapter.cjs','source/pair.cjs','source/run.cjs','source/check.py','source/spec.json','source/result-contract.json','source/guardian.py','source/supervise.py']
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
    identity_check()
    resultdir=package/'results';resultdir.mkdir(exist_ok=True)
    if args.stage=='checker':
        if (resultdir/'kernel-terminal-error.json').exists():raise RuntimeError('Kernel finalization failed')
        prev=json.loads((resultdir/'kernel-supervision.json').read_text())
        if not prev.get('success') or not prev.get('closed') or prev.get('sourceCommit')!=publication['commit'] or prev.get('sourceManifestSha256')!=sha(mb):raise RuntimeError('Kernel not qualified for saved checker')
        for name in ['output','journal']:
            x=prev[name]
            if pin(root/x['path'],root)!=x:raise RuntimeError('Kernel saved evidence changed')
            prior_pins.append(x)
        prior_pins.append(pin(resultdir/'kernel-supervision.json',root))
    private=Path(env['RESEARCH_PRIVATE_RUN_DIR']);private.mkdir(parents=True,exist_ok=True)
    dump(resultdir/(args.stage+'-attempt.json'),{'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(mb),'allocation':'sole attempt; existence prevents retry','startedUtc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    output=resultdir/('pair-results.json' if args.stage=='kernel' else 'independent-check.json')
    if args.stage=='kernel':
        command=[str(runtime_paths['node']),str(package/'source/run.cjs')];env['RESEARCH_RESULT_PATH']=str(output);template=['NODE','PACKAGE/source/run.cjs']
    else:
        command=[str(runtime_paths['python']),str(package/'source/check.py'),'--spec',str(package/'source/spec.json'),'--input',str(resultdir/'pair-results.json'),'--manifest',str(mp),'--output',str(output),'--root',str(root)]
        template=['PYTHON','PACKAGE/source/check.py','--spec','PACKAGE/source/spec.json','--input','PACKAGE/results/pair-results.json','--manifest','PACKAGE/source-manifest.json','--output','PACKAGE/results/independent-check.json','--root','REPOSITORY_ROOT']
    events=resultdir/(args.stage+'-guardian.jsonl');env['RESEARCH_CHILD_COMMAND']=json.dumps(command);env['RESEARCH_GUARD_EVENTS']=str(events)
    stdout=private/(args.stage+'-stdout.raw');stderr=private/(args.stage+'-stderr.raw')
    report={'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(mb),'commandTemplate':template,'runtimePins':runtimes,'wallLimitSeconds':120,'sampledRssLimitBytes':1073741824,'outputLimitBytes':16777216,'nominalSleepSeconds':0.05,'success':False,'closed':False,'samples':0,'peakSampledGroupRssBytes':0,'maxSampleGapSeconds':0,'terminationReason':None,'containmentScope':'Reviewed children spawn no subprocesses. Retained guardian owns process group; sampling is not hostile-code/escaped-descendant isolation.'}
    started=time.monotonic();last=started;guardian=None;child_exit=None;child_pid=None
    def output_bytes():return sum(p.stat().st_size for p in [stdout,stderr] if p.exists())+sum(p.stat().st_size for p in resultdir.iterdir() if p.is_file())
    def sample():
        nonlocal last
        now=time.monotonic();report['maxSampleGapSeconds']=max(report['maxSampleGapSeconds'],now-last);last=now
        table=subprocess.run(['ps','-axo','pid=,ppid=,pgid=,rss='],capture_output=True,text=True,timeout=2,check=True).stdout
        allrows=[tuple(map(int,l.split())) for l in table.splitlines() if len(l.split())==4]
        rows=[r for r in allrows if r[2]==guardian.pid];rss=sum(r[3]*1024 for r in rows)
        report['samples']+=1;report['peakSampledGroupRssBytes']=max(report['peakSampledGroupRssBytes'],rss)
        if rss>1073741824:raise RuntimeError('rss-limit')
        if len(rows)>2 or any(r[0]!=guardian.pid and r[1]!=guardian.pid for r in rows):raise RuntimeError('unexpected-descendant')
        if any(r[1] in {guardian.pid,child_pid} and r[2]!=guardian.pid for r in allrows):raise RuntimeError('escaped-descendant-observed')
        return rows
    try:
        with stdout.open('xb') as out,stderr.open('xb') as err:
            guardian=subprocess.Popen([str(runtime_paths['python']),str(package/'source/guardian.py')],cwd=root,env=env,stdout=out,stderr=err,stdin=subprocess.PIPE,text=True,start_new_session=True)
            report['processGroup']=guardian.pid
            while True:
                if time.monotonic()-started>120:raise RuntimeError('wall-limit')
                if output_bytes()>16777216:raise RuntimeError('output-limit')
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
    except Exception as e:report['terminationReason']=str(e) if str(e) in {'wall-limit','rss-limit','output-limit','unexpected-descendant','escaped-descendant-observed','guardian-failure','guardian-exited-before-release','residual-group-member'} else 'supervisor-'+type(e).__name__
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
            dest=resultdir/(p.stem+'.log');dest.write_text(text)
            logs.append({'path':str(dest.relative_to(root)),'rawBytes':len(raw),'rawSha256':sha(raw),'publishedBytes':dest.stat().st_size,'publishedSha256':sha(dest.read_bytes()),'redaction':'machine/runtime path prefixes replaced; raw logs retained privately'})
        report['logs']=logs
        for name,p in [('output',output),('journal',Path(str(output)+'.jsonl'))]:
            if p.exists():report[name]=pin(p,root)
        try:identity_check();report['sourceAndRuntimeRechecked']=True
        except Exception:report['sourceAndRuntimeRechecked']=False;report['terminationReason']='postrun-identity-failure'
        report['wallSeconds']=time.monotonic()-started;report['finalOutputBytesBeforeReport']=output_bytes()
        if report['wallSeconds']>120:report['terminationReason']='wall-limit'
        if report['finalOutputBytesBeforeReport']+65536>16777216:report['terminationReason']='output-limit'
        report['success']=report.get('exitCode')==0 and report.get('guardianExitCode')==0 and report['terminationReason'] is None and report['closed'] and output.exists()
        if len((json.dumps(report,indent=2)+'\n').encode())>65536:raise RuntimeError('final-report-budget')
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
