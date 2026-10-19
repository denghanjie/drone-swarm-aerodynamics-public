# Sources and normalization finding

Kiran, Ayanian & Breuer, *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, RSS2025,[DOI10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102),[primary manuscript](https://arxiv.org/html/2507.09463v1). Eq1 includes rotor count in induced-speed normalization. The single-PIV plotting script merely labels already-normalized values. Separate multi-vehicle scripts use a denominator without that count. This establishes inconsistent documented conventions, not the actual single-PIV conversion; no automatic factor-of-two correction is justified.

Dataset: Kiran, Ayanian & Breuer,*Aerodynamic Interaction Dataset Measuring Quadrotor Downwash Forces, Moments, and Velocity Profiles*,[Brown DOI10.26300/64d4-wa17](https://doi.org/10.26300/64d4-wa17),CCBY4.0. Reuse only predecessor's saved derived records with exact hashes; no new raw-data reading. Original archive SHA256b495b7a224b3c1db9f15efd5a15815c586e4e11ea29d4df6edcbc25bf50554fa. Retrieved19October2026,READMEupdated5May2026; original publication-version equivalence unresolved.

Bauersfeld,Muller,Ziegler,Coletti & Scaramuzza,*Robotics meets Fluid Dynamics: A Characterization of the Induced Airflow below a Quadrotor as a Turbulent Jet*,[arXiv2403.13321v3](https://arxiv.org/html/2403.13321v3). Historical model coefficients originated here. Original flow-magnitude observable differs from our project's axial interpretation. We do not retest its complete published method.

Kiran,Ayanian & Breuer,*The Structure of Merging Turbulent Jets Beneath a Small Quadrotor*,[arXiv2608.30900v1](https://arxiv.org/html/2608.30900v1#S2),gives an explicit later reference-speed convention. It cannot supply missing provenance for the earlier dataset. No numerical value from it is used to tune this checkpoint.

Independent source inspection found no release preprocessing script establishing the single-PIV divisor or fitting pipeline. All source reading was text/figure inspection; no MATLAB execution, author contact, paid access or installation. See review/NORMALIZATION-SOURCE.md for public-script identities and limitations.
