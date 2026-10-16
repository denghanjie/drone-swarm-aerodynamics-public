"""Display derivation from saved records only; no scientific model or timing."""
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent.parent
read=lambda name:json.loads((p/name).read_text())
def pin(f):
 b=f.read_bytes();return {'path':str(f.relative_to(p)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
e=read('results/evidence.json') if (p/'results/evidence.json').exists() else read('results/partial-evidence.json')
r=read('results/independent-review.json');a=read('results/analysis.json');run=read('results/candidate-run.json');rr=read('results/review-run.json')
verified=bool(r['pass'] and run['supervisor_success'] and rr['supervisor_success']);passed=a['practicalRulePass'];cases=[]
for info in read('config.json')['cases']:
 f=p/('generation/'+info['id']+'.json')
 if not f.exists():continue
 g=json.loads(f.read_text());rec={**info,'frames':g['poses']['frames'],'poses':g['poses'],'description':'Fresh two-second local 3D Boids flight. Airflow was off; the final pose supplies this separate coupled-load query. The short horizon does not test mature flock behavior or long-flight success.'}
 match=next((c for c in a['cases'] if c['id']==info['id']),None)
 if verified and match:
  q=read('results/'+info['id']+'-A.json');rec.update(y=q['solutions']['O']['y'],loadPin=pin(p/('results/'+info['id']+'-A.json')),methods={m:v['totalMs'] for m,v in match['methods'].items()},pairs=match['pairs'],practicalRulePass=match.get('practicalRulePass'))
 cases.append(rec)
if verified and passed:
 headline='Same answers.<br>Less storage work.';lead='The typed assembly package met the fixed timing rule on both fresh 5,000-drone cases while preserving the computed results.';finding='Typed storage passed this bounded engineering test beyond matched lean arithmetic. It remains an implementation result on two short-flight inputs; the individual causes and broad generalization remain untested.'
elif verified:
 headline='Same answers.<br>Storage target missed.';lead='The typed assembly package preserved the calculation but did not meet the fixed improvement rule against the equally lean baseline.';finding='The matched comparison did not support the planned practical advantage. We retain the negative result and close this storage-variant line instead of tuning it on these cases.'
else:
 headline='A preserved attempt.<br>An unresolved result.';lead='This attempt did not complete all required evidence checks. Its records remain available, and no practical performance conclusion is accepted.';finding='A failed or incomplete evidence gate is a research result to investigate, not a reason to replace cases or relax tolerances.'
display={'kind':'fresh-recorded-boids-and-typed-assembly','sourceCommit':run['source_commit'],'verified':verified,'practicalPass':passed,'timingCalls':len(e['timings']),'headline':headline,'lead':lead,'finding':finding,'cases':cases}
(p/'viewer/display.json').write_text(json.dumps(display,separators=(',',':'))+'\n')
records={'display':'viewer/display.json','run':'results/candidate-run.json','review':'results/independent-review.json','analysis':'results/analysis.json','reviewRun':'results/review-run.json'}
(p/'viewer/binding.json').write_text(json.dumps({'records':{k:pin(p/v) for k,v in records.items()}},indent=2)+'\n')
print(json.dumps({'displayCases':len(cases),'verified':verified,'practicalPass':passed}))
