from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[3];b=Path(__file__).resolve().parents[1]
def spec(path,url):return {'url':url,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
r=json.loads((b/'raw/result.json').read_text());m={'result':spec(b/'raw/result.json','../raw/result.json'),'metadata':spec(root/'research/m31-restart-2026-10-15/viewer/data.json','../../m31-restart-2026-10-15/viewer/data.json'),'poses':spec(root/'research/m31-restart-2026-10-15/viewer/snapshots.bin','../../m31-restart-2026-10-15/viewer/snapshots.bin'),'snapshots':{}}
for s in r['snapshots']:
 m['snapshots'][s['id']]={kind:spec(b/'raw'/f"{s['id']}-{kind}.f64",f"../raw/{s['id']}-{kind}.f64") for kind in ['rotors','vehicles']}
(b/'viewer/data.json').write_text(json.dumps(m,indent=2)+'\n')
