# Research block 19–21 — better evidence, no claimed breakthrough

**The previous controller remains an experimental reference. The new alternatives were worse, and delayed information exposed a repeatable proximity failure.**

We completed 81 numerical runs across three checkpoints, including two exact replay regenerations. Every checkpoint has source, a frozen protocol, full final states, measurements, a plain-language report and a Three.js replay. Earlier failures remain available.

|Milestone|Question|Result|3D replay|
|---|---|---|---|
|19|Would smoother, simultaneous braking decisions make the flock reliable?|No. The candidate completed 84/150 passages at 5 ms versus 150/150 for the previous controller. All 6 candidate numerical comparisons failed.|[Compare filters](milestone-19-lab.html)|
|20|Would stronger center guidance or a fixed heading fix it?|Neither was sufficient. None of the variants completed all 50 drones in any of its tested runs. Only 1/18 numerical comparisons passed.|[Compare the two changes](milestone-20-lab.html)|
|21|Does the previous controller tolerate delayed observations?|All 8 no-delay and all 8 50 ms delay primary runs finished. At 100 ms, 7/8 finished; the remaining run reached the contact limit. The failure repeats at the finer step.|[See the retained contact case](milestone-21-lab.html)|

## The most useful new finding

In fresh starting flock 1103, a 100 ms delay causes two drones to cross the model's 15 cm center-distance limit at 10.1725 seconds. At the finer simulation step, the same failure occurs at the same time. With current observations, all 50 finish. That makes this a concrete controller limitation under the chosen delay model, not an animation glitch resolved by drawing more frames.

The red markers in the viewer identify the closest pair at the stop. Click **Contact moment** to inspect it, then **Outcome · 60 s** to see the no-delay flock finish while the failed simulation stays stopped. Other examples retain successful passage through the changing-height obstacle course.

## What passed, and what did not

The optimization, delay scheduling, frozen-source checks and replay checks pass their software tests. The unsuccessful controller variants fail the research acceptance tests and are rejected. Checkpoint 21 passes 8/8 preregistered numerical refinements. Its separate post-hoc audit passes both the no-delay and delayed-case refinements and reproduces both replays exactly. A numerical pass means the tested calculation agrees; it does not mean the mission succeeds or the physical model is validated.

These are local 3D Boids throughout: separation, alignment and cohesion use nearby drones. The map and route preferences are supplied. No central scheduler assigns passage slots. The viewer replays saved rigid-body motion computed in Node; it does not demonstrate live browser physics or GPU performance.

## Implications for the original goal

The original question is still how much aerodynamic detail is needed, and whether the actual flock calculation can run interactively in a browser. These checkpoints remain within Step 5 of the eight-step plan. Airflow is still off. Independent flight/force validation, coupled multi-wake accuracy, actual Boids GPU scaling and scientific novelty remain unresolved.

A newer measured-wake preprint has been added to the [physical-reference update](research-aerodynamics-update-2026-10-11.md). The preferred raw interaction dataset could not be retrieved in this session. The new paper's vehicle geometry differs from ours; its equations and dimensions must not be silently substituted and called validation.

The next useful work is a local delay-aware controller tested against the retained failure and untouched new cases, alongside obtaining an independent aerodynamic reference. Further visual polish or a bigger drone count would not by itself answer the research question.

## Records

[19 report](milestone-19-report.md) · [20 report](milestone-20-report.md) · [21 report](milestone-21-report.md) · [Numerical failure audit](milestone-21-failure-audit.json) · [Trial table](research-block-19-21-trials.csv) · [Software/viewer QA](research-block-19-21-qa.md) · [Original roadmap](research-roadmap.md) · [Full stage history](research-stage-log.md) · [Previous research block](research-block-15-18-summary.md).
