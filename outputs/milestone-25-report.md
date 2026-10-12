# Milestone 25 — actual flock cost and numerical audit

## Purpose

Measure the complete current local-Boids pipeline from 50 to 5,000 bodies, and investigate the retained 200-drone numerical discrepancy. Separate offline dynamics cost, browser replay cost and mission evidence.

## Frozen method

One post-hoc 120 s refinement of seed 1302 / 200 drones at 1.25 ms, followed by three serial timing repeats at each count: 50, 200, 1,000 and 5,000. Each timing run starts in a fresh Node process, performs a 0.1 s same-count warmup, then measures 2 s at a 5 ms physics step. Count order rotates across repeats. The short warmup does not guarantee steady-state JIT or garbage-collection behavior. These repeats use the same initial condition and measure runtime variability, not independent navigation evidence.

The numerical source matches milestone 24 except for an initialization timing field. Local steering uses the deterministic spatial grid, full rigid-body RK4 and swept contact checks. No passage scheduler or assigned paths are introduced. Airflow is off; observations are ideal.

At 0.75 m nominal lattice spacing, larger groups occupy greater initial volume; the cross-section caps at 16×9 sites and grows longitudinally thereafter. Initial density is roughly maintained, but boundary fraction and shape change. This is not a fixed-volume density test. The two-second windows are near the start, before the front reaches the first partition. They cannot establish cost in a later congested passage or successful factory completion.

## Numerical audit

The post-hoc 2.5 → 1.25 ms comparison has a maximum final position difference of **0.0010159245 m**. Finish counts: [200, 200]. Stops: [None, None]. It **passes** the prescribed joint comparison. Initial states identical: True.

The original 5 → 2.5 ms failure (2.728 cm against a 1 cm threshold) remains in milestone 24. Agreement at finer steps, if achieved, is numerical evidence for that case only; it does not establish physical accuracy or robustness for other initial conditions.

## Serial dynamics timing

|Drones|Median total ms per 2 simulated seconds|Range ms|Simulated seconds / wall second|Reached 2 s without stop|
|---:|---:|---|---:|---|
|50|685.6|659.5–693.0|2.917|True|
|200|2876.6|2850.8–2943.7|0.695|True|
|1000|18163.9|17414.8–18652.8|0.110|True|
|5000|104863.4|103276.6–105268.6|0.019|True|

A ratio below 1 means slower than real time in this Node benchmark. Total includes initialization, steering, physics, contact checks, measurements and recording; it excludes process startup, warmup, external JSON serialization, browser rendering and file transfer. Background OS load is uncontrolled. These figures are measurements of this machine/session, not hardware-independent complexity bounds.

|Drones|Initialization ms|Steering ms|Physics ms|Contact checks ms|Measurements/recording ms|
|---:|---:|---:|---:|---:|---:|
|50|0.2|456.0|147.7|40.9|36.9|
|200|0.5|2147.5|424.0|137.4|173.2|
|1000|1.9|14422.5|1885.9|674.7|1177.6|
|5000|6.4|86409.4|8378.7|3013.6|7010.0|

|Drones|Final mean local neighbors|Neighbor visits during steering|
|---:|---:|---:|
|50|25.32|236092|
|200|46.29|1599582|
|1000|62.48|9902214|
|5000|72.87|57837242|

Runtime environment: withheld in this public export. Browser tabs and other OS work were not globally disabled; serial means no overlapping numerical study jobs.

Stage medians are independent medians and need not sum to median total. Total also includes loop/bookkeeping overhead. Spatial hashing reduces distant-neighbor searches; dense local neighborhoods can still be expensive.

## Browser replay cost

The Three.js viewer includes an explicit 240-frame measurement after 30 warmup frames. It loops saved motion, turns trails off and fixes the overview camera. Frame intervals include browser scheduling. CPU update time covers interpolation, instance matrices, UI and trail cleanup; render submission is the CPU duration of the Three.js render call. Neither measures GPU completion. Browser/OS load and viewport affect these values. Saved observations are in `milestone-25-rendering.json` when browser QA is complete.

## Conclusion and next evidence

This milestone demonstrates execution of the actual local-Boids pipeline at 1,000 and 5,000 bodies for short initial windows. It does not demonstrate a completed large-flock factory mission, live browser physics, GPU physics, aerodynamic accuracy or a scientific novelty claim. The next mission block must retain failures and assess navigation, connectivity and numerical sensitivity over the full course, then compare labeled aerodynamic approximations.

## Records

[3D replay and rendering measurement](milestone-25-lab.html) · [Frozen protocol](milestone-25-protocol.json) · [All results](milestone-25-summary.json) · [Scaling table](milestone-25-scaling.json) · [Numerical audit](milestone-25-audit.json) · [QA](milestone-25-qa.md) · [Active goal](research-complex-environment-goal.md). Full states and exact replay frames remain in `milestone-25-source/*.json`.

Reproduction: `python3 research-reproduce.py --stage 25 --node /path/to/node` runs in a copied output tree.

## Observed browser replay measurements

One measurement per count in the visible document at 1280×800, device pixel ratio 2 (canvas backing size 2464×1180). Timing is session-specific; no GPU execution measurement or browser physics occurs.

|Drones|Median frame interval ms|95th percentile interval ms|Median scene-update CPU ms|Median render-submission CPU ms|
|---:|---:|---:|---:|---:|
|50|16.70|17.40|0.30|0.50|
|200|16.70|17.60|0.50|0.40|
|1000|16.70|17.10|1.40|0.40|
|5000|16.70|17.30|5.40|0.40|

Frame intervals near 16.7 ms are consistent with the display cadence in this session, not proof of excess GPU capacity. Local replay performance must not be conflated with the much larger offline simulation cost. [Rendering protocol](milestone-25-render-protocol.json) · [Raw rendering measurements](milestone-25-rendering.json).
