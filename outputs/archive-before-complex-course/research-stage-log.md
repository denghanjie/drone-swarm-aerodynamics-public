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
