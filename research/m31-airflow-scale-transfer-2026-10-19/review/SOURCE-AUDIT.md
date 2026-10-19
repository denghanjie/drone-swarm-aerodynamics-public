# Independent scale-transfer source review

19 October 2026. **Accepted for prospective source freeze, conditional on exact-public source verification before either scientific invocation. No remaining static evidence-review blocker.** This is source acceptance, not a numerical audit result or evidence that the correction transfers.

The reviewer inspected the current protocol, evaluator, supervisor, prior publication-receipt metadata and independently authored `source/audit.py`. Preparation used source text, AST parsing and source hashes only. The predecessor comparison payload was not opened, no MAT values were decoded, and no old/new scientific source, synthetic control or auditor was imported or executed. Earlier scientific allocations remain closed.

## Reviewed identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 6,594 | `f601656aa02217b05f84204e29ae62a0dca7b6ecda30f6d92e684f82dc623ef0` |
| `source/evaluate.py` | 5,492 | `ed721f4aacd194833dca847101c7f55a6024721380bdc2ba416ca8572e4a5d9c` |
| `source/audit.py` | 22,524 | `50e6a31a5d0a3f4778cc70a259736c1697243e9e8679a557bcce36f3e2176279` |
| `source/supervise.py` | 1,715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |

The sole scientific input is the predecessor's saved `results/comparison.json`, pinned to **1,112,834 bytes** and SHA-256 **`dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3`**. Its values and prior results were exposed before this design. The new split is a prospective within-dataset diagnostic on that already-known evidence, not a blind holdout.

## Saved records and partition

The evaluator checks complete predecessor status, the exact input hash/length, 3,240 unique records, finite X/Z/u/a/b, positive a/b and the fixed geometric domain. It copies the original record dictionary before adding outputs. It forms the calibration subset solely from Z<12, with exactly 800 records, and evaluation solely from Z>=12, with exactly 2,440. The evaluation bands are 12<=Z<20 with 1,640 records and 20<=Z<=30 with 800. The coordinate bounds identify selection intervals, not actual measured endpoint coverage.

The auditor reads the same saved JSON independently, refuses duplicate JSON keys/nonfinite numeric constants, and requires the known original field schema. It checks the original zero-based row/column/index domain, stride, linear-index relationship, unique increasing column-major order and finite values. Every copied numeric word, including X, Z, u, finite v, original a/b and original residualA/residualB, must retain its exact binary64 representation. A null v must remain null, and integer indices must remain exact integers. The audit also requires the exact ordered 800-entry `calibrationIndices` list and independently reconstructs all four subset counts. Neither implementation revisits the raw PIV data or old wake equations.

## Fitting and evaluation separation

For each of the two fixed predictors, the producer computes the numerator sum(p*u) and denominator sum(p*p) with `math.fsum`, using only the 800 calibration records. It requires a positive denominator, takes the nonnegative gain, and creates both gains before any corrected predictions or evaluation summaries. No evaluation record enters either fit, no intercept or alternative partition is introduced, and no model selection follows the fit. The independent auditor forms its own immutable calibration/evaluation tuples from the original coordinates, then derives both gains from the calibration tuple using 60-digit Decimal arithmetic. It never calls the producer's fit function or imports any scientific producer.

Saved numerator, denominator and gain are checked against those independent sums and ratios with 2e-12 absolute tolerance; the saved binary64 gain must also equal the nonnegative ratio of its saved sums. All 6,480 corrected predictions are independently recomputed from the frozen independent gains and the original saved predictor values. Their saved products and residual subtractions are additionally checked exactly in binary64, and their independent values must agree within tolerance. A zero-clamped gain is permitted algebraically but is a degenerate empirical correction, not a physically plausible positive reference-speed conversion.

The static control review confirms the source includes exact multiplicative recovery, a zero-clamped negative correlation, two positive observation rescalings, denominator-zero refusal and a calibration-invariance check after changing only a synthetic evaluation velocity. These remain inside the single future evaluator invocation. The auditor checks their saved receipt only and runs no new synthetic controls.

## Metrics and interpretation

The audit independently computes all sixteen metric groups: two models, four fixed subsets, and raw/corrected predictions. Every group is checked for count, equally weighted MAE, RMSE, signed mean residual and normalized RMS discrepancy. The latter is `sqrt(sum(error²)/sum(u²))`; a zero observed squared norm is refused. It is neither an average pointwise percentage nor an uncertainty estimate. All corrected metrics use independent Decimal products, not the saved corrected outputs as their computational inputs.

The primary endpoints are `subsets.evaluation.a.corrected.nrmse` and `subsets.evaluation.b.corrected.nrmse`: corrected normalized RMS discrepancy over the pooled evaluation cells. Both fixed models remain in the report. The two evaluation MAE reductions are checked as raw minus corrected, with signs retained; relative reduction is 1−corrected/raw, or null if raw MAE is zero. The sixteen metrics and these changes use the same 2e-12 absolute numerical consistency tolerance. It is not a physical acceptance threshold, confidence interval or experimental error bound.

A positive common rescaling of all observed velocities scales each fitted gain and corrected residual by that factor, while the corrected residual norm divided by observed norm is unchanged. This supports the primary normalized diagnostic. Raw errors and raw-to-corrected improvements retain the predecessor's reference-speed convention and do not share that invariance when only observations are rescaled. Calibration squared-error reduction alone is expected from least-squares fitting and cannot establish transfer; MAE need not decrease. A fitted gain may absorb amplitude, operating-point and other errors; it does not identify a physical Ui/UH ratio. Spatially varying calibration, shape/coordinate discrepancies and observable differences remain unresolved.

## Provenance, bounds and preservation

The new frozen manifest must include this package's protocol, evaluator, auditor, supervisor and review, as well as the predecessor protocol, saved comparison, original source/publication manifests, result manifest, execution receipt, successful evaluator/auditor receipts and independent audit report. It also requires the separate published-result receipt at `research/publication-receipts/m31-airflow-result-2026-10-19.json`.

Before the saved-result computation, the auditor verifies every new-manifest pin and the new source-publication receipt's manifest hash and exact remote/local plus committed/local flags. It binds the predecessor input to its execution hash, independently passing audit's input/result pin, original source commit/manifest and published result manifest. Both prior scientific supervisors must show successful bounded completion. This checks retained provenance rather than reopening any predecessor scientific invocation; the auditor makes no independent network claim.

The current evaluator must have a successful external supervisor, no failure artifact, an exact result execution hash/size and the expected control receipt. The auditor checks the 16 MiB cap and independently reconstructs the evaluator's saved-byte count, excluding the later supervisor receipt and current audit locks/logs. No unrelated output artifact may be inserted in results/UI between the consecutive evaluator and audit runs. The supervisor enforces separate 60-second deadlines, marks final elapsed times at or above sixty seconds as timeout, observes aggregate output size, and preserves stdout/stderr and exit/timeout status.

One exclusive `audit.lock` permits one audit. Success writes `audit.json`; failure writes `audit-failure.json` without overwriting an earlier report. The audit rechecks frozen files and exact input, provenance receipt, source receipt, control and result bytes after computation. It cannot fit another candidate, change thresholds, repair a failed evaluator or retry the allocation.

A later pass would establish preservation, training-only fitting and numerical consistency for this exploratory planar diagnostic. It would not establish independent physical validation, statistical significance, reference-speed calibration, a valid 3D wake or receiving-force law, or a deployable swarm model. The published RSS reference was already fitted to this study, all cells belong to a spatially correlated stitched mean field, and neither candidate is an independent challenger. Preserve these claim limits regardless of numerical outcome.

Any source change after these identities requires static review before launch. No new numerical outcome is known to this reviewer.
