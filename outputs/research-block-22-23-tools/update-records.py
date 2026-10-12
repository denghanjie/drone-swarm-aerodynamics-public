from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
x=json.loads((root/'milestone-23-summary.json').read_text());coarse=[r for r in x if r['config']['dt']==.0025];cp=json.loads((root/'milestone-23-comparisons.json').read_text());audit=json.loads((root/'milestone-23-failure-audit.json').read_text());n=55+len(audit)
s={e:sum(r['metrics']['passed']==50 and not r['metrics']['stopReason'] for r in coarse if r['config']['estimator']==e) for e in ['raw','predict']}
p=root/'research-roadmap.md';t=p.read_text().replace('Checkpoints 19–21 are the latest larger block','Checkpoints 22–23 are the latest larger block');t=t.replace('The new soft filters are rejected. A fresh 100 ms observation-delay contact failure is reproduced at a finer step.','Soft filters remain rejected. Local position prediction recovers some delayed-observation failures and introduces others; a numerical counterexample is retained.')
a=t.index('## Current research block');b=t.index('## Next research gates',a)
t=t[:a]+'''## Current research block

- [22 — local prediction](milestone-22-report.md): recovery, a200ms counterexample and a retained trajectory-refinement failure.
- [23 — fresh flocks](milestone-23-report.md): six new seeds in two courses, with the controller frozen before testing. Prediction helps some cases and hurts others.

[Consolidated explanation](research-block-22-23-summary.md) · [Current3D viewer](research-results.html) · [Prior block19–21](research-block-19-21-summary.md) · [Complete history](research-stage-log.md)

'''+t[b:]
a=t.index('1. Keep checkpoint');b=t.index('\n2. ',a)
t=t[:a]+'1. Keep raw observations and local prediction as separate experimental baselines, with all counterexamples retained. Do not promote prediction as a universal fix. Navigation work remains within Step5; completion, contact and connectivity require separate reporting.'+t[b:]
t=t.replace('Obtain a physical force/wake reference matched to vehicle geometry and operating conditions.','Prioritize the [physical measurement gate](research-physical-validation-gate-2026-10-12.md): obtain a force/wake reference matched to vehicle geometry, measurement plane and motor operating conditions. The data repository currently returns human verification; its observations have not been acquired.')
p.write_text(t)
report=f'''# Research status — a working local flock with unresolved validation

## Goal and methodology

Determine how much aerodynamic detail is needed to predict a drone flock moving through restricted space, and whether the actual calculation can run interactively in a browser. The original eight-step plan remains in force.

The current testbed uses50 rigid bodies with motor and attitude dynamics, local3D Boids, known-map guidance and a local velocity-command filter. We compare matched starting conditions, retain failures and refine the physics step at fixed100Hz control. Three.js replays trajectories computed offline in Node; it does not demonstrate live browser physics or GPU performance.

## Latest results

Checkpoints22–23 completed{n} numerical runs, including separately identified post-hoc audits. The new observer extrapolates locally visible delayed positions using their measured velocities. No global trajectory assignment or passage scheduler is introduced.

At100ms delay it recovers the development failure, with all50 drones finishing at both tested steps. Nevertheless, that case fails the planned endpoint agreement criterion with a55cm discrepancy. A separate finer-step audit agrees with the middle step to2.9e-8m. At200ms prediction causes contact while raw observations finish.

On six untouched seeds and two courses at100ms delay, raw observations complete{s['raw']}/12 whole-flock runs and prediction completes{s['predict']}/12. Individual matched cases show both benefit and harm. {sum(c['passed'] for c in cp)}/14 planned fresh-study numerical comparisons pass;{sum(c['passed'] for c in audit)}/{len(audit)} separate raw-failure audits pass. The failed fresh comparison is seed1201/tight with prediction: all50 finish at both steps, but final positions differ by0.401m. Exact source, states and failures remain saved.

## Conclusion and implications

Local prediction is not a validated general replacement. This is useful negative evidence against treating a plausible adjustment as a reliable solution. Contact in these runs means crossing a conservative15cm center-distance envelope; it is not a resolved physical rotor collision. Earlier collision, fragmentation and numerical counterexamples remain part of the record.

The original research remains incomplete. Airflow is off in the latest flock trials. No independent flight/receiver-force validation, coupled multi-wake accuracy, current Boids-plus-wake GPU scaling or scientific novelty has been established. Prediction and Boids are established techniques.

The priority is now the physical measurement gate, not an indefinite sequence of navigation tweaks. The published raw dataset resolves to a human-verification page, and the browser attempt times out. Paper-reported observations can guide model design, but cannot substitute for acquired, versioned validation data. The [validation contract](research-physical-validation-gate-2026-10-12.md) separates geometry, motor-input conditions, wake velocity and receiving-vehicle forces.

## Records

[Plain-language summary](research-block-22-23-summary.md) · [Current3D replay](research-results.html) · [Eight-step roadmap](research-roadmap.md) · [Stage history](research-stage-log.md) · [Physical validation gate](research-physical-validation-gate-2026-10-12.md) · [QA](research-block-22-23-qa.md) · [Manifest](research-manifest.json) · [Reproduction helper](research-reproduce.py).

Previous assessment: [archive-before-prediction-block](archive-before-prediction-block/research-final-report.md).
'''
(root/'research-final-report.md').write_text(report)
p=root/'research-stage-log.md';t=p.read_text();marker='\n## Research block22–23 — 12 October2026\n';t=t.split(marker)[0]
t+=marker+f'''
**{n} runs retained.** Checkpoint22 tests local constant-velocity position prediction in16 development runs. All three100ms predicted cases finish, but1103 fails the planned final-position comparison; a separate0.625ms audit agrees with1.25ms. A200ms prediction contact occurs where raw observations finish. Seven of eight planned refinements pass. [Report](milestone-22-report.md) · [3D replay](milestone-22-lab.html).

Checkpoint23 freezes the same source before six fresh seeds across tight/slalom courses at100ms:24 primary runs and14 planned refinements. Raw{s['raw']}/12 and prediction{s['predict']}/12 complete flocks. {sum(c['passed'] for c in cp)}/14 planned comparisons pass. Another{len(audit)} post-hoc raw-stop refinements are saved separately, with{sum(c['passed'] for c in audit)}/{len(audit)} passing. [Report](milestone-23-report.md) · [3D replay](milestone-23-lab.html).

Decision: retain both observer variants as experimental; no universal promotion. Return research priority to the physical measurement gate. Direct dataset retrieval yields human verification, not raw observations. No physical-validation, novel-algorithm or browser-scaling claim is made.

[Block summary](research-block-22-23-summary.md) · [Trial table](research-block-22-23-trials.csv) · [QA](research-block-22-23-qa.md) · [Artifact checks](research-block-22-23-artifact-checks.json).
''';p.write_text(t)
