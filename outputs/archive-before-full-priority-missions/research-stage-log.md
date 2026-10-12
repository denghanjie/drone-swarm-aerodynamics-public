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

## Research block22–23 — 12 October2026

**56 runs retained.** Checkpoint22 tests local constant-velocity position prediction in16 development runs. All three100ms predicted cases finish, but1103 fails the planned final-position comparison; a separate0.625ms audit agrees with1.25ms. A200ms prediction contact occurs where raw observations finish. Seven of eight planned refinements pass. [Report](milestone-22-report.md) · [3D replay](milestone-22-lab.html).

Checkpoint23 freezes the same source before six fresh seeds across tight/slalom courses at100ms:24 primary runs and14 planned refinements. Raw11/12 and prediction11/12 complete flocks. 13/14 planned comparisons pass. Another1 post-hoc raw-stop refinements are saved separately, with1/1 passing. [Report](milestone-23-report.md) · [3D replay](milestone-23-lab.html).

Decision: retain both observer variants as experimental; no universal promotion. Return research priority to the physical measurement gate. Direct dataset retrieval yields human verification, not raw observations. No physical-validation, novel-algorithm or browser-scaling claim is made.

[Block summary](research-block-22-23-summary.md) · [Trial table](research-block-22-23-trials.csv) · [QA](research-block-22-23-qa.md) · [Artifact checks](research-block-22-23-artifact-checks.json).


## Milestone 24 — factory benchmark (12 October 2026)

Created the active complex-environment goal at the user's request. The synthetic factory has 34 solid collision-checked boxes, three offset 5×4 m doorways, storage racks, machinery and overhead structures. All drones use local Boids, common route guidance and a local heuristic avoidance filter; there are no per-drone trajectories or passage schedules. Airflow remains off.

All 16 prescribed runs completed. Full-Boids missions passed in all three seeds at both 50 and 200 drones. All six 50-drone social ablations also completed: this course does not establish a passage advantage for Boids. All primary cases retained full sampled connectivity. Three of four prescribed numerical comparisons passed. The 200-drone seed 1302 comparison failed the 1 cm endpoint threshold with a 2.728 cm difference despite identical 200/200 completion and no contact at both steps. This failure is retained; larger-count trajectory reliability is not established.

Six numerical implementation checks and 19 artifact checks passed. All 12 exact primary replays were checked in the viewer, with desktop/mobile screenshots and UI outcomes saved. Historical failures remain unchanged. Next: independently labeled finer-step audit of the 200-drone discrepancy and isolated actual-pipeline timing at 50/200/1,000/5,000 before expensive large-flock missions. The active goal and original eight-step study remain incomplete.

[Milestone report](milestone-24-report.md) · [3D replay](milestone-24-lab.html) · [Protocol](milestone-24-protocol.json) · [QA](milestone-24-qa.md) · [Artifact checks](milestone-24-artifact-checks.json) · [Active goal](research-complex-environment-goal.md).


## Milestone 25 — actual flock scaling and finer-step audit (12 October 2026)

The frozen study completed 13 new runs. A post-hoc 200-drone refinement at 1.25 ms agrees with the prior 2.5 ms case to 1.016 mm and both finish 200/200 without contact. The earlier 5→2.5 ms failure remains retained; a fine-step success does not establish reliability at all counts.

Three serial two-second timing repeats per count use actual local Boids, RK4 bodies, contact checks and measurements. Median wall times: 50 drones 0.686 s; 200 drones 2.877 s; 1,000 drones 18.164 s; 5,000 drones 104.863 s. All windows reach two seconds without a contact stop. The early windows are before the first partition, not full-course mission evidence. Increasing count increases initial cloud volume at nominal 0.75 m spacing; local neighbor counts also grow as the boundary fraction changes. At 5,000, steering accounts for most measured cost. The previous scheduled-queue benchmark is not reused.

The new Three.js viewer shows exact recorded trajectories at all four counts plus the full 200-drone audit. Browser rendering measurements are saved separately from offline physics. No aerodynamic or real-flight validation is claimed. Next: full 1,000/5,000 mission attempts with memory-bounded recording, difficult passage variants and clearly labeled aerodynamic comparisons. The active goal remains open.

[Report](milestone-25-report.md) · [3D viewer](milestone-25-lab.html) · [Frozen protocol](milestone-25-protocol.json) · [Serial timings](milestone-25-scaling.json) · [Numerical audit](milestone-25-audit.json) · [QA](milestone-25-qa.md).


## Block26–29 — initial progress record (superseded by completion below)

Milestone26 currently has9/11 completed runs. All four50-drone cases and both200-drone primary cases finish. The1,000-drone primary stops at16.020s at partition-0-above; the finer run repeats the same drone296/wall event at16.01875s, with1.067mm maximum endpoint difference. The200-drone narrow refinement also finishes, but its5.445cm endpoint difference fails the1cm threshold. The two5,000 runs are still computing. Available comparisons and diagnostic limitations are saved; no partial run is counted as a completed mission.

Milestone27 is retained with an explicit implementation-error warning. Direct inspection of the published wake-geometry diagram found adjacent-motor spacing was used where opposite-motor spacing is required. This also affects earlier illustrative pair examples using the same mapping. Navigation and airflow-off results are unaffected. Milestone28 freezes25 paired reruns with the corrected length; all geometry, power, zero-flow and terminal-recording development checks pass. The corrected study is queued after27 to limit concurrent load. Sources, original results, the paper hash and correction rationale are preserved.

Milestone29 has a frozen48-case serial timing protocol: four counts50/200/1,000/5,000, four corrected aerodynamic variants, three one-second repeats. It must start only after other numerical studies terminate; it is not yet executed. This will separate actual physics computation from the already measured Three.js replay cost.

3D viewers now end their timeline at the recorded stop, name the affected drone/solid and show stop markers through occluding walls. The milestone27 correction warning and contact marker were verified in the browser. Final all-case/mobile audits and the consolidated immutable manifest await completed studies. The previous manifest is preserved in archive-before-full-missions and remains a pre-block snapshot.

[Mission report](milestone-26-report.md) · [3D missions](milestone-26-lab.html) · [Normalization correction](research-wake-normalization-correction.md) · [Corrected protocol](milestone-28-protocol.json) · [Cost protocol](milestone-29-protocol.json) · [Prior-art assessment](research-contribution-assessment.md).


### Live-record integrity update

The manifest utility now accepts explicitly declared live stages. It pins completed trial files and stable source/report artifacts, lists excluded mutable outputs with reasons, and writes the snapshot atomically. The reproduction helper separately verifies every protocol-pinned numerical source. The first live snapshot verified974 files with no changes/missing files;65 mutable outputs were explicitly excluded for26/27/28. The pre-block manifest is preserved. This is an incremental integrity check, not final completion or physical validation. The [requirement audit](research-goal-completion-audit.md) lists the evidence still needed before the active goal can be closed.


### Original airflow study terminated; full corrected study started

After verifying the wake geometry error, the remaining erroneous-model calculations were deliberately stopped to prioritize corrected evidence. The20 primary cases were completed and preserved. Five refinement/cadence cases were not completed; any partial Float64 file is listed in `milestone-27-termination.json` and is not a completed result. Both the old parent and waiting launcher exited with code143; the numerical child was separately signaled and its disappearance checked. The two5,000 navigation jobs were unaffected.

Milestone28 is now running its full frozen25-case protocol directly. The earlier plan to finish the erroneous study before starting28 has been superseded; the correction audit retains the history. Paired correction analysis uses only original cases with completed records, and does not fabricate original refinement outcomes. The stage27 reproduction helper repeats its20 completed cases only; stage28 remains the full corrected experiment. The terminal27 artifact audit passes162 checks, including complete accounting of all25 planned jobs as20 completed plus five uncompleted.


### Milestone26 complete — retained large-flock failures

All11 planned runs finished.50/200 primary cases complete;1,000 and5,000 hit the upper first partition. The5,000 refinement repeats drone4215 at11.95125s versus11.9525s, with1.084mm endpoint difference. The original20s-checkpoint comparison remains unavailable/failed. Its prewritten early-stop supplement is reported separately.85 artifact checks pass, and all11 outcomes were checked in Three.js. The200 narrow endpoint comparison still fails. Corrected airflow28 and isolated timing29 remain pending.


### Milestone28 complete; serial cost study29 started

All25 corrected cases finished. Five primary airflow-off missions complete; all15 active-airflow primary cases stop early. Four physics-step comparisons pass, but the separate airflow-refresh comparison fails:7.76875→8.99375s stop time and0.92035m unequal-time endpoint difference. This cadence sensitivity remains an explicit limitation.202 artifact checks and20 paired correction checks pass. All25 replay outcomes were checked in Three.js.

Both numerical study handles26 and28 returned exit0 before launching29. The48 timing jobs now execute as serial child processes; background OS/browser work remains uncontrolled. No overlap with the prior mission integrations occurs. Early workload exits are retained and excluded from full-window performance rankings.


## Block26–29 completed — 12 October 2026

All planned corrected studies are complete: 11 mission cases, 25 corrected-airflow cases and 48 serial workload records. The 20 completed erroneous-model cases and five uncompleted refinements remain explicitly historical. There are 104 completed executions and five uncompleted original cases in the consolidated trial index.

The final workload audit passes 389 checks. All 52 representative visible outcomes across26/28/29 match their raw records; desktop/mobile screenshots and exact replays are saved. Runtime repetitions reproduce the same simulated states/outcomes but vary substantially in wall time. For one simulated second at5,000 drones, the no-airflow median is133.943s (range47.241–208.680), and force-only median297.441s (range128.811–477.183). Turning-moment/alternative-overlap windows stop early and are not ranked as full workloads. Background host load is uncontrolled.

The benchmark goal is supported by the saved evidence, including navigation failures and failed numerical criteria. The original eight-step programme remains open: independent physical validation, robust general navigation, current-pipeline GPU validation and a defensible novelty claim are unestablished. See the [plain-language synthesis](research-block-26-29-summary.md), [trial CSV](research-block-26-29-trials.csv), [final cost report](milestone-29-report.md) and [completion audit](research-goal-completion-audit.md).

## Milestone 30 started — 12 October 2026

The next bounded goal tests a wall-priority correction to the retained local avoidance filter. The historical26/28/29 numerical sources remain unchanged. The corrected ten-case protocol freezes two development runs, six held-out primary comparisons and two refinements. Large flocks use20-second windows;50-drone runs use180seconds. This is a controller experiment without airflow, not completion of physical validation.

The first implementation attempt mishandled a geometry normal with17entries and produced invalid commands. Its source, protocol and attempted outputs are retained in `milestone-30-error-record/`. The corrected interface uses spatial components, passes integration checks through5,000drones, and replaces attempted evaluation seeds1801/1802 with1901/1902 before refreezing. An independent active-set reference agrees on200feasible generated projection problems (maximum discrepancy1.41e-9m/s). These mathematical checks do not establish dynamic safety.

## Milestone 30 complete — wall-priority experiment, 12 October 2026

All ten corrected protocol trials complete. The two fresh 1,000-drone baselines contact the upper first partition (15.98/15.3025s); both candidates reach 20 s without contact. The 1,000/5,000 development candidates also reach 20 s, and the 50-drone full mission finishes under both filters. The 50-drone repair is inactive and final states match exactly. The 1,000/50 candidate step refinements pass at common saved times (maximum position differences 3.616e-6/3.333e-6 m); this does not validate physical accuracy or the 5,000-drone candidate’s numerical convergence.

The source and artifact audit passes 157 checks; 21 solver/interface/equivalence checks pass; 200 independent projection-reference cases agree. Pre-contact traces retain the actual preceding commands for the two new baseline failures. An explicitly post-hoc progress check finds 437/441 fresh-seed drones beyond the first partition’s far face plus body radius at 20 s; this does not count factory completion.

Decision: advance the wall-priority candidate to full-duration large-flock testing. Do not claim generally safe navigation, aerodynamic validation or algorithmic novelty. Original 26/28/29 numerical sources are unchanged. The initial implementation error remains preserved as three invalid completed executions, two interrupted partial executions and five unstarted jobs. [Report](milestone-30-report.md) · [3D replay](milestone-30-lab.html) · [trial CSV](milestone-30-trials.csv).
