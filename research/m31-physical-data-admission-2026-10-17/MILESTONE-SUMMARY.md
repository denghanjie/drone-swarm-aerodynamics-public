# Measured flight records are accessible, but force validation is not yet admitted

We checked all four complete recordings from two paired small-drone flights: 25,464 rows and 30 fields per row. Every file matched its immutable public identity, contained finite numbers and increasing timestamps, and passed the prespecified quaternion/PWM integrity screen. No time segment was discarded or repaired. These are two paired flights, not four independent flights or thousands of independent experiments.

The internal motion check and the authors' preprocessing support interpreting the timestamps as **microseconds**, despite the CSV header saying milliseconds. That gives roughly 64-second recordings with a typical 9.9-millisecond interval. However, the largest gaps range from 0.158 to 0.900 seconds. A smooth animation or interpolation would conceal these gaps; this audit retained them. Raw pair start differences were 25 and 210 ticks. Small start offsets alone do not prove sensor synchronization.

**Decision:** retain the records as candidate development evidence, but do not score our aerodynamic model against them yet. The authors' force targets are reconstructed residuals: estimated motion minus modeled motor thrust. Their accuracy depends on mass, coordinate/gravity conventions, calibration and delay. We found a 32g small-drone mass in the inspected training script versus 34g in the paper, and the exact relationship between that script and the historical experiment remains unresolved. This is a provenance gap, not evidence that the published paper is wrong.

The logged motor-force fields also contain negative values in these files. Together with their firmware origin, this makes an unqualified interpretation as independent positive rotor-thrust measurements unjustified. No force target was constructed, model fitted or physical accuracy measured here.

The single audit took 6.735 seconds, kept about 19.3MB privately, and preserved all 547 protected artifacts. The preceding fresh-flock numerical result remains intact: both browser implementations passed on two new 64-drone states. Its Three.js view is a recorded synthetic Boids replay with airflow off during flight and final loads evaluated afterwards.

[Open the updated 3D research view](viewer/) · [Aggregate data observations](results.json) · [Claim–evidence ledger](CLAIM-EVIDENCE.md) · [Independent source review](review/SOURCE-CHALLENGE.md) · [Fixed protocol](PROTOCOL.md) · [Restart](RESTART.md)

The overall 5,000-drone research goal, physical validation and publication-level novelty remain open.
