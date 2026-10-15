# Independent saved-result review

2026-10-15 UTC. VERIFIED: the saved neighborhood result has complete coverage and correct interval arithmetic. No wake function, evaluator or alternative predictor was run in this review. Calculations use frozen measurements and already saved kernel outputs only.

RESULT.json: 10,125 bytes, SHA256 08d8ae7612355a6900c085e3ffab445613c6b2808c1b36a21ac0196670f8d1cb. The release binds evaluator SHA256 4528859fabe3c7fbaaf4c437f3f7b5d7f46b617454c0b3535f2db54dd9bb12c6 and input manifest b3c14e51a256f161df96f5f1df96c1b42d3c3cb2abed7869272a58b4fe1a01de. The current evaluator and immutable wake source match their recorded hashes. All files in the extraction and referenced pilot manifests still match. The receipt records exit 0, no timeout, empty stderr, 36 calls and the matching result hash. Its wall time is 0.059096104 seconds; this is an execution receipt, not a speed benchmark.

## Arithmetic and coverage

All 11 frozen response IDs occur exactly once, with their original coordinates, neighborhood memberships and partial-eligibility flags. The four groups contain 3/3/3/2 responses; the fixed anchor supplies the shared denominator. The saved 12 sets of three kernel values correspond to the bounded 36-call evaluation; no model calls were added here.

For each response, recomputed observed ratio v_i/v_anchor and its nonnegative-numerator bounds [v_i_low/v_anchor_high, v_i_high/v_anchor_low]. From saved q values, recomputed q_i/q_anchor and [q_i_low/q_anchor_high, q_i_high/q_anchor_low]. Recomputed central differences and coordinate-paired residual bounds [observed_low-model_high, observed_high-model_low]. Saved endpoint q values are positive and bracket their centers.

Independently rebuilt sorted interval unions and hulls from each group's paired residual intervals. All 126 scalar comparisons agree within 1e-13. Each union is connected in this result. No cross-coordinate pooling was used, and target-20 truncation remains flagged.

## Verified result and limits

Every one of the 11 pointwise descriptive residual intervals contains zero. Central differences range from -0.03413713498548998 to +0.05931189767676759. Neighborhood residual hulls are:

- 11: [-0.0269464576393, +0.133873582306]
- 14: [-0.0146777599517, +0.126954338504]
- 17: [-0.0499208519534, +0.0979312361938]
- 20: [-0.102528045805, +0.0628996491580]

Thus the adopted pointwise extraction envelopes do not resolve a normalized-shape discrepancy. This is not a scientific pass, a confidence statement or a demonstrated common solution satisfying all points. The shared anchor and calibration make the ratios dependent; interval overlap supplies no independent replications. A hull containing zero alone would not even establish a matching candidate, although here each individual interval also contains zero.

Ratios remove only a common multiplicative amplitude. Unknown experimental uncertainty, additive offsets, spatial calibration/stitching differences, nominal plane geometry, axial-mean versus modeled-magnitude approximation, scale extrapolation and sparse occluded orange pixels remain. These extraction bounds are not guaranteed experimental error bars. Target 20 lacks source coverage beyond the plotted z/l=20 boundary. Absolute velocity, force aggregation, dynamics and physical validity remain untested.

The original nearest-marker pilot remains failed before prediction. This completed successor used the separately adopted neighborhood observable and retained every qualifying plotted response. No outcome-based selection, refitting or recollection is warranted by this result. Preserve both studies and stop this bounded evaluation campaign.
