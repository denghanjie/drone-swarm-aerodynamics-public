# Lean repeated-cost proposal for the fixed-pose coupled pipeline

Planning only, 2026-10-16. No new model, geometry, solver, runtime or timing
execution was performed while preparing this proposal. This is a proposed new
allocation; it does not reopen any closed invocation.

## Decision to make

Measure the incremental cost benefit, if any, of ordered evaluation after paying
for complete coefficient construction, admission, required setup and a separate
final residual. The primary contrast uses the **same exact spatial grid** for
ordered and synchronous Picard solving. An all-pairs ordered implementation is a
diagnostic control for neighborhood construction, not the headline baseline.

Use only the four exposed inputs and reference records from the published swarm
transfer, result `d35cec6`, receipt `455d14f`, source
`702abf6b02d53b1008495e2fa579aabf58a445c5`:

| Input | Positive rotor terms | Unique vehicle edges | Depth | Saved Picard updates |
|---|---:|---:|---:|---:|
| n1000-t20 | 14,166 | 4,111 | 8 | 7 |
| n5000-t20 | 115,943 | 33,706 | 14 | 10 |
| n5000-t60 | 110,491 | 32,097 | 15 | 10 |
| n5000-t180 | 79,600 | 23,201 | 8 | 8 |

These are already known, mild admitted cases: maximum tilt below 8.37 degrees,
ordinary bounds below 0.356, and no order violations. The prior independent
review passed 581 grouped checks, including 304 million exact symbol entries.
Its 5.553-second supervisor duration was explicitly not a timing experiment and
must not be used as a speed baseline. The present repetitions are development
measurements on these same records, not independent scenarios or stronger
theorem-domain evidence.

Earlier CPU work already had a spatial neighborhood in its original B method.
The omission ablation found median paired C/Z ratios 1.003815 and 0.993453 and
failed its useful incremental positive-omission criterion. The zero-screen
package accounted for about 90–92% of summed savings; subsequent simplifications
also missed their usefulness rules. Its fastest reported 5,000-source complete
query median was about 1.059 seconds, under a different uncoupled source/nominal
contract. Do not compare that time numerically with the new coupled results.
That existing exact-zero-screen package is a potentially stronger baseline than
the simple grid here. Adapting it is excluded because it would introduce another
question. Therefore this campaign cannot claim best available CPU efficiency,
generic algorithmic superiority, or novelty.

## Three complete-query methods, plus one separate cache workload

| Label | Neighborhood | Solve | Role |
|---|---|---|---|
| A | Every directed center pair | Ordered | Diagnostic reference cost |
| B | Conservative exact grid | Ordered | Primary candidate |
| C | Identical conservative exact grid | Synchronous Picard | Primary comparison |

Use one common input preparation, pairTerm, coefficient representation, root
closure and residual implementation. Change only neighborhood enumeration and
the solve schedule. Every retained source row is sorted by ascending source ID;
do not accidentally change floating accumulation order with hash-cell order.
Keep binary64, unchanged constants and nominal motor states, exact hard support,
56 bisection loop iterations for positive alpha, exact root one at alpha zero,
Picard initialization at all ones, first stopping test at update one,
max-log-change threshold 1e-11, cap 64 and a separate final residual. No root,
precision, tolerance, support, seed or parameter sweep.

Both complete grid queries rebuild their geometry, grid, neighbor lists, positive
K, CSR, a and admission decisions on every invocation. Ordered sorting and
ordering-specific scratch preparation are inside B's measured setup. Picard
must not be charged for building an unused ordered schedule just to make B look
better: it can check each positive edge against the descending-height/ascending-ID
key directly during the common graph-admission scan. The same tie convention and
domain decision apply. Dependency depth is a qualification diagnostic, not a
required repeated solver operation. Record each method's actual required setup.

The separate **cached-matrix O/P workload** reuses one already qualified immutable
CSR/a, original f0/S0 and ordered schedule per case. Compare ordered and Picard
solves, each with fresh scratch, fresh initial amplitudes and a separate residual.
No previous solution is a warm start. Cache preparation/validation bytes and its
one-time cost are reported separately; this workload explicitly excludes geometry,
admission and matrix construction. Do not combine its result with full-query
times or infer an amortization break-even from unrelated median components.

## Exact grid contract

Start with one simple grid, not a tuned collection: center-position cells of
width 3 m. Enumerate a conservatively expanded axis-aligned neighborhood, then
apply the unchanged exact center guard and Math.hypot(center delta) < 3 test to
every enumerated candidate before calling pairTerm. Padding changes lookup
coverage only; it never changes a support or admission threshold. Do not add
positive omission or source-level wake zero screening.

A practical fixed lookup specification is radius `3 + 1e-8` m for cell-range
enumeration, with positions bounded in absolute value by 2^20 m and safe integer
cell keys. The static implementation review must justify that this padding covers
subtraction/division rounding in that admitted lookup range. This is a broad-phase
coverage argument, not permission for epsilon reclassification. Freeze it before
any new evaluation; do not shrink the padding after inspecting timings.

Preserve the full symbol semantics outside enumerated neighbors. The original
all-pairs code checks invalid center ranges before classifying a far pair as one.
A grid cannot silently skip those errors. Before using the grid, perform a cheap
global finite-coordinate/bounding-box guard sufficient to prove that every
directed center pair passes the original component and distance guards. For
example, each coordinate span <= 256 m and the sum of the three spans <= 500 m
provide slack beneath the 257 m component and 512 m distance limits. Check the
lookup-coordinate/key range too. If this sufficient fast-path premise fails,
fall back to the exact all-pairs enumeration in that query and record the fallback.
Do not reject an otherwise valid state merely because the grid fast path is
unavailable. All guard/fallback work is timed.

The non-enumerated entries are symbol one only under that established premise;
self stays one. Candidate IDs must be unique. Save candidate-pair counts,
center-distance tests, exact eligible pairs and pairTerm calls separately. A
reduction in tests is not itself a measured speed benefit. If the grid falls back
on a planned case, retain the result and identify it as a fallback comparison.

## Correctness first, against the existing complete reference

Pin the four original input bytes and the published full symbols, CSR, input /
admission / graph records, direct and Picard loads and residuals. Do not regenerate
or replace the references. The earlier independent Python review is the numerical
oracle provenance; this campaign need not rerun that expensive review.

Qualification performs each builder once per case: eight full geometry builds.
Each resulting matrix is solved both ways: sixteen qualification solves, each
with its own residual. The builder can emit the full canonical symbol stream in
qualification mode; the compact timing path uses the same predicates and sparse
construction without allocating or persisting an N-by-N symbol tensor.

Require complete exact symbol equality, exact CSR offsets/source support/order,
K within 2e-12 absolute plus 2e-12 relative, exact admission and graph decisions,
and all returned amplitudes/rotor forces within 1e-9 relative of the frozen
reference. Preserve generating loads separately from the final residual map.
Require finite solution values, correct root/work counters, the unchanged
convergence rule and iteration cap, and independently checked saved-reference
residual/mismatch tolerances. Freeze concrete residual tolerances in the final
source specification; inheriting 1e-9 log residual and 2e-9 normalized mismatch
from the transfer checker is sufficient here. Do not use a checksum as a
substitute for these qualification comparisons.

Add only a small lookup/control set: eight two-vehicle cases. Six use receiver
x=0 or x=-6 and source x equal to nextDown(receiver x+3), receiver x+3, or
nextUp(receiver x+3), with y=z=0. The other two use coincident centers and receiver
at zero/source x=258, respectively; the latter must exercise the all-pairs guard
fallback and retain invalid-center symbols. Use identity quaternions and the
unchanged positive hover nominal forces. Construct adjacent values with explicit
binary64 nextDown/nextUp.
Both builders must agree on complete symbols, support and domain outcomes. These
are lookup/admission regressions, not a performance population. The cases need no
load solve when their domain rejects. Existing reference classification handles
the other support gates; do not expand this into another boundary campaign.

Any qualification mismatch stops before timing. During timing, save duration,
phase values and counters before validating outputs. After the clock stops,
compare every returned matrix/solution/residual array to its qualified result;
also require exact per-method output fingerprints and counters for repeatability.
Save maximum discrepancies, hashes and any full failing
row. Stop on a numerical/runtime mismatch; never discard a slow but correct call.

## What the complete-query clock covers

Start with the same immutable, decoded 17-column states resident in memory. Input
file reading/decoding is measured once and reported separately. Each complete
query's uninterrupted wall timer covers:

1. Input/nominal census, quaternion-derived axes and four rotor offsets.
2. Grid or all-pairs enumeration setup, including global guard/fallback checks.
3. Exact center tests, all eligible rotor classifications, positive K construction,
   canonical CSR construction and source sorting.
4. S0/a construction, scaled-cap and complete domain checks, graph eligibility,
   and method-required solve preparation/order construction.
5. All solver updates/closures, convergence tests and output assembly.
6. A separate final map, log residual and source/receiver consistency mismatch.
7. A small fixed output checksum shared by all methods.

Record phase boundaries with a monotonic high-resolution clock and record the
total around the entire call; report any unassigned remainder. Allocation,
instrumentation and GC occurring inside a call remain in its time. Use coarse
stage timers, not per-term profiling. Preserve the same receiver-level resource
guards across methods. No forced/selective GC, JIT flags, affinity tuning or
parallel benchmark processes. This is an instrumented hot-process CPU query,
not cold-start latency or a model of total application frame cost.

## Keep diagnostic persistence separate

Qualification enables full symbol census and Picard trace capture. Write one
canonical diagnostic bundle per case from an already qualified result, retaining
all reference-equivalent geometry, coefficients and final solutions. Record the
diagnostics-enabled qualification time separately, then time compression, hashing,
serialization and filesystem writes. Do not estimate incremental diagnostic
overhead by subtracting unrelated timing medians. No extra scientific solve is
needed to write that bundle. State whether writes use fsync; choose ordinary
buffered writes here and do not label them durable-storage latency.

These one-off diagnostic-I/O measurements are not repeated storage benchmarks.
They are excluded from the compact query timer and must appear alongside it, not
disappear into the phrase "end to end." A full-census artifact workload and a
compact coefficient-to-residual workload are different interfaces. Do not save
full output tensors for every timing repeat: retain the first qualified bundle,
per-repeat hashes/counters/comparison results and bounded failure witnesses. A
saved-record reviewer can audit those recorded assertions, not independently
recover every transient timed array from a hash.

## Repetitions, order and measured environment

Use one fresh Node process. After qualification, run exactly one warmup per
case/method, recording and validating it but excluding it from timing summaries.
Then six measured blocks per case. Use all six permutations:

```text
ABC, BCA, CAB, CBA, ACB, BAC
```

Each method occupies every within-block position twice; every directed within-block
predecessor pair occurs twice. Interleave the four cases by rotating their fixed
listed order by block index modulo four; use permutation `(block + caseIndex) % 6`
for each case. Retain that exact schedule. This balances method order, while not
claiming to remove all JIT/GC, thermal, background-load or carryover effects.

After the full-query schedule, give cached O/P one warmup each per case and six
measured paired blocks, alternating OP/PO three times each. Rotate case order in
the same way. Do not pool these times with complete-query observations.

The fixed allowance is 84 complete-query timing calls (12 warmup, 72 measured),
56 cached timing solves (8 warmup, 48 measured), eight large qualification builds
and sixteen large qualification solves. The eight tiny controls each call both
builders once. Every solve has one separate residual. No pilot or adaptive extra
warmup/repetition is permitted.

Record actual CPU model, physical/logical core counts, installed RAM, architecture,
OS/kernel version, Node/V8 versions and execution flags, executable hash, clock
API, process/thread configuration, and start/end power or low-power state and
coarse system-load observations where available. Report unavailable fields as
unknown. Record peak RSS with platform units/semantics. Do not assume the old
Apple M4 / Darwin 25.5.0 / Node 24.19.0 environment still applies. Omit serials,
hostname, username and private executable paths. No installations, updates or
hardware/environment switch inside the allocation.

## Reporting, bounds and stopping

Report every raw duration; per case give total and phase median/min/max, paired
B/C ratios and absolute time differences, plus A/B as a diagnostic. Ratios are
computed within blocks before summarization, not from marginal medians. Show the
sum-of-matched-block stage contributions when attributing time differences;
separately averaged medians need not add to a total. Report root closures,
bisection iterations, source multiplications, center tests, eligible terms and
bytes alongside wall time, without treating them as interchangeable cost units.

The primary outcome is the observed incremental B/C cost and its consistency on
each fixed state, not an omnibus "speedup" verdict. A predeclared descriptive
practical signal, if a binary next-step rule is wanted, is paired median B/C <=
0.95 and at least five of six strict wins on each of the three 5,000-state inputs;
the 1,000 case remains contextual. This is an engineering preference, not a
statistical significance test. Prefer publishing the actual per-case differences
even when that optional criterion fails. No confidence intervals across swarms,
trajectory generalization or device populations are justified by these repeats.

Use one 300-second science invocation with a 295-second cooperative cutoff and
external 300-second termination, sampled 1.5-GiB process RSS guard, the inherited
2,000,000-positive-term/case cap, and 128 MiB of new scientific output with 4 MiB
reserved for failure. Known supervisor logs/locks/provenance are separate and
bounded/inspected; the diagnostic symbol cap remains 64 MiB per case. One small
saved-record audit receives 60 seconds and performs no geometry, roots or timing
reruns. Missing coverage is incomplete, not an excuse to trim the matrix.

Keep execution machinery lean: one frozen script/config, existing pinned kernels,
one manifest/source review, one consumed invocation record, one saved-record
review and one result report. No browser/runtime qualification apparatus, viewer
rewrite, environment experiment, extra optimization family or new physical data
collection is needed for this CPU question.

Stop on failed qualification, nonconvergence, a repeat mismatch, timeout, memory
or output cap; preserve the completed prefix and current witness. A complete
negative timing result closes this allocation normally. No retry, parameter
adjustment, longer run, new snapshot or stronger-baseline adaptation follows
automatically. A later proposal can use the measured phase bottleneck to choose
one further question, or conclude that ordering contributes little to total cost.

All conclusions remain about a hypothetical fixed-pose coupled load contract on
historical airflow-OFF development snapshots. They establish neither browser or
flight cost, real-time feasibility, physical accuracy, unsteady wake fidelity,
new independent scenarios, best implementation performance nor novelty.

## Documents inspected

- `m31-swarm-coupling-transfer-2026-10-16/MILESTONE-SUMMARY.md`,
  `results/analysis.json`, `results/run.json`, and the previously reviewed frozen
  `PROTOCOL.md`, `SCHEMA.md` and checker.
- `m31-source-omission-2026-10-16/PROTOCOL.md` and `README.md`.
- `m31-omission-ablation-2026-10-16/PROTOCOL.md` and `README.md`.
- `m31-zero-screen-2026-10-16/PROTOCOL.md` and `README.md`.
- `m31-body-runtime-replication-2026-10-16/OVERNIGHT-SUMMARY.md` for the explicit
  distinction between CPU component results and the still incomplete browser /
  flight / physical goals.

All paths above are relative to the public repository's `research/` directory.
