# Literature and claims ledger

15 October 2026. Targeted primary-source review supporting DECISION-MEMO.md. Targeted review, not novelty clearance or a simulator ranking; no downloads or model calls. Evidence root: [checkpoint 5975b71](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/5975b71bec076e5ec498296668479a03a2ad80ba/research).

## 1. Closest numerical prior work

### L1. CHOPtrey
Ben Khaled-El Feki, Duval, Faure, Simon and Ben Gaid. SIMULATION 93(3), 185–200 (2017), DOI 10.1177/0037549716684026. Read [author version v2](https://arxiv.org/html/1610.09261v2), §§4.3, 5.2–5.3, Eqs. (9)–(13), and §7.2.

Exact scope: §4.3 says “one recovers the Lagrange polynomials” for zero weighting and degree-plus-one samples. §5.3 compares the current sample with predictions made in the previous interval, selects weights for the next interval, and uses constant hold when the residual ratio exceeds Γ; 0.7≤Γ<1, with 0.9 illustrated. The published weight set is Ω={0,1/8,1/4,1/2,1,2}. Our restricted quadratic gate omits the full context machinery; label it an adaptation.

Claim boundary: causal polynomial prediction and history-based fallback are established. No drone or hybrid stability guarantee is transferred.

### L2. ECCO
Sadjina, Kyllingstad, Skjong and Pedersen. Engineering with Computers 33(3), 607–620 (2017), DOI [10.1007/s00366-016-0492-8](https://doi.org/10.1007/s00366-016-0492-8). Read [author v2](https://arxiv.org/html/1602.06434v2), §§II.1–II.3, Eqs. (3)–(10), §III.2 Eqs. (13a–b), §III.3.

Conditions: two coupled simulators exchange conjugate flow/effort variables through power ports. Their inconsistent transferred powers define residual energy and motivate non-iterative step control. The present algebraic wake has no matched resolved fluid-energy port. An arbitrary inflow/load residual cannot inherit ECCO's exact power-error identities. Use final issue metadata, rather than conflating the earlier author-version date with publication year.

### L3. MRI-GARK
Adrian Sandu. A Class of Multirate Infinitesimal GARK Methods. SIAM Journal on Numerical Analysis 57(5), 2300–2327 (2019), DOI [10.1137/18M1205492](https://epubs.siam.org/doi/10.1137/18M1205492). Read [author v3](https://arxiv.org/html/1808.02759v3), §2 Definitions 1–2 and 6; this revision is dated 2022, not asserted byte-identical to the 2019 article.

The methods construct modified fast dynamics using slow-stage information for additive or component partitions, with coupling/order conditions. A useful comparator would need an explicit, verified partition such as nominal vehicle dynamics plus aerodynamic correction, not merely replacing an airflow-history callback and calling it MRI-GARK. Controller discontinuities/clamps need separate treatment; smooth-problem order does not automatically transfer.

### L4. Convergence versus stability
[Moshagen, author v1](https://arxiv.org/html/1706.07273v1), Theorem 2.1/Eq. (12), previously verified in the coupling ledger: smooth split-ODE assumptions and exchange error remain distinct from inner-step accuracy and stability. Final publication: DOI 10.1080/13873954.2019.1595667 (2019). No fresh full-paper reread claimed.

## 2. Closest drone-model and simulator comparisons

### L5. Panerati et al., gym-pybullet-drones
Learning to Fly—a Gym Environment with PyBullet Physics for Reinforcement Learning of Multi-agent Quadcopter Control. [Read v3, 25 July 2021](https://arxiv.org/html/2103.02142v3), §§III-C3, IV and V-A4, Eq. (6), Fig. 9.

Eq. (6) supplies an experimentally identified single downwash contribution at the receiver center of mass. In V-A4 the two vehicles follow opposite sinusoidal horizontal paths at 0.5 and 1 m altitudes. The figure comparison uses “experimental data collected to identify the parameters”; it is not an independent holdout. The text acknowledges incomplete capture of pitch and related horizontal-velocity effects. This is direct simulator prior art, with a different output scope; it does not validate our closure.

### L6. Jain et al., velocity-to-rotor-load model
Modeling of aerodynamic disturbances for proximity flight of multirotors. ICUAS 2019, pp. 1261–1269. [Author-lab full paper](https://hiperlab.berkeley.edu/wp-content/uploads/2019/05/Modeling_of_aerodynamic_disturbances_for_proximity_flight_of_multirotors.pdf); [institutional record](https://escholarship.org/uc/item/43q2t9cv). Read §§II-C and IV-B–H, Eqs. (5)–(8), Table I and discussion on PDF page 8.

II-C motivates thrust loss under “constant power consumption”, but actually uses fitted Δf=−b_v v_on ω_p², normal inflow and individual propeller forces/moments. IV-B/C identify velocity-profile and propeller-response coefficients separately. Platforms are 145 g and 650 g. IV-E uses low-speed sweeps; IV-H reports agreement at z={1,1.5,2,2.5} m and poor prediction at 0.5 m. This anticipates the architecture, not our constants, ideal closure or arbitrary aggregation.

### L7. RotorPy
Folk, Paulos and Kumar, [RotorPy v1](https://arxiv.org/html/2306.04485v1), 2023 workshop/preprint. Read §II-A–C, especially Eqs. (7)–(10): parasitic drag, rotor drag, blade-flapping moments and first-order actuator dynamics. The [official repository](https://github.com/spencerfolk/rotorpy), read 15 October 2026, documents CPU/GPU batched simulation. Its workload differs from mutually coupled rotor-resolved wakes. Repository capabilities are dated observations, not independently verified speedups.

### L8. Aerial Gym
[Author v1](https://arxiv.org/html/2503.01471v1), March 2025. Read §III-A–C and §IV/Table I: Isaac Gym-based parallel aerial simulation, configurable drag/motor models, GPU rendering and throughput benchmarking. No inter-vehicle downwash model was established by those sections; no universal absence claim. Relevant to scaling expectations, not aerodynamic truth or comparable numerical rates.

## 3. Physical-model limitations and aggregation

### L9. Bauersfeld et al.
[Read/previously verified v3](https://arxiv.org/html/2403.13321v3), §§III–VI, especially VI-B/Fig. 9. Final RA-L 10(2), 1241–1248 (2025), DOI 10.1109/LRA.2024.3518835. Hover-source mean-jet model; original fitted uncanted vehicles span 230 g–6.3 kg. Radial tails beyond ξ=2 are overpredicted in its measurements. Removing our taper does not therefore imply better physics. Its single-source evidence does not validate arbitrary source sums or the public receiver response.

### L10. Kiran, Ayanian and Breuer
[The Structure of Merging Turbulent Jets Beneath a Small Quadrotor, v1](https://arxiv.org/html/2608.30900v1), 31 August 2026 preprint. Current page and prior §§2–3/Fig. 5 record checked. The public screen uses six encoded centerline symbols from a 32 g platform. Nominal amplitude mismatch is conditional; omnidirectional mean-speed and PIV mean-axial observables differ. Graphical envelopes do not include experimental uncertainty. No journal acceptance or physical calibration is inferred.

### L11. Gielis et al.
[Author v1](https://arxiv.org/html/2312.03488v1), §§2–6, previously verified; final ISER proceedings chapter (2024), DOI 10.1007/978-3-031-63596-0_35. Measured aggregate interactions and set-based models challenge simple pairwise-force summation. That is not algebraically identical to adding velocities before a nonlinear receiver response. Multi-source validation is therefore necessary, not already supplied by our single-source symbol screen.

### L12. Historical error-budget context
The earlier [verified assessment](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/5975b71bec076e5ec498296668479a03a2ad80ba/research/campaign-continuation-20261015/literature/ASSESSMENT.md#closest-verified-primary-work) records Braack/Ern and Farrell-Maupin/Oden. No new attribution or bibliography entry is added here. Current sensitivities are not calibrated physical uncertainty.

## 4. Claim-to-record map

- **Numerical predictor benefit:** CAUSAL-AIRFLOW-PREDICTOR-20261015 summary SHA256 d6312e7420323c70f3ad36bc7e4f4c5df8c698433e499d63d08f4196d9d73767; PREDICTOR-EVENT-STRESS-20261015 summary SHA256 6efb79738c4c05e7eef033cae817ff5da5151ea01bb76d43bb21eb407fcf0d90. Scope: short cases of the same public model, not physical accuracy or measured speedup.
- **Required events absent:** event summary above and wall-replay RESULT SHA256 7d667d68d2fcc7b7d86dcfde873def39f29336b5dacf91f4924f48b2d4c88402. Wall replay concerns 50 saved J32 pre-control states only. Event decision remains unchanged.
- **Prior qualification stopped:** summary SHA256 f5cd17150fc487220d95b5a601857758f5c5c9cc04053a45ea94685a025f3e36. Air64 angular-rate cap failed; cadence reduction passed. No retroactive rescue.
- **Conditional empirical discrepancy:** EPOCH2-RESULT SHA256 eaf189fa69b2b74913c741e6ac58c8e373956d034898807cd803c7f9e702c1fe. Six points, no fit; unknown physical/observable errors. Earlier shape-only ratios removed a common amplitude and cannot settle this result.
- **Formal support behavior:** PUBLIC-SUPPORT-FACTORIAL-20261015 and CORE-EXTENT-CERTIFICATE-20261015 saved reports. The 1.9686%-of-weight change and 90.27–92.73% formal omissions have different denominators and references. Neither measures physical error.
- **Retention defect:** event results/RETENTION-ERRATUM.md, SHA256 9355aa4879e0f4ab6663eb46b8489cd1135c2a0d304c0cbf9a4a7b8a6cbcfd6a. Unused failure schema unqualified; successful native JSON preserved. Correction is a future prerequisite, not a retrospective source edit.

The memo specifies prospective falsification and stopping rules. The operator fixture cannot qualify own-state flock behavior. Search coverage is bounded; no absence-of-hits novelty inference is made.

Roadmap: checkpoint-verified eight steps; direct web fetch cache-missed. [Full bibliography](references.bib) records version, metadata corrections and access limits; no exhaustive erratum search.
