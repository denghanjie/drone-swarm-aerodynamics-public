# Milestone 31 — full missions with the frozen wall-priority controller

Question: does the short-window improvement from milestone 30 survive a full factory mission, including larger flocks and narrower doors?

The wall-priority algorithm, gains, local 3D Boids, route guidance, rigid-body physics, initial lattice and contact detection are unchanged from corrected milestone 30. This source adds passive diagnostics only: obstacle IDs, neighboring-drone IDs, the actual state at the last control update, and the actuator command and desired attitude returned by the flight controller. The run still stops on the first contact or vehicle-model limit. No drone is deleted, reset, teleported or assigned a trajectory/slot. Completed drones continue flying.

Ten prescribed jobs:
- A 5,000-drone development continuation uses seed 1501, rerun from its original initial state for 180 seconds. Its 20-second checkpoint must exactly match the retained milestone 30 final state. The historical milestone 26 baseline remains a comparison record.
- Matched baseline/candidate full 180-second trials use fresh seed 2001 at 1,000 and 5,000 drones in the wide factory, plus fresh seed 2002 at 1,000 drones in the narrow factory. Seed and geometry effects are not separately identified between the two 1,000-drone scenarios; each within-scenario controller comparison is matched.
- Candidate 1,000-drone wide and narrow trials each receive a full 1.25 ms refinement. A separate 5,000-drone candidate refinement covers only the first 60 seconds. This does not validate the later 5,000-drone mission.

Wide doors are 5×4 m, narrow doors 3×2.5 m; all other geometry and the shared route are unchanged. Ideal observations, airflow off, 100 Hz control, primary RK4 step 2.5 ms and refinement 1.25 ms. Larger counts occupy larger starting clouds at nominal 0.75 m spacing, not higher density in a fixed volume.

Primary results: first contact type/identity/time, completed count out of the full flock, and whether the prescribed horizon was reached. Record sampled connectivity and clearance separately. An unfinished horizon is not automatically a permanent jam. Describe the last ten seconds of motion of the final unfinished drones using common saved positions; mean forward displacement below 0.2 m is an operational low-progress flag, not a proof of deadlock. Do not stop runs because that flag is raised.

Refinement: compare exact common saved frames, with a 1 cm maximum positional-difference criterion. Also report contact identity, stop-time difference and passage count separately. Full-pair outcome agreement requires the same event identity/count and stop times within 10 ms. For the 60-second 5,000 comparison, use the primary 60-second checkpoint when available; if both runs contact before 60 seconds, report an early-stop comparison explicitly. A missing checkpoint is not replaced by a fabricated state. No unequal-time endpoint error is called synchronized trajectory error.

Retain full 17-component endpoints, exact Float64 poses every second and at stop, 0.1-second science samples, and full-state checkpoints at 20/60/120/180 seconds when reached. The whole pre-contact snapshot belongs to the actual preceding control update, not a recomputation at the contact state. Actuator targets are not measured thrust; the state contains the motor-lag thrust values separately.

All evaluation seeds, controllers, geometry, horizons and refinements are frozen before evaluation. No tuning in response to outcomes. Two numerical subprocesses may overlap; elapsed times are not a scaling benchmark. Three.js shows offline trajectories with visual interpolation, not real-time physics throughput. General navigation safety, physical calibration, airflow validity and algorithmic novelty remain unestablished.
