# GWS exposed coefficient-transfer design review

2026-10-16. Design scrutiny only; no target scoring, root solving, browsing, new
acquisition or public edits. The protocol specification came from the coordinator.
Existing local `physical-data-followup.md` and the previously read
`physical-compatibility-review.md` under
`[repository root]/research/m31-omission-ablation-2026-10-16`
provide the retained methods/compatibility context. No raw coefficient file was
opened in this review. The baseline row identities/values and file provenance
still require the coordinator's frozen input admission; they were not independently
verified here.

## Verdict

**Useful and admissible as a separately declared, exposed, descriptive
coefficient-level transfer of a law plus a nominal-RPM baseline bridge.** It is
the alternative transfer allowed by the preceding control-condition correction,
not direct physical qualification of the unchanged M28 receiver.

The finite question is whether the constant-ideal-disk-power thrust curve, when
given the explicit bridge `f0 = T0(RPM-setpoint)`, describes the reported GWS
specimen-1 advancing-flow coefficients. This tests the combined transfer
hypothesis. It does not establish that fixed RPM physically maintains constant
ideal power, shaft power, electrical power or the original model's nominal state.
An exposed discrepancy can be informative without an adequacy/significance
threshold, provided it remains a descriptive discrepancy.

## Formula and control interpretation

The proposed formulas are consistent with the retained UIUC conventions
`CT = T/(rho*n^2*D^4)` and `J = V/(n*D)`, with rotor disk area `pi*D^2/4`:

`alpha = J*sqrt(pi/(2*CT0))`,
`x^3 + alpha*x - 1 = 0`,
`CT_hat = CT0*x`.

No dimensional density, thrust reconstruction or replacement diameter is needed
to make this coefficient comparison. That cancellation does not erase Reynolds,
geometry, control or baseline mismatch. Do not substitute motor spacing for rotor
diameter or reinterpret the coefficient table as measured nanoquad receiver data.

Describe 15030 RPM as the published nominal/prescribed-RPM run label. The released
`J, CT, CP, eta` table is not per-row RPM telemetry. The bridge assumes that the
static baseline at that label is applicable across the target run. Retained
methods report RPM sensing and prescribed-RPM operation, but their reported
sampling-period speed stability is not a bound on every point's deviation from
the nominal setpoint, nor total force uncertainty.

Source-file hashes, the source-index association of the static and dynamic files
with specimen 1, coefficient conventions, the exact two adjacent static rows,
the 14 target rows and their order should be fixed from the retained evidence.
This can be done within the existing admission record; it does not require broader
acquisition. Stop on an actual mismatch rather than repairing or replacing rows.

## Baseline scenarios

Linear interpolation of static `CT` against RPM, using the declared adjacent
15006.667 and 15960 RPM rows at nominal 15030 RPM, is a reproducible baseline
choice. State explicitly that it is interpolation of **CT**, not thrust, power,
log RPM or another variable. The targets do not choose the interpolation rule.
It does not independently validate a linear Reynolds dependence or guarantee the
true static baseline.

Use the two endpoint CT values as two additional deterministic baseline-choice
scenarios. For each scenario, recompute **alpha, the root and CT_hat**, then every
residual and aggregate; divide its relative metrics by that same scenario's CT0.
Merely dividing the primary residuals by another denominator would not test the
baseline choice, since CT0 enters the prediction itself.

Report the primary and both endpoint scenarios side by side. These are three
evaluations of the same exposed targets, not independent experimental replicates.
Do not pick the best-scoring baseline. The endpoint values are not confidence
limits, a total uncertainty budget, or a guaranteed bracket for the physically
correct baseline; no unsupported uncertainty propagation should be inferred.

## Finite metrics and row treatment

The proposed all-14-row maximum absolute CT discrepancy and RMS CT discrepancy,
each also divided by the scenario CT0, are sufficient. Define the signed residual
once, preferably `e_i = CT_hat_i - CT_i`, and retain every signed row residual.
Then the aggregate definitions are `max |e_i|`, `sqrt(sum e_i^2 / 14)`, and each
divided by CT0. RMS gives each released operating point equal weight; it is not
an integral over advance ratio, an experimental standard deviation, a confidence
measure or a flight-error distribution. Record the row/J attaining the maximum,
including numerical ties.

Baseline-normalized errors are fractions of the positive static CT0, not relative
errors against each measured CT. Do not divide by measured CT near zero, use MAPE,
or interpret baseline-normalized RMS as an error percentage at every inflow.
Always retain the absolute-coefficient metrics alongside normalized ones.

Tag reported positive versus nonpositive target CT in the row table. With positive
CT0 and nonnegative J, this model's selected root yields positive CT_hat. It cannot
represent a reported nonpositive target, irrespective of baseline tuning. Keep
those rows and residuals in the primary 14-row summary; do not clip targets or
predictions, omit rows or silently reduce the domain. Call this a limitation of
the positive-thrust branch in the declared full-run transfer, not proof of failure
under the original actuator condition. Uncertainty about near-zero measured signs
remains unavailable; reported sign and physical significance are separate claims.

The full-run metrics combine mismatch on positive-thrust rows with this known
sign-representation limitation. They must not be presented as an isolated estimate
of accuracy within the positive-thrust regime. The per-row table supplies this
distinction without adding another selected metric or altering the primary scope.

Require positive finite CT0, finite admitted J >= 0, and the unique physical
root in `(0,1]` for the allocated domain. Numerical root checks concern computation
only. They are not physical adequacy thresholds. A calibrated zero-inflow identity
is not an additional successful target observation.

## Claims and stopping boundary

Supported: a reproducible, finite, exposed comparison of this specified
constant-ideal-power curve plus nominal-RPM baseline bridge with the selected GWS
coefficient run, and its sensitivity to the two declared baseline substitutions.
The comparison can show where that transfer departs from the reported values.

Unsupported: original-control M28/Crazyflie qualification or falsification;
fixed-RPM/shaft-power/ideal-power equivalence; total experimental uncertainty or
statistical significance; acceptance without a purpose-specific tolerance;
independent held-out confirmation; novelty; transient or nonuniform-wake receiver
response; receiver moments; source superposition; or the 5,000-drone
accuracy/computation claim.

No extra power analysis, CP fitting, source-profile experiment or expanded dataset
is needed for this declared question. CP remains a separate measured coefficient
unless a future explicitly defined power diagnostic is selected. Preserve the
retained data attribution/reuse limitations rather than applying the repository's
license to the original dataset. This design review neither scores the experiment
nor allocates or authorizes its execution.
