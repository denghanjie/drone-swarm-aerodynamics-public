from pathlib import Path
import json,hashlib
base=Path(__file__).resolve().parent.parent
assert json.loads((base/'results/audit.json').read_text())['passed'] is True
closed=json.loads((base/'results/exit.json').read_text())
assert closed['exitCode']==0 and closed['exportWallSeconds']<=30
assert not (base/'results/failure.json').exists()
assert sum(p.stat().st_size for p in (base/'results').iterdir() if p.is_file())<=10*1048576
pins={}
for name in ['view-data.json','audit.json','exit.json']:
 b=(base/'results'/name).read_bytes();pins[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
with (base/'viewer/pins.json').open('x') as f:json.dump(pins,f,indent=2);f.write('\n')
