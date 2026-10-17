# Verified physical-model antecedent and next-decision limits

This is a bounded literature/documentation update, not an experiment or a novelty claim. No external code, training, data sync or physical experiment was run. The successful fresh numerical check concerns our specified model; this paper supplies evidence about what real small-drone interaction modeling may need.

## Verified reference

Guanya Shi, Wolfgang Hönig, Xichen Shi, Yisong Yue and Soon-Jo Chung, **Neural-Swarm2: Planning and Control of Heterogeneous Multirotor Swarms Using Learned Interactions**, IEEE Transactions on Robotics **38**(2), 1063–1079 (April 2022), DOI [10.1109/TRO.2021.3098436](https://doi.org/10.1109/TRO.2021.3098436). Crossref verified the journal identity. The text read was [arXiv:2012.05457v2](https://arxiv.org/html/2012.05457v2), dated16July2021, identified as the accepted manuscript. The journal full text was not compared.

## What was actually read and how it applies

- **III-B:** neighbor membership uses an interaction-volume cuboid chosen from observed interactions. This supports the need to justify a physical neighborhood from evidence; it does not validate our inherited cutoff.
- **IV-B, equation9 and the computational-efficiency paragraph:** per-neighbor encodings are summed before a nonlinear receiver mapping. Evaluation cost grows with the number of neighbors, while network count depends on robot types. This is a known antecedent for local aggregate models, not a new idea we can claim.
- **VII-A and TableI:** the small/large vehicles are34g/67g; the authors calibrate nominal thrust against PWM and battery voltage and identify motor delay. Our27g parameters and hypothetical source/receiver law cannot inherit this calibration.
- **VII-B:** force residual labels are inferred from measured trajectories and an identified nominal model; the reported dataset contains1.4million pairs. In the implemented experiments they learn the vertical interaction force, not a full validated four-rotor torque model.
- **VII-C:** removing relative velocity worsens reported mean squared validation error from6.42 to7.60 (about18%). The paper also reports a gap of11.4gram-force units between a learned multi-neighbor prediction and a pairwise-superposition construction. The latter is a comparison of model predictions, not an independent load-cell measurement of our proposed law. These findings motivate velocity and multi-neighbor tests; they do not automatically falsify every detail of our model.
- **VII-E:** experiments include5- and16-robot flight cases. The16-robot example has up to15neighbors versus up to2during training, and the authors report reduced prediction accuracy as neighborhood size increases. These are finite demonstrations, not evidence for5000drones or arbitrary dense neighborhoods.

The calibration, local learned representation, trajectory-level split and multi-neighbor evaluation suggest a useful future path: assess model error against compatible held-out measurements before investing further in tiny arithmetic-error improvements. This is a proposed direction, not a newly achieved result. Our current exact numerical tolerance remains unchanged.

## Code/data availability check

GitHub's repository search identified [aerorobotics/neural-swarm](https://github.com/aerorobotics/neural-swarm). Its README explicitly links both papers and describes code plus data. The inspected README blob is611684356b7ae1a4790a472f6bc1c497f603cb75. It says some training data must come from a Box account and describes authenticated rclone operations. Those are external documentation instructions, not authorization: none was run. This check establishes documentation of a data dependency, not that the measured data are accessible to us, licensed for redistribution, complete, or suitable for our benchmark. No contact, account connection or bulk download was attempted.

## Retrieval boundary

The search-service connector failed before returning results. Public Crossref, arXiv's API and versioned HTML, then GitHub repository/readme metadata were retrieved successfully using HTTPS. Only bibliographic facts, short paraphrases, applicability limits and response hashes are saved here; the full paper is not republished. Other search hits and the paper's cited references were not inspected or used. This is not an exhaustive current-literature or priority search.

**Follow-up:** the later DATA-AVAILABILITY-UPDATE.md records public tree metadata and one inspected CSV. It supersedes only the initial uncertainty about whether any data are publicly accessible, while retaining the compatibility/licensing/validation limits.
