# Final interpretation review and one next experiment path

2026-10-16. Read-only review of `PROFILE-PROTOCOL.md`, the updated
`analyze_profiles.py`, and saved `results/result.json` under
`research/m31-source-reference-admission-2026-10-16`.
The result records source commit
`37750e0ea4d929ac7bb414a7636cfebaea3f3c2a`, analysis-source SHA-256
`ac5f392eff6a129180af6fd111fcda5ec1d6b8ad787d760321621a229d28e926`, and input
SHA-256 `967618633c59a1786cbe6a811e2c96cb213b8b2119525816f2206e9775d19509`.
These identifiers are quoted from the saved result, not independently rehashed
here. No scientific comparison was executed or recomputed, no new evidence was
acquired, and no public file was edited.

## Interpretation verdict

The proposed descriptive conclusion is supported by the saved record, with one
essential wording correction: **normalized centerline median speeds** nearly
coincide. The plotted quantity is `U/U_H`, and the two conditions use different
hover-normalizers. Saying only “center speeds nearly coincide” can incorrectly
suggest that their dimensional velocities agree.

Suggested final wording:

> At `s/l = 3`, the two published normalized centerline medians are close
> (`U/U_H` about 1.155 and 1.157), while their radial profiles differ. The maximum
> normalized deviation is 0.258, the radially weighted relative L2 discrepancy
> referenced to Offboard 2 is 0.241, and the unique downward half-centerline
> crossings occur at `r/l` about 0.449 and 0.559. A normalized centerline check
> alone therefore misses differences across the displayed profile.

All numbers in that wording are rounded from the saved result. The audit concerns
the published binned-median polylines, the finite radial window `0 <= r/l <= 3`,
and one downstream station. Reporting fewer digits in prose avoids suggesting
that the many reconstruction digits are experimental precision.

The result records maximum deviation at `r/l = 0.38095222496350567`, so the
largest displayed discrepancy is off axis. Both reported half-speed intersections
are classified downward, unique, and without plateau intervals. Their comparison
describes this plotted width statistic, not every aspect of wake geometry.

“Close” is descriptive proximity in the normalized graph. It is not physical
equivalence, statistical agreement, validation of centerline scaling, or adequacy
for a receiver model. Conversely, the off-axis discrepancy is not a demonstrated
causal load effect, significance result, rejection of an entire source law, or
proof that an added shape parameter is necessary for the eventual application.
The L2 number is an asymmetric profile norm; do not call it a thrust error,
percentage error at every location, mean absolute error, or accuracy score.

The updated analyzer now verifies source identity, axes, profile order and finite
strictly increasing knots; it classifies tangency/endpoint cases separately from
downward crossings. The saved scope now says “same tabulated frame-dimension
hover pair.” These address the previous review's identified concerns. This is a
static confirmation of the changes, not an independent arithmetic reproduction
of the results or of the promised quadrature check.

## Exactly one next useful experiment path

**A controlled receiver-thrust transfer at fixed measured RPM: one rotor,
zero imposed axial inflow, and two predeclared nonzero axial-inflow conditions.**

This next path moves from displayed flow-profile disagreement to a directly
measured response quantity. The present median speed magnitude is insufficient
to identify the signed axial inflow or thrust response of a receiving rotor.
Separately controlling the imposed inflow avoids inferring it from this source
model and avoids reconstructing thrust from a scalar flow integral.

Use one documented receiver rotor geometry at one measured RPM. Hold the hardware
and control mode fixed, establish the external axial-inflow sign convention, and
require known approximately uniform inflow over the disk. Choose the two nonzero
conditions from the admitted operating envelope before inspecting their force
values. Measure axial rotor thrust directly, with tare/background treatment and
force/inflow uncertainty appropriate to the finite comparison.

The zero-inflow condition supplies the baseline `T0`. Predict both nonzero
conditions using a receiver-response rule frozen beforehand and compare the
directly measured ratio `T(v)/T0` with that prediction. Using the zero-inflow
baseline for one amplitude is legitimate calibration; fitting a response gain or
inflow parameter on either target and then counting that target as validation
would be circular. Shared baseline uncertainty must propagate to both ratios.
Fixed RPM isolates an aerodynamic response; it does not validate motor-command,
power-supply or speed-controller dynamics.

This is a modest three-condition receiver experiment, not a requirement for a
complete physical swarm dataset. Suitable published data can be used if they
document the same rotor, RPM, inflow and force statistic across conditions. Do not
silently combine static thrust from one rotor/run with dynamic thrust from
another. The earlier UIUC hardware/control compatibility concern remains until
such admission is actually established. A reference rotor can qualify only its
matching configured receiver model; it does not automatically qualify a different
27 g vehicle. If admissible observations are absent, report that limitation before
authorizing execution, rather than substituting a force reconstructed from flow.

This review recommends the path only. It does not establish that the observations
are in hand, acquire them, freeze an implementation, allocate a run, or approve
execution. Source actuator mapping, nonuniform/turbulent wake reception,
aggregation, moments, transients and coupled dynamics remain separate gates.

The full objective remains preserving specified mutual-aerodynamic predictions
while enabling genuinely local 3D drone flocks within measured browser/WebGPU
budgets toward 5,000 drones. This direct receiver observable can eventually connect
flow approximations to force error; it establishes neither the current source
law nor the final accuracy/computation trade-off on its own.
