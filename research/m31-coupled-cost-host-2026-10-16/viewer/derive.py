"""Saved-record display/report derivation only. No model, root solve or timing."""
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent.parent
prior=p.parent/'m31-swarm-coupling-transfer-2026-10-16'
a=json.loads((p/'results/analysis.json').read_text())
r=json.loads((p/'results/independent-review.json').read_text())
e=json.loads((p/'results/evidence.json').read_text())
assert a['complete'] and r['pass'] and r['complete'] and e['complete']
def pin(f):
 b=f.read_bytes();return {'path':str(f.relative_to(p)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
cs=[]
for case in a['cases']:
 raw=json.loads((p/('results/'+case['id']+'-grid.json')).read_text())
 times=[x for x in e['timings'] if x['id']==case['id'] and x['method']=='B' and not x['warmup']]
 cs.append({'id':case['id'],'n':case['n'],'t':int(case['id'].split('-t')[1]),'rejectedVehicles':[],'rejectionEdges':[],
 'solutions':{'direct':{'y':raw['solutions']['O']['y']}},'methods':{m:v['totalMs'] for m,v in case['methods'].items()},
 'primary':case['primary'],'allPairsDiagnostic':case['allPairsDiagnostic'],'cachedSeparate':case['cachedSeparate'],
 'geometryShare':sum(x['phasesMs']['geometry'] for x in times)/sum(x['totalMs'] for x in times),
 'rawSolution':pin(p/('results/'+case['id']+'-grid.json'))})
(p/'viewer/display.json').write_text(json.dumps({'kind':'saved-pose-and-complete-query-cost-display','sourceCommit':r['resources']['sourceCommit'],'cases':cs},separators=(',',':'))+'\n')
old=json.loads((p.parent/'m31-coupled-cost-2026-10-16/viewer/binding.json').read_text())
b={'files':[pin(p/f) for f in ['viewer/display.json','results/candidate-run.json','results/independent-review.json','results/analysis.json','results/review-run.json']],'inputs':old['inputs']}
(p/'viewer/binding.json').write_text(json.dumps(b,indent=2)+'\n')
lines=['# Complete-query timing: a useful solver change, an expensive grid','',
'We tested whether solving mutual aerodynamic loads in dependency order saves time after paying for the whole interaction query. The answer is yes on these four exposed frozen swarm states—but the chosen conservative grid is slower than direct all-pairs enumeration. This is a computational development result, not physical validation or a completed live swarm.','',
'All 21 controls, eight qualification builds, 16 qualification solves and 140 planned calls completed. The independent saved-record checker passed 10,010 grouped checks. The all-pairs and grid builders matched the previous reference across 608 million saved classification entries in total, sparse coefficients and solved loads. Every timed output passed the frozen postclock comparisons.','',
'| Historical state | All-pairs + ordered A (ms) | Grid + ordered B (ms) | Grid + repeated solve C (ms) | Paired B/C median [min, max] | B wins |',
'|---|---:|---:|---:|---:|---:|']
for c in cs:
 t=c['methods'];v=c['primary']['ratio'];lines.append(f"| {c['id']} | {t['A']['median']:.2f} | {t['B']['median']:.2f} | {t['C']['median']:.2f} | {v['median']:.4f} [{v['minimum']:.4f}, {v['maximum']:.4f}] | {c['primary']['strictWins']}/6 |")
lines+=['','Durations are medians of six measured calls per case/method; ratio summaries use paired blocks, not ratios of marginal medians. Ranges describe observed repetitions, not confidence intervals. One process/device and one historical seed do not provide independent swarm replication.','',
'The predeclared practical rule—at least 5% lower paired median cost and five wins out of six on each 5,000-drone state—passed, with six wins on each. The observed reduction was 7.0%, 7.1% and 8.7%. The grid/ordered complete query still took 621–1,023 ms at N=5,000; even the faster direct all-pairs diagnostic took 517–587 ms. These numbers exclude steering, flight, rendering and data transport.','',
'Geometry construction occupied 96.3–97.6% of aggregate B time on the 5,000-drone states. That measured phase includes candidate enumeration, sorting, exact pair evaluation and sparse assembly; the experiment does not isolate which internal operation dominates. Grid candidate counts were lower, but its overall cost was higher. The earlier exact-zero-screen implementation remains a relevant stronger baseline and was not adapted in this test.','',
'With the matrix already built, ordered solve plus residual cost 17.77–18.29 ms at N=5,000 versus 76.21–97.06 ms for repeated solving. Those cached timings exclude matrix construction, schedule creation and changing poses. They do not establish that a moving swarm can reuse its matrix accurately.','',
'Hardware: Apple M4, 10 physical/logical cores, 24 GiB RAM, arm64 Darwin 25.5.0; Node 24.19.0 / V8 13.6.233.17-node.51, one JS worker, AC power, low-power mode off. Internal sampled RSS peaked at 944,439,296 bytes; external peak was 907,776 KiB. Candidate and reviewer finished in 67.276 s and 3.625 s with exit 0 and no monitoring errors. These invocation durations include evidence work and are not query benchmarks.','',
'What changed: ordered solving earned a modest complete-query saving without observed numerical loss under the frozen tolerances. What failed: the conservative grid did not beat all-pairs enumeration. What remains unresolved: real-time browser flight, changing-pose approximation accuracy, physical model validity, generalization and novelty. Uniform grids and dependency ordering are established methods.','',
'[Frozen protocol](PROTOCOL.md) · [Raw evidence](results/evidence.json) · [Every timing and phase analysis](results/analysis.json) · [Independent checker](results/independent-review.json) · [Reproduction](REPRODUCE.md) · [Visible Three.js checkpoint](viewer/) · [Claim ledger](RESULT-CLAIM-LEDGER.md).', '',
'Source commit: [a459802](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/a459802be0b46beac72f35568a60533215f8f784). Source manifest SHA256: f88099916c1a26fe999fb9a0d998d4e048c486e3d27916541762fa0b93b2284f. Result commit and exact remote manifest verification are recorded separately under research/publication-receipts/.','',
'The original permission-failed allocation stays closed and public. This was a separately registered replacement with unchanged numerical files and the same already exposed states. The review note’s protocol hash discrepancy was corrected in a retained addendum before dispatch; no scientific source or threshold changed.']
(p/'MILESTONE-SUMMARY.md').write_text('\n'.join(lines)+'\n')
print('Derived 4 display cases and result summary from saved audited records.')
