"""One bounded saved-word export. No producer/reference execution."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,time
p=Path(__file__).resolve().parent;start=time.monotonic();need=lambda x: x or (_ for _ in ()).throw(ValueError('export-preflight'))
need(datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat('2026-10-17T07:14:28+00:00'))
need(not(p/'EXPORT-STARTED.json').exists() and not(p/'data').exists())
r=json.loads((p.parent/'runtime.json').read_bytes())['python'];b=Path(sys.executable).resolve().read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'])
source=(p/'export-saved.py').read_bytes();marker={'scientificCalls':0,'budgetSeconds':60,'startedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exporterSha256':hashlib.sha256(source).hexdigest()}
with(p/'EXPORT-STARTED.json').open('x') as f:json.dump(marker,f,indent=2);f.write('\n')
child=subprocess.Popen([sys.executable,'-I','-B',str(p/'export-saved.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:out,err=child.communicate(timeout=max(.1,60-(time.monotonic()-start)));status='completed' if child.returncode==0 else 'failed'
except subprocess.TimeoutExpired:child.kill();out,err=child.communicate();status='timeout'
need((p/'export-saved.py').read_bytes()==source)
result={'status':status,'exitCode':child.returncode,'wallSeconds':time.monotonic()-start,'scientificCalls':0,'stdoutBytes':len(out),'stderrBytes':len(err),'stderrSha256':hashlib.sha256(err).hexdigest(),'newOutputBytes':sum(f.stat().st_size for f in p.rglob('*') if f.is_file()),'failureDetail':None if not err else 'Exporter emitted private diagnostic; inspect locally.'}
with(p/'EXPORT-SUPERVISION.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result));print(out.decode());
if err:sys.stderr.buffer.write(err)
raise SystemExit(0 if status=='completed' else 1)
