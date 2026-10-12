# Research direction assessment — 12 October 2026

The user asked us to consider four screenshots critically. They are suggestions to assess, not instructions to execute verbatim. This record revises the emphasis of the original eight-step programme; it introduces no new experimental result or completed milestone.

## Revised goal

Determine which approximations to mutual aerodynamic interaction allow a physically informed, locally controlled 3D drone flock to run within measured browser compute and memory budgets, and quantify the prediction errors and failure boundaries introduced by those approximations. Investigate scaling toward 5,000 drones through complex environments using WebGPU.

5,000 drones is a target to test, not an already established capability of the coupled browser solver. The application supplies broad common route guidance and each agent retains local Boids rules. Physical fidelity refers to specified observables and operating conditions, rather than an unrestricted claim of “realistic flight.”

## Assessment of the suggestions

|Suggestion|Judgment|Consequence|
|Boids obstacle avoidance alone may have limited paper value.|A reasonable concern for our current work; not a universal judgment about all flock-navigation research.|Treat factory passage as a test workload. A contribution needs a demonstrated methodological or empirical advance over relevant prior work.|
|Include mutual airflow and physical flight control.|Adopt for the central research target.|Retain rigid-body, actuator and controller dynamics; compare coupled interaction models against explicit references. Flow-free runs remain useful controls.|
|Study which compromises preserve useful physics on constrained hardware.|Adopt as the principal experimental question.|Measure error, compute cost, memory, stability and model-domain coverage together. Define acceptable error before evaluating candidates.|
|This necessarily needs enormous computing resources.|Qualify.|Resolved rotor/wake flow can be expensive, but cost depends on fidelity, density, algorithms and hardware. Profile our implementation and compare alternatives instead of assuming an unavoidable cost.|
|WebGPU represents low-compute devices.|Qualify.|WebGPU is an API, available across very different GPUs. State browser, adapter/device, limits and workload for each result; performance on one device cannot establish performance on low-end hardware generally.|
|Finding the right compromise should produce a paper.|A plausible research direction, not a publication guarantee.|Adding airflow, using WebGPU, or producing many simulations is not sufficient evidence of novelty. Show a useful, reproducible advance over matched baselines and review the relevant literature.|
|Try original algorithms as ideas arise.|Adopt as hypothesis-driven development.|Use small development experiments, retain failures, freeze promising variants, then evaluate untouched conditions. Do not invent complexity merely to label something novel.|

## Why this direction fits the evidence

Milestone 29 already measures the complete CPU pipeline with exploratory airflow. Its 5,000-drone force-only model takes a median 297.44 wall seconds for one simulated second, versus 133.94 with airflow off. The repeat spread is large and the window covers startup rather than crowded passages. These observations establish a problem in the present implementation; they do not establish an optimal CPU baseline, a general complexity lower bound, a GPU speedup, or browser feasibility. Higher-moment variants stop early and cannot be credited with completing a cheaper equivalent workload.

Milestone 28 supplies corrected mean-wake coupling experiments but leaves receiver response uncalibrated and shows airflow-update sensitivity. Milestone 31 supplies successful large-flock airflow-off missions with failed trajectory agreement. Milestone 32 supplies visible reconstructed airflow and a bounded inherited-state sensitivity diagnosis. These are useful components of the proposed study, but none yet establishes the desired accuracy-versus-cost result.

The work had increasingly concentrated on controller passage. We should now give aerodynamic model comparison and actual compute cost the central role. Controller diagnosis remains necessary where it undermines trustworthy closed-loop comparisons; it should not grow indefinitely as a substitute for the principal research question.

## What “best compromise” will mean

A candidate is useful when it meets independently justified error and operating-domain requirements while using less compute or memory. There may be several useful choices: a weak GPU and a stronger GPU may justify different models. Report the set of choices for which further savings require a loss of accuracy, rather than declaring one universal winner.

Keep three comparisons separate:

1. **Physical discrepancy:** compare predicted airflow, receiver force and moments against independent measurements matched to vehicle geometry and actuation. A more elaborate simulator is not automatically ground truth. If only published summaries or an unvalidated reference solver are available, limit the claim accordingly.
2. **Approximation and implementation error:** compare cheaper models with a converged reference implementation on the same prescribed states/motions. Compare CPU and WebGPU implementations of the same equations separately, including float precision, update schedules and reduction-order effects. Agreement with an unvalidated model establishes numerical agreement only.
3. **Closed-loop consequences:** run local Boids and flight control with the candidate interaction model. Measure short-horizon response, clearance/contact, tilt, group structure and passage outcomes. Retain long-horizon path discrepancies; do not retroactively replace the failed 1 cm criterion with a forgiving group metric. New aggregate tolerances need their own rationale and frozen evaluation.

Measure actual simulated-time throughput, latency distribution, GPU computation with appropriate synchronization, CPU overhead, memory and end-to-end rendering separately. Include warmup and sustained-run conditions, and report failed or out-of-domain workloads explicitly. Smooth Three.js replay is not a compute benchmark.

## Candidate approximations to investigate

These are development hypotheses, not a frozen test matrix or established novel algorithms:

- **Spatial locality:** accurate nearby contributions with a controlled distant-wake approximation or omission. Separate exact neighbor-search acceleration from physically dropping interactions. Quantify dense and sparse cases, since 5,000 drones at fixed spacing differs from 5,000 in a fixed volume.
- **Temporal updates:** compare fixed refresh rates with a change-triggered policy. The existing airflow-cadence failure makes stale fields a measured risk, not a free speedup. Inspect close approaches and abrupt maneuvers.
- **Receiver resolution:** compare an aggregate force estimate against four-rotor force-and-moment prediction. A scalar model may save work while missing tipping effects; quantify those errors explicitly.
- **Field representation:** investigate direct evaluation versus a lookup/interpolated field where appropriate, with bounded interpolation and domain checks. Compare wake memory or transport only if the chosen prediction requires it and a reference supports evaluation.

Begin with a small set of interpretable comparisons. Change one approximation at a time, shortlist useful candidates, then test combinations. Tune on development conditions; reserve independent physical configurations and fresh simulated seeds/geometries for evaluation. Preserve model failures rather than optimizing only over successful cases.

## Execution order within the original eight steps

1. **Specify the prediction and budgets (step 1):** define physical observables, target device classes, runtime/memory reporting and scientifically justified tolerances. Hardware inspection and a bounded provisional WebGPU feasibility probe may proceed while reference data are pursued. No fixed latency target or acceptance tolerance is invented by this memo.
2. **Prepare trustworthy reference cases (steps 2–4):** measurement-matched one/two/multiple-drone cases, numerical refinement, receiver response and operating-domain checks. Use fixed-motion interactions first to isolate aerodynamic approximation error from controller divergence.
3. **Compare approximation candidates (steps 3–5):** inexpensive development cases followed by a frozen evaluation, with the same controller and environment where the comparison requires them.
4. **Implement and scale promising candidates (steps 6–7):** CPU/WebGPU equation agreement, then end-to-end coupled performance from small flocks toward 5,000. Engineering can advance before physical validation is complete, but validated-fidelity claims must wait for the evidence.
5. **Evaluate the contribution (step 8):** report the accuracy/cost trade-offs and their failure boundaries against relevant existing methods. A new adaptive rule is an option if the evidence motivates it. A rigorous benchmark could also be valuable, subject to a literature comparison and evidence of a useful gap.

Every subsequent experimental milestone keeps the requested visible 3D update, frozen methods where applicable, raw traces, failures, plain-language summary and reproducibility record. This planning revision does not change the current Three.js milestone or its historical findings.

## Expected outcome and decision

The desired result is a defensible map of which models are sufficiently accurate for which conditions and devices, and the largest coupled flock each can support within the chosen budgets. Success at 5,000 drones would be a measured finding. A well-supported lower limit or a demonstrated unsafe approximation is also useful evidence, though its publication value requires assessment.

Proceed with this reframed question. Keep the physical-data gate explicit, allow clearly labeled engineering feasibility work in parallel, and avoid spending the next block solely on obstacle-avoidance tuning. No new novelty search has been performed for this memo; originality and publication readiness remain unestablished.

References to our evidence: [CPU workload measurements](milestone-29-report.md), [corrected airflow study](milestone-28-report.md), [trajectory failures](milestone-31-summary.md), [checkpoint diagnosis and visible airflow](milestone-32-report.md), [physical validation requirements](research-physical-validation-gate-2026-10-12.md).
