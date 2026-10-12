# Research roadmap — the original eight steps

**Research question:** How much aerodynamic detail is needed to predict a drone flock moving through restricted space, and can the calculation run interactively in a browser?

The original eight steps remain in force. Checkpoints 15–18 are a larger block within Step 5, not a replacement plan. Every checkpoint has a saved Three.js replay, source, protocol, results and a stage summary.

| Original step | Purpose | Status |
|---|---|---|
|1. Define the experiment|Fix the vehicle, task, measurements and references.|Specification and source inventory exist. A suitable independent physical reference is still needed.|
|2. Build one credible drone|Check hover, acceleration, braking, attitude and motor response.|Rigid-body model implemented and numerically checked. Agreement with measured flight remains unestablished.|
|3. Model two-drone interaction|Predict how one wake affects another drone.|Published wake equation implemented and assumed force response explored. Physical validation is open.|
|4. Model several overlapping wakes|Determine whether pairwise interactions can simply be added.|Exploratory comparison exists. An independent multi-wake reference is still needed.|
|5. Test a real local flock|Run about 50 drones through restricted geometry.|Local 3D Boids, multi-obstacle courses and staggered apertures implemented. Checkpoints 15–18 improve passage and diagnose numerical sensitivity, with retained collision and fragmentation failures. A further refinement changes one result from50 to49 finishers. Airflow remains off.|
|6. Accelerate validated calculations|Compare CPU and WebGPU implementations.|Earlier mechanics CPU/GPU agreement is established for tested cases. The current Boids and wake pipeline has not been GPU-verified.|
|7. Scale the actual flock|Test 50→200→1,000→5,000 at controlled density.|Earlier scheduled hybrid benchmark exists; it does not establish scaling for the current local flock or aerodynamic model.|
|8. Evaluate the contribution|Report accuracy, cost, limitations and novelty.|Exploratory software feasibility is supported. Aerodynamic accuracy-versus-cost and scientific novelty remain unresolved.|

## Current research block

- [15 — diagnose steering and filter transitions](milestone-15-report.md): preserve components that fail numerical refinement.
- [16 — test stronger retention](milestone-16-report.md): completing a route does not ensure staying connected or numerical repeatability.
- [17 — compare on new seeds and three courses](milestone-17-report.md): preserve a collision in the retention variant and every refinement failure.
- [18 — steer farther inside the opening](milestone-18-report.md): remove tested stranding cases while measuring the connectivity cost.

[Consolidated explanation](research-block-15-18-summary.md) · [Current 3D viewer](research-results.html) · [Complete history](research-stage-log.md)

## Next research gates

1. Keep the smoother controller and the inward-offset alternative as separate frozen candidates. Test observation delays/errors and limited sensing on matched cases; distinguish passage, contact and connectivity. Do not silently replace local flocking with scheduled traffic.
2. Obtain a physical force/wake reference matched to vehicle geometry and operating conditions. Numerical agreement between two versions of our equations is insufficient.
3. Compare aerodynamic models on fixed missions, including difficult cases, then benchmark the full current Boids and physics loop. Preserve fixed-density and fixed-volume scaling as distinct experiments.
4. Reassess novelty against prior work using the resulting accuracy-versus-cost evidence.

Earlier completion wording has been withdrawn. The project is an ongoing simulation study, with useful numerical evidence and explicit physical-validation gaps.
