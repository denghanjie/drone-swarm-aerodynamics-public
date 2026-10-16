# Next decision: establish the command-to-thrust bridge

Decision: close the exposed GWS transfer as development evidence. Do not fit its baseline, replace its rows, or infer shaft-power efficiency to improve agreement. This is a new planning decision, not an empirical result or an allocated experiment.

The receiver equation assumes constant ideal actuator-disk power, including throughflow. A physical motor command does not automatically impose that condition. The hypothesis to test next is the equation plus an explicit mapping `f0 = T0(c)`, where `c` is one identified, documented drive command and `T0(c)` is independently measured zero-external-inflow thrust. A mismatch initially challenges both together.

## Evidence admission before any target scoring

Identify the rotor, drive, command definition and operating limits. Diameter alone is insufficient. A compatible published reference must document the actual held command, external inflow and direct thrust, and associate the baseline and target measurements with the same hardware/control setting. RPM control, shaft-power control, PWM and throttle must retain their actual meanings. A fixed-RPM transfer may be studied explicitly but cannot silently stand in for another control.

Select the source and obtain reuse terms before reading fresh target values where possible. Log previous exposure. Verify primary-source bibliographic details and the passages establishing control, geometry, calibration and uncertainty. Existing GWS data do not supply a fresh confirmation of this hypothesis. No compatible original-receiver reference has yet been admitted.

## Minimal prospective design

Use one zero-inflow baseline and two nonzero axial inflows chosen from documented application conditions before their thrust outcomes are inspected. Hold the same real command. Freeze baseline estimation, model parameters, domain, comparison metrics and failure handling before calculating targets. Obtain repeated measurements and a justified uncertainty model; two inflow levels alone do not provide statistical replication. Required repeats and tolerances remain unset until measurement precision and the intended prediction budget are known.

Primary observable: steady thrust discrepancy in newtons, with absolute and baseline-normalized values kept together. Compare against the declared receiver prediction and an unchanged-static-thrust baseline under matched inputs. Keep every admitted target, including sign or domain failures. Separate sensor/calibration uncertainty, baseline uncertainty, numerical error and model discrepancy. If the data cannot support uncertainty propagation, limit the result to descriptive differences.

RPM, torque, voltage and current can help diagnose a mismatch if available. They are not a substitute for direct thrust. Do not adjust command to force ideal power using target thrust, infer a new `f0` separately at each inflow, or tune the law to those targets. Uniform steady axial inflow would still leave nonuniform wakes, moments, dynamics and interactions among rotors unqualified.

## Decision and stopping rule

First perform a finite source-admission review of an identified candidate, not an open-ended parameter sweep. If no compatible evidence can be admitted, save that specific gap and keep physical qualification unresolved. A physical experiment would then require equipment/access that is not currently established; do not purchase, contact authors, or invent measurements. Independently scoped computational research can continue with explicitly assumed physics.

If evidence is admitted, create a separate preregistered protocol with numeric conditions, uncertainty handling, accuracy allocation, matched baselines and compute limits. Publish and verify it before scoring. Success would support only the tested rotor/command/inflow scope; it would not settle the 5,000-drone objective. There is no new scientific invocation or source acquisition authorized by this planning file.

Basis: [GWS results](results/aggregate.json), [independent interpretation](review/INTERPRETATION.md), and the [control-condition correction](../m31-source-reference-admission-2026-10-16/review/CONTROL-CONDITION-CORRECTION.md). No new external citation or empirical claim is introduced here.
