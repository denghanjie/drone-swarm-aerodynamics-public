# Step 2C — A known downward force

## Research goal
Before predicting what airflow from another drone will do, verify that our drone responds correctly to a force whose size and timing we already know. This is a mechanics verification milestone in the broader research on aerodynamic model fidelity, swarm throughput and computational cost.

## What to do in the demo
Open `step-02c-force-test.html` through the local server. Press **Reset flight**, then **Play**.

1. Before 4 seconds, both runs hover at 1 m.
2. From 4 to 8 seconds, the solid drone receives a downward push. The pale wireframe is the separately computed unloaded reference. The magenta arrow shows the extra force.
3. After 8 seconds, the force is removed. With default settings, the drone returns to its target.
4. Set **Downward load** to zero: the runs coincide. Restore 20%, then set **Available thrust** to 1.10×: it cannot hold altitude under that load. The grid is only a coordinate reference; this model has no ground contact, so negative altitude is allowed.

The simulation is fully 3D, but this deliberately symmetric test produces only vertical motion. Earlier 3D maneuver demonstrations remain in Step 2B.

## Methodology
Use the same 27 g rigid body, inertia, geometry, controller and 40 ms first-order motor response as Step 2B. Add a constant world-vertical force at the center of mass during the half-open interval [4,8) s. It has no applied torque. Compare with a separate zero-force run, using identical initial conditions and controller settings. Default maximum thrust is 2.25 times weight.

The force magnitude is a selectable fraction L of weight, not an estimate from a wake model:

`F_external = (0, 0, -L m g)` during the pulse, otherwise zero.

The vertical force balance is `m z'' = T - m g - L m g` for this level flight. Before the motors respond, a 20% push therefore produces acceleration `-0.2 g = -1.962 m/s²`.

The unchanged controller requests vertical acceleration `g + 6(1-z) - 4 vz`, with the existing acceleration and actuator limits. It reacts to altitude error and vertical velocity, but has no integral correction or disturbance feedforward. In unsaturated steady flight, `vz = 0` and `T = (1+L)mg`, giving:

`altitude loss = L g / 6`.

For L=0.2, this predicts 0.327 m. This equation applies to a sustained load; the four-second pulse is long enough to approach it closely.

Integration uses RK4 at 5 ms, controller updates at 10 ms. The external force is held constant over each integration interval; 4 s and 8 s are exactly aligned to timestep boundaries, so the pulse is never averaged across a discontinuity. Smaller-step checks use 1.25 ms with the same controller update schedule.

Three.js r180 renders recorded states with WebGL. Physics runs on the CPU. Drone geometry is drawn 6× larger; positions, forces and integration use physical units. This is not a GPU performance test.

## Results

| Quantity | Result |
|---|---:|
| Default applied force | 0.052974 N |
| Predicted steady altitude loss | 0.327000 m |
| Simulated altitude loss at 8 s | 0.326985 m |
| Maximum loss in the default run | 0.329539 m |
| Final altitude at 16 s | 1.00000000043 m |
| Largest altitude difference across timestep checks | 6.70 × 10⁻⁸ m |
| Automated checks passed | 31 |

The small overshoot is a transient effect of the controller and motor dynamics. Numerical digits are reported for reproducibility; they do not imply equivalent real-world accuracy.

With maximum thrust limited to 1.10 times weight and downward load 0.20 times weight, level hover would require more thrust than is available. Once the motors saturate, acceleration is approximately `(1.10 - 1 - 0.20)g = -0.981 m/s²`. The model continues descending after force removal while it brakes. Its minimum altitude is -15.543 m over this 16-second run. This large excursion belongs to an ideal free-space, no-drag, no-ground-contact stress test, not a realistic near-ground flight prediction. Recovery need not finish within the playback interval.

## Verification
Run `node outputs/step02c-source/verify.cjs` from the workspace. Rebuild the browser physics copy after source edits with `node outputs/step02c-source/build.cjs`.

The 31 checks cover F/m in all world axes, an analytic constant-force trajectory, exact zero-load final-state regression against all five Step 2B scenarios, pulse timing, unchanged hover before the pulse, predicted equilibrium, recovery, symmetry, a zero-derivative equilibrium state, eight timestep comparisons, finite states and motor bounds across eight load/thrust combinations, and the expected saturated downward acceleration. Data are in `step-02c-verification.json` and `step-02c-flight.csv`. The CSV includes the unloaded reference altitude.

UI verification used the available Codex computer-use browser API with its Playwright locators (the separate Browser plugin was not listed). On the local URL `http://127.0.0.1:8874/outputs/step-02c-force-test.html`, desktop 1440×1000 and mobile 390×844 layouts were inspected. Page identity, meaningful rendering, absence of error overlays, console health, playback, timeline seeking, load changes, thrust limits and Side camera control passed. The mobile document width equaled the viewport width, with no horizontal overflow. Zero-load explanatory text was corrected after interaction testing. The CSV file generated by verification was checked; the browser download workflow was not re-tested in this step. Other browsers and physical flight remain untested.

## Conclusion and implications
The simulator correctly couples the prescribed external force to the existing rigid-body and controller model in these checks. It is ready to receive a candidate aerodynamic force model. This does not validate airflow physics, prove research novelty, or establish large-swarm scalability.

The result also gives us an experimental design requirement: keep controller settings and thrust limits fixed when comparing aerodynamic models. Otherwise, changes caused by the controller could be mistaken for changes caused by airflow.

## Measurement access and next step
On 2026-10-10, the published dataset DOI resolved successfully but returned a human-verification page at Brown Digital Repository instead of dataset metadata or files. No measurements or license were inspected. No challenge was bypassed.

- Kiran, Ayanian & Breuer, *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, RSS 2025: https://www.roboticsproceedings.org/rss21/p102.html
- Dataset: https://doi.org/10.26300/64d4-wa17
- Repository destination: https://repository.library.brown.edu/studio/item/bdr:rnnfmt6u/

Next, obtain accessible measured force data and document vehicle geometry, separation coordinates, operating conditions, measurement uncertainty and license. Reconcile the paper's reported geometry with our nominal CF2X reference before fitting. Fit a simple candidate model on one subset, then evaluate on held-out separations or conditions. Static offset loads may require moments as well as vertical force. Until those data are available, any two-drone wake demonstration must remain explicitly illustrative and unvalidated.
