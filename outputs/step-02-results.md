# Step 2A — One drone: hover, move, brake

10 October 2026. Status: planar mechanics implemented and numerically verified. Full 3D dynamics and physical validation remain open.

[Open the interactive experiment](step-02-drone-lab.html). This standalone HTML works offline in a browser; it requires no external libraries. Use Play, pause, reset, or the time slider. Export CSV saves the complete selected 12-second experiment, including future samples when playback is paused early.

## Follow the experiment

1. Leave **Move & brake** selected and press **Play**. From 0 to 2 seconds, upward thrust balances weight.
2. At 2 seconds, the controller requests 0.5 m/s rightward speed. The drone tilts right, directing some thrust sideways. It then levels out as it approaches the requested speed. Air drag is omitted, so continuing at constant speed needs no sustained sideways force.
3. At 6 seconds, requested speed becomes zero. The drone tilts left even while still moving right: this is braking. It stops near x = 2 m. Zero-speed control does not return it to its starting point.
4. Select **Climb**, lower **Available thrust** to **1.10 ×**, and play. The requested altitude changes from 1 to 3 m at 2 seconds. The motor command reaches its limit; the drone climbs more slowly. Repeat at 2.25 ×.

## What the calculation contains

Position (x,z), velocity, pitch angle, pitch rate, and two motor-group thrusts are dynamic states. Left and right groups represent the two motors on each side of an X-layout quadrotor. Positive pitch directs thrust toward positive x. The equations are:

```text
T = f_left + f_right
horizontal acceleration = T sin(pitch) / mass
vertical acceleration   = T cos(pitch) / mass - gravity
pitch acceleration      = lever (f_left - f_right) / pitch inertia
motor thrust rate       = (commanded thrust - current thrust) / motor time constant
```

Commands are clipped separately for each motor group. A velocity/altitude controller requests total thrust and pitch; an angular controller requests the turning moment. Commands update at 100 Hz, with a 200 Hz physics step and fourth-order Runge–Kutta integration. Timestep comparisons preserve the same controller update rate.

The browser precomputes each deterministic run and plays it back. This makes inspection easy and isolates physics from rendering speed. It is not a WebGPU performance benchmark. The educational side view uses Canvas; Three.js and WebGPU remain later milestones.

## Parameters and assumptions

The [CF2X reference file](https://github.com/learnsyslab/gym-pybullet-drones/blob/main/gym_pybullet_drones/assets/cf2x.urdf) supplies the 0.027 kg mass, 1.4e-5 kg m² pitch inertia, 0.028 m projected motor lever, and baseline 2.25 thrust/weight limit. Values were transcribed from the inspected parameter file; no upstream code was copied. A specific upstream commit has not yet been pinned.

The 0.04 s motor time constant, controller gains, and 15-degree requested-pitch limit are explicit design assumptions. They are not measured calibration results. Gravity is 9.81 m/s². Initial state is airborne at 1 m with motors already supplying hover thrust. No roll, yaw, drag, wakes, wind, sensor noise, battery variation, or contact is represented. Actual pitch is integrated rather than forcibly clamped to the requested limit.

## Measured results from this implementation

| Test | Result | Interpretation |
|---|---|---|
| Hover, 12 s | x = 0 m; z = 1 m | Equilibrium is preserved. |
| Move & brake | Final x ≈ 2.000 m; final sideways speed effectively zero | Acceleration and braking follow the commands. |
| Move & brake peak tilt | 5.862 degrees | The drone turns dynamically; it does not instantly set velocity. |
| Move & brake maximum altitude error | 0.343 mm | Small numerical-model tracking error, not a claim of real-world precision. |
| Climb, 2.25 × thrust | z ≈ 2.462 m at t = 3 s | Higher available thrust supports the requested initial climb acceleration. |
| Climb, 1.10 × thrust | z ≈ 1.453 m at t = 3 s; saturation for 11.83% of the run | Limited motors delay the climb. |
| First reaching z = 2.9 m | t = 3.505 s at 2.25 ×; t = 4.380 s at 1.10 × | Both eventually reach the target, at different rates. |

The gentle sideways maneuver does not saturate at either thrust setting: its peak total thrust is only about 1.006 times weight. A weak visible effect of the slider in that scenario is expected.

## Verification and its limits

All **17 numerical checks passed**: hover equilibrium; analytical free fall; fixed-tilt acceleration; exponential motor response; differential-thrust angular acceleration; finite states and thrust bounds for six configurations; move/brake behavior; climb saturation; and four timestep comparisons.

Across the tested move/climb cases, changing the physics step from 5 ms to 1.25 ms produced a maximum position difference below 1.8e-8 m and speed difference below 1.7e-7 m/s at matched sample times. These tiny differences describe convergence of a smooth, idealized model under the same controller. They do not imply comparable physical accuracy or cover future wake/contact dynamics.

[Machine-readable verification](step-02-verification.json) · [Move/brake samples](step-02-move-brake.csv) · [Physics source](step02-source/physics.cjs) · [Verification script](step02-source/verify.cjs)

Reproduce using Node.js: run `node verify.cjs` and `node build.cjs` from the `step02-source` directory. No npm dependencies are required.

## What we learned and what follows

The controller-to-motor-to-motion chain is implemented consistently in a vertical plane. Limited thrust demonstrably changes transient behavior. This completes an educational and numerical substep of Step 2; it does not complete the planned physical validation.

Before using this as a foundation for aerodynamic claims, extend/verify the full vehicle model as needed, pin reference sources, and resolve independent flight-response and downwash evidence. The next understandable physical question is how a known external downward force changes the motion; introducing it as a controlled disturbance can test mechanics, but calling it realistic downwash requires the independent evidence from Step 1.
