# Checkpoint 17 — Fresh comparison across three courses

Within original research Step 5. These are numerical simulation results, not physical validation.

## Decision

Smoothed steering improves tight-course completion from **179/250 to 249/250**, with no contact stops in these five matched runs. It is still provisional: two of its seven predeclared refinement cases fail the 1 cm trajectory criterion (2.875 m and 0.085 m discrepancies), despite stable completion counts. Stronger retention is rejected: one fresh collision, three failed fresh refinement checks, and the earlier development failure remain in the record.

The development result did not generalize completely. Smoothing steering helps, but does not remove every source of trajectory sensitivity in the remaining filter and closed loop. A post-hoc third-step audit examines the failed primary cases without replacing the original failures.

## Method

45 cases: five previously unused seeds 901–905 × three courses × three controllers. All controller sources were frozen before the fresh trials. The smoothed-steering candidate was chosen on development cases 801–802. Stronger retention was already inconsistent in development and is retained as a diagnostic comparison.

Every run uses 50 rigid bodies for 60 seconds,5 ms RK4 integration,10 ms command updates, local separation/alignment/cohesion, ideal state observations and known geometry. Airflow is off. Both variants use the same initial states in each matched case. The previous joint filter is a heuristic; it has neither a feasibility proof nor a collision-avoidance certificate for this lagged plant.

## Results

|Course|Controller|Contact stops / runs|Total finished|Finished per run|Smallest sampled connected group|
|---|---|---|---|---|---|
|slalom|Previous joint-clearance Boids|0/5|250/250|50–50|50/50|
|slalom|Stronger retention|0/5|250/250|50–50|50/50|
|slalom|Smoothed steering|0/5|250/250|50–50|50/50|
|staggered|Previous joint-clearance Boids|0/5|249/250|49–50|45/50|
|staggered|Stronger retention|0/5|250/250|50–50|50/50|
|staggered|Smoothed steering|0/5|250/250|50–50|49/50|
|tight|Previous joint-clearance Boids|0/5|179/250|31–40|22/50|
|tight|Stronger retention|1/5|199/250|0–50|29/50|
|tight|Smoothed steering|0/5|249/250|49–50|48/50|

A contact stop ends the whole run; the completion count then records only drones that crossed the finish plane before stopping. Unfinished drones at 60 s have not necessarily collided. Connectivity uses the largest chain of neighbors within 1.8 m, sampled every 0.1 s, including the initial condition. Heading agreement does not imply connectivity. The CSV preserves every case rather than hiding failures in averages.

## Numerical refinement

The predeclared criterion is matching completion/stop outcome, endpoint-position discrepancy below 1 cm, and end-time difference below 10 ms. Refinement halves the integration step to 2.5 ms, keeping the physical controller at 100 Hz. Maximum endpoint discrepancy is over all drones. Different stop times make endpoint position discrepancies less directly comparable; those checks fail if time differs by 10 ms or more.

|Seed|Course|Controller|Coarse / fine finished|Max endpoint difference (m)|Criterion|
|---|---|---|---|---|---|
|901|slalom|Stronger retention|50 / 50|2.2553466e-05|pass|
|901|slalom|Smoothed steering|50 / 50|4.7013269e-07|pass|
|901|staggered|Stronger retention|50 / 50|5.4615727e-06|pass|
|901|staggered|Smoothed steering|50 / 50|6.3011953e-08|pass|
|901|tight|Stronger retention|0 / 0|0.0019466652|pass|
|901|tight|Smoothed steering|50 / 50|1.0191752e-05|pass|
|902|tight|Stronger retention|49 / 49|5.2289603|FAIL|
|902|tight|Smoothed steering|50 / 50|0.00016997179|pass|
|903|tight|Stronger retention|50 / 50|0.00048887215|pass|
|903|tight|Smoothed steering|49 / 49|0.0046680783|pass|
|904|tight|Stronger retention|50 / 50|0.91442839|FAIL|
|904|tight|Smoothed steering|50 / 50|2.8746355|FAIL|
|905|tight|Stronger retention|50 / 50|0.058261615|FAIL|
|905|tight|Smoothed steering|50 / 50|0.085091049|FAIL|

Agreement of these two integration steps supports numerical repeatability only for the tested configurations. It does not prove convergence for all inputs, robustness to controller-rate changes or agreement with flight data.

## Subsequent three-step diagnostic

A further **post-hoc diagnostic** repeated the three failed primary cases at a 1.25 ms step. The previous 2.5 ms results reproduced exactly. Seed 904 smoothed steering then agreed within 0.049 mm, and seed 1002 inward steering within 0.019 mm. But seed 905 smoothed steering diverged by 8.594 m and changed from 50 to 49 finishers. Thus, reducing the step alone is not a general fix. The original failed tests remain failed, and the difficult seed 905 case is preserved for further diagnosis.

[Predeclared diagnostic](research-block-refinement-audit-protocol.json) · [Full states](research-block-refinement-audit-runs.json) · [Comparison](research-block-refinement-audit.json)

## Evidence and reproducibility

- [3D replay](milestone-17-fresh-trials.html), [protocol](milestone-17-protocol.json), [per-case CSV](milestone-17-case-table.csv)
- [Full states and samples](milestone-17-study.json), [refinements](milestone-17-refinements.json), [verification](milestone-17-verification.json)
- [Simulator](milestone-17-source/sim.cjs), [steering components](milestone-17-source/continuous.cjs), [run script](milestone-17-source/study.cjs)

All seeds and unsuccessful variants are retained. No claim of arbitrary-terrain navigation, unknown-map planning, dense-swarm scalability, flight safety, aerodynamic fidelity or novelty follows from these experiments.
