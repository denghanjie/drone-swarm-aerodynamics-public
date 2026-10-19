# Independent airflow source review

19 October 2026. **Accepted for prospective source freeze, conditional on retained exact-public source verification before launch. No remaining static evidence-review blocker.** This is source acceptance, not an executed audit or a physical result.

This reviewer read the protocol, producer, restricted reader, supervisor and DATA-PINS metadata, then authored `source/audit.py`. Only text inspection, AST syntax parsing and source-file hashing were performed. No PIV coordinate or velocity payload was decoded; no parser fixture, prediction, evaluator or auditor was executed. The eventual single audit has its own 60-second allocation and cannot repair or rerun the evaluator.

## Reviewed identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 6,602 | `d3c77aa8d4f9b79d2cfa862418080040c148f8715959da7041be295a2f0781c3` |
| `DATA-PINS.json` | 690 | `61d01b7cf276ed9f8458d8bec6dbe5aeb14724cec414ddc9b5f51ce56e87c7c2` |
| `source/evaluate.py` | 6,349 | `2aea217af06e4190793323cdc831fea74ea4fd146c4c89989ea9ed57ba1f3a54` |
| `source/mat5.py` | 2,494 | `f581668b05ead28d9ccfb0e280c24dbab90e9a08daec7f030abcad2834d26b36` |
| `source/supervise.py` | 1,715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |
| `source/audit.py` | 21,384 | `df819abba076c806f15394a5468cb66dcc52a910d9500b65f0fc52bc960ade7a` |

## Data binding and selection

The producer permits only a single bounded little-endian MATLAB v5 real dense double matrix, with exact class/flags, rank, name and payload size. Its 4 MiB bound covers both file and decompression output. The explicit nonfinite option preserves masked cells; it does not silently substitute zero. The declared two parser fixtures retain a NaN, and the two refusal controls cover truncation and strict-mode nonfinite rejection. Their source was reviewed, not executed.

The fixed 272×537 shape gives 68×135=9,180 candidates at the declared row/column stride of four, below the 9,216 cap. All indices are zero-based, beginning at row 0 and column 0. Traversal is column-major, with original linear index `column*272+row`. The sequential exclusion rules are nonfinite coordinates, outside the joint domain `8<=Z<=30` and `abs(X)<=4`, then nonfinite u. A missing v is counted only among admitted finite-u cases and is saved as JSON null. Finite negative u remains included. At least twenty accepted cells and three distinct Z values are required without widening selection. The accepted count is unknown at this source-review stage.

The auditor has a separate MAT cursor and decompressor and imports no producer modules. It explicitly reconstructs columns, independently checks the four original MAT hashes and lengths plus README against hardcoded pins and DATA-PINS, and reproduces every exclusion count. Each admitted row/column/index must match the ordered selection. X, Z, u and finite v are checked by exact binary64 words; masked v must be null. No interpolation, duplication removal or data-dependent slice selection occurs.

## Model and metric consistency

The producer uses the declared physical plane at y/l=1. Model A therefore samples the axisymmetric kernel at radial distance `sqrt(X²+1)`, with motor-center diameter `D/l=2sqrt(2)`. Its normalized axial coordinate, profile width and center coefficient retain the original D scaling. The radial fade is one through ratio two, transitions smoothly to zero at three, and then remains zero. The selected Z domain lies above the near-height exclusion and below the physical axial fade and source cutoff. No receiver cubic or thrust conversion appears. The amplitude comparison explicitly assumes a common induced-speed convention Ui=UH; it does not establish equality to an independently calibrated operating point or an SI velocity scale. The saved result retains this limitation.

Model B uses `abs(X)` in the measured plane, the published l-unit coefficients 9.508, .0667 and −6.0585, and no added cutoff. Its in-sample provenance is explicit. The producer's unit-conversion controls divide the origin and numerator by D/l together when rewriting B in D units; they do not substitute l-unit constants unchanged into A. The three prescribed points include X=0 and check lateral symmetry. Two endpoint controls call the same radial-fade helper used by the producer predictions, checking its values at ratios two and three.

The independent fields use 60-digit Decimal arithmetic and algebraic expressions wholly in l units. In particular, A uses shifted distance `Z+5.817*2sqrt(2)`, radius squared `X²+1`, and a rational width-to-denominator expression. B similarly uses its l-unit shifted distance and X². The fade is evaluated as `1−3t²+2t³`, unlike the producer's factored expression. This independently computes the same two declared fields once for each saved admitted cell, with **2e-12 absolute tolerance in Ui units**. That is solely an arithmetic audit tolerance, not a physical accuracy criterion or experimental uncertainty.

For each field, saved residuals must equal prediction minus measured u, including exact binary64 agreement with the saved prediction/subtraction and independent Decimal agreement. Overall and each fixed bin are checked for count, MAE, RMSE, signed bias, maximum absolute residual and index. Empty bins must have count zero and null numerical metrics/location. Equal cell weights are used. The maximum location follows the first column-major maximum of the already independently checked binary64 residuals; its independently computed high-precision magnitude must agree with the independent maximum within tolerance. This preserves the specified floating-point tie semantics. The paired MAE difference is also checked independently and against the saved metric subtraction.

## Execution guard and scope

The producer checks the manifest, exact file pins and public receipt before running its controls or decoding matrices. The auditor independently requires the manifest to include the protocol, DATA-PINS, all four sources including itself and supervisor, this review, and pinned data/README. It requires manifest SHA agreement, exact committed/local and remote/local receipt flags, matching source commit, successful evaluator supervisor status, and the execution receipt's exact saved-result size/hash. It checks saved control metadata but runs no new controls. The parent must complete the actual public verification before invoking either allocated program; receipt checks are not an independent network retrieval by the auditor.

The auditor uses its own exclusive `audit.lock`, fails closed, and writes either `audit.json` or `audit-failure.json` without replacing an existing report. Its output is bounded to 16 MiB. Both programs remain subject to the external supervisor's separate 60-second limits and 16 MiB saved-output cap; the supervisor also marks a completed process timed out if its final elapsed time reaches sixty seconds. The auditor requires no output-limit breach and independently reconstructs the evaluator's saved-byte total, excluding only the evaluator receipt and audit invocation's own locks/logs, then checks exact agreement with the supervisor's captured count. No new unrelated result/UI artifacts may be inserted between these consecutive scientific invocations. The auditor rechecks all frozen files after its work and verifies that source/publication and saved result/control/execution/supervisor bytes have not changed. No additional cases, fitting, repairs or retries are authorized by it.

Any passing saved-result audit would establish data binding, selection and numerical consistency of this descriptive comparison. It would not establish independent validation of the fitted RSS curve, statistical significance, calibrated experimental uncertainty, full three-dimensional airflow, receiving-rotor force accuracy, or a valid multi-drone controller. The aggregate cells are not independent trials, the measurement plane is limited, stitched-field/calibration errors are unquantified, and A is the project's axial interpretation of a kernel whose original observable was flow magnitude. These limitations remain in the saved result and must remain in the report.

Changes to the reviewed identities require static review before launch. No scientific outcome is known to this reviewer at this checkpoint.
