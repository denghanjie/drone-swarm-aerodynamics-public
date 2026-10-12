# Research status — a working local flock with unresolved validation

## Goal and methodology

Determine how much aerodynamic detail is needed to predict a drone flock moving through restricted space, and whether the actual calculation can run interactively in a browser. The original eight-step plan remains in force.

The current factory testbed uses 50/200 rigid bodies with motor and attitude dynamics, local 3D Boids, known-map guidance and a local velocity-command filter. We compare matched starting conditions, retain failures and refine the physics step at fixed 100 Hz control. Three.js replays trajectories computed offline in Node; it does not demonstrate live browser physics or GPU performance.

## Latest results

[Milestone 25](milestone-25-report.md) completed a finer 200-drone audit (1.016 mm agreement with 2.5 ms) and actual local-flock serial timing up to 5,000. Median calculation cost for two simulated seconds: 0.686/2.877/18.164/104.863 wall seconds at 50/200/1,000/5,000 drones. All short windows complete without contact; none establishes full larger-flock navigation. Steering is the dominant cost. The [new 3D viewer](milestone-25-lab.html) separately measures replay rendering, with raw observations saved.

The [active complex-environment goal](research-complex-environment-goal.md) now has a factory benchmark with 34 solid boxes, three offset doorways, changing route heights and local 3D Boids. Milestone 24 completed all 16 planned runs. All three full-Boids seeds finished at both 50 and 200 drones; the social ablations also finished. Three of four numerical refinements passed: the 200-drone seed 1302 endpoint discrepancy was 2.728 cm against a 1 cm threshold despite identical completion. This failed comparison remains unresolved. [Full results](milestone-24-report.md) and [exact 3D replays](milestone-24-lab.html) preserve all outcomes. Shared map guidance and local avoidance are retained in every ablation, so course completion alone cannot establish a Boids advantage.

### Previous observer block

Checkpoints 22–23 completed 56 numerical runs, including separately identified post-hoc audits. The new observer extrapolates locally visible delayed positions using their measured velocities. No global trajectory assignment or passage scheduler is introduced.

At 100 ms delay it recovers the development failure, with all 50 drones finishing at both tested steps. Nevertheless, that case fails the planned endpoint agreement criterion with a 55 cm discrepancy. A separate finer-step audit agrees with the middle step to 2.9e-8 m. At 200 ms prediction causes contact while raw observations finish.

On six untouched seeds and two courses at 100 ms delay, raw observations complete 11/12 whole-flock runs and prediction completes 11/12. Individual matched cases show both benefit and harm. 13/14 planned fresh-study numerical comparisons pass;1/1 separate raw-failure audits pass. The failed fresh comparison is seed 1201/tight with prediction: all 50 finish at both steps, but final positions differ by 0.401 m. Exact source, states and failures remain saved.

## Conclusion and implications

Local prediction is not a validated general replacement. This is useful negative evidence against treating a plausible adjustment as a reliable solution. Contact in these runs means crossing a conservative 15 cm center-distance envelope; it is not a resolved physical rotor collision. Earlier collision, fragmentation and numerical counterexamples remain part of the record.

The original research remains incomplete. Airflow is off in the latest flock trials. No independent flight/receiver-force validation, coupled multi-wake accuracy, current Boids-plus-wake GPU scaling or scientific novelty has been established. Prediction and Boids are established techniques.

The active goal now prioritizes complex-environment evidence and actual flock scaling while keeping the physical measurement gate open. The published raw dataset resolves to a human-verification page, and the browser attempt times out. Paper-reported observations can guide model design, but cannot substitute for acquired, versioned validation data. The [validation contract](research-physical-validation-gate-2026-10-12.md) separates geometry, motor-input conditions, wake velocity and receiving-vehicle forces.

## Records

[Plain-language summary](research-block-22-23-summary.md) · [Current 3D replay](research-results.html) · [Eight-step roadmap](research-roadmap.md) · [Stage history](research-stage-log.md) · [Physical validation gate](research-physical-validation-gate-2026-10-12.md) · [QA](research-block-22-23-qa.md) · [Manifest](research-manifest.json) · [Reproduction helper](research-reproduce.py).

Previous assessment: [archive-before-prediction-block](archive-before-prediction-block/research-final-report.md).
