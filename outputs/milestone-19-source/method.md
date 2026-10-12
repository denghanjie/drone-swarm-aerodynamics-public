# A simultaneous soft command filter

At every 10 ms control update each drone first computes its usual local Boids velocity, with the checkpoint18 inward map-guidance offset. It then balances that preferred velocity against local neighbor and obstacle demands **at the same time**. The earlier filter applied demands in sequence and contained abrupt on/off switches.

The new objective is

`J(v) = 0.5 ||v - v_nominal||² + 0.5 Σ w max(0, b - n·v)²`.

Each constraint prefers `n·v >= b`. The weights fade continuously as a neighbor or obstacle leaves the active region. The identity quadratic gives a unique minimizer for fixed inputs, even when soft demands conflict. Squared hinges are continuously differentiable but their second derivatives change at the hinge. We solve the three-variable problem with a semismooth Newton method and line search, monitoring the gradient residual. We then cap the speed at0.9m/s.

The resulting command is not a certified collision-avoidance velocity. Soft constraints can be violated; the speed cap can further change the optimum. The rigid body also has attitude response and motor lag, so requested velocity differs from actual velocity. The claim tested here is improved numerical consistency, not a safety theorem. Small gradient residual only verifies the unconstrained objective solution before the speed cap.

Each drone uses its own current state, nearby drone positions/velocities, and the known map. There is no central assignment of paths, ranks, passage times, leader, or global connectivity graph. Local separation/alignment/cohesion stay active. Connectivity is independently measured using the same1.8m distance throughout.

Physics is unchanged:6DOF rigid-body RK4,27g vehicle,40ms motor lag,100Hz control,airflow off. Physical parameter calibration and flight-data validation remain open. Three.js is a recorded-trajectory viewer, not the numerical engine.

The development study tests tight-course seeds905,1002,1004 at5,2.5,1.25ms for both the old inward controller and new soft filter. Seed905 was previously sensitive in a *different* steering-only controller; the matched interior run here is essential to avoid attributing that earlier difference entirely to the filter.
