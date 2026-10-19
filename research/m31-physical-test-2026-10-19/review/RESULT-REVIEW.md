# Saved physical-result interpretation review

19 October 2026. Reviewer: `/root/m31_protocol_challenge`.

**Accept this as a completed, no-fit descriptive empirical challenge with an observed discrepancy. It does not validate the current operational approximation, establish calibrated statistical rejection, or constitute a new physical discovery.** The comparison tests real published force measurements, while the independent audit verifies data binding and model arithmetic. These are distinct achievements.

I read only saved comparison, control, execution, audit and publication records. I did not decode the original MAT files anew, rerun either program, evaluate a new case, fit parameters or recompute the reported statistics. Values below are taken from those saved records. Only this review was written.

## What the saved comparison shows

The executed variant is `Kiran-stacked-projected-arm-fixedPWM-v1`, with the corrected figure-supported R = sqrt(2)l mapping. It uses the 11 preselected stacked separations 0.25–1.10 m, excluding the three closer near-domain cases. The discarded R = l interpretation was not tested against these forces.

| Prespecified quantity | Saved result |
|---|---:|
| Upper measured F/W at 0.25 m | 0.9163536076 |
| Upper measured F/W at 1.10 m | 0.9997614788 |
| Upper near-minus-far contrast | -0.0834078712 F/W |
| Model upper contrast | 0 |
| Approximate measured upper contrast in newtons | -0.0221031 N |
| Lower-force MAE across the 11 cases | 0.1019791556 F/W, approximately 0.0270245 N |
| Lower maximum absolute residual | 0.1771778334 F/W, approximately 0.0469521 N |

The upper contrast challenges the model's separation-independent upper response under the declared upright, fixed-input operation. It does not require identifying the far case as an isolated calibration. The saved correction threshold is 0.0834078712 F/W of differential error, or equal and opposing corrections of 0.0417039356 F/W per endpoint. These are deterministic reconciliation thresholds, not measured bias, error bars or probabilities. Unresolved measurement and setup effects must not be assumed smaller merely because the supplied SD fields are small.

The lower residual pattern adds useful physical information beyond the aggregate error. At 0.25 m, the measured value is 0.6942100 F/W versus the prediction 0.7508165: the nominal model underestimates the loss. At 0.70 m, the measured value has recovered to 0.9725187 while the prediction is 0.7953408; this case has the saved maximum absolute residual. At 1.10 m, the measurement is 0.9911450 versus the prediction 0.8318678. Thus the conditional model's thrust recovery with separation is slower than the recovery in these published mean values.

The saved finite sensitivity range at 0.70 m is 0.6970120–0.8958929 F/W, below the measured mean 0.9725187. This is a discrepancy with that particular prespecified set of illustrative input variations. It is not a rejection over every plausible input, a continuous uncertainty enclosure or an experimental coverage statement. Do not select a parameter combination from the exposed grid and present its agreement as an independent validation.

## What passed, and what remains limited

The saved evaluator and auditor supervisor records both report exit 0 without timeout, at approximately 0.035 s and 0.131 s respectively. The evaluator reports completed output of 235,014 bytes and passed registered controls. The saved independent audit reports all 11 nominal cases, 891 sensitivity cases, 44 selected observational words and 336 coordinate cells checked, with 43 source pins preserved. It uses separate decoding and 70-digit Decimal model arithmetic; its stated numerical tolerance is not an experimental uncertainty tolerance.

The result pin is SHA256 `61d81032b36aa9952bfea214269298ce82dd0c4fd6d68342a54812313966c0f9`. The saved publication receipt identifies source commit `dce1a2949aa425738ef9dbee7b8b1f0e0b378a03` and exact-public verification at 2026-10-19T03:06:06Z, before the registered run. This review reads those receipts; it does not repeat the audit or remote verification.

The experiment supports a discrepancy for the **combined fixed-PWM operational approximation**. The lower prediction assumes nominal total force F0 = W and equal nominal rotor forces; W is not an independently measured isolated-force baseline. Constant voltage/PWM does not establish constant electrical power, ideal power or RPM. The result cannot isolate the receiver cubic, wake profile, directed coupling or actuator approximation as the sole source of error. The primary upper invariance is a structural limitation of the supplied-input model, but the experiment does not separately resolve aerodynamic feedback from actuation/setup effects.

The archive contains aggregate means and spread fields, not the individual trial/time-series records for this endpoint. SD aggregation is unresolved. Calibration, differential tare/drift and full pose uncertainty remain unbounded by the available record, so there is no justified p-value, confidence interval or calibrated rejection. Approximate newtons use the paper's W approximately 0.265 N. MAE expressed in F/W is normalized force error, not a percentage accuracy score.

This is an already-exposed published dataset, using a retrieved archive version whose exact equivalence to the 2025 figure-generation version is not independently established. The result applies to this static homogeneous stacked pair and these separations. It establishes no dynamic, offset-moment, many-drone, trajectory, controller or general physical-accuracy claim. Improved numerical precision or faster evaluation does not supply the absent physical evidence.

## Best next research step

Obtain a focused calibrated static comparison at the already identified 0.25 m, 0.70 m and 1.10 m separations, together with independently measured isolated baselines for both vehicles at the same voltage/PWM. These positions address the upper contrast, the largest lower residual and far-separation recovery. Interleave isolated and paired conditions, vary their acquisition order, retain independent trial means, and document sensor calibration, tare/drift, mounting alignment and actual motor voltage/current/RPM. Set the next study's precision target prospectively to determine whether a contrast on the observed approximately 0.022 N scale is resolved.

That evidence would distinguish a reproducible upper interaction from differential setup error and constrain how fixed-PWM actuation changes with loading. It would also determine whether F0 = W explains part of the lower discrepancy. Use those measurements to choose and freeze the necessary model extension, then test it on new held-out configurations. This is a recommendation for a separately authorized study, not permission to rerun, tune or expand the completed checkpoint.

The useful present conclusion is: **the corrected, no-fit model has been compared with measured forces and shows a documented descriptive mismatch; it should not be presented as physically validated.** Preserve the negative result and its limits alongside the passed numerical audit.
