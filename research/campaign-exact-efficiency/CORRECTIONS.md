# Editorial correction C1: independent field-time gate count

Date: 2026-10-13. This is an explicit reporting correction to the original evidence package. The original package remains a retained version; this correction does not silently redefine its contents.

## Correct result

**Three of twelve independent nonzero field cases pass both conditions versus previous-zero:** median paired time ratio at most 0.9, and paired-bootstrap 95% upper ratio strictly below 1. Four of twelve meet the median-only condition.

The original report said “4/12” and the independent findings said “four of twelve” passed the complete screen. That wording counted the median-only condition as if it were the full two-part gate.

The three actual passing cases are:

- `independent-field-628791-100-sparse-lean`
- `independent-field-628791-200-tilted-lean`
- `independent-field-628792-100-tilted-lean`

## Decisive evidence

The [628791 / N=100 / tilted raw record](robustness/raw/independent-field-628791-100-tilted-lean.json) has:

- Median lean/previous-zero ratio: **0.872160303446306**
- Paired-bootstrap 95% interval: **[0.7046978668544749, 1.0105362127091932]**
- Saved full-screen `qualified` flag: **false**

Its median is at most 0.9, but its upper bound is above 1. The stored per-case interval and flag were already correct. Independent recalculation from all twelve saved paired timing records reproduces every median, bootstrap endpoint and per-case gate. There is no change to the comparator, threshold, resampling method or evaluation population.

## Scope of the correction

- The primary held-out N=100/200 result remains **8/12** against previous-zero.
- The independent nonzero result against legacy remains **12/12**.
- No family/count passes the full previous-zero gate on both fresh independent seeds.
- No timing measurements, fixture data, simulation equations, evaluator code, source-selection decisions, numerical records or per-case qualification flags change.
- The reporting template in `src/summarize.py` changes only prose literals and the obsolete prose-formatting replacement, so regenerating the report cannot restore the incorrect count. No computation or statistical logic is changed.
- No new experiment, rerun, retuning or additional timing was performed.

The scientific interpretation is slightly more conservative: incremental gains over previous-zero are workload-sensitive. The substantial observed improvement over legacy, short-window software equivalence, smaller whole-pipeline gains and unresolved physical validation remain as previously scoped.

## Original artifact identity

These SHA256 values identify the affected original artifacts, before this correction:

| Original campaign-relative artifact | Original SHA256 |
|---|---|
| `REPORT.md` | `015c9a232175b8641f21ca42e2466ae646d248bd08be08ed5104e3128e47a272` |
| `robustness/FINDINGS.md` | `8f0fe4c54a8cbd2265bd1975ba6d474752d7810eede9ce9d08250f30dd27210f` |
| `src/summarize.py` | `c2ff61e6aaa9d3782db1e953094f1fd72c4c0a6f2b33a057530944781f72e067` |
| `exact-airflow-evidence.html` | `0b7ec7e511da1aa31a49d56f66486d32686dd1720aaff2078319901dcf47ff50` |

The candidate evaluator remains SHA256 `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`.

## Versioning and viewer

Corrected prose explicitly links this notice. The original standalone viewer contains an embedded copy of the old report; it must remain preserved as the original version. A corrected viewer should be rebuilt from the corrected campaign prose, given a new versioned filename and recorded with its own hash. Static identity checks should confirm the embedded report equals the corrected `REPORT.md`. Rebuilding or statically checking the viewer does not establish rendered or interactive browser QA.

The correction package supplies a minimal campaign-root overlay, original/replacement hash pairs, a unified diff and a reproducible saved-record verification. Apply it only to a new publication staging copy after confirming each original hash; do not overwrite the retained original package.
