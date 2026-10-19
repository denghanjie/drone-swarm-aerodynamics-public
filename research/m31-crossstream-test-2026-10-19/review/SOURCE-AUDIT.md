# Independent cross-component source review

19 October 2026. **Accepted for prospective source freeze, conditional on exact-public verification before either scientific invocation. No remaining static evidence-review blocker.** This accepts source and the declared conditional sign/geometry mapping; it is not a numerical or physical result.

Preparation consisted of source and archive-document inspection, reading the official paper's coordinate definitions/figures, analytic derivation, AST syntax parsing and source hashing. No new saved-velocity scoring, model arithmetic, synthetic control, evaluator or auditor was executed. No MAT payload was decoded. Existing allocations remain closed.

## Reviewed identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 6,652 | `42eb96273aa42235805bee145cc1b6cf2feb717a9c0504707c3e0e6320c6e25e` |
| `source/evaluate.py` | 6,063 | `d7bbc3f85c36f933b3b0e5d16034acba2188aedc4a6666dc54274bfe5aa41cd2` |
| `source/audit.py` | 24,368 | `f32a08a401f319a6cbe8aac04907db275a328576f28c51fc1bd24d8a2c6562c1` |
| `source/supervise.py` | 1,715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |
| `review/GEOMETRY-AND-CONTINUITY.md` | 7,344 | `7c7bc00e9aff02bb423f591042e523f1c73bf05460e72f529f736af534b06f3e` |

## Sign, geometry and candidate

The companion derivation records the evidence chain: official paper §III-B identifies v along x and u along z; Fig. 3 shows +x right/+z down; the single-source archive script directly plots x_piv/z_piv/v_piv without negating x or v. Fig. 7 and its discussion corroborate the sign qualitatively. Positive v along increasing X is therefore admitted as the fixed documented mapping, with missing preprocessing/instrument traceability explicitly retained. Neither the sign nor a magnitude-only target may be selected after seeing the new scores.

The producer matches the stated unfaded axial profile and its steady incompressible axisymmetric radial completion. With `s=Z+5.817*2sqrt(2)`, `b=.07668*s`, `R²=X²+1`, `c=sqrt(2)−1` and `Uc=g*10.11*2sqrt(2)/s`, the auditor independently uses

    H = b²+cR²
    U = Uc*b⁴/H²
    factor = Uc*.07668*b*(b²−cR²)/(2H²)
    V_R = factor*R
    V_X = factor*X.

This rational expression follows integration of cylindrical continuity from the regular axis and is algebraically equivalent to the producer's ξ-polynomial/projection expression. The auditor uses 60-digit Decimal arithmetic and no producer imports. It independently checks radius, ξ, axial core, radial candidate and horizontal candidate for every one of the 3,240 saved rows, including geometrically excluded rows whose candidate values are retained only as generated bookkeeping. Only the admitted core enters metrics.

The completion assumes zero mean azimuthal velocity. Continuity fixes the radial component, not swirl; on Y=1 swirl would add −Vtheta/R to the horizontal component. The off-axis plane's two-dimensional divergence need not vanish because the y derivative is omitted. The regular-axis boundary condition, axisymmetric extension, axial interpretation of the original scalar kernel and reference-speed convention remain assumptions. This is a local completion of the unfaded core, not a globally conservative finite-support kernel or a Navier–Stokes solution.

The ξ<=2 criterion keeps the entire radial integration disk inside the unfaded region. The fixed Z domain is also before the axial fade and above near admission. The positive/negative radial branches are retained: the expression crosses zero at ξ=1/sqrt(c). No forcing of an outward sign, additional scale, intercept, width or origin occurs.

## Immutable saved inputs and inherited gain

Both scientific inputs are independently hard-pinned:

| Saved input | Bytes | SHA-256 |
|---|---:|---|
| Original airflow comparison | 1,112,834 | `dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3` |
| Closed scale-transfer comparison | 1,766,917 | `027165cb42fe4445496779d3f4cdb87a902248d38cdf9a8ddc4adfa1b042d269` |

The fixed gain 0.5450089857597356 must match the prior A gain by exact binary64 word and the new saved inherited-gain word. The prior result must name the original airflow input's exact pin. Its previously passing audit and publication chain bind this value; the new audit does not re-fit or rerun the prior allocation. Lateral values enter neither an old nor a new gain fit in this checkpoint.

Every original record is preserved, including excluded rows. The auditor checks the exact original field schema, integer row/column/index, stride and increasing unique column-major index relationship. X, Z, u, finite v, a, b, residualA and residualB are compared by exact binary64 words. A null v remains null. Duplicate JSON keys and nonfinite numeric constants are refused. No missing lateral value is replaced with zero; zero is solely the defined baseline prediction.

## Selection, controls and metrics

Selection is reconstructed using independent high-precision ξ geometry: outside-core first, missing lateral second. Exclusion reasons, inclusion booleans and the total partition must agree; no residual, sign or signal threshold controls admission. Missing/excluded residuals must be null. Included residuals are checked against the independent prediction minus measured v and exactly against the saved binary64 subtraction. Any independent geometry/producer classification mismatch fails the audit rather than prompting a threshold change.

The primary group is admitted Z>=12; the near group is admitted Z<12 and remains descriptive. Middle and far split the primary group at Z=20. The auditor independently requires at least twenty primary records, three distinct primary Z values and positive primary lateral squared norm. It checks every group count and all eight metric groups: baseline/candidate for primary, near, middle and far. Empty groups must have null metric objects; nonempty secondary groups with zero target norm have null NRMSE. The nonzero-norm baseline must have NRMSE exactly one, a mathematical identity rather than an accuracy criterion.

All equal-cell MAE, RMSE, signed bias and NRMSE values are independently recomputed. The primary signed contrast is baseline RMSE minus candidate RMSE, with relative reduction 1−candidate/baseline; adverse changes remain signed. Saved contrasts also must exactly equal the subtraction/division of saved RMSE values. The absolute tolerance is 2e-12 for independent numerical checks. It is not a physical acceptance threshold, uncertainty bound or statistical confidence interval.

The producer's fixed controls are coherent with the declared allocation: odd symmetry and projection at three fixed points; radial zero and regular-axis limit; three centered finite-difference cylindrical continuity checks; a zero-baseline metric; and geometry/missing-value precedence. The continuity difference evaluates the actual producer radial/axial functions at the fixed coordinates with h=1e-5 and tolerance 2e-8. These controls have not run during review. The auditor checks their saved labels, count, tolerance and residual bounds, but executes no additional control cases.

## Provenance and bounded execution

The new manifest must pin current protocol/source/reviews and both predecessor chains: protocol, source manifest/publication receipt, result manifest, comparison, execution, successful evaluator/auditor supervisor receipts and independent audit report. Each predecessor result manifest must bind its exact saved comparison and match the separate exact-public publication receipt. The audit checks these links and prior successful bounded statuses, without an independent network claim or a predecessor scientific rerun.

Before decoding the saved scientific inputs, the auditor verifies all current manifest pins, the public source receipt's hash and remote/local plus committed/local equality flags, current successful evaluator status, absence of failure, the result execution hash/size and saved control metadata. It independently reconstructs the evaluator's aggregate saved-byte count, excluding the later evaluator receipt and current audit locks/logs, and requires agreement with the supervisor under the 16 MiB cap. Do not insert unrelated results/UI artifacts between these consecutive scientific invocations.

The supervisor independently enforces sixty seconds and observes aggregate scientific output size, preserving logs and exit/timeout/limit status. The auditor has its own exclusive permanent lock and writes success or failure without replacing an earlier report. It checks every frozen file again and verifies exact preservation of original inputs, predecessor receipts, source receipts, controls and saved results. No retry, sign reversal, candidate tuning or repair of an evaluator is authorized.

A later audit pass would establish input preservation and numerical consistency for this exposed same-experiment component diagnostic. It would not establish calibrated lateral uncertainty, independent experimental validation, a uniquely reconstructed three-dimensional vector field, global continuity/momentum, a receiving-force model or flight/swarm validity. The missing single-PIV preprocessing remains unresolved regardless of outcome.

Any source change after these identities requires static review before launch. No new numerical outcome is known to this reviewer.
