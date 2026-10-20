from pathlib import Path
import json,hashlib
base=Path(__file__).resolve().parent.parent
audit_record=json.loads((base/'audit/audit.json').read_text())
assert audit_record['passed'] is True
assert json.loads((base/'audit-supervisor.json').read_text())['returncode']==0
assert json.loads((base/'audit-supervisor.json').read_text())['allocationWallPassed'] is True
assert json.loads((base/'audit-supervisor.json').read_text())['outputCapPassed'] is True
assert json.loads((base/'results/exit.json').read_text())['exitCode']==0
audit_exit=json.loads((base/'audit/exit.json').read_text())
assert audit_exit['exitCode']==0 and audit_exit['closed'] is True and audit_exit['wallSeconds']<=1200
assert not (base/'audit/failure.json').exists()
assert sum(p.stat().st_size for p in (base/'audit').iterdir())<=64*1024*1024
out={}
for key,file in [('audit','audit/audit.json'),('data','audit/viewer-data.json'),('exit','results/exit.json'),('auditExit','audit/exit.json')]:
 raw=(base/file).read_bytes();out[key]={'file':file,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
assert out['data']==audit_record['viewerPin']
with (base/'viewer/pins.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
