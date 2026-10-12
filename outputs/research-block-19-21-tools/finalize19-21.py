from pathlib import Path
import json,csv,re
O=Path('outputs')
refs=json.loads((O/'milestone-21-comparisons.json').read_text());passed=sum(q['passed'] for q in refs)
summary=f'''# Research block19–21 — better evidence, no claimed breakthrough

**The previous controller remains an experimental reference. The new alternatives were worse, and delayed information exposed a repeatable proximity failure.**

We completed81 numerical runs across three checkpoints, including two exact replay regenerations. Every checkpoint has source, a frozen protocol, full final states, measurements, a plain-language report and a Three.js replay. Earlier failures remain available.

|Milestone|Question|Result|3D replay|
|---|---|---|---|
|19|Would smoother, simultaneous braking decisions make the flock reliable?|No. The candidate completed84/150 passages at5ms versus150/150 for the previous controller. All6 candidate numerical comparisons failed.|[Compare filters](milestone-19-lab.html)|
|20|Would stronger center guidance or a fixed heading fix it?|Neither was sufficient. None of the variants completed all50 drones in any of its tested runs. Only1/18 numerical comparisons passed.|[Compare the two changes](milestone-20-lab.html)|
|21|Does the previous controller tolerate delayed observations?|All8 no-delay and all8 50ms-delay primary runs finished. At100ms,7/8 finished; the remaining run reached the contact limit. The failure repeats at the finer step.|[See the retained contact case](milestone-21-lab.html)|

## The most useful new finding

In fresh starting flock1103, a100ms delay causes two drones to cross the model's15cm center-distance limit at10.1725 seconds. At the finer simulation step, the same failure occurs at the same time. With current observations, all50 finish. That makes this a concrete controller limitation under the chosen delay model, not an animation glitch resolved by drawing more frames.

The red markers in the viewer identify the closest pair at the stop. Click **Contact moment** to inspect it, then **Outcome ·60s** to see the no-delay flock finish while the failed simulation stays stopped. Other examples retain successful passage through the changing-height obstacle course.

## What passed, and what did not

The optimization, delay scheduling, frozen-source checks and replay checks pass their software tests. The unsuccessful controller variants fail the research acceptance tests and are rejected. Checkpoint21 passes{passed}/8 preregistered numerical refinements. Its separate post-hoc audit passes both the no-delay and delayed-case refinements and reproduces both replays exactly. A numerical pass means the tested calculation agrees; it does not mean the mission succeeds or the physical model is validated.

These are local3D Boids throughout: separation, alignment and cohesion use nearby drones. The map and route preferences are supplied. No central scheduler assigns passage slots. The viewer replays saved rigid-body motion computed in Node; it does not demonstrate live browser physics or GPU performance.

## Implications for the original goal

The original question is still how much aerodynamic detail is needed, and whether the actual flock calculation can run interactively in a browser. These checkpoints remain within Step5 of the eight-step plan. Airflow is still off. Independent flight/force validation, coupled multi-wake accuracy, actual Boids GPU scaling and scientific novelty remain unresolved.

A newer measured-wake preprint has been added to the [physical-reference update](research-aerodynamics-update-2026-10-11.md). The preferred raw interaction dataset could not be retrieved in this session. The new paper's vehicle geometry differs from ours; its equations and dimensions must not be silently substituted and called validation.

The next useful work is a local delay-aware controller tested against the retained failure and untouched new cases, alongside obtaining an independent aerodynamic reference. Further visual polish or a bigger drone count would not by itself answer the research question.

## Records

[19 report](milestone-19-report.md) · [20 report](milestone-20-report.md) · [21 report](milestone-21-report.md) · [Numerical failure audit](milestone-21-failure-audit.json) · [Trial table](research-block-19-21-trials.csv) · [Software/viewer QA](research-block-19-21-qa.md) · [Original roadmap](research-roadmap.md) · [Full stage history](research-stage-log.md) · [Previous research block](research-block-15-18-summary.md).
'''
# Make prose spacing readable without altering filenames or code identifiers.
for a,b in {'block19':'block 19','completed81':'completed 81','completed84':'completed 84','versus150':'versus 150','at5ms':'at 5 ms','All6':'All 6','Only1/18':'Only 1/18','all50':'all 50','all8':'all 8','All8':'All 8','50ms-delay':'50 ms delay','At100ms':'At 100 ms','flock1103':'flock 1103','a100ms':'a 100 ms',"model\'s15cm":"model's 15 cm",'at10.1725':'at 10.1725','·60s':'· 60 s','Checkpoint21':'Checkpoint 21',f'passes{passed}/8':f'passes {passed}/8','local3D':'local 3D','Step5':'Step 5'}.items():summary=summary.replace(a,b)
(O/'research-block-19-21-summary.md').write_text(summary)
rows=[]
for stage in [19,20,21]:
 for r in json.loads((O/f'milestone-{stage}-study.json').read_text()):rows.append((str(stage),r))
for r in json.loads((O/'milestone-21-failure-audit-runs.json').read_text()):rows.append(('21-post-hoc',r))
with (O/'research-block-19-21-trials.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['checkpoint','seed','course','controller','physics_dt_s','observation_delay_s','completed','stop_reason','end_s','minimum_center_distance_m','minimum_obstacle_envelope_clearance_m','minimum_sampled_connected_drones','final_connected_drones','max_solver_gradient_residual'])
 for stage,r in rows:
  c,m=r['config'],r['metrics'];w.writerow([stage,c['seed'],c['scenario'],c['mode'],c['dt'],c.get('observationDelay',0),m['passed'],m['stopReason'] or '',m['end'],m['minimum'],m['obstacleMinimum'],round(50*min(s['largestFraction'] for s in r['samples'])),round(50*m['final']['largestFraction']),m.get('maxSolverResidual',0)])
report='''# Research status — a working local flock with unresolved validation

## Goal and methodology

Determine how much aerodynamic detail is needed to predict a drone flock moving through restricted space, and whether the actual calculation can run interactively in a browser. The original eight-step plan remains in force.

The current experiment uses50 rigid bodies with motor and attitude dynamics, genuine local3D Boids, known-map guidance and a local velocity-command filter. We compare matched starting conditions, retain failed cases, refine the physics step at a fixed100Hz control rate, and distinguish mission success from software verification and physical validity. Three.js displays recorded trajectories computed offline in Node.

## Latest results

Checkpoints19–21 completed81 numerical runs, including two exact replay regenerations. A simultaneous soft filter and three heading/centering variants were rejected: they worsened passage and mostly failed trajectory refinement. The prior inward-guidance controller remains a provisional reference.

In24 fresh matched delay trials, all eight0ms and all eight50ms cases finished every drone. Seven of eight100ms cases finished; one reached the drone-to-drone contact envelope at10.1725s. A post-hoc refinement reproduced that stop at the same time; its no-delay counterpart completed50/50. Earlier collision, fragmentation and numerical counterexamples remain preserved.

NUMERICAL

## Conclusion and implications

A genuine three-dimensional flock can be implemented and studied reproducibly. This block strengthens the evidence about its limitations; it does not solve reliable narrow-passage navigation. A local controller that works with ideal observations can fail when the high-level state is stale.

The research remains exploratory. Airflow is off in the current flock runs. No independent flight or wake-force validation has been completed; no current Boids-plus-wake GPU scaling claim is supported. Smoothing, soft optimization, heading changes and delay tests are established techniques, not novelty by themselves. The original aerodynamic accuracy-versus-cost question is still open.

The next gates are delay-aware local control on retained and fresh cases, an independent aerodynamic reference with matched geometry, and controlled CPU/GPU comparisons of the actual integrated flock pipeline. A visually convincing replay and an internally consistent equation are insufficient physical validation.

## Records

[Consolidated explanation](research-block-19-21-summary.md) · [Current3D viewer](research-results.html) · [Eight-step roadmap](research-roadmap.md) · [Stage history](research-stage-log.md) · [Physical-reference update](research-aerodynamics-update-2026-10-11.md) · [QA](research-block-19-21-qa.md) · [Manifest](research-manifest.json) · [Isolated reproduction helper](research-reproduce.py).

The previous assessment is preserved in[archive-before-optimization-block](archive-before-optimization-block/research-final-report.md).
'''.replace('NUMERICAL',f'{passed}/8 preregistered delay-study refinements passed the endpoint/count/stop criteria; both separate failure-audit refinements passed. These numerical results do not establish real-flight accuracy or safety.')
for a,b in {'uses50':'uses 50','local3D':'local 3D','fixed100Hz':'fixed 100 Hz','Checkpoints19':'Checkpoints 19','completed81':'completed 81','In24':'In 24','eight0ms':'eight 0 ms','eight50ms':'eight 50 ms','eight100ms':'eight 100 ms','at10.1725s':'at 10.1725 s','completed50':'completed 50','Current3D':'Current 3D','in[archive':'in [archive'}.items():report=report.replace(a,b)
(O/'research-final-report.md').write_text(report)
p=O/'research-roadmap.md';s=p.read_text();s=s.replace('Checkpoints 15–18 are a larger block','Checkpoints 19–21 are the latest larger block');s=re.sub(r'\|5\. Test a real local flock\|.*', '|5. Test a real local flock|Run about 50 drones through restricted geometry.|Local 3D Boids and multi-obstacle courses exist. The new soft filters are rejected. A fresh 100 ms observation-delay contact failure is reproduced at a finer step. Reliable passage and connectivity remain unresolved. Airflow is off.|',s)
a=s.index('## Current research block');b=s.index('## Next research gates',a)
s=s[:a]+'''## Current research block

- [19 — simultaneous soft filtering](milestone-19-report.md): verified local solver, unsuccessful flock controller.
- [20 — heading and center-guidance diagnosis](milestone-20-report.md): neither treatment is a sufficient fix.
- [21 — fresh observation-delay trials](milestone-21-report.md): retained, numerically reproduced contact failure.

[Consolidated explanation](research-block-19-21-summary.md) · [Current3D viewer](research-results.html) · [Prior block15–18](research-block-15-18-summary.md) · [Complete history](research-stage-log.md)

'''+s[b:]
s=s.replace('1. Keep the smoother controller and the inward-offset alternative as separate frozen candidates. Test observation delays/errors and limited sensing on matched cases; distinguish passage, contact and connectivity. Do not silently replace local flocking with scheduled traffic.','1. Keep checkpoint18 inward guidance as a provisional reference and retain every failed alternative. Test a local delay-aware rule against the reproduced1103 counterexample and untouched new seeds. Add observation errors/limited sensing only with explicit models. Measure passage, contact and connectivity separately; preserve local flocking.')
(O/'research-roadmap.md').write_text(s)
