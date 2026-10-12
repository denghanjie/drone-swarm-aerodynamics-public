# Step 3C — Does uneven rotor loading matter?

## Goal
Determine how much predicted motion changes when we keep wake-induced lift loss but remove its rotational effect. This is an internal comparison between two hypothetical models, not a comparison against experimental truth.

## Understand the experiment
Open [the 3D comparison](http://127.0.0.1:8874/outputs/step-03c-model-comparison.html). Start with the default 0.45 m vertical separation, 0.06 m horizontal offset and 2.25× still-air thrust limit.

1. Press Play. The solid receiver follows the selected model; the purple wireframe follows the other model. The pale reference stays at undisturbed hover. The blue source is fixed.
2. Choose Pitch in the plot menu. Uneven rotor loading produces rotation; the force-only receiver stays level from these initial conditions.
3. Choose Horizontal X position. Rotation directs lift sideways, changing the receiver's path and the wake it encounters.
4. Set offset to zero. Symmetry makes the two models agree.
5. Inspect Total force only to exchange the solid and purple roles. Both runs are recomputed with identical starting conditions.

These are alternative predictions for the same receiver, not several receiving drones interacting at once.

## Methodology: change only the aerodynamic moments
Both models evaluate the same wake at all four rotor hubs and solve the same assumed constant ideal induced-power relation from [Step 3B](step-03b-results.md). The source is stationary, and its wake is not affected by the receiver.

Let `n` be the vector of nominal still-air rotor thrust states and `f` the wake-adjusted rotor thrust estimates. Let `T` and `τ` denote total thrust and body torque from a rotor vector.

| Term | Uneven rotor model | Total-force-only model |
|---|---|---|
| Collective thrust | T(f) | T(f) |
| Body torque | τ(f) | τ(n) |
| Motor-state dynamics | Existing nominal lag | Identical lag |
| Controller and limits | Existing controller | Identical controller |

Thus the simplified model removes `Δτ = τ(f) − τ(n)`, while retaining commanded control torques. It does **not** set all torques to zero. Total force remains along the receiver's body lift axis; this differs from prescribing an arbitrary world-vertical force.

At an identical state, both models have identical linear accelerations. Once their trajectories diverge, their positions, motor states and sampled flow also diverge. Their actual force histories then need not match. This feedback is part of the comparison.

This is a controlled removal of a model feature, often called an ablation. It still evaluates four rotors and is not offered as a computational optimization. It isolates one assumption before we design faster approximations.

## Default results
16-second simulation, same initial conditions and settings in both models:

| Metric | Uneven rotor loads | Total force only |
|---|---:|---:|
| Maximum altitude loss | 0.14527 m | 0.19492 m |
| Maximum absolute pitch | 15.34695° | 0° |
| Maximum horizontal separation between predictions | 0.20759 m, jointly measured | Same comparison |
| Maximum altitude difference between predictions | 0.07741 m, jointly measured | Same comparison |

The last two metrics compare the models at matching times; they are not differences between independently timed extrema. Neither model reaches the 20° cutoff in this default case.

The simpler model predicts more altitude loss here, while missing all of the predicted pitch and sideways motion. Therefore, “more conservative altitude loss” does not imply “more conservative motion overall.” That is a result of this hypothetical model/controller combination, not an established property of real quadrotors.

## Parameter sweep and fair time windows
We ran all 30 combinations of:

- Initial vertical separation: 0.25, 0.45 and 0.80 m.
- Source horizontal offset: 0, 0.04, 0.06, 0.12 and 0.20 m.
- Still-air thrust limit: 1.10× and 2.25× weight.

Both runs reached 16 s in 18 configurations. The remaining 12 comparisons ended early at a model limit. Every sweep row reports the common end time and each model's stop reason. Metrics in those rows cover only that common interval and must not be ranked directly against full 16-second metrics as if observation times were equal. No stopped path is continued or silently held stationary.

The sweep is a deterministic exploration, not 30 independent empirical trials. It supports no confidence interval or population-level claim.

## Verification and files
12 targeted checks passed: same-state translational and motor-derivative equality, preservation of nominal control torque in force-only mode, nonzero aerodynamic moment in rotor mode, exact Step 3B rotor-model regression, two no-interaction regressions, aligned trajectory agreement, level/centered force-only hover response, smaller-timestep agreement, finite matched-time sweep metrics, and explicit truncated-case handling.

The numerical and modeling limitations of Step 3B remain: uncalibrated wake transfer to a 27 g vehicle, idealized power response, hub sampling, approximate yaw reaction torque, no receiver-motion inflow, turbulence, walls or ground contact. The 20° cutoff is a software boundary, not a safety limit. No new physical validation or performance benchmark is claimed.

- [Sweep CSV](step-03c-sweep.csv)
- [Default model trajectories](step-03c-default-trajectories.csv)
- [Verification JSON](step-03c-verification.json)
- [Comparison physics](step03c-source/pair.cjs)

Run `node outputs/step03c-source/verify.cjs` from the workspace. After editing physics, run `node outputs/step03c-source/build.cjs` to update the browser copy. The demo's CSV export contains all three predictions over the common interval, with model and experiment settings; the saved default trajectory CSV contains the two interacting models.

## Conclusion and implications
Under our current assumptions, discarding aerodynamic moments materially changes the motion of an offset receiver, even when the total force rule is kept identical. A credible comparison of swarm models should therefore include attitude and lateral path errors alongside altitude and throughput.

This is not proof that the rotor model is more physically accurate: measurements are still needed to establish that. It is evidence that this modeling choice can alter conclusions and deserves an explicit place in the research design.

Before expanding to a crowd, the next useful control is to repeat the comparison with horizontal position holding. Our present controller regulates horizontal velocity; some lateral drift is therefore allowed by design. Keeping both controller versions explicit will help distinguish an aerodynamic-model effect from a controller-dependent outcome.

## Interface checks
In-app-browser checks passed at 1440×1000 and 390×844: page identity and meaningful rendering, playback and seeking, model selection, pitch plotting, parameter changes and a shared 0.165-second stopping window. No app console errors or warnings were observed; mobile document width matched viewport width. Desktop screenshot was saved and inspected. Plot selection is preserved when experiment settings change. The browser CSV download was not exercised; numerical CSV output was generated by the verification script. Other browsers and physical flight remain untested.
