"""Saved-byte metadata only: no fields, geometry generation, roots or timing repeats."""
from pathlib import Path
import json,hashlib,os
base=Path(__file__).resolve().parents[1];v=base/'viewer';r=json.loads((base/'raw/result.json').read_text())
def spec(p):return {'url':os.path.relpath(p,v),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
cases=[]
for s in r['results']:
 item={**s,'poses':spec(base/'raw'/(s['id']+'-states.f64')),'poseStride':17,'poseOffset':0,'poseQOffset':6,'candidate':None,'zero':None,'reference':None,'decisions':None}
 item['label']=s['id']+(' · expected domain test' if 'domain' in s else ' · fresh static case' if s['kind']=='fresh' else ' · exposed fixture')
 for field,suffix in [('candidate','C.f64'),('zero','Z.f64'),('reference','I.f64'),('decisions','C-decisions.ndjson')]:
  p=base/'raw'/(s['id']+'-'+suffix)
  if p.exists() and 'domain' not in s:item[field]=spec(p)
 cases.append(item)
(v/'data.json').write_text(json.dumps({'result':spec(base/'raw/result.json'),'cases':cases,'scope':'Saved static poses, full/Z/C loads and shadow C selection; no simulation or interpolated flight'},indent=2)+'\n')
print('Saved-only metadata for',len(cases),'cases')
