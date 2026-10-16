"""Single bounded invocation; failure and partial artifacts are retained."""
import datetime, hashlib, json, pathlib, subprocess, sys, time
if sys.flags.optimize:
    raise RuntimeError('Provenance checks require nonoptimized Python.')
p=pathlib.Path(__file__).resolve().parent.parent
root=p.parent.parent
manifest=p/'source-manifest.json'
assert len(sys.argv)==4, 'Supply Python executable, independently verified manifest SHA256, and published commit.'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==sys.argv[2]
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert commit==sys.argv[3]
assert subprocess.check_output(['git','show',commit+':'+str(manifest.relative_to(root))],cwd=root)==manifest.read_bytes()
m=json.loads(manifest.read_text())
for f in m['files']:
    b=(p/f['path']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
    assert subprocess.check_output(['git','show',commit+':'+str((p/f['path']).relative_to(root))],cwd=root)==b
out=p/'results'; out.mkdir(exist_ok=True)
with (out/'review-invocation.lock').open('x') as f: f.write('One invocation consumed. Do not remove.\n')
record={'source_commit':commit, 'source_manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_cap_seconds':240,'command':'python3 source/independent-check.py PACKAGE_PATH results/independent-review.json','returncode':None}
t=time.monotonic()
try:
    with (out/'review-stdout.txt').open('xb') as stdout,(out/'review-stderr.txt').open('xb') as stderr:
        r=subprocess.run([sys.argv[1],str(p/'source/independent-check.py'),str(p),str(out/'independent-review.json')],stdout=stdout,stderr=stderr,timeout=240)
        record['returncode']=r.returncode
except subprocess.TimeoutExpired: record['timeout']=True
except BaseException as exc: record['exception_class']=type(exc).__name__
finally:
    record['supervisor_elapsed_seconds']=time.monotonic()-t
    record['performance_measurement']=False
    record['artifacts']=[{'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(out.iterdir()) if f.is_file()]
    (out/'review-run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
sys.exit(0 if record['returncode']==0 else 1)
