# Saved-result review: physical-data admission

2026-10-17. **The saved attempt and its aggregate data-quality results are internally consistent with the frozen protocol. All four files pass the declared structural screening; physical labels and synchronization remain unadmitted.** The retained gaps and source-provenance questions are part of the outcome, not grounds to trim, repair or replace records.

This review read saved JSON/source metadata, compared file bytes and Git objects, and checked arithmetic relationships between saved aggregates. It did not rerun `audit.py`, parse the private CSVs, download anything, reconstruct labels, fit a delay/model, score a model or execute third-party code. In particular, the saved RMSE values, extrema and quaternion norms were not independently recomputed from raw rows. Their scope is the output of the previously source-reviewed, pinned audit. Existing frozen files were left unchanged; this review is a new artifact.

## Closure and associations

- Public source commit: `fd56ee27f358d7542ba29310ba1a44a620e098fa`. All **556 source-manifest pins** match both current local bytes and the exact committed Git objects. The manifest itself matches the publication receipt's byte count, SHA256 and Git blob `bbff0b49bd09e2ee3121707ddd58a2c8b3de4810`.
- The previous fresh-result manifest retains its recorded SHA256 `5b2188c33904b612a56056050c6b575404e0c9df539fd75c0bff84d2dee39a89`; all **547 prior pins** are identical members of the verified source closure. The attempt records 547 before and 547 after. This saved review also verifies their present bytes through the full manifest comparison.
- `STARTED.json` identifies the reviewed 9,500-byte audit with SHA256 `c93fc0da2bbca57f80d5911b63bb0988eb5383276af45779ba37d45ec9996032`. The result hash and byte count in `attempt.json` match the saved result exactly. The four filenames, byte counts and full Git blob IDs agree with the frozen source's literal `FILES` list; both pair identifiers and their receiver associations agree.
- The saved public-verification receipt is timestamped **01:52:13.431149 UTC**, preceding STARTED and the attempt start **01:52:22.911404 UTC**. Completion is **01:52:29.646750 UTC**; the monotonic elapsed report is **6.7351915 s**, consistent with the wall-clock interval and below 600 s. The launch precedes the fixed 03:00 UTC cutoff. Status is completed, with no failure fields or partial-results file. This reviewer checked the saved remote-verification receipt and local/committed bytes; it did not independently contact the remote server.
- The attempt records **19,305,511 private bytes**, below 32 MiB, and zero new scientific simulation calls/model scores. The four saved CSV byte counts sum to **19,298,710**. This review did not independently inventory private storage. The saved result is 9,111 bytes, below its public-output limit. No retry is evidenced by the one-use STARTED/attempt/result artifacts; this is not a claim about unobserved activity outside the recorded attempt.

The independent bookkeeping pass completed 1,203 metadata/pin/aggregate-relationship checks without a failed check. These are review checks, not physical samples, independent experiments or a rerun of the data audit.

## Reconciled data-quality outcome

| File | Rows | Duration if ticks are µs (s) | Median interval (ms) | Maximum gap (s) | Component RMSE, µs interpretation (mm/s) | Component RMSE, header-ms interpretation (mm/s) |
|---|---:|---:|---:|---:|---:|---:|
| CF50/04 | 6,369 | 63.635314 | 9.875 | 0.740633 | 44.133 | 140.674 |
| CF51/04 | 6,319 | 63.638577 | 9.893 | 0.781719 | 44.879 | 137.648 |
| CF50/05 | 6,448 | 63.843796 | 9.875 | 0.158007 | 44.148 | 160.257 |
| CF51/05 | 6,328 | 63.846282 | 9.893 | 0.900231 | 43.559 | 148.422 |

Rows sum to **25,464** and finite fields to **763,920 = 30 × 25,464**. Every saved schema matches, every observed column count is 30, and every nonfinite/nonpositive-interval count is zero. Each scale's compared-component count equals `3 × (rows − 1)`, totaling **76,380**. Thus the saved counts support the declared all-positive-interval/all-three-coordinate denominator rather than a selected moving-frame subset.

For each file, duration equals saved raw end minus raw start divided by the declared scale, and scaled medians equal saved raw medians divided by that scale. Header-ms durations and median intervals are 1,000 times the corresponding µs interpretation. The RMSE is the pooled component disagreement between position secants and average endpoint logged velocities; it is not an independent reference velocity error, a time-weighted error, or physical model score. Its smaller value under the µs interpretation supports internal compatibility with that interpretation. It does not independently calibrate the clock, establish signal latency, or resolve firmware timestamp semantics.

The saved pair-start differences are **25 ticks (04)** and **210 ticks (05)**, CF51 minus CF50. If ticks are µs, common-clock overlap is **63.635289 s** and **63.843586 s**, while overlap after separately zeroing each record is **63.635314 s** and **63.843796 s**. Both follow directly from the saved endpoints; their differences equal the respective start offsets on that interpretation. Under the header-ms interpretation those offsets are 25 ms and 210 ms instead. Both pairs correctly retain `synchronizationEstablished: false`. Start proximity and interval intersection do not prove same-instant observation or sensor/actuator synchronization.

The recorded quaternion norm error is at most **1.1102230246251565e-16**, and all PWM extrema fall in the structural interval [0,1]; the largest recorded PWM is about **0.934586**. These saved values reproduce the true structural-eligibility flags under the frozen 0.01 norm-error rule. The norm result concerns stored endpoints, not the validity of later component interpolation or the physical attitude reference.

## Retained flags and interpretation limits

1. **Long gaps remain.** The maximum intervals are approximately 0.16–0.90 s despite median intervals near 9.9 ms under the µs interpretation. All are included in the source's positive-interval diagnostic. The result stores extrema, not gap counts or locations, so this review cannot infer how many gaps occur or prescribe an exclusion window. No trimming, interpolation, imputation or repair was allocated.
2. **Firmware-force columns are not measured external force.** Every one of the 16 saved channel minima is negative; the most negative is approximately **−0.508790 N** in CF50/05. These are flagged source-defined firmware fields, not evidence of negative measured rotor thrust and not usable interaction-force truth merely because the header contains newtons.
3. **Structural eligibility does not settle calibration.** Every file includes zero PWM, outside the positive lower PWM fitting range in the inspected calibration script. The audit reports ranges, not how many samples lie outside that domain. No calibrated-label reconstruction or data exclusion follows from this observation. Battery and acceleration extrema likewise do not establish calibration accuracy, gravity convention or mass provenance.
4. **Physical questions remain open.** The 32 g training versus 34 g paper association, acceleration frame/gravity convention, per-run calibration, lag/boundary treatment, quaternion handling and independent holdout questions in [SOURCE-CHALLENGE.md](SOURCE-CHALLENGE.md) remain unresolved. The audit cannot identify a residual as only an inter-drone wake force. These are exposed development/admission flights, not untouched confirmatory tests.

The appropriate next state is continued provenance work with all complete files retained. The saved fields `physicalLabelAdmitted: false` for every file and `physicalEvidenceAdmitted: false` for the package are consistent with that boundary. No physical-validity, synchronization, prediction-accuracy or novelty conclusion is established here.

## Reviewed artifact identities

| Artifact | Bytes | SHA256 |
|---|---:|---|
| `results.json` | 9,111 | `395d175ade22caa25079a227d5eb8bc92e072794f19380bfb9aed23bd2db48ae` |
| `attempt.json` | 462 | `839f3271bd6f0834f288e168488971f489887e3207f17cb3d56b36bdffebf6e9` |
| `STARTED.json` | 229 | `67d37c508a243651d9032417b22f9d306a17aee62e95316812a86ab275fb7e07` |
| `source-publication.json` | 878 | `d4f9ad5bc5982081f20890fc0dca38f65810aae203346af2bc138ddc78b10ad4` |
| `source-manifest.json` | 116,349 | `2d915308399c4ce7b8c9eb5ba94554dd864fef714b95aff2b931a581f647f6eb` |
