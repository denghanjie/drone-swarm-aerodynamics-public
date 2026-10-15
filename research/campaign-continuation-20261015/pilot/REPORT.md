# Collection stopped before model evaluation

2026-10-15 UTC. The adopted strict-nearest-marker protocol stopped at target z/l=11. This is an extraction/selection-method failure, not evidence against the wake law.

The original Fig. 9 raster is 560x420 pixels and 35,740 bytes. Its SHA256 is 8b5d74e3736fe85d26dff5c46b613dbffb21bc9b31a112b6ec372fbe6235eea8. The figure is retained for analysis only; public redistribution is not authorized.

## Exact stopping witness

Shared affine x calibration uses ticks (value,pixel)=(0,77),(5,184),(20,506), each with a fixed +/-2-pixel bound. Every marker's horizontal bound follows the adopted visible-extent/repeated-read rule. The complete feasible affine-calibration polygon, both read records and selected bounds are preserved.

At target 8, the selected interval is [7.6319875776,8.1351981352]. Its distance upper bound 0.3680124224 is below the next marker's distance lower bound 0.3773291925; the gate passes narrowly.

At target 11:
- Selected centerline marker: pixels x=310 +/-3.5; z/l interval [10.6133540373,11.1188811189]; distance upper bound 0.3866459627.
- Competing marker, x-only inspection: pixels x=326 +/-3.5; z/l interval [11.3586956522,11.8648018648]; distance lower bound 0.3586956522.
- Required inequality 0.3866459627 < 0.3586956522 is false.

The nominal nearest marker is visually identifiable, but it lacks the adopted conservative interval certificate. This does not prove that the competing marker is physically nearer. The competitor's interval also crosses the original upper eligibility boundary 11.75; it cannot silently be discarded in a revised method.

## What was collected

A first visual read covered the five prechosen targets. Repeated centerline-only reads and bounded extraction were completed for targets 8 and 11. The pass stopped when target 11 failed; targets 14,17,20 retain provisional first reads only. There is no eligible five-point dataset. Orange centerline pixels were used; purple maximum-series markers and the dashed fit were not substituted.

Two calibration tick pairs per axis were checked. Repeated reads share one raster and are not independent experiments. The calibration enclosure retains shared affine constraints; treating individual derived intervals independently is conservative.

No observed ratios, wake-kernel calls, model predictions, residuals or fits were produced. Positive-ordinate and exact downstream-floor checks pass for the two bounded rows. No paid compute, blocked dataset access or new experiments occurred.

## Frozen evidence and next gate

See calibration.json, read-1.json, read-2.json, partial-measurements.json, selection-stop.json and freeze-extraction.py. The latter reproduces calibration/selection arithmetic only; it does not import the wake model. evidence-freeze.json records hashes before any model evaluation.

Root authorized a separate prospective set-valued selection plan. It must disclose this pilot failure, retain every plausible candidate and uncertainty in eligibility, and receive independent review/adoption before any new collection or evaluation. The failed campaign remains stopped.
