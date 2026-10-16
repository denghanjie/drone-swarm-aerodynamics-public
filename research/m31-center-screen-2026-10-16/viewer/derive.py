"""Display-only transformation of terminal saved records; no model or timing run."""
from pathlib import Path
import hashlib
import json

p = Path(__file__).resolve().parent.parent

def read(name):
    return json.loads((p/name).read_text())

def pin(f):
    b = f.read_bytes()
    return dict(path=str(f.relative_to(p)), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

e = read('results/evidence.json') if (p/'results/evidence.json').exists() else read('results/partial-evidence.json')
r = read('results/independent-review.json')
a = read('results/analysis.json')
run, rr = read('results/candidate-run.json'), read('results/review-run.json')
seal = read('results/qualification.json')
verified = bool(r.get('pass') is True and r.get('complete') is True and a.get('independentAuditPass') is True and all(x.get('supervisorSuccess') is True and x.get('closed') is True and x.get('childGroupAbsent') is True for x in [run, rr]) and seal.get('sealSuccess') is True and seal.get('evidenceQualified') is True)
passed = verified and bool(seal.get('practicalRulePass'))
cases = []
for info in read('config.json')['cases']:
    f = p/('generation/'+info['id']+'.json')
    if not f.exists():
        continue
    g = json.loads(f.read_text())
    rec = dict(**info, frames=g['poses']['frames'], poses=g['poses'],
               description='Fresh two-second local 3D Boids flight. Airflow was off; the final pose supplies the separate coupled-load query. The short horizon does not test mature flock behavior or long-flight success.')
    match = next((c for c in a.get('cases', []) if c['id']==info['id']), None)
    if verified and match:
        q = read('results/'+info['id']+'-L.json')
        rec.update(y=q['solutions']['O']['y'], loadPin=pin(p/('results/'+info['id']+'-L.json')),
                   methods={m:v['totalMs'] for m,v in match['methods'].items()}, pairs=match['pairs'],
                   practicalRulePass=match.get('performanceRulePass'))
    cases.append(rec)

if verified and passed:
    headline = 'Same tested answers.\nFewer distance calculations.'
    lead = 'The current-position screen met the fixed timing rule on both fresh 5,000-drone cases while preserving all checked outputs.'
    finding = 'This ordinary implementation optimization passed a bounded engineering test. It is finite evidence for the named runtime and tested inputs, without portable equivalence, a physical-accuracy finding or a live-swarm speed claim.'
elif verified:
    headline = 'Same tested answers.\nTiming target missed.'
    lead = 'The current-position screen preserved the checked outputs but did not meet the fixed improvement rule on both 5,000-drone cases.'
    finding = 'The fixed performance premise was not supported on this workload. The result closes this screen experiment; its threshold and seeds are not tuned afterward.'
else:
    headline = 'A preserved attempt.\nAn unresolved result.'
    lead = 'This attempt did not pass every required evidence check. No performance qualification is accepted.'
    finding = 'The incomplete or failed records remain available. They do not justify a speed, equivalence or physical-validity conclusion.'

display = dict(kind='fresh-recorded-boids-and-center-screen', sourceCommit=run['sourceCommit'],
               verified=verified, practicalPass=passed, timingCalls=len(e.get('timings', [])),
               headline=headline, lead=lead, finding=finding, cases=cases)
(p/'viewer/display.json').write_text(json.dumps(display, separators=(',', ':'))+'\n')
records = dict(display='viewer/display.json', run='results/candidate-run.json', review='results/independent-review.json',
               analysis='results/analysis.json', reviewRun='results/review-run.json', qualification='results/qualification.json')
(p/'viewer/binding.json').write_text(json.dumps(dict(records={k:pin(p/v) for k,v in records.items()}), indent=2)+'\n')
print(json.dumps(dict(displayCases=len(cases), verified=verified, practicalPass=passed)))
