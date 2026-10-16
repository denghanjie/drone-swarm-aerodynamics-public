import json,pathlib,hashlib,gzip
import numpy as np
p=pathlib.Path.cwd()/'research/m31-swarm-coupling-transfer-2026-10-16'
e=json.loads((p/'results/evidence.json').read_text());review=json.loads((p/'results/independent-review.json').read_text())
assert e['complete']
display=[];summary=[]
for c in e['cases']:
 n=c['n'];rejected=set();edges=[];total_edges=0
 with gzip.open(p/c['symbols']['path'],'rb') as f:
  for i in range(n):
   row=np.frombuffer(f.read(n*4),dtype=np.uint8).reshape(n,4)
   js=np.flatnonzero(np.any((row==4)|(row==11),axis=1))
   for j in js:
    rejected.update([i,int(j)]);total_edges+=1
    if len(edges)<200: edges.append([int(j),i])
  assert f.read(1)==b''
 display.append(dict(id=c['id'],rejectedVehicles=sorted(rejected),rejectionEdges=edges,totalRejectedVehiclePairs=total_edges,edgeDisplayPolicy='first 200 unique rejected receiver/source pairs in canonical order; all endpoints retained'))
 s=dict(id=c['id'],n=n,t=c['t'],admission=c['admission'],input=c['input'],geometryWork=c['geometryWork'],graph={k:c['graph'][k] for k in ['uniqueVehicleEdges','maxIncomingDegree','heightViolationEdges','orderViolationEdges','descendingEligible','maxDependencyDepth']},ordinaryLmax=c['ordinaryLmax'],rejectedVehicleCount=len(rejected),rejectedVehiclePairs=total_edges,solutions=None)
 if c['solutions']:
  a,b=c['solutions']['direct'],c['solutions']['picard'];ar=np.array([[r['T'] for r in x] for x in a['rotors']]);br=np.array([[r['T'] for r in x] for x in b['rotors']]);ratios=np.square(a['y'])
  s['solutions']=dict(iterations=b['iterations'],converged=b['converged'],directWork=a['work'],picardWork=b['work'],directResidualWork=a['residualWork'],picardResidualWork=b['residualWork'],directResidualLog=a['residualLog'],picardResidualLog=b['residualLog'],directVsPicardMaxRotorRelativeDifference=float(np.max(np.abs(ar-br)/ar)),sourceLoadRatioMin=float(np.min(ratios)),sourceLoadRatioMean=float(np.mean(ratios)),sourceLoadRatioMax=float(np.max(ratios)))
 summary.append(s)
result=dict(kind='saved-evidence-descriptive-analysis',independentReviewPassed=review['pass'],checkCount=review['checkCount'],cases=summary,interpretation='No model reevaluation; statistics derived from saved record and symbol bytes. Frozen historical airflow-off poses; no real-time or physical-validation result.')
for rel,obj in [('results/analysis.json',result),('viewer/display.json',dict(cases=display))]:
 with (p/rel).open('x') as f: json.dump(obj,f,indent=2);f.write('\n')
def pin(rel):
 b=(p/rel).read_bytes();return dict(path=rel,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
index=json.loads((p/'inputs/index.json').read_text())
binding=dict(kind='saved-experiment-display-binding',files=[pin(x) for x in ['results/evidence.json','results/independent-review.json','viewer/display.json']],inputs=[dict(id=x['id'],**pin(x['path'])) for x in index['cases']])
with (p/'viewer/binding.json').open('x') as f: json.dump(binding,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
