# Prospective exact-decimal extraction amendment

2026-10-15. NOT ADOPTED. Applies only to PLAN.md SHA256 c2ca80c01e18deb314e7a2425c747b49c13cdb3469d1a25c88720f9fe8a1a497. The original collection stopped before marker extraction; GATE-STOP.json preserves its unverified export-quantization gate. This is a new method, not a passed gate.

Replace only the sentence requiring coordinate decimal quantization <=0.001 SVG unit. Treat each encoded finite decimal as the exact published vector coordinate. Parse source matrices/path coordinates by exact decimal or rational arithmetic and independently through a second parser. The full transformed center from each must agree within 1e-6 SVG unit; bound conversion/arithmetic error against the exact value, not by agreement alone. No re-quantization or historical export-accuracy inference.

Keep the fixed +/-0.01 SVG-unit envelope around each transformed tick/marker coordinate as a CHOSEN GRAPHICAL REPRESENTATION envelope, with 1e-12 output arithmetic padding. It does not bound unknown export rounding before publication, symbol placement, PIV error, nominal geometry/normalization error or physical variability. Its narrowness must not be interpreted as physical confidence.

All other frozen rules remain: exact asset/hash; gold-series identity and full transforms; two tick pairs per axis and common feasible maps; all intersecting points near 7/11/15 +/-0.5, max12; fixed nominal geometry and kappa; no fitted curves, model-based selection or fallback. Reuse the preserved tick inspection with provenance. No measured marker coordinates were extracted in the stopped pilot.

After independent review and root adoption, permit ONE new exact-decimal collection pass, explicitly epoch 2. Freeze all selected XML, calibration, coordinates/bounds and hashes, then stop for independent extraction review. Model evaluation remains separately gated. Keep the 500000-byte cap, one eventual evaluation pass and no source-figure redistribution.
