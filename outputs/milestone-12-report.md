# Milestone 12 — the flock encounters obstacles

## Plain-language result

All 50 drones pass a sphere and a wide opening in every tested case, both with full Boids and with separation-only steering. Narrow passage is unresolved: full Boids passes 11–15/50 by 40 seconds, while the separation-only comparison stops at drone contact after 5–9 passages. The narrow Boids trajectory is sensitive to the numerical time step. These are exploratory model results, not physical safety evidence.

## Goal and method

Test local 3D flocking with shared environmental guidance. Eighteen cases: seeds501–503 × sphere/wide/narrow × full Boids/separation-only. Each pair shares full initial states, including mixed velocities and headings. Fifty drones start in a volumetric cloud centered at x=-6 m, z=4 m; integration step0.005 s, control interval0.01 s, horizon40 s. Source hashes and planned jobs were saved before the evaluation. A seed1 sphere pilot is retained. No evaluation failures were discarded or used to tune this controller.

The sphere has radius1 m and center(0,0,4). The common guidance explicitly favors flight above it; the controller does not discover this route. Both opening scenarios use an infinite zero-thickness plane x=0 with a square aperture centered at z=4: side3 m or1.2 m. The renderer shows a finite patch of this plane. Shared guidance aims at the aperture interior and brakes forward movement when lateral/vertical alignment is incomplete. Local separation, alignment and cohesion retain the milestone11 parameters; no lanes, slots, leader, central scheduler or group-centroid steering is introduced. Self-propulsion and goal guidance remain in both comparisons. Shared guidance itself can align velocities, so successful passage does not isolate a social-rule benefit.

Contact is measured with an assumed7.5 cm drone radius. Straight swept segments are tested against the sphere and four aperture half-planes; drone pairs use relative swept segments. This detects intersections between integration endpoints, subject to the piecewise-linear path approximation. A run stops at the first detected envelope contact; impact response is not modeled. Passage means first crossing x=1.2 m beyond the obstacle plane. A lower ground guard remains; no airflow, sensor errors or physical validation are included.

## All evaluation results

Obstacle clearance subtracts the assumed drone radius. Connectivity is the terminal largest component under the1.8 m neighbor radius, not proof of continuous connectivity throughout the run. Stopped runs have shorter exposure and must not be compared as40-second completions.

| Seed | Scenario | Controller | Passed /50 | End(s) | Minimum obstacle clearance(m) | Minimum drone distance(m) | Terminal connected | Stop |
|---|---|---|---:|---:|---:|---:|---:|---|
| 501 | narrow | boids | 15 | 40.000 | 0.115 | 0.183 | 50/50 | none |
| 501 | narrow | separation-only | 5 | 24.965 | 0.068 | 0.148 | 48/50 | contact envelope reached |
| 501 | sphere | boids | 50 | 40.000 | 0.472 | 0.503 | 50/50 | none |
| 501 | sphere | separation-only | 50 | 40.000 | 0.638 | 0.494 | 50/50 | none |
| 501 | wide | boids | 50 | 40.000 | 0.110 | 0.487 | 50/50 | none |
| 501 | wide | separation-only | 50 | 40.000 | 0.239 | 0.413 | 50/50 | none |
| 502 | narrow | boids | 11 | 40.000 | 0.009 | 0.199 | 44/50 | none |
| 502 | narrow | separation-only | 5 | 29.350 | 0.075 | 0.146 | 45/50 | contact envelope reached |
| 502 | sphere | boids | 50 | 40.000 | 0.460 | 0.515 | 50/50 | none |
| 502 | sphere | separation-only | 50 | 40.000 | 0.630 | 0.443 | 50/50 | none |
| 502 | wide | boids | 50 | 40.000 | 0.105 | 0.508 | 50/50 | none |
| 502 | wide | separation-only | 50 | 40.000 | 0.224 | 0.414 | 49/50 | none |
| 503 | narrow | boids | 12 | 40.000 | 0.206 | 0.184 | 46/50 | none |
| 503 | narrow | separation-only | 9 | 32.555 | 0.099 | 0.150 | 42/50 | contact envelope reached |
| 503 | sphere | boids | 50 | 40.000 | 0.513 | 0.482 | 50/50 | none |
| 503 | sphere | separation-only | 50 | 40.000 | 0.649 | 0.395 | 50/50 | none |
| 503 | wide | boids | 50 | 40.000 | 0.208 | 0.482 | 50/50 | none |
| 503 | wide | separation-only | 50 | 40.000 | 0.074 | 0.395 | 50/50 | none |

At saved 0.1 s samples, full Boids maintains a 50/50 connected component throughout every sphere and wide run. Narrow minima are50/50,44/50 and46/50 for seeds501–503. Between-sample connectivity was not separately measured.

## Verification and retained uncertainty

Four of five checks pass: matched initial states, wall intersection outside the hole, centered free crossing and sphere intersection between endpoints. The combined refinement criterion fails for the narrow opening. At seed501, halving the step from0.005 to0.0025 s preserves15 passages and no stop, but the maximum terminal position difference is0.422 m, exceeding the1 cm criterion. Sphere and wide cases retain50 passages/no stop with position differences below0.0001 mm. Only these three displayed Boids cases were refined. Do not infer convergence for all cases or treat the narrow trajectory as numerically reliable.

## Conclusion and next gate

Guided volumetric passage around a simple sphere and through a3 m opening is feasible in these limited model tests. No passage benefit from full Boids is established in those easy scenarios, because the control also succeeds. Narrow openings expose congestion and numerical sensitivity. We should diagnose that sensitivity and measure sustained clearance/connectivity before increasing density or adding aerodynamic interactions; the current failures remain regression cases. This milestone does not solve general obstacle navigation, establish scientific novelty, or complete the original aerodynamic accuracy–cost research.

## Trace and reproduction

- [Three.js comparison](milestone-12-obstacles.html)
- [Protocol](milestone-12-protocol.json), [all runs](milestone-12-study.json), [summary](milestone-12-summary.json), [verification including failure](milestone-12-verification.json)
- [Source](milestone-12-source/sim.cjs), [study runner](milestone-12-source/study.cjs), [pilot](milestone-12-pilot.json)
- [Prior volumetric flocking](milestone-11-flocking.html)

Use `python3 research-reproduce.py --stage 12 --node /path/to/node` for a run in an isolated copy. A finished script is not a passing scientific result; inspect the saved checks and stop conditions.
