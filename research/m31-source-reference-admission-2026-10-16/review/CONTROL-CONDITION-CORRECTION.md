# Additive correction: receiver control condition

2026-10-16. This corrects the next-experiment recommendation in `REVIEW.md`;
that original record is retained unchanged. The profile-result interpretation is
unchanged. **The original fixed-RPM proposal omitted a necessary control mapping
and must not be read as direct qualification of the frozen M28 receiver law.**

## Existing definitions inspected

Read only:

- `research/m31-browser-receiver-2026-10-16/source/reference.cjs`, especially
  `solveAlpha` and `powerRatio`.
- `research/m31-browser-receiver-2026-10-16/PROTOCOL.md`, including its definition
  of represented/original ideal power and its shaft/electrical-power disclaimer.
- `outputs/milestone-28-source/aero.cjs`, especially `idealPower`,
  `effectiveThrust` and the nominal actuator-state derivative.
- `research/m31-omission-ablation-2026-10-16/physical-compatibility-review.md`.

All paths are under
`[repository root]`.
No source edits, numerical evaluation, scientific execution, new acquisition or
data requests occurred.

## What is fixed in this law

The source uses nominal rotor thrust `f0`, not RPM, as its actuator state. At
fixed nominal state it defines `vi0 = sqrt(f0/(2 rho A))`, `alpha = U/vi0`,
`T = f0*x`, and solves `x^3 + alpha*x - 1 = 0`.

The retained source/protocol identity is

`P*(T,U) = T[U/2 + sqrt(U^2/4 + T/(2 rho A))] = f0*vi0`.

Thus the held quantity is the model's **ideal actuator-disk power**, including
the throughflow term `T*U`. It is not merely the induced contribution `T*vi`.
The source contains no independently identified mapping that makes this ideal
quantity equal to measured shaft or electrical power.

| Condition | What it fixes | Why it does not establish the frozen condition |
|---|---|---|
| Fixed RPM | Measured angular speed | Torque, shaft power and ideal disk power may change with inflow. |
| Fixed shaft power | Measured torque times angular speed | Profile, swirl and other losses require a separate mapping to `P*`; fixed shaft power does not establish fixed `P*`. |
| Fixed electrical power or throttle | An electrical input or command | Drive efficiency and aerodynamic loading may vary; neither shaft nor ideal disk power is thereby fixed. |
| Fixed model `f0` | Nominal thrust state and its model-implied `f0*vi0` | The code enforces the ideal-power identity; its relation to a real motor/ESC control remains to be established. |

The last row is a mathematical model condition, not an already demonstrated
laboratory control mode. A held real command is also not automatically equivalent
to fixed model `f0`; it needs an explicit, independently specified bridge.

## Corrected single next path for the current-law question

Replace the original fixed-RPM qualification suggestion with a **steady,
documented fixed-command receiver transfer, conditional on an explicit
command-to-nominal-thrust bridge**. Retain its small zero-plus-two-nonzero-inflow
design. This is the sole next path recommended here for challenging the current
receiver implementation plus that bridge.

For one identified rotor/drive and one documented hardware command `c`, determine
the matched zero-external-inflow baseline independently and set the proposed
mapping `f0 = T0(c)` before examining either nonzero-inflow target. Declare that
mapping as a physical hypothesis added to the source, not something the source
has established. Keep the same real command at both admitted inflows, allow RPM
to respond, and compare directly measured steady thrust with the frozen cubic
prediction at that fixed `f0`. Do not recalibrate `f0` from each target thrust.
Hardware, inflow sign, positive-thrust operating domain and baseline compatibility
must remain explicit. Different hardware qualifies only that declared transfer,
not the original 46 mm rotor representation.

If RPM, torque, voltage or current are available, use them as diagnostics of the
actuation/power bridge. They do not replace measured thrust, and their use must
not assume shaft-power/ideal-power equivalence. Do not servo the apparatus to hold
`P*` inferred from its measured thrust and then claim that the resulting constancy
independently validates the same equation. The primary target is the independently
measured thrust at a declared real control condition.

A discrepancy challenges the frozen receiver law **together with the explicit
control mapping**; without further evidence it cannot uniquely identify which
part failed. Agreement supports only that finite hardware/control/inflow
comparison. If the bridge cannot be specified, a direct physical qualification of
the unchanged current law is not yet well-defined.

The retained fixed-RPM proposal remains scientifically meaningful only as an
**explicit alternative-model transfer to fixed-RPM operation**. It is not the
selected direct-current-law path in this correction, and it cannot be relabeled
as constant shaft-power or constant ideal-power validation.

No experiment is authorized or run by this correction. Its purpose is to prevent
a control-condition substitution in the next-step record, while preserving the
original recommendation and the full source/receiver and 5,000-drone objectives.
