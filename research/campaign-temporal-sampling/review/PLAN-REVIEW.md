# Independent temporal-plan review

Reviewed 2026-10-13 before numerical execution. Recommendation: adopt PROPOSED-PLAN-AMENDMENT.md, freeze final plan/configuration/source hashes, and require a separate implementation review before granting execution. The original plan is scientifically appropriately scoped but not executable without resolving its gate, event, excitation and cap ambiguities. No simulations, benchmarks or synthetic numerical checks were run for this review.

## Source findings

- Four held inflows are nonnegative scalar rotor values. Source/receiver-axis projection occurs inside field evaluation, not when the held load is applied: integration/publication-v2/src/exact-aero.cjs:85-105, especially 99-105.
- Endpoint loads return thrust force in world coordinates and body torque with nominal yaw retained: exact-aero.cjs:116-121. Nominal endpoint thrust must be nonnegative. This function has one-state/one-four-inflow signature; whole-swarm notation in the prose must be implemented by mapping over drones.
- At each RK4 derivative stage, aerodynamic effective thrust is recomputed from that stage's nominal motor states and the held scalar inflows. Current stage attitude is used by the rigid-body derivative. Aerodynamic yaw replacement is undone and the nominal motor ODE is restored: implementation/repo/outputs/milestone-28-source/aero.cjs:18-19 and outputs/step02c-source/physics.cjs:15,18-19. Do not normalize intermediate RK4 quaternions or reuse endpoint load results for stage derivatives.
- Physics quaternion order is [x,y,z,w], body/world +z up; angular velocity and inertia are in body coordinates: physics.cjs:1,3-7,17-19. Rotors are [±a,±a], so centre-to-rotor distance is sqrt(2)*a, while opposite-motor distance is 2*sqrt(2)*a. These distinct scales must remain distinct; neither is physically validated by this study.
- Production loop is field, control, integration, then safety. There is no terminal field/control event: publication-v2/src/boids.cjs:13-30. Same-path diagnostics may evaluate a separate instantaneous terminal field without altering production final held-field evidence.
- The inherited controller remains genuine local 3D separation/alignment/cohesion plus a shared broad route and wall/pair constraints: implementation/repo/outputs/milestone-31-source/sim.cjs:7-25. No scripted path is needed or permitted.
- Full source read/hash checks match all 11 dependencies recorded in prior provenance plus exact-aero.cjs (12/12). Details are in SOURCE-STATIC-AUDIT.json. Existing publication source.cjs has placement-dependent fallback resolution; the new standalone harness needs a pinned snapshot and resolved dependency manifest rather than assuming that archival directory is directly runnable.

## Blocking corrections supplied

1. Distinguish production final held values, diagnostic instantaneous fields, and refresh left/right limits; include left limits in sampled peaks and event-aware quadrature.
2. Make reference-screen failure branching explicit. Stop later coupled rows; permit only conditional replay of valid already-saved drivers. A dense diagnostic model-domain failure is a hard failure, not a screen failure or a zero wake.
3. Define physics reduction floors, airflow reduction floors, ancillary coupled thresholds, and vector-prefix quadrature comparisons exactly. Avoid relative normalization by a potentially vanishing error.
4. Freeze loaded-fraction, inflow-range and load-amplitude excitation labels before seeing new outcomes. Preserve numerical results for low-excitation cases while preventing a general cadence recommendation.
5. Replace the suggested storage number with a hard decimal-byte cap, reserve failure-record capacity, and enforce independent job/total watchdogs. Distinguish an exact cooperative stop record from the last durable checkpoint after an external kill.
6. Retain full fine drivers/fields and common-time comparison states so maxima and failures are independently recomputable. Raw planned arrays require about 76.22 MB before metadata, leaving practical room beneath 150 MB.

No additional numerical-method paper is asserted as an authority for the new thresholds. Existing audited sources establish model/controller provenance and historical motivation; the new refinement and quadrature conditions are explicitly analyst-designed empirical screens. Two mesh comparisons and two seeds cannot prove an asymptotic convergence order, continuous-time error bound, physical validity or general mission adequacy.
