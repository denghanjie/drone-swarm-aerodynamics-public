from pathlib import Path
import json,hashlib,subprocess,os,time,signal,stat
p=Path(__file__).resolve().parent.parent;r=p.parent.parent;origin='bf064b2c4d54c7ed61a55ae1791fa64bf4e044fe'
paths=[]
def add(pre,names):paths.extend(pre+'/'+n for n in names)
add('research/m31-buffered-motion-2026-10-22',['extract/index.json','transport/index.json','audit/audit.json','ALLOCATION-CLOSURE.json','result-manifest.json'])
t=json.loads((r/'research/m31-buffered-motion-2026-10-22/transport/index.json').read_text());add('research/m31-buffered-motion-2026-10-22/transport',[x['file'] for x in t['parts']])
add('research/m31-radial-integration-2026-10-23',['audit/audit.json','ALLOCATION-CLOSURE.json','result-manifest.json'])
add('research/publication-receipts',['m31-radial-integration-result-2026-10-23.json'])
add('research/m31-neighbor-density-2026-10-23',['results/stages.jsonl','results/summary.json'])
add('research/m31-phase-attribution-2026-10-23',['results/summary.json','audit/audit.json','ALLOCATION-CLOSURE.json','result-manifest.json','SUMMARY.md'])
add('research/publication-receipts',['m31-buffered-motion-result-2026-10-22.json','m31-phase-attribution-result-2026-10-23.json'])
add('research/m31-native-fresh-transfer-2026-10-17/source',['native-load.cjs','native-controls.cjs','vendor/kernel.cjs','vendor/anchor-kernel.cjs','vendor/lean-anchor.cjs','vendor/reference-excerpt.cjs','vendor/controls.cjs'])
add('research/m31-normalizer-planning-2026-10-17',['CANDIDATE-DESIGN.md','PARENT-DECISION.md'])
add('research/m31-normalizer-replication-2026-10-17',['MILESTONE-SUMMARY.md'])
add('research/m31-typed-assembly-2026-10-16',['MILESTONE-SUMMARY.md'])

start=time.monotonic();events=[];pins=[]
ledger=p/'INPUT-RECOVERY.json'
assert not ledger.exists() and not (p/'input-pins.json').exists()
def save():ledger.write_text(json.dumps({'schema':'m31-factor-input-recovery-v1','closed':False,'events':events,'scope':'Opaque local bytes bound to origin tree blob OID; no archive decode or Git blob extraction'},indent=2)+'\n')
def expire(*_):raise TimeoutError('administrative-recovery-120s')
signal.signal(signal.SIGALRM,expire);signal.alarm(120);save()
try:
 for path in sorted(set(paths)):
  f=r/path;s=f.lstat();assert stat.S_ISREG(s.st_mode) and not f.is_symlink()
  env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
  raw=subprocess.check_output(['git','ls-tree','-z',origin,'--',path],cwd=r,env=env,timeout=min(45,120-(time.monotonic()-start)))
  entry=raw.removesuffix(b'\0');meta,name=entry.split(b'\t');mode,kind,oid=meta.split()
  assert name.decode()==path and kind==b'blob' and mode in (b'100644',b'100755')
  h=hashlib.sha256();g=hashlib.sha1(b'blob '+str(s.st_size).encode()+b'\0');count=0
  with f.open('rb') as stream:
   for b in iter(lambda:stream.read(1048576),b''):h.update(b);g.update(b);count+=len(b)
  assert count==s.st_size==f.stat().st_size and g.hexdigest()==oid.decode()
  pin={'path':path,'bytes':count,'sha256':h.hexdigest(),'kind':'input','originCommit':origin,'gitBlobOid':oid.decode()}
  pins.append(pin);events.append({'path':path,'kind':'tree-local-blob-identity-pass','bytes':count,'sha256':pin['sha256'],'gitBlobOid':pin['gitBlobOid']});save()
 (p/'input-pins.json').write_text(json.dumps({'files':pins},indent=2)+'\n')
 result={'closed':True,'passed':True,'pins':len(pins),'events':events,'wallSeconds':time.monotonic()-start,'gitBlobExtracted':False}
except BaseException as e:
 result={'closed':True,'passed':False,'events':events,'wallSeconds':time.monotonic()-start,'error':type(e).__name__,'detail':str(e).replace(str(r),'[repository]')[:500],'gitBlobExtracted':False}
 ledger.write_text(json.dumps(result,indent=2)+'\n');raise
finally:signal.alarm(0)
ledger.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'pins':len(pins),'bytes':sum(x['bytes'] for x in pins)}))
