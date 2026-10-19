# Static protocol and identifiability review

19 October 2026. Reviewer: protocol challenge agent. **Accepted for prospective source freeze, conditional on the source identities below remaining current and the required exact-public verification being completed before either scientific invocation.** No remaining scientific-design or model-implementation blocker was found in the reviewed source. This is not an executed numerical audit or a physical result.

## Review boundary

This reviewer read source, protocol, attribution, README, retained article text and previously rendered article figures. The only machine operations for this review were static text/image reading, filesystem metadata, cryptographic hashes, and writing review documents. No project import, syntax parser, MAT payload decoder, model calculation, synthetic fixture, evaluator, numerical auditor, test, or browser run was executed by this reviewer. Coordinate and velocity payload values remain uninspected by this reviewer. The prior physical-force allocation remains closed.

## Question and interpretation

The chosen single-drone mean-axial-airflow comparison is an appropriate next diagnostic. It can reveal a discrepancy in the project's airflow prediction before a receiving-drone thrust law is used. It cannot identify the receiving-rotor cubic, actuator response, paired-wake feedback, mutual upper-vehicle interaction, or a safe many-drone controller. No force transfer or fit is implemented.

The RSS reference was fitted to this experimental setting. Its error here is descriptive and in-sample, not independent validation. Article plots and coefficients, and the prior stacked-force outcomes, were already exposed. The source protocol records that exposure rather than presenting the new payload comparison as blind. The aggregate stitched field does not supply independent trial replicates or an uncertainty distribution. Equal grid-cell weighting is explicit; neither fine sampling nor a small reference error supplies a confidence interval or experimental accuracy threshold.

The original Bauersfeld instrument measured flow-speed magnitude, whereas RSS u_piv is the mean downward axial component. The declared target is consequently the project's axial interpretation of that scalar kernel. The protocol, saved-result schema and visible viewer prose retain this limitation. The shared Ui=UH induced-speed convention is an assumption about normalization, not an independently calibrated operating point or established dimensional speed scale. An amplitude discrepancy cannot be attributed solely to wake shape.

## Geometry, units, selection and arithmetic

The RSS Fig. 4 sheet passes through the front rotor row. For rotor centers at (±l,±l), the declared plane y/l=1 and Model A radial coordinate sqrt(X²+1) are consistent. Model B intentionally uses the planar coordinate |X|. Its coefficients cannot silently become a three-dimensional radial field.

Model A preserves the project's historical D=2sqrt(2)l normalization, center coefficient, width, and radial fade. Model B preserves RSS l units, including Bd=9.508, slope .0667, and origin −6.0585. The unit-identity source divides the reference numerator and origin together when rewriting B in D units. The selected domain is beyond A's near admission and before its physical axial fade and source cutoff. The independent auditor checks the same two fields with different l-unit rational expressions and 60-digit Decimal arithmetic. Its 2e-12 tolerance is an arithmetic agreement criterion only.

The fixed zero-based stride begins at row 0 and column 0; traversal is column-major and saved linear index is column*272+row. Geometry is selected before reading u/v for inclusion. Sequential counts distinguish nonfinite coordinates, outside-domain cells, and missing u. Finite negative u remains admitted. Missing v is counted among admitted finite-u cells and saved as null; it never excludes an axial record. The minimum accepted-count/distinct-Z requirements fail closed without widening the domain. No interpolation, smoothing, duplicate removal or adaptive slice selection is present.

Both producers of numerical evidence use the fixed bins [8,12), [12,20), and [20,30], preserve empty-bin null metrics, and define residual as predicted minus measured. MAE, RMSE, bias and maximum absolute residual follow that sign convention and equal-cell weighting. The first maximum is the first in column-major traversal; the audit separately checks independently computed magnitudes within its declared tolerance while preserving the saved binary64 tie rule. The paired MAE difference is A minus B and receives no inferential interpretation.

The restricted reader rejects unsupported MAT representations, oversized/truncated structures, extra matrices, wrong class/rank/name/shape, and bad compressed-stream boundaries. The explicit nonfinite mode permits missing-data masks without zero filling. The independent auditor uses its own cursor, decompressor, original input pins and column reconstruction, with no producer imports. It checks every admitted original numeric word, predictions, residuals, selection counts, overall metrics, bins, and source/result preservation.

## Controls, bounds and display

Pre-freeze review corrections are present: refusal controls are accurately named as truncation and strict nonfinite rejection; fade endpoints call the same helper used by the prediction; zero-based indexing is explicit; and the axial-versus-magnitude and induced-speed assumptions are visible. These controls were read but not run by this reviewer.

The sole evaluator and sole auditor have exclusive invocation locks and separate external 60-second limits. The supervisor observes aggregate saved output, reserves receipt space, records output-bound violations, and terminates its owned process group on a time/output breach. Final elapsed time is checked even when the child has just exited. The auditor also requires a successful evaluator output-bound receipt and reconstructs its saved-byte total. Sequential execution with no overlapping jobs remains a required parent invocation discipline; no unrelated result or UI files may be inserted between evaluator and audit because the byte-total check intentionally binds that interval. Failures must remain preserved; this acceptance grants no repair, retry, extra cases or reopened allocation.

The saved-only viewer hashes comparison bytes before parsing/rendering, requires a complete evidence status and count, and places each point at [X*l,l,−Z*l]. It uses one measurement plane, with schematic rotor geometry, and does not generate a new airflow volume or flight simulation. Its source distinguishes negative measured values from saved-data alteration and uses a shared color scale for the measured/two-model views. Browser correctness, mobile layout, interaction, corruption refusal and console behavior still require the already allocated UI verification; static reading does not claim those checks have passed.

## Freeze identities and remaining procedural gates

Paths below are relative to this checkpoint package. The independent source-review note is separately included in the source manifest; this note does not substitute for that review. The eventual manifest must include these reviewed implementation/protocol files, both review notes, all input files and the applicable viewer dependencies. Any changed reviewed source needs static review before launch.

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 6602 | `d3c77aa8d4f9b79d2cfa862418080040c148f8715959da7041be295a2f0781c3` |
| `DATA-PINS.json` | 690 | `61d01b7cf276ed9f8458d8bec6dbe5aeb14724cec414ddc9b5f51ce56e87c7c2` |
| `data/ATTRIBUTION.md` | 797 | `56abda5764f77612df3a082af723b2ecefe79d8fba56ab8ae7e03002e47085a5` |
| `source/evaluate.py` | 6349 | `2aea217af06e4190793323cdc831fea74ea4fd146c4c89989ea9ed57ba1f3a54` |
| `source/mat5.py` | 2494 | `f581668b05ead28d9ccfb0e280c24dbab90e9a08daec7f030abcad2834d26b36` |
| `source/supervise.py` | 1715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |
| `source/audit.py` | 21384 | `df819abba076c806f15394a5468cb66dcc52a910d9500b65f0fc52bc960ade7a` |
| `source/ui.cjs` | 4005 | `b5036d17af390503d453337372384eb307672a9b825e7d66cc9b2afa511e76a2` |
| `viewer/app.js` | 5738 | `b6fed976b3392364e36d2ce106f40f181cf07cf9d4f622fe02ddfa8a55370079` |
| `viewer/index.html` | 5094 | `2595a1807c16f2778fd8567d645c63fb431c28658bcf86ff2227f4e97ba3905a` |

At the review boundary there was no results directory and no inspected numerical outcome. Source-manifest creation, immutable commit/push, actual exact-public retrieval verification, both bounded scientific invocations, result publication and UI execution remain the parent's separately authorized work. Receipt flags inside a program are not themselves this reviewer's network verification. Success, if later established, supports only faithful calculation of this fixed descriptive comparison and its stated limitations.
