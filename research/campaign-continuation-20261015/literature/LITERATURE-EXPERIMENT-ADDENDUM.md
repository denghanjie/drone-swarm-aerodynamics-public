# Literature–experiment ledger: completed support study

Experiment: PUBLIC-SUPPORT-FACTORIAL-20261015, completed 15 October 2026. Executed runner SHA-256: 9b27c5fe2e3011ee994cd35179e8b2948bf62241ebd9a286f7eae235c6518e9b. [Implementation and evidence checkpoint](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/23fec0a263fe3cec939417fdebc8525dbc8e2204/research/campaign-public-support-factorial).

Bauersfeld et al., RA-L 2025, DOI 10.1109/LRA.2024.3518835; technical version consulted: [arXiv v3](https://arxiv.org/html/2403.13321v3). Eqs. (3)–(9) and VI-C informed the existing scalar hover-jet kernel; we adapted that kernel into a four-arm support sensitivity comparison, without fitting parameters. VI-B/Fig. 9/Table II informed interpretation of uncertain radial tails. We did not reproduce the paper's empirical measurements or validate its transfer to this small, moving swarm.

Outcome: 401 fixed historical snapshots; all 25,664 original rotor inflows reproduced exactly. Removing radial taper/cutoff increased predicted inflow by up to 0.305555 m/s and reduced modeled thrust by up to 1.9686% of vehicle weight. Every change arose outside two radial half-widths; 26.398% of summed added inflow arose beyond five half-widths. These regions are precisely where empirical interpretation needs caution. Removing axial support limits changed nothing because the selected trajectory never reached the axial fade region. This is a coverage limitation, not validation of the axial cutoff.

Gielis et al., ISER 2023 proceedings (2024), DOI 10.1007/978-3-031-63596-0_35, and Kiran et al., RSS 2025, DOI 10.15607/RSS.2025.XXI.102, informed future validation questions only. No equations, measurements or fitted coefficients from these works were used in this completed numerical comparison. Their relevant assumptions and versions remain in the source ledger. A separate published-figure extraction pilot is not part of this experiment.

No physical-accuracy, flight-safety, speedup or novelty conclusion follows. The complete tensors and failed/blocked earlier research remain preserved; the checkpoint discloses the narrower public evidence availability.
