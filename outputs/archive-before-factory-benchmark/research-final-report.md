# Research status — a working local flock with unresolved validation

## Goal and methodology

Determine how much aerodynamic detail is needed to predict a drone flock moving through restricted space, and whether the actual calculation can run interactively in a browser. The original eight-step plan remains in force.

The current testbed uses 50 rigid bodies with motor and attitude dynamics, local 3D Boids, known-map guidance and a local velocity-command filter. We compare matched starting conditions, retain failures and refine the physics step at fixed 100 Hz control. Three.js replays trajectories computed offline in Node; it does not demonstrate live browser physics or GPU performance.

## Latest results

Checkpoints 22–23 completed 56 numerical runs, including separately identified post-hoc audits. The new observer extrapolates locally visible delayed positions using their measured velocities. No global trajectory assignment or passage scheduler is introduced.

At 100 ms delay it recovers the development failure, with all 50 drones finishing at both tested steps. Nevertheless, that case fails the planned endpoint agreement criterion with a 55 cm discrepancy. A separate finer-step audit agrees with the middle step to 2.9e-8 m. At 200 ms prediction causes contact while raw observations finish.

On six untouched seeds and two courses at 100 ms delay, raw observations complete 11/12 whole-flock runs and prediction completes 11/12. Individual matched cases show both benefit and harm. 13/14 planned fresh-study numerical comparisons pass;1/1 separate raw-failure audits pass. The failed fresh comparison is seed 1201/tight with prediction: all 50 finish at both steps, but final positions differ by 0.401 m. Exact source, states and failures remain saved.

## Conclusion and implications

Local prediction is not a validated general replacement. This is useful negative evidence against treating a plausible adjustment as a reliable solution. Contact in these runs means crossing a conservative 15 cm center-distance envelope; it is not a resolved physical rotor collision. Earlier collision, fragmentation and numerical counterexamples remain part of the record.

The original research remains incomplete. Airflow is off in the latest flock trials. No independent flight/receiver-force validation, coupled multi-wake accuracy, current Boids-plus-wake GPU scaling or scientific novelty has been established. Prediction and Boids are established techniques.

The priority is now the physical measurement gate, not an indefinite sequence of navigation tweaks. The published raw dataset resolves to a human-verification page, and the browser attempt times out. Paper-reported observations can guide model design, but cannot substitute for acquired, versioned validation data. The [validation contract](research-physical-validation-gate-2026-10-12.md) separates geometry, motor-input conditions, wake velocity and receiving-vehicle forces.

## Records

[Plain-language summary](research-block-22-23-summary.md) · [Current 3D replay](research-results.html) · [Eight-step roadmap](research-roadmap.md) · [Stage history](research-stage-log.md) · [Physical validation gate](research-physical-validation-gate-2026-10-12.md) · [QA](research-block-22-23-qa.md) · [Manifest](research-manifest.json) · [Reproduction helper](research-reproduce.py).

Previous assessment: [archive-before-prediction-block](archive-before-prediction-block/research-final-report.md).
