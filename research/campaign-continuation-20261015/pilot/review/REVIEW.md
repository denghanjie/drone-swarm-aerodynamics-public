# Independent review: five-marker ratio-only empirical screen

2026-10-15 UTC. Decision: READY for root adoption with the two conditions below. No collection, prediction or residual calculation occurred in this review. Prior plot inspection is disclosed; the study is not blinded.

Reviewed final PLAN.md, 5,921 bytes, SHA-256 f3407c35e2840151b3fcade06f21d569cb4185d324851bc2dd6340782e0a82a0, plus the original protocol and amended readiness. Adoption must require all observed ordinate lower bounds >=0 and use exact 2.5lambda for the domain gate (7.0711 is display rounding). Anchor 8 supersedes the unadopted anchor 20 draft.

## What the comparison can establish

This external measured-marker comparison can reveal a conditional decay-shape mismatch. It cannot validate amplitude, all model parameters, forces, power, swarm interaction, flight or safety. Five graphical estimates establish no novelty.

For a common velocity multiplier k, v_i=k*u_i gives v_i/v_a=u_i/u_a. The model's overall amplitude C and hover-induced speed likewise cancel from q_i/q_a. Thus an arbitrarily large constant amplitude error can remain invisible. The anchor ratio is identically one; five markers yield four informative contrasts, not five successful validations. Their shared denominator makes them correlated. This is normalization by one observed reference, not an independent empirical determination of amplitude.

Cancellation does not remove additive velocity-zero bias, coordinate-origin error, uncertain D/l, plane offset, a multiplier that varies with height or acquisition section, or a difference between mean speed magnitude and mean axial velocity. Even a zero mean lateral component does not make mean speed equal mean axial velocity in fluctuating three-dimensional flow. These remain interpretation limits, not parameters to fit away.

## Coordinate mapping: correct under the declared nominal interpretation

K's paper describes a laser plane through the front motor row, axial mean velocities for the single-vehicle case, and composite fields stitched from multiple acquisition sections. It gives l=32.5 mm and relates z/l=6.5 to about 2.3 motor spacings. These support the readiness note's nominal square-layout interpretation, but do not supply exact plane-placement metrology. Source: [Kiran et al., II-A2/III-B](https://arxiv.org/html/2507.09463v1#S3.SS2).

With lambda=D/l=2sqrt(2), eta=y0/l=1 and chi=x/l=0, use
s=zeta/lambda and r=1/lambda
as the dimensionless arguments to normalizedWake, where zeta is each actual digitized z/l coordinate. Do not set r=0 or insert the swarm's different physical arm length. The far-field requirement is zeta>=2.5lambda, approximately 7.0711, for the entire coordinate interval, not merely its center.

Independently simplifying the unchanged kernel gives
q(zeta)=C*lambda/t * [1+c*eta^2/(S^2*t^2)]^(-2),
where t=zeta+5.817lambda, c=sqrt(2)-1, S=0.07668 and C=10.11. This matches the readiness transformation. Although C cancels in the ratio, lambda remains in the virtual-origin term and eta remains in the radial correction: geometry errors do not disappear.

B's model targets mean flow magnitude and was fitted on larger vehicles; comparison to K's axial PIV means is therefore conditional on an axial-dominance approximation and scale transfer. Source: [Bauersfeld et al., abstract, III and IV](https://arxiv.org/html/2403.13321v3). Keep nominal geometry explicit. Unknown metrology is not zero uncertainty; do not invent or optimize geometry bounds to improve agreement.

## Selection and extraction conditions

The draft's targets 8,11,14,17,20, anchor 8 and maximum target distance 0.75 are acceptable prospective conventions. The 0.75 window is eligibility, not a scientific tolerance. Require the selected marker's whole horizontal interval to lie in its target window. Unique nearestness requires its largest possible target-distance to be smaller than every competing marker's smallest possible target-distance. Overlapping distance bounds, ties, reused markers, missing points or uncertain series identity mean stop. Nearby x-only inspection can establish nearestness; do not collect extra velocity values.

Use only the measured in-plane centerline series. Do not replace an unreadable point with the dashed fit, the maximum series, a nearby favorable ordinate or an interpolated fit value. Record actual coordinates rather than target coordinates. Five eligible points are required; do not silently reduce the planned set.

Preserve one complete original figure with source/version, hash, native dimensions, axes and legend. Two marker reads without predictions are useful extraction checks, not independent physical replicates. Preserve both reads and use the prospective bound max(2 native pixels, half visible marker extent+1 pixel, read disagreement). Include repeated tick readings, tick extent and calibration uncertainty. Zooming cannot create resolution. Stop when overlap, compression or axis ambiguity defeats reliable bounds.

Two tick-pair calibrations should agree within their location bounds. The common affine calibration parameters must remain shared across points. On a linear velocity axis its multiplicative pixel-to-unit slope cancels in ratios, but the pixel location of velocity zero does not. Hence reading only marker heights, without the axis intercept and bounds, is inadequate. Freeze the complete extraction record before displaying model output; no residual-driven recollection or uncertainty adjustment.

## Ratio intervals and cheap model evaluation

Let measured ordinate bounds be [v_i-,v_i+] and [v_a-,v_a+]. Require every ordinate interval nonnegative and anchor lower bound strictly positive. Conservative observed-ratio bounds are
R_i in [v_i-/v_a+, v_i+/v_a-].
Use the same anchor record for all four targets. These are bounded extraction ranges, not confidence intervals. Do not combine pixel bounds by root-sum-square, assume independent ratios, or infer experimental uncertainty from two reads.

For fixed nominal geometry, write A=c*eta^2/S^2. Then q=C*lambda*t^3/(t^2+A)^2 and derivative sign is sign(3A-t^2). The stated constants make q decreasing throughout the admitted far-field domain. Verify this one algebraic inequality before evaluation; no numerical sweep is needed. For each actual coordinate interval [zeta-,zeta+], q_low=q(zeta+) and q_high=q(zeta-). Thus
Q_i in [q_i_low/q_a_high, q_i_high/q_a_low].
Evaluate at most the center and two endpoints of each of five points: 15 scalar kernel calls, reusing the anchor. Preserve unchanged source hash and parameters. Central R-Q and its enclosure [R_low-Q_high,R_high-Q_low] are sufficient. Round reported interval endpoints outward; do not imply more digits than extraction supports.

Independent interval bounds can over-cover shared calibration; do not infer independent errors. No Monte Carlo, fitting, repeated runs or unknown-geometry optimization is needed.

## Interpretation and stopping

Missing uncertainty for the plotted means prevents statistical validation even if pixel intervals are narrow. A mismatch outside the conditional extraction bands can identify an incompatibility worth investigating, but cannot by itself assign the cause to the wake model rather than geometry, acquisition or measurement-quantity differences. Interval overlap is not model acceptance. Do not invent a 5% or 10% success rule.

The four contrasts remain one small correlated graphical screen. Preserve all outcomes, including an ambiguous-marker stop or disagreeing result. Do not contact authors, access blocked raw-data routes, buy compute or extend collection under this plan. A defensible terminal result is either the four transparent conditional discrepancies or a precise explanation of why the fixed five-point comparison could not be made.
