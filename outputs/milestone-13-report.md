# Milestone 13 — multiple obstacles and staggered openings

## What we learned

The geometry now exposes failures hidden by the single sphere. Both controllers finish the three-obstacle course and the wider staggered openings in all three tested starting conditions. At 1.8 m openings, full Boids hits a wall in two of three runs. The simpler separation-only comparison does better in those two cases, but has its own drone-contact failure in the other case. Neither controller reliably completes the restrictive course.

## Research goal and methodology

Test whether the existing local 3D flock survives sequential changes in geometry, rather than a single isolated obstacle. Eighteen cases were frozen before inspection: seeds 601–603 × three courses × full Boids / separation-only. No parameters were retuned against these results. Fifty rigid-body drones start from the same scattered positions, mixed velocities and yaw headings within each paired comparison. Runs last at most 60 s; physics step 0.005 s, control interval 0.01 s. Every failure is retained.

The courses are:

- Three spheres at (-1,-0.5,3.8), (3,0.7,4.8), (7,-0.6,3.5) m, radii 1, 1.1, 0.9 m. Known-map guidance changes lateral and altitude targets across the course. Finish plane x=10 m.
- Two square openings of side 3 m, centered at (0,-1,3.5) and (5,1,5) m. Finish plane x=6.2 m.
- The same two openings reduced to side 1.8 m. Finish plane x=6.2 m.

The gate centers differ by 2 m laterally and 1.5 m vertically. The wider apertures overlap in their projected yz area, so they do not force every individual drone to turn or climb. The tight apertures have disjoint lateral intervals, requiring a lateral route change. This is a more demanding controlled benchmark, not a cluttered real-world environment or a maze-planning benchmark.

All drones share the same known map and route preferences. There is no central release schedule, assigned lane, leader or prescribed individual trajectory. Full Boids adds local alignment and cohesion to the separation-only control; cruise propulsion, environmental guidance, physics and contact checks are shared. Programmed routing is not claimed as emergent planning. Shared guidance itself encourages alignment, so successful passage does not demonstrate a Boids advantage.

## Geometry and physics

Swept drone segments are checked against the union of all sphere surfaces or all aperture walls, including the second wall. Walls are infinite zero-thickness planes with square holes; the renderer shows finite patches. The drone envelope radius is assumed to be 7.5 cm. Drone-to-drone relative swept segments detect contact below 15 cm. The entire run stops on contact; impact response is not modeled. These checks are exact for the straight segments used between integration states, not exact for the continuous curved physical path.

The existing gravity, motor lag, attitude control and 6DOF integration remain. Navigation is CPU-based and observes ideal states. Airflow, wind, sensing uncertainty and real-flight validation are absent. Mesh enlargement in the UI affects only appearance.

## All results

Completed = drones reaching the finish plane before any stop or timeout. Contact-stop exposures differ, so passage counts are not equal-duration throughput comparisons. Connectivity minima use saved 0.1 s samples and include the final stop sample; they do not guarantee continuous connectivity.

| Seed | Course | Controller | Completed /50 | Stop | End (s) | Minimum obstacle clearance (m) | Minimum sampled connected group |
|---|---|---|---:|---|---:|---:|---:|
| 601 | slalom | boids | 50 | none | 60.000 | 0.6239 | 50/50 |
| 601 | slalom | separation-only | 50 | none | 60.000 | 0.7290 | 50/50 |
| 601 | staggered | boids | 50 | none | 60.000 | 0.0996 | 49/50 |
| 601 | staggered | separation-only | 50 | none | 60.000 | 0.2142 | 48/50 |
| 601 | tight | boids | 7 | obstacle contact envelope | 24.400 | -0.0007 | 50/50 |
| 601 | tight | separation-only | 44 | none | 60.000 | 0.0255 | 43/50 |
| 602 | slalom | boids | 50 | none | 60.000 | 0.6580 | 50/50 |
| 602 | slalom | separation-only | 50 | none | 60.000 | 0.7300 | 50/50 |
| 602 | staggered | boids | 50 | none | 60.000 | 0.0287 | 47/50 |
| 602 | staggered | separation-only | 50 | none | 60.000 | 0.1364 | 46/50 |
| 602 | tight | boids | 48 | none | 60.000 | 0.0095 | 35/50 |
| 602 | tight | separation-only | 0 | contact envelope reached | 14.850 | 0.0456 | 50/50 |
| 603 | slalom | boids | 50 | none | 60.000 | 0.6639 | 50/50 |
| 603 | slalom | separation-only | 50 | none | 60.000 | 0.7288 | 50/50 |
| 603 | staggered | boids | 50 | none | 60.000 | 0.0108 | 45/50 |
| 603 | staggered | separation-only | 50 | none | 60.000 | 0.0970 | 49/50 |
| 603 | tight | boids | 0 | obstacle contact envelope | 13.485 | -0.0005 | 50/50 |
| 603 | tight | separation-only | 42 | none | 60.000 | 0.0851 | 35/50 |

The full Boids sphere-course runs remain connected at every saved sample. Wide staggered passage temporarily fragments the group (smallest components contain 45–49 of 50 drones); passing all drones is not the same as keeping every drone connected throughout. Wide Boids obstacle clearance is as low as about 1.1 cm beyond the assumed envelope, so these successes do not imply robust margins. Tight full-Boids completions are 7, 48 and 0; the control completes 44, 0 and 42. This small sample is diagnostic, not a statistical generalization.

## Numerical verification

All five checks pass: matched full initial states, second-wall rejection, free second-aperture passage, middle-sphere intersection, and the predeclared refinement test for the three displayed Boids trajectories. Refinement halves the step to 0.0025 s and requires identical passage counts and stop reasons with terminal position differences below 1 cm.

| Displayed course (seed 601) | Maximum terminal difference | Coarse / fine completions | Stop agreement |
|---|---:|---:|---|
| slalom | 0.000183 mm | 50 / 50 | none |
| staggered | 0.001426 mm | 50 / 50 | none |
| tight | 1.740788 mm | 7 / 7 | obstacle contact envelope |

For the tight course, wall contact occurs at 24.400 s versus 24.3975 s. Refinement supports this particular failure, not all seeds or scenarios. The earlier milestone-12 narrow case remains numerically unresolved; passing this new test does not retroactively validate it.

## Conclusion and implications

Local flocking plus common route guidance can negotiate these wider courses in the model, but simple weighted Boids steering does not reliably maintain clearance at restrictive openings. These comparisons do not establish that alignment/cohesion are intrinsically harmful: they show the current combination can fail where the separation-only control survives. A next intervention should explicitly prioritize predicted obstacle clearance over social steering and test that change against this frozen suite and new seeds, rather than quietly replacing Boids with a central scheduler. Diagnose local forces at wall contacts, then test uncertainty and numerical stability before adding airflow.

The original aerodynamic accuracy–cost research and novelty assessment remain open. This milestone is a controlled navigation diagnosis, not research completion.

## Records and reproduction

- [Interactive 3D course](milestone-13-course.html)
- [Protocol and source hash](milestone-13-protocol.json), [all trajectories and metrics](milestone-13-study.json), [summary](milestone-13-summary.json), [verification](milestone-13-verification.json)
- [Simulation source](milestone-13-source/sim.cjs), [study runner](milestone-13-source/study.cjs), [course geometry](milestone-13-source/courses.json)
- [Previous milestone](milestone-12-report.md)

Run `python3 research-reproduce.py --stage 13 --node /path/to/node` to verify integrity and rerun in an isolated copy. All records remain pinned by the current manifest.
