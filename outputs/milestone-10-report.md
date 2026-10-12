# Milestone 10 — correcting the flocking baseline

The earlier passage studies used centralized scheduling. They did not establish Boids behavior, and the previous completion framing was premature. The original research remains ongoing.

## What changed

Each drone now computes separation (avoid crowding), alignment (match local velocities), and cohesion (stay near its local group). Only neighbors within 1.25 m contribute. A shared direction and map-based gate steering guide the group; Boids has no assigned lanes, release permissions, or leader. CPU neighbor discovery still scans all pairs. Three.js displays recorded simulated states, not a decorative flock animation.

This is horizontal flocking at near-fixed altitude using the existing 3D rigid-body model. It is not volumetric flocking, a GPU Boids implementation, or physical validation. Airflow is off.

## Method

45 matched cases: three controllers × three widths × five holdout seeds (201–205). Controllers: preserved milestone-7 scheduler, Boids, and the same goal/map controller with all three social rules removed. Each run has 50 drones, 0.6 m initial spacing, 0.5 m/s requested speed cap, ideal observations, a 60 s limit, and 0.01 s physics steps. Parameters were inspected in three seed-1 pilots, frozen, then evaluated on the holdout seeds. All failures are retained.

The gate is a virtual measurement plane without wall collision response. A distance below 15 cm stops a run; below 20 cm is a spacing breach. Crossings outside the allowed opening are invalid. These are assumed model thresholds, not measured safety margins.

## Results

Counts below sum five runs, with at most 250 valid passages. They are coarse-step outcomes, not guaranteed throughput or converged narrow-gate estimates.

| Opening | Controller | Valid passages | Runs with invalid crossings | Runs with spacing breaches | Contact stops |
|---|---|---:|---:|---:|---:|
| 0.6 m | flow | 40 | 0 | 0 | 0 |
| 0.6 m | boids | 101 | 5 | 5 | 1 |
| 0.6 m | goal-only | 30 | 0 | 5 | 5 |
| 1.2 m | flow | 75 | 0 | 0 | 0 |
| 1.2 m | boids | 157 | 5 | 4 | 0 |
| 1.2 m | goal-only | 65 | 0 | 5 | 5 |
| 2.4 m | flow | 175 | 0 | 0 | 0 |
| 2.4 m | boids | 250 | 0 | 0 | 0 |
| 2.4 m | goal-only | 250 | 0 | 0 | 0 |

`flow` is the preserved centralized scheduler, not a flocking controller.

Wide-opening Boids passes all 250 drones without measured breaches. However, goal-only also passes all 250: this easy case does not demonstrate a benefit from social steering. At smaller widths, Boids produces invalid crossings in every run. The scheduler avoids measured breaches but passes fewer drones within the time limit. These differences do not justify claiming that either method is generally superior.

## Verification and a retained failure

10 of 11 checks pass, including locality, invariance to drone ordering, direction of each social term, removal of social terms in the control condition, matched initial conditions, absence of reservations, exact scheduler regression, and replay integrity.

The combined time-step refinement check fails. For narrow seed 201, dt=0.01 gives 21 valid passages without a contact stop; dt=0.005 and 0.0025 both give 12 and a contact stop. Their final-position difference is about 1.26 mm. For medium and wide seed 201, passage/stop counts remain unchanged; half-versus-quarter position differences are about 0.146 mm and 0.00272 mm. This is limited numerical evidence for those replays, not convergence of the entire study. The narrow coarse-step aggregate remains exploratory and must not support a safety claim. No parameter was changed to hide this failure.

## Conclusion and next research gate

The implementation now addresses the intended local Boids concept. The correction does not complete the research goal. Next work should refine contact-event treatment and time-step convergence across seeds, then address narrow-gate behavior using local rules and compare against the retained controls. Subsequent work must evaluate true 3D flocking, uncertain observations, physical airflow evidence, and actual Boids GPU computation/scaling. Novelty remains unestablished.

## Records and reproduction

- [Visible 3D comparison](milestone-10-boids.html)
- [Protocol and frozen controller hashes](milestone-10-protocol.json)
- [All 45 results](milestone-10-study.json) and [CSV](milestone-10-study.csv)
- [Verification, including failed check](milestone-10-verification.json)
- [Pilot records](milestone-10-pilot.json)
- [Steering source](milestone-10-source/boids.cjs), [physics integration](milestone-10-source/sim.cjs), [study runner](milestone-10-source/study.cjs)
- [Previous assessment preserved](archive-before-boids/research-final-report.md)

Run `python3 research-reproduce.py --stage 10 --node /path/to/node` from the outputs directory. It verifies hashes and runs the study in an isolated copy, retaining the pinned results. The failed refinement criterion is recorded as evidence; process completion alone is not a passing scientific result.
