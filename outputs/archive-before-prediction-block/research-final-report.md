# Research status — a working local flock with unresolved validation

## Goal and methodology

Determine how much aerodynamic detail is needed to predict a drone flock moving through restricted space, and whether the actual calculation can run interactively in a browser. The original eight-step plan remains in force.

The current experiment uses 50 rigid bodies with motor and attitude dynamics, genuine local 3D Boids, known-map guidance and a local velocity-command filter. We compare matched starting conditions, retain failed cases, refine the physics step at a fixed 100 Hz control rate, and distinguish mission success from software verification and physical validity. Three.js displays recorded trajectories computed offline in Node.

## Latest results

Checkpoints 19–21 completed 81 numerical runs, including two exact replay regenerations. A simultaneous soft filter and three heading/centering variants were rejected: they worsened passage and mostly failed trajectory refinement. The prior inward-guidance controller remains a provisional reference.

In 24 fresh matched delay trials, all eight 0 ms and all eight 50 ms cases finished every drone. Seven of eight 100 ms cases finished; one reached the drone-to-drone contact envelope at 10.1725 s. A post-hoc refinement reproduced that stop at the same time; its no-delay counterpart completed 50/50. Earlier collision, fragmentation and numerical counterexamples remain preserved.

8/8 preregistered delay-study refinements passed the endpoint/count/stop criteria; both separate failure-audit refinements passed. These numerical results do not establish real-flight accuracy or safety.

## Conclusion and implications

A genuine three-dimensional flock can be implemented and studied reproducibly. This block strengthens the evidence about its limitations; it does not solve reliable narrow-passage navigation. A local controller that works with ideal observations can fail when the high-level state is stale.

The research remains exploratory. Airflow is off in the current flock runs. No independent flight or wake-force validation has been completed; no current Boids-plus-wake GPU scaling claim is supported. Smoothing, soft optimization, heading changes and delay tests are established techniques, not novelty by themselves. The original aerodynamic accuracy-versus-cost question is still open.

The next gates are delay-aware local control on retained and fresh cases, an independent aerodynamic reference with matched geometry, and controlled CPU/GPU comparisons of the actual integrated flock pipeline. A visually convincing replay and an internally consistent equation are insufficient physical validation.

## Records

[Consolidated explanation](research-block-19-21-summary.md) · [Current 3D viewer](research-results.html) · [Eight-step roadmap](research-roadmap.md) · [Stage history](research-stage-log.md) · [Physical-reference update](research-aerodynamics-update-2026-10-11.md) · [QA](research-block-19-21-qa.md) · [Manifest](research-manifest.json) · [Isolated reproduction helper](research-reproduce.py).

The previous assessment is preserved in [archive-before-optimization-block](archive-before-optimization-block/research-final-report.md).
