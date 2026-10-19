# Air entering and leaving: six regions checked

The measured airflow gives a normalized balance gap of **1.12% to 4.61%** across the six regions chosen before the calculation. All six had enough measurements to run the test. A separately written checker confirmed the saved calculation. This is a useful consistency observation within one experiment, not a new validated drone model or a breakthrough claim.

Imagine a hollow sleeve below a drone. Air can enter or leave through its top, bottom, inner wall and outer wall. We added those four signed flow terms. We did this separately for measurements on the left and right of the drone, keeping the missing center outside the sleeve. The sleeve interpretation assumes rotational symmetry and no average swirl; only one offset sheet was measured.

| Side and preset depth band z/l | Signed full-grid balance | Magnitude | Coarse-minus-full signed change |
|---|---:|---:|---:|
| Left 12–16 | −1.1214% |1.1214%|+0.0725 percentage points|
| Left 16–20 |+3.4307%|3.4307%|+0.0840 percentage points|
| Left 20–24 |+1.7791%|1.7791%|+0.0351 percentage points|
| Right 12–16 |+4.6144%|4.6144%|+0.1620 percentage points|
| Right 16–20 |+4.5902%|4.5902%|−0.0384 percentage points|
| Right 20–24 |+1.1985%|1.1985%|−0.0590 percentage points|

The percentage divides the net imbalance by the sum of the magnitudes of the four integrated surface terms. It is **not a percentage accuracy score for our model**, nor the percentage of air lost. Positive means net outward flow in the conditional reconstruction; negative means net inward flow. Cancellation between surfaces can produce a small total even when individual flow terms are wrong. The earlier lateral-model mismatch remains unchanged.

The fixed coarser grid changed the signed percentages by at most 0.1621 percentage points. That is a numerical sensitivity observation only. It supplies no experimental uncertainty estimate, confidence interval or physical acceptance threshold. No pooled score or left/right average was formed.

Exactly 1,220 of 3,240 retained measurement records fell in the six windows. Each region had 10 radial levels and 20 or 21 depth levels. All six exact grids were complete, all selected velocities finite, and upstream missing-coordinate/missing-axial gates were zero. Actual endpoints—not nominal band edges—were used, with slightly different left/right radii. All 3,240 original records remain preserved. The independent audit verified 12 quadratures, 48 signed face terms and 74,535 preserved binary64 words. No model coefficient changed and no new prediction or fit ran.

This result justifies examining the individual model-versus-measurement surface transports next: does the model send the right amount of air through each surface, or can errors cancel in the total? That question requires a separate prospective protocol. Small net imbalance alone does not identify the cause of the preceding sideways-flow error.

[Open the Three.js evidence view](viewer/) · [Saved results](results/comparison.json) · [Independent audit](results/audit.json) · [Fixed protocol](PROTOCOL.md) · [Literature](LITERATURE.md). The viewer shows saved points and assumed annular geometry; it is not flight or a measured 3D volume.

Source 56048e7731de8896434b35d31419b4b7c42bf88c was publicly verified before the sole execution. Evaluator, audit and first display checks passed; all three allocations are now closed. Historical milestones are unchanged.
