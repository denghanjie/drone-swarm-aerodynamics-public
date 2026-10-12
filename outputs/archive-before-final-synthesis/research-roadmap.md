# Research roadmap — the original eight steps

**Research question:** How much aerodynamic detail is needed to predict a drone flock moving through restricted space, and can the calculation run interactively in a browser?

The original eight steps remain in force. The active complex-environment goal extends Steps 5–8; milestones 24–25 establish the factory benchmark and short-window actual-flock scaling. Every checkpoint has a saved Three.js replay, source, protocol, results and a stage summary.

| Original step | Purpose | Status |
|---|---|---|
|1. Define the experiment|Fix the vehicle, task, measurements and references.|Specification and source inventory exist. A suitable independent physical reference is still needed.|
|2. Build one credible drone|Check hover, acceleration, braking, attitude and motor response.|Rigid-body model implemented and numerically checked. Agreement with measured flight remains unestablished.|
|3. Model two-drone interaction|Predict how one wake affects another drone.|Published wake equation implemented and assumed force response explored. Physical validation is open.|
|4. Model several overlapping wakes|Determine whether pairwise interactions can simply be added.|Exploratory comparison exists. An independent multi-wake reference is still needed.|
|5. Test a real local flock|Run local flocks through increasingly complex geometry.|Local 3D Boids, multi-obstacle courses and a 34-solid factory with 50/200-drone trials exist. Soft filters remain rejected. Local position prediction recovers some delayed-observation failures and introduces others; a numerical counterexample is retained. Reliable passage and connectivity remain unresolved. Airflow is off.|
|6. Accelerate validated calculations|Compare CPU and WebGPU implementations.|Earlier mechanics CPU/GPU agreement is established for tested cases. The current Boids and wake pipeline has not been GPU-verified.|
|7. Scale the actual flock|Test 50→200→1, 000→5, 000 at controlled density.|Factory trials now cover 50/200 genuine local Boids. Serial two-second actual-flock timing now reaches 1,000/5,000; full larger-count missions remain open; the earlier scheduled hybrid benchmark is not evidence for this pipeline.|
|8. Evaluate the contribution|Report accuracy, cost, limitations and novelty.|Exploratory software feasibility is supported. Aerodynamic accuracy-versus-cost and scientific novelty remain unresolved.|

## Current research block

**Running:** [26 full missions](milestone-26-report.md) and [28 corrected paired airflow study](milestone-28-report.md). [27](milestone-27-report.md) is a terminated normalization-error record with20 completed cases and five uncompleted refinements; [29 isolated cost protocol](milestone-29-protocol.json) is prepared but not run. Final outcomes remain pending. [Correction audit](research-wake-normalization-correction.md).


- [25 — scaling and audit](milestone-25-report.md): actual flock computation through 5,000, separate replay rendering measurements and a passing finer 200-drone comparison. [3D viewer](milestone-25-lab.html).

- [Active goal](research-complex-environment-goal.md): complex environments, actual flock scaling, aerodynamic comparisons and physical validation.
- [24 — factory benchmark](milestone-24-report.md): 34 solids, three offset doorways, 50/200 genuine local drones, matched social-rule ablations and numerical refinements. [3D replay](milestone-24-lab.html).

- [22 — local prediction](milestone-22-report.md): recovery, a200ms counterexample and a retained trajectory-refinement failure.
- [23 — fresh flocks](milestone-23-report.md): six new seeds in two courses, with the controller frozen before testing. Prediction helps some cases and hurts others.

[Consolidated explanation](research-block-22-23-summary.md) · [Current3D viewer](research-results.html) · [Prior block19–21](research-block-19-21-summary.md) · [Complete history](research-stage-log.md)

## Next research gates

1. Keep raw observations and local prediction as separate experimental baselines, with all counterexamples retained. Do not promote prediction as a universal fix. Navigation work remains within Step5; completion, contact and connectivity require separate reporting.
2. Continue the [physical measurement gate](research-physical-validation-gate-2026-10-12.md): obtain a force/wake reference matched to vehicle geometry, measurement plane and motor operating conditions. The data repository currently returns human verification; its observations have not been acquired. Numerical agreement between two versions of our equations is insufficient.
3. The finer 200-drone comparison passed at 1.016 mm, while the original failure remains. Serial early-window timing through 5,000 is complete. Next execute full larger-count missions with bounded recording and numerical sensitivity checks. Distinguish short timing windows from completed missions. Then compare aerodynamic approximations on fixed missions. Data access does not block this software benchmark. Preserve fixed-density and fixed-volume scaling as distinct experiments.
4. Reassess novelty against prior work using the resulting accuracy-versus-cost evidence.

Earlier completion wording has been withdrawn. The project is an ongoing simulation study, with useful numerical evidence and explicit physical-validation gaps.
