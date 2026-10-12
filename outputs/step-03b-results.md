# Step 3B — Two drones with an explicit rotor assumption

## Goal and what to try
Connect the candidate airflow model to the verified rigid-body mechanics, using a transparent, testable assumption for the missing rotor response. This is an exploratory model, not physical validation.

Open [the experiment](http://127.0.0.1:8874/outputs/step-03b-two-drones.html), press Reset flight, then Play. The upper blue drone is held in hover; the lower drone responds dynamically. The pale outline is a separately computed receiver with interaction disabled.

1. With the default alignment, the receiver loses lift, sinks and increases its motor commands. It remains level.
2. Set the upper drone's horizontal offset to 0.06 m. Different rotor loads generate pitch and lateral motion.
3. Select “No interaction · baseline.” The receiver remains at 1 m.
4. Adjust initial separation and the still-air thrust limit to explore the model. Controls restart the run. Some combinations stop at an explicit model limit.

The steady altitude offset is expected: our existing controller responds proportionally to altitude error and vertical velocity and has no integral correction. It regulates horizontal velocity rather than holding a horizontal location.

## Methodology in plain language
The upper drone supplies a stationary mean wake. At each integration stage, we evaluate that wake at the four lower rotor hubs. Each motor state is interpreted as the thrust it would produce in still air, and converted to an ideal aerodynamic power. We then ask how much thrust that same power can produce in the incoming downward flow.

More incoming flow reduces lift under this assumption. An offset wake can reduce one pair of rotors more than the other, creating a moment. The receiver's controller responds using the same gains and motor limits as the no-interaction run. The changed receiver position and orientation affect subsequent wake samples.

This is a one-way interaction experiment: the source remains fixed, and the receiver cannot alter its wake. Only the receiver is dynamically integrated; this is not two freely flying, mutually interacting drones.

## Exact assumptions and equations
Let `n_i` be a motor's still-air-equivalent thrust state, in newtons. It follows the existing 40 ms lag toward the controller's command. Set rotor disk area `A = π(0.023 m)²` and air density `ρ = 1.225 kg/m³`. Both are explicit modeling choices, not calibrated here.

The assigned ideal induced power is:

`P_i = n_i sqrt(n_i / (2ρA))`.

For positive axial incoming speed `U_i`, solve for effective rotor thrust `f_i`:

`P_i = f_i [U_i/2 + sqrt(U_i²/4 + f_i/(2ρA))]`.

The right side increases with nonnegative `f_i`. A 40-iteration bisection finds the solution on `[0, n_i]`; zero inflow returns `f_i = n_i` exactly. No extra downward force is added afterward, so the lift reduction is counted once.

This power construction uses ideal actuator-disk momentum reasoning. **Constant ideal induced power at a given motor state is our hypothesis.** It is not a measurement of constant voltage, constant RPM, electrical power or real rotor efficiency. The controller can change the nominal state and therefore the assigned power over time.

The source mean wake uses the implementation from [Step 3A](step-03a-model-selection.md), reproducing the hover model of [Bauersfeld et al.](https://arxiv.org/html/2403.13321v3), Sections III and VI. The ideal power relationship is related to its Section VII. The source remains 27 g, and the length scale supplied here is the 56 mm adjacent rotor spacing from our nominal geometry. This is an illustrative transfer of coefficients, not a validated identification of our vehicle.

Rotor positions are transformed by the receiver quaternion before querying the source wake. The downward airflow magnitude is projected onto the receiver rotor axis; only its nonnegative axial component is used. Receiver translational/rotational velocity contributions to inflow and tangential inflow forces are omitted. Sampling occurs at each hub rather than averaging over its entire disk.

The effective rotor thrusts supply collective lift and roll/pitch moments in the rigid-body equations. Yaw reaction torque retains the previous proportional-thrust approximation; shaft speed, shaft torque and power are not jointly resolved. The model therefore does not claim a complete energetically consistent motor/rotor system.

## Results
All values below are predictions of the assumed model. Initial separation is 0.45 m and nominal maximum thrust is 2.25 times weight. The receiver begins at 1 m with still-air hover motor states, released into an already established wake at time zero. It is not a simulation of source spin-up or wake arrival.

| 16-second experiment | No interaction | Aligned | Upper offset 0.06 m |
|---|---:|---:|---:|
| Maximum altitude loss | 0 m | 0.26988 m | 0.14527 m |
| Final altitude | 1.00000 m | 0.73843 m | 0.87690 m |
| Maximum absolute pitch | 0° | 0° | 15.34695° |
| Final horizontal X position | 0 m | 0 m | 0.08945 m |
| Nominal command saturation | 0% | 0% | 0% |

The smaller altitude loss in the offset case does not imply a gentler interaction: its pitch disturbance is much larger. The final offset-case position is a sample at 16 s, not evidence that the full state has settled.

At initial separation 0.25 m, offset 0.04 m and thrust limit 1.10 times weight, the next integration step would exceed the 20° tilt cutoff. The last accepted state is at 0.165 s. This is a model-limit result, not a prediction of a crash.

## Verification
23 numerical checks passed. They cover zero-inflow thrust recovery, preservation of the assumed induced power at nine operating points, monotonic response, exact no-interaction regression to the previous hover simulation, aligned symmetry, offset torque, mirrored trajectories, timestep convergence in four configurations, finite states and rotor bounds, near-field refusal, and the tilt-limit stop.

The largest matched-time position difference between 5 ms and 1.25 ms integration was 1.40 × 10⁻⁶ m, keeping controller updates at 10 ms. The largest relative residual in the power inversion was 1.04 × 10⁻¹². These are numerical checks, not experimental error bounds.

- [Verification results](step-03b-verification.json)
- [Aligned trajectory CSV](step-03b-aligned.csv)
- [Original coupling code](step03b-source/pair.cjs)
- Run `node outputs/step03b-source/verify.cjs` from the workspace.
- After editing physics, run `node outputs/step03b-source/build.cjs` to rebuild the browser copies.

## Limits and interpretation
The source wake's near-field exclusion is 2.5 chosen length scales (0.14 m). We refuse a query there instead of silently returning zero or extrapolating. The additional 20° receiver-tilt cutoff is an exploratory software boundary, not an experimentally established validity limit. These checks do not ensure validity everywhere else: vehicle scale, flow development, rapid movement, rotor configuration and large distances remain unvalidated.

No walls, ground contact, turbulence, wake memory, source reaction or multi-neighbor interference are modeled. Negative altitude passes through a reference grid, not a physical floor. Wake rings mark half-speed radii; they do not delimit all affected air. Graphics enlarge both drone bodies 2×, while geometry used by physics remains unchanged.

## Conclusion and research implication
We now have a working, inspectable chain from a source wake through an assumed rotor response to receiver motion. The most useful result is methodological: measure moments and attitude as well as altitude when comparing aerodynamic approximations.

This supports continuing to a controlled sensitivity comparison before scaling to a crowd. A single assumed rotor response cannot establish feasibility at a specific drone spacing. Next compare this coupling with a deliberately simpler total-force-only approximation, using the same source wake, initial conditions and controller. That will isolate what changes when uneven rotor loading is discarded. Physical validation still requires matched measured force/moment data, with held-out configurations.

## Interface verification
The existing lab layout was extended and tested in the Codex in-app browser at 1440×1000 and 390×844. Meaningful page rendering, 3D scene, baseline selector, offset and separation controls, nominal thrust limit, playback, seeking, camera presets, and model-limit reporting were inspected. No app console errors or warnings were observed; mobile document width matched its viewport. The initial camera cropped the upper source after receiver descent; framing was corrected to track the pair midpoint and expand with separation. Desktop screenshot: [preview](step-03b-preview.png).

CSV generation was exercised through the numerical verification script. The browser download button, other browsers and real flight were not re-tested in this step. Interface success does not validate the aerodynamic assumptions.
