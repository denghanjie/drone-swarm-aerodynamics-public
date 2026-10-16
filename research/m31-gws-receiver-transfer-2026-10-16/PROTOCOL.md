# GWS receiver transfer: exposed-data descriptive test

Saved before scoring. This is a new, separately bounded test of an explicitly transferred equation plus a control mapping. It does not reopen any completed campaign. All 14 target records were exposed in previous source inspection; no blind confirmation is claimed.

## Question and hypothesis

How does the existing ideal actuator-disk thrust-loss curve compare with a published small-propeller axial-inflow run when we explicitly map its nominal thrust to a zero-inflow, prescribed-RPM baseline?

The current receiver solves x³+αx−1=0 at constant nominal f0 and therefore constant model-defined ideal actuator-disk power, including throughflow. Prescribed RPM does not establish this power condition. Our added hypothesis is f0=T0(c), where c is the published nominal/prescribed-speed run label, 15030 RPM. The following is a nominal-speed coefficient transfer of the law plus that bridge. It cannot isolate an error in the equation from an error in the bridge, and does not reconstruct exact dimensional forces without per-row RPM/density.

For baseline C0, use α=J sqrt(π/(2 C0)), solve the unique positive root x, and predict CT_hat=C0 x. This follows from the published CT=T/(ρn²D⁴), J=U/(nD), and disk area πD²/4. No shaft-power equivalence, dimensional atmosphere or rotor-RPM history is invented. The true diameter is reported as 2.55 inches, but no dimensional conversion is required in this test. No measured power coefficient is used to fit or validate ideal power.

## Fixed source selection and baseline

Use the existing UIUC GWS Direct Drive 2.5×0.8 first specimen block's entire 0503rd/15030 axial file (14 rows), and the associated 0500rd static file (24 rows). Source hashes and URLs are pinned in config.json. The published database groups these files together, separately from specimens 2 and 3; this is database association, not an independently inspected specimen log. No new file acquisition, run substitution, inflow selection or fitting.

Find the nearest strictly lower and higher static RPM around 15030 by RPM value, not file order: the static file is not completely sorted. They must be data rows 13/14 at 15006.667 and 15960.000 RPM, CT 0.061549/0.062855. Require exactly these known anchors and positive finite coefficients. There is no exactly matched static row. Three scenarios, fixed before calculation:

1. Linear CT interpolation in RPM between those anchors at 15030.
2. Use the lower-RPM anchor CT unchanged.
3. Use the higher-RPM anchor CT unchanged.

Recompute α, root, CT prediction and every normalized metric for each scenario. The two endpoint scenarios describe baseline-choice sensitivity only; they are not uncertainty bounds or confidence intervals. Do not select the best scenario after scoring.

## Metrics and numerical verification

Signed residual e_i=CT_hat_i−CT_reported_i. Preserve all 14 rows and row numbering, including CT≤0. Primary summaries for each scenario: maximum |e| and all maximizing row IDs; unweighted RMS sqrt(mean(e²)); both quantities divided by that scenario's positive C0. This weights reported run conditions equally; it is not a continuous-inflow integral or a mean pointwise percentage error. Report signed mean residual as a direction diagnostic.

Also report the same explicitly secondary summaries for rows with reported CT>0, and their exact count and row IDs. CT≤0 rows remain visible in the complete private evidence and are counted publicly as outside the model's representable positive-thrust branch. Do not silently delete them or call them a falsification under the original ideal-power control. No residual-based membership rule, tuning, rejection cutoff, statistical test, or physical adequacy threshold.

Use standard-library binary64 bisection on x∈[0,1], up to 96 iterations, with a positive-domain sign bracket and stop width≤2e-15. Require each reported cubic residual≤1e-12 and 0<x≤1. Save original operands, bracket, iteration count and prediction. Unit checks before real scoring: zero inflow identity, synthetic roots with known α, interpolation with unsorted synthetic rows, and exact constant-vector max/RMS. Independently review saved outcomes using a different root formula or method, not importing this analyzer. Separate numerical reconstruction tolerances from unavailable measurement uncertainty.

One finite scoring invocation, expected 42 roots, max 4032 bisection iterations. Local execution cap 15 seconds and 256 KiB output. No benchmark, new CFD, GPU or simulation invocation. If an implementation fault occurs, preserve the failed output and record a versioned correction; never change the selected evidence or metrics to improve agreement.

## Evidence and reporting boundaries

Primary source: Deters, Ananda and Selig, *Reynolds Number Effects on the Performance of Small-Scale Propellers*, AIAA 2014-2151, DOI 10.2514/6.2014-2151, §§II-A–E pp. 2–5; UIUC Propeller Database Volume 2, first GWS 2.5×0.8 block. Measured thrust uses a load-cell balance; RPM is measured separately before loads. Methods describe calibration and flow corrections, but total uncertainty and per-row raw data are unavailable. Published J and CT errors need not be independent because tunnel corrections use thrust. A ≤1% calibration-slope statement is not a total uncertainty bound.

Publish our protocol, code, source URLs/hashes and aggregate discrepancy/sensitivity results with attribution. Keep original files/PDF and the complete per-row derived table private; no dataset redistribution license has been established. The public viewer may plot aggregate metrics and model-only curves, clearly distinguished from individual observations. Public summary must contain no per-row predictor/residual pairs reconstructing the entire source table. Reproduction requires the cited inputs from their official source. Record a SHA-256 of retained private row evidence and let the independent reviewer examine it locally.

The numerical result is descriptive evidence about an exposed, reduced coefficient table. It cannot qualify the original 46 mm vehicle, fixed PWM, motor time constants, moments, nonuniform wake reception, multiple wakes, or 5,000 drones. It is not a novelty result. No scientific adequacy or statistical claim is possible from this test alone.

## Completion

Publish source/protocol before scoring. Save all outputs, review, limitations, literature/claim ledgers and a clear Three.js milestone view tied to public aggregate results. Preserve previous source/profile checkpoints unchanged. Close this campaign after the finite analysis and review; decide the next experiment from its evidence rather than adding more exposed rows.
