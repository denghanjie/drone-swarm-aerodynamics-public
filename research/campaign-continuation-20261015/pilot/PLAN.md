# Prospective five-marker velocity-ratio screen

2026-10-15 UTC. NOT ADOPTED. No collection or evaluation until root adopts and independent review agrees. Earlier exploratory figure inspection is disclosed in the physics protocol; this is not a blinded first viewing.

## Hypothesis and sources

Test the unchanged wake law's axial-decay shape against Kiran's single-Crazyflie measurements. Ratios remove common amplitude, not shape mismatch. They cannot validate absolute velocity, receiver forces, swarm interactions or safety. The approximately 27 g vehicle is outside the model's fitted mass range.

Measurement: Kiran et al., arXiv:2507.09463v1, Fig. 9, Sections II-A/III: https://arxiv.org/html/2507.09463v1
Full figure: https://arxiv.org/html/2507.09463v1/figures/axial_decay.png
Model: Bauersfeld et al., arXiv:2403.13321v3, Eqs. 3–9: https://arxiv.org/html/2403.13321v3

## Frozen selection

Anchor: measured centerline marker nearest z/l=8. Other targets: 11, 14, 17, 20. Root chose 8 before collection, explicitly replacing the earlier unadopted readiness draft's anchor 20. Never change anchor, points or coefficients after prediction.

Identify the measured centerline series from the full legend. Never use the dashed fit, fitted coefficients or substitute maximum-velocity markers. Targets are selection rules, not measured coordinates.

Select the uniquely nearest marker within 0.75 in z/l of each target. This eligibility window is one quarter of target spacing, not a scientific agreement tolerance. Its entire horizontal interval must lie inside the window. Require the winner's distance upper bound to be strictly less than every competitor's distance lower bound. Ties, overlapping distance bounds, marker reuse, missing or unidentified markers stop collection. Inspect adjacent markers' x positions only to establish nearestness; do not collect extra response values. No replacement or window widening.

## One collection pass, then freeze

Save/hash the full original image with axes and legend; record URL, version, access time, dimensions and bytes. Zoom does not increase source resolution.

Calibrate each axis with two independently read pairs of labeled ticks spanning the selected region. Confirm scale/orientation; record values and pixel coordinates. Stop if calibration pairs disagree beyond bounds.

Within one collection pass, read each selected marker twice without predictions. Record both x/y pixel centers, series identity and marker extents. Use mean centers and, for each axis, half-bound:
h=max(2 pixels, half visible marker extent + 1 pixel, absolute repeated-read difference).
For tick locations use the same rule with tick-line extent. Propagate tick and marker bounds through the affine axis mapping; calibration variables are shared. Stop if overlap/compression makes identity or bounds indefensible.

Record actual zeta=z/l and v=u/U_i with intervals; never snap to targets. Label each row “digitized visual estimate, not raw data.” Freeze/hash calibration, both reads, selection decisions and five rows before evaluation. No recollection motivated by residuals.

## Geometry and normalization gates

Fixed paper-consistent geometry: l=32.5 mm, lambda=D/l=2sqrt(2), D=91.924 mm, offset eta=y0/l=1. Fig. 9's in-plane centerline has chi=0 but r/D=1/lambda, not zero. Every axial lower bound must satisfy zeta>=2.5lambda=7.0711, including the anchor. Do not use the swarm's different dimensional geometry.

All points must use one common U_i and stationary hover configuration. Its unknown numerical value cancels. Point-dependent normalization, incompatible configuration or unresolved plane/coordinate interpretation stops evaluation. Ratios do not remove additive velocity zero error, position-dependent calibration/stitching, or speed-magnitude versus axial-mean mismatch. Plane-placement uncertainty is unknown: use nominal geometry conditionally, with no invented geometry error bars.

## One evaluation pass

Use unchanged normalizedWake(s,r) from public commit 1336f5c416875a9651f92b58b2ed06649f25b04e:
research/campaign-joint-stage-reference/implementation/snapshot/outputs/step03a-source/wake.cjs
Record its hash. Inputs: s=zeta/lambda, r=1/lambda. Keep C=10.11, S=0.07668, origin=-5.817, floor=2.5. No taper, receiver model or fitted Kiran coefficients.

Let q_i be kernel speed and a the anchor. Evaluate four ratios R_i=v_i/v_a and Q_i=q_i/q_a at actual coordinates. Anchor ratio 1 is not an independent test. No amplitude or shape fit.

Require v_a_low>0. Observed bounds:
R=[v_i_low/v_a_high, v_i_high/v_a_low].
For model bounds, write t=zeta+5.817lambda, A=(sqrt(2)-1)/S^2:
q=C lambda t^3/(t^2+A)^2; derivative sign is 3A-t^2<0 on the accepted domain. Use centers and interval endpoints only, at most 15 kernel calls, reusing anchor values. Thus:
Q=[q_i_low/q_a_high, q_i_high/q_a_low].
Independent bounds may over-cover shared calibration. Retain common-anchor dependence; no independence claim or quadrature error combination. Report central R-Q and interval [R_low-Q_high,R_high-Q_low].

These are descriptive extraction/model-coordinate intervals, not confidence intervals. Experimental uncertainty is unavailable. No statistical pass/fail, scientific tolerance, or physical-validation conclusion follows from overlap or a round percentage.

## Budget and stopping

Total campaign cap: 1,000,000 retained bytes, including figure, source, reviews, evidence and results. Final PLAN cap: 6,000 bytes. Check totals before additions. Use existing lightweight tools; no paid compute, installation, data-repository access, CAPTCHA, new experiment or CFD.

Deliver plan/adoption, figure/provenance, calibration/five-row evidence, kernel hash, evaluator, result and limitations. One collection pass (two reads per point), then one evaluation pass. Any failed gate is a terminal blocked outcome; revisions require a newly adopted plan. Stop after the report.
