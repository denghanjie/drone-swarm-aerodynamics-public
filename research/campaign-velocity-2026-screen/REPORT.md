> Public edition: numerical results unchanged; links use the public repository layout.

# Six-point 2026 screen: nominal predictions exceed published velocities

All six selected published centerline markers are below the unchanged model's nominal predictions by **0.6294–0.7603 m/s**, including both points assigned in advance to the approximately self-similar stratum. Every coordinate-paired difference is negative throughout the chosen graphical envelopes. This is a conditional amplitude discrepancy; the unknown physical/measurement errors prevent a statistical or physical-validation verdict.

## What was tested

The observations are filled-centerline symbols in Fig. 5(a) of Kiran, Ayanian and Breuer, *The Structure of Merging Turbulent Jets Beneath a Small Quadrotor*, [arXiv:2608.30900v1](https://arxiv.org/html/2608.30900v1), submitted 31 August 2026. This is a preprint, with no journal reference located. Sections 2 and 3 identify a 32 g tethered-hover source and true-axis diagonal PIV cut. We extracted published SVG symbols, not raw measurements.

The unchanged [Bauersfeld model, arXiv:2403.13321v3](https://arxiv.org/html/2403.13321v3), was evaluated at the actual extracted positions. Its opposite-motor scale is D=2l=92 mm, with l=46 mm and radial offset zero. The kernel arguments are (zeta/2,0), where zeta=z/l; all lower coordinate bounds exceed its floor zeta=5.

Original constants 10.11, 0.07668 and -5.817 were retained. Nominal m=.032 kg, rho=1.29 kg/m^3, rotor radius .0225 m and g=9.81 give U_H=4.373329400265024 m/s. The paper reports U_i approximately 4.36 m/s. The predeclared factor kappa=U_H/4.36=1.0030572018956476 expresses the model on the reported plot scale. The 0.306% inconsistency is disclosed, not fitted or treated as an uncertainty tolerance. No published fitted decay/width parameters entered the kernel.

## All six results

Delta is observed minus predicted; negative means the nominal model is higher. Values are display-rounded; exact saved bounds are in EPOCH2-RESULT.json. D denotes the preassigned developing-profile strata (windows 7/11); S denotes approximately self-similar (window 15), following the preprint's Section 3.3.

| Gold ID | Stratum | z/l | Observed u/U_i | Predicted kappa*q | Delta normalized |
|---|---|---:|---:|---:|---:|
| gold-12 | D | 6.615031 | 0.937002 | 1.111391 | -0.174390 |
| gold-13 | D | 7.141514 | 0.922916 | 1.080227 | -0.157311 |
| gold-20 | D | 10.826885 | 0.758622 | 0.902984 | -0.144361 |
| gold-21 | D | 11.353368 | 0.733374 | 0.882303 | -0.148929 |
| gold-27 | S | 14.512259 | 0.610626 | 0.775706 | -0.165080 |
| gold-28 | S | 15.038739 | 0.592513 | 0.760395 | -0.167882 |

| Gold ID | Normalized delta envelope | Observed m/s | Predicted m/s | Delta m/s envelope |
|---|---|---:|---:|---|
| gold-12 | [-0.174531, -0.174248] | 4.085328 | 4.845667 | [-0.760956, -0.759721] |
| gold-13 | [-0.157450, -0.157172] | 4.023913 | 4.709790 | [-0.686483, -0.685270] |
| gold-20 | [-0.144487, -0.144236] | 3.307594 | 3.937010 | [-0.629965, -0.628867] |
| gold-21 | [-0.149053, -0.148805] | 3.197510 | 3.846840 | [-0.649873, -0.648788] |
| gold-27 | [-0.165198, -0.164963] | 2.662328 | 3.382079 | [-0.720264, -0.719237] |
| gold-28 | [-0.167999, -0.167765] | 2.583357 | 3.315322 | [-0.732475, -0.731455] |

Neighborhood hulls summarize the already paired difference intervals, not separately pooled predictions and measurements:
- Window 7: [-0.174531, -0.157172] normalized.
- Window 11: [-0.149053, -0.144236] normalized.
- Window 15: [-0.167999, -0.164963] normalized.

The six individual intervals and all three hulls exclude zero under this graphical convention. Shared calibration remains dependent; hulls are not simultaneous confidence regions.

## What the narrow envelopes do and do not establish

The fixed +/-0.01 SVG-unit envelopes are a chosen graphical sensitivity convention. Exact-decimal symbol extraction, two tick pairs per axis, full transform checks and independent forward/inverse affine calculations reproduced all 86 interval endpoints. This establishes fidelity to encoded symbols. It does not quantify historical exporter rounding, author symbol placement, PIV uncertainty, stitching, or nominal geometry/normalization error.

Bauersfeld's omnidirectional sensor measures mean speed magnitude; Kiran PIV measures mean axial velocity. Even on the true axis, zero mean lateral flow does not equate these quantities in turbulence. This mismatch can contribute to the difference and is not quantified here. The much smaller platform also probes transfer beyond the original fit's reported 230 g–6.3 kg uncanted vehicles. Consequently, this screen does not isolate a cause, establish statistical significance, justify changing coefficients, or validate swarm forces, transients, ground effect or flight safety.

The pattern remains present in the preassigned window-15 stratum, so it cannot be dismissed solely because windows 7/11 have developing profiles. Calling this a formal falsification of a physically matched observable would require experimental/parameter uncertainty and the measurement-quantity mismatch to be resolved.

## Preserved protocol history and reproducibility

The first collection epoch stopped before marker extraction because historical export quantization could not be verified. [GATE-STOP.json](GATE-STOP.json) preserves that method-admission failure. A separately reviewed/adopted [exact-decimal amendment](EXACT-DECIMAL-AMENDMENT.md) created epoch 2; the old gate was never declared passed. Every intersecting gold marker in the three preselected +/-0.5 windows was retained: two per window, all wholly eligible. No maximum marker, fitted curve, nearest-point substitute, refit or post-result recollection was used.

The separately reviewed evaluation ran exactly 18 scalar kernel calls once. Result SHA256: eaf189fa69b2b74913c741e6ac58c8e373956d034898807cd803c7f9e702c1fe. Input freeze: 1f7d28e85096abf4f3e4c62633370437dd60bf8bb9bc74e635e4b7aa9614844e. Kernel: fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc, public commit 1336f5c416875a9651f92b58b2ed06649f25b04e. This report only reads saved results; it adds no model evaluations.

The earlier [2025 shape-only screen](../campaign-continuation-20261015/neighborhood/REPORT.md) had eleven ratio envelopes containing zero, after a separately preserved strict-selection pilot stop. That result removed a common amplitude factor and used a different publication, approximate platform mass, projected-arm convention and offset measurement plane. It is not the same matched experiment and cannot establish or refute this amplitude finding; raw-measurement independence/reuse is unknown.

PUBLIC-SUMMARY.json contains figure-free numerical results. The original SVG and rendering are retained for audit only and are excluded from public export under this campaign's restriction. No paid compute, raw-data repository access or new experiment was used. The bounded campaign ends here; no further collection or fitting is authorized by this report.
