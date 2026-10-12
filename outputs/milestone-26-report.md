# Milestone 26 — full factory missions

Generated: 2026-10-12T01:10:04+00:00 (UTC).

**Status: all frozen numerical runs complete.**

The previous milestone established short-window computation cost. This block attempts full factory missions at 1,000 and 5,000 drones, adds narrower openings at 50/200, and keeps numerical sensitivity separate from passage outcomes.

## Frozen methodology

Eleven runs were specified before outcomes: two fresh 50-drone seeds in wide/narrow factories, one fresh 200-drone seed in each, one 1,000-drone and one 5,000-drone wide mission, plus two full refinements and one 20-second refinement. Primary and full refinement horizons are 180 seconds. Larger counts have only one primary seed, which is not a statistical safety demonstration.

Wide doorways are 5×4 m; narrow doorways are 3×2.5 m. Door centers, shared route, remaining 34-box factory geometry and local rules are unchanged. The 1,000/5,000 runs test only the wide geometry. Every agent retains separation, alignment, cohesion and a common route preference plus the local heuristic avoidance filter. No individual assigned path, leader or passage scheduler is added. Airflow is off and observations are ideal.

Larger groups extend their starting volume at nominal 0.75 m spacing; cross-section caps at 16×9 lattice sites. This is not fixed-volume density scaling. Completed drones continue flying after crossing x=36 m. A single contact stops the entire run; unfinished drones are not separate collisions.

Physics steps are 2.5 ms for primary runs and 1.25 ms for refinements, with 100 Hz control. Scientific samples remain every 0.1 s and swept contacts every physics step. Exact positions/quaternions stream to Float64LE files every second and at terminal contact. Viewer interpolation is purely visual and does not detect contacts. Full 17-state endpoints and selected intermediate checkpoints are retained.

Conservative obstacle broadphase skips only boxes too far away to activate the previous steering constraints. Neighbor queries avoid temporary arrays while preserving arithmetic. Exact final states, metrics and samples match milestone25 at 50/200/1,000/5,000 over fixed two-second runs. Streaming also reproduces the corresponding exact frames. These implementation checks do not validate long trajectories or real aerodynamics.

## All prescribed outcomes

|Drones|Seed|Doors|Kind|Completed|End s|Stop|Minimum connected fraction|
|---:|---:|---|---|---:|---:|---|---:|
|50|1501|wide|primary|50/50|180.0000|none|1.0000|
|50|1501|narrow|primary|50/50|180.0000|none|1.0000|
|50|1502|wide|primary|50/50|180.0000|none|1.0000|
|50|1502|narrow|primary|50/50|180.0000|none|1.0000|
|200|1501|wide|primary|200/200|180.0000|none|1.0000|
|200|1501|narrow|primary|200/200|180.0000|none|1.0000|
|1000|1501|wide|primary|0/1000|16.0200|obstacle contact envelope|1.0000|
|5000|1501|wide|primary|0/5000|11.9525|obstacle contact envelope|1.0000|
|200|1501|narrow|refinement|200/200|180.0000|none|1.0000|
|1000|1501|wide|refinement|0/1000|16.0188|obstacle contact envelope|1.0000|
|5000|1501|wide|window-refinement|0/5000|11.9512|obstacle contact envelope|1.0000|

The 20-second case is explicitly a window refinement, not a completed factory mission. Local connectivity is measured through chains of neighbors within 1.8 m; separation samples are capped at that radius. Contact detection uses a 0.075 m body sphere and straight segments between physics samples, not resolved rotor geometry.

## Numerical sensitivity

|Case|Scope|Maximum endpoint difference m|Ends s|Pass|
|---|---|---:|---|---|
|refinement-1501-200-narrow-0.00125|full mission|0.054454193543712635|[180, 180]|False|
|refinement-1501-1000-wide-0.00125|full mission|0.0010669079015199153|[16.02, 16.01875]|True|
|window-refinement-1501-5000-wide-0.00125|coarse mission has no20s checkpoint|—|—|False|

Full comparisons require identical completion/stop outcomes, end-time difference below 0.01 s and maximum final position difference below 0.01 m. A 5,000-drone comparison at 20 seconds cannot validate the later trajectory. When stop times differ, endpoint positions are not time-synchronized. The joint comparison permits a stop-time difference below0.01s; that tolerance does not validate the intervening path.

### Available comparisons and early-stop supplement

|Case|Scope|Endpoint difference m|Event identity agrees|Joint thresholds met|
|---|---|---:|---|---|
|refinement-1501-200-narrow-0.00125|available prescribed full-mission comparison|0.054454194|True|False|
|refinement-1501-1000-wide-0.00125|available prescribed full-mission comparison|0.0010669079|True|True|
|window-refinement-1501-5000-wide-0.00125|supplemental early-stop description; original missing20s checkpoint result retained|0.0010841997|True|True|

The200-drone narrow case completes at both steps but fails the1cm endpoint threshold. The1,000-drone failure is reproduced closely. Any early-stop5,000 supplement is descriptive and does not replace the original20s-checkpoint criterion. See [supplement plan](milestone-26-supplement-plan.json) and [comparison details](milestone-26-available-comparisons.json).

## Contact-state diagnostic

At the saved1,000-drone contact state, recomputing the heuristic velocity filter leaves an obstacle-normal constraint deficit of about0.199m/s. This witnesses an unsatisfied heuristic inequality at that state. It is not the exact preceding controller command, a proof that the constraints are infeasible, or a full causal reconstruction. [1,000-drone diagnostic](milestone-26-contact-diagnostic.json). At the saved5,000-drone contact state, the recomputed command still points toward the wall and leaves a0.339m/s normal-constraint deficit with65 neighbors. This has the same post-hoc limitations; it is not a reconstruction of the preceding control update. [5,000-drone diagnostic](milestone-26-contact-diagnostic-5000.json).

## Cost and limitations

Three numerical child processes run concurrently; wall times include recording and are descriptive mission execution times, not isolated performance measurements. Milestone25 is the separate serial benchmark of the earlier equivalent implementation. Verification timings for the small optimization are not a repeated performance benchmark.

These experiments cannot establish measured aerodynamic accuracy, real-flight safety, robustness to delay/noise, or general industrial navigation. Only one primary seed is used at each large count. Full failures, unfinished counts, connectivity losses and numerical counterexamples must remain visible. The subsequent [aerodynamic comparison contract](research-aerodynamic-comparison-contract.md) separates exploratory assumptions from independent physical validation.

## Records

[3D replay](milestone-26-lab.html) · [Frozen protocol](milestone-26-protocol.json) · [Completed-run records](milestone-26-progress.json) · [Equivalence checks](milestone-26-verification.json) · [Geometry/callback checks](milestone-26-course-verification.json) · [QA](milestone-26-qa.md) · [Active goal](research-complex-environment-goal.md). Run JSON, Float64LE replays and checkpoints are in `milestone-26-source/`; progress files record simulation time while a job is live. A progress file alone is not proof that its process is still running.
