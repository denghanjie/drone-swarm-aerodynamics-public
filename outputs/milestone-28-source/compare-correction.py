"""Paired comparison of preserved erroneous scale and corrected scale; not accuracy."""
from pathlib import Path
import json,math,hashlib
root=Path(__file__).resolve().parent.parent;old=root/'milestone-27-source';new=root/'milestone-28-source'
p0=json.loads((root/'milestone-27-protocol.json').read_text());p1=json.loads((root/'milestone-28-protocol.json').read_text());assert p0['jobs']==p1['jobs']
for name in ['sim.cjs','factory.cjs','factory-wide.cjs','grid.cjs','geometry.cjs']:
 assert (old/name).read_text().replace('milestone-27','milestone-28')==(new/name).read_text(),name+' changed beyond correction'
a=(old/'aero.cjs').read_text();b=(new/'aero.cjs').read_text();a='\n'.join(x for x in a.splitlines() if not x.startswith('//'));b='\n'.join(x for x in b.splitlines() if not x.startswith('//'));assert a.replace('motorDistance:2*F.P.a','motorDistance:2*Math.SQRT2*F.P.a')==b
rows=[];unpaired=[]
for job in p1['jobs']:
 file=job['id']+'.json'
 if not (new/file).exists():continue
 if not (old/file).exists():unpaired.append({'job':job['id'],'reason':'Original erroneous-model study terminated before a completed matching run; corrected run still evaluated against its own protocol.'});continue
 a=json.loads((old/file).read_text());b=json.loads((new/file).read_text());assert a['initial']==b['initial'],file+' starts differ'
 if job['aeroMode']=='off':assert a['final']==b['final'] and a['metrics']==b['metrics'] and a['samples']==b['samples'],file+' airflow-off changed'
 rows.append({'job':job,'wrongScale':{'end':a['metrics']['end'],'completed':a['metrics']['passed'],'stop':a['metrics']['stopReason'],'failure':a['metrics']['failure'],'maximumInflow':a['aeroStats']['maximumInflow']},'correctedScale':{'end':b['metrics']['end'],'completed':b['metrics']['passed'],'stop':b['metrics']['stopReason'],'failure':b['metrics']['failure'],'maximumInflow':b['aeroStats']['maximumInflow']},'sameInitialStates':True,'endpointDifferenceM':max(math.dist(x[:3],y[:3]) for x,y in zip(a['final'],b['final'])),'sameEndTime':a['metrics']['end']==b['metrics']['end'],'caution':'When terminal times differ, endpoint differences include unequal flight duration; this is not a synchronized trajectory error or error against reality.'})
result={'status':'paired correction evidence, not physical validation','sourceIsolationVerified':True,'changedParameter':'motorDistance: adjacent0.056m to opposite0.07919595949289333m','completedPairs':len(rows),'originalProtocolCases':len(p1['jobs']),'correctedCasesWithoutCompletedOriginal':unpaired,'comparisons':rows};(root/'milestone-28-correction-comparisons.json').write_text(json.dumps(result,indent=2));print({'matchedPairs':len(rows),'sourceIsolationVerified':True})
