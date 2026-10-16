"""Descriptive argmax extraction from closed saved records; no model imports/solves."""
from pathlib import Path
import json,math,hashlib
p=Path(__file__).resolve().parent.parent
read=lambda name:json.loads((p/'results'/name).read_text())
a=read('analysis.json');out={'kind':'postrun-descriptive-saved-extrema','sourceCommit':read('candidate-run.json')['source_commit'],'method':'Locate maxima from saved arrays only; no simulation, fitting or new gate. Drone and rotor indices are zero-based.','inputPins':[],'grids':[]}
mg=.027*9.81;hover=mg/4;R=math.sqrt(2)*.028
norm=lambda xs:math.sqrt(math.fsum(x*x for x in xs))
def angle(a,b):
 sign=-1 if math.fsum(x*y for x,y in zip(a,b))<0 else 1
 return 4*math.atan2(norm([x-sign*y for x,y in zip(a,b)]),norm([x+sign*y for x,y in zip(a,b)]))
for dt in [.005,.0025,.00125]:
 files=['boids16-'+mode+'-'+str(dt)+'.json' for mode in ['coupled','reuse10ms']]
 full,reuse=[read(f) for f in files]
 for f in files:
  raw=(p/'results'/f).read_bytes();out['inputPins'].append({'path':'results/'+f,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 extrema={k:{'maximum':-1} for k in ['position','velocity','attitude','rotor','bodyRate']}
 for x,y in zip(full['samples'],reuse['samples']):
  for i,(s,t) in enumerate(zip(x['states'],y['states'])):
   values={key:norm([s[k]-t[k] for k in range(start,start+3)]) for key,start in [('position',0),('velocity',3),('bodyRate',10)]};values['attitude']=angle(s[6:10],t[6:10]);rotor=max(range(4),key=lambda r:abs(x['forces'][i][r]-y['forces'][i][r]));values['rotor']=abs(x['forces'][i][rotor]-y['forces'][i][rotor])/hover
   for k,v in values.items():
    if v>extrema[k]['maximum']:extrema[k]={'maximum':v,'t':x['t'],'droneIndex':i,**({'rotorIndex':rotor} if k=='rotor' else {})}
 events={k:{'maximum':-1} for k in ['rotor','force','moment']}
 for e in reuse['events'][1:]:
  left,fresh=e['left'],e['instantaneous']
  for i in range(16):
   rotor=max(range(4),key=lambda r:abs(left['forces'][i][r]-fresh['forces'][i][r]));values={'rotor':abs(left['forces'][i][rotor]-fresh['forces'][i][rotor])/hover,'force':norm([x-y for x,y in zip(left['corrections'][i]['force'],fresh['corrections'][i]['force'])])/mg,'moment':norm([x-y for x,y in zip(left['corrections'][i]['torque'],fresh['corrections'][i]['torque'])])/(mg*R)}
   for k,v in values.items():
    if v>events[k]['maximum']:events[k]={'maximum':v,'t':e['t'],'eventIndex':e['index'],'droneIndex':i,'rawSI':v*{'rotor':hover,'force':mg,'moment':mg*R}[k],**({'rotorIndex':rotor} if k=='rotor' else {})}
 expected=next(x for x in a['comparisons'] if x['dt']==dt)['maximumSampled'];expected_events=next(x for x in a['eventErrors'] if x['dt']==dt)['maxima']
 for key,val in extrema.items():assert abs(val['maximum']-expected[key])<1e-12
 for key,val in events.items():assert abs(val['maximum']-expected_events[key])<1e-12
 out['grids'].append({'dt':dt,'trajectoryExtrema':extrema,'beforeRefreshExtrema':events})
with (p/'analysis/saved-extrema.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out['grids'][-1]))
