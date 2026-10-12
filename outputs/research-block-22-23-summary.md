# Research block 22–23 — prediction helps some flocks and hurts others

**The new rule is not a reliable replacement. We now have saved examples of both recovery and newly introduced contact.**

We completed 56 simulation runs: 16 development runs, 38 fresh-flock runs, one extra development refinement, and one separate audit of a new raw-observer failure. Both checkpoints include their own Three.js comparisons, source, protocols, full states, failure records and reports.

## What we tried

A delayed measurement tells a drone where its neighbors **were**. Our candidate estimates where they are **now** by continuing their last measured motion. It still uses only nearby drones, with separation, alignment and cohesion. No leader or central traffic scheduler is introduced.

## What we learned

|Milestone|Result|View it|
|---|---|---|
|22 — development|The saved 100 ms failure completes with prediction. At 200 ms prediction instead creates a contact failure. One planned trajectory comparison fails.|[Development replay](milestone-22-lab.html)|
|23 — fresh flocks|At 100 ms, the original completes 11/12 whole-flock runs; prediction completes 11/12. The same frozen rule is used on six new starting flocks and two courses.|[Fresh-flock replay](milestone-23-lab.html)|

Prediction changes failure into success in: **1203/tight**. It changes success into failure in: **1202/tight**. These matched cases are more informative than one attractive animation. They do not establish general superiority.

The two panels always use the **same observation delay**. Select a case and click **Contact moment** to inspect a stop; **Outcome ·60 s** shows the completed mission alongside any frozen failure. Every primary case is selectable, including unsuccessful ones.

## How much can we trust the calculations?

The six observer implementation checks pass. Seven of eight planned development refinements pass. In the exceptional recovered run, all 50 finish at both steps but the final positions differ by 55 cm. A separate, still finer step agrees with the middle step to 2.88e-08 m. That supports the finer calculation in this case; it does not erase the original discrepancy. Saved frames place the first 1 cm divergence after 27 s, well after the original 10.17 s contact time.

The fresh study passes 13/14 planned numerical comparisons. Seed 1201/tight with prediction finishes at both steps, but its final positions differ by 40 cm, so this comparison fails. Separate raw-failure audits pass 1/1. Numerical agreement means that repeating a calculation more finely gives the specified agreement. A contact can be numerically repeatable and still be a bad mission outcome. Passing these tests does not validate the physical model.

## Implication for the eight-step goal

We have a reproducible 3D local-flocking testbed and useful counterexamples. We have **not** established reliable passage, real-flight safety, aerodynamic accuracy, large-flock browser performance or novelty. Airflow is off in these navigation experiments.

The next major priority is the physical measurement gate. The published dataset URL now returns a human-verification page; measured files have not been acquired. The [saved validation contract](research-physical-validation-gate-2026-10-12.md) explains the necessary geometry, motor-input and force-response matching. A mean air-velocity equation alone cannot tell us how much thrust a receiving drone loses.

Further navigation tweaks should not indefinitely replace the original question: **how much airflow detail is necessary, and what does it cost to compute?** Prediction by itself is an established technique, not a novelty claim.

## Records

[22 report](milestone-22-report.md) · [23 report](milestone-23-report.md) · [Every planned trial](research-block-22-23-trials.csv) · [Development audit](milestone-22-refinement-audit.json) · [Fresh failure audit](milestone-23-failure-audit.json) · [Artifact checks](research-block-22-23-artifact-checks.json) · [Viewer QA](research-block-22-23-qa.md) · [Original roadmap](research-roadmap.md) · [Full history](research-stage-log.md) · [Previous block](research-block-19-21-summary.md).
