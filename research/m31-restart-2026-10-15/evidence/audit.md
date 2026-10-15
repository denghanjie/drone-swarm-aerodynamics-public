# M31 independent evidence audit — first research checkpoint

M31 supports a narrow result: in the saved ideal-observation, zero-airflow factory simulations, the wall-priority candidate completed the prescribed missions and the three matched fresh baseline runs stopped at obstacle contacts. The numerical trajectory criterion failed in every refinement. The files and main report agree on both findings. This checkpoint does not establish aerodynamic validity, safe navigation, or a statistically estimated success rate.

This audit read the sanitized public repository, independently recomputed quantities from saved JSON and Float64 trajectories, inspected the actual dependency chain, and performed six single-drone RK4 steps plus same-state controller probes. It did not rerun full missions, alter frozen outputs, run the original artifact-writing audit scripts, or change Git state. Source references below are relative to the public repository. New scripts and their results are relative to this evidence directory.

## Directly checked observations

All ten entries in `outputs/milestone-31-protocol.json:105` match the SHA-256 of their current files, including `outputs/step02c-source/physics.cjs`. The wall filter is byte-identical to M30. A textual M30/M31 `outputs/milestone-31-source/sim.cjs` comparison shows added obstacle/neighbor identities, preceding-control state, and actuator traces; the numeric steering and integration statements are unchanged. The recorded development 20 s state equals the earlier M30 endpoint in all 17 components for all 5,000 drones.

For all ten jobs, the independent audit checked binary dimensions and finite values, exact JSON/binary initial and final poses, control-update accounting, crossing counts, and minima recomputed from the saved science samples. All passed. All 26 available checkpoints exactly match binary poses and crossing accounting; terminal checkpoints also match full final states. The three fresh baseline/candidate pairs and all refinement pairs have exactly equal initial states. All 108 selected current public-manifest entries for M31 and its rigid-body dependency match. All six passage-figure data hashes and crossing arrays match the raw records. This is a separately written check, not a rerun of the reported 224-check script.

|Primary case|Raw-record baseline outcome|Raw-record candidate outcome|Last candidate crossing|
|---|---|---|---:|
|Seed 2001, 1,000, wide|Obstacle contact, 16.775 s, drone 521, partition-0-above|1,000/1,000; no recorded stop through 180 s|109.7500 s|
|Seed 2002, 1,000, narrow|Obstacle contact, 9.995 s, drone 196, partition-0-left|1,000/1,000; no recorded stop through 180 s|149.7700 s|
|Seed 2001, 5,000, wide|Obstacle contact, 11.665 s, drone 1855, partition-0-below|5,000/5,000; no recorded stop through 180 s|168.4125 s|
|Development seed 1501, 5,000, wide|Historical comparison is separate|5,000/5,000; no recorded stop through 180 s|168.5625 s|

“No recorded stop” is an observed record plus verified code behavior. One-second pose files cannot independently recheck every substep of a 180 s flight. The three baseline contact drones were cheaply replayed from their actual preceding control state, for two 2.5 ms steps each. Their actuator output, all 17 endpoint components, contacted obstacle, and clearance were reproduced exactly using the saved trial-specific geometry. Their first replayed step was clear and the second contacted. This is internal consistency using the frozen dynamics, not independent physical validation (`audit-controls.json`, `contacts`).

The development flock has a largest connected component of 4,999/5,000 at 50 saved science samples from 105.0 through 109.9 s. The three fresh primary candidate flocks have one connected component at every saved 0.1 s science sample. Connectivity uses an undirected distance graph with radius 1.8 m and includes finished drones. It is neither continuous-time connectivity nor evidence of a realistic communication network.

## Numerical result and useful new descriptive summaries

The independent binary calculation exactly reproduces every published maximum, median, and nearest-rank p95 in `outputs/milestone-31-comparisons.json`; maximum absolute discrepancy is zero. Drones are paired by saved ID at identical saved times. There is no interpolation or rematching.

|Comparison|Saved times|First saved error ≥1 cm|Maximum ID-matched position error|Endpoint median / p95 error|Frozen criterion|
|---|---:|---:|---:|---:|---|
|1,000 wide, 2.5 vs 1.25 ms|181 through 180 s|35 s|5.1666097555 m|0.397739 / 1.108852 m|Fail|
|1,000 narrow, 2.5 vs 1.25 ms|181 through 180 s|30 s|32.7674603483 m|1.784078 / 17.370774 m|Fail|
|5,000 wide, 2.5 vs 1.25 ms|61 through 60 s|31 s|7.9817922075 m|0.343936 / 1.971201 m|Fail|

All maxima occur at the comparison endpoint. This does not say the position error was small before completion: the first ≥1 m discrepancies occur at 73, 38, and 41 s, respectively. Two step sizes give a discrepancy, not an observed convergence order or a continuum error estimate. A third step size, a control-cadence investigation, and local error/switch diagnostics are missing. The 5,000-drone refinement finishes with zero crossings at 60 s, so its passage-count agreement does not test late bottlenecks or full-course passage. The three fresh baseline contacts have no matched refinement in M31.

The following are **new post-hoc descriptive calculations**, not revised acceptance criteria:

|Quantity|1,000 wide|1,000 narrow|
|---|---:|---:|
|Maximum same-ID absolute crossing-time difference|6.6325 s|53.55125 s|
|Median same-ID absolute crossing-time difference|0.0800 s|2.5450 s|
|Fraction of IDs with crossing-time difference >1 s|3.5%|63.7%|
|Maximum difference in cumulative finished fraction, at all event times|0.009 (9/1,000)|0.006 (6/1,000)|
|Wasserstein-1 distance between empirical crossing-time distributions|0.04092125 s|0.09080375 s|
|Last crossing: primary / fine|109.7500 / 109.72125 s|149.7700 / 149.5975 s|
|Maximum center-position difference over saved poses|0.0214255 m|0.0734393 m|

The published equal terminal times mean both runs reached the prescribed 180 s horizon. They do not mean equal last-crossing times: those differ by 28.75 ms and 172.5 ms. No claim of violating a *prespecified completion-time criterion* follows, because the protocol's 10 ms rule concerns stop/horizon time, not last crossing. The narrow result shows large changes in which drone emerges when, while the aggregate passage curve is similar. It motivates future, separately frozen ensemble estimands; it cannot retroactively rescue the failed trajectory criterion. Chaos, rank swapping, solver error, and switching sensitivity remain hypotheses rather than identified causes.

## Controller, clearance, and model caveats

`outputs/milestone-31-source/sim.cjs:4` defines the local social radius (1.8 m), separation/alignment/cohesion, speed limit (0.9 m/s), body radius (0.075 m), wall margin (0.3 m), pair margin (0.38 m), and 100 Hz control. The shared route is a hand-specified spatial field in `outputs/milestone-31-source/factory-wide.cjs:9`; it is evaluated at each drone's x-position plus 0.8 m (`outputs/milestone-31-source/sim.cjs:8` and `outputs/milestone-31-source/sim.cjs:13`). There are no per-drone slots or schedules, but all drones receive common map-informed guidance. M31 has only `mode='boids'` runs and therefore cannot isolate the contribution or necessity of Boids versus shared guidance, or claim purely emergent navigation from local interactions.

The baseline applies six cyclic wall/pair projection sweeps and clips speed (`outputs/milestone-31-source/sim.cjs:21`). The candidate then projects the result onto wall halfspaces and the speed ball (`outputs/milestone-31-source/wall-filter.cjs:4`); pair constraints are deliberately soft. Pair constraints use neighbors' current velocity, not a simultaneous jointly feasible multi-agent solution. Finite cyclic projections and hard pair inclusion at distance <1.5 m are plausible sensitivity mechanisms. The grid explicitly sorts IDs (`outputs/milestone-31-source/grid.cjs:5`), so cell traversal alone does not randomly reorder constraints.

At the primary candidate control-update level, pair-request residuals exceed 1e-7 m/s for 1.2168% of wide 1,000-drone updates, 5.0244% of narrow 1,000-drone updates, and 7.5576% of fresh wide 5,000-drone updates. These are normalized counts of drone-control updates, not collision probabilities or counts of individual violated pairs. They are not controlled comparisons with baseline rates because baselines stop much earlier. Primary candidate sampled minimum pair center distances are 0.376594, 0.234959, and 0.237268 m; corresponding modeled surface gaps are 0.226594, 0.084959, and 0.087268 m. The nominal 0.38 m pair margin is thus not maintained, although the 0.15 m contact diameter remains below these sampled minima. Sampled clearances do not prove intersample minima.

Candidate wall residuals remain approximately 1e-10 m/s in saved totals, while some repair solves reach 512 iterations. A feasible final velocity and the solver's combined residual/iterate-change stopping test are different facts. Aggregate totals do not identify the state/time of each iteration-limit event, so local diagnosis of those events requires additional logging in a future test.

At baseline contact, command deficits against the contacted wall were 0.217873, 0.405917, and 0.354149 m/s. Actual velocities were still toward the wall. These traces support a mechanism consistent with the correction, but one snapshot is not a causal decomposition or a uniform bound on tracking error. The wall-margin comparison inequality in `outputs/research-wall-priority-physics-note.md` requires a verified adverse tracking bound; M31 has not supplied it.

The actual dependency `outputs/step02c-source/physics.cjs:18` is rigid-body dynamics with gravity, motor thrust/torque, and 40 ms first-order motor lag. M31 calls `integrate` without an external-force argument (`outputs/milestone-31-source/sim.cjs:44`), so it uses zero force. There is no wake interaction, rotor inflow, drag, ground/wall aerodynamic effect, or sensing delay in this experiment. Its 15 cm spherical contact envelope is a model assumption, not a validated physical rotor-volume envelope. Contact tests compute the minimum distance along straight endpoint segments; they do not exactly minimize the curved RK4 physical path. Events and finish crossings are assigned to the integration step endpoint. If multiple events fall within one step, the loop's first drone index is reported, not an exact chronological ordering of substep impacts (`outputs/milestone-31-source/sim.cjs:45`). None of those limits is an established error in the three reported contacts, but their magnitude is unbounded by the present evidence.

## Exploratory same-state order probe

`audit_controls.cjs` evaluates each of the 1,000 drones in the saved primary candidate checkpoints at 20 s, for wide seed 2001 and narrow seed 2002. For each drone, the normal ascending list `Grid.neighbors(i, 1.8)` is replaced by `ids.slice().reverse()`. Every state, gain, geometry, route, and chosen filter remains fixed. Both social floating-point summation and sequential pair-projection order reverse; the experiment does not isolate these contributions.

|Candidate probe|Maximum change in requested velocity|p95 change|Requests changing >0.01 m/s|
|---|---:|---:|---:|
|1,000 wide at 20 s|0.176566882 m/s|0.039249453 m/s|132/1,000|
|1,000 narrow at 20 s|0.172430360 m/s|0.063740032 m/s|223/1,000|

This is direct evidence of same-state order sensitivity in the implemented controller. It is an **artificial permutation, newly explored after inspecting M31**, not preregistered confirmation, a more accurate solution, or proof of the cause of timestep divergence. The normal runs keep ascending ID order. `audit-controls.json` retains input hashes, exact forward/reverse neighbor IDs for every probe, requested velocities, and both wall/pair residuals. Baseline-filter probes at these *candidate* states are diagnostic evaluations, not reruns of baseline missions.

## Confounding and evidence boundaries

The controller comparison within each scenario is matched and interpretable as changing the wall repair in this deterministic model. The wide/narrow 1,000-drone comparison changes both seed and geometry, so their difference does not identify a geometry effect. Increasing count changes the cloud shape and travel burden: actual initial extents are approximately 8.409 × 6.904 × 6.155 m at 1,000 versus 25.658 × 11.409 × 6.159 m at 5,000, at the same nominal 0.75 m spacing. The larger flock is not a fixed-volume density experiment; IDs/positions are not a nested copy across counts. Seeds 2001 and 2002 are only two fresh initialization seeds across three prescribed scenarios, not three independent samples from a declared deployment distribution.

The historical claim that 793 source-tree files were preserved belongs to the original pre-export audit. The current public export deliberately changes metadata in 13 of those source records. This audit verified all 13 original/public hash mappings in `docs/public-export-changes.json`; they explain the differences checked. It did not finish an exhaustive 793-file archival rehash and does not claim that every current public byte equals the private historical manifest. All M31 frozen scientific dependency hashes and all selected current public-manifest hashes do match. These are integrity/consistency checks, not external timestamped proof of preregistration.

The evidence lacks per-update logs for successful runs, full states at each saved second, continuous connectivity/clearance records, a late 5,000-drone refinement, independently refined baseline events, physically calibrated interaction forces, and measurement-based tracking-error envelopes. Existing 0.1 s scalar samples and 1 s position/quaternion frames cannot reconstruct all of those missing facts.

## Priorities for the next bounded experiment

1. Freeze a numerical-diagnosis protocol before generating new outcomes. Keep the original 1 cm result as failed. Separate physics-step, control-period, event-localization, and solver-iteration effects; do not change multiple axes at once. Use short windows around the first divergence and small isolated controller/geometry fixtures before expensive whole-flock runs. Treat already viewed M31 cases as development evidence.
2. Test ordering and switching with controlled local fixtures. Hold the social sum fixed while permuting only constraint order, then hold constraint order fixed while changing social accumulation. Log active pair IDs, distances around 1.5 m, residuals, iterations, actual/requested velocity, and per-agent differences. Include label-permutation invariance as a diagnostic. A better residual is not automatically a safer or more accurate mission.
3. Refine the three baseline contacts locally with unchanged 100 Hz control and compare event time/identity using appropriate event localization. Compare the actual envelope and curved path against the segment approximation. This can test whether the qualitative baseline failure is numerically robust without a large campaign.
4. Define future ensemble estimands and tolerances on independent grounds: passage-time quantiles/distribution, fraction crossing by fixed time, pair and wall clearances, and connected-component duration. Keep ID-matched trajectories alongside them; do not choose tolerance values from the observed 0.006/0.009 ECDF discrepancies.
5. Before aerodynamic claims, independently validate force/moment and actuator/tracking models with traceable measurements and uncertainty. After the numerical gate, use a seed×geometry design, matched count/extent contrasts, and route/Boids ablations to isolate the intended mechanism. Full 5,000-drone refinement and broader sensing/airflow tests belong to a later declared gate.

## Reproduction and claim ledger

Run `node audit_controls.cjs PUBLIC_REPOSITORY`, then `python3 audit_recompute.py PUBLIC_REPOSITORY` with a standard-library Python 3. Both require an explicit relative or absolute repository-root argument, check for its M31 protocol, and write only beside themselves. The Python output includes the Node output hash when that file is present. The Python calculation reads little-endian Float64 frames, computes Euclidean equal-ID xyz distances at intersecting exact timestamps, uses `ceil(.95*n)-1` for p95 and the usual midpoint median, and evaluates passage ECDF differences at the union of exact stored crossing times. Crossing times are discrete step-end records. The replay layout is `[time, x,y,z,qx,qy,qz,qw, ...]`; quaternion order is **xyzw**, confirmed by `outputs/milestone-31-source/sim.cjs:41` and `outputs/step02c-source/physics.cjs:1`. The Node calculation reuses the frozen dependencies only for the small consistency/probe calculations described above. The precise scripts are retained; no path to a particular machine is required.

|Claim|Evidence classification|Assessment and main source|
|---|---|---|
|Candidate completes prescribed primary cases; fresh baselines stop|Directly checked raw-record accounting, plus contact replay|Supported within saved model; raw job JSON and `outputs/milestone-31-source/sim.cjs:45`|
|Exact trajectories are resolved to 1 cm|Independent calculation from binary traces|Rejected in 3/3; `audit-data.json`, `trajectoryComparisons`|
|Aggregate passage is less sensitive than ID histories in two 1,000-drone pairs|New post-hoc calculation|Observed descriptively; no prospective threshold or generalization|
|Wall repair enforces requested wall constraints in these records|Saved diagnostics, inspected solver, exact contact traces|Supported as request-level statement; no tracking or pair-safety theorem|
|Same-state output depends on input neighbor ordering|New exploratory controlled calculation|Observed; both social sum and pair order changed, causal source not isolated|
|Boids alone solves factory navigation|Source inspection and experiment design|Not identified; shared route and all local terms remain active|
|M31 validates aerodynamics or real flights|Actual physics dependency and run arguments|Unsupported; airflow force is zero and observations ideal|
|Historical sources are intact in the sanitized public export|Frozen/current hashes and sanitization mappings|M31 dependency checks pass; historical metadata redactions explained; no fresh exhaustive 793-file claim|
|Four successes estimate field safety/reliability|Experiment design and stopping rule|Unsupported; four prescribed candidates include development reuse and three matched cases with whole-run stopping|
