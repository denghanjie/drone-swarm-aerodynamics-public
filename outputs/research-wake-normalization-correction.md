# Wake length-scale correction — 12 October 2026

## Finding

The geometry diagram in [Bauersfeld et al., arXiv2403.13321v3, Fig.2](https://arxiv.org/pdf/2403.13321) defines the motor length across opposite rotor centers. The source was inspected as a rendered PDF; the schematic dimension spans the left and right opposing motors. The normalized distances in Eq.8 divide by this length. The published measurements concern near-hover flow; our 27g vehicle is below the measured mass range and remains an extrapolation.

Our four rotor centers are (±0.028, ±0.028) m. Opposite-motor length is 2√2×0.028 = 0.07919595949 m. The milestone27 coupling used adjacent spacing 2×0.028 = 0.056 m, inherited from the earlier illustrative pair model. That is a physical-parameter mapping error even though its numerical regression checks pass.

## Treatment of existing evidence

Milestone27 numerical sources and scheduled results are preserved, with an explicit warning. Its active-airflow results are an implementation-error record, not a correctly scaled application of the cited wake model. Its airflow-off branch is unaffected. Earlier illustrative aerodynamic pair results that used the same mapping must likewise not be treated as correctly normalized physical predictions. Airflow-off navigation/scaling results are unaffected.

Milestone28 reruns all25 matched cases with the corrected length only. No controller gains, seeds, doorways or thresholds change. The correction also changes the far-wake exclusion distance and radial wake width as required by the same formula. Updated geometry and analytic-profile checks replace a misleading regression against the old pair implementation. Source files are frozen before corrected mission outcomes.

These are paired correction runs, not a new independent test set. Mean-wake extrapolation, assumed receiver response, overlap heuristics and wall/ground omissions still preclude claims of aerodynamic accuracy. This correction does not calibrate the model.

## Trace

PDF retrieval: https://arxiv.org/pdf/2403.13321 (v3 indicated in PDF).
Local reference: `work/bauersfeld-2403.13321v3.pdf`; rendered page: `work/bauersfeld-page2.png`.
PDF SHA256: 81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c

## Historical viewer notices

The affected Step3B–3E, milestone1 and milestone2 pages now carry a correction banner. Their numerical source and recorded outcomes are unchanged, and copies of the pre-notice HTML are saved in `archive-before-normalization-notices/`. Milestone2’s separate reference-equation screening is not silently relabeled as corrected receiving-vehicle validation. Airflow-off navigation pages are unaffected.

## Execution decision

The original milestone27 study was terminated after all20 primary cases were saved. Five refinement/cadence cases remain uncompleted, with partial files retained. The full25-case corrected study28 was started directly; its frozen protocol is unchanged. See `milestone-27-termination.json`. This supersedes the earlier queue plan and avoids spending further computation on a verified implementation error.

## Corrected study completed

All25 corrected cases are now saved. The20 completed historical primary cases are paired in `milestone-28-correction-comparisons.json`; all five airflow-off outcomes are exact regressions. All four physics-step refinements pass, while the separate airflow-refresh comparison fails. The five original uncompleted refinements remain unpaired. See the final milestone28 report for outcomes and the explicit physical-validation limits.
