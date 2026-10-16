# Saved-result interpretation and next controlled question

2026-10-16. Source commit `ee1c888d1e10fd712750c8a80150b13abb32eb19`; source manifest `4cffb621a5925441fd0c4fcea5a55e7d1fa70d7bd931496fd74b45d9bcb6b63d`. This review read saved JSON and summarized saved values only. No model import/evaluation, geometry reconstruction, integration, new target, external access or repository edit occurred.

## What the completed diagnostic establishes

All 18 primary and six conditional exploratory paths completed. Null, symmetry, initial-wrench and sampled-resolution gates passed. The independent saved-only reviewer passed 283,446 assertions over 234 saved endpoint arrays and 192 captured first/last-stage witnesses, including independent geometry/load/derivative checks and saved-slope RK4 assembly. Those assertions are implementation checks, not independent physical observations. Unsaved stages have candidate diagnostics; the reviewer did not reintegrate the paths, rerun the controller or independently certify collisions.

The supported conclusion is narrow and useful: this frozen projected-stage RK4 implementation applies the provisional current-pose load law consistently on these cases, and its shared-time observables change very little across the three chosen timesteps. Every one of the 32 scalar convergence gates has `bothTiny=true`: both adjacent-grid discrepancies were below the predeclared 1%-of-tolerance comparison floor. Consequently the gate passes do not establish an observed convergence order. For coupled Boids the medium–fine maxima were 5.354e-8 m position, 2.141e-7 m/s velocity, 1.433e-7 rad orientation and 1.136e-7 of nominal-hover rotor force. These sampled differences are not rigorous continuous-time error bounds.

## What the simulated response means

| Saved finest-grid result | Interpretation |
|---|---|
| No-influence on/off full-state discrepancy zero, empty coupling and identity loads | The null branch and adapter identity behave as declared. |
| Centered lower vehicle drops 0.245510 m in 0.5 s; zero tilt and zero moment correction | Common axial load loss produces descent while the symmetry control remains exact. This is a fixed nominal-input fall, not stabilized hover. |
| Offset lower vehicle ends at 92.972767° body-axis tilt after 0.5 s; displacement from off is 0.496115 m | Differential loads produce a strong rotational/lateral response within the equations. This run leaves the near-hover regime substantially despite remaining computationally admitted. |
| Boids maximum sampled on/off position difference 1.102444 m over 2 s | The coupling has a consequential effect in this one simulated seed/controller. That effect is far larger than the observed grid differences. |
| Boids maximum sampled quaternion orientation difference 1.468352 rad, about 84.13° | This is full orientation separation and includes yaw. It must not be labeled vehicle tilt. |
| Boids maximum recorded stage tilt 19.555806° coupled versus 8.853804° off | These are the actual body-axis tilt diagnostics. The two maxima occur at different stages/times. |

The offset record contains a useful temporal qualification: initial pitch correction is +2.99659e-4 N m; by 0.3 s it is -6.79317e-5 N m; at 0.5 s all four loads equal their nominal values and both added force and moment are zero. Nevertheless the final pitch rate is 3.81178 rad/s. The saved motion is consistent with transient moment input followed by inertial carry-through; it does not require persistent final forcing. The held nominal commands provide no attitude restoration.

In Boids, the maximum sampled on/off rotor-force difference (0.328858 times mg/4) and the maximum coupled effective-minus-own-nominal change (0.303468 times mg/4) are different quantities. The former includes changes mediated through the controller and nominal motor states. Neither is a measured thrust loss. The candidate reports smaller minimum swept separation with coupling (0.571454 m versus 0.613391 m off), so these records provide no basis for claiming a safety improvement. Segment/contact checks also do not certify continuous safety.

## Claims these records can and cannot challenge

The results contradict a no-effect implementation hypothesis for these nonzero-influence simulated cases, and give strong evidence against the three tested timesteps being the main cause of the large on/off response. They support the sign/frame bookkeeping and declared sampled self-consistency. They do not validate the inherited ideal-power closure, moving/tilted wake physics, fixed-input-to-physical-power interpretation, retained nominal yaw torque or omitted wake history/self-airspeed terms. Computational admission beyond 90° tilt is not a physical validity certificate. The offset result is an especially clear warning against presenting this checkpoint as accurate near-hover flight physics.

The 2.550640 s candidate and 1.050639 s reviewer supervisor times close the allocated execution accounting. They are neither a browser benchmark nor evidence for 5,000-drone feasibility. The physical-validation and broader scale/novelty goals remain open.

## Recommended next decision

Close this numerical implementation diagnostic as completed, preserve its limitations, and prioritize a mechanism question before expanding fleet size or making a physical claim: **in the same 16-vehicle seed and controller, how much of the trajectory/tilt response survives when the aerodynamic roll/pitch correction is suppressed while the collective-force correction remains?**

A prospective comparison would use off, full correction and collective-force-only arms, with unchanged initial state, controller/gains, held-input schedule, load law, source/receiver solve, projection and predeclared numerical gates. In the collective-only arm set the added body roll/pitch moment to zero; retain the original nominal moments, motor lag and yaw treatment. Compute the axial correction from that arm's own current states at each stage. This is an explicit software intervention within the hypothetical model, not a new physically realizable actuator law. A fixed-input centered/offset pair can serve as an implementation control: with zero initial rates and equal nominal inputs, removing added moments predicts zero rotation by construction, so repeating that fact alone adds little mechanism evidence.

Predeclare body-axis tilt and angular-rate summaries separately from full quaternion orientation, alongside position/altitude and own-nominal force deficits. If collective-only retains a comparable Boids response, direct aerodynamic differential moments are not required for most of the chosen response measure; collective-force loss and controller feedback remain plausible contributors. If the response falls substantially when moments are removed, that supports dependence on the moment pathway in this model. Because the trajectories change, subsequent geometry, forces and commands also change: the contrast measures the total consequence of suppressing that pathway, and cannot be decomposed additively into independent force and moment contributions. A full force/moment factorial would be justified only if that interaction becomes the next question.

Freeze any equivalence or material-change threshold and fresh finite allocation before such a comparison. No new arm, rerun or allocation was started by this review. A result either way would refine the model's causal explanation; compatible independent physical measurements are still needed to decide whether that explanation describes real vehicles.
