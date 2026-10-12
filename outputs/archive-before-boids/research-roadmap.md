# Research roadmap — the original eight steps

The research question remains: **How much aerodynamic detail is needed to predict swarm passage, and can that detail run interactively in a browser?**

Every milestone includes an updated, viewable Three.js simulation and a short plain-language summary. We now report larger milestones. Intermediate experiments stay in the supporting files; they do not add new numbered steps to this plan.

| Original step | Purpose | Current status |
|---|---|---|
| 1. Define exactly what we are testing | Fix the vehicle, task, measurements and sources. | Specification written. Access to suitable physical validation data remains unresolved. |
| 2. Make one drone behave credibly | Implement and check hover, acceleration, braking and turning. | 3D mechanics implemented and numerically verified. Measured-flight agreement is not established. |
| 3. Reproduce the interaction between two drones | Compare forces and response across separations. | Published wake equation implemented; assumed rotor response investigated. Physical validation remains open. |
| 4. Test whether several wakes can simply be added | Compare pairwise and aggregate interaction models. | Exploratory two-source comparison implemented. A measured or independently validated aggregate reference is still needed. |
| 5. Run the first swarm passage experiment | Compare about 50 drones through a virtual opening. | Navigation baseline and uncertainty comparison completed. Extra-clearance candidate avoided measured failures in 60 new-seed cases, with lower throughput. Aerodynamic passage accuracy and real-flight safety remain unestablished. |
| 6. Make the validated calculations run efficiently on WebGPU | Accelerate and compare against the reference. | Rigid-body CPU/WGSL numerical agreement established for the tested cases. Only mechanics is on GPU; physically validated wake computation remains open. |
| 7. Scale up and identify the limits | Test 50 → 200 → 1,000 → 5,000 at controlled density. | Short fixed-density computational study completed. Hybrid loop is faster than simulated time at 1,000 and slower at 5,000 on the tested machine; no dense/long-mission/airflow scaling claim. |
| 8. Draw conclusions and assess the contribution | Establish supported findings, limitations and novelty. | Feasibility synthesis completed. Software approach feasible; original aerodynamic accuracy question unresolved and scientific novelty not established. See final report and stage record. |

## How the milestone reviews work

- **Small-scale confidence:** finish interaction diagnosis and decide what physical claims the evidence permits. The current milestone completes a substantial diagnostic package, not the physical-validation gate.
- **Swarm passage:** complete controlled navigation comparisons and explain whether the aerodynamic choice changes the result.
- **Browser scaling:** establish measured CPU/GPU agreement and performance limits.
- **Research conclusion:** assemble the accuracy–cost findings and reassess the exact contribution against prior work.

The project can continue as an exploratory simulation study while physical evidence is unresolved. We must label such results as model sensitivity, rather than reliable predictions of real swarm performance. We will not silently treat numerical verification as physical validation or mark all of Steps 3–4 complete.

Current deliverable: [final research dashboard](research-results.html), [final feasibility report](research-final-report.md), and [milestone trace](research-stage-log.md). All previous milestone reports and 3D pages remain available through the trace.

The feasibility pass is concluded; this is not a claim that the physical-validation gates in Steps 3–4 have been passed. The final record identifies the external evidence and further experiments needed to answer the original accuracy–cost question.
