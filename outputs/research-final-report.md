# Research status — full flock passage demonstrated; accuracy unresolved

The complex-environment benchmark and the full-mission controller extension are complete. Local 3D flocks of up to 5,000 drones now finish the prescribed factory missions with the wall-priority controller. All three new trajectory-refinement comparisons fail, so precise motion remains numerically unresolved. Physical validation and the broader research programme remain open.

## Goal

Find out whether drones following local group rules can travel through a complex factory, what breaks as the flock grows, and what the computation costs. Establishing real aerodynamic accuracy requires independent measurements, which we do not yet have.

## Method

Each drone reacts to nearby drones using separation, alignment and cohesion—the three Boids rules. All receive the same broad route through a factory with 34 solid obstacles and three offset openings. Each computes its own motion; there are no individual flight schedules. A rigid-body model, motor lag and a local avoidance filter translate those preferences into movement.

Starting flocks, settings and acceptance thresholds were fixed before each study. We saved the source, states and exact replay frames. We separately checked finer physics steps, more frequent airflow updates and actual calculation time. Three.js displays recorded motion; it is not performing the research integrations live.

## Latest diagnostic — milestone 32

The [new Three.js wake lab](milestone-32-lab.html) shows mutual airflow influence in four historical 50-drone recordings and a static two-drone explorer. It reconstructs snapshot fields from exact poses using the corrected milestone 28 model. Those fields are not measured airflow or the original held rotor loads. Coupled historical flights still fail; the successful large wall-priority missions remain airflow-off.

Six new 1,000-drone continuations test the selected narrow-course interval from 20 to 30 seconds. At the same starting state, changing the step from 2.5 to 1.25 ms changes paths by at most 0.879 micrometres. At the same step, changing between the two historical starting states produces 4.85 cm divergence. This reproduces the historical difference and identifies inherited-state sensitivity as relevant in this window. It does not isolate a particular controller mechanism or prove chaos. All three milestone 31 trajectory criteria remain failed. [Summary](milestone-32-summary.md) · [Full evidence](milestone-32-report.md).

## Full-mission result — milestone 31

All ten frozen trials are saved. The corrected controller finishes every drone in all four primary cases without contact through 180 seconds. Fresh 1,000-drone wide/narrow cases finish by 109.75/149.77 seconds; the fresh 5,000-drone case by 168.4125 seconds. Their three matched baselines hit the first partition at 16.775/9.995/11.665 seconds. The reused development 5,000-drone flock finishes by 168.5625 seconds; its smallest sampled largest component is 4,999/5,000. The three fresh primary candidates remain connected at every science sample. These prescribed cases are not general safety rates.

**Both full 1,000-drone cases finish at both tested physics steps, but individual paths do not agree.** The two full 1,000-drone comparisons differ by up to 5.17/32.77 m; the 5,000-drone comparison differs by up to 7.98 m within its first 60 seconds. All fail the unchanged 1 cm criterion. The 60-second window cannot validate the later large-flock mission. Detailed error profiles, iteration-limit events and pair-request violations remain recorded. No cause of the sensitivity or physically correct trajectory has yet been established.

The controller, local Boids and broad shared route were fixed, with ideal observations and airflow off. No individual path or passage schedule was assigned. Numerical sources remain unchanged; 224 artifact checks pass. These checks verify software records, not flight accuracy. [Plain-language summary](milestone-31-summary.md) · [Three.js replay](milestone-31-lab.html) · [Detailed report](milestone-31-report.md) · [Next scientific gate](research-next-controller-gate.md).

## Historical benchmark results — milestones 26–29

**Small flocks get through; larger flocks reveal a navigation limit.** All six primary 50/200-drone cases in milestone 26 finish. The 1,000- and 5,000-drone cases contact the first partition at 16.020 s and 11.9525 s. Smaller physics steps repeat the same affected drone and wall with approximately 1 mm endpoint differences. Both flocks remain connected: staying together does not imply safe passage. Only one primary seed was tested at each large count.

**Numerical agreement is mixed.** The 200-drone narrow case completes at both physics steps, but final positions differ by 5.45 cm, exceeding the 1 cm criterion. The 5,000 primary stops before its prescribed 20 s comparison checkpoint; that original criterion remains unmet. Its early-stop comparison is a separately declared supplement.

**Airflow assumptions matter, but accuracy is unresolved.** All five corrected airflow-off primary cases finish; all 15 primary cases with active airflow stop by contact or a declared model limit. A model-limit stop means the state left the range we chose to model; it is not evidence that a real drone crashes at that instant. Four physics-step checks agree. However, updating the airflow every 5 ms instead of 10 ms changes one stopping time from 7.769 s to 8.994 s. We cannot call the airflow trajectories converged merely because smaller rigid-body steps agree.

We also found and corrected a wake-length mapping error: the paper specifies opposite-motor spacing, while the earlier implementation used adjacent spacing. The erroneous 20 primary runs and five uncompleted refinements remain labeled in milestone 27. The corrected 25-run study is milestone 28. Neither version is independent physical validation. The factory walls affect obstacle avoidance, but their effects on airflow are omitted. The receiver response, overlapping wakes and controller's limited compensation remain assumptions.

**Calculation and display have different costs.** The following are median wall times for one simulated second, with three serial repeats of the same startup scene. A stopped window is excluded from full-window rankings.

|Drones|No airflow|Mean wake: force|Mean wake: moments|Alternative overlap|
|---:|---:|---:|---:|---:|
|50|0.77 s|1.23 s|1.44 s|1.20 s|
|200|2.97 s|4.90 s|4.56 s|0/3 full windows; no matched cost|
|1000|8.99 s|23.01 s|0/3 full windows; no matched cost|0/3 full windows; no matched cost|
|5000|133.94 s|297.44 s|0/3 full windows; no matched cost|0/3 full windows; no matched cost|

These timings include local steering, physics, contact checks, airflow and in-memory recording. They exclude process startup, warmup and file serialization. Background operating-system/browser load is uncontrolled, and identical repeats show substantial runtime variation. These are descriptive session measurements rather than stable hardware guarantees. They measure startup scenes, not crowded doorways. Earlier replay measurements gave a median frame interval of about 16.7 ms at all four counts; that is display performance, not real-time simulation or GPU physics evidence.

## Conclusion and implications

The concept is achievable as an inspectable simulation benchmark, including nominal 5,000-drone factory passage with the corrected controller. Reliable navigation under realistic conditions, numerically resolved individual trajectories, accurate multi-drone aerodynamics and a new flocking algorithm remain unestablished. These failures identify where the setup needs improvement or validation; they do not prove that such flocks are physically impossible. The factory social-rule ablations also finish, so this course does not establish a passage advantage for Boids.

Further work is worthwhile if it targets the unresolved scientific questions: diagnose the long-horizon numerical sensitivity, obtain matched physical wake/force data, verify receiving-rotor response and airflow update convergence, then compare navigation/control baselines under frozen tests. More visual complexity alone would add little evidence. A defensible potential contribution is a validated accuracy-versus-cost comparison for local flocks; the accuracy half is still missing.

## Records and 3D views

- [Factory missions and large-flock failures](milestone-26-lab.html) · [report](milestone-26-report.md).
- [Corrected airflow comparison](milestone-28-lab.html) · [report](milestone-28-report.md).
- [Actual workload through 5,000 drones](milestone-29-lab.html) · [report](milestone-29-report.md).
- [All planned cases as CSV](research-block-26-29-trials.csv) · [Stage history](research-stage-log.md) · [eight-step roadmap](research-roadmap.md) · [completion audit](research-goal-completion-audit.md).
- [Correction record](research-wake-normalization-correction.md) · [prior-art assessment](research-contribution-assessment.md) · [physical measurement gate](research-physical-validation-gate-2026-10-12.md).
- [Artifact manifest](research-manifest.json) · [reproduction helper](research-reproduce.py).

This block retains 104 completed numerical executions: 11 mission cases, 20 erroneous-model historical cases, 25 corrected cases and 48 workload repeats. Five original erroneous-model refinements are explicitly uncompleted; they are not counted as results. Development checks and previous milestones are additional records.

## Controller extension — milestone 30

A final wall-clearance correction improves the retained early contact failures without changing the local 3D Boids or shared route. On fresh 1,000-drone seeds 1901/1902, the baselines contact the upper doorway wall at 15.98/15.3025seconds; both corrected runs reach 20 seconds without contact. The development 5,000-drone run also reaches20seconds, beyond its historical 11.9525-second contact. These are short windows, not full factory missions.

Both 50-drone full-mission variants finish, with identical final states because the repair is inactive there. The 1,000-drone 20-second and 50-drone 180-second refinements agree within 3.62/3.34 micrometres at exact common saved frames; this is numerical agreement, not measured physical accuracy. No 5,000-drone candidate refinement was prescribed.

All ten corrected trials are complete. The initial invalid implementation and its interrupted attempts are separately preserved. [Plain-language milestone report](milestone-30-report.md) · [3D replay](milestone-30-lab.html) · [next scientific gate](research-next-controller-gate.md). The 104 completed 26–29 executions above remain a separate historical block.

Milestone 31 adds ten completed trials separately from the 104 executions in block 26–29 and ten corrected milestone 30 trials. Its failures of numerical agreement remain failed, even though the prescribed primary candidate missions complete.
