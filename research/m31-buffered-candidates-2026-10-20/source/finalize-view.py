from pathlib import Path
import json,hashlib
base=Path(__file__).resolve().parent.parent
assert json.loads((base/'results/audit.json').read_text())['passed'] is True
pins={}
for name in ['view-data.json','audit.json']:
 b=(base/'results'/name).read_bytes();pins[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
with (base/'viewer/pins.json').open('x') as f:json.dump(pins,f,indent=2);f.write('\n')
