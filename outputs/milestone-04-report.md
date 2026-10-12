# Milestone 4 — orderly merging, paired with the previous baseline

## Plain-language result

**Scheduling removes contact-envelope stops in all 120 tested starting conditions, at a cost in passage speed in some conditions.** This is a useful conservative reference, not a finished high-throughput controller.

The previous reactive controller stopped in 83/120 runs. The scheduled controller stopped in 0/120, had no invalid gate crossings, and never entered the 20 cm desired-separation threshold. Its smallest measured center separation across the study was 0.2910 m. Nevertheless, only **10/120 scheduled runs cleared all 50 drones within 60 seconds**. The previous controller had 31/120 runs with all 50 valid passages, no stop and no invalid crossing. Avoiding contact and completing the passage task are distinct outcomes; the scheduler does not improve both everywhere.

The default 3D example uses the narrow 0.6 m opening, spacing 0.6 m, speed 0.5 m/s and seed 1. The old controller stops at 3.26 s after one valid passage; the new controller records 14 valid passages over 60 s without contact. In the displayed wide example, the counts are 50 old versus 40 scheduled. Airflow remains off.

## Goal and comparison design

Continue Step 5 of the original eight-step plan: isolate how navigation changes passage outcomes before introducing uncertain aerodynamic forces. Compare an intentionally basic reactive baseline with a conservative central reservation scheduler, using the exact same vehicle mechanics, initial conditions, horizon, integration step and stopping criteria. Prior milestone results are retained unmodified.

This is a system-level controller comparison. The scheduler uses global exact state information and explicit batch reservations. It is not an ablation that attributes all improvement to a single parameter, nor a comparison of equally decentralized algorithms. It is not a novelty claim.

## What the new controller does

1. Keep waiting vehicles at their original lateral positions and queued row spacing.
2. Reserve a small batch from the front row. The maximum batch size is 2, 4 or 5 for openings of 0.6, 1.2 or 2.4 m, respectively. Lane spacing is at least 0.3 m by construction for these configurations, with the same 7.5 cm body clearance plus a 4 cm edge margin.
3. Move the batch forward to a staging line near x = −0.45 m, keeping original lateral positions until x > −0.61 m.
4. Align each reserved drone to its lane while holding near the staging line. Permit forward passage only once lateral error is below 2 cm, lateral speed below 0.06 m/s, longitudinal staging error below 5 cm and longitudinal speed below 0.06 m/s.
5. Wait until every drone in the batch reaches x > 0.45 m before reserving the next batch. Advance waiting rows when the previous front row has fully cleared.

The scheduler changes reference velocities, not positions. The 6-DOF dynamics, attitude controller, four motor thrust states and motor lag still determine actual motion. The global horizontal velocity command remains capped at the selected speed. Waiting vehicles are controlled in hover rather than frozen in the physics.

**Why the narrow reactive case fails:** its five lateral target lanes are only 9.25 cm apart. It steers every row inward at once, despite the 15 cm contact envelope. In the displayed seed-1 run, the first contact envelope is between zero-based vehicle IDs 46 and 48 in the rear row, before those vehicles reach the gate. The new rule avoids squeezing waiting rows together and permits at most two drones in the narrow opening. The replay's “Inspect old stop” button frames that actual encounter in both scenes.

This pilot uses nominally horizontal flight at z = 1.2 m, with small initial altitude perturbations. It has 3D rigid-body mechanics and 3D visualization, but it is **not yet a volumetric swarm with multiple planned flight heights**.

## Conditions and metrics

- 50 drones; 60-second horizon; widths 0.6, 1.2, 2.4 m; gate height 1.2 m; spacings 0.3, 0.6 m; requested speeds 0.25, 0.5 m/s; ten seeds per condition. This yields 120 paired cases (120 preserved reactive plus 120 new scheduled runs).
- Identical initial states in each pair: 10-by-5 horizontal grid, front row at x = −1.2 m, independent lateral/altitude offsets up to 5 mm. Seeds 1–10 are repeatability cases; they are not held-out physical validation data. Seed-1 examples informed implementation checks before the full sweep.
- Unchanged 27 g mechanics from `step02c-source/physics.cjs`, RK4 at 10 ms, control at 10 ms, 40 ms motor time constant, thrust-to-weight command bound 2.25. No saturation was observed in the scheduled cases.
- Unique valid forward crossings require the drone center to fit inside the opening with 7.5 cm clearance. Invalid-crossing drones are reported separately. Stopped runs retain every crossing before the stop.
- Separation is the minimum over swept linear relative-motion segments within integration steps. This approximates curved motion over each small step. Contact envelope: 15 cm; desired separation: 20 cm. These are conservative geometric envelopes, not simulated physical impacts.
- Both controllers stop on first contact-envelope detection or vehicle model limit. A stop is recorded at the integration-step endpoint. No wall or impact dynamics are simulated; the opening is a measurement plane.
- Passage counts and throughput use the full 60-second denominator, even for a stopped run. A comparison of stopped versus continuing cases measures achieved task outcome under this rule, not unconstrained steady-state flow capacity.
- Tracking RMS in each record is against that controller's current lateral reference and common altitude reference. References differ, so this metric is not used to rank the controllers here.

## Full comparison

Values are means over ten seeds. Descriptive ranges reflect these small initial perturbations, not physical uncertainty or statistical safety bounds. No run is discarded.

| Width (m) | Spacing (m) | Speed (m/s) | Old mean passed / 50 | Scheduled mean passed / 50 | Scheduled range | Old contact stops | Scheduled all 50 passed |
|---|---|---|---|---|---|---|---|
| 0.6 | 0.3 | 0.25 | 0.0 | 10.0 | 10–10 | 10/10 | 0/10 |
| 0.6 | 0.3 | 0.5 | 0.0 | 16.8 | 15–17 | 10/10 | 0/10 |
| 0.6 | 0.6 | 0.25 | 1.0 | 9.0 | 9–9 | 10/10 | 0/10 |
| 0.6 | 0.6 | 0.5 | 1.0 | 14.0 | 14–14 | 10/10 | 0/10 |
| 1.2 | 0.3 | 0.25 | 0.0 | 15.0 | 15–15 | 10/10 | 0/10 |
| 1.2 | 0.3 | 0.5 | 0.0 | 24.0 | 24–24 | 10/10 | 0/10 |
| 1.2 | 0.6 | 0.25 | 44.6 | 14.0 | 14–14 | 2/10 | 0/10 |
| 1.2 | 0.6 | 0.5 | 5.2 | 20.0 | 20–20 | 10/10 | 0/10 |
| 2.4 | 0.3 | 0.25 | 46.0 | 30.0 | 30–30 | 1/10 | 0/10 |
| 2.4 | 0.3 | 0.5 | 12.6 | 50.0 | 50–50 | 10/10 | 10/10 |
| 2.4 | 0.6 | 0.25 | 50.0 | 25.0 | 25–25 | 0/10 | 0/10 |
| 2.4 | 0.6 | 0.5 | 50.0 | 40.0 | 40–40 | 0/10 | 0/10 |

All scheduled rows have zero contact stops, zero close pairs below 20 cm and zero invalid crossings. The throughput in drones/s is each count divided by 60. The scheduler can improve or reduce passage count depending on the condition; no universal throughput improvement is claimed.

## Verification

Eleven numerical and bookkeeping checks passed:

- Exact equality of initial positions for all 120 pairs; finite metrics; correct replay sizes and endpoint times.
- New reactive-code path reproduces the saved metrics and crossing times of all three displayed reactive examples exactly.
- Scheduled examples at all three widths preserve their passage counts and stop outcomes when integration steps are reduced from 10 to 5 to 2.5 ms, retaining 10 ms control updates. Maximum final-position difference across successive refinements is below 1.3e−8 m; maximum 5 vs 2.5 ms crossing-time difference is below 1.9e−7 s. This very close numerical agreement does not measure physical accuracy. Only the displayed scheduled examples receive this refinement check, not all 120 runs.
- Initial reservation behavior, the 2/4/5 batch capacities, reservation event ordering and capacity limits across all event traces, and paired count/throughput consistency.

The visualization replays 0.1-second saved samples with interpolated positions and quaternion attitudes. Both scenes share a clock. A stopped reactive scene remains frozen at its recorded endpoint; the scheduled scene continues. Computation is CPU-based and rendering is Three.js/WebGL; no WebGPU or performance claim is made.

## Conclusion and next research decision

A conservative global scheduler gives us a contact-free reference over these tested cases. The outcome is consistent with the idea that coordinated merging can overcome failures of naive local steering. It does not prove that all 50 drones can cross every opening within the chosen horizon, that the controller is optimal, or that real drones would reproduce the result.

The main unresolved questions are now distinct: improve passage efficiency, test robustness to imperfect state/timing information, extend beyond the horizontal-flight pilot, and establish the physical interaction model. Keep these within the original eight-step plan; Steps 3–4 remain physically unvalidated. A useful next milestone is a robustness comparison with an updated 3D demonstration, rather than immediately claiming aerodynamic or large-scale feasibility.

No airflow, drag, wind, sensing error, communication delay, solid-wall contact or physical collision response is included. No real-flight safety or novelty claim follows from this milestone.

## Reproduce and inspect

From the workspace root, run:

```
node outputs/milestone-04-source/study.cjs
node outputs/milestone-04-source/verify.cjs
```

The study uses four local worker threads for independent cases, then runs the numerical refinements. It reads the preserved milestone-3 records for pairing. No external npm packages are required for computation. Serve the workspace over HTTP to view the local vendored Three.js modules.

- [Interactive comparison](milestone-04-merging.html)
- [Paired CSV](milestone-04-study.csv)
- [Full data and reservation events](milestone-04-study.json)
- [Checks and source hashes](milestone-04-verification.json)
- [Scheduler](milestone-04-source/scheduler.cjs)
- [Simulator](milestone-04-source/sim.cjs)
- [Study runner](milestone-04-source/study.cjs)

## Browser verification

Checked the rendered comparison in the Codex in-app browser at 1440 × 1000, 390 × 844 and the default panel size. Both Three.js views render; playback/pause, restart, the shared time slider, all three paired endpoint counts, frozen stop behavior and the overview, gate, top and actual-encounter cameras passed. The encounter control is disabled for the unstopped wide case. Mobile views stack without horizontal overflow. No console warnings or errors were observed. The saved preview was inspected visually. Other browsers and sustained performance remain untested.
