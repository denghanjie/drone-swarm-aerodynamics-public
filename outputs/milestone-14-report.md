# Milestone 14 — local clearance priority, including a rejected attempt

## Goal

Test whether an explicit local clearance rule improves the saved wall failures without replacing Boids with centralized traffic scheduling. Preserve matched physics, course geometry, social weights, stop conditions and initial states. The candidate changes velocity commands; it never edits positions or skips collisions.

## First attempt: obstacle clearance alone

A local filter constrains lateral/vertical motion toward gate edges and reduces forward commands when a predicted gate intercept is outside the interior margin. It uses a 0.25 m center-to-edge margin and a 1.2 s command time scale. Near spheres it limits inward radial commands. This is a heuristic command constraint, not a safety certificate for the lagged rigid-body model.

The first attempt fails: all six tested restrictive cases (old seeds 601–603, fresh seeds 701–703) stop at drone contact, despite positive obstacle clearance. The saved commands show how to inspect this failure. Attribution to a particular term would require further isolation; a wall-only priority does not by itself address interactions between drones. All wider/sphere first-candidate cases complete 50/50. The candidate is rejected, with original source, protocol, results, replays and failure states preserved.

## Revised attempt: joint wall and neighbor constraints

Starting from the same Boids command, each drone alternates obstacle-command projection and nearby-drone closing-speed projection six times. The neighbor rule uses actual neighbors within 1.5 m and a 0.38 m desired center separation with a 1.2 s closing time scale. Boids itself still uses neighbors within 1.8 m. Speed remains capped at 0.9 m/s. The final projection prioritizes obstacle clearance.

No drone is assigned a lane or release time. The filter observes neighboring positions and velocities, not their future plans. Finite sequential projections may be order-dependent and may not satisfy all constraints simultaneously; the final obstacle projection or speed cap can undo part of a neighbor correction. Feasibility is not guaranteed. These limitations are why full-physics trials and retained failures are required.

The revised source was frozen before fresh seeds 801–803. These new seeds provide 18 matched runs: three courses × original Boids / joint filter × three seeds. The candidate also revisits three old restrictive cases. In total this milestone records 42 study cases across both attempts, plus the saved first-attempt pilot and refinement reruns. The two attempts use different fresh seeds, so do not infer their relative effect from a direct unmatched aggregate comparison.

## Revised results

Completed means reaching the course finish plane before a contact stop or the 60 s deadline. Stopped runs have shorter exposures; counts do not represent equal-duration throughput. Connectivity minima refer to saved 0.1 s samples, not every instant. Fresh paired baselines are unchanged Boids; historical baselines for seeds 601–603 remain in milestone 13.

| Seed | Course | Controller | Completed /50 | Stop | End (s) | Min obstacle clearance (m) | Min drone separation (m) | Filter active | Min sampled connected |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| 601 | tight | joint | 36 | none | 60.000 | 0.1588 | 0.3576 | 33.6% | 40/50 |
| 602 | tight | joint | 25 | none | 60.000 | 0.1657 | 0.3509 | 42.4% | 20/50 |
| 603 | tight | joint | 30 | none | 60.000 | 0.1659 | 0.3566 | 39.6% | 29/50 |
| 801 | slalom | boids | 50 | none | 60.000 | 0.6551 | 0.4296 | 0.0% | 50/50 |
| 801 | slalom | joint | 50 | none | 60.000 | 0.6957 | 0.5051 | 1.4% | 50/50 |
| 801 | staggered | boids | 33 | obstacle contact envelope | 27.600 | -0.0002 | 0.4532 | 0.0% | 50/50 |
| 801 | staggered | joint | 50 | none | 60.000 | 0.1771 | 0.4741 | 6.3% | 45/50 |
| 801 | tight | boids | 50 | none | 60.000 | 0.1079 | 0.3766 | 0.0% | 47/50 |
| 801 | tight | joint | 31 | none | 60.000 | 0.1569 | 0.3772 | 35.9% | 21/50 |
| 802 | slalom | boids | 50 | none | 60.000 | 0.6417 | 0.4914 | 0.0% | 50/50 |
| 802 | slalom | joint | 50 | none | 60.000 | 0.6669 | 0.5004 | 1.2% | 50/50 |
| 802 | staggered | boids | 50 | none | 60.000 | 0.0504 | 0.4483 | 0.0% | 47/50 |
| 802 | staggered | joint | 50 | none | 60.000 | 0.1919 | 0.4698 | 5.8% | 49/50 |
| 802 | tight | boids | 50 | none | 60.000 | 0.1093 | 0.3866 | 0.0% | 29/50 |
| 802 | tight | joint | 32 | none | 60.000 | 0.1250 | 0.3541 | 39.8% | 44/50 |
| 803 | slalom | boids | 50 | none | 60.000 | 0.6415 | 0.4894 | 0.0% | 50/50 |
| 803 | slalom | joint | 50 | none | 60.000 | 0.6531 | 0.4829 | 1.4% | 50/50 |
| 803 | staggered | boids | 50 | none | 60.000 | 0.0465 | 0.4401 | 0.0% | 50/50 |
| 803 | staggered | joint | 50 | none | 60.000 | 0.1885 | 0.4678 | 5.9% | 50/50 |
| 803 | tight | boids | 48 | none | 60.000 | 0.1000 | 0.4198 | 0.0% | 48/50 |
| 803 | tight | joint | 31 | none | 60.000 | 0.1653 | 0.3486 | 37.7% | 22/50 |

## Numerical verification

- PASS — Baseline trajectory exactly reproduces milestone13 implementation.
- PASS — Fresh matched initial states.
- PASS — Far-from-obstacle filter is identity.
- PASS — Obstacle projection reduces forward and outward command.
- FAIL — Refinement: same stop/count and final positions within1cm.

| Displayed revised run (seed 801) | Coarse / fine completed | Coarse / fine stop | Terminal difference |
|---|---:|---|---:|
| slalom | 50 / 50 | none / none | 0.4649 mm |
| staggered | 50 / 50 | none / none | 0.0006 mm |
| tight | 31 / 31 | none / none | 2489.2606 mm |

The comparison halves the physics step from 0.005 to 0.0025 s, leaving the control period at 0.01 s. It tests only the three displayed candidate trajectories. Exact baseline trajectory regression against the milestone-13 implementation is separately checked on seed 801 tight. A locality probe confirms no change from a remote drone; one permutation probe is not a general guarantee of order independence. Earlier narrow-case numerical sensitivity is not retroactively resolved by this milestone.

## Decision and plain-language conclusion

Reject obstacle-only filtering. Retain the joint filter as a provisional candidate, not a validated solution. Across its 12 coarse-step runs it records no contact stop, including all three historical regressions. In fresh tests it fixes the wider-opening wall failure at seed 801 (33 completions and wall stop becomes 50 with no stop). However, fresh tight-course completion drops from 48–50 with original Boids to 31–32 with the filter, and the group fragments: the smallest sampled connected component in the displayed tight run contains only 21 of 50 drones.

The refinement criterion also fails for that tight run: the maximum terminal position difference is 2.489 m when the physics step is halved. Both runs still record 31 completions and no contact, but their detailed trajectories are not converged. Sphere and wider-opening displayed cases pass the position criterion. These results support further investigation of combined local clearance constraints, not declaring narrow passage solved or robustly safe.

Next gate: diagnose the discontinuous gate/constraint switching and refinement sensitivity, then check whether conservative clearance can preserve group connectivity and acceptable throughput. Do not increase complexity or add airflow on the assumption that this candidate is validated. The original aerodynamic accuracy–cost research remains unfinished.

## Scope and trace

6DOF rigid-body dynamics, motor lag and actual contact checks remain active. Observations and obstacle map are ideal. Airflow, sensing errors, wind, physical validation and actual GPU Boids execution are absent. Programmed route guidance is unchanged; no claim of autonomous path discovery, novelty or real-flight safety is made. Overall research remains ongoing.

- [Revised 3D comparison](milestone-14-clearance.html)
- [Revised protocol](milestone-14-joint-protocol.json), [all revised runs and failure states](milestone-14-joint-study.json), [verification](milestone-14-joint-verification.json), [locality probe](milestone-14-joint-locality.json)
- [Revised source](milestone-14-joint-source/sim.cjs), [study runner](milestone-14-joint-source/study.cjs)
- [Rejected obstacle-only replay](milestone-14-obstacle-only.html), [first protocol](milestone-14-protocol.json), [first results](milestone-14-study.json), [failure diagnosis](milestone-14-failure-analysis.json), [first source](milestone-14-source/sim.cjs)

Reproduce in an isolated copy with `python3 research-reproduce.py --stage 14 --node /path/to/node` or `--stage 14-first` for the rejected candidate. Do not overwrite pinned evidence in place. Verify saved checks, not merely process completion.
