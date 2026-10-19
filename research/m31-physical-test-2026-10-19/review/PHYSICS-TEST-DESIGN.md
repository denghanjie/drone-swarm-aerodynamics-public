# Physical test design: a no-fit operational challenge

19 October 2026. Reviewer: `/root/m31_protocol_challenge`.

**A useful empirical test is feasible.** Use a separately named, hardware-matched variant of the current directed model to predict static upper and lower forces at the experiment's fixed voltage/PWM. Supply independently measured geometry and isolated-hover nominal force; freeze the remaining physics. Test this combined operational approximation against direct force measurements. Do not silently identify constant PWM with constant ideal power, and do not attribute a failure uniquely to the ideal-power-style receiver cubic.

The earlier `m31-upper-response-admission-2026-10-17/ADMISSION.md` correctly identifies the closest case as outside coverage, but its demand for complete exact 17-component experimental states is too strong for this empirical purpose. Nominal static poses with documented tolerances are sufficient. Unknown velocity words can be set to the declared static representative values because this model does not use them in its physics. Measurement uncertainty must be represented; microscopic state reconstruction is unnecessary.

This is a test design, not an executed physical result. I read the earlier compatibility NOTE and upper-response ADMISSION, their provenance, and the retained Kiran v1 methods/captions. No numerical model, digitizer, codec, fit or checker was executed; no new source was acquired. Only this review was written.

## Hypothesis and hardware mapping

Name the variant explicitly, for example `Kiran-Crazyflie-static-fixedPWM-v1`. The operational hypothesis is: at the published constant 4 V and hover PWM, the current memoryless directed field plus receiver law, supplied with each vehicle's isolated-hover nominal force, predicts its measured mean axial force when another vehicle is placed at the specified static separation.

The test jointly challenges the aerodynamic field, directed coupling, receiver law, simplified geometry/load map and the use of fixed isolated nominal force under loaded fixed-PWM operation. RPM or electrical power may change under interaction; that is part of what this operational approximation neglects, not a reason to equate PWM with ideal power or evade testing it. Do not fit an actuator correction to the interaction forces afterward.

| Input | Predeclared treatment |
|---|---|
| Motor layout | Published body-center-to-motor distance is l = 32.5 mm. In the current square-corner convention set `arm = l/sqrt(2)`, so R = l and D = 2l. D is not propeller diameter. Confirm the physical yaw/layout from the apparatus figure or metadata. |
| Propeller radius and other geometry | Use direct apparatus metadata or independently sourced hardware dimensions, with explicit uncertainty where needed. Never tune these to the force curves. Preserve old frozen simulation constants in their own package. |
| Static pose | Nominal stage coordinates and upright axes, with bounds for stage accuracy, center/reference-plane offset, mounting alignment, tilt and yaw. The stated 100 μm stage accuracy is not a complete bound on vehicle attitude or rotor-plane location. |
| Nominal rotor force | Prefer each vehicle's own independently measured isolated force at the same voltage, PWM and mounting; use total/4 as an explicitly declared symmetry approximation if individual forces are unavailable. Do not infer unequal rotor forces from interaction moments. |
| Weight normalization | The paper plots force/W, W approximately 0.265 N. Weight is not automatically an exact isolated transducer reading. Predict and compare in the same normalization; propagate baseline/weight uncertainty. |
| Remaining model | Freeze wake constants, source closure, support, receiver cubic and load mapping. No interaction-data fitting, result-driven parameter choice or coefficient rescaling. |

The geometry change makes the nominal near-height cutoff `2.5D = 5l`. The published closest `Δz/l = 4` case remains excluded for the usual stacked or modest-offset arrangement; changing hardware geometry does not admit it. Select a documented grid point whose entire plausible pose/geometry range is admitted, such as a point at or above 6l if that point exists and its uncertainty clears the gate. Check the actual rotor-point geometry and whole-query contract, not center separation alone. Domain exclusion is a coverage result, not a predicted force error.

## Cases and observables

Select cases from geometry/metadata before extracting their force values. Prefer the stacked `Δx/l = 0` and offset `Δx/l = 2` configurations, using all available static vertical coordinates in those slices that robustly clear the model's domain. If those exact slices are unavailable, freeze a documented replacement selection before reading their numerical outcomes; do not interpolate an apparent point from an unlabeled surface. Retain the complete candidate/exclusion list. The prose's horizontal range conflicts with the stacked/2l examples, so use jointly identified figure axes or raw case metadata rather than inventing a hidden case table.

Use axial mean force as the primary observable. Compare total force with total force, or subtract the matching isolated baseline from both model and measurement. Respect transducer signs and the distinction between upper A and lower B. Pitch moment is a secondary endpoint only when reference point, axes and baseline are identified. Do not turn an SD/unsteadiness panel into a mean-force observation.

The smallest sharp test is the **upper mean interaction response**. For a robustly upright isolated pair with the lower source upstream-excluded for the upper receiver, the model predicts exactly the upper isolated baseline, independent of lower position. A resolved change at an admitted separation rejects that operational null even without a complicated lower-force fit.

If no independent isolated transducer baseline is available, a useful primary fallback is the **difference of upper mean force between two preselected admitted separations**, under identical voltage/PWM and mounting. The model predicts zero difference. Select the nearest robustly admitted stacked point and the farthest documented point in the same slice by geometry, not by force magnitude. This contrast can cancel a common additive tare and does not require asserting that `F_upper/W = 1`. It remains vulnerable to differential drift or changed setup, which must be bounded. Do not call the far point an isolated measurement unless the source establishes that fact.

Report the lower-force comparison at every selected case as well. It tests whether the field/cubic combination captures actual loss magnitude and its separation dependence. Upper disagreement is already sufficient to reject a universal upper-and-lower prediction claim for these operations; lower agreement cannot cancel it. Conversely, an unresolved upper difference is not validation of the lower law.

## Raw-data route and figure route

The primary article explicitly links the Brown dataset at [DOI 10.26300/64d4-wa17](https://doi.org/10.26300/64d4-wa17). The old access failure does not establish current unavailability. If direct force records and case metadata are accessible, they are preferable to inferred flight residuals or firmware motor labels. This reviewer has not established that the archive actually exposes all required channels/baselines.

With raw static force records, preserve the published case identities and repetitions. Define the steady averaging window from apparatus metadata before comparing predictions; retain all declared repeats and report any excluded transient window. The stated acquisition is 20 kHz for 30 seconds, repeated three times. Those hundreds of thousands of serial samples are not independent experimental replications. Base repeatability uncertainty on trial-level summaries, accounting for within-record dependence when estimating each mean. If using a three-repeat t interval, identify its independence/normality assumptions; it is not a distribution-free guarantee. Use one preselected primary contrast, or predeclare multiplicity control for a grid-wide rejection. Report other endpoints descriptively.

Published Figs. 5(a) and 6(a) can support a **no-fit descriptive interval comparison** if joint coordinates, normalization and color/axis scale can be read. This is a real physical challenge, not merely another admission audit. Before digitization, freeze source version/resolution, selected coordinates, axis/color calibration, handling of interpolation, and the interval extraction rule. Include full pixel/bin width, anti-aliasing or color ambiguity, axis localization and rounding; retain unresolved cells instead of selecting cleaner-looking outcomes. A plotted interpolated surface is not a new independent measurement at every pixel. Use intervals and sensible precision, not invented raw-data digits.

Figs. 5/6 explicitly label their SD panels as **unsteadiness**. The methods say standard deviation was computed from the repeated trials, but this does not by itself identify those panels as confidence intervals for the mean, establish sample independence, or bound calibration/tare error. Do not divide that SD by the square root of 600,000, assign it a 95% interpretation, or treat it as the total measurement uncertainty.

These papers are already exposed evidence. The resulting challenge is no-fit and prospectively specified from this point onward; it is not a blind or newly unseen holdout validation.

## Uncertainty and decision rules to freeze before evaluation

Separate these quantities rather than hiding all disagreement in an adjustable “model uncertainty”:

1. **Input uncertainty:** measured geometry/pose, propeller dimensions, isolated force and normalization. Use a justified interval or a finite, prespecified sensitivity set. Label a sampled sensitivity envelope honestly; endpoint sampling does not automatically prove a nonlinear global enclosure. The upper-zero structural null can often be bounded analytically over the plausible pose set.
2. **Observation uncertainty:** repeat-mean variability and dependence; sensor calibration/cross-talk/resolution at the applicable range; tare and differential drift; gravity/axis transformation; isolated-baseline uncertainty/covariance; figure extraction and interpolation if used. Shared scale/tare errors may cancel in a contrast only when the acquisition supports that assumption. Unknown terms are unknown, not zero.
3. **Operational approximation error:** loaded-PWM behavior, missing upper interaction and receiver-law misspecification belong to the hypothesis being tested. Do not grant them arbitrary adjustable bounds that guarantee agreement.

Predeclare one of the following evidence levels, with a result table containing coordinates, admitted status, measured interval, prediction/input envelope, signed residual interval and decision:

- **Resolved operational rejection:** at an admitted primary case/contrast, the observation interval including justified statistical and systematic uncertainty is disjoint from the model prediction/input envelope. State the inferential assumptions and any multiplicity rule. Reject the combined operational approximation in this case; do not isolate the ideal-power law as the sole cause.
- **Figure-level discrepancy with explicit robustness:** when digitization is bounded but some systematic uncertainty is unreported, report whether plotted-mean intervals and prediction envelopes overlap, and the minimum additional differential bias needed to reconcile them. State the conclusion conditionally on that missing bias being smaller than the reported margin. Do not manufacture a calibrated confidence level. This still yields concrete physical evidence and identifies what uncertainty could change the result.
- **No resolved discrepancy on the tested cases:** overlap means this test did not reject the approximation at its stated resolution. Quantitative adequacy requires a separately predeclared useful error tolerance with sufficiently narrow uncertainty; overlap alone is not proof of accuracy.

Do not choose a physical tolerance after seeing residuals. If no external application tolerance exists, publish normalized/absolute error intervals and their coverage rather than a retrospective accuracy pass. If the available figures cannot establish a baseline, calibrated interval or raw case grid, complete the narrower identifiable contrast and report its actual limitation instead of claiming broad physical validation or stopping with an access-only report.

## Minimal defensible final claim

“We tested an explicitly hardware-matched, fixed-PWM operational approximation of the current directed model, without fitting to the interaction measurements, against published static upper/lower force evidence at the listed admitted separations. The table reports its measured discrepancies and uncertainty. The result applies to these vehicles, actuation, apparatus and static cases.”

A resolved failure is scientifically useful and can finish this checkpoint. A successful limited comparison supports only this restricted operating envelope. Neither outcome establishes moving-wake fidelity, trajectory/controller performance, general mutual aerodynamics, many-drone accuracy or a separately validated ideal-power law.

Primary source: Kiran, Ayanian and Breuer, *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, RSS 2025, [DOI 10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102); retained body [arXiv:2507.09463v1](https://arxiv.org/html/2507.09463v1), §II-A/II-A1, Figs. 3/5/6, §III-A, dataset footnote. Earlier local source pins and structural deductions are in the compatibility NOTE and upper-response ADMISSION/READ-RECEIPT. No quantitative figure claim was extracted in this review.
