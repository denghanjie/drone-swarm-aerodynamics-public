# Research roadmap — the original eight steps

The research question remains: **How much aerodynamic detail is needed to predict swarm passage, and can that detail run interactively in a browser?**

Every milestone includes an updated, viewable Three.js simulation and a short plain-language summary. We now report larger milestones. Intermediate experiments stay in the supporting files; they do not add new numbered steps to this plan.

| Original step | Purpose | Current status |
|---|---|---|
| 1. Define exactly what we are testing | Fix the vehicle, task, measurements and sources. | Specification written. Access to suitable physical validation data remains unresolved. |
| 2. Make one drone behave credibly | Implement and check hover, acceleration, braking and turning. | 3D mechanics implemented and numerically verified. Measured-flight agreement is not established. |
| 3. Reproduce the interaction between two drones | Compare forces and response across separations. | Published wake equation implemented; assumed rotor response investigated. Physical validation remains open. |
| 4. Test whether several wakes can simply be added | Compare pairwise and aggregate interaction models. | Exploratory two-source comparison implemented. A measured or independently validated aggregate reference is still needed. |
| 5. Run the first swarm passage experiment | Compare about 50 drones through a virtual opening. | Centralized navigation baseline and uncertainty comparison completed; this was not Boids. Planar Boids added in milestone10; volumetric open-space coordination established in milestone11 under modeled conditions. Narrow-gate behavior and earlier passage time-step sensitivity remain unresolved. Extra-clearance candidate avoided measured failures in 60 new-seed cases, with lower throughput. Aerodynamic passage accuracy and real-flight safety remain unestablished. |
| 6. Make the validated calculations run efficiently on WebGPU | Accelerate and compare against the reference. | Rigid-body CPU/WGSL numerical agreement established for the tested cases. Boids remains on CPU and has not been GPU-verified. Only mechanics is on GPU; physically validated wake computation remains open. |
| 7. Scale up and identify the limits | Test 50 → 200 → 1,000 → 5,000 at controlled density. | Short fixed-density centralized-scheduler computational study completed; it does not establish Boids scaling. Hybrid loop is faster than simulated time at 1,000 and slower at 5,000 on the tested machine; no dense/long-mission/airflow scaling claim. |
| 8. Draw conclusions and assess the contribution | Establish supported findings, limitations and novelty. | Earlier completion framing withdrawn; corrected exploratory assessment ongoing. Software approach feasible; original aerodynamic accuracy question unresolved and scientific novelty not established. See final report and stage record. |

## How the milestone reviews work

- **Small-scale confidence:** finish interaction diagnosis and decide what physical claims the evidence permits. The current milestone completes a substantial diagnostic package, not the physical-validation gate.
- **Swarm passage:** complete controlled navigation comparisons and explain whether the aerodynamic choice changes the result.
- **Browser scaling:** establish measured CPU/GPU agreement and performance limits.
- **Research conclusion:** assemble the accuracy–cost findings and reassess the exact contribution against prior work.

The project can continue as an exploratory simulation study while physical evidence is unresolved. We must label such results as model sensitivity, rather than reliable predictions of real swarm performance. We will not silently treat numerical verification as physical validation or mark all of Steps 3–4 complete.

Current deliverable: [current research dashboard](research-results.html), [corrected feasibility report](research-final-report.md), and [milestone trace](research-stage-log.md). All previous milestone reports and 3D pages remain available through the trace.

The original research is ongoing. [Milestone 10](milestone-10-report.md) corrects the missing Boids controller and retains its failures. Next: resolve numerical sensitivity and narrow-gate local steering, then validate airflow and test actual Boids scaling.

Current behavioral baseline: [Milestone 11 — volumetric flocking](milestone-11-report.md). Next: obstacles/passages while preserving emergent 3D coordination. Physical-validation gates remain open.

Milestone12 adds sphere and square-aperture experiments. Easy scenarios pass in both controls; narrow congestion and numerical sensitivity remain unresolved. Next gate: diagnose narrow-case convergence and sustained clearance before adding airflow. [Evidence](milestone-12-report.md).

Milestone13 adds sequential 3D geometry. Tight-course wall failures show the current blend of social and map steering is insufficient. Next: diagnose wall contacts and test local clearance-prioritized steering against frozen and new-seed cases. [Evidence](milestone-13-report.md).

Milestone14 tests obstacle-only and combined local-clearance constraints. Obstacle-only fails; combined filtering remains provisional due to fragmentation, slower passage and tight-case numerical sensitivity. Next: diagnose constraint switching and convergence before further complexity or airflow claims. [Evidence](milestone-14-report.md).
