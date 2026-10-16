# Coupled-cost campaign: source-only fairness and evidence audit

Prepared 2026-10-16 for `research/m31-coupled-cost-2026-10-16`. This review inspected `PROTOCOL.md`, `SCHEMA.md`, the candidate driver/kernel/reference and runner, plus the preceding planning documents. It did not execute/import JavaScript, generate/evaluate controls, decode target states, solve roots, run a checker, or measure timings. Source fingerprints and byte comparisons are file inspection, not numerical pilot runs. The independent grid review and saved-record checker are separate deliverables.

**Disposition:** no remaining blocking discrepancy found in the inspected candidate/runner source after the corrections below. This is readiness for the coordinator's final source-freeze process, conditional on complete dependency pins, final checker review and independently observed remote publication. It is not permission to skip those gates and is not a prediction of numerical or performance success.

## Fairness and scope

The adopted design is three complete-query arms: A all-pairs+ordered, B conservative grid+ordered, C the same grid+Picard. B/C isolates the incremental solver/setup question; A/B diagnoses indexing. The earlier 2×2 proposal is not being claimed as executed. Omitting all-pairs/Picard narrows the inference but does not invalidate these defined comparisons. A must not be presented as the strongest prior CPU implementation; older fixed-source baselines already used a grid and some used additional exact-zero screening.

Both grid arms use the same builder. Every full query recomputes input census, quaternion-derived geometry, certificate/index/candidates, exact terms, CSR, scaled coefficients, admission and common graph eligibility. B pays for its ordered schedule; C checks eligibility using the same descending-height/id key without constructing an unused schedule. A uses a direct integer source loop without an unused box scan, Map or per-receiver N-element ID vector. Retained source order remains ascending. No positive approximation, altered root algorithm or support change is mixed into the index comparison.

The common root closure, synchronous initialization/stopping, four-rotor output and separate residual work follow the preceding coupled contract. Source dependence remains the assumed fixed-shape total-load scaling with historical unequal nominal motor forces. P is also restricted to admitted descending-eligible states in this campaign; it is not a new cyclic-solver qualification. The copied pairTerm is byte-identical to the preceding frozen reference.

Full-query clocks cover fresh resident-state preparation through usable returned solution/residual and a small checksum. They exclude file decoding/reference loading, complete tensor/Picard trace capture, postclock comparisons/hashes and persistence. Allocations, receiver-level RSS/time guards and GC within the call remain charged. Because Picard performs more map visits, it also performs more of the same per-visit instrumentation; any measured gain belongs to these instrumented implementations, not a separately measured intrinsic arithmetic cost. Coarse phase spans are disjoint, and the outer total retains the unassigned remainder.

Cached O/P is explicitly a different workload: one qualified immutable grid CSR/a, nominal data and schedule are reused; every solve starts from ones with fresh scratch and has its own residual. There is no previous-solution warm start. Setup origin/validation time and typed CSR bytes are reported, while retained states/geometry/graph/solutions and JS object overhead are disclosed. Cached results cannot substitute for complete-refresh latency or establish pose-change cache validity.

## Exact schedule and accounting

Source inspection gives the prescribed schedule:

| Work | Count if completed |
|---|---:|
| Tiny controls | 21 |
| Tiny builder calls, all and grid each | 42 |
| Large qualification builds | 8 |
| Large qualification solves, each followed by residual | 16 |
| Full-query warmups | 12 |
| Full-query measured calls | 72 |
| Cached warmups | 8 |
| Cached measured calls | 48 |
| All recorded timing calls | 140 |

Thus a completed invocation has 92 large builds including timed full queries and 156 large solves including cached/qualification calls, each with one residual evaluation. These are schedule arithmetic, not observed execution counts. Early stopping leaves an explicitly incomplete prefix.

The six full permutations are ABC, BCA, CAB, CBA, ACB and BAC. For each original case index, `(block+caseIndex)%6` visits all six once; every method occupies each within-case position twice. Case order rotates by block modulo four. Full warmups use fixed case order and ABC. Cached warmups use OP, followed by three OP and three PO measured blocks with the same case rotation. Cached timings occur after all full timings; they cannot be treated as interchangeable samples of a common clock/environment phase. The final driver explicitly checks control/qualification/call totals and every call's expected identity before completion.

`logicalDirectedPairs` records N(N−1), while gathered candidates, actual center tests and certified skips are distinct. Eligible centers, pair calls and positive coefficients retain their original meanings. All grid-fallback cost remains charged. Root closures, positive-alpha bisection loops and term multiplications are separated from residual work. A smaller count is not a time measurement. No operation-counter unit should be relabeled as completed vehicles, hardware instructions or a uniform-cost operation.

The practical B/C signal is prospectively defined per large case: median of six block-paired ratios at most .95 and at least five strict B wins, required on each of the three N=5,000 records. It is an engineering decision rule, not a statistical significance or scenario-generalization claim. Phase attribution must use matched-block sums/differences; marginal medians need not sum to a total. The independent saved-record reviewer is responsible for reconstructing these summaries; it was not yet finalized during this audit.

## Qualification and repeat evidence

Both full diagnostic bundles per input are saved with complete symbols, CSR K/a, graph/admission/counters and both solutions. Qualification checks exact classification/support/order/decisions, coefficient tolerances, all returned source/rotor alpha/x/T values and residual-map values, work, convergence/iterations and residual/mismatch bounds against the previously independently checked reference. The revised source also compares all saved Picard iterates and exact lastChange. Any qualification mismatch stops before timed calls.

The 21 small controls retain exact position tokens, including signed zero and nonfinite values, and both builders' complete classifications, sparse outputs, admission, graph and work. Their expected grid/fallback choice is explicit. A separate recount checks symbol counts. This is a finite implementation matrix; cross-builder agreement is not a mathematical proof of all possible geometry. Independent grid reasoning and the known far-invalid fallback witnesses remain relevant.

Every completed timed observation is first written as a raw record. Outside the clock, the driver compares all K/a and solution arrays, CSR offsets/source IDs, geometry counts, certificate and checksum to the matching qualified path, and requires exact per-solver matrix/solution fingerprints. Validation maxima, first failing scalar and raw-record pin are retained. A failure retains the full available solution plus comparison record subject to resource limits. Full timed matrices are not duplicated: a saved-record review can audit qualification arrays, hashes/counters and recorded comparison assertions, but cannot reconstruct each transient array or independently prove a measured duration from a hash.

Checksums are a deliberately small common output-consumption cost, not a numerical correctness substitute. Canonical fingerprints exclude diagnostic P traces and timing values; qualification trace verification is separate. Consumers must follow the documented JS JSON/typed-byte serialization exactly, especially numeric formatting, field order and ordered default fields.

## Findings reported and corrections reread before freeze

| Finding | Inspected correction | Status |
|---|---|---|
| Timed checksum was emitted without comparison, and repeat certificate equality was absent. | Both are compared to the qualified output after the clock and participate in validation.pass. | Resolved. |
| Qualification compared final arrays/work/iteration count but omitted P trace and lastChange. | Every flattened saved P iterate is compared at the declared tolerance; lastChange is exact. | Resolved. |
| Completion had no explicit final schedule/count gate. | Driver reconstructs expected identities and checks 21 controls, 8 qualifications, 140 calls and every call's workload/id/method/block/warmup. | Resolved for the pinned four-input schedule. |
| Persistence's I/O/hash/serialization bucket also recomputed graph sorting/depth. | Full diagnostic graph is computed inside qualificationComputeMs and reused by comparison and persistence. | Resolved. |
| A raw-record write failure could lose the just-completed duration from catch context. | progress.currentTiming is assigned before attempting that write. | Resolved for available caught-failure context. |
| Failure after setting complete could leave partial-evidence.complete true. | Catch resets complete=false. | Resolved. |
| External RSS errors were silently represented as zero samples. | Supervisor separately records successful sample and sample-error counts. | Resolved as disclosed sampling evidence; if rssSamples=0, the zero-initialized peak must be reported as unavailable, not a measured zero. |
| execArgv did not disclose inherited NODE_OPTIONS. | Candidate runner refuses nonempty NODE_OPTIONS; candidate also requires empty NODE_OPTIONS and no exec arguments, with the fact recorded. | Resolved. |

The corrections do not change the target law or use observed numerical outcomes; none was available from this campaign during this review.

## Resources, retention and reproducibility

The candidate has a 295-second cooperative clock, receiver-level sampled RSS checks at 1.5 GiB, a per-build 2-million-positive-term guard, a 64 MiB per-symbol-artifact compressed cap and 124 MiB normal-write limit with 4 MiB reserved within 128 MiB for caught failure/partial records. The retained evidence index contains bounded small comparison/control/call records rather than all qualification arrays, so emergency records do not intentionally duplicate the full tensor payload. Normal full bundles and completed call files remain authoritative. Under a hard kill, process crash or disk failure, only already-written artifacts and supervisor context may exist; no complete current-call output is guaranteed.

The runner verifies the supplied manifest digest, current expected source commit, exact committed manifest and every listed root-relative file's hash/length/committed bytes before consuming an exclusive candidate/review lock. Python optimization is rejected so assertions remain active. Separate process-group invocations enforce 300/60-second caps, monitor RSS/logs/total result-directory bytes and retain return/termination status. Sampling is coarse and can overshoot; it is not a hard real-time memory or disk boundary. The supervisor's elapsed duration is explicitly not the query benchmark measurement.

Environment metadata includes actual Node/V8 and executable hash, CPU/core/RAM/platform information, power fields where available, clock/thread scope and start/end load. Private executable paths, user/host names and serials are omitted. Controlled error phrases/classes keep candidate JSON safe; raw stderr and supervisor artifacts still need the required publication privacy inspection.

Before dispatch, the final root-relative source manifest must include this package's numerical source, copied reference, protocol/schema, runner and finalized reviewer, plus every consumed preceding input/index/reference JSON/symbol/CSR and the earlier independent-review provenance needed for its oracle claim. Final source/dependency and remote-publication verification are not completed by this local static note. Existing allocations remain closed, and the new locks must never be removed for a retry. A correct negative timing result closes normally.

## Reviewed source identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 8578 | `151515893ee582131255583a61ec795489827f7e7615ff47f79b9de435947751` |
| `SCHEMA.md` | 6095 | `5e2054037c1929c0a13ded56a52aa748424dbf52b71a983a67f5ae6cdaec0548` |
| `source/experiment.cjs` | 17107 | `af36eab1f047778fecb0b831db35cdb156f1e8c7517252605eceed94193fea23` |
| `source/kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `source/reference-excerpt.cjs` | 2731 | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| `source/run.py` | 3844 | `75844e3748b5402139396555c2fe2a7d36a47a2a3268cc546845ec00a58499b4` |

The review applies to these bytes. Later changes need a recorded diff review. No result on accuracy, timing, memory fit, physical validity, real-time capability, superiority over all CPU methods or novelty follows from this source-only disposition.
