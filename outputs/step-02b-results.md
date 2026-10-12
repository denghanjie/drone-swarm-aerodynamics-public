# Step 2B — Three.js and full 3D mechanics

10 October 2026 · Numerically verified; physical validation pending

## Open and explore

The running experiment is [available locally](http://127.0.0.1:8874/outputs/step-02b-drone-3d.html). Its entry file is [step-02b-drone-3d.html](step-02b-drone-3d.html). It uses locally stored Three.js r180 and OrbitControls. Use a local HTTP server rather than double-clicking the file, because browser module loading can be restricted for file URLs. If the server has stopped, run `python3 -m http.server 8874 --bind 127.0.0.1` from the project folder.

1. Press **Play** with **3D flight sequence** selected. Hover lasts 2 seconds; the drone moves along X until 5 s, along Y until 8 s, then brakes and climbs to 1.8 m. At 11 s it turns 90 degrees.
2. Drag the scene to orbit. Scroll to zoom. Use **Top**, **Side**, or **Perspective** to restore a convenient camera angle. **Follow** moves the camera with the drone; turn it off to watch the path from a fixed location.
3. Scrub to **5.3 s**. Both roll and pitch are active: the drone brakes its X motion while starting Y motion.
4. Scrub to **11.25 s**, select **Top**, and plot **Yaw angle**. Opposite-spin motor pairs have different thrusts while the drone turns.
5. Select **Climb**, set thrust to **1.10 ×**, and inspect **2.5 s**. All motors reach their limits. Compare with **2.25 ×**.

The drone drawing is enlarged sixfold to make orientation visible; physical coordinates and force calculations retain the original dimensions. The orange nose marks body-forward. Rotor animation is schematic. The grid provides a spatial reference, not a solid collision surface. CSV export saves all 3,201 samples from the selected 16-second run.

## What changed from Step 2A

Three.js now displays a genuine three-dimensional model with a perspective camera. Independently, the physics now contains position and velocity in three dimensions, a quaternion orientation, three body angular rates, and four individually evolving motor thrusts. This represents six rigid-body degrees of freedom: three translations and three rotations.

The equations are Newton–Euler rigid-body dynamics:

```text
m dv/dt = R(q) [0, 0, sum(motor thrusts)] + [0, 0, -mg]
I dω/dt = motor torque - ω × (Iω)
dq/dt   = 0.5 q ⊗ [ωx, ωy, ωz, 0]
df_i/dt = (clipped motor command_i - f_i) / motor time constant
```

World and body +Z point upward. Quaternions use [x,y,z,w]. Roll/pitch moments follow each rotor's lever arm; yaw reaction torque is proportional to rotor thrust, with alternating signs. The controller requests an orientation from desired acceleration and heading, then allocates collective thrust and three torques to four motors. It clips each motor command separately. There is no instantaneous overwrite of position or attitude.

Physics runs with a 5 ms step using RK4; control commands update every 10 ms. The complete deterministic run is computed on the CPU when settings change and played back through Three.js/WebGL. This separation supports inspection; WebGPU compute and swarm performance remain later work.

## Parameters, provenance and limitations

The public CF2X parameter source is pinned to commit [7ebad1ecabd28a7000add2d05f888aa2e837c2cc](https://github.com/learnsyslab/gym-pybullet-drones/blob/7ebad1ecabd28a7000add2d05f888aa2e837c2cc/gym_pybullet_drones/assets/cf2x.urdf), with a local copy and MIT notice under `step02b-source/vendor`. Mass is 0.027 kg; inertia diagonal is (1.4e-5, 1.4e-5, 2.17e-5) kg m². Rotor coordinates use ±0.028 m; torque/thrust ratio uses the source km/kf values. Motor indices follow our documented ordering, not the upstream ordering.

The motor time constant of 0.04 s, control gains, and requested tilt cap of 15° remain explicit assumptions. This model omits drag, wake interaction, sensing error, rotor gyroscopic effects, battery changes, ground effects and contact. Perfect symmetry makes hover unusually clean. No claim of matching real flight follows from the numerical tests.

## Results

| Experiment | Measured outcome in this model |
|---|---|
| Hover | Remains at (0,0,1) m. |
| Move & brake | Stops near (2,0,1) m, with negligible final velocity. |
| Yaw alone | Reaches 90° while maintaining altitude and negligible translation. |
| Full sequence, 2.25 × thrust | Ends near (1.5005,1.5218,1.8000) m and 90° heading. |
| Full sequence, 1.10 × thrust | Ends near (1.5006,1.8548,1.8000) m; motor commands saturate for 6.81% of the run. |

The low-thrust sequence travels about 0.333 m farther along Y before stopping. Climbing and braking compete for the available motor forces. This is a consequence of this controller/model, not a measured claim about a real Crazyflie. Horizontal control requests velocity, not an exact stopping position. Accordingly, the flight acceptance test checks travel in the intended directions and a stop, rather than falsely requiring the integrated requested velocity to equal the final position exactly.

## Verification

**30 checks passed**, covering analytical free fall; fixed roll/pitch acceleration; motor exponential response; mixing and each motor's torque direction; torque-free energy and world-angular-momentum conservation; finite states, quaternion normalization and motor bounds in ten runs; yaw, movement and saturation behavior; and eight timestep-refinement comparisons.

Across the checked cases, comparing 5 ms and 1.25 ms physics steps with identical control timing gave maximum position differences below 1.8e-8 m, velocity differences below 1.7e-7 m/s, and attitude differences below 1.8e-7 radians. These are numerical convergence results for the simplified dynamics, not physical accuracy estimates.

[Verification JSON](step-02b-verification.json) · [Flight CSV](step-02b-flight.csv) · [Physics implementation](step02b-source/physics.cjs) · [Verification script](step02b-source/verify.cjs)

To reproduce, run `node verify.cjs` and `node build.cjs` inside `step02b-source`. The build synchronizes the browser physics copy. The library versions and licenses are stored locally.

## Browser checks

Tested in the Codex in-app browser at 1440 × 1000 and 390 × 844. Playback, seeking, scenario changes, camera presets, drag-to-orbit, force visibility, thrust adjustment, plot selection, reset, and CSV download were exercised. Mobile content width matches the viewport. The export contains the expected data header and 3,201 samples.

The existing white/navy/teal design was extended rather than replaced. Copy, layout, typography, colors, panels and responsive stacking were reviewed; the live 3D scene, motor bars, camera controls, and multi-variable chart are intentional additions. Camera framing was tightened, visual drone scale was labeled, and a scene-height growth issue was corrected. Screenshot captures were visually inspected.

## Conclusion and next step

Step 2B provides the promised Three.js demonstration and verified six-degree-of-freedom mechanics. Step 2's empirical validation remains incomplete. We can next test a known external force in the mechanics, while resolving experimental data and actuator calibration before representing that force as validated downwash. A more detailed scene does not itself improve aerodynamic accuracy.
