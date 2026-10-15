# Temporal force updates: bounded prior-art check

Verified 2026-10-15, 15:08–15:12 UTC, using free primary papers, author/institutional copies and publisher metadata. Five publications below. No experiments, simulations, third-party dataset acquisition or repository changes were performed. “Read” identifies the relevant sections actually inspected, not a reproduction of every result.

**Finding:** two-history-value causal linear extrapolation of expensive forces is explicit prior art. Its application to predicted aerodynamic **inflow**, followed by current-state receiver-force evaluation, needs its own assessment, but the basic predictor cannot support a broad algorithmic novelty claim. The reported improvement on one prescribed pair remains a numerical lead, not evidence of physical accuracy, closed-loop stability or broad superiority.

## Verified publications

### T1 — Direct match for the simple predictor

**Helmut Grubmüller and Paul Tavan (1998). _Multiple Time Step Algorithms for Molecular Dynamics Simulations of Proteins: How Good Are They?_ Journal of Computational Chemistry 19(13), 1534–1552.** [Publisher/DOI](https://doi.org/10.1002/%28SICI%291096-987X%28199810%2919%3A13%3C1534%3A%3AAID-JCC10%3E3.0.CO%3B2-I); [author-institution full text](https://www.mpinat.mpg.de/634333/paper_alg_evaluation.pdf).

Read pp. 1539–1541, Eq. (2), Table I and Fig. 3; pp. 1549–1550 and abstract for scope/results. Evidence anchor: “estimated from previously computed forces” (p. 1539). Distance classes refresh exact forces every n steps; **DC-1b** uses coefficients **a = 1 + i/n, b = −i/n** on the latest and preceding exact values. DC-0 holds the latest value; DC-i applies impulses. They also investigate correction variants intended to reduce artifacts at class transitions.

The test is a simplified protein model, not aerodynamics. DC-1b produces significant distribution artifacts; DC-1d performs better on their selected observables. This defeats a broad “new linear predictor between costly evaluations” claim. It does not establish that DC-1d is suitable for a dissipative controlled UAV. Their preference for statistical observables in protein dynamics is no reason to waive M31's trajectory criterion.

### T2 — Established separation of fast and expensive slow forces

**M. Tuckerman, B. J. Berne and G. J. Martyna (1992). _Reversible multiple time scale molecular dynamics._ Journal of Chemical Physics 97(3), 1990–2001.** [DOI 10.1063/1.463137](https://doi.org/10.1063/1.463137); [author-hosted full text](https://www.columbia.edu/cu/chemistry/groups/berne/papers/jcp_97_1990_1992.pdf); [author publication list](https://wp.nyu.edu/tuckerman_group/publications/).

Read abstract, introduction and §II through the Verlet derivation, pp. 1990–1992. Evidence anchor: “separation of time scales or with long range forces” (abstract). Reversible reference-system propagator algorithms derive multirate integration from Trotter splitting, with a connection to predictor–corrector methods. This is strong prior art for evaluating different force components on different clocks; it is **not** the same as linearly extrapolating a cached inflow vector.

Useful comparison concept: a justified fast/slow force split with a defined integrator, rather than an update schedule alone. Hamiltonian/reversibility arguments do not automatically apply to directed wakes, actuator lag, feedback and drag. The detailed r-RESPA implementation was not audited here, so do not present it as an immediately verified drop-in method or promise its reported molecular speedups for M31.

### T3 — Higher-order multirate methods and embedded estimates

**Emil M. Constantinescu and Adrian Sandu (2013; online 2012). _Extrapolated Multirate Methods for Differential Equations with Multiple Time Scales._ Journal of Scientific Computing 56, 28–44.** [Publisher/DOI 10.1007/s10915-012-9662-z](https://link.springer.com/article/10.1007/s10915-012-9662-z); [author-institution preprint ANL/MCS-P1796-1010](https://www.mcs.anl.gov/papers/P1796.pdf).

Read preprint §§1–4, especially Eqs. (2.1)–(2.3), (3.1)–(3.4) and pp. 5–6; journal identity/year verified against publisher. Evidence anchor: “automatic lower-order embedded methods” (preprint p. 6, immediately before §4).

The method uses **Richardson extrapolation of solutions computed with different step sizes**, with explicit or linearly implicit multirate base schemes and alternative slow-state interpolants. This differs from causal linear extrapolation using two past refreshes. Embedded methods can support error control, but the paper explicitly leaves automatic-controller details outside its study. It examines coupled linear stability and multiscale ODE examples; it is not a drone/wake validation paper. Worth testing later: an embedded estimate for coupled-state error, while charging its additional evaluations to the same work budget. A mere force-history residual is not that estimator.

### D1 — Existing lightweight multi-drone downwash simulation

**Jacopo Panerati, Hehui Zheng, SiQi Zhou, James Xu, Amanda Prorok and Angela P. Schoellig (2021). _Learning to Fly—a Gym Environment with PyBullet Physics for Reinforcement Learning of Multi-agent Quadcopter Control._** [arXiv:2103.02142v3](https://arxiv.org/abs/2103.02142v3); [full text](https://arxiv.org/html/2103.02142v3). The note cites the inspected arXiv version rather than inferring an unverified conference DOI.

Read §§III-C2–3, IV and V-A4; v2 was initially read and the relevant v3 passages then checked. Evidence anchor: “single contribution applied to the center of mass” (§III-C3). The simulator has separate physics/control frequencies and a fitted pairwise downwash force using relative horizontal and vertical separation (Eq. 6). Figure 9 compares two crossing Crazyflies with the data used to identify those parameters; this is not an independent holdout. The authors explicitly identify missed pitch effects.

This is a concrete inexpensive aerodynamic-interaction baseline. Distinguish physics/control rate separation from skipping wake evaluations: the inspected text does not establish causal cached-force extrapolation. Its CPU/renderer timings also do not establish performance for thousands of mutually interacting drones or WebGPU.

### D2 — Adaptive integration and current-state aerodynamic response

**Spencer Folk, James Paulos and Vijay Kumar (2023). _RotorPy: A Python-based Multirotor Simulator with Aerodynamics for Education and Research._** [arXiv:2306.04485v1](https://arxiv.org/abs/2306.04485v1); [full text](https://arxiv.org/html/2306.04485v1); [ICRA 2023 workshop copy](https://imrclab.github.io/workshop-uav-sims-icra2023/papers/RS4UAVs_paper_3.pdf). This is a contributed workshop paper, not an ICRA main-track claim.

Read §§II-A–C/E, III-B and IV. Evidence anchor: “RK45 integrator with variable step size” (§III-B). RotorPy integrates continuous dynamics between discrete controller updates. Aerodynamic force and moment depend on local relative airspeed, attitude and rotor speed; the paper separates parasitic drag, rotor drag and blade flapping, with first-order actuator lag. Its single-Crazyflie circle experiment probes sensor/aerodynamic behavior.

Useful baseline: adaptive integration with fresh model evaluations, and recomputation of the receiver response from current state even when an external wind/inflow estimate is reused. The paper does not establish mutual-wake simulation at swarm scale or savings from stale airflow. Its model coefficients and validation do not transfer automatically to M31.

## Concrete comparisons suggested by this evidence — not performed

1. **Equal-refresh-budget hold versus two-point predictor.** Retain the current all-refresh numerical reference. For actual refresh times t_k, use u_hat(t) = u_k + (t − t_k)(u_k − u_(k−1))/(t_k − t_(k−1)); only actual computed samples enter history. This is the unequal-interval analogue of T1's DC-1b, not a novelty claim. Keep physical integration and controller clocks fixed when comparing the reconstruction choices.
2. **Predict inflow versus predict force.** Recompute the receiver response from current attitude, velocity and actuator state when predicting inflow. Compare that with directly extrapolated force at the same refresh budget. Nonlinear response means the two procedures need not agree; D2 explains why the distinction matters.
3. **Expose temporal artifacts.** Test approaching/receding pairs, turning points, changing source thrust, overlap entry/exit and neighbor-set changes, including long closed-loop runs. Log peak force/moment and trajectory error, predictor jumps and control response, not only mean inflow error. A limiter or reset can be a useful ablation, but no bound has been proved for it here.
4. **A more principled next stage.** If simple prediction remains useful, assess a defined fast/slow integrator or embedded estimate (T2/T3) and count every force/field evaluation. Avoid calling all step-size or interpolation techniques the same “extrapolation” method.

## Unresolved scope and access limits

- Does M31's predicted signal include motion through a spatial wake, source actuation changes and receiver motion consistently? What happens when the refresh interval varies or the neighbor set changes?
- Does the prescribed-pair gain survive closed-loop coupling, changed geometry and convergence checks? No cited work answers that for this implementation. Numerical agreement and physical validation remain separate gates.
- A bounded search did not establish whether the exact combination of inflow-history prediction, this wake law and GPU scheduling has already been published. This is not an exhaustive novelty review. Existing internal spatial wake pruning is also prior project work and should not be described as untried.
- T1's DOI/publisher record and author PDF were accessible; its table was read from extracted PDF text. T2's author PDF initially opened, but later section retrieval and DOI landing returned internal errors; detailed later sections remain unread. T3's public text is a preprint; publisher metadata verifies the 2013 journal publication, not byte-for-byte identity of proofs. Schlick/Barth and Gear/Wells appeared as leads but were not included as verified full-method entries because this bounded pass did not secure the necessary primary text.
