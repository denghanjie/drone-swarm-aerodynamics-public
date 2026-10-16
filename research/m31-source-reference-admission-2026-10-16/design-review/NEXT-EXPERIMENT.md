# Exactly one next experiment: an exposed-profile normalization audit

**Recommend the coordinator's bounded Bauersfeld Offboard 1/2 curve comparison,
using the revised unchanged-profile metrics below. Treat it as descriptive
physical-source evidence, with no physical pass/fail threshold.** This is the
single next experiment recommended by this final desk review. No broader dataset
acquisition is required for this question.

This final recommendation incorporates the coordinator's later evidence and
supersedes this note's earlier preference to admit the Wolf same-airframe load
comparison first. Wolf remains a possible later causal load-transfer study, not a
second experiment requested here. The accessible exposed curves can answer a
narrower useful question now, provided their measured support is admitted.

This document is a design review, not execution approval. This agent performed no
browser lookup, primary-PDF inspection, acquisition, digitization, scientific
calculation, model invocation or runtime test.

## Evidence and exact question

Coordinator-reported evidence, not independently reopened here:

- Bauersfeld Fig. 7, PDF page 5, separately encoded measured vector polylines for
  Offboard 1 and Offboard 2; a fitted black curve is also present but excluded.
- Displayed axes are `x = r/l` and `g = U/U_H`, at `s/l = 3`, with a displayed
  rectangle `x = 0…3`, `g = 0…1.5`.
- Table I supplies independently specified `l` and calculated hover-normalizer
  `U_H`; neither is to be fitted to the extracted profiles.
- Measured curves have binned-median semantics. Displayed mean-plus/minus-standard-
  deviation bands are not uncertainty bounds for those median curves.
- Some vector paths extend outside the clipping rectangle. Those continuations
  are not hidden measured observations for this audit.

Ask: **How different are these two exposed, published hover-normalized measured
profiles over their shared visible radial window?** The source-accounting result
that the current field ignores source motor states at fixed geometry remains
unchanged. These published profiles add a physical spatial comparison; they do
not themselves identify a motor-command-to-thrust map.

Retain the exact source definition of `U`, including whether it denotes a
component or magnitude and the binning/median operation. Do not silently call a
median profile a mean velocity. If source inspection changes the stated axes or
normalization semantics, record the discrepancy before scoring.

## Freeze this one bounded comparison

Let `g1(x)` and `g2(x)` be the displayed measured polylines for Offboard 1 and
Offboard 2. Use them unchanged in the published coordinates. Do not area-normalize
them, align peaks, rescale widths, fit a gain, refit the source model, or use the
black fit as a target. The use of each condition's independently specified
hover-normalizer is part of the published hypothesis being descriptively audited.

On the fixed visible interval `[0,3]`, report:

1. **Maximum absolute normalized deviation:**
   `max |g2(x) - g1(x)|`.
   This retains near-axis amplitude differences and is in the plotted normalized
   velocity units. It is not a percentage unless an additional denominator is
   explicitly declared; no such denominator is needed here.
2. **Radially weighted relative L2 discrepancy, with Offboard 2 as reference:**
   `sqrt[ integral x (g2-g1)^2 dx / integral x g2^2 dx ]`.
   Use the same interval for numerator and denominator. This is asymmetric and
   emphasizes larger radii, where cylindrical annuli have greater area. It is a
   profile discrepancy, not a measured thrust error or full momentum balance.
   The denominator must be positive and resolved. Fix this reference choice
   before extraction; do not switch references according to which score is smaller.
3. **Each profile's centerline-half-speed crossing(s):**
   solve the piecewise-linear curve for `g_j(x) = g_j(0)/2`, separately for each
   condition. Preserve multiple, missing, tangential or unresolved crossings as
   ambiguities. A unique outward crossing can be reported as a normalized
   centerline-half-speed radius. Do not silently select a convenient crossing,
   replace the centerline by a fitted peak, or infer an off-window crossing.

These are complementary descriptions of one comparison, not independent
confirmations. Max deviation retains differences that radial weighting can
suppress near the axis. The crossing diagnostic removes amplitude locally and
summarizes width, while the unchanged-profile metrics retain both amplitude and
shape. Crossing agreement alone cannot establish profile agreement.

Use the piecewise-linear path representation and the stated coordinate measure,
not equally weighted vector vertices: vertex density is a drawing property.
Freeze curve identity, axis mapping, clipping, interval and metric definitions
before comparison. Independent extraction by different PDF parsers is useful
verification of that representation, not a second physical experiment.

## Admission and bounded failure handling

Both measured polylines must have eligible, visible support across `[0,3]`.
Apply the actual plot clipping in both dimensions. Do not use off-canvas path
continuations, bridge missing regions, extrapolate tails, or silently shorten the
interval after seeing the residual. If full support is absent, report that the
prespecified interval is not admitted; do not manufacture a full-window score.

A half-speed diagnostic additionally requires an actually supported positive,
resolved `g_j(0)`. The first radial bin is not automatically the centerline. If
that prerequisite fails, mark that diagnostic unavailable with the reason; do not
substitute a model estimate. If the two full-window metrics are still admissible,
report them with this diagnostic omission clearly recorded.

The published profiles are finite spatial/statistical summaries. No assumption
that their drawing segments are new physical samples is permitted. The result
says nothing about omitted tails or other downstream stations. Same reported
frame size and propeller diameter do not establish identical hardware, and even
identical hardware would not by itself isolate all operating-condition effects.

## Uncertainty and the role of sensitivity

The latest coordinator protocol permits optional **graphical line-width
sensitivity only**. That is sufficient for a descriptive report if its limited
meaning is explicit. It is neither a physical confidence interval nor a
probability distribution over the true wake.

Any stroke-based perturbation must state how vertical and horizontal displacement,
axis registration and clipping are treated. For half-speed crossings, perturb the
centerline value and hence its half-speed threshold consistently with the same
curve perturbation. Keeping the threshold fixed while changing the centerline
would understate that diagnostic's graphical sensitivity.

Separate extraction reproducibility from physical uncertainty. Two parsers
agreeing establishes reproducible access to the same published drawing. It cannot
recover measurement calibration, run variation, geometry uncertainty, binning
uncertainty, median sampling uncertainty or hover-normalizer uncertainty.

The earlier proposal to combine an instrumental-accuracy envelope with the audit
is not required by the latest bounded protocol and is not added here. If the
coordinator nevertheless reports an instrument specification, identify its units
and the effects it covers; do not turn it into an unsupported total uncertainty
bound. Mean-plus/minus-standard-deviation bands are spread descriptions, not
confidence intervals for the median. Do not use them as SEM or divide by a square
root of sample count without justified effective counts and correlation handling.

No physical acceptance/rejection threshold, significance test, claimed confidence
level, or arbitrary percentage tolerance is warranted from this bounded audit.
A discrepancy robust to graphical sensitivity is only robust to that stated
sensitivity, not automatically physically significant.

## What the result can establish, and what to reject

A defensible outcome is a reproducible description of the distance between two
exposed measured curves under the source authors' fixed `r/l`, `U/U_H`
normalization, with finite-window width diagnostics where supported. This retains
more information than area-normalizing both profiles and avoids fitting target
amplitude. It can reveal a discrepancy that a common deterministic normalized
curve would need to accommodate. A small distance describes limited consistency.

**Reject stronger interpretations:**

- Independent, blind or held-out validation: these published conditions were
  exposed and contributed to the original modeling evidence.
- Validation of square-root effective-thrust scaling: `U_H` is calculated from
  prescribed hover quantities, not an independently measured thrust target.
  This audit is descriptive consistency with a hover normalization and cannot
  identify the exponent, causality or a command-to-thrust map.
- Proof that loading alone changes or preserves shape: hardware/control and
  environmental comparability have not been established as an intervention.
- Mean-field momentum closure or thrust identification from the median curves.
- Statistical physical rejection or practical adequacy without the necessary
  uncertainty and an application-specific accuracy tolerance.
- Generalization to other hardware, downstream stations, transients, unequal
  motors, powered receivers, aggregated wakes or a 5,000-drone simulation.

The conditional matched-load Wolf test remains scientifically stronger for a
later same-airframe shape question, but no admission work for it is requested
here. NASA HVAB near-wake/collective-pitch fields cannot substitute for this
far-field comparison or reject a conditional fixed-pitch far-field law. The
Busetto RPM/acceleration lead lacks spatial flow. A receiver-thrust/inflow test
addresses another module. Another analytic normalization would repeat numerical
accounting rather than this spatial observation.

## Connection to the full objective

The objective remains determining which mutual-aerodynamic approximations preserve
specified physical predictions while enabling genuinely local 3D drone flocks
within measured browser/WebGPU budgets, scaling toward 5,000 drones.

This audit contributes one small piece of observed source-field evidence. Its
bounded scope does not require a comprehensive source/receiver dataset before
making progress. It also does not discharge source amplitude/control mapping,
receiver forces and moments, aggregation, temporal behavior, trajectory accuracy,
local control, CPU/WebGPU equivalence, total cost or scale. The retained trajectory
and GPU/observer failures remain unchanged. Provisional numerical feasibility may
proceed only as assumed-model evidence until the relevant physical gates are met.
