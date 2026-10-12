Latest update: [Milestone12](milestone-12-report.md) tests volumetric obstacle passage. Sphere/wide cases succeed with both controllers; narrow cases remain unresolved and numerically sensitive. Research remains ongoing.

Current update: [Milestone 11](milestone-11-report.md) demonstrates local volumetric coordination against separation-only controls. This supersedes the planar behavioral baseline, but does not establish physical validation, aerodynamic accuracy, novelty or completed passage research.

# Corrected research status — ongoing

The earlier completion framing is withdrawn. Passage milestones used centralized scheduling, and GPU measurements covered mechanics or a scheduled hybrid loop. They did not establish Boids flocking or Boids scaling. Actual local Boids is now implemented and tested in [milestone 10](milestone-10-report.md). Narrow-gate failures and a failed convergence check remain; physical accuracy and scientific novelty remain unestablished.

The following assessment is retained as historical baseline context, subject to this correction. Its feasibility conclusion does not close the original goal. The unmodified version is [archived](archive-before-boids/research-final-report.md).

---

# Drone-swarm research — final feasibility assessment

## Decision

**The software concept is achievable and worth pursuing as a focused research project. This work does not yet support a claim of a physically validated, novel, large-scale turbulent drone-swarm simulator.**

We have reached a defensible conclusion for this feasibility pass. The original question—how much aerodynamic detail is needed to predict swarm passage—remains unanswered because we have not established a matched physical reference for the interaction models. Faster calculations and successful navigation tests cannot fill that evidence gap.

## Research goal

Determine what physical detail is necessary to predict collective drone passage, and whether the resulting model can run interactively in a browser. The original eight-step plan narrows the first task to a virtual opening. It does not yet implement arbitrary terrain or a freely navigating, dense volumetric swarm.

## Methodology

Separate three kinds of evidence:

1. **Mechanics and numerical checks:** integrate position, velocity, attitude, angular velocity and motor thrust, and check numerical consistency and CPU/GPU agreement.
2. **Navigation experiments:** run 50 vehicles through a virtual opening under fixed controls and reproducible initial conditions; measure valid passages, invalid crossings, spacing breaches and contact-envelope stops. Retain unsuccessful cases.
3. **Computational scaling:** measure isolated mechanics, then the fuller control/mechanics/transfer/checking loop at 50, 200, 1,000 and 5,000 vehicles, holding queue spacing fixed. Measure rendering separately.

Published aerodynamic models and experiments were reviewed independently of those navigation tests. The principal swarm runs keep airflow off because a matching wake-to-force and multi-wake validation was not established. Every claim is tied to a stage report and raw record.

## Results in plain language

**Order matters.** Letting drones converge without adequate scheduling produced failures in the earlier pilot. Scheduling groups improved the outcome, and reducing unnecessary pauses improved passage under ideal information.

**Uncertainty consumes clearance.** Fixed position errors and stale observations exposed failures. A candidate with wider clearance and slower group handling avoided measured failures in all 60 new-seed cases. Under the stronger error profile it passed 514 drones across 30 runs, compared with 786 for the faster rule: a 34.6% reduction. The faster rule had invalid crossings in 14/30 runs, spacing breaches in 5/30 and one contact stop. This is a finite-model trade-off, not proof of safety or optimality. [Milestone 7](milestone-07-report.md)

**WebGPU can execute these mechanics accurately relative to our CPU code.** Across the tested 0.5-second fixed-command batches, the largest position-component discrepancy was about 0.0106 mm at 5,000 bodies. This is agreement between two implementations of the same equations, not micrometer physical accuracy. [Milestone 8](milestone-08-report.md)

**The rest of the loop becomes the bottleneck.** For one simulated second, the GPU-assisted full computation took a median of about 54 ms at 50 vehicles, 86 ms at 200, 284 ms at 1,000 and 1,335 ms at 5,000. CPU-only was faster for the smallest case. These measurements exclude rendering and deliberate UI yields; they do not certify an integrated live frame rate. Most vehicles were waiting in a long queue, so this is not a demonstration of 5,000 drones clearing obstacles. [Milestone 9](milestone-09-report.md)

## Physics: what has and has not been validated

The implemented rigid-body structure is physically motivated: gravity, thrust, moments, inertia, attitude kinematics and motor lag. Its parameters and control laws have not been identified against matched measured flight data. Geometric contact envelopes and virtual gate crossings are measurement conventions; collision and wall-impact dynamics are absent.

Published work supplies useful constraints, but a mean airflow field does not automatically specify the force and moment on another operating rotor. Kiran, Ayanian and Breuer measure force, moment and flow under explicitly controlled motor conditions; these are the kinds of measurements a matching validation needs. Public DOI metadata resolved the dataset to Brown’s repository, but the web tool could not retrieve it and an ordinary HTTPS request returned HTTP 403. Raw measurements and reuse terms were not established. The [access record](physical-data-access-record.json) preserves the resolved URL and outcomes. We did not replace missing samples with invented data or interpret a textual range as a complete validation set. [Primary paper](https://arxiv.org/html/2507.09463v1) · [Dataset DOI](https://doi.org/10.26300/64d4-wa17)

Bauersfeld and colleagues characterize induced airflow as a turbulent jet, while Gielis and colleagues investigate aggregate downwash forces. They support treating geometry, force response and aggregation as distinct questions. They do not validate our transferred 27 g model merely by being cited. Earlier discrepancies and a singular reference expression remain recorded. [Airflow paper](https://arxiv.org/html/2403.13321v3) · [Aggregate-force paper](https://arxiv.org/html/2312.03488v1) · [Our audit](milestone-02-evidence.md)

## Novelty assessment

The initial pasted conversation asserted that no exact combination existed. We cannot substantiate that absence claim. A focused review found substantial overlap:

- **DroneMD** publicly describes GPU drone physics, Boids motion and Three.js visualization. Its architecture uses a backend rather than proving that all computation happens in browser WebGPU. Its README performance and accuracy claims were not independently reproduced here. [Repository](https://github.com/atvm/droneMD)
- **Crazyflow** is an existing GPU-accelerated drone simulator with reported physical experiments and large parallel workloads. Many independent worlds must not be equated to one densely interacting swarm. [Primary paper, v2](https://arxiv.org/abs/2606.01478v2)
- **DOP SIM** already combines data-oriented quadrotor simulation and downwash support. [Repository](https://github.com/Li-Jinjie/dop_sim)
- **Neural-Swarm2** already studies learned aerodynamic interactions for multirotor planning and control. [Primary paper](https://arxiv.org/abs/2012.05457)

This is a focused review, not an exhaustive novelty search. Browser deployment, adding Boids, or combining existing models is not enough by itself to claim a new scientific result. A plausible contribution would be a measured accuracy-versus-cost result for a well-defined interaction approximation, or a demonstrably improved uncertainty-aware passage method compared with strong existing baselines. Neither contribution has yet been established here.

## Implications and next decision

The useful outcome is a reproducible experimental foundation and a clearer boundary around what is known. We can now identify failures, compare changes on unseen seeds and measure browser computation without relying on attractive animation as evidence.

Before investing in more elaborate airflow or terrain graphics, the highest-value next input is a matched physical dataset: vehicle geometry, motor operating conditions, forces/moments, relative positions, uncertainty and held-out configurations. Reconcile the geometry and rotor response, validate pairwise cases, then validate multi-source interactions before returning to the same passage experiment. If physical data cannot be obtained, frame the project as a conditional simulation/engineering study and state that limitation in its title and claims.

A separate engineering continuation could keep state, control and neighbor search resident on WebGPU, then test long, genuinely active missions. The present results establish neither that optimization’s performance nor 5,000-drone real-time turbulent navigation.

## Preserved records

[Milestone index and change trace](research-stage-log.md) · [Original eight-step status](research-roadmap.md) · [Interactive 3D dashboard](research-results.html) · [Source/evidence list](final-related-work.json) · [File integrity manifest](research-manifest.json) · [Verification and isolated reproduction helper](research-reproduce.py)
