# Milestone 31 — the flocks get through, but exact paths remain uncertain

**All ten planned trials are complete.** The corrected controller carries the tested flocks through the factory. Changing the physics time step, however, substantially changes individual paths. That limitation remains part of the result.

## Research goal

Find out whether the wall-clearance correction can carry an entire large flock through the factory, beyond the short initial tests.

## What we did

We kept the controller fixed and compared it with the original controller on identical starting flocks. Every drone still follows local 3D Boids rules, with the same broad route through 34 solid obstacles. No drone receives an individual flight schedule. We used ideal observations and no airflow, ran full missions for 180 simulated seconds, and repeated selected cases with a smaller physics step.

## What happened

|Fresh starting case|Original controller|Corrected controller|
|---|---|---|
|1,000 drones, wide openings|Wall contact at 16.775 s|All finish by 109.75 s|
|1,000 drones, narrow openings|Wall contact at 9.995 s|All finish by 149.77 s|
|5,000 drones, wide openings|Wall contact at 11.665 s|All finish by 168.4125 s|

All three corrected flocks remain contact-free through 180 seconds. A separate reused 5,000-drone development flock also finishes, by 168.5625 seconds. Its largest connected group briefly drops to 4,999/5,000 in the saved samples; the three fresh candidate flocks stay connected at every science sample. These few prescribed cases do not establish a success rate for other environments.

**The accuracy check fails in all three comparisons.** Halving the physics step changes matched-drone positions by up to 5.17 m for the wide 1,000-drone case, 32.77 m for the narrow case, and 7.98 m for the first 60 seconds of the 5,000-drone case. Our unchanged acceptance threshold was 1 cm. Both 1,000-drone versions still finish, but that agreement does not make their detailed paths trustworthy. The 5,000-drone refinement does not cover its full mission.

## Conclusion and implications

The controller correction is worth investigating: it fixes the observed passage failures in these idealized tests. We have demonstrated simulated group passage through this factory. We have not established precise trajectory accuracy, reliable navigation under realistic sensing or airflow, physical validation, or a new algorithm.

The next scientific task is to diagnose the numerical sensitivity and independently validate the physical interaction model. If we later evaluate whole-flock statistics instead of individual paths, those new criteria must be declared beforehand; they cannot erase this failed test. The original eight-step research programme remains open.

All failures, solver iteration-limit events, pair-request violations, source hashes, checkpoints and interim summaries are retained. The detailed report records 224 passing artifact checks; those verify the saved software evidence, not physical flight accuracy.

[Open the Three.js replay](milestone-31-lab.html) · [Detailed report](milestone-31-report.md) · [All trials](milestone-31-trials.csv) · [Numerical comparisons](milestone-31-comparisons.json) · [Passage figure](milestone-31-passage.pdf) · [Research history](research-stage-log.md) · [Next scientific gate](research-next-controller-gate.md).

[Final verification and screenshots](milestone-31-qa.md).
