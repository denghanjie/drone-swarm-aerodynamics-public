# Step 1 — Experiment specification

Version 0.1 · 10 October 2026 · Planning decisions, not experimental results

## Our question

How much aerodynamic detail is needed to predict a drone swarm's passage through a bottleneck, and can that detail run interactively in a browser?

We will measure three things together: physical prediction error, passage performance, and computation time. The candidate contribution is an experimentally supported accuracy–cost comparison, potentially followed by an improved approximation. Novelty is provisional until the exact method and findings are compared with prior work.

## Selected starting point

Use the Crazyflie CF2X reference configuration from gym-pybullet-drones for initial implementation verification. Its parameter file specifies a 0.027 kg mass, 0.0397 m arm parameter, and inertia diagonal (1.4e-5, 1.4e-5, 2.17e-5) kg m². These are source-model parameters, not newly measured values. Source: [CF2X parameter file](https://github.com/learnsyslab/gym-pybullet-drones/blob/main/gym_pybullet_drones/assets/cf2x.urdf).

Keep published experimental configurations separate. Before using a dataset to validate this model, reconcile geometry, propellers, motor operating points, payload, coordinate conventions, and normalization. Sharing the name “Crazyflie” does not establish equivalence. Pin the source commit and preserve its license when importing code.

Initial test machine: hardware identity withheld in this public export. Browser version, OS version, WebGPU adapter, resolution, and power/thermal conditions will be recorded when benchmarking begins. WebGPU capability and performance have not yet been tested. Target: Three.js visualization and WebGPU computation, total sustained frame time at or below 30 ms, with 20 ms as a stretch target. Report median and 95th-percentile times plus simulated-time/wall-time ratio.

## First task, in plain language

Fifty identical drones start on one side of a virtual rectangular gate and move to a destination beyond it. The gate is a navigation constraint in free air; it is not a physical wall. This isolates crowding and drone-to-drone interaction. A later solid-wall experiment requires separate treatment of surface-related airflow or explicit qualification as an idealized geometry study.

Proposed pilot values, subject to revision before confirmatory experiments:

- Start with 1 drone, then 2, then a small formation; use 50 only after those checks.
- For the 50-drone task, sweep gate widths of 0.6, 1.2, and 2.4 m; gate height 1.2 m.
- Initial center spacings: 0.3 and 0.6 m; commanded speeds: 0.25 and 0.5 m/s; initial tilt cap: 15 degrees.
- These are test settings, not validated physical limits. Exclude or label any state outside the eventual model's measured domain.
- Still ambient air; no floor, ceiling, or wall aerodynamic effects. Use a shared gate/goal direction plus local flocking and avoidance rules. Hold navigation and controller parameters fixed across the first aerodynamic comparison.
- Ten reproducible seeds per pilot condition; separate pilot seeds from final evaluation seeds. Record every timeout and failure. Pilot horizon: 60 simulated seconds.

## What we compare

1. Vehicle dynamics without inter-drone aerodynamic disturbances.
2. The same dynamics with pairwise downwash, adding individual neighbor effects.
3. A richer aggregate model only if its data, scope, and implementation can be supported.

Do not label model 3 “ground truth” merely because it is more complex. First compare predictions with independent physical evidence. For offset configurations, assess disturbance moments as well as forces before adopting a force-only approximation. Avoid double-counting an empirical thrust-loss effect as both reduced thrust and a second external force.

## Measurements and decision rules

| Quantity | Definition |
|---|---|
| Completion | Fraction of drones reaching the destination beyond the gate within the horizon; each counted once. |
| Throughput | Unique successful gate crossings divided by the full fixed observation duration; also plot cumulative crossings over time. |
| Contact and gate violations | Count distinct contact events and invalid crossings; use swept collision checks or demonstrate timestep adequacy. |
| Tracking error | Distance between the commanded trajectory/setpoint and actual position; retain time traces and summarize RMS and peak. |
| Saturation | Fraction of simulated time each drone spends at a motor command limit. |
| Physical model error | Force/moment prediction error on withheld configurations; report units, bias, RMSE, and a tail error alongside experimental uncertainty. |
| Computation | Physics, neighbor search, rendering, and total frame costs on the named device. |

Use paired seeds for model comparisons and uncertainty intervals across runs. Preserve failed runs. Do not treat thousands of correlated samples from a single trajectory as thousands of independent experiments. Choose final sample counts using pilot variability and freeze settings before final evaluation.

Numerical checks: start with a 5 ms physics timestep and compare with 2.5 ms and, if necessary, 1.25 ms. This is a trial schedule, not an established adequate rate. A provisional engineering target is less than 2% change in continuous summary metrics, accompanied by absolute errors and inspection of changes in collision/completion outcomes. GPU/reference differences and interaction-cutoff effects must be smaller than the scientific effects we interpret. Physical accuracy thresholds remain pending measurement uncertainty and controller thrust/clearance margins; numerical convergence does not establish physical validity.

## Expected outputs and allowed conclusions

Outputs: validation plots, passage-performance curves, accuracy–cost curves, reproducible configurations, and an interactive demonstration. No beneficial aerodynamic effect or performance improvement is assumed in advance.

Possible conclusion: a simple model suffices in some tested conditions; richer interactions matter in others; or current uncertainty prevents reliable passage predictions. Any conclusion must name the tested vehicle, operating range, and limitations. A 5,000-agent simulation demonstrates computational scale, not real-world validation at that scale. Increase total count at fixed density separately from increasing local crowding.

## Current status and next step

Specification and baseline selection complete. Experimental data acquisition, reuse terms, configuration matching, and independent flight-response evidence remain unresolved. The full physical-validation gate has therefore not passed.

Step 2 can begin as implementation verification: one drone hovering, accelerating, braking, and obeying thrust limits. Its first result will be a transparent mechanics demonstration, not a physically validated digital replica. In parallel, resolve data access before making Step 3 validation claims. No hardware purchase or author contact has been made.

See [source and data inventory](step-01-source-inventory.md) for evidence and access status.
