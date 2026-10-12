# Milestone 11 — emergent coordination in a three-dimensional flock

The previous baseline kept drones at nearly one altitude. This experiment allows all three components of motion and starts from a scattered volume with different velocity directions and yaw headings. No drone is assigned a position, lane, leader or destination.

## Goal and method

Ask whether local social rules produce coordinated motion and preserve a connected group beyond what collision avoidance alone provides. Use 50 drones in the existing 6DOF rigid-body model. Compare full Boids, separation-only, and all social terms off using exactly matched initial states. Each drone has self-propulsion toward 0.65 m/s; local steering uses neighbors within 1.8 m and a 0.9 m/s command cap. Separation, alignment and cohesion act in xyz. The altitude controller receives an algebraically converted vertical-velocity request, giving commanded vertical acceleration 2.5 × (requested velocity − actual velocity) before existing limits. Motor lag, thrust saturation, attitude control, gravity and rigid-body integration remain active.

Soft environmental responses outside x/y ±8 m and altitude 2–7 m apply restoring steering and outward-velocity damping; they do not snap positions or represent collision walls. A steering cue in x>0 from 15–18 s is identical across modes. In displayed seed401 it reaches all Boids drones, so this is not evidence of information propagation from a small subgroup. The initially connected cloud tests self-organization and retention, not merging disconnected groups. No obstacle or narrow gate is included in this milestone.

## Development trace

The seed1 pilot coordinated successfully. Development seeds301–305 revealed late ground braking: two Boids runs and three separation-only runs hit the vehicle model limit. Those runs, source, protocol and failed no-stop verification are preserved in `milestone-11-development-v1/`. Environmental braking was revised; social-rule parameters were unchanged. The revised source was frozen before new evaluation seeds401–405. Failed older results have not been removed or relabeled as successful.

## Fresh evaluation

15 cases: five seeds × three modes, 30 seconds, 0.005 s integration and 0.01 s control. The table reports terminal values; stopped controls have shorter observation durations and are not 30-second comparisons.

| Seed | Mode | End (s) | Direction agreement | Largest connected group | Height spread (m) | Minimum separation (m) | Stop |
|---|---|---:|---:|---:|---:|---:|---|
| 401 | boids | 30.000 | 99.9% | 50/50 | 2.24 | 0.498 | none |
| 401 | off | 1.705 | 17.4% | 50/50 | 4.73 | 0.150 | contact envelope reached |
| 401 | separation-only | 30.000 | 17.8% | 13/50 | 4.77 | 0.216 | none |
| 402 | boids | 30.000 | 99.6% | 50/50 | 2.86 | 0.424 | none |
| 402 | off | 1.590 | 8.2% | 50/50 | 4.39 | 0.146 | contact envelope reached |
| 402 | separation-only | 30.000 | 17.5% | 7/50 | 5.10 | 0.254 | none |
| 403 | boids | 30.000 | 99.7% | 50/50 | 2.58 | 0.472 | none |
| 403 | off | 1.140 | 24.5% | 50/50 | 4.10 | 0.148 | contact envelope reached |
| 403 | separation-only | 30.000 | 28.4% | 5/50 | 5.42 | 0.328 | none |
| 404 | boids | 30.000 | 99.8% | 50/50 | 3.46 | 0.424 | none |
| 404 | off | 1.075 | 11.6% | 50/50 | 4.03 | 0.148 | contact envelope reached |
| 404 | separation-only | 30.000 | 13.8% | 6/50 | 5.11 | 0.303 | none |
| 405 | boids | 30.000 | 99.2% | 50/50 | 2.56 | 0.402 | none |
| 405 | off | 0.800 | 11.8% | 50/50 | 4.03 | 0.149 | contact envelope reached |
| 405 | separation-only | 30.000 | 16.5% | 5/50 | 4.96 | 0.299 | none |

All five full-Boids runs retain 50/50 connectivity and end with 99.2–99.9% direction agreement. Separation-only ends at 13.8–28.4%, with largest components of 5–13 drones. Both modes complete the full horizon without contact stops; all-off stops at contact in all five cases. This supports a combined alignment-and-cohesion benefit beyond separation alone in these model conditions; it does not isolate their individual contributions or establish universal superiority. A connected component means a chain of local neighbors, not that every drone sees every other drone. Direction agreement is the magnitude of the mean unit velocity. Height spread alone is not a measure of isotropic flock shape.

## Verification

Locality, drone-order invariance and matched initial-state checks pass. Displayed Boids seed401 also passes halved-step refinement with unchanged no-stop outcome and maximum terminal position difference below 0.001 mm. This checks one trajectory, not convergence of every possible scenario. The earlier failed development criterion remains archived. The assumed 15 cm contact envelope and model-based clearance are not measured flight safety margins.

## Conclusion and implication

There is now a visible three-dimensional collective response caused by local rules, with a relevant control comparison. The prior flat procession was a setup limitation. This is a useful behavioral baseline, not a new scientific contribution by itself: classical Boids coordination is established prior art. Airflow, sensor errors and real-flight accuracy remain unvalidated, and Boids computation remains on the CPU. Narrow-gate passage and obstacle avoidance are not solved here.

Next milestone: preserve this volumetric flock while adding an obstacle/passage task, with independent local-rule controls and numerical checks. Then connect the behavioral baseline back to the original aerodynamic accuracy–cost question. The overall eight-step research remains ongoing.

## Records

- [Interactive Three.js replay](milestone-11-flocking.html): same simulated trajectories, trails, local neighbors and full camera orbit. Drone meshes are enlarged 2.5× only for readability.
- [Frozen protocol](milestone-11-protocol.json), [all evaluation records](milestone-11-study.json), [summary](milestone-11-summary.json), [verification](milestone-11-verification.json)
- [Simulation and controller](milestone-11-source/sim.cjs), [study runner](milestone-11-source/study.cjs)
- [Preserved development failures](milestone-11-development-v1/milestone-11-study.json)

Reproduce in an isolated copy using `python3 research-reproduce.py --stage 11 --node /path/to/node`. Do not rerun directly over pinned evidence. Research-manifest hashes cover the current deliverables and archived traces.
