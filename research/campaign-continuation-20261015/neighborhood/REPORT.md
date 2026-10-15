# Completed conditional normalized-shape screen

2026-10-15 UTC. The root executed the reviewed evaluator once: 36 scalar kernel calls, exit 0. This report reads the saved result; it does not rerun the model. RESULT.json is 10,125 bytes, SHA256 08d8ae7612355a6900c085e3ffab445613c6b2808c1b36a21ac0196670f8d1cb.

## Result

All 11 coordinate-paired descriptive residual intervals contain zero. Central observed-minus-model ratios range from -0.03414 to +0.05931. Thus these adopted pointwise extraction bounds do not resolve a normalized-shape mismatch. This does not establish a jointly feasible match across all points, a confidence level, physical validation, or absolute-velocity accuracy.

Every observed ratio uses the same frozen centerline anchor at z/l=7.8835. Ratios discard the unresolved common amplitude. Coordinates are digitized visual estimates, not raw measurements. Table precision is for compact reporting; exact values remain in RESULT.json.

| Marker | z/l | Observed ratio | Model ratio | Difference | Descriptive difference interval |
|---|---:|---:|---:|---:|---|
| m294 | 10.12 | 1.0015 | 0.9480 | +0.0535 | [-0.0188, +0.1293] |
| m310 | 10.87 | 0.9725 | 0.9312 | +0.0413 | [-0.0269, +0.1129] |
| m326 | 11.61 | 0.9741 | 0.9148 | +0.0593 | [-0.0117, +0.1339] |
| m358 | 13.09 | 0.9375 | 0.8831 | +0.0544 | [-0.0147, +0.1270] |
| m374 | 13.84 | 0.9222 | 0.8676 | +0.0546 | [-0.0138, +0.1265] |
| m390 | 14.58 | 0.9054 | 0.8525 | +0.0529 | [-0.0119, +0.1209] |
| m422 | 16.06 | 0.8521 | 0.8237 | +0.0284 | [-0.0379, +0.0979] |
| m438 | 16.81 | 0.8261 | 0.8097 | +0.0164 | [-0.0460, +0.0818] |
| m454 | 17.55 | 0.8078 | 0.7961 | +0.0118 | [-0.0499, +0.0764] |
| m486 | 19.04 | 0.7728 | 0.7699 | +0.0029 | [-0.0545, +0.0629] |
| m501 | 19.74 | 0.7239 | 0.7581 | -0.0341 | [-0.1025, +0.0376] |

Neighborhood unions each form one connected interval in this result; their hulls are:
- Target 11: [-0.0269, +0.1339].
- Target 14: [-0.0147, +0.1270].
- Target 17: [-0.0499, +0.0979].
- Target 20: [-0.1025, +0.0629] (source truncated at z/l=20).

Only paired difference intervals at the same measured coordinate were aggregated. A hull containing zero does not establish any particular matching candidate or simultaneous agreement. No candidate, coefficient or anchor was chosen using residuals.

## Preserved design history and scientific limits

The first strict-nearest-marker pilot failed at target 11 before any predictions. Its immutable evidence and failure report remain in the [failed pilot report](../pilot/REPORT.md). The separately adopted successor changed the observable to four neighborhoods with all intersecting measured centerline markers. It retained seven partially eligible intervals without clipping, plus the already certified anchor. It is not a retroactive pilot pass.

The unchanged Bauersfeld arXiv:2403.13321v3 law was evaluated against Kiran arXiv:2507.09463v1 Fig. 9 under nominal D/l=2sqrt(2) and an offset plane y0/l=1. No fitted Kiran coefficient, receiver-force closure or swarm model entered this comparison. The approximately 27 g source is outside the original wake fit's vehicle-mass range.

The bounds cover the declared raster extraction and coordinate arithmetic only. They omit unknown experimental mean-velocity uncertainty and unquantified plane-position error. Purple maximum markers and the fitted line overlap the orange centerline series; only 9 and 13 orange pixels remain at the last two markers. Visible-fragment midpoints can be biased. Repeated reads of one raster and all ratios share calibration/anchor dependence; they are not independent experimental replications.

The measured axial-mean versus modeled flow-magnitude approximation, possible additive velocity offsets and position-dependent calibration remain. Source coverage ends at the plotted z/l=20 boundary, below the last neighborhood's upper boundary 20.75. No unplotted data were inferred. Absolute amplitude remains unresolved for this 2025 source.

This is a bounded descriptive transfer screen, not evidence about force additivity, transients, ground effect, flight stability, numerical time-step convergence, or publication readiness. The numerical evaluator's completion and plausible curve shape do not validate those phenomena.

## Next source phase

A later 2026 preprint was identified after this protocol and data were frozen. It was not used to adjust this screen. Its geometry, normalization and independent measurement availability are being verified separately; the present 2025-source screen should not be presented as using the latest available physical data. No further collection, tuning or evaluation belongs to this completed campaign.
