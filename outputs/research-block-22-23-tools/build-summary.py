from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'milestone-23-summary.json').read_text());primary=[r for r in data if r['config']['dt']==.0025];checks=json.loads((root/'milestone-23-comparisons.json').read_text());audit=json.loads((root/'milestone-23-failure-audit.json').read_text());a22=json.loads((root/'milestone-22-refinement-audit.json').read_text())
def ok(r):return r['metrics']['passed']==50 and not r['metrics']['stopReason']
stats={e:sum(ok(r) for r in primary if r['config']['estimator']==e) for e in ['raw','predict']}
pairs=[]
for raw in primary:
 if raw['config']['estimator']!='raw':continue
 pred=next(r for r in primary if r['config']['seed']==raw['config']['seed'] and r['config']['scenario']==raw['config']['scenario'] and r['config']['estimator']=='predict')
 pairs.append((raw,pred))
helped=[(a['config']['seed'],a['config']['scenario']) for a,b in pairs if not ok(a) and ok(b)];hurt=[(a['config']['seed'],a['config']['scenario']) for a,b in pairs if ok(a) and not ok(b)]
fmt=lambda cases:', '.join(f'{s}/{c}' for s,c in cases) or 'none'
text=f'''# Research block22–23 — prediction helps some flocks and hurts others

**The new rule is not a reliable replacement. We now have saved examples of both recovery and newly introduced contact.**

We completed {55+len(audit)} simulation runs:16 development runs,38 fresh-flock runs, one extra development refinement, and{len(audit)} separate raw-failure audit run(s). Both checkpoints include their own Three.js comparisons, source, protocols, full states, failure records and reports.

## What we tried

A delayed measurement tells a drone where its neighbors **were**. Our candidate estimates where they are **now** by continuing their last measured motion. It still uses only nearby drones, with separation, alignment and cohesion. No leader or central traffic scheduler is introduced.

## What we learned

|Milestone|Result|View it|
|---|---|---|
|22 — development|The saved100ms failure completes with prediction. At200ms prediction instead creates a contact failure. One planned trajectory comparison fails.|[Development replay](milestone-22-lab.html)|
|23 — fresh flocks|At100ms, the original completes{stats['raw']}/12 whole-flock runs; prediction completes{stats['predict']}/12. The same frozen rule is used on six new starting flocks and two courses.|[Fresh-flock replay](milestone-23-lab.html)|

Prediction changes failure into success in: **{fmt(helped)}**. It changes success into failure in: **{fmt(hurt)}**. These matched cases are more informative than one attractive animation. They do not establish general superiority.

The two panels always use the **same observation delay**. Select a case and click **Contact moment** to inspect a stop; **Outcome ·60s** shows the completed mission alongside any frozen failure. Every primary case is selectable, including unsuccessful ones.

## How much can we trust the calculations?

The six observer implementation checks pass. Seven of eight planned development refinements pass. In the exceptional recovered run, all50 finish at both steps but the final positions differ by55cm. A separate, still finer step agrees with the middle step to{a22['comparison']['difference']:.3g}m. That supports the finer calculation in this case; it does not erase the original discrepancy. Saved frames place the first1cm divergence after27s, well after the original10.17s contact time.

The fresh study passes{sum(c['passed'] for c in checks)}/{len(checks)} planned numerical comparisons. Seed1201/tight with prediction finishes at both steps, but its final positions differ by40cm, so this comparison fails. Separate raw-failure audits pass{sum(c['passed'] for c in audit)}/{len(audit)}. Numerical agreement means that repeating a calculation more finely gives the specified agreement. A contact can be numerically repeatable and still be a bad mission outcome. Passing these tests does not validate the physical model.

## Implication for the eight-step goal

We have a reproducible3D local-flocking testbed and useful counterexamples. We have **not** established reliable passage, real-flight safety, aerodynamic accuracy, large-flock browser performance or novelty. Airflow is off in these navigation experiments.

The next major priority is the physical measurement gate. The published dataset URL now returns a human-verification page; measured files have not been acquired. The [saved validation contract](research-physical-validation-gate-2026-10-12.md) explains the necessary geometry, motor-input and force-response matching. A mean air-velocity equation alone cannot tell us how much thrust a receiving drone loses.

Further navigation tweaks should not indefinitely replace the original question: **how much airflow detail is necessary, and what does it cost to compute?** Prediction by itself is an established technique, not a novelty claim.

## Records

[22 report](milestone-22-report.md) · [23 report](milestone-23-report.md) · [Every planned trial](research-block-22-23-trials.csv) · [Development audit](milestone-22-refinement-audit.json) · [Fresh failure audit](milestone-23-failure-audit.json) · [Artifact checks](research-block-22-23-artifact-checks.json) · [Viewer QA](research-block-22-23-qa.md) · [Original roadmap](research-roadmap.md) · [Full history](research-stage-log.md) · [Previous block](research-block-19-21-summary.md).
'''
(root/'research-block-22-23-summary.md').write_text(text)
# Append post-hoc audit clearly separated from the frozen primary study.
p=root/'milestone-23-report.md';p.write_text(p.read_text()+'\n## Separate post-hoc raw-failure audits\n\n'+f'{len(audit)} additional runs selected after the primary study;{sum(c["passed"] for c in audit)}/{len(audit)} comparisons pass. See [selection protocol](milestone-23-failure-audit-protocol.json), [comparisons](milestone-23-failure-audit.json) and [full audit states](milestone-23-failure-audit-runs.json). These are not part of the14 predefined refinements.\n')
p=root/'milestone-22-report.md';p.write_text(p.read_text()+'\n## Saved trajectory divergence\n\nThe2.5ms versus0.625ms saved-frame comparison first exceeds1cm at27.3s and0.1m at29.3s; peak difference0.5523m at58.3s. This locates divergence without identifying its causal controller branch. [Trace](milestone-22-refinement-trace.json).\n')
print(json.dumps({'runs':55+len(audit),'complete':stats,'helped':helped,'hurt':hurt,'numericalPass':sum(c['passed'] for c in checks)},indent=2))
