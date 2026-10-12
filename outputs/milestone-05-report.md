# Milestone 5 — more passage with fewer pauses

## Plain-language result

**The new schedule improves passage counts in 165/180 matched cases, ties in 15, and moves fewer drones in 0.** It does this with the same requested-speed cap, vehicle mechanics, batch capacities and separation checks. Across all 180 new runs, there are 0 contact/model stops, 0 cases entering the 20 cm desired-separation threshold and 0 cases with an invalid gate crossing. Minimum measured separation is 0.2905 m.

All 50 drones pass within 60 seconds in **30/180** new runs, versus **15/180** cautious runs. This is an improvement, not completion of the crowded-passage problem. Narrow openings still leave a queue.

The displayed examples use seed 1, 0.6 m initial spacing and 0.5 m/s requested speed:

| Opening | Cautious count / 50 | Fewer-pauses count / 50 |
|---|---|---|
| 0.6 m | 14 | 19 |
| 1.2 m | 20 | 25 |
| 2.4 m | 40 | 50 |

In the wide example, the new rule completes all 50 valid crossings at approximately 47.00 simulated seconds, then keeps simulating through the full 60-second horizon. No early success termination is used.

## Goal

Continue Step 5 of the original research plan: improve the slow, conservative merging reference without concealing failures or raising the hardware or speed settings. The goal here is controller efficiency in a simplified environment. It does not establish aerodynamic accuracy, real-flight safety, optimality or novelty.

## What changed

Both algorithms remain centralized batch schedulers with exact state information. Both allow at most two, four or five drones per batch for 0.6, 1.2 or 2.4 m openings. The new rule reduces pauses by changing several staging/readiness thresholds together:

| Decision | Previous cautious scheduler | New schedule |
|---|---|---|
| Front-row readiness | Within 3.5 cm of x = −1.2 m and longitudinal speed below 0.06 m/s | Front-row centers have reached x ≥ −1.35 m; no requirement to halt |
| Begin lateral alignment | x > −0.61 m | x > −0.80 m |
| Longitudinal staging reference | x = −0.45 m | x = −0.25 m |
| Admit a vehicle into passage | Lateral error < 2 cm, lateral speed < 0.06 m/s; staging error < 5 cm and longitudinal speed < 0.06 m/s | Same lateral position tolerance, lateral speed < 0.10 m/s and x > −0.65 m; no full longitudinal stop required |
| Release next batch | Every previous-batch center is beyond x = 0.45 m | Every previous-batch center is beyond x = 0.05 m |

The earlier batch-release point refers to centers, not full-body clearance. It permits the next group to start approaching from upstream; it does not instantly put that group at the gate. The full trajectories still undergo the unchanged swept separation checks. The relaxed lateral-velocity readiness threshold is explicitly part of this intervention; only the geometric contact/separation thresholds remain unchanged.

This is a combined controller change, not an ablation proving which threshold causes each gain. The new thresholds were chosen using twelve seed-1 pilot conditions, then fixed for the full comparison. There was no subsequent selection of a best seed or removal of failed cases.

## Experiment and reproducibility

- 180 paired configurations: three gate widths × two initial spacings (0.3, 0.6 m) × two requested speeds (0.25, 0.5 m/s) × fifteen seeds. The 120 cautious records for seeds 1–10 are reused from milestone 4; 60 cautious records for seeds 11–15 and all 180 new-controller records are newly computed. Thus this milestone adds 240 main simulations plus replays and verification runs.
- Seeds 11–15 were not used in the seed-1 design pilot. In those 60 additional cases, 55 improve, 5 tie and 0 worsen; 0 new-controller runs stop. These seeds change only initial lateral/altitude offsets by up to 5 mm. They are not a sensor-noise, delay, wind or hardware-validation test.
- Every pair starts from exactly the same 50 vehicle positions. Initial layout, gate and measurements are unchanged from milestone 4. Flight remains near a single nominal height of 1.2 m; this is 3D rigid-body physics/rendering, not yet a volumetric multi-height swarm.
- Same 27 g model, gravity, quaternion attitude, four motor states, 40 ms motor lag, motor allocation limits, 10 ms control updates and 10 ms RK4 integration. The same 2.25 thrust-to-weight command bound and horizontal reference-speed cap are retained. Actual velocity follows dynamics and is not forcibly clipped to the requested speed.
- Same 60-second horizon and stop criteria. Count unique forward crossings inside the virtual opening with 7.5 cm body clearance; retain invalid crossings separately. Every vehicle remains in the physical calculation after crossing. No wall or collision-impact response is modeled.
- Pair separation uses the closest point on a relative line segment over each integration step, approximating curved within-step motion. Stop at the first 15 cm contact envelope or model limit; report pairs below the unchanged 20 cm desired separation. All failures, if any, are retained.
- Full-horizon throughput is crossing count / 60 s, even for a stopped run. Complete-group passage time is reported only when all 50 have valid crossings. A low-contact run that leaves drones waiting is not labeled successful whole-group completion.
- Controller-specific lateral/altitude reference RMS is kept in raw records but not used to rank the algorithms, because their references differ.

## Results by condition

Each row includes all fifteen seeds. Counts are descriptive means and ranges, not confidence bounds on real flight. Pooled counts across this selected grid do not estimate a general probability of safety.

| Width (m) | Spacing (m) | Requested speed (m/s) | Cautious mean passed / 50 | New mean passed / 50 | New range | New all 50 passed |
|---|---|---|---|---|---|---|
| 0.6 | 0.3 | 0.25 | 10.00 | 14.00 | 14–14 | 0/15 |
| 0.6 | 0.3 | 0.5 | 16.87 | 24.00 | 24–24 | 0/15 |
| 0.6 | 0.6 | 0.25 | 9.00 | 10.00 | 10–10 | 0/15 |
| 0.6 | 0.6 | 0.5 | 14.00 | 19.00 | 19–19 | 0/15 |
| 1.2 | 0.3 | 0.25 | 15.00 | 20.00 | 20–20 | 0/15 |
| 1.2 | 0.3 | 0.5 | 24.00 | 34.00 | 34–34 | 0/15 |
| 1.2 | 0.6 | 0.25 | 14.00 | 15.00 | 15–15 | 0/15 |
| 1.2 | 0.6 | 0.5 | 20.00 | 25.00 | 25–25 | 0/15 |
| 2.4 | 0.3 | 0.25 | 30.00 | 45.00 | 45–45 | 0/15 |
| 2.4 | 0.3 | 0.5 | 50.00 | 50.00 | 50–50 | 15/15 |
| 2.4 | 0.6 | 0.25 | 25.00 | 35.00 | 35–35 | 0/15 |
| 2.4 | 0.6 | 0.5 | 40.00 | 50.00 | 50–50 | 15/15 |

The split and each paired difference are retained in the CSV/JSON. No broad performance or CPU/GPU acceleration claim is made.

## Numerical checks

9/9 checks passed. They cover exact initial-state pairing, all planned configurations, finite metrics and arithmetic, 50-vehicle replay records/endpoints, independent reproduction of the three previous cautious examples, reservation phase ordering/capacity, and time-step refinement.

Refinement uses 10, 5 and 2.5 ms integration with fixed 10 ms control updates for the three displayed new-controller examples plus one dense narrow case at seed 11 (spacing 0.3 m, requested speed 0.5 m/s). Maximum successive final-position difference is 2.6e-08 m; maximum 5 vs 2.5 ms crossing-time difference is 8.81e-07 s. The checks require unchanged counts/stops, final differences below 1 cm and crossing-time differences below 0.05 s. Detailed pass/fail records are retained; this is numerical verification, not physical validation. It does not refine every one of the 180 cases.

The 3D comparison renders the actual recorded trajectories at a shared time using Three.js/WebGL. Displayed states interpolate 0.1-second samples; physics uses finer steps. The CPU study runs independently of animation frame rate. A stopped run, if present, freezes visibly while the other continues.

## Conclusion and implications

Removing conservative pauses improves passage counts in the tested cases without triggering the unchanged proximity criteria. This makes the reference more useful for later comparisons, while preserving the distinction between avoiding contact and moving all drones through within a deadline.

The result is limited to exact-state, undisturbed simulation. The next useful milestone is a paired robustness study with explicitly defined position errors and timing delays, again with a 3D update. Dense volumetric motion and aerodynamic interactions remain separate unresolved questions. Steps 3–4 still require physical evidence, and neither Step 5 completion nor overall conceptual feasibility is declared here.

## Reproduce

From the workspace root:

```
node outputs/milestone-05-source/study.cjs
```

The study uses four worker threads for independent cases. It requires the preserved milestone-4 records and local physics source, but no external npm dependencies. The protocol records the scheduler hash before running the cases. Serve the workspace over HTTP to load the vendored Three.js modules.

- [Interactive comparison](milestone-05-flow.html)
- [Paired CSV](milestone-05-study.csv)
- [Full records](milestone-05-study.json)
- [Checks and source hashes](milestone-05-verification.json)
- [Comparison protocol](milestone-05-protocol.json)
- [Scheduler](milestone-05-source/scheduler.cjs)
- [Study runner](milestone-05-source/study.cjs)

## Browser verification

Verified the page, both Three.js views, shared playback/pause, restart, exact 60-second endpoints for all three presets, and the new 30-second comparison shortcut in the Codex in-app browser. Desktop 1440 × 1000, mobile 390 × 844 and the default panel were checked. Both mobile canvases fit without horizontal overflow. No browser console warnings/errors were observed. All local deliverable links resolve to saved files. The saved desktop preview was inspected visually. Other browsers and sustained rendering performance remain untested.
