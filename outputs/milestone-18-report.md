# Checkpoint 18 — Steering inside the clearance boundary

Within original research Step 5. These are numerical simulation results, not physical validation.

## Decision

The inward offset completes all 50 drones in each of eight fresh runs: **400/400**, versus 399/400 for the matched smoothed-steering reference. Neither has a contact stop. The added completion comes from seed 1002; it is a small holdout benefit, not evidence of universal superiority.

**The connectivity trade-off remains.** Two candidate flocks end fragmented, compared with four reference flocks. However, the worst candidate case ends as 41+9 (seed 1004), whereas its matched reference remains 50/50 connected. Seed 1003 ends 49+1. Steering farther inside also reduces the worst observed physical-envelope clearance to 0.127 m from 0.153 m, and minimum center separation to 0.198 m from 0.257 m. More completions do not imply more clearance.

Five of six preregistered refinement checks pass. Seed 1002 fails the unchanged 1 cm criterion with 0.018684 m endpoint disagreement, even though both runs finish 50/50. This variant remains an experimental alternative, not a validated replacement. The later three-step audit is diagnostic and does not erase the original failed check.

## Development and mechanism

The two development cases 801–802 each leave one drone behind under smoothed steering. At 60 s those drones are over 18 m from their nearest neighbor and lie on the lateral boundary shared by map guidance and filtering. Their filtered forward commands are zero. The 10 cm inward offset introduces a lateral command away from that boundary. Both development cases then finish 50/50 at both tested integration steps, with maximum differences 0.00002383 m and 0.000003608 m. Minimum sampled connectivity is 49/50 and 50/50 respectively. This intervention supports the practical fix in these cases; it does not prove a unique cause for every stall.

[Development protocol](milestone-18-development-protocol.json) · [Development comparisons](milestone-18-development-comparisons.json) · [Stranded-state inspection](milestone-18-stall-diagnosis.json) · [Exact command regression](milestone-18-regression.json) · [Diagnostic replay reproduction](milestone-18-replay-check.json)

## Method

16 fresh matched cases: seeds 1001–1005 on tight openings, seeds 1001–1003 on wide openings, two controllers each. The only change is map guidance aiming 0.35 m inside the aperture edge instead of 0.25 m. The clearance filter remains 0.25 m and the physical body radius remains 0.075 m. Development used seeds 801–802; fresh results were not used to tune the candidate. Sphere guidance is unchanged by this conditional edit and is not a new sphere validation claim.

Every run uses 50 rigid bodies for 60 seconds,5 ms RK4 integration,10 ms command updates, local separation/alignment/cohesion, ideal state observations and known geometry. Airflow is off. Both variants use the same initial states in each matched case. The previous joint filter is a heuristic; it has neither a feasibility proof nor a collision-avoidance certificate for this lagged plant.

## Results

|Course|Controller|Contact stops / runs|Total finished|Finished per run|Smallest sampled connected group|
|---|---|---|---|---|---|
|staggered|Smoothed steering + inward offset|0/3|150/150|50–50|50/50|
|staggered|Smoothed steering|0/3|150/150|50–50|49/50|
|tight|Smoothed steering + inward offset|0/5|250/250|50–50|41/50|
|tight|Smoothed steering|0/5|249/250|49–50|47/50|

A contact stop ends the whole run; the completion count then records only drones that crossed the finish plane before stopping. Unfinished drones at 60 s have not necessarily collided. Connectivity uses the largest chain of neighbors within 1.8 m, sampled every 0.1 s, including the initial condition. Heading agreement does not imply connectivity. The CSV preserves every case rather than hiding failures in averages.

## Numerical refinement

The predeclared criterion is matching completion/stop outcome, endpoint-position discrepancy below 1 cm, and end-time difference below 10 ms. Refinement halves the integration step to 2.5 ms, keeping the physical controller at 100 Hz. Maximum endpoint discrepancy is over all drones. Different stop times make endpoint position discrepancies less directly comparable; those checks fail if time differs by 10 ms or more.

|Seed|Course|Controller|Coarse / fine finished|Max endpoint difference (m)|Criterion|
|---|---|---|---|---|---|
|1001|staggered|Smoothed steering + inward offset|50 / 50|3.8217631e-07|pass|
|1001|tight|Smoothed steering + inward offset|50 / 50|2.0054453e-05|pass|
|1002|tight|Smoothed steering + inward offset|50 / 50|0.018683885|FAIL|
|1003|tight|Smoothed steering + inward offset|50 / 50|0.0001077488|pass|
|1004|tight|Smoothed steering + inward offset|50 / 50|9.410872e-06|pass|
|1005|tight|Smoothed steering + inward offset|50 / 50|5.6427273e-05|pass|

Agreement of these two integration steps supports numerical repeatability only for the tested configurations. It does not prove convergence for all inputs, robustness to controller-rate changes or agreement with flight data.

## Subsequent three-step diagnostic

A further **post-hoc diagnostic** repeated the three failed primary cases at a 1.25 ms step. The previous 2.5 ms results reproduced exactly. Seed 904 smoothed steering then agreed within 0.049 mm, and seed 1002 inward steering within 0.019 mm. But seed 905 smoothed steering diverged by 8.594 m and changed from 50 to 49 finishers. Thus, reducing the step alone is not a general fix. The original failed tests remain failed, and the difficult seed 905 case is preserved for further diagnosis.

[Predeclared diagnostic](research-block-refinement-audit-protocol.json) · [Full states](research-block-refinement-audit-runs.json) · [Comparison](research-block-refinement-audit.json)

## Evidence and reproducibility

- [3D replay](milestone-18-interior.html), [protocol](milestone-18-protocol.json), [per-case CSV](milestone-18-case-table.csv)
- [Full states and samples](milestone-18-study.json), [refinements](milestone-18-refinements.json), [verification](milestone-18-verification.json)
- [Simulator](milestone-18-source/sim.cjs), [steering components](milestone-18-source/continuous.cjs), [run script](milestone-18-source/study.cjs)

All seeds and unsuccessful variants are retained. No claim of arbitrary-terrain navigation, unknown-map planning, dense-swarm scalability, flight safety, aerodynamic fidelity or novelty follows from these experiments.
