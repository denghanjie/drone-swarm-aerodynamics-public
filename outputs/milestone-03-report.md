# Milestone 3 — first 50-drone passage pilot

## Plain-language result

**The 50-drone 3D passage simulation is implemented. The simple navigation rule is not robust enough for crowded passage.** In the displayed wide-opening run, all 50 drones passed; the medium and narrow runs reached the contact envelope and were stopped. The failures are retained, not edited out.

Across 120 runs, 83 stopped on the contact envelope and 37 reached the full 60-second horizon. Of those 37, only 31 achieved all 50 valid crossings without any invalid gate crossing. No run hit the motor thrust limits. These outcomes describe this specific steering rule and simplified environment, not what is possible with a better planner or real drones.

## Research goal and method

This begins Step 5 of the original eight-step plan: establish a reproducible swarm navigation and measurement baseline before attributing effects to uncertain aerodynamic models. Steps 3–4 remain physically unvalidated. This milestone makes no novelty claim.

Each of the 50 vehicles uses the existing `step02c-source/physics.cjs`: 27 g mass, gravity, 6-DOF rigid-body dynamics, quaternion attitude, four motor thrust states, a 40 ms motor time constant and bounded thrust allocation. The integration is RK4 at 10 ms; control is updated every 10 ms. The requested thrust-to-weight upper bound is 2.25 and the commanded tilt limit is 15°. Actual tilt is measured, not forcibly clipped. Translation follows from thrust orientation, not direct position animation.

Initial positions are a 10-by-5 horizontal grid at nominal altitude 1.2 m. The leading row starts at x = −1.2 m; both row and column spacing use the selected 0.3 or 0.6 m. Each seed perturbs lateral position and altitude independently by up to 5 mm. Identical seeds give identical starting groups across widths and speeds.

The gate lies at x = 0, from z = 0.6 to 1.8 m. Five lane targets are distributed within the width, leaving a 7.5 cm body envelope plus an extra 4 cm edge margin. Local steering aims toward these targets, repels nearby vehicles, slows behind a nearby leader and requests a pause near the gate when lateral alignment is incomplete. Total commanded horizontal speed is capped. There is no reservation system, predictive optimization, vertical lane changing or communication model. This is a basic reactive baseline, not a proposed novel boids controller.

**A known structural weakness:** at width 0.6 m the five target lanes are only 9.25 cm apart—less than the 15 cm contact envelope and 20 cm desired separation. Side-by-side passage in those five lanes cannot work. The controller would need to stagger or merge them; this baseline does not explicitly schedule that. Narrow-gate failure does not establish that the gate is impassable. Wider-gate failures show additional limitations of the reactive steering rule.

No aerodynamic interactions, wind, sensor noise, drag, impact physics or solid-wall physics are included. The gate is a virtual measurement opening, so out-of-opening crossings are recorded rather than blocked by an artificial wall force. Vehicles continue moving after a successful crossing and remain in separation checks throughout the horizon, including when they leave the camera view.

## Measurements and failure handling

- Unique forward valid crossings: each drone counted once, provided its center is inside the gate with the 7.5 cm body clearance at the interpolated crossing time. An earlier invalid crossing does not erase a later valid crossing; invalid-crossing drones are reported separately.
- Completion fraction: valid crossings / 50. Full-horizon throughput: valid crossings / 60 s, even when a run stops early; for stopped cases this is an achieved-count score, not a steady-state flow estimate.
- Minimum pair separation: closest point of the relative line segment over each integration step. This catches between-step encounters, but approximates curved within-step paths.
- Close pairs: unique pairs coming within 20 cm; contact pairs: unique pairs coming within 15 cm. Pair counts are not repeated event counts or actual rotor-impact counts.
- Stop at the first detected contact envelope or numerical/vehicle limit; all drones stop together. Reported stopping time is the end of that integration step, not an exact event root. No physical collision outcome is inferred.
- Motor saturation: accumulated saturated motor-command time / simulated drone-time. Tracking RMS measures lateral lane and altitude error across the full simulated run; it is not error against a prescribed full trajectory. A completed 60-second run alone does not mean successful passage.

## All tested conditions

10 seeds per row. No failed run was removed. Means and ranges are descriptive across small initial perturbations, not confidence intervals for physical flight. The full-horizon throughput for each case is the valid-crossing count divided by 60.

| Width (m) | Initial spacing (m) | Speed (m/s) | Reached 60 s | Mean valid crossings / 50 | Valid-crossing range | Runs with an invalid crossing |
|---|---|---|---|---|---|---|
| 0.6 | 0.3 | 0.25 | 0/10 | 0.0 | 0–0 | 0/10 |
| 0.6 | 0.3 | 0.5 | 0/10 | 0.0 | 0–0 | 0/10 |
| 0.6 | 0.6 | 0.25 | 0/10 | 1.0 | 1–1 | 0/10 |
| 0.6 | 0.6 | 0.5 | 0/10 | 1.0 | 1–1 | 0/10 |
| 1.2 | 0.3 | 0.25 | 0/10 | 0.0 | 0–0 | 0/10 |
| 1.2 | 0.3 | 0.5 | 0/10 | 0.0 | 0–0 | 0/10 |
| 1.2 | 0.6 | 0.25 | 8/10 | 44.6 | 28–50 | 7/10 |
| 1.2 | 0.6 | 0.5 | 0/10 | 5.2 | 4–7 | 10/10 |
| 2.4 | 0.3 | 0.25 | 9/10 | 46.0 | 10–50 | 0/10 |
| 2.4 | 0.3 | 0.5 | 0/10 | 12.6 | 9–15 | 0/10 |
| 2.4 | 0.6 | 0.25 | 10/10 | 50.0 | 50–50 | 0/10 |
| 2.4 | 0.6 | 0.5 | 10/10 | 50.0 | 50–50 | 0/10 |

The displayed seed-1, spacing-0.6 m, speed-0.5 m/s examples have:

| Width | Valid crossings | Run end | Minimum separation |
|---|---|---|---|
| 2.4 m | 50/50 | Full 60 s | 0.539 m |
| 1.2 m | 5/50 | Contact envelope at 5.75 s | 0.1492 m |
| 0.6 m | 1/50 | Contact envelope at 3.26 s | 0.1485 m |

The medium example also records one drone crossing outside the opening. The narrow example records none before the stop.

## Numerical checks

Seven checks passed, covering analytic swept-distance cases, configuration accounting, finite metrics, replay shape and endpoint agreement, crossing records and step-size refinement. For each displayed example, integration steps were reduced from 10 to 5 to 2.5 ms while retaining the same 10 ms control updates. Valid-crossing counts and stop reasons were unchanged. Stopping times differed by at most 7.5 ms. Successive final-position differences were below 2.6 mm (including differing stop times). This checks three examples, not all 120 trajectories, and does not validate physical accuracy.

No CPU/GPU speed comparison is claimed. The calculation is CPU-based; the browser replays saved states using Three.js/WebGL. Positions and attitudes are interpolated between 0.1-second recording samples for display. UI instantaneous separation is based on those displayed positions, while reported minima use every integration step.

## Conclusion and implications

This milestone establishes working swarm mechanics, passage accounting, failure retention and a viewable 3D baseline. It also identifies a navigation confound: congestion can cause failure before aerodynamic interaction is introduced. The next useful comparison is an explicitly scheduled or predictive merging controller under the same initial conditions and metrics. Only after a credible navigation baseline should we interpret the effect of changing airflow assumptions. No evidence here establishes real-world safety, full project feasibility or research novelty.

Every subsequent milestone will include an updated 3D simulation and a short plain-language summary.

## Reproduce and inspect

Run `node outputs/milestone-03-source/study.cjs` from the workspace root. No external npm dependencies are needed for the numerical study. Serve the workspace over HTTP and open `outputs/milestone-03-passage.html`; local vendored Three.js modules supply rendering.

- [Interactive 3D replay](milestone-03-passage.html)
- [All cases (CSV)](milestone-03-study.csv)
- [Full results](milestone-03-study.json)
- [Checks and refinement](milestone-03-verification.json)
- [Simulation source](milestone-03-source/sim.cjs)
- [Study runner](milestone-03-source/study.cjs)

## Browser verification

Verified in the Codex in-app browser at 1440 × 1000, 390 × 844 and the default panel size. Page identity, rendered 3D scene, playback/pause, exact-end scrubbing, all three opening presets, restart and camera views passed. No browser console warnings/errors were observed. Mobile layout had no horizontal overflow. Fixed high-DPI canvas clipping, exact-stop slider access and narrow-screen camera framing. Other browsers and sustained playback performance remain untested.
