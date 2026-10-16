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
with (out/(kind+'-invocation.lock')).open('x') as f:f.write('One invocation consumed. Do not remove.\n')
cap=300 if kind=='candidate' else 60
cmd=[executable,str(p/'source/experiment.cjs'),str(p)] if kind=='candidate' else [executable,str(p/'source/review.py'),str(p),str(out/'independent-review.json')]
record={'source_commit':commit,'source_manifest_sha256':verified_sha,'kind':kind,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_cap_seconds':cap,'rss_cap_bytes':1610612736,'returncode':None,'command':'node source/experiment.cjs PACKAGE_PATH' if kind=='candidate' else 'python3 source/review.py PACKAGE_PATH results/independent-review.json','performance_measurement':False,'externalSampledPeakRSSKiB':0,'sampleIntervalSeconds':0.2,'rssSamples':0,'rssSampleErrors':0}
t=time.monotonic();proc=None
try:
    with (out/(kind+'-stdout.txt')).open('xb') as stdout,(out/(kind+'-stderr.txt')).open('xb') as stderr:
        proc=subprocess.Popen(cmd,stdout=stdout,stderr=stderr,start_new_session=True)
        while proc.poll() is None:
            elapsed=time.monotonic()-t
            try:
                rss=int(subprocess.check_output(['/bin/ps','-o','rss=','-p',str(proc.pid)],text=True,stderr=subprocess.DEVNULL,timeout=2).strip() or 0)
                record['externalSampledPeakRSSKiB']=max(record['externalSampledPeakRSSKiB'],rss)
                record['rssSamples']+=1
            except (ValueError,subprocess.SubprocessError):
                rss=0;record['rssSampleErrors']+=1
            cause=None
            if elapsed>cap:cause='wall cap'
            elif rss*1024>record['rss_cap_bytes']:cause='RSS cap'
            elif stdout.tell()+stderr.tell()>4*1024**2:cause='log cap'
            elif sum(x.stat().st_size for x in out.iterdir() if x.is_file())>132*1024**2:cause='total result cap'
            if cause:
                record['terminated_for']=cause;os.killpg(proc.pid,signal.SIGKILL);break
            time.sleep(.2)
        record['returncode']=proc.wait(timeout=5)
except BaseException as exc:
    record['exception_class']=type(exc).__name__
    if proc is not None and proc.poll() is None:
        os.killpg(proc.pid,signal.SIGKILL);proc.wait()
finally:
    record['supervisor_elapsed_seconds']=time.monotonic()-t
    if record['rssSamples']==0:record['externalSampledPeakRSSKiB']=None
    record['artifacts']=[{'path':str(x.relative_to(p)),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(out.iterdir()) if x.is_file()]
    (out/(kind+'-run.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='artifacts'}))
sys.exit(0 if record['returncode']==0 else 1)
