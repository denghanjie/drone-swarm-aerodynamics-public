# Independent source and audit review

**Disposition: accepted for prospective freeze; no remaining static evidence-review blocker.** This is source acceptance, not a physical result or a completed numerical audit. The source manifest and exact public verification must precede the single evaluator invocation. The independent auditor runs once afterward, under its own 60-second allocation.

This reviewer read source and the published coordinate/schema metadata, compared the algebra to the historical kernel text, authored `source/audit.py`, and performed AST syntax parsing and file hashing. No experimental force/moment MAT values were decoded; no reader, model, synthetic control, evaluator, or auditor was executed. Only `source/audit.py` and this review were written in this task. The earlier text-only `review/DATA-SCHEMA.md` remains unchanged.

## Geometry correction before execution

The earlier acceptance of `R=l` is withdrawn. That unexecuted draft and its source identities are preserved under `design-history/radial-l-unexecuted/`; they do not authorize a launch. The corrected prospective variant is **`Kiran-stacked-projected-arm-fixedPWM-v1`**. This review supersedes the old radial-mapping discussion in the unchanged `review/DATA-SCHEMA.md`.

The primary-source reasoning recorded in `review/GEOMETRY-CORRECTION.md` combines the horizontal dimension in official PDF Fig. 3, the square/X layout in Fig. 4, and the statement that Δx/l=2 aligns opposing motor columns. Together they support Cartesian motor coordinates `(±l, ±l)`, with l=0.0325 m and radius `R=sqrt(2)*l`. Both the profile radius and diameter are corrected consistently. The experimental conversion remains `z=z_l*0.0325`; it is not changed to z/R. The correction precedes force inspection, evaluator launch, or empirical comparison of alternate mappings.

## Reviewed identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/mat5.py` | 2,445 | `c70e1c511a89bfe8adf1302dd5590f42042c412e6c46ef7beb6d191d13ed1032` |
| `source/evaluate.py` | 6,251 | `d807dda83b7c20e74f68a4dca767a05b6ed57589d9965f715051cb1a5b0c1ea4` |
| `source/supervise.py` | 1,200 | `2c25c016c2fcbf549ef55e9b75532b211f4038f10295b352ccaa56696dbc681a` |
| `source/audit.py` | 21,164 | `f7da88cec48eb91d3c8ab5cab302f4c4d54512c30af01a0763539cb8328b21a8` |
| `PROTOCOL.md` | 7,419 | `f7bf506252fc737631199e76af0b316fed4010ab5fec8a7c59e06ed1d6c1ef79` |
| `SCHEMA.json` | 10,250 | `2b1e87af178d2a23becba9d5e852ca69d9f98af8c991b2b3ad4e1802a09806c2` |

## Reader and indexing

The evaluator's MAT reader accepts only a bounded, little-endian MATLAB v5 file with one real, dense, two-dimensional double matrix. It handles ordinary and small-element tags and one zlib-compressed matrix; it checks version/endian, element lengths, dimensions, variable name, exact real payload size, stream completion, and finite decoded values. It rejects complex/logical/sparse/other classes through its strict flags check. It does not load MATLAB code, cells, objects, or arbitrary Python objects. This is deliberately a restricted reader, not general MAT compatibility.

The declared synthetic controls cover an uncompressed and compressed 2×3 double fixture, a small name tag, the flattened column-major values, truncation rejection, and nonfinite rejection. Their source is coherent, but they have not been run by this reviewer. They execute within the one declared evaluator invocation. The fixture's flattened ordering alone is not a complete coordinate-grid check; the independent auditor separately reconstructs all row/column associations.

SCHEMA exposes coordinate values and force/moment names, shapes, lengths, and hashes, without force/moment values. Its geometry fixes 14 rows × 12 columns; column zero is stacked. The corrected near-domain requirement is z/l≥5√2; on this frozen grid it selects rows 3–13, the same rows as the producer’s z/l≥7 grid check. Their physical separations are 0.25–1.10 m. Rows 0, 1, and 2 are all excluded as `near domain`. Exact x/l=2 is absent. Source uses MATLAB offset `row + 14*column`, so flat index `row` is the selected column-zero observation. No interpolation or outcome-dependent case selection occurs. Force means may be signed; only the selected SD fields are required nonnegative. The earlier proposed positivity requirement on all means was removed before freeze.

## Model specialization

Inspection of the historical `reference-excerpt.cjs` and `anchor-kernel.cjs` supports the stated scalar reduction. For upright stacked centers, each receiving rotor is at radius R=√2l from the source axis. Square-corner coordinates are `(±l, ±l)`, hence D=2R=2√2l and the near-height cutoff is 2.5D=5√2l. D is a motor-center diameter, not a propeller diameter. Source yaw has no effect on this axisymmetric stacked calculation.

For the upper receiver, the lower source has negative downstream displacement and contributes zero. Its output is the supplied isolated nominal baseline, independent of separation. Consequently the primary upper row-3-minus-row-13 prediction is zero without requiring the baseline to equal W. The nominal upper value of one in the case table is still an assumed normalization, not an independently measured isolated force.

For the lower receiver, the historical profile is evaluated at radial=R=√2l and down=z, with normalized down z/(2R) and width `0.07668*(z+11.634*R)`. With equal hardware/rotor area and four symmetric nominal rotor forces, the induced scale times the source total-force scaling, divided by receiver induced speed, reduces to `sqrt(q_upper/q_lower)`. The upper source's solved scale is one. Thus alpha is the declared profile times that ratio, the rotor ratio solves `x³+alpha*x=1`, and total lower force/W is `q_lower*x`. The code preserves the stated wake constants and smooth support factors. Nominal and sensitivity cases all must clear the near-domain check.

This is an algebraic hardware-matched operational approximation. It is not execution of the old full native query or certification of every old implementation admission gate. Fixed voltage/PWM is not fixed ideal power. Missing actuator response, unknown isolated baseline, pose/tare/calibration effects, and the directed-field/receiver-law choices remain joint limitations; a discrepancy cannot uniquely identify one of them as its cause.

## Independent auditor

`audit.py` imports only standard-library modules and does not import or call `mat5.py` or `evaluate.py`. It has its own bounded MAT tag cursor, decompressor, double-array reconstruction, and six fixed raw-file SHA-256/length pins. Its eventual single execution will independently decode x/z and upper/lower force means and SDs, check all 336 coordinate cells against the frozen schema, verify the rectilinear grid and geometry-only case selection, and compare all 44 selected observations by exact binary64 words.

It independently verifies all 11 nominal outputs and the ordered 81-point sensitivity grid per case, 891 sensitivity outputs total. It reconstructs the stacked rotor radius and upstream exclusion, uses 70-digit Decimal arithmetic and a 160-step monotonic cubic enclosure, and checks alpha, rotor ratio, upper/lower predictions, signed residuals, sampled extrema, MAE and maximum error in normalized and approximate-newton units. Primary difference and reconciliation thresholds are checked against the independently decoded observations, including exact rounded binary64 contrast/bias words.

The fixed model-arithmetic acceptance tolerance is `2e-12 * max(1, abs(independent value))`. It accommodates different arithmetic paths between the producer's 56-step binary64 bisection and the independent Decimal computation. It is a numerical audit tolerance, not a measurement error bar, useful physical-accuracy threshold, rigorous global floating-point proof, or experimental confidence interval. This tolerance was chosen before force-value inspection.

The auditor requires the normal `source-manifest.json` and `source-publication.json` receipt with exact manifest hash and committed/local plus remote/local equality. It requires a successful `evaluate-supervisor.json`, pins the completed comparison through `execution.json`, checks the saved control metadata, and verifies source/input pins before and after its work. It preserves result and receipt bytes. One exclusive lock permits one audit; success writes `results/audit.json`, while failure writes `results/audit-failure.json` and stops. Its report is bounded to 1 MiB. It does not create new cases, fit parameters, run additional synthetic tests, or supply confidence intervals.

## Allocation and claim limits

The evaluator's 11 nominal plus 891 sensitivity rows are separate from the explicitly budgeted fixed controls: two admitted prediction calls at 0.25 m and 1.10 m, one near refusal at 0.21 m, and five explicit root calls plus the two inside admitted controls. The protocol now states that distinction. The external supervisor invokes Python with `-I -B` and independently enforces 60 seconds for evaluate and audit, preserving stdout/stderr and exit/timeout metadata. Source publication remains an orchestration gate before evaluate; the current supervisor does not itself prove that gate occurred. The parent has committed to exact public verification before launch, and the auditor checks the corresponding retained receipt and pins afterward.

The README calls SD “over three trials,” while the paper describes fluctuations/unsteadiness. That aggregation ambiguity remains unresolved. No sqrt(n) conversion, p-value, calibrated confidence interval, or statistically resolved rejection is permitted by the current evidence. Unknown calibration/tare/drift and pose uncertainty are not zero. The primary reconciliation bias is a sensitivity threshold, not estimated uncertainty. The 81-point input grid is an illustrative sampled sensitivity set, not a continuous uncertainty enclosure or probability coverage.

No physical outcome is known to this reviewer. A later passing audit would establish data binding and computational correctness of this declared descriptive comparison; it would not by itself establish physical validity, moving-wake accuracy, full-controller behavior, novelty, or general multi-drone performance. Any source change after these hashes requires review before launch; no failed launch may be replaced under the current allocation.
