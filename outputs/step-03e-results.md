# Step 3E — Can controller gains stop the oscillation?

The selected gains produce less tilt but worse horizontal position holding. Both tested gain sets have an unstable steady hover in the uneven-rotor model at the default geometry. The force-only model predicts a stable hover there. This reinforces the need to diagnose aerodynamic moments before drawing swarm-performance conclusions.

## 1. Research question

Are the oscillations merely a poorly chosen controller setting, or does the current aerodynamic coupling change closed-loop stability? We test local stability and a limited gain search. We do not establish that no stabilizing gains exist.

Open `step-03e-stability-lab.html` through the existing local server to explore the Three.js comparison. The renderer uses WebGL; physics is precomputed on the CPU.

## 2. Understand what we did

**Equilibrium** is a balance point: position, attitude, rates and motor states stay constant, and the controller keeps requesting those same motor states. We solve for it rather than treating the last frame of an oscillating flight as settled.

**Local stability** asks what happens after a very small nudge near that balance point. A locally stable system brings sufficiently small disturbances back. An unstable system has at least one kind of small disturbance that grows. This does not predict every large maneuver or prove that there are no other equilibria.

**A mode multiplier** is the factor applied to a particular disturbance pattern over one 0.01-second control cycle. Its magnitude below 1 means decay; above 1 means growth. It is not a claim that every position error grows by that factor on every frame. Complex modes also oscillate.

**Controller gains** set how strongly the drone reacts. Horizontal position feedback asks it to return; velocity feedback reacts to movement; attitude feedback asks it to tilt; angular-rate damping resists rapid rotation. Adding damping can calm tilting while slowing the response needed to hold position.

**RMS error** is the square root of the average squared error over the flight. It summarizes the whole trajectory and gives larger errors more weight. It avoids mistaking a brief return through the target for settling.

## 3. Fixed study design

Training case: initial vertical gap 0.45 m, source offset 0.06 m, nominal still-air thrust limit 2.25 times weight. Duration 16 s; control period 0.01 s; RK4 integration step 0.005 s. The fixed source is above a receiver initially at (0, 0, 1) m with still-air hover motor states. The established wake is present from release.

The grid, score and evaluation configurations were written before running the study. This is an internal fixed protocol, not an externally preregistered experiment. The evaluation cases were excluded from selection in this study; related geometries appeared in previous exploratory stages, so this is not a blind validation dataset.

- Position gain: 0.5, 1, 2 s⁻¹.
- Horizontal velocity gain: 1, 2.5, 4 s⁻¹.
- Attitude gain: fixed at 100 s⁻².
- Angular-rate damping: 20, 30, 40 s⁻¹.
- Total: 27 candidates. Other model parameters and command caps are unchanged.

Score = horizontal RMS / 0.1 m + altitude RMS / 0.2 m + 3D speed RMS / 0.5 m/s + tilt RMS / 10°. The normalizing scales are exploratory preferences, not measured safety limits. Samples are equally spaced and equally weighted, including endpoints. Only runs completing 16 s are eligible. Select the lowest training score. Do not tune separately for the two aerodynamic models.

The selected gains are position 0.5, velocity 2.5, attitude 100, damping 40. Original gains are 1, 2.5, 100, 20 respectively. This is the best candidate under this score and grid, not an optimum over all controllers.

## 4. Local stability method and results

We numerically solve F(x) − x = 0, where F advances one actual sampled control cycle: calculate commands once, hold them, and apply two RK4 steps including motor lag. The state uses 16 independent coordinates: position, velocity, three quaternion vector components, three body rates, and four motor states. The quaternion scalar is reconstructed on the positive branch. This removes the redundant quaternion-norm direction.

Central finite differences with absolute increment 1e−5 in each coordinate produce the Jacobian of F. We obtain its eigenvalues with macOS Accelerate LAPACK `dgeev`. The increments have each coordinate's native units; halving all increments checks sensitivity. We separately halve the RK4 step while preserving the 0.01 s controller period. This is a linearization of the numerically integrated sampled system, not an exact analytic continuous-time proof.

The solver is initialized at ordinary hover without wake, and near x = 0.06 m, z = 0.75 m for the uneven-rotor wake case. Force-only initialization uses x = 0. The root search does not establish uniqueness. Every reported root has positive motor states below their limits, no command clipping, and negligible instantaneous derivative as well as sampled-map residual.

| Gains | Aerodynamics | Largest multiplier magnitude | Local classification |
|---|---|---:|---|
| original | no wake | 0.98132215 | Stable |
| original | rotor | 1.01984142 | Unstable |
| original | force-only | 0.98417034 | Stable |
| chosen | no wake | 0.99387425 | Stable |
| chosen | rotor | 1.01704346 | Unstable |
| chosen | force-only | 0.99366767 | Stable |

The uneven-rotor equilibria lie at approximately (0.05787, 0, 0.73852) m with original gains and (0.05892, 0, 0.73845) m with selected gains. They are substantially below the 1 m altitude target. A proportional controller can need persistent error to request extra thrust or balancing torque. These equilibrium positions differ from the 16-second endpoints of the released flights.

The growing modes are oscillatory. Removing aerodynamic moment changes also changes the equilibrium, so this comparison does not isolate one derivative at an identical state. It does establish a qualitative difference between the two complete closed-loop model variants at their respective equilibria. We have not decomposed the instability into spatial wake gradients, motor effectiveness and lag contributions.

## 5. Full-flight results

| Training result | Original gains | Selected gains |
|---|---:|---:|
| Horizontal RMS (cm) | 11.5686 | 14.5068 |
| Peak pitch (degrees) | 16.8502 | 9.1627 |
| Altitude RMS (cm) | 11.3701 | 9.5304 |
| 3D speed RMS (m/s) | 0.4114 | 0.3581 |
| Combined score | 3.4519 | 3.1684 |

The score improves about 8.2%, but horizontal RMS worsens about 25.4%. The score rewards reduced speed and tilt enough to outweigh worse position holding. Neither score nor reduced pitch certifies stability.

Evaluation cases below use the same selected gains. Metrics compare the earliest common horizon across both gains and both aerodynamic models. They are not all 16-second results.

| Gap / offset / thrust limit | Shared time | Rotor horizontal RMS, original → selected | Peak pitch, original → selected |
|---|---:|---:|---:|
| 0.25 m / 0.04 m / 2.25× | 16.00 s | 12.10 → 14.57 cm | 19.85 → 11.22° |
| 0.45 m / 0.12 m / 2.25× | 16.00 s | 12.76 → 15.41 cm | 17.52 → 8.04° |
| 0.80 m / 0.06 m / 2.25× | 16.00 s | 10.12 → 13.23 cm | 12.90 → 7.52° |
| 0.80 m / 0.20 m / 2.25× | 16.00 s | 15.34 → 16.14 cm | 13.32 → 8.09° |
| 0.45 m / 0.00 m / 2.25× | 16.00 s | 0.00 → 0.00 cm | 0.00 → 0.00° |
| 0.45 m / 0.06 m / 1.10× | 0.25 s | 0.92 → 0.70 cm | 19.85 → 11.75° |

All four off-axis, full-duration evaluation cases show reduced peak pitch and worse horizontal RMS. The aligned case has no horizontal excitation under exact symmetry; that does not demonstrate robustness to perturbations. At 1.10× thrust, original and selected rotor runs stop at 0.25 s and 0.39 s respectively, each before accepting a state above the 20° exploratory tilt limit. The table compares only their shared first 0.25 s. It cannot be read as successful low-thrust stabilization. The force-only runs stay horizontally level in these symmetric initial states; full metrics are in the CSV/JSON.

## 6. Verification and limits

Seven automated checks passed: exact previous-stage regression with original gains; full-trajectory step-size convergence; equilibrium dynamics and motor feasibility; tiny-perturbation prediction; eigenvalue sensitivity; training-only selection; common stopping horizons. Halving the integration step changes the default selected position trajectory by at most 1.06 micrometers over 16 s. Largest multiplier magnitudes change by less than 3.1e−9 across the numerical sensitivity checks. These are numerical checks, not wind-tunnel or flight validation.

Physics still uses the published mean far-field hover wake, extrapolated geometry for a 27 g drone, hub-point sampling, and an assumed constant ideal-induced-power rotor response. It omits receiver-velocity inflow, disk averaging, unsteady wakes, reciprocal interaction and detailed motor/propeller aerodynamics. Reaction yaw torque remains proportional to effective thrust; this is not a complete shaft-power model. The 20° cutoff is a software boundary. There is no collision or ground model. Review the earlier source inventory and Step 3A/3B model limitations before interpreting these results physically.

## 7. Conclusion and next step

The research remains worth pursuing as a question about when aerodynamic simplification changes a control/performance conclusion. This small experiment supplies a concrete candidate discrepancy: stable versus unstable predicted hover. It does not establish research novelty, calibrated physics, or achievable swarm throughput by itself.

Next, vary the strength of aerodynamic moment coupling from zero to full strength, explicitly as a diagnostic parameter rather than a physical law. Track how the equilibrium and stability change, then test motor lag separately. This can reveal whether the qualitative discrepancy is robust or depends on aggressive uncalibrated coupling. Measured rotor-force/moment data are still needed before trusting real-flight predictions. Defer the large swarm until that distinction is understood.

## Reproduce

From the workspace root, with Node and macOS Python available:

```sh
node outputs/step03e-source/study.cjs
node outputs/step03e-source/stability.cjs
python3 outputs/step03e-source/eigen.py
node outputs/step03e-source/verify.cjs
```

The browser uses the saved gain choice. `step-03e-study.json` contains the full design, 27 trials and all evaluation metrics. `step-03e-linearization.json` contains Jacobians; `step-03e-stability.json` contains all eigenvalues and roots. `step-03e-comparisons.csv` contains the seven paired configurations. Live browser CSV export includes four alternatives plus no-wake reference over their shared interval.
