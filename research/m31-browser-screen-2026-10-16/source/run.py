"""Frozen serial stage supervisor; retained owned group and full-tree RSS.

Process snapshots are sampled, not a cgroup or a peak-memory guarantee. Private
PIDs, command paths and profiles stay in a temporary supervisor directory.
"""
from pathlib import Path
import datetime, hashlib, importlib.metadata, json, os, platform, re, signal, subprocess, sys, tempfile, time
p=Path(__file__).resolve().parent.parent;repo=p.parent.parent
if len(sys.argv)!=5:raise RuntimeError('kind executable source_sha source_commit')
kind,executable,source_sha,commit=sys.argv[1:]
if kind not in ('generation','candidate','review'):raise RuntimeError('unknown-stage')
out=p/'results';out.mkdir(exist_ok=True)
with (out/(kind+'-invocation.lock')).open('x') as f:f.write('Sole frozen stage consumed. Never repeat.\n')
start=time.monotonic();cfg=json.loads((p/'config.json').read_text());limits=cfg['limits'];cap=limits[kind+'WallSeconds']
rec=dict(kind=kind,sourceCommit=commit,sourceManifestSha256=source_sha,startedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),wallCapSeconds=cap,rssCapBytes=limits['rssBytes'] if kind!='candidate' else None,controllerRSSCapBytes=limits['controllerRSSBytes'] if kind=='candidate' else None,browserTreeRSSCapBytes=limits['browserTreeRSSBytes'] if kind=='candidate' else None,sampleIntervalSeconds=.1,rssSamples=0,sampledPeakRSSBytes=0,browserTreePeakRSSBytes=0,controllerPeakRSSBytes=0,signals=[],monitorErrors=[],exitRaces=[],closed=False,childGroupAbsent=False,ownedGroupAbsent=False,returncode=None,runtimeIdentityVerified=False,phaseClosures=[],containment='retained-session-leader; Chrome detached=false; group plus observed descendants; sampled RSS sum')
proc=None;pins=[];protected={};private=Path(tempfile.mkdtemp(prefix='m31-browser-screen-'+kind+'-'));known={};slot_stats={};barrier_samples={};slot_started={};stage_initial_bytes=0
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(f):
    h=hashlib.sha256()
    with f.open('rb') as s:
        for b in iter(lambda:s.read(1048576),b''):h.update(b)
    return h.hexdigest()
def pin(f):return dict(path=str(f.relative_to(p)),bytes=f.stat().st_size,sha256=digest(f))
def files():return sorted(f for d in ['results','inputs','generation','runs'] for f in (p/d).rglob('*') if f.is_file())
def snapshot():
    raw=subprocess.check_output(['/bin/ps','-axo','pid=,ppid=,pgid=,rss=,lstart='],text=True,timeout=3)
    table={}
    for line in raw.splitlines():
        a=line.split(None,4)
        if len(a)==5:table[int(a[0])]=dict(ppid=int(a[1]),pgid=int(a[2]),rss=int(a[3])*1024,start=a[4])
    return table
def owned(table):
    ids={i for i,r in table.items() if r['pgid']==proc.pid}
    ids|={i for i,s in known.items() if i in table and table[i]['start']==s}
    while True:
        more={i for i,r in table.items() if r['ppid'] in ids}
        if more<=ids:break
        ids|=more
    for i in ids:known[i]=table[i]['start']
    return ids
def group_absent():
    try:os.killpg(proc.pid,0);return False
    except ProcessLookupError:return True
def storage_guard():
    listing=files();total=0;logs=0
    for f in listing:
        try:size=f.stat().st_size
        except FileNotFoundError:
            if f.name.endswith('.partial'):continue
            raise
        total+=size
        if f.name.endswith(('-stdout.txt','-stderr.txt')):logs+=size
    check(total<=limits['scientificDirectoryBytes']-limits['administrativeReserveBytes'],'storage-reserve-cap');check(logs<=limits['supervisorLogsBytes'],'log-cap')
    if kind=='review':check(total-stage_initial_bytes<=limits['reviewBytes'],'review-output-cap')
    if kind=='generation':
        generation_total=0
        for f in listing:
            if f.parts[-2] in ('inputs','generation') or (f.parent==out and f.name.startswith('generation-') and not f.name.endswith(('-stdout.txt','-stderr.txt','-run.json'))):generation_total+=f.stat().st_size
        check(generation_total<=limits['generationBytes'],'generation-output-cap')
    return total,logs
def identity(f,x):return f.stat().st_size==x['bytes'] and digest(f)==x['sha256']
def exclusive_json(f,obj):
    with f.open('x') as h:json.dump(obj,h,allow_nan=False)
try:
    check(sys.flags.optimize==0 and not os.environ.get('NODE_OPTIONS'),'runtime-flags')
    manifest=p/'source-manifest.json';check(digest(manifest)==source_sha,'source-manifest-sha')
    check(subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True,timeout=5).strip()==commit,'source-head')
    pins=json.loads(manifest.read_text())['files']
    for x in pins+[dict(path=str(manifest.relative_to(repo)),bytes=manifest.stat().st_size,sha256=source_sha)]:
        f=repo/x['path'];check(identity(f,x),'local-source-pin');check(subprocess.check_output(['git','show',commit+':'+x['path']],cwd=repo,timeout=10)==f.read_bytes(),'committed-source-pin')
    receipt=json.loads((p/'source-publication.json').read_text());rec['sourceReceiptSha256']=digest(p/'source-publication.json')
    check(receipt['commit']==commit and receipt['manifestSha256']==source_sha and receipt['remoteManifestMatchesLocal'] is True and receipt['localAndCommittedPinsMatch'] is True,'publication-receipt')
    r=json.loads((p/'runtime.json').read_text());check(sys.platform==r['platform'] and platform.machine()==r['architecture'],'platform')
    check(identity(Path(sys.executable).resolve(),r['python']) and sys.version==r['python']['version'],'supervisor-runtime')
    dist=importlib.metadata.distribution('numpy');check(dist.version==r['numpy']['version'] and hashlib.sha256(dist.read_text('RECORD').encode()).hexdigest()==r['numpy']['distributionRecordSha256'],'numpy-identity')
    check(identity(Path(executable).resolve(),r['python'] if kind=='review' else r['node']),'child-runtime')
    if kind=='candidate':
        for x in r['chrome']['files']:check(identity(Path('/Applications/Google Chrome.app/Contents')/x['appRelativePath'],x),'chrome-component-identity')
    rec['runtimeIdentityVerified']=True;rec['runtime']=r
    dependencies=[] if kind=='generation' else ['generation'] if kind=='candidate' else ['generation','candidate']
    for dep in dependencies:
        q=json.loads((out/(dep+'-run.json')).read_text());check(q['closed'] and q['childGroupAbsent'],'predecessor-not-closed')
        if kind=='candidate':check(q['supervisorSuccess'],'generation-failed')
        rec[dep+'SupervisorSuccess']=q['supervisorSuccess']
    protected={str(f.relative_to(p)):digest(f) for f in files() if f.name!=kind+'-invocation.lock'}
    stage_initial_bytes=sum(f.stat().st_size for f in files())
    script={'generation':'generate.cjs','candidate':'controller.cjs','review':'review.py'}[kind]
    command=[executable,str(p/'source'/script),str(p)]
    if kind=='review':command.append(str(out/'independent-review.json'))
    env={**os.environ,'RESEARCH_SUPERVISOR_DIR':str(private)}
    with (out/(kind+'-stdout.txt')).open('xb') as stdout,(out/(kind+'-stderr.txt')).open('xb') as stderr:
        proc=subprocess.Popen([sys.executable,str(p/'source/group-runner.py'),*command],stdin=subprocess.PIPE,stdout=stdout,stderr=stderr,start_new_session=True,env=env)
        while True:
            check(time.monotonic()-start<=cap,'wall-cap');check(proc.poll() is None,'guardian-exited-early')
            table=snapshot();ids=owned(table);check(proc.pid in ids,'guardian-missing');check(all(table[i]['pgid']==proc.pid for i in ids),'owned-group-escape')
            child_file=private/'child.json';child_id=json.loads(child_file.read_text())['pid'] if child_file.exists() else None
            total=sum(table[i]['rss'] for i in ids);rec['rssSamples']+=1;rec['sampledPeakRSSBytes']=max(rec['sampledPeakRSSBytes'],total)
            controller=table.get(child_id,{}).get('rss',0);others=ids-{proc.pid,child_id};browser_rss=sum(table[i]['rss'] for i in others)
            rec['controllerPeakRSSBytes']=max(rec['controllerPeakRSSBytes'],controller);rec['browserTreePeakRSSBytes']=max(rec['browserTreePeakRSSBytes'],browser_rss)
            if kind=='candidate':
                check(controller<=limits['controllerRSSBytes'],'controller-rss-cap');check(browser_rss<=limits['browserTreeRSSBytes'],'browser-tree-rss-cap')
                active=private/'active-slot.json'
                if active.exists():
                    slot=json.loads(active.read_text())['processId'];slot_started.setdefault(slot,time.monotonic())
                    if not (private/('barrier-'+slot+'-ack.json')).exists():check(time.monotonic()-slot_started[slot]<=900,'external-browser-slot-wall-cap')
                    s=slot_stats.setdefault(slot,dict(samples=0,peakBrowserRSSBytes=0,peakControllerRSSBytes=0,observedBrowserProcesses=set()))
                    s['samples']+=1;s['peakBrowserRSSBytes']=max(s['peakBrowserRSSBytes'],browser_rss);s['peakControllerRSSBytes']=max(s['peakControllerRSSBytes'],controller);s['observedBrowserProcesses']|=others
                for slot in cfg['processes']:
                    request=private/('barrier-'+slot+'.json');ack=private/('barrier-'+slot+'-ack.json')
                    if request.exists() and not ack.exists():
                        barrier_samples[slot]=barrier_samples.get(slot,0)+1 if not others else 0
                        if barrier_samples[slot]>=2:
                            s=slot_stats.get(slot,{})
                            observation=dict(processId=slot,allOwnedBrowserProcessesAbsent=True,monitorHealthy=True,consecutiveEmptySamples=barrier_samples[slot],samples=s.get('samples',0),peakBrowserRSSBytes=s.get('peakBrowserRSSBytes',0),peakControllerRSSBytes=s.get('peakControllerRSSBytes',0),observedBrowserProcessCount=len(s.get('observedBrowserProcesses',set())))
                            tmp=ack.with_suffix('.tmp');exclusive_json(tmp,observation);tmp.rename(ack)
            else:check(total<=limits['rssBytes'],'stage-rss-cap')
            storage_guard()
            if (private/'exit.json').exists():
                rec['returncode']=json.loads((private/'exit.json').read_text())['returncode']
                final_table=snapshot();final_ids=owned(final_table);check(final_ids=={proc.pid},'residual-owned-processes-after-child')
                proc.stdin.write(b'R');proc.stdin.flush();proc.stdin.close();check(proc.wait(timeout=5)==0,'guardian-release-exit');break
            time.sleep(.1)
except BaseException as exc:
    rec['exception']=dict(type=type(exc).__name__,reason=str(exc) if type(exc) is RuntimeError else 'details-withheld')
finally:
    if proc is None:rec['childGroupAbsent']=True;rec['ownedGroupAbsent']=True
    else:
        try:
            if proc.poll() is None:
                os.killpg(proc.pid,signal.SIGKILL);rec['signals'].append('SIGKILL-owned-retained-group');proc.wait(timeout=5)
            # Known descendants may have escaped the original group. Signal only after
            # a fresh matching process-start identity check; retain failure status.
            escaped=snapshot()
            for pid,identity_start in known.items():
                if pid in escaped and escaped[pid]['start']==identity_start and escaped[pid]['pgid']!=proc.pid:
                    current=snapshot().get(pid)
                    if current and current['start']==identity_start:
                        try:os.kill(pid,signal.SIGKILL);rec['signals'].append('SIGKILL-observed-escaped-descendant')
                        except ProcessLookupError:rec['exitRaces'].append('escaped-descendant-exited')
            for _ in range(30):
                current=snapshot()
                remaining=[i for i,st in known.items() if i in current and current[i]['start']==st]
                if group_absent() and not remaining:break
                time.sleep(.1)
            rec['childGroupAbsent']=group_absent()
            live=snapshot();surviving=[i for i,s in known.items() if i in live and live[i]['start']==s]
            rec['ownedGroupAbsent']=not surviving
            rec['survivingOwnedProcessCount']=len(surviving)
        except BaseException as exc:rec['cleanupError']=type(exc).__name__
    rec['closed']=proc is None or (rec['childGroupAbsent'] and rec['ownedGroupAbsent'] and proc.returncode is not None)
    try:
        rec['protectedInputsUnchanged']=all((repo/x['path']).is_file() and identity(repo/x['path'],x) for x in pins)
        rec['candidateOutputsUnchanged']=all((p/name).is_file() and digest(p/name)==h for name,h in protected.items())
        rec['protectedInputsUnchanged'] &= rec['candidateOutputsUnchanged'] and digest(p/'source-publication.json')==rec.get('sourceReceiptSha256')
        rec['phaseClosures']=[pin(p/'runs'/slot/'closure.json') for slot in cfg['processes'] if (p/'runs'/slot/'closure.json').is_file()]
        rec['scientificBytesBeforeClosure'],rec['logBytes']=storage_guard()
        rec['artifacts']=[pin(f) for f in files() if f.name!=kind+'-run.json']
    except BaseException as exc:rec['finalizationError']=type(exc).__name__
    rec['elapsedSeconds']=time.monotonic()-start
    rec['supervisorSuccess']=bool(rec['closed'] and rec['returncode']==0 and rec['runtimeIdentityVerified'] and rec.get('protectedInputsUnchanged') and rec.get('candidateOutputsUnchanged') and rec['rssSamples']>0 and not rec['signals'] and not rec['monitorErrors'] and not any(k in rec for k in ['exception','cleanupError','finalizationError']) and rec['elapsedSeconds']<=cap)
    if rec['elapsedSeconds']>cap:rec['finalWallCapExceeded']=True
    while True:
        rec['elapsedSeconds']=time.monotonic()-start
        if rec['elapsedSeconds']>cap:rec['finalWallCapExceeded']=True;rec['supervisorSuccess']=False
        payload=(json.dumps(rec,indent=2,allow_nan=False)+'\n').encode();total=sum(f.stat().st_size for f in files())
        fits=len(payload)<=limits['administrativeReserveBytes']//3 and total+len(payload)<=limits['scientificDirectoryBytes']
        if fits or rec.get('finalStorageCapExceeded'):break
        rec['finalStorageCapExceeded']=True;rec['supervisorSuccess']=False
    with (out/(kind+'-run.json')).open('xb') as f:f.write(payload)
print(json.dumps({k:rec.get(k) for k in ['kind','closed','supervisorSuccess','returncode','elapsedSeconds','sampledPeakRSSBytes','browserTreePeakRSSBytes','controllerPeakRSSBytes','exception','cleanupError','finalizationError']}))
sys.exit(0 if rec['supervisorSuccess'] else 1)
