# Step 3D — Controller sensitivity

## Goal
Check whether Step 3C's model disagreement disappears when the receiver tries to return to its original horizontal position. Use a two-by-two comparison: two aerodynamic models, each with two controllers. All four runs start at the same state and use the same source wake, motor limits and physical assumptions.

[Open the 3D comparison](http://127.0.0.1:8874/outputs/step-03d-controller-comparison.html). Select Horizontal X position or Pitch in the plot menu, then Play. Solid is the selected prediction; purple changes the aerodynamic model only; orange changes the controller only; pale is undisturbed hover. These are alternative predictions for one receiver, not multiple receivers interacting.

## Method: what position holding means here
The old controller requests zero horizontal velocity. The new controller requests velocity toward the original horizontal position:

`v_xy_requested = −k_position × (position_xy − target_xy)`

Here target_xy = (0,0), k_position = 1 s⁻¹, and the requested velocity vector is capped at 0.5 m/s without changing its direction. This request goes into the existing velocity and attitude loops. Their gains, the 15° requested-tilt cap, altitude loop, 40 ms nominal motor lag, 10 ms controller updates and 5 ms integration remain unchanged. No integral action or aerodynamic feedforward was added.

These are fixed illustrative settings, selected before evaluating outcomes. They were not fitted to flight data or tuned separately for either aerodynamic model. “Hold position” is a requested behavior, not a claim that the controller will succeed under disturbance.

The aerodynamic models are unchanged from Step 3C. One applies unequal wake-derived rotor forces and moments. The other applies the same total thrust at an identical state while removing the aerodynamic moment changes and retaining nominal control torques. Both retain the hypothetical constant ideal induced-power conversion; neither is physically validated.

## Default results
Initial vertical separation 0.45 m; source horizontal offset 0.06 m; still-air thrust limit 2.25× weight; all four runs complete 16 seconds.

| Metric | Rotor model, velocity control | Rotor model, position control | Force-only, either controller |
|---|---:|---:|---:|
| Maximum horizontal position error | 20.76 cm | 20.03 cm | 0 cm |
| Horizontal RMS position error | 11.69 cm | 11.57 cm | 0 cm |
| Maximum absolute pitch | 15.35° | 16.85° | 0° |
| Maximum altitude loss | 14.53 cm | 14.34 cm | 19.49 cm |
| X position at 16 s | +8.95 cm | −2.48 cm | 0 cm |

RMS means the square root of the average squared horizontal distance from the target, sampled uniformly over the shared interval. It summarizes displacement throughout the trajectory, rather than selecting one endpoint.

The new loop reduces RMS horizontal error by only about 1.1%, and peak displacement by about 3.5%, while increasing peak pitch. The smaller endpoint error alone would overstate the improvement: the rotor-model receiver continues to oscillate. A full 16-second run merely means it did not trigger our stopping criteria; it is not proof of asymptotic stability.

Force-only runs remain level at x=y=0 under these symmetric initial conditions, so adding position feedback does not change them. This is expected behavior of that model, not evidence that real downwash has no lateral effect.

## Thirty configurations, four runs each
We repeated the same grid from Step 3C: gaps 0.25/0.45/0.80 m, offsets 0/0.04/0.06/0.12/0.20 m and still-air thrust limits 1.10/2.25×. This produces 120 deterministic trajectories over 30 configurations.

All four runs reached 16 seconds in 17 configurations. In 13, at least one run reached a model limit sooner. Each comparison uses the earliest stopping time among all four runs. CSV rows include both the common end and each run's own end and stop reason. Short-window metrics must not be compared to full-window metrics without accounting for the different observation times. These are simulated configurations, not independent experimental samples or flight-success rates.

## Verification
11 targeted checks passed:

- Restoring velocity sign and vector speed-cap direction.
- Exact regression of both aerodynamic models with the old velocity controller.
- Recovery from a 10 cm initial displacement without wake under position control; persistence of displaced hover under zero-velocity control.
- Smaller-timestep agreement for both aerodynamic models with position control.
- Shared four-way horizons, finite states and normalized quaternions throughout the sweep.
- Agreement of the two controllers in aligned rotor-model cases.

The displaced-hover test checks that position feedback actually works in a simpler setting. The wake experiment then tests a different question: whether that same fixed controller handles this assumed aerodynamic disturbance.

Run `node outputs/step03d-source/verify.cjs`. Rebuild browser physics after source edits with `node outputs/step03d-source/build.cjs`.

- [Verification and complete metrics](step-03d-verification.json)
- [Sweep CSV](step-03d-sweep.csv)
- [Default four trajectories](step-03d-default-trajectories.csv)
- [Controller and physics source](step03d-source/pair.cjs)

## Conclusion
For these fixed gains and assumed aerodynamics, adding position feedback does not remove the substantial difference between force-only and rotor-resolved motion. The earlier disagreement cannot be explained solely by the old controller allowing a displaced hover. However, this does not prove that all position controllers would perform poorly: a different controller or gains could change the outcome.

The research comparison should therefore vary controller choice explicitly, report whole-trajectory errors and operating-limit events, and avoid selecting a controller/model based on its final position alone.

## Next step and remaining limits
Before increasing drone count, characterize the local closed-loop stability of the rotor model near an offset operating point. A controlled gain study, with gains chosen on one configuration and evaluated on others, can test whether the oscillation is a controller/model interaction. Do not tune each aerodynamic model independently and then attribute all performance differences to airflow physics.

The larger validation gap remains: the rotor response and wake transfer to this nominal 27 g vehicle are uncalibrated. Receiver-motion inflow, wake history, disk averaging and bidirectional interaction are omitted. Actual force/moment data are needed to decide whether the predicted oscillation occurs in physical flight. No crowd-scale feasibility, safety threshold or novel physics claim follows from this comparison alone.

## Interface verification
The in-app browser rendered the comparison at desktop 1440×1000 and mobile 390×844. Controller selection exchanged the expected state readouts, playback and seeking worked, the horizontal-position plot rendered, and the early-stop case displayed a shared 0.165 s interval. No app console errors or warnings were observed; mobile width matched the viewport. The desktop screenshot was saved and inspected. Browser CSV downloading and other browsers were not tested; verification generated the numerical CSV files.
