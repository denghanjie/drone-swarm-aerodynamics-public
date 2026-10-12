# Research stage record

This log is the entry point for regression and future continuation. Milestone numbers are delivery checkpoints, not the original eight step numbers. Milestones 1–6 predate this final research pass and remain preserved; their summaries link to their original evidence rather than pretending those studies were rerun today.

| Milestone | Question / outcome | Original plan | Record and 3D view |
|---|---|---|---|
| 1 — small group | Diagnostic mechanics and interaction sensitivity; numerical verification does not establish physical agreement. | 2–4 | [Summary](milestone-01-report.md), [3D](milestone-01-small-group.html) |
| 2 — evidence | No matched, validated airflow-to-force model established. Navigation work proceeds with airflow off. | 3–4 | [Evidence audit](milestone-02-evidence.md), [Review](milestone-02-evidence.html) |
| 3 — passage pilot | First 50-drone gate task; failures retained as a navigation baseline. | 5 | [Summary](milestone-03-report.md), [3D](milestone-03-passage.html) |
| 4 — orderly merging | Scheduled groups reduce contact failures, but passage remains slow. | 5 | [Summary](milestone-04-report.md), [3D](milestone-04-merging.html) |
| 5 — fewer pauses | 165 of 180 matched cases pass more drones, 15 tie; ideal information. | 5 | [Summary](milestone-05-report.md), [3D](milestone-05-flow.html) |
| 6 — imperfect information | Stronger bias/delay exposes invalid crossings and spacing breaches. | 5 | [Summary](milestone-06-report.md), [3D](milestone-06-robustness.html) |
| 7 — clearance candidate | 60 new-seed candidate cases avoid measured failures; stress-profile passage costs 34.6% relative to faster rule. | 5 | [Summary](milestone-07-report.md), [3D](milestone-07-clearance.html) |
| 8 — GPU mechanics | CPU/WGSL agreement passes at 50–5,000 independent bodies; isolated kernel timing only. | 6 | [Summary](milestone-08-report.md), [3D](milestone-08-compute.html) |
| 9 — loop scaling | CPU control + GPU mechanics + transfers + grid checks: faster than real-time computation at 1,000, below real time at 5,000 in a one-second queue test. | 7 | [Summary](milestone-09-report.md), [3D](milestone-09-scaling.html) |
| Final — feasibility decision | Engineering approach feasible; core aerodynamic accuracy question unanswered; novelty unestablished. | 8 | [Final report](research-final-report.md), [3D research dashboard](research-results.html) |

## Change and measurement trace, 2026-10-11

1. Milestone 7 candidate frozen before seeds 101–110. Lane/gate margins, position gain and release threshold changed together. Old controllers and all old result files retained. One old-controller contact failure appears in new seeds and remains in raw records.
2. Milestone 8 WGSL ports the existing rigid-body derivative and RK4 equations. Open-loop, fixed motor commands deliberately isolate integration. The initial timing run left the render loop active; an explicit render pause was added and measurements repeated. Both raw runs remain; the pinned result and report use the repeat. This was a measurement-isolation correction, not parameter tuning.
3. Milestone 9 adds swept spatial-grid pair detection. All-pairs comparisons verify it on 100 random cases plus a crossing test. Both CPU and GPU-assisted backends run the same scheduler. All 24 timing runs and all recorded trajectory frames are retained.
4. Rendering is measured separately, with 30 timed whole-queue draws per count. It is not conflated with compute timing or claimed as total application FPS.
5. The loopback benchmark server initially could not bind inside the execution sandbox. An approved loopback-only process now serves port 8875. No physics or numerical failure was hidden by this environment correction.
6. The related-work review found direct overlap with existing GPU/Boids/Three.js systems. The initial pasted conversation’s “no exact match” claim is not adopted. The DOI metadata was ultimately resolved through DataCite to a Brown repository page; web retrieval failed and an ordinary HTTPS GET returned 403. No access restriction was bypassed. The access record is preserved; this does not imply the dataset is unavailable to everyone.

7. The first final dashboard embedded milestone pages in an iframe. Browser console events occurred during frame navigation; it was replaced with a directly mounted Three.js comparison and links to the other viewers. The initial dashboard HTML is preserved for diagnosis.

## Trace and regression policy

- Read a stage’s protocol before interpreting its results. The same number in different stages may use different controllers, seeds, information profiles or horizons.
- Keep fixed inputs, seeds, integration/controller intervals and measured failure definitions when making a regression comparison.
- Re-run in a copied output tree. Do not overwrite the pinned outputs to make a revision look like the original experiment.
- The [file manifest](research-manifest.json) records SHA-256 hashes. [Verification/reproduction helper](research-reproduce.py) checks them and can create an isolated numerical reproduction.
- A numerical pass means implementation consistency. It does not grant physical validity, flight safety, optimality or novelty.


## 2026-10-11 — Milestone 10: Boids scope correction

Previous navigation and compute milestones are centralized/compute baselines, not evidence of Boids flocking or its GPU scaling. Overall completion framing withdrawn. Added genuine local separation, alignment and cohesion, matched scheduler and social-rules-off controls, 45 holdout cases, Three.js replays and local-neighbor visualization. Wide cases pass with and without social terms; narrower Boids cases fail. One numerical-refinement check fails and is retained. Original research remains ongoing.

[3D milestone](milestone-10-boids.html) · [Summary, methods, failures and next gate](milestone-10-report.md) · [Previous record](archive-before-boids/research-stage-log.md)


## 2026-10-11 — Milestone 11: volumetric flocking

Added scattered xyz starts, local xyz separation/alignment/cohesion and velocity tracking through existing rigid-body physics. Fifteen fresh cases compare full Boids, separation-only and all-off. Full Boids retains 50/50 connectivity and 99.2–99.9% terminal alignment in all five seeds. Separation-only remains less aligned and fragments; all-off contact-stops. Development ground-limit failures and the associated source are retained; revised environmental braking was tested on new seeds. Four final verification checks pass, including one trajectory refinement. No airflow or real-flight validation claim.

[Visible 3D milestone](milestone-11-flocking.html) · [Milestone summary and methods](milestone-11-report.md) · [Development failures](milestone-11-development-v1/milestone-11-study.json)


## 2026-10-11 — Milestone12: obstacles and volumetric openings

18 fresh matched cases501–503, full Boids versus separation-only with identical known-map guidance. All sphere/wide cases pass50/50 without contact stops. Narrow Boids passes11–15/50; comparison stops at drone contact. Narrow seed501 fails the1 cm refinement criterion (0.422 m terminal difference), although passage/stop counts agree. Failures and all sources retained. No physical validation, general navigation or novelty claim.

[3D demonstration](milestone-12-obstacles.html) · [Milestone summary](milestone-12-report.md) · [Verification](milestone-12-verification.json)


## 2026-10-11 — Milestone 13: sequential obstacle course

Added three offset spheres and two staggered wall openings at two widths.18 fixed cases, seeds601–603. Both controllers finish wider courses. Tight Boids wall-stops in two of three runs; simpler control performs better in those cases but drone-contact-stops in the third. All five checks pass, including refinement of displayed trajectories. Earlier narrow-case convergence failure remains unresolved.

[3D course](milestone-13-course.html) · [Milestone summary](milestone-13-report.md) · [Frozen protocol](milestone-13-protocol.json).


## 2026-10-11 — Milestone 14: local clearance priority

Two candidates and42 study cases retained. Obstacle-only filter rejected: all six tight tests stop at drone contact. Joint wall/neighbor filter records no contact stops in12 candidate cases and recovers a fresh wide-opening wall failure, but tight completion slows to31–32/50 and groups fragment. Tight seed801 fails refinement with2.489m terminal-position difference despite stable passage/no-stop outcomes. Candidate remains provisional; previous unresolved numerical issues are not closed.

[3D comparison](milestone-14-clearance.html) · [Milestone report and decision](milestone-14-report.md) · [First-candidate failures](milestone-14-failure-analysis.json).


## 2026-10-11 — larger convergence and local-passage block (completed; research ongoing)

Checkpoint15 isolated steering and filter transitions with10 development runs and threshold probes. Smoothed steering alone is promising; smoothing filtering is not supported. [Report](milestone-15-report.md) · [3D](milestone-15-diagnosis.html).

Checkpoint16 tested corrected retention on two development seeds at two physics steps. A coarse50/50 retention result changed to49/50 with12.13m endpoint disagreement. Primary smoothed steering remained49/50 with micrometer-scale numerical differences. [Report](milestone-16-report.md) · [3D](milestone-16-retention.html).

Checkpoint17 controller sources and fresh seeds901–905 were frozen before45 matched cases and14 refinements. Checkpoint18 is a separate follow-up hypothesis from the stranded development drones: guide10cm inside the filter boundary, retaining the filter and local Boids. It does not alter checkpoint17 sources/results. Protocols and incremental records are saved as each run finishes.


Final block record: 103 initial simulation executions, 6 additional numerical-audit runs and 2 exact diagnostic replay regenerations. Checkpoint17 smoother steering improved narrow completion179/250→249/250 at5ms but failed2/7 refinements. Retention contact-stopped on fresh seed901 and failed3/7 fresh refinements. Checkpoint18 inward steering reached400/400 completions in eight fresh cases, with two disconnected final flocks and a worst41+9 split. Its1/6 initial refinement failure shrank at finer steps, while the later seed905 smoothed-steering audit changed50 to49 completions. The original failed criteria are retained. No overall research completion, physical validation or novelty claim.

All four checkpoints have Three.js views. The latest view includes the deliberately retained fresh connectivity regression (seed1004), whose regenerated trajectories match the saved study exactly. Updated the current report and eight-step roadmap; widened whole-course camera framing, gated playback while records load, and fixed mobile selector overflow. [Consolidated summary](research-block-15-18-summary.md) · [Current 3D](research-results.html) · [Checkpoint17](milestone-17-report.md) · [Checkpoint18](milestone-18-report.md) · [Third-step audit](research-block-refinement-audit.json).

## Checkpoint19 — simultaneous soft filter rejected (11 October2026)

18 development runs completed. Mathematically verified soft optimization replaced sequential projections while preserving local Boids and inward map steering. At5ms it completed84/150 vs150/150 for the prior controller. All6 soft-filter refinements failed; seed1002 counts33→27→25. No contact stops in these18 runs. Prior controller passed all three2.5→1.25ms comparisons here, with its coarse1002 failure retained. [Summary](milestone-19-report.md) · [3D replay](milestone-19-lab.html) · [Protocol](milestone-19-protocol.json) · [Full records](milestone-19-study.json). Solver correctness is distinct from trajectory acceptance.

## Checkpoint20 — heading/centering diagnosis (11 October2026)

27 new development runs completed, plus checkpoint19 soft references reused. Fixed-heading, center-guidance and combined variants completed77/150,126/150 and128/150 at5ms respectively. Only1/18 new adjacent-step comparisons passed; no variant is promoted. All27 runs avoided a contact stop, which does not offset incomplete passage and numerical failures. [Summary](milestone-20-report.md) · [3D replay](milestone-20-lab.html) · [Protocol](milestone-20-protocol.json) · [Full records](milestone-20-study.json). Center guidance also changes the existing forward slowdown; this is not a pure lateral-gain ablation.

## Checkpoint21 — fresh delayed-observation study (11 October2026)

24 fresh primary runs plus8 preregistered refinements completed. All eight0ms and eight50ms cases finished50/50; seven of eight100ms cases finished. Seed1103/tight/100ms reached the0.15m drone-contact envelope at10.1725s. A separately frozen four-run audit reproduced both ideal/failure replays exactly and repeated the contact stop at1.25ms at the same time. All8 preregistered and2 audit refinements pass numerical acceptance. This confirms a modeled delay vulnerability, not physical validation. [Summary](milestone-21-report.md) · [3D replay](milestone-21-lab.html) · [Protocol](milestone-21-protocol.json) · [Full records](milestone-21-study.json) · [Post-hoc audit](milestone-21-failure-audit.json).

Block19–21 total:81 numerical executions, including two exact replay regenerations. All milestones have saved source, protocols, results, reports and Three.js replays. [Consolidated summary](research-block-19-21-summary.md). Original eight-step research remains ongoing.
