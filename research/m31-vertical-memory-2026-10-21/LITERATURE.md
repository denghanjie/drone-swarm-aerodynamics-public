# Retained literature and claim scope

21 October 2026. No new research acquisition or external browsing was performed for this checkpoint. The citations below were inspected previously and are reused within their documented reading limits. This is not a new or exhaustive novelty search.

The authoritative retained records are [sources.bib](../m31-restart-2026-10-15/literature/sources.bib), [annotated-ledger.md](../m31-restart-2026-10-15/literature/annotated-ledger.md) and [source-access-log.md](../m31-restart-2026-10-15/literature/source-access-log.md). Their verification date is 15 October 2026; it must not be relabeled as a fresh external verification on 21 October.

## Relevant verified antecedents

**Bauersfeld, Leonard; Muller, Koen; Ziegler, Dominic; Coletti, Filippo; Scaramuzza, Davide. _Robotics meets Fluid Dynamics: A Characterization of the Induced Airflow below a Quadrotor as a Turbulent Jet_. arXiv:2403.13321v3, 12 December 2024.** [Version read](https://arxiv.org/abs/2403.13321v3). Local key `bauersfeld2024jetv3`.

- The retained verification read relevant normalization, vehicle-domain, far-field and control sections, including III-D, IV, VI, VII and VIII. Section VII's compensation example converts modeled inflow into additional power through vehicle-specific throttle behavior.
- This establishes that lightweight wake modeling and downwash compensation have antecedents. It does not establish the proposed integral tracking law, its gain, anti-windup rule, stability, or effectiveness in this N64 model.
- The version read is an accepted RA-L manuscript; the authors' laboratory lists journal publication in 2025. The journal DOI page could not be independently checked, so no unverified journal DOI is added here. The source's smallest measured vehicle is 230 g; our 27 g model and moving coupled paths are not validated by that paper.
- Verification support: A2 in the [annotated ledger](../m31-restart-2026-10-15/literature/annotated-ledger.md), A2 rows in the [access log](../m31-restart-2026-10-15/literature/source-access-log.md), and the earlier local [model-selection discussion](../../outputs/step-03a-model-selection.md). The latter is implementation history, not an independent external source.

**Shi, Guanya; Hönig, Wolfgang; Shi, Xichen; Yue, Yisong; Chung, Soon-Jo. _Neural-Swarm2: Planning and Control of Heterogeneous Multirotor Swarms Using Learned Interactions_. IEEE Transactions on Robotics 38(2), 1063–1079, 2022. DOI 10.1109/TRO.2021.3098436.** [Verified institutional record](https://authors.library.caltech.edu/records/psxc9-vps89). Local key `shi2022neuralswarm2`; relevant full text read in [arXiv:2012.05457v2](https://arxiv.org/abs/2012.05457v2).

- The retained verification read III-A/B, IV-A, VI-A/B and VII-B, and checked journal metadata. Online publication is 2021; the journal volume is 2022.
- Relevant antecedent: nominal rigid-body and actuator-delay dynamics combined with learned interactions for planning/control. Although the general equations include torque, the reported implementation learns vertical residual force.
- It is contextual support for interaction-aware control, not verification of our source-total aerodynamic law, rotor/moment response, local Boids policy or proposed vertical-memory correction. The stability assumptions and bounded model errors must not be presented as measured guarantees for this implementation. Its proofs and every flight result were not audited; code and training were not reproduced.
- Verification support: A4 in the [annotated ledger](../m31-restart-2026-10-15/literature/annotated-ledger.md) and A4 rows in the [access log](../m31-restart-2026-10-15/literature/source-access-log.md).

## What these references do not establish

No specifically verified PI/integral-control or anti-windup source was identified in the inspected retained records. This is a bounded absence finding, not a claim that the methods lack published antecedents. Do not attribute a proposed accumulator equation, chosen gain, saturation policy or guarantee to either paper without appropriate source support. The candidate is a computational intervention using an established control idea, not a reproduction of a cited controller or a novel integral method.

The planned scope is one already exposed failing N64 seed, 2026102001, at h = 0.005 and 0.0025 s, through at most five seconds. Selecting it after observing a floor stop makes the study an outcome-selected diagnostic. The paired resolutions are numerical sensitivity checks, not independent trials. A successful result would not establish a population success rate, physical airflow accuracy, safe real flight, a general controller cure, optimal gains, novelty or large-swarm feasibility.

The [historical check](HISTORICAL-CHECK.md) distinguishes the earlier fixed-height PD tests, horizontal position-hold/gain studies, force ablations and nominal-load comparisons. Those local studies support the next question and its limitations; they are not published validation of the proposed intervention.
