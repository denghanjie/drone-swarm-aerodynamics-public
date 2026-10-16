# Removing airflow's added turning effect changes the model's motion

**A new numerical mechanism result, not a physically validated or novel research finding.** We compared the same 16-drone local 3D Boids flock in three versions: airflow off, full airflow feedback, and airflow feedback with its added roll/pitch torque removed. Normal steering, attitude control and nominal motor torques stayed active. Each version calculated airflow from its own evolving positions and orientations.

Removing the added torque changed a drone's position by up to **0.511 m over two seconds**. Maximum recorded tilt fell from **19.56° to 8.90°**, near the airflow-off value of 8.85°. Yet the group's final mean height remained almost the same with full and force-only feedback: 3.6554 m versus 3.6546 m, compared with 4.2835 m for airflow off. The retained collective-force/controller pathway still produces substantial motion differences in this model.

| Finest recorded comparison | Largest sampled position difference |
|---|---:|
| Full feedback versus force only | 0.511 m |
| Full feedback versus airflow off | 1.102 m |
| Force only versus airflow off | 1.331 m |

These maxima can occur on different drones; they cannot be added or turned into force/torque contribution percentages. Here all occur at 2 s, but the full/off maximum is drone 15, while the other two are drone 12 (zero-based IDs). Removing torque actually produces a larger maximum displacement from airflow off in this seed. Less tilt does not imply less position change or better flight.

All 12 planned paths completed and passed the declared checks. The six unchanged off/full Boids paths exactly reproduced the specified saved numbers from the preceding checkpoint. Three simple force-only pair controls kept zero rotation by construction, while still having nonzero modeled torque. The independent Python/NumPy audit passed **360,829 implementation assertions**, covering 207 saved endpoints and 96 selected RK stages plus saved-slope step assembly. It verified normal angular dynamics on recorded states with nonzero rates and unequal nominal rotor forces. It did not independently regenerate every integration stage, Boids command or contact check.

Full and force-only medium/fine position differences were 5.35e-8 m and 6.90e-9 m. Of 20 refinement gates, 19 used the predeclared small-error exemption; full-feedback body rate passed the ordinary reduction rule. These sampled checks support numerical consistency, not rigorous trajectory error bounds or formal integration-order validation. Both supervised executions completed within their caps; their 4.447 s and 2.108 s durations are accounting, not performance benchmarks.

The practical lesson for the next experiment is to retain the distinction between collective force and differential moment. Ignoring the moment is not numerically neutral in this example. Force-only still performs the same load solve, so this implementation demonstrates no computation saving. The force-only version is a synthetic intervention in the equations; its solved rotor loads are not a physically realizable set of applied rotor thrusts. The provisional airflow law remains unvalidated, this seed was previously examined, and two seconds does not establish stability, safety, generalization or 5,000-drone dynamic accuracy.

The new Three.js replay shows the three pairwise comparisons using exact saved poses, common viewing bounds and a frame slider. Both scientific allocations are closed. Raw evidence, the frozen protocol, independent checker, review and source/result hashes remain available for regression and future review.
