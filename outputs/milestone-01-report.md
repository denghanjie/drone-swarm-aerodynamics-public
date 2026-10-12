# Small-scale confidence milestone — research record

## Plain-language finding

We have a numerically checked simulator and a working demonstration with two fixed wake sources and one responding drone. We do **not** yet have a physically validated small-group model.

The instability seen earlier is not eliminated by simply making the modeled motors respond faster. How much turning effect we assign to the airflow matters strongly. Two plausible ways of combining wakes can initially produce very similar lift. Modest changes to starting position reveal sensitivity, including one class of trajectories that does not converge well enough to compare quantitatively. This is useful diagnostic evidence, not proof of real aerodynamic behavior.

The original eight steps remain unchanged; these experiments advance Step 3 and begin an exploratory part of Step 4. They do not replace measured validation or complete those steps' evidence gates.

## Work completed in this milestone

1. Swept the strength of the assumed aerodynamic moment from zero to full strength and solved for steady hover at each setting.
2. Repeated that analysis for both existing gain sets and motor response times of 10, 20, 40 and 80 ms.
3. Ran 24 transient flight cases across moment strength and motor response.
4. Added two fixed wake sources and compared two combination rules across 18 arrangements, first from the nominal initial state and then with the same controlled 1 mm displacement in both models: 36 paired cases, 72 trajectories.
5. Checked regression, force accounting, numerical convergence, equilibrium feasibility, and sensitivity near the stability boundary.
6. Replaced the many controls and technical readouts with one milestone page and three selectable 3D scenes. Prior stages remain available.

## A. What changes when the aerodynamic turning effect is reduced?

At an identical state, keep effective total thrust and nominal motor response unchanged. Interpolate only torque:

`torque = nominal torque + lambda × (effective torque − nominal torque)`

Lambda = 0 reproduces the previous force-only variant; lambda = 1 reproduces the uneven-rotor variant. Intermediate values are a **diagnostic construction**, not a proposed physical law or measured uncertainty distribution. In general they do not correspond to one internally consistent set of four actual rotor forces. This is acceptable for identifying sensitivity but not for asserting real motor behavior.

We hold the default initial geometry (0.45 m gap, 0.06 m offset, thrust limit 2.25× weight) and examine lambda from 0 to 1 in increments of 0.025. Use the two previously defined gain sets without further optimization. Motor time constants of 0.01, 0.02, 0.04 and 0.08 s test response sensitivity; they are hypothetical settings, not measurements of this vehicle.

For each setting, solve for a sampled-system fixed point using the previous solution as an initial guess, falling back to a near-source hover guess when needed. All 328 roots converge, remain unsaturated, and have instantaneous derivative residual below 8.7e−10 in the coordinates' native units. This follows one numerically found equilibrium branch and does not prove uniqueness.

We use the same 16-coordinate quaternion chart, central finite differences and sampled 10 ms control map as Step 3E. Motor dynamics are included in the RK4 integration. Eigenvalues are calculated with macOS Accelerate LAPACK. A largest eigenvalue magnitude below one means locally decaying disturbances; above one means at least one growing disturbance pattern. The result concerns the tested equilibrium, not every initial condition.

| Gains | Motor response | First sampled unstable lambda | Full-strength multiplier |
|---|---:|---:|---:|
| original | 10 ms | 0.150 | 1.020617 |
| original | 20 ms | 0.175 | 1.020297 |
| original | 40 ms | 0.175 | 1.019841 |
| original | 80 ms | 0.225 | 1.020599 |
| selected | 10 ms | 0.100 | 1.018186 |
| selected | 20 ms | 0.100 | 1.017801 |
| selected | 40 ms | 0.100 | 1.017043 |
| selected | 80 ms | 0.100 | 1.015604 |

These are sampled transition brackets, not exact physical thresholds. At the baseline 40 ms response, the first observed transition is between lambda 0.150 and 0.175 for original gains and between 0.075 and 0.100 for selected gains. Classifications on both sides survive halved finite-difference increments and halved integration steps. The selected gains were chosen earlier to reduce a trajectory score, not to maximize stability margin.

At full moment strength the equilibrium is unstable for every tested motor response and both gains. Faster motors therefore do not resolve this particular model's instability. This does not establish that no controller can stabilize it, nor does it separate every individual aerodynamic derivative. Do not extrapolate the lambda boundary into a flight safety rule.

## B. What happens with two wake sources?

This is a three-drone geometry: two upper drones held fixed, one lower drone responding dynamically. It is not a free-flying formation. Fixed sources are treated as independent hover wakes and do not respond to each other or to the receiver.

At each rotor hub, let n denote the nominal still-air-equivalent thrust and f(n,U) the previously assumed constant ideal-induced-power response to downward axial airflow U. We compare:

- **Combine airflow first:** evaluate f(n, U1 + U2).
- **Add separate lift losses:** evaluate max(0, n − [(n − f(n,U1)) + (n − f(n,U2))]).

Both reproduce the one-source model; neither is a calibrated aggregate model. Adding airflow is not the same as solving interacting wakes. Adding force losses can double-count effects and includes a zero-thrust clamp; the clamp is a numerical definition, not a measured saturation law. Both variants retain the existing assumptions about source wake geometry, ideal power, body-axis thrust and yaw torque.

Test gaps: 0.25, 0.45, 0.80 m. Source center spacing: 0.12, 0.24, 0.40 m. Source-pair midpoint offsets: 0 and 0.06 m. Initial receiver position (0,0,1) m, then repeat with x = 0.001 m. Sources lie at (offset ± spacing/2, 0, 1 + gap). Both rules use original gains, 40 ms motors, full moments and the same 16-second horizon. Metrics use the earlier stopping time of the two alternatives. All stops are retained.

A preliminary 0.06 m source-spacing trial was excluded because nominal propeller disks would overlap. No conclusion uses that geometry. The final source spacings avoid source-to-source disk overlap for the nominal level geometry. There is no general collision detection, swept separation guarantee, or aerodynamic model for interactions among the fixed sources.

During inspection, exact symmetry exposed amplification of tiny floating-point asymmetries. We made summation of the two individual losses symmetric in source order and then added the controlled 1 mm displacement test. This was an explicit diagnostic extension after inspecting initial results, not a preregistered confirmatory test. Exact zero displacement in a symmetric configuration is not evidence of robustness.

| Initial receiver X displacement | Paired cases completing 16 s | Largest initial lift difference | Largest horizontal RMS difference among completed pairs |
|---|---:|---:|---:|
| 0 mm | 16 / 18 | 0.2847 percentage points of weight | 0.352 cm |
| 1 mm | 13 / 18 | 0.2846 percentage points of weight | 5.350 cm |

The remaining paired cases encounter the software tilt limit before 16 s. They are not silently dropped from the dataset; the maxima above explicitly refer only to completed pairs. These deterministic configurations provide no statistical confidence interval or population-level success estimate. **The x-only perturbation row is provisional: its largest discrepancy failed the subsequent path-convergence check and must not be interpreted as a reliable aerodynamic model difference.**

The x-only perturbation tests show why a symmetric setup can be misleading. One remaining exactly unperturbed horizontal axis develops roundoff-seeded motion that differs with the integration step. In the gap 0.45 m / spacing 0.12 m / centered-source case, halving the step from 5 to 2.5 ms changes the airflow-sum trajectory by up to 6.35 cm over 16 s. Further steps of 1.25 and 0.625 ms do not bring the complete path comparison within the preselected 0.1 mm target. We retain this failed convergence gate, not an aerodynamic finding.

As a follow-up diagnostic, apply the same explicit initial displacement in **both** horizontal axes (x = 1 mm, y = 0.7 mm) to that case, without changing the controller or physical parameters. Repeat both rules at 5, 2.5, 1.25 and 0.625 ms. The maximum path change is then 1.28 micrometers at the first refinement, falls below 0.08 micrometers at the next, and below 0.005 micrometers at the last. The 5 ms horizontal RMS errors are approximately 12.05 cm and 12.13 cm. Both predict continued motion; this case supports numerical consistency, not experimental correctness.

The two-axis test is one diagnosed configuration, not a rerun of the entire grid and not a license to dismiss every sensitivity as roundoff. The nominal demonstration cases have their own convergence checks. We should use explicit reproducible perturbations in future formation tests rather than relying on exact symmetry or unspecified numerical noise.

## C. What the visual demonstration shows

`milestone-01-small-group.html` replays fixed, reproducible trajectories:

- One neighbor: full turning effect versus its removal.
- Two neighbors: source gap 0.45 m, spacing 0.12 m, midpoint offset 0.06 m; the two combination rules.
- Farther-apart neighbors: source spacing 0.40 m with the same gap and midpoint offset.

These three scenes use the nominal initial state and complete 16 s. Blue vehicles are held wake sources. The solid teal and orange wireframe receivers are alternative model predictions for the same drone, not simultaneous physical vehicles. Grid height is a visual reference, not a floor. Playback samples are saved every 40 ms from the 5 ms CPU physics integration. Three.js uses WebGL; this is not a GPU simulation benchmark.

## D. Verification and remaining limits

The verification file records numerical regression against both previous endpoints, identical-state force accounting, one-source consistency, no-wake hover, source-order invariance, trajectory step refinement, equilibrium residuals, common horizons, controlled displacement refinement, and eigenvalue sensitivity. Nine checks pass; the x-only long-horizon trajectory-convergence gate remains failed and is explicitly recorded. The supporting local-stability conclusions and tested nominal demonstrations survive their numerical checks. None of this validates the rotor-response law.

Physical evidence is still needed for the source length-scale transfer, rotor inflow response, moments and combined wakes. The model omits disk averaging, receiver-motion inflow, unsteady wakes, reciprocal interaction, walls and ground effects. The source wake is extrapolated to the illustrative 27 g configuration. The 20° stopping threshold is an exploratory software boundary, not a flight safety limit. An aggregate method inferred from these assumptions cannot serve as independent ground truth.

No new measured dataset, hardware result, learned aggregate model, novelty claim, GPU benchmark, or passage-throughput result was produced in this milestone. Relevant published sources and prior access limitations remain in the Step 1 inventory and Step 3A model-selection record.

## Decision and next milestone

**The simulation infrastructure is ready for further small-group software experiments. The physical-validation gate is not passed.** We should stop treating gain tuning alone as the solution, and prioritize evidence for the aerodynamic interaction law and aggregation choice before interpreting swarm passage physically.

The next milestone should use independently supported force/moment evidence or a documented experimental aggregate baseline to bound the small-group error. If usable evidence remains unavailable, explicitly narrow the study to model sensitivity and separate a 50-drone navigation demonstration from claims about real aerodynamics. The original Step 5 task remains a virtual gate; physical walls require additional modeling.

## Reproduce

From the workspace root, using the existing Node runtime and macOS Python:

```sh
node outputs/milestone-01-source/diagnose.cjs
python3 outputs/milestone-01-source/eigen.py
node outputs/milestone-01-source/group-study.cjs
node outputs/milestone-01-source/export-demo.cjs
node outputs/milestone-01-source/refinement.cjs
node outputs/milestone-01-source/verify.cjs
python3 outputs/milestone-01-source/check-eigen.py
```

`milestone-01-diagnostics.json` retains all 328 equilibrium cases and eigenvalues. `milestone-01-flights.json` retains the 24 transient diagnostics. `milestone-01-group-study.json` retains all 36 paired group cases. `milestone-01-verification.json` records the checks. The matrices are retained separately for audit. All source files are in `milestone-01-source/` and prior stages are preserved.
