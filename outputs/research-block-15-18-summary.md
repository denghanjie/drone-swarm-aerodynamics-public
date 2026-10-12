# Larger research block — passage improved, whole-flock reliability remains open

We completed four connected checkpoints inside the original research Step 5. Each checkpoint has its own report, frozen inputs, saved results, source code and a Three.js replay. Earlier versions and unsuccessful experiments remain available.

## The question

Can we help a genuine local Boids flock pass through staggered openings without contact, stranding drones or breaking into separate groups—and can we reproduce the result when we make the physics calculation more precise?

## What we did and learned

|Checkpoint|Plain-language experiment|Finding|Saved 3D view|
|---|---|---|---|
|15|Replace abrupt steering changes with gradual changes, one component at a time.|Smoothing flocking and route steering helped the development case. Smoothing the clearance filter did not.|[Numerical diagnosis](milestone-15-diagnosis.html)|
|16|Pull the flock together more strongly and slow leaders when neighbors fall behind.|Apparently better completion concealed a failed numerical check and fragmentation. Stronger cohesion was not a reliable fix.|[Retention comparison](milestone-16-retention.html)|
|17|Test three fixed controllers on five new starting conditions in three courses.|In the narrow course, smoother steering improved completion from 179/250 to 249/250 without contact stops. However, two of its seven numerical checks failed. Stronger retention caused a fresh collision.|[Fresh three-course trials](milestone-17-fresh-trials.html)|
|18|Aim 10 cm inside the old steering boundary so the preferred path has room before the clearance rule brakes.|All 50 drones finished in each of eight fresh runs, versus 399/400 total for the reference. Two resulting flocks still split; one numerical check failed.|[Inward-offset comparison](milestone-18-interior.html)|

The sphere course, wide openings and narrow openings are distinct experiments. These stage labels are checkpoints within the original eight-step plan.

## The improvement—and its cost

The new inward offset recovered the two development stragglers and one fresh straggler. It does not assign any drone a passage slot or individual route.

But **finishing is not the same as staying together**. In fresh seed 1004, all 50 finished, yet the flock ended as two groups of 41 and 9. The matched reference stayed connected. Another candidate case ended 49+1. Across the eight runs, the candidate reduced the number of disconnected final flocks from four to two, but made the worst split larger.

The worst observed center separation also decreased from 25.7 cm to 19.8 cm; the modeled contact threshold is 15 cm. The smallest obstacle-envelope clearance decreased from 15.3 cm to 12.7 cm. Aiming farther inside an opening did not improve every actual clearance once the drones interacted.

For that reason, the inward offset remains an **experimental alternative**, and stronger retention is **rejected**. Neither is a universal solution to narrow-passage congestion.

## What the numerical checks mean

We first used a 5 ms physics step, then repeated selected cases at 2.5 ms, keeping the controller at 100 updates per second. The agreed test requires the final position of every drone to differ by less than 1 cm, with matching completion and stopping outcomes.

- Smoother steering passed 5/7 fresh checks. The other two had maximum path-end differences of 2.875 m and 8.51 cm, despite identical completion counts.
- The inward offset passed 5/6 checks. The failed case differed by 1.868 cm, again with 50/50 completions at both steps.
- Stronger retention failed 3/7 fresh checks and also reproduced its collision in the smaller-step run.

So the number arriving is more consistent than the detailed paths in these cases. We must account for this before claiming that a changed path was caused by a new aerodynamic model.

A further **post-hoc diagnostic** repeated the three failed primary cases at a 1.25 ms step. The previous 2.5 ms results reproduced exactly. Seed 904 smoothed steering then agreed within 0.049 mm, and seed 1002 inward steering within 0.019 mm. But seed 905 smoothed steering diverged by 8.594 m and changed from 50 to 49 finishers. Thus, reducing the step alone is not a general fix. The original failed tests remain failed, and the difficult seed 905 case is preserved for further diagnosis.

These tests measure consistency of our equations and code. They do not compare the drones against physical flight measurements.

## Research conclusion

**The concept is feasible as a reproducible 3D flocking simulation, and worth pursuing. The original aerodynamic research goal is not finished.** We now have a better-tested navigation experiment and concrete failure cases, rather than relying on a successful animation alone.

The drones use local separation, alignment and cohesion in x, y and z. Their aperture map and sphere-route preferences are programmed. The resulting individual paths and group shape arise from local interactions, but this is not unknown-terrain route discovery. Three.js replays the numerical runs; it is the visual layer, not the physics validator.

Airflow is still off, observations are ideal, and the current flock has not been validated against measured flight or benchmarked as a full Boids/aerodynamics pipeline at thousands of drones. Smoothing and clearance margins are established techniques; these improvements alone do not establish scientific novelty.

The next useful block should freeze these candidates and failure cases, test observation uncertainty, and secure an independent aerodynamic reference. Subsequent aerodynamic comparisons must separate model effects from numerical variability. The [eight-step roadmap](research-roadmap.md) retains those gates.

## Record and reproduction

The block contains 103 initial simulation executions, followed by 6 post-hoc refinement-audit executions and 2 exact replay regenerations. Repeated runs are not counted as independent evidence. Threshold probes and command regression checks are saved separately.

- [Checkpoint 15 report](milestone-15-report.md), [16](milestone-16-report.md), [17](milestone-17-report.md), [18](milestone-18-report.md)
- [Per-case table 17](milestone-17-case-table.csv), [table 18](milestone-18-case-table.csv)
- [Three-step diagnostic protocol](research-block-refinement-audit-protocol.json), [full audit states](research-block-refinement-audit-runs.json), [audit comparison](research-block-refinement-audit.json)
- [Unchanged physics dependencies](research-block-dependency-audit.json), [2,400 exact baseline-command comparisons](milestone-18-regression.json), [diagnostic replay equality](milestone-18-replay-check.json)
- [Stage history](research-stage-log.md), [file integrity manifest](research-manifest.json), [isolated reproduction helper](research-reproduce.py)
