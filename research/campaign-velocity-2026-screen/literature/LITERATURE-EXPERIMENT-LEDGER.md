# Literature-to-experiment ledger: completed 2026 screen

Public checkpoint, 2026-10-15. This ledger records an executed comparison, not merely a literature review or proposed test. No novelty or publication-readiness guarantee is made.

## Source status and matched definitions

1. **Bauersfeld et al.** Robotics Meets Fluid Dynamics: A Characterization of the Induced Airflow Below a Quadrotor as a Turbulent Jet. IEEE Robotics and Automation Letters 10(2),1241–1248 (2025), DOI [10.1109/LRA.2024.3518835](https://doi.org/10.1109/LRA.2024.3518835). Technical authority: [arXiv:2403.13321v3](https://arxiv.org/html/2403.13321v3), Fig.2 and Eqs.(1),(7)–(9), with SectionIV-A's omnidirectional sensing limitation. Used opposite-motor length, original coefficients and hover normalization without refitting.
2. **Kiran, Ayanian and Breuer.** The Structure of Merging Turbulent Jets Beneath a Small Quadrotor. [arXiv:2608.30900v1](https://arxiv.org/html/2608.30900v1), submitted31Aug2026. PREPRINT; peer review unverified and no journal reference located. Section2 fixes32g, center-to-hub arm46mm, rotor diameter45mm, density1.29 and reported induced velocity about4.36m/s. Figure5(a) supplies filled centerline symbols in the true-axis diagonal plane. Section3.3 motivates preassigned developing windows7/11 and approximately self-similar window15. HTML identifies CC BY4.0; source artwork is omitted from this public package regardless. No raw dataset link or experimental uncertainty budget was established.
3. **Kiran et al.2025.** Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems, RSS2025, DOI [10.15607/RSS.2025.XXI.102](https://roboticsproceedings.org/rss21/p102.html). The [earlier ratio-only screen](../../campaign-continuation-20261015/neighborhood/REPORT.md) used an offset plane, projected arm convention and approximately27g source; common amplitude canceled. It is a different comparison. Raw-measurement independence/reuse between papers is unknown.

## Actual experiment and result

- Six published vector symbols: gold IDs12/13,20/21,27/28, selected by all-intersecting neighborhoods before predictions. No dashed-fit or open-maximum replacement.
- Geometry D=2l=92mm,r=0; frozen kappa=1.0030572018956476 converts original hover scaling to the paper's reported plot normalizer. Original constants remain unchanged.
- One released evaluation, exactly18 scalar kernel calls (center and two coordinate endpoints for each point). Kernel hash fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc.
- [Exact result](../EPOCH2-RESULT.json),11196bytes,SHA256 eaf189fa69b2b74913c741e6ac58c8e373956d034898807cd803c7f9e702c1fe: predictions exceed all six selected observations by0.629–0.760m/s nominally; mature-stratum points differ by0.720/0.732m/s. All chosen graphical difference envelopes are negative. [Full report](../REPORT.md).
- The initial quantization-admission epoch stopped before extraction; [stop](../GATE-STOP.json) remains unverified. A separate [exact-decimal amendment](../EXACT-DECIMAL-AMENDMENT.md) governed epoch2. No post-result recollection or fit.

## Claim boundary

This is a conditional amplitude discrepancy against published symbols. The +/-0.01SVG-unit envelope is a chosen graphical sensitivity convention, not physical uncertainty. Mean speed magnitude and mean axial PIV velocity differ under fluctuations; export history, symbol placement, stitching, experimental uncertainty and nominal-parameter uncertainty remain unresolved. Numerical checks and faithful rendering do not establish physical validity. No swarm superposition, force response, ground effect, transient flight or safety outcome was tested. All six points, including the preassigned mature stratum, remain reported.
