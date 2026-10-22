from pathlib import Path
import json,hashlib,time,sys
import os
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
base=Path(__file__).resolve().parent.parent;out=base/'finalize';out.mkdir();start=time.monotonic()
def pin(p):
 b=p.read_bytes();return {'file':str(p.relative_to(base)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
try:
 for phase in ['extract','producer','audit']:
  s=json.loads((base/(phase+'-supervisor.json')).read_bytes());assert s['returncode']==0 and s['allocationWallPassed'] and s['outputCapPassed'] and not s.get('timeout')
 for phase in ['extract','results','audit']:
  assert not (base/phase/'failure.json').exists();e=json.loads((base/phase/'exit.json').read_bytes());assert e['closed'] and e['exitCode']==0
 a=json.loads((base/'audit/audit.json').read_bytes());assert a['passed']
 data=pin(base/'audit/viewer-data.json');assert data['sha256']==a['viewerPin']['sha256'] and data['bytes']==a['viewerPin']['bytes']
 pins={k:pin(base/p) for k,p in {'data':'audit/viewer-data.json','audit':'audit/audit.json','producer':'producer-supervisor.json','auditor':'audit-supervisor.json'}.items()}
 raw=(json.dumps(pins)+'\n').encode();assert len(raw)<=65536
 with (base/'viewer/pins.json').open('xb') as f:f.write(raw)
 with (out/'report.json').open('x') as f:json.dump({'passed':True,'closed':True,'wallSeconds':time.monotonic()-start,'pins':pins},f);f.write('\n')
except Exception as e:
 with (out/'failure.json').open('x') as f:json.dump({'passed':False,'closed':True,'message':str(e)[:500]},f)
 sys.exit(1)
