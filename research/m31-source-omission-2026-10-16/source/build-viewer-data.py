"""Postrun byte-copy/reformat only; no fields, geometry generation, roots or timing."""
from pathlib import Path
import struct,json,hashlib
root=Path(__file__).resolve().parents[3];base=Path(__file__).resolve().parents[1];v=base/'viewer';(v/'reference').mkdir(exist_ok=True)
r=json.loads((base/'raw/result.json').read_text());old=root/'research/m31-flock-force-reference-2026-10-15';oldr=json.loads((old/'raw/result.json').read_text())
def spec(p):return {'url':str(Path(__import__('os').path.relpath(p,v))),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
cases=[]
for s in r['results']:
 item={**s,'candidate':None,'reference':None,'decisions':None}
 if s['kind']=='exposed':
  orig=next(x for x in oldr['snapshots'] if 'historical-'+x['id']==s['id']);item['poses']=spec(root/'research/m31-restart-2026-10-15/viewer/snapshots.bin');item['poseStride']=7;item['poseOffset']=orig['binaryOffsetValues'];item['poseQOffset']=3
  rr=(old/'raw'/(orig['id']+'-rotors.f64')).read_bytes();vv=(old/'raw'/(orig['id']+'-vehicles.f64')).read_bytes();out=bytearray()
  for i in range(s['n']):
   rv=lambda k,col:struct.unpack_from('<d',rr,8*(16*(4*i+k)+col))[0]
   vl=lambda j:struct.unpack_from('<d',vv,8*(35*i+j))[0]
   row=[rv(k,1) for k in range(4)]+[rv(k,4) for k in range(4)]+[vl(j) for j in [1,5,6,11,12,13,25,26,27]];out+=struct.pack('<17d',*row)
  dst=v/'reference'/(s['id']+'.f64');dst.write_bytes(out);item['reference']=spec(dst)
  item['label']=['1,000 · wide','1,000 · narrow','5,000 · wide'][orig['caseIndex']]+f" · saved {orig['time']} s"
 else:
  item['poses']=spec(base/'raw'/(s['id']+'-states.f64'));item['poseStride']=17;item['poseOffset']=0;item['poseQOffset']=6;item['label']=s['id']+(' · expected domain test' if 'domain' in s else ' · new static case')
  f=base/'raw'/(s['id']+'-I.f64')
  if f.exists():item['reference']=spec(f)
 f=base/'raw'/(s['id']+'-C.f64')
 if f.exists():item['candidate']=spec(f)
 f=base/'raw'/(s['id']+'-decisions.ndjson')
 if f.exists() and item['candidate']:item['decisions']=spec(f)
 cases.append(item)
(v/'data.json').write_text(json.dumps({'result':spec(base/'raw/result.json'),'cases':cases,'scope':'Exact saved poses and static full/approximate model loads; no live flight or interpolation'},indent=2)+'\n')
print('Built viewer metadata for',len(cases),'recorded inputs')
