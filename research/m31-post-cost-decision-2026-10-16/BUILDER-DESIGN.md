# Next coefficient-builder question — source-only recommendation

**ADOPT one design question: can a stable, typed receiver-row coefficient builder
reduce complete coupled-query cost beyond a matched scalar lean builder?**
This adopts source/design work only. It creates no execution allocation and
predicts no speedup. A fresh coupled-construction comparison could be useful
engineering; neither batching nor allocation removal would establish novelty.

The current approximately500ms all-pairs A result is the fastest measured arm in
its campaign, not a proven best CPU baseline. Its geometry phase includes several
operations whose individual costs were not measured. Allocation expressions in
source are not measurements of heap allocations, GC cost or time: V8 may optimize
some away. [1]

## What is distinct, and what is already known

Current build calls pairTerm four times per eligible center. Each call constructs
an eight-field diagnostic object and a temporary displacement array, although
the caller consumes only symbol and term. Positive terms become `[j,K]` tuples,
then global JS source/K arrays, then typed CSR copies. A Set collects dependencies
and is copied/sorted even though j is already ascending. These are concrete source
paths, not an attributed performance bottleneck. [2,3]

**Mere inlining, cached rotor points, four-call unrolling or scratch reuse is
insufficiently distinct.** DOT lean already uses typed axes/points, scalar
rotation without temporary vectors and an inline rotor kernel; reuse adds
refreshed geometry/flag scratch. Its report finds robust gains over allocation-
heavy legacy but mixed incremental gains over the stronger previous-zero method;
scaling stopped before N500. Support/reuse did not consistently beat lean. [4]

The remaining distinguishable mechanism is **the sparse coefficient-construction
and ownership path**: build four stable typed rows directly, then emit canonical
CSR and graph dependencies without per-coefficient objects, a Set/sort, or global
boxed-number accumulation. Inspected DOT produces four summed winds per receiver,
not the current coupled solver's retained K/a matrix, symbol census and dependency
graph. Its published result therefore does not already measure this assembly
change. This is a contract-specific engineering distinction, not a claim that
stable sparse assembly is a new algorithm.

## One concrete design

Keep all-pairs A's i→j→rotor traversal and original scalar branch/arithmetic order.
Here “batch” means one receiver's four complete source-ordered rows, not SIMD,
parallel reduction or a changed geometric approximation.

1. At each receiver, form the four world rotor points once using exactly
   `p_center + offset`, preserving binary64 grouping and signed zero. Cache the
   source position/axis values while processing that source's four rotors. These
   are known lean implementation techniques and must also be present in the
   matched scalar lean comparator.
2. Use a fused scalar four-rotor classifier that writes symbols/K into scratch
   slots rather than returning diagnostic objects. Preserve every current
   center/rotor invalid guard, near-field branch and terminal symbol. Compute
   projection lazily when first needed, with identical arithmetic; do not turn
   it into a new early rejection. Again, this known inlining layer belongs in
   both matched construction arms.
3. The proposed assembly arm owns four Uint32 source rows and four Float64 K rows,
   each with capacity N and a reset length. Append only positive terms as j
   ascends. No dense4N² coefficient array, truncation or count-first second
   geometry pass. Scratch capacity is48N bytes for IDs and K, plus small counters;
   initialization and writes are paid by the complete query.
4. After all four rotors for j, append j once to the dependency row if any K was
   positive. Ascending j makes that row unique and sorted without a Set/sort.
   After finishing receiver i, copy the four compact row prefixes in rotor order
   into a fixed-policy typed chunk writer; finalize contiguous CSR once. Count
   chunk allocation, spare capacity, final copies and peak overlap. A fixed
   chunk policy must be selected in source, not tuned on target results.
5. Keep K→a scaling, ordinary-bound sums, graph eligibility, ordered solve,
   residual and output ownership unchanged. Returned CSR must not alias scratch.
   Emit optional full symbols at their original `[i,j,r]` indices and maintain
   the same complete census. Preserve the2million-term cap and canonical failure
   progress; batching does not license dropping unsupported entries.

This design changes output construction, while retaining global i/j/rotor order.
An across-receiver vector tile is deliberately excluded: it complicates first-
failure ordering and adds a separate scheduling/cache hypothesis. JS typed arrays
do not by themselves establish SIMD execution. A WASM, native or GPU rewrite
would be another arithmetic/runtime intervention, especially for Math.hypot,
and is not hidden inside this recommendation.

## Honest comparison and reasons to stop

Current A remains an externally anchored baseline. A matched scalar lean builder
must share the inlined classifier/point caching but retain ordinary assembly;
the typed-row candidate changes assembly only. Without that separation, a gain
over A could simply rediscover DOT's known inlining benefit and must be described
that way. These are conceptual comparator requirements, not an allocated test.

Retain all current guards before the strict3m skip, all four roots, canonical
source sums, rejection semantics and complete-query setup/output-consumption
costs. Correctness would need the entire symbol tensor, CSR support/order/K,
input/admission/graph/work records and final solutions, not just an aggregate
checksum. Any later evidence would require its own authorization and frozen
protocol, independently frozen states and practical stopping rule. No retuning
or rerun of closed inputs is authorized here.

The mechanism remains **unmeasured**. Typed writes, copies and initialization may
cost more than the removed representations, while Math.hypot/profile evaluation
may dominate regardless. If the purported batch is only a thin wrapper around
four existing calls, or cannot be separated from scalar lean improvements,
reject it as the next structural question. Do not launch a grid-parameter sweep
or another branch-bookkeeping variant in its place.

Closed E/Z and L/E experiments already missed their joint usefulness gates;
roughly49% fewer center radial norms did not establish a corresponding elapsed
saving. They caution against reading speed from source operation counts. [5]
Cadence reuse changes the model evaluated at moving poses; its two-encounter pilot
retained four unresolved5ms RMS sampling checks and no accepted cadence. It
cannot make coefficient rebuild cost disappear in an exact frozen-pose query or
justify stale-matrix reuse after motion. [6]

## Inspected support and scope

Only source and saved narrative reports were read. No target arrays/raw timings
were rescored, no model or benchmark was executed, and no repository file changed.
No new external literature was needed. General tiling/data reuse is established
in the previously verified Nyland–Harris–Prins GPU Gems3 chapter31,
§§31.2–31.4/31.6; those CUDA gravitational results predict neither JS speed nor
directed-wake behavior. [7]

1. `research/m31-coupled-cost-host-2026-10-16/review/RESULT-INTERPRETATION.md`,
   sections “What the saved phases support” and “One next question”; also
   MILESTONE-SUMMARY.md. Its all-pairs diagnostic wins and phase shares are
   accepted saved-report findings here, not newly recomputed observations.
2. Same package `source/kernel.cjs:49–83`, especially64–76. SHA256
   `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a`.
3. Same package `source/reference-excerpt.cjs:5–33`, particularly7,12–16.
   SHA256 `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e`.
4. Previously verified remote source retained at
   [public exact-efficiency tree at the inspected commit](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/1336f5c416875a9651f92b58b2ed06649f25b04e/research/campaign-exact-efficiency):
   `src/exact-aero.cjs:24–49,64–113` (SHA256
   `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`);
   `REPORT.md`, “Result,” “Frozen methods and controls,” and “Independent robustness
   replication.” Public inspected tree was commit1336f5c416875a9651f92b58b2ed06649f25b04e;
   the report identifies original source checkpointc024dfc27b9e6b7cd5b39132164d1339cb95b12f.
5. `research/m31-zero-screen-2026-10-16/README.md`, “Evidence and outcome” and
   “What this means for the research”; source/control.cjs:12–35 and48–78.
6. `research/m31-airflow-cadence-2026-10-15/README.md:24–35` and
   POSTRUN-RESTART.md, opening paragraph. Prior allocation remains closed.
7. Verified literature ledger
   `research/m31-restart-2026-10-15/literature/annotated-ledger.md`, C1 row/finding;
   [primary chapter](https://developer.nvidia.com/gpugems/gpugems3/part-v-physics-simulation/chapter-31-fast-n-body-simulation-cuda).
   This task relied on the earlier verified reading, not a new retrieval.
