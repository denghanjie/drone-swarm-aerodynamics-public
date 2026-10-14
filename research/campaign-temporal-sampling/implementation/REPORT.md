# Temporal airflow sampling: reference not established

## Result

The bounded campaign did not establish a usable coupled numerical reference. Both independent physics-step screens passed. Both airflow-reference screens failed the predeclared velocity, attitude and angular-rate absolute caps, despite passing the empirical reduction checks. The four planned 5/10 ms coupled rows were therefore skipped. No airflow cadence is qualified, recommended or physically validated by this study.

The separately permitted fixed-path diagnostics were completed on the already valid fine drivers. They show stale-field load error decreasing as the hold interval shortens, but they remain conditional on an unqualified driver. A small position difference alone would have missed the failed attitude and velocity gates.

## What ran, and what did not

- One historical compatibility preflight: full final17-state/held-field SHA matched exactly; 400 steps, 100 field updates, 100 controller updates.
- Ten fresh, genuine local 3D Boids coupled runs: N16, one second, seeds 840131 and 840137. No scripted trajectories or seed replacement.
- Both fine drivers retained all 6,401 full17-state endpoints at 0.15625 ms. Other fresh runs retained full states every common 0.625 ms.
- Four coupled rows were skipped by the frozen gate: air 5 and10 ms for both seeds.
- Conditional same-path diagnostics evaluated five held-inflow cadences on each saved fine driver, using two event-aware quadratures. All ten quadrature consistency screens passed; the largest stored normalized fine/coarse discrepancy was 6.1326e-8. These are not additional coupled trajectories.
- Independent reconstruction from hash-verified raw common states reproduced all four reference gates. No post-budget simulation or numerical replay was performed.

[Explicit attempted/skipped matrix](results/matrix-status.json) · [Compatibility record](results/compatibility.json) · [Raw reconstruction check](results/recomputed/verification.json)

## Reference gate failures

The entries below are maxima over all drones and common 0.625 ms endpoints for air 1.25→0.625 ms at fixed physics0.15625 ms. Caps are analyst-chosen numerical screens, not physical tolerances. Both seeds had to pass separately.

| Seed | Position (mm), cap1 | Velocity (mm/s), cap1 | Attitude (mrad), cap1 | Body angular rate (mrad/s), cap10 |
|---|---:|---:|---:|---:|
| 840131 | 0.889096 | 2.246735 | 2.438374 | 17.839376 |
| 840137 | 0.467362 | 2.134535 | 7.295006 | 72.349607 |

All four empirical reduction tests passed on each seed. The finest differences were not below all absolute caps, so reduction alone could not establish the reference. Physics refinement at fixed 0.625 ms airflow was much smaller: the largest fine-pair position difference was 2.28e-12 m and velocity difference 8.58e-12 m/s. The maximum computed attitude difference was 4.21e-8 rad, below its predeclared comparison floor. No asymptotic order or Richardson bound is inferred.

[Complete per-seed gates, coarse/fine values and worst locations](results/campaign.json)

## Conditional same-path loads

Each row uses the same current full17-state path for every hold cadence. The held data are four already-projected nonnegative scalar inflows per receiver. Loads use current endpoint motor thrust and attitude, preserve nominal yaw torque, and rotate error torque into world coordinates before angular-impulse integration. Refresh left limits and terminal old-hold values are included.

W=m·g; arm=√2·a; T=1 s. Force and torque peaks below are percentages of W and W·arm. Impulses and error-norm integrals are percentages of W·T and W·arm·T. These are observed conditional values, not cadence qualifications.

| Seed | Hold (ms) | Force peak (%) | RP torque peak (%) | Max-prefix force impulse (%) | Max-prefix world torque impulse (%) | Force-error norm integral (%) | Torque-error norm integral (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 840131 | 10 | 2.903663 | 1.355770 | 0.092590 | 0.051792 | 0.239376 | 0.104981 |
| 840131 | 5 | 1.453998 | 0.696514 | 0.046288 | 0.025972 | 0.119701 | 0.052557 |
| 840131 | 2.5 | 0.729826 | 0.349052 | 0.023149 | 0.013003 | 0.059853 | 0.026288 |
| 840131 | 1.25 | 0.365116 | 0.174796 | 0.011575 | 0.006506 | 0.029929 | 0.013146 |
| 840131 | 0.625 | 0.182548 | 0.087404 | 0.005788 | 0.003254 | 0.014965 | 0.006573 |
| 840137 | 10 | 2.895094 | 1.793277 | 0.079024 | 0.038492 | 0.241771 | 0.087143 |
| 840137 | 5 | 1.448851 | 0.911870 | 0.039433 | 0.019256 | 0.121058 | 0.043604 |
| 840137 | 2.5 | 0.728777 | 0.457200 | 0.019696 | 0.009631 | 0.060538 | 0.021816 |
| 840137 | 1.25 | 0.364817 | 0.228883 | 0.009843 | 0.004818 | 0.030273 | 0.010909 |
| 840137 | 0.625 | 0.182436 | 0.114439 | 0.004920 | 0.002409 | 0.015137 | 0.005455 |

The frozen conditional error limits were 1% for each sampled peak and 0.1% for each impulse/error-norm integral. The raw records preserve every comparison, per-drone RMS, vector-prefix quadrature disagreement, worst drone/tick/side, rotor-inflow errors and elapsed-hold-age diagnostics. At 10 ms, the signed-prefix impulse values remain below their limits while error-norm integrals exceed limits, showing why cancellation-resistant metrics were retained. No cadence is accepted because the coupled reference gate failed. Sampled peaks and prefix maxima are not proven continuous-time suprema.

[Seed 840131 conditional record](results/replay/s840131-p1-a4.json) · [Seed 840137 conditional record](results/replay/s840137-p1-a4.json) · [Explicit unqualified cadence flags](results/cadence-screens.json)

## Excitation and domain scope

Both retained drivers were non-low by all frozen field, force and torque excitation criteria:

| Seed | Loaded receiver-time fraction | Inflow range/v0 | Force wake amplitude/W | RP torque wake amplitude/(W·arm) |
|---|---:|---:|---:|---:|
| 840131 | 0.625000 | 0.766731 | 0.293272 | 0.042172 |
| 840137 | 0.625000 | 0.801314 | 0.251437 | 0.043282 |

The loaded fraction uses left endpoints only; ranges and load amplitudes use all saved endpoints. Instantaneous diagnostics retained the frozen input/tilt/near-wake guards at every dense endpoint, including terminal T. No observed domain or safety rejection occurred. This does not establish continuous-time or internal-RK-stage field-domain validity. Pair-clearance diagnostics are swept straight-segment endpoint envelopes; obstacle minima are endpoint samples. Neither is a proof of safe flight or exact curved-path clearance.

## Resource and timing scope

The one supervised window finished in 51.136 s, with exit 0 and no watchdog interruption. The final worker checkpoint reported 53.786 CPU seconds and process max RSS 469,044 KiB. CPU can exceed wall time due to runtime/helper threads. Logical retained artifacts were about 80.22 MB at terminal execution, below the 150 MB cap with a 2 MB failure reserve. Later report/viewer artifacts are separately accounted before publication.

There was no timing warmup, repetition or speedup claim. Full IPC-delimited per-job wall times including writes were not separately logged: the evidence is watchdog enforcement and no kill, not an asserted maximum measured job duration. Per-run stages include instrumentation; total simulation-loop timings exclude subsequent binary serialization, while the external supervised window includes checksums, gzip, output writes and numerical analysis. Process RSS is a cumulative high-water mark including retained states and garbage collection, not algorithm-only allocation. Rendering is excluded from simulation/diagnostic costs.

| Run | Field ms | Controller ms | RK4 ms | Safety/diagnostics ms | Recording ms | Instrumented loop ms |
|---|---:|---:|---:|---:|---:|---:|
| s4301-p16-a64 | 39.79 | 50.09 | 86.64 | 213.53 | 28.85 | 448.81 |
| s840131-p4-a4 | 412.65 | 43.45 | 261.42 | 557.43 | 94.99 | 1432.40 |
| s840131-p2-a4 | 425.16 | 36.80 | 537.71 | 1230.29 | 196.24 | 2538.68 |
| s840131-p1-a4 | 432.08 | 41.34 | 1118.35 | 2617.64 | 397.58 | 4812.26 |
| s840137-p4-a4 | 358.66 | 38.59 | 215.08 | 520.12 | 89.23 | 1275.82 |
| s840137-p2-a4 | 400.52 | 33.07 | 425.05 | 1049.27 | 186.57 | 2197.19 |
| s840137-p1-a4 | 398.37 | 29.54 | 874.66 | 2161.46 | 369.02 | 4040.28 |
| s840131-p1-a8 | 202.04 | 27.54 | 837.84 | 2047.04 | 364.41 | 3681.90 |
| s840131-p1-a16 | 113.59 | 26.20 | 897.97 | 2187.35 | 384.17 | 3830.61 |
| s840137-p1-a8 | 209.83 | 27.06 | 881.05 | 2144.80 | 390.00 | 3862.01 |
| s840137-p1-a16 | 111.30 | 27.36 | 882.87 | 2116.92 | 390.05 | 3740.13 |

[Supervisor receipt including stdout/stderr](results/supervisor.json) · [Invocation](results/invocation.json) · [Execution validity](results/execution-validity.json)

## Reproducibility and retention

- Frozen plan SHA256: `0f528635c0c0e12dad5870fa7ccbad509029da741294e75e18bb63823033f267`
- Frozen source aggregate SHA256: `dc73105f85b4f81c9a84899a117eefbb03c82b3c651a34fa9c73716f2c2c289b`
- Exact evaluator SHA256: `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`
- Raw retention: 15 gzip Float64 arrays, 70,122,112 logical bytes, 64,975,968 stored bytes.
- Full source dependencies, configuration, two separately recorded analytic fixture attempts, raw arrays, all gates, all conditional diagnostics, terminal states/held scalars, event hashes and stopping/skipping reasons are retained. No failure was overwritten to produce a successful result.
- Retention is complete for the preregistered saved data, not every intermediate step of every run. Five full-step state-stream hashes are independently rehashable from retained arrays; six runs retain their common snapshots plus rolling hashes. See the independent post-run audit.
- Runtime: Node v24.19.0, Linux x64. Integer base tick 1/6400 s.

[Frozen plan](PLAN.md) · [Freeze](FREEZE.json) · [Source manifest](source-manifest.json) · [Raw retention manifest](results/RAW-RETENTION-MANIFEST.json) · [Independent source review](../review/IMPLEMENTATION-REVIEW.md) · [24 final analytic checks](../robustness/RESULTS.md)

## Viewer and interpretation limits

[Three.js recorded-data viewer](demo/index.html) shows the 10 actual completed fresh coupled records, with 10 ms visual display sampling and interpolation. Metrics come from dense/raw states, not interpolated display poses. The bundled offline viewer provides the same records and summaries without a network dependency. Browser-rendered validation was blocked: installed cloud Chromium exited on `socket() failed: Operation not permitted` before opening the page. Source/data linkage and static module/record checks are available; rendering and interactive behavior are unverified. See [retained browser failure](viewer-qa/browser-check.json).

The mean wake, receiver response, projection truncation and physical length convention remain physically unvalidated. The earlier figure-overlay comparison was withdrawn for normalization/domain mismatch, and the original empirical dataset remains unavailable. This numerical result neither repairs nor validates that model. It establishes a useful negative result: the declared coupled airflow-reference target was not met within this fixed budget. The observations favor ordinary hold-age sensitivity at the sampled resolution, without causally excluding field nonsmoothness or feedback. A new refinement study would require a new prospective plan; it is not silently appended here.
