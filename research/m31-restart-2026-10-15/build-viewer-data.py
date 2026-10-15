#!/usr/bin/env python3
"""Extract exact historical poses for an audit viewer; never runs the simulator."""
from pathlib import Path
import argparse,array,sys,json,hashlib,math,statistics
P=argparse.ArgumentParser();P.add_argument('--evidence-root',type=Path,default=Path(__file__).resolve().parents[2]);a=P.parse_args();out=Path(__file__).resolve().parent/'viewer';out.mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
comp=json.loads((a.evidence_root/'outputs/milestone-31-comparisons.json').read_text());cases=[];blob=array.array('d')
for c in comp:
 ids=[c['coarse'],c['fine']];runs=[];hashes=[]
 for id in ids:
  p=a.evidence_root/'outputs/milestone-31-source'/f'{id}.json';r=json.loads(p.read_text());bp=p.parent/r['replay']['file'];v=array.array('d')
  with bp.open('rb') as f:v.fromfile(f,bp.stat().st_size//8)
  if sys.byteorder!='little':v.byteswap()
  stride=r['replay']['valuesPerFrame'];assert len(v)==stride*r['replay']['frames'];frames={v[i]:v[i+1:i+stride] for i in range(0,len(v),stride)};runs.append((r,frames));hashes.extend([{'path':str(p.relative_to(a.evidence_root)),'sha256':sha(p)},{'path':str(bp.relative_to(a.evidence_root)),'sha256':sha(bp)}])
 n=runs[0][0]['config']['count'];times=[t for t in [0,20,30,60,180] if t in runs[0][1] and t in runs[1][1]];samples=[]
 for t in times:
  x,y=runs[0][1][t],runs[1][1][t];assert len(x)==len(y)==7*n
  errors=[math.dist(x[7*i:7*i+3],y[7*i:7*i+3]) for i in range(n)];maximum=max(errors);stored=next(q for q in c['positionDifferenceAtSavedTimes'] if q['t']==t);assert abs(maximum-stored['maximum'])<1e-10
  offsets=[]
  for poses in [x,y]:offsets.append(len(blob));blob.extend(poses)
  samples.append({'t':t,'offsets':offsets,'maximum':maximum,'median':statistics.median(errors),'p95':sorted(errors)[math.ceil(.95*n)-1],'worstDrone':errors.index(maximum)})
 course=runs[0][0]['job']['course'];geometryPath=a.evidence_root/f'outputs/milestone-31-source/factory-{course}.json';geometry=json.loads(geometryPath.read_text());hashes.append({'path':str(geometryPath.relative_to(a.evidence_root)),'sha256':sha(geometryPath)})
 cases.append({'label':f'{n:,} drones · {course} openings','count':n,'course':course,'seed':runs[0][0]['config']['seed'],'ids':ids,'stepMs':[runs[0][0]['config']['dt']*1000,runs[1][0]['config']['dt']*1000],'times':times,'samples':samples,'geometry':geometry,'scope':c['scope'],'firstSavedTimeAtOrAboveOneCentimeter':c['firstSavedTimeAtOrAboveOneCentimeter'],'maximumOverAllSavedTimes':c['maximumSynchronizedPositionDifference'],'inputHashes':hashes})
if sys.byteorder!='little':blob.byteswap()
with (out/'snapshots.bin').open('wb') as f:blob.tofile(f)
result={'schema':'m31-audit-saved-poses-v1','dataType':'Float64LE','valuesPerDrone':7,'quaternionOrder':'x,y,z,w','positionUnits':'m','offsetUnits':'Float64 values','scope':'Exact selected saved poses from existing M31 traces. No new simulations. Statistics computed for all drones at each displayed time, with no interpolation.','binarySha256':sha(out/'snapshots.bin'),'binaryBytes':(out/'snapshots.bin').stat().st_size,'comparisonInput':{'path':'outputs/milestone-31-comparisons.json','sha256':sha(a.evidence_root/'outputs/milestone-31-comparisons.json')},'cases':cases};(out/'data.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'cases':len(cases),'bytes':result['binaryBytes'],'allDisplayedMaximumsMatchHistoricalComparisons':True}))
