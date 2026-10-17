# Next decision after the direct-load negative result

Recommendation: close the fixed smallest-upper 10% deletion route. The next prerequisite should be a fair, ordinary binary64 full-interaction baseline under an explicitly native-load/offline-audit contract, before any grouped approximation. Only after its semantics, accuracy and complete cost are known should contribution-preserving aggregation take first algorithmic priority. The native contract differs from Q-current's per-query proof output; it does not erase this strict failure or authorize a looser tolerance. This memo allocates and implements nothing.

## What the saved evidence establishes

The accepted checker reports `fixed-route-stress-accuracy-definite-failure`. All six full controls pass A and B at 1e-8. For the omission proposals, every one of the four categories definitely fails both 1e-8 and 1e-4 in every state. Both t0 states definitely fail all four categories even at 1e-2. The other four states pass all four A categories at that stress tier.

Approximate numerical levels below are rounded displays of the saved rational A error intervals, not new gate calculations. Rotor errors are normalized by mg/4, collective and world force by mg, and moment by mg*R. Collective/world-force values agree at the displayed precision; they are not asserted exactly identical. Each category is a maximum and can concern a different drone/rotor.

| State | Deleted / positive | A rotor | A collective / world force | A moment | B=C rotor upper |
|---|---:|---:|---:|---:|---:|
| run-a-t0 | 39 / 389 | 6.174e-2 | 4.703e-2 | 1.305e-2 | 2.552e-1 |
| run-a-t5 | 26 / 252 | 2.283e-3 | 1.197e-3 | 5.429e-4 | 1.253e-2 |
| run-a-t10 | 20 / 192 | 7.639e-4 | 3.328e-4 | 2.274e-4 | 4.304e-3 |
| run-b-t0 | 40 / 394 | 6.589e-2 | 2.516e-2 | 1.772e-2 | 2.643e-1 |
| run-b-t5 | 26 / 256 | 1.876e-3 | 7.714e-4 | 5.203e-4 | 1.116e-2 |
| run-b-t10 | 17 / 163 | 6.453e-4 | 2.363e-4 | 1.738e-4 | 3.861e-3 |

This is actual omission error relative to the declared full mathematical model, not merely failed certification. No signed-error mean was measured, so call it neither statistical nor signed bias. These are numerical relative-to-normalization quantities, not experimentally validated physical percentages. The snapshots were taken from airflow-off flights; no closed-loop trajectory error follows.

There is also certificate slack: at t5 the actual rotor errors are about 0.00228 and 0.00188, while B's upper bounds exceed 0.01. Rotor alone blocks the B/C stress gate at both t5 states. B/C stress passes only at the two t10 states. Improving that certificate could recognize some looser-tier accuracy, but cannot turn the strict A failures into strict accuracy.

For the omitted candidate, B and C have exactly equal K, all 256 local k values, all 256 outward root boxes, and maximum-error intervals in every state. These are equality comparisons of canonical saved rationals, not rounded decimal comparisons. This agrees with the prospective observation: widening the lower contraction endpoint need not change max(1,pUpper,1/pLower) when its upper term controls. Equality does not prove the sufficient tL*pUpper>=1 condition on every row, nor does it mean that the contraction intervals have no extra uncertainty. The saved-row condition counts belong to the prespecified analysis plan. C is not an independently identified bottleneck on these candidates.

The full native control, supplied oracle coefficients, has A rotor errors near 2e-16. That supports the fixed native solve on these states. It leaves coefficient construction, admission, and whole-query cost unresolved. The 17–40 deleted positive terms per state were drawn from 16,128 possible rotor/source pairs; their count is neither the fraction of total work avoided nor a speed measurement.

## Priority and contract before the next experiment

The original target is useful 5,000-drone browser computation, not a succession of high-precision oracle demonstrations. Historical named-Chrome query medians around 366–396 ms remain context, and the later exact beta/nu reuse comparison missed its complete-worker speed gate at all six states. Those are different contracts and timing boundaries; do not compare either directly with this Python diagnostic's runtime. Dense diagnostic tensors were already excluded from the old timed queries, so removing them is not a new saving.

Recommend making the next primary artifact a complete native current-input-to-load path, with independent offline reference checks on a prospectively fixed, disjoint small-state/sequence holdout. Define that interface explicitly: required current-input domain/status behavior, rotor/collective/world-force/moment outputs, retained provenance, and which verification is offline. Requalify a full-contribution native control against the same independent mathematical reference before attributing an approximation failure. Keep 1e-8 as the present primary numerical gate; 1e-4 and 1e-2 stay separately named diagnostics unless a new tolerance contract is justified before results.

Such a native interface must not be called Q-current certified output if it omits online enclosing bounds/admission proofs. Conversely, if per-query online certification is an actual requirement, charge it to all methods and preserve its failure outcomes. This decision should be explicit before further source preparation. No hypothesis here establishes physical-model validity or exempts later coupled-flight evaluation.

**Ranked prerequisite: qualify the strongest ordinary binary64 full-interaction implementation first.** The oracle full control only establishes the solve after coefficients have already been supplied; it is not that baseline. Existing legacy native source may be a starting point, but its preparation, constants, weights, branch precedence, caps, ordering and full load equations must be checked against the same supplied M-current model. Do not assume matching names imply matching semantics. Use prospectively fixed fresh conditions plus retained failure/boundary controls, with independent offline references and an explicit no-online-load-certificate claim. Maintain all four strict 1e-8 categories as the primary numerical test.

This prerequisite can be the next complete checkpoint rather than bundling a new approximation into it. It must report stagewise and complete native cost, including current coefficients, guards, solution and outputs. Replacing rational/interval work with ordinary doubles is not algorithmic novelty. Existing seconds-scale exact/reference-method timings do not isolate physical K evaluation as the dominant application cost; online proof, arithmetic and process/output costs may be substantial. A native baseline that fails the reference/guard controls blocks approximation attribution. A baseline that already meets the application budget removes the immediate need for an approximation. If it passes accuracy but misses that budget, its measured dominant cost determines whether either direction below is justified.

Also declare the actual aerodynamic update cadence and its available browser-step budget D before scoring. A small percentage improvement from a hundreds-of-milliseconds query is not the application goal. Instrument complete-stage cost in the same bounded comparison, rather than opening another elaborate oracle-only screening campaign. If non-avoidable baseline stages already exceed D, making the proposed target operation free cannot suffice; stop or redesign that contract explicitly.

## Direction 1 — contribution-preserving spatial aggregation (after the baseline)

Hypothesis: a fixed current-geometry hierarchy can replace many individual positive K evaluations by a nonzero node contribution while preserving the chosen final-load accuracy and reducing complete native cost.

The expensive work to avoid is per-member rotor/source geometry, projection/norm, fade/exponential kernel evaluation and individual coefficient materialization. A representative kernel plus a current weighted source aggregate is one concrete mechanism: schematically, K_rep * sum_C(beta_j*y_j) / nu_ir, with an independently justified approximation-error account. This expression is a proposed mechanism, not an established bound. Native candidate y changes during solving, so its aggregate must be recomputed consistently. Current beta/nu and their costs remain included.

The online method must discover groups from raw current poses, orientations, offsets and forces. It cannot receive reference-positive membership, coefficient order, saved coefficients, or a previously selected mask for free. Branch boundaries, self membership, guard precedence, caps and ordered-domain obligations must be handled by the chosen interface, with refinement/current exact fallback where required. Source orientation and rotor offsets prevent a distance-only guarantee. A group whose lower bound is zero may still be approximated nonzero, but its accuracy is not established by that choice alone.

Freeze one representative/approximation rule and one admissibility policy before a fresh holdout, not a sweep of orders or fractions on these six states. Compare against both the strongest accepted F-derived full-contribution method and an equally lean exact hierarchy under identical outputs and admission obligations. Charge preparation, build/refit, grouping, aggregates on every candidate pass, refinement, fallback, solve, storage and output consumption. Independent reference generation is offline for every arm; it cannot be a free online input.

Falsification: any required category/state failing the declared numerical gate rejects that fixed version. If satisfying accuracy forces near-singleton work, or complete cost fails its predeclared comparator/deadline gate after charging the above work, reject its practical premise. A node-count reduction or oracle accuracy pass alone is insufficient. Do not rescue a failure by altering the rule on the same holdout. Small-reference admission can authorize only the next explicitly scoped browser scaling test, not certify all 5,000-drone outputs.

Hierarchical accuracy-controlled kernel evaluation is established prior art [1,2]. The already-verified passages support that methodological direction, not this wake kernel's bound, a claimed speedup, or novelty. The project-specific question is whether nonzero aggregate accuracy and current admission can be obtained cheaply enough.

## Direction 2 — temporally valid reuse of current contributions (conditional alternative)

Hypothesis: consecutive updates permit substantial reuse of geometry/kernel work while maintaining valid current contributions, with cheap invalidation or refresh. This is distinct from the failed within-query beta/nu memoization: it must avoid repeated K construction or a substantial current spatial/graph rebuild, not only a few repeated square roots.

Use a fixed reuse policy over a prospectively frozen sequence of complete consecutive input states, including initial construction. Update current force normalizers and candidate-dependent weights/aggregates. Bound or otherwise independently assess coefficient change caused by translation, orientation, rotor-offset and force changes; crossing support, near-field, order or cap boundaries must trigger the declared refresh/fallback behavior. Reusing yesterday's K or load vector without a current error account is not evidence for this hypothesis. A previous root can be a warm start but does not by itself remove coefficient cost.

Falsification: reject the fixed policy if any required audited frame/category violates the declared gate, an invalidation misses a transition, resident storage breaches its declared budget, or refresh/check overhead eliminates the complete sequence-time benefit and deadline compliance. Compare with a fresh-current-build control in the same persistent runtime. Charge initial build, all invalidations, full refresh bursts, reaggregation, solve and output; fix the amortization horizon and include tail update cost. Do not choose a slower update rate after seeing errors. The t0/t5/t10 samples do not test frame-to-frame reuse, and the present result supplies no temporal hit-rate evidence.

Treat this as an alternative requiring its own contract and independent review, not an automatic second campaign if Direction 1 fails. No new temporal theorem, source access, seed, sequence, implementation, or allocation is adopted here.

## Evidence and citation limits

Read saved `results/check.json`, `results/analyze.json` fields, and both attempt records from `research/m31-direct-load-diagnostic-2026-10-17`. Source commit recorded by both attempts: `ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf`; manifest SHA256 `93d26849dcd0a86d18b254f8eb5babc3d13e0f46d08efc92dfc2bc5cef79635b`. Rehashed outputs match their attempt records: analyze SHA256 `8b2cee37458583fbf4b78f343134f2805221f211209ba13d53208a42eaa8624b`; check SHA256 `18caa7a9d1153adead64e3f5741dc15225d5e1fa1dd1f5b17e0c6f817046fe35`. This is a saved-data interpretation, not a repeat of the full independent postrun audit. JSON extraction, rounded display conversion and exact saved-object equality comparisons did not invoke either scientific stage.

Historical scope/cost context was read from the normalizer replication milestone/protocol, M-current adopted design/current milestone, and prior browser/current-construction/neighbor planning records. The older browser next-decision document's dense-tensor remark is superseded by the later M-current clarification and is not used as a saving here.

Citation identities and reading limits come from `research/m31-current-bound-design-2026-10-16/review/PRIOR-ART.md` (SHA256 `a35f4b75694957b6b0406a305aa5e37a9c2eb784312f81abd419f7c3d2bafd20`) and its access ledger. No new external retrieval occurred; full-paper proofs and wake-specific applicability were not newly verified.

[1] A. G. Gray and A. W. Moore, “Nonparametric Density Estimation: Toward Computational Tractability,” SIAM SDM 2003, pp. 203–211. DOI: https://doi.org/10.1137/1.9781611972733.19. Verified publisher abstract/metadata and author overview support hierarchical, accuracy-controlled kernel summation; detailed formulas/proofs were not read in that review.

[2] R. R. Curtin et al., “Tree-Independent Dual-Tree Algorithms,” ICML 2013, PMLR 28(3), pp. 1435–1443. https://proceedings.mlr.press/v28/curtin13.html. Verified publication record and partial author text support separating tree, traversal, base case and pruning. No wake-law or temporal-cache theorem is attributed to it.

No fraction/mask adjustment, solver rerun, new scientific input, source implementation, or allocation was performed for this memo. Retain the closed strict and stress failures as published evidence.
