"""Read-only job snapshot (also usable after an interrupted chat)."""
from pathlib import Path
import json,struct
root=Path(__file__).resolve().parent.parent;d=root/'milestone-31-source';p=root/'milestone-31-progress.json';runs=json.loads(p.read_text()) if p.exists() else [];done={r['job']['id'] for r in runs};out=dict(completed=len(runs),planned=10,recent=[dict(id=r['job']['id'],t=r['metrics']['end'],passed=r['metrics']['passed'],stop=r['metrics']['stopReason']) for r in runs[-2:]],running=[])
for p in d.glob('progress-*.json'):
 r=json.loads(p.read_text());j=r['job']
 if j['id'] in done:continue
 f=d/(j['id']+'.f64');w=8*(1+7*j['count']);size=f.stat().st_size;complete=size//w
 with f.open('rb') as fd:fd.seek(max(0,(complete-1)*w));t=struct.unpack('<d',fd.read(8))[0]
 out['running'].append(dict(id=j['id'],savedFrameTime=t,progressTime=r['t'],passed=r['passed'],lastProgressWallSeconds=round(r['wallMs']/1000,1)))
print(json.dumps(out,indent=2))
