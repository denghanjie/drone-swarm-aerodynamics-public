# Milestone 30 — wall-priority avoidance

This experiment asks whether repairing wall-clearance commands after the old pair filter prevents the saved large-flock wall contacts. All runs keep local 3D Boids, shared route guidance and rigid-body dynamics. Airflow is off and observations ideal.

## Plain-language result

On the two fresh 1,000-drone starting flocks, the old filter stopped for contact in 2/2 trials; the wall-priority filter stopped in 0/2. Each large-flock test covers 20 seconds only. The 5,000-drone development trial ends at 20.0000 s with no contact stop.

The 50-drone full-mission comparison finishes baseline: 50/50, wall-priority: 50/50.

The two 50-drone final states are exactly equal. Wall repair never activates in that candidate run; this is a regression check, not evidence that the repair improves small-flock navigation.

The correction is promising for the tested early wall failure. Advance it to full-duration large-flock testing; do not call it generally safe or a completed navigation solution. Wall requests can still conflict with requests to keep drones apart, and a later queue or contact remains possible.

This changes how competing movement requests are resolved. It preserves local Boids and supplies no individual paths or crossing schedules. The underlying projection method is standard; no algorithmic novelty is claimed. [Next test gate](research-next-controller-gate.md).

## Every planned run

Large-flock tests cover the first 20 seconds only. The 50-drone tests cover 180 seconds. Reaching a short horizon is not completing a factory mission.

|Role|Seed|Drones|Filter|Step ms|End seconds|Finished|Outcome|
|---|---:|---:|---|---:|---:|---:|---|
|development|1501|1000|wall-priority|2.5|20.0000|0|horizon reached|
|development|1501|5000|wall-priority|2.5|20.0000|0|horizon reached|
|heldout|1901|1000|baseline|2.5|15.9800|0|obstacle contact envelope|
|heldout|1901|1000|wall-priority|2.5|20.0000|0|horizon reached|
|heldout|1902|1000|baseline|2.5|15.3025|0|obstacle contact envelope|
|heldout|1902|1000|wall-priority|2.5|20.0000|0|horizon reached|
|heldout|1901|50|baseline|2.5|180.0000|50|horizon reached|
|heldout|1901|50|wall-priority|2.5|180.0000|50|horizon reached|
|refinement|1901|1000|wall-priority|1.25|20.0000|0|horizon reached|
|refinement|1901|50|wall-priority|1.25|180.0000|50|horizon reached|

## Command diagnostics

Wall priority can repair a wall request while violating requests to separate from other drones. Values below count drone-control updates, not independent trials or collisions. A finite-iteration nonconvergence flag does not prove infeasibility.

|Trial|Wall violations before → after|Largest wall residual after m/s|Pair violations after|Nonconverged solves|
|---|---:|---:|---:|---:|
|development-1501-1000-wall-priority-0.0025|14949 → 0|9.65996e-11|51390|0|
|development-1501-5000-wall-priority-0.0025|43886 → 0|9.74462e-11|556346|0|
|heldout-1901-1000-baseline-0.0025|6797 → 6797|0.34616|23274|0|
|heldout-1901-1000-wall-priority-0.0025|15440 → 0|9.08471e-11|51995|0|
|heldout-1902-1000-baseline-0.0025|6039 → 6039|0.378856|24208|0|
|heldout-1902-1000-wall-priority-0.0025|15763 → 0|9.52112e-11|54051|0|
|heldout-1901-50-baseline-0.0025|0 → 0|0|26|0|
|heldout-1901-50-wall-priority-0.0025|0 → 0|0|26|0|
|refinement-1901-1000-wall-priority-0.00125|15440 → 0|9.08551e-11|51995|0|
|refinement-1901-50-wall-priority-0.00125|0 → 0|0|26|0|

## Does the flock still move?

This post-hoc descriptive check was added after the two fresh-seed candidate outcomes. It counts final centers beyond the first partition’s far face plus the body radius (x > 0.255 m). It does not count completed factory missions or establish freedom from later stalls.

|Candidate trial|End s|Beyond first partition|Mean forward displacement m|
|---|---:|---:|---:|
|development-1501-1000-wall-priority-0.0025|20.0000|441|10.009|
|development-1501-5000-wall-priority-0.0025|20.0000|611|9.314|
|heldout-1901-1000-wall-priority-0.0025|20.0000|437|10.013|
|heldout-1902-1000-wall-priority-0.0025|20.0000|441|9.992|

## Actual commands before contact

These are saved at the preceding control update, not recomputed at the terminal state. Each row is one active wall constraint for a contact-involved drone; the normal alone does not uniquely identify the box. Negative away velocity means motion toward that surface.

|Trial / drone|Command time s|Contact time s|Required away m/s|Commanded away m/s|Actual away m/s|
|---|---:|---:|---:|---:|---:|
|heldout-1901-1000-baseline-0.0025 / 891|15.97000|15.98000|0.24925|-0.03245|-0.09912|
|heldout-1902-1000-baseline-0.0025 / 946|15.30000|15.30250|0.24984|-0.12600|-0.12430|

## Numerical refinement

- refinement-1901-1000-wall-priority-0.00125: maximum synchronized position difference **3.6164377e-06 m**, 1 cm test **True** across 21 exact common saved frames through 20.0 s. Same terminal event identity: True; terminal times [20, 20].
- refinement-1901-50-wall-priority-0.00125: maximum synchronized position difference **3.3332076e-06 m**, 1 cm test **True** across 181 exact common saved frames through 180.0 s. Same terminal event identity: True; terminal times [180, 180].

No candidate 5,000-drone refinement was prescribed here. Passing a 1,000-drone comparison cannot certify the 5,000-drone candidate.

## Records and limits

[3D replay](milestone-30-lab.html) · [Protocol](milestone-30-protocol.json) · [Method](milestone-30-source/method.md) · [Checks](milestone-30-artifact-checks.json) · [Initial implementation-error record](milestone-30-error-record/README.md). Actual preceding commands for affected drones are in each run’s `lastControl`. The analytic solver and baseline equivalence checks are in [solver checks](milestone-30-checks.json). Larger flocks start in larger clouds at the same nominal 0.75 m lattice spacing; this is not fixed-volume density scaling. No dynamic safety guarantee, physical calibration, airflow validity, general navigation or novelty claim follows. Concurrent wall times are not a performance benchmark.

[All trials as CSV](milestone-30-trials.csv) · [Independent projection reference](milestone-30-reference-checks.json). The independent reference enumerates affine faces and intersects each with the speed ball; all 200 generated feasible problems agree within 1.41e-9 m/s.
