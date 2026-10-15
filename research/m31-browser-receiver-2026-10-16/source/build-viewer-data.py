"""Package links to retained evidence only. No scientific module/solver execution."""
from pathlib import Path
import json,hashlib,os
base=Path(__file__).resolve().parents[1];repo=base.parents[1];view=base/'viewer'
def spec(path):
 b=path.read_bytes();return {'url':os.path.relpath(path,view),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
cases=[]
for id,n in [('fresh1000',1000),('fresh5000',5000)]:
 row={'id':id,'n':n,'label':f'{n:,} drones · reused static poses','poseStride':17,'poseQOffset':6,'poses':spec(repo/'research/m31-zero-screen-2026-10-16/raw'/(id+'-states.f64'))}
 for key,suffix in [('reference','-original.f64'),('gpu','-gpu.u32'),('packed','-packed.u32'),('q','-Q.f64'),('a','-A.f64')]:row[key]=spec(base/'raw'/(id+suffix))
 cases.append(row)
meta={'scope':'Recorded receiver-only WebGPU results on reused static numerical inputs. Poses are context; no wake, controller or trajectory computed in this campaign. Host force sums are display reductions, not GPU assembly qualification.','review':spec(base/'results/independent-review.json'),'result':spec(base/'results/result.json'),'budget':spec(base/'results/budget.json'),'cases':cases,'scalars':{k:spec(base/'raw'/('scalar32'+suffix)) for k,suffix in [('reference','-original.f64'),('gpu','-gpu.u32'),('q','-Q.f64'),('a','-A.f64')]},'invalid':spec(base/'raw/invalid5-gpu.u32')}
view.mkdir(exist_ok=True);(view/'data.json').write_text(json.dumps(meta,indent=2)+'\n')
print('Saved-data viewer links prepared; no new science.')
