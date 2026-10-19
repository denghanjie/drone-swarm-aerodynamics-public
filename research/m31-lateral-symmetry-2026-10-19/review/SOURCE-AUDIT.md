# Independent paired-support source review

19 October 2026. **Accepted for prospective freeze, conditional on exact-public source verification before either scientific invocation. No remaining static evidence-review blocker.** This is source acceptance, not a completed audit or a numerical outcome.

The reviewer inspected the protocol, producer and supervisor, independently derived the paired-component identity, and authored the saved-result auditor. Only source text, AST parsing and source hashes were inspected during implementation. No input payload was paired or scored, no controls were run, no field or gain was evaluated, and no previous/new scientific producer or auditor was imported or executed. Closed allocations remain closed.

## Reviewed identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 7,157 | `f71a7aa0e1876d5fd77c2be120cc0c71470cc11ca99f02e57b7b151460060d2c` |
| `source/evaluate.py` | 9,053 | `84651fe343d8b66410d14c84d86ed78a3a99a9b442ecd7a1f695774368f8fd8f` |
| `source/audit.py` | 27,738 | `19c207081b488e5085cb95903f37eae2509d6494948d31b05159d753c205d885` |
| `source/supervise.py` | 1,715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |
| `review/PAIR-DECOMPOSITION.md` | 6,072 | `c0b1e8f2816e13ce8c462827629e841b9c2237ca704aead5f5ddd3336fbf8371` |

The single scientific input is the closed crossstream comparison: **2,291,932 bytes**, SHA-256 **`1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a`**. Its 3,240 cases and all values were already exposed. No new measurements or independent holdout are created by matching them.

## Geometry-only graph and retained support

The producer groups predecessor-included, nonaxis records by the hexadecimal representation of their saved Z values. It enumerates every opposite-sign edge within each level and accepts only pairs whose two endpoints each have exactly one eligible neighbor. The 0.01 normalized-X mismatch test is fixed and uses no measurement, candidate error or residual. Neighbor lists are sorted by original index. Pair order is increasing positive-X endpoint index, with consecutive zero-based pair IDs. Ambiguous relationships are reported, not resolved greedily or by nearest response.

The independent auditor constructs a bipartite graph keyed by the exact binary64 Z word, with negative-X versus positive-X vertices. It uses 60-digit Decimal geometry and the fixed .01 bound, then independently derives all degrees, edges, mutual-unique links, order and membership. It counts the same potential opposite-sign comparisons and enforces the declared 10,497,600 limit and 1,620-pair bound. Any producer/Decimal classification disagreement at a numerical boundary fails without tolerance widening or replacement of the pairing.

Every row's matching reason is checked in the declared precedence: prior exclusion, axis, no eligible neighbor, own ambiguity, counterpart ambiguity, paired. Pair IDs, partner indices and complete sorted neighbor lists must agree. Every eligible cell is either paired once or unmatched; prior exclusions remain unchanged inside the copied original case. The saved `selection.json` must independently match the result's matching table, reason counts, comparison count and four regional coverage records.

Coverage uses all predecessor-included cells in the region, including axis and ambiguous/unmatched cells. Its numerator is twice the pair count. The auditor requires at least twenty primary pairs, three distinct primary Z words and at least 90% primary coverage, checking the latter by exact integer inequality `10*pairedCells >= 9*eligibleCells`. It does not exclude difficult cells from the denominator or change the center/tolerance after failure. Near, middle and far group membership remains fixed by coordinates.

## Exact recursive preservation and provenance

The auditor requires the original and copied `originalCases` trees to match recursively: dictionary keys, list lengths/order, exact integer/boolean/null/string types and values, and exact finite binary64 words including sign bits. The same check covers the complete predecessor `subsets` tree copied into `fullFieldSubsets`. This preserves every nested original record, inclusion flag, earlier exclusion reason, measurement, saved candidate, residual and full-field metric, rather than only the new paired support. The inherited gain must exactly equal its saved predecessor value and the fixed 0.5450089857597356 word. No wake, continuity function or gain fit is called.

The new manifest must pin the predecessor protocol, source manifest/public receipt, result manifest, comparison, execution receipt, successful evaluator/auditor supervisor receipts and independent audit report, plus the separate crossstream result-publication receipt. The auditor binds the exact input to its execution, passing audit and published result manifest, and links the predecessor source commit to its publication receipt. This verifies retained provenance without reopening the earlier science or claiming a fresh network retrieval.

## Components and pooled metrics

The companion derivation proves, for residuals eR and eL,

    errorE=(eR+eL)/2,  errorO=(eR−eL)/2
    eR²+eL²=2*errorE²+2*errorO².

The producer obtains errors by subtracting observed components from predicted components. The independent auditor uses residual-first arithmetic and 60-digit Decimal values from the unchanged saved predictions/measurements. It checks every signed observed/predicted/error E/O value, all three pair SSE values, pair indices/order, exact copied coordinates, geometric mismatch and the per-pair identity. PredictedE is independently computed from both saved predictions and is never forced to zero on imperfectly mirrored positions.

For each of four regions, the audit independently recomputes six component RMS values, pooled direct/even/odd SSE, the two pooled shares, paired candidate RMSE and maximum geometric mismatch. It checks all twenty-four side metric groups: baseline/candidate for left/right/joint across four regions, each with count, MAE, RMSE and signed bias. Both models use identical paired support. The paired RMSE must agree with the independently computed joint candidate RMSE. Pooled direct SSE must agree with even plus odd SSE within the fixed tolerance.

The primary endpoint is `groups.primary.summary.energyShareE`, the pooled same-direction residual SSE divided by pooled even-plus-odd residual SSE. It is not an average of per-pair fractions. Exact zero residual energy retains agreement and yields null shares; it does not force failure or exclusion. Empty secondary groups have null summaries; zero eligible count has null coverage. These conventions are checked explicitly.

All independent numerical comparisons use 2e-12 absolute tolerance. Original copies and selected saved arithmetic/coordinate words receive exact binary64 checks. The tolerance is numerical consistency only, not physical accuracy or measurement uncertainty. Here residual “energy” means sums of squared normalized-velocity residuals; it is not a measured kinetic-energy budget. The algebraic identity holds even for geometric mismatch and is not evidence of incompressibility or field symmetry. Neither additive MAEs nor an additive RMSE identity follows from it.

## Controls, bounds and claims

Static inspection confirms the fixed controls exercise pure same/opposite components, a mixed identity, exact agreement/null shares, exact matching, response invariance, outside-tolerance rejection, same-sign/unequal-Z rejection, mutual ambiguity, axis/prior-exclusion precedence and an empty summary. They remain inside the sole future evaluator invocation. The auditor checks the saved control receipt and runs no extra synthetic cases.

Before saved-value matching, the auditor verifies current manifest pins, source-publication equality flags/hash, successful evaluator supervisor status, absence of failure, and exact result execution size/hash. It independently reconstructs the aggregate saved-byte count under the 16 MiB limit, excluding only the later evaluator receipt and current audit locks/logs. No unrelated results/UI artifact may be inserted between consecutive evaluator and audit runs.

The supervisor enforces separate sixty-second limits and observes aggregate output caps while preserving stdout/stderr and exit/timeout/limit status. The audit uses its own permanent exclusive lock and writes success or failure without replacing prior evidence. It rechecks every frozen file and exact input, predecessor/source receipt, control, selection and result bytes after computation. It cannot retry, repair a failed evaluator, widen matching or remove an observed component as a new correction.

A later passing audit would establish preservation and numerical consistency of this paired-support diagnostic. It would not identify swirl, drift, asymmetry, centering or calibration as a cause, establish exact field parity, improve the unchanged full-field model, calibrate SI units/uncertainty, or validate force/swarm behavior. Paired-only outcomes cannot replace the retained full-field metrics. These are exposed, correlated cells from one experiment, with no independent trial or significance claim.

Any change to the reviewed identities requires static review before launch. No new pairing or metric outcome is known to this reviewer.
