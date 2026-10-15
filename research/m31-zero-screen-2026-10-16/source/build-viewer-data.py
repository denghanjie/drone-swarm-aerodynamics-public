"""Hash saved artifacts only. No scientific modules or calculations."""
from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parents[1]
r=json.loads((base/'raw/result.json').read_text())
def spec(name):
 b=(base/'raw'/name).read_bytes()
 return {'url':'../raw/'+name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
cases=[]
for c in r['results']:
 d={k:c[k] for k in ['id','kind','n','pass','expected']};i=c['id']
 d.update(poses=spec(i+'-states.f64'),poseStride=17,poseOffset=0,poseQOffset=6,label=i+(' · fresh static lattice' if c['kind']=='fresh' else ' · exposed fixture'))
 if (base/'raw'/f'{i}-I.f64').exists():d.update(reference=spec(i+'-I.f64'),candidate=spec(i+'-E.f64'),zero=spec(i+'-L.f64'),decisions=spec(i+'-E-decisions.ndjson'),lazyDecisions=spec(i+'-L-decisions.ndjson'))
 cases.append(d)
(base/'viewer/data.json').write_text(json.dumps({'result':spec('result.json'),'cases':cases,'scope':'Saved static inputs, E/L exact-zero category masks and loads. No flight or live scientific simulation.'},indent=2)+'\n')
