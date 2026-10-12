# Milestone 24 — a genuine local flock in a synthetic factory

## Goal

Move beyond spheres and a single opening. Establish a reproducible factory mission with changing heights, substantial solid geometry and local decision-making, then provide a basis for actual flock scaling.

This is the first milestone of the [active complex-environment goal](research-complex-environment-goal.md). The broader goal remains active.

## What changed

The new synthetic factory contains 34 collision-checked solid boxes: floor/ceiling/side boundaries, three thick partitions with offset 5 m ×4 m doorways, 12 storage racks, three presses, two overhead structures and a loading platform. The shared route changes horizontal position and height between halls. Its centerline is checked for clearance, but this does not guarantee passage for a finite flock.

Every drone uses the existing 27 g rigid-body/motor model. Separation, alignment and cohesion act within 1.8 m. A deterministic spatial grid finds neighbors; its commands and short trajectories match brute-force search exactly. Each drone follows a broad common route field and local velocity constraints. No scheduler, assigned trajectory, designated leader or timed passage slot is introduced.

The initial condition is a jittered volumetric lattice with shuffled IDs and random three-dimensional velocities, not preassigned flight lanes. Nominal spacing is 0.75 m. Increasing count increases initial volume; the cross-section eventually caps at16×9 sites and the cloud grows lengthwise. It is not a fixed-volume density experiment.

## Method

All 16 runs were specified before mission outcomes were inspected: three seeds × three social variants at50 drones, three full-Boids cases at200 drones, and four finer-step full-Boids runs. The common mission horizon is120 s. Coarse/fine physics steps are5/2.5 ms; control runs at100 Hz. Airflow is off and observations are ideal.

The two ablations remove social terms but retain the same map guidance and local collision-avoidance filter. Therefore “No social forces” is not an independent, noninteracting-particle model.

Drone contacts use a0.075 m radius body envelope. Box contact distances are exact for a straight segment; true curved rigid-body motion between steps is approximated by that segment. The pair-search radius is enlarged by twice the maximum displacement, so its candidate stage cannot omit a straight-segment contact. Numerical step checks remain necessary.

## Primary outcomes

|Drones|Seed|Social model|Completed|Stop|Minimum connected group|Final connected group|Min sampled separation m|
|---:|---:|---|---:|---|---:|---:|---:|
|50|1301|boids|50/50|none|50/50|50/50|0.57659|
|50|1301|goal-only|50/50|none|50/50|50/50|0.37069|
|50|1301|separation-only|50/50|none|50/50|50/50|0.54657|
|50|1302|boids|50/50|none|50/50|50/50|0.57886|
|50|1302|goal-only|50/50|none|50/50|50/50|0.37021|
|50|1302|separation-only|50/50|none|50/50|50/50|0.56172|
|50|1303|boids|50/50|none|50/50|50/50|0.57080|
|50|1303|goal-only|50/50|none|50/50|50/50|0.37625|
|50|1303|separation-only|50/50|none|50/50|50/50|0.56054|
|200|1301|boids|200/200|none|200/200|200/200|0.47475|
|200|1302|boids|200/200|none|200/200|200/200|0.48155|
|200|1303|boids|200/200|none|200/200|200/200|0.46744|

Connectedness, separation and spread are sampled every0.1 s; contact tests run every physics step. Sampled separation is capped at1.8 m: a capped value means “at least1.8 m,” not an exact larger minimum. Finishing means crossing x=36 m; completed drones continue moving to the fixed horizon. A single contact stops the entire run, so other unfinished drones must not be counted as independent collisions.

## Numerical agreement

3/4 predefined5→2.5 ms comparisons pass the joint criterion: identical finish count/stop reason, end-time difference below0.01 s and maximum final position difference below0.01 m.

|Drones|Seed|Maximum final difference m|Finish counts|Pass|
|---:|---:|---:|---|---|
|50|1301|2.2211189e-05|[50, 50]|True|
|50|1302|1.1011189e-06|[50, 50]|True|
|50|1303|5.9924193e-06|[50, 50]|True|
|200|1302|0.027280049|[200, 200]|False|

## Conclusion and next milestone

50-drone boids: 3/3 complete missions.
200-drone boids: 3/3 complete missions.
50-drone separation-only: 3/3 complete missions.
50-drone goal-only: 3/3 complete missions.

Passing the course does not by itself establish an advantage from Boids: shared map guidance and the retained avoidance filter can also organize motion. The ablations and connectedness measurements are kept to expose that distinction. This factory is a larger geometric benchmark, not a claim that it captures every difficult industrial navigation problem.

The spatial index is now part of the actual steering and contact pipeline. Initial valid, connected clouds were checked at50,200,1,000 and5,000, but initialization is not a completed navigation or performance test. This milestone only simulates50 and200. Next: isolated serial timing and progressively larger real flock missions, including failures and numerical checks. Do not reuse the old scheduled-queue benchmark as evidence.

Worker timing fields are descriptive wall times under three concurrent workers. They are not isolated performance measurements or live browser FPS. Three.js replays saved offline motion. Aerodynamic approximations, independent physical validation, GPU execution of the current pipeline,1,000/5,000 missions and novelty remain open.

## Records

[3D replay](milestone-24-lab.html) · [Frozen protocol](milestone-24-protocol.json) · [All metrics](milestone-24-summary.json) · [Full study](milestone-24-study.json) · [Geometry/grid checks](milestone-24-verification.json) · [Numerical comparisons](milestone-24-comparisons.json) · [Trial CSV](milestone-24-trials.csv) · [QA](milestone-24-qa.md). Each exact primary trajectory is in `milestone-24-source/run-*.json`.

Reproduce with `python3 research-reproduce.py --stage 24 --node /path/to/node`; source is copied before execution.
