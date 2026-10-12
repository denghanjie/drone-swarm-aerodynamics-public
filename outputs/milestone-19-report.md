# Checkpoint 19 — reject the simultaneous soft filter

The proposed smoother command filter is mathematically well behaved in isolated tests, but it worsens this flock-passage task. Do not promote it.

## What we tested

Three previously troublesome starting flocks, two controllers, three physics steps:18 runs. Both controllers use identical checkpoint 18 inward map guidance and the same local 3D Boids, rigid-body dynamics and contact detection. This is development evidence, not new holdout evidence. The fixed controller period is 10 ms. See the [frozen protocol](milestone-19-protocol.json) and [filter method](milestone-19-source/method.md).

## What happened

At 5 ms the previous controller completed 150/150 passages; the new soft filter completed 84/150. None of the 18 runs stopped for contact. The new filter failed all 6 adjacent time-step comparisons; seed 1002 changed 33→27→25 completions. The old controller passed 5/6 comparisons, including all three 2.5→1.25 ms comparisons. Its 1002 coarse comparison still fails and remains in the record. Seed 905 here uses inward guidance; do not conflate it with the earlier steering-only seed 905 counterexample.

|Seed|Controller|Step(ms)|Finished|Contact stop|Smallest connected group|Final connected group|
|---|---|---:|---:|---|---:|---:|
|905|interior|5|50/50|None|50/50|50/50|
|905|interior|2.5|50/50|None|50/50|50/50|
|905|interior|1.25|50/50|None|50/50|50/50|
|905|soft|5|26/50|None|36/50|36/50|
|905|soft|2.5|26/50|None|36/50|36/50|
|905|soft|1.25|26/50|None|36/50|36/50|
|1002|interior|5|50/50|None|49/50|50/50|
|1002|interior|2.5|50/50|None|49/50|50/50|
|1002|interior|1.25|50/50|None|49/50|50/50|
|1002|soft|5|33/50|None|44/50|44/50|
|1002|soft|2.5|27/50|None|20/50|28/50|
|1002|soft|1.25|25/50|None|27/50|27/50|
|1004|interior|5|50/50|None|41/50|41/50|
|1004|interior|2.5|50/50|None|41/50|41/50|
|1004|interior|1.25|50/50|None|41/50|41/50|
|1004|soft|5|25/50|None|18/50|30/50|
|1004|soft|2.5|25/50|None|18/50|30/50|
|1004|soft|1.25|25/50|None|18/50|30/50|

## Numerical evidence

|Seed|Controller / scenario|Step pair(ms)|Maximum final position difference(m)|Finish counts|Pass 1 cm test|
|---|---|---|---:|---|---|
|905|interior|5→2.5|5.2827466e-05|[50, 50]|Yes|
|905|interior|2.5→1.25|3.1363318e-06|[50, 50]|Yes|
|905|soft|5→2.5|4.3932149|[26, 26]|No|
|905|soft|2.5→1.25|0.44967863|[26, 26]|No|
|1002|interior|5→2.5|0.018683885|[50, 50]|No|
|1002|interior|2.5→1.25|1.8924154e-05|[50, 50]|Yes|
|1002|soft|5→2.5|10.563761|[33, 27]|No|
|1002|soft|2.5→1.25|5.8030324|[27, 25]|No|
|1004|interior|5→2.5|9.410872e-06|[50, 50]|Yes|
|1004|interior|2.5→1.25|5.6577592e-07|[50, 50]|Yes|
|1004|soft|5→2.5|1.6227239|[25, 25]|No|
|1004|soft|2.5→1.25|2.1407963|[25, 25]|No|

The solver test suite covers analytic half-space solutions, finite-difference gradients, linear solves, reversed constraint ordering and conflicting random constraints. These checks pass. The largest gradient residual during the nine soft-filter runs is below 1e-6. This verifies the local soft-objective solution, not the safety or convergence of an entire trajectory. A speed cap applied after optimization can further violate constraints. Long-horizon divergence may involve nonlinear amplification as well as controller transitions; these experiments do not identify a single root cause.

## Decision and records

Retain the previous controller as a provisional reference. Preserve this unsuccessful replacement for diagnosis; do not claim smoothing solved numerical sensitivity. [3D comparison](milestone-19-lab.html), [full final states and samples](milestone-19-study.json), [all numerical comparisons](milestone-19-comparisons.json), [solver checks](milestone-19-solver-checks.json). Individual files in the source directory retain complete runs and recorded trajectories.
