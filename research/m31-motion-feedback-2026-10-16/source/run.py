"""One consumed allocation for each frozen candidate/review; no retries."""
import datetime, hashlib, json, os, pathlib, signal, subprocess, sys, time
if sys.flags.optimize: raise RuntimeError('Nonoptimized Python required')
p=pathlib.Path(__file__).resolve().parent.parent
root=p.parent.parent
assert len(sys.argv)==5, 'kind executable verified_manifest_sha published_commit'
kind,executable,verified_sha,published_commit=sys.argv[1:]
assert kind in ('candidate','review')
if kind=='candidate':assert not os.environ.get('NODE_OPTIONS'), 'NODE_OPTIONS must be empty'
manifest=p/'source-manifest.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==verified_sha
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert commit==published_commit
assert subprocess.check_output(['git','show',commit+':'+str(manifest.relative_to(root))],cwd=root)==manifest.read_bytes()
for f in json.loads(manifest.read_text())['files']:
    b=(root/f['path']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
    assert subprocess.check_output(['git','show',commit+':'+f['path']],cwd=root)==b
out=p/'results';out.mkdir(exist_ok=True)
def scientific_files():
    return sorted(x for name in ('results','inputs','generation') for x in (p/name).rglob('*') if x.is_file())

with (out/(kind+'-invocation.lock')).open('x') as f:f.write('One invocation consumed. Do not remove.\n')
cap=300 if kind=='candidate' else 120
cmd=[executable,str(p/'source/experiment.cjs'),str(p)] if kind=='candidate' else [executable,str(p/'source/review.py'),str(p),str(out/'independent-review.json')]
record={'source_commit':commit,'source_manifest_sha256':verified_sha,'kind':kind,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_cap_seconds':cap,'rss_cap_bytes':805306368,'returncode':None,'command':'node source/experiment.cjs PACKAGE_PATH' if kind=='candidate' else 'python3 source/review.py PACKAGE_PATH results/independent-review.json','performance_measurement':False,'externalSampledPeakRSSKiB':0,'sampleIntervalSeconds':0.2,'rssSamples':0,'rssSampleErrors':0,'last_phase':'prelaunch','monitorErrors':[],'monitorExitRaces':[],'executionContext':'approved-host-new-motion-feedback'}
t=time.monotonic();proc=None
try:
    with (out/(kind+'-stdout.txt')).open('xb') as stdout,(out/(kind+'-stderr.txt')).open('xb') as stderr:
        record['last_phase']='before-child-popen'
        proc=subprocess.Popen(cmd,stdout=stdout,stderr=stderr,start_new_session=True)
        record['last_phase']='child-popen-returned'
        while proc.poll() is None:
            elapsed=time.monotonic()-t
            try:
                record['last_phase']='before-monitor-ps'
                rss=int(subprocess.check_output(['/bin/ps','-o','rss=','-p',str(proc.pid)],text=True,stderr=subprocess.DEVNULL,timeout=2).strip() or 0)
                if rss<=0:raise ValueError('Nonpositive RSS sample')
                record['externalSampledPeakRSSKiB']=max(record['externalSampledPeakRSSKiB'],rss)
                record['rssSamples']+=1
                record['last_phase']='monitor-ps-returned'
            except (ValueError,subprocess.SubprocessError,OSError) as exc:
                if proc.poll() is not None:
                    record['monitorExitRaces'].append({'phase':record['last_phase'],'exception_class':type(exc).__name__,'errno':getattr(exc,'errno',None)})
                    record['last_phase']='monitor-after-child-exit'
                    break
                rss=None;record['rssSampleErrors']+=1
                record['monitorErrors'].append({'phase':record['last_phase'],'exception_class':type(exc).__name__,'errno':getattr(exc,'errno',None)})
            cause=None
            if rss is None:cause='RSS monitor unavailable'
            elif elapsed>cap:cause='wall cap'
            elif rss*1024>record['rss_cap_bytes']:cause='RSS cap'
            elif stdout.tell()+stderr.tell()>4*1024**2:cause='log cap'
            elif sum(x.stat().st_size for x in scientific_files())>32*1024**2:cause='aggregate scientific directory cap'
            if cause:
                record['terminated_for']=cause;record['last_phase']='before-cap-termination';os.killpg(proc.pid,signal.SIGKILL);break
            time.sleep(.2)
        record['last_phase']='before-child-wait'
        record['returncode']=proc.wait(timeout=5)
        record['last_phase']='child-wait-returned'
except BaseException as exc:
    record['exception_class']=type(exc).__name__
    record['exception_errno']=getattr(exc,'errno',None)
    record['exception_phase']=record['last_phase']
    if proc is not None:
        try:
            if proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL)
            record['returncode']=proc.wait(timeout=5)
            record['cleanup_returncode']=record['returncode']
        except BaseException as cleanup:
            record['cleanup_exception_class']=type(cleanup).__name__
            record['cleanup_exception_errno']=getattr(cleanup,'errno',None)
finally:
    record['supervisor_elapsed_seconds']=time.monotonic()-t
    if record['rssSamples']==0:record['externalSampledPeakRSSKiB']=None
    # A final write or fast exit must not bypass the fixed storage limits.
    record['finalScientificDirectoryBytes']=sum(x.stat().st_size for x in scientific_files())
    record['finalSupervisorLogBytes']=sum(x.stat().st_size for x in out.iterdir() if x.is_file() and x.name.endswith(('-stdout.txt','-stderr.txt')))
    if record['finalScientificDirectoryBytes']>32*1024**2:record['terminated_for']='final aggregate scientific directory cap'
    if record['finalSupervisorLogBytes']>4*1024**2:record['terminated_for']='final aggregate supervisor log cap'
    if record['supervisor_elapsed_seconds']>cap:record['terminated_for']='final wall cap'
    record['supervisor_success']=record['returncode']==0 and not any(record.get(k) for k in ('exception_class','terminated_for','cleanup_exception_class','monitorErrors'))
    record['artifacts']=[{'path':str(x.relative_to(p)),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in scientific_files()]
    encoded=(json.dumps(record,indent=2)+'\n').encode('utf-8')
    if record['finalScientificDirectoryBytes']+len(encoded)>32*1024**2:
        record['terminated_for']='final supervisor-record aggregate cap'
        record['supervisor_success']=False
        encoded=(json.dumps(record,indent=2)+'\n').encode('utf-8')
    with (out/(kind+'-run.json')).open('xb') as f:f.write(encoded)
print(json.dumps({k:v for k,v in record.items() if k!='artifacts'}))
sys.exit(0 if record['supervisor_success'] else 1)
