# What the saved 180-drone capacity pilot establishes

The unchanged prepared reference completed the fixed 64/180/180 allocation and
passed both exact accuracy comparisons and the separately declared practical
pilot hurdle. The dense 180-drone case is meaningful nonzero evidence: it
contains 3,056 positive rotor/source terms and 600 nonpoint root boxes. The
sparse case has no positive terms and 720 exact unit roots. Together they show
that this particular reference implementation can finish these two exposed
static 180-drone workloads within the chosen offline budget. They do not
establish capacity for arbitrary 180-drone scenes or for 5,000 drones.

This interpretation reads only saved JSON and frozen source text. It verified
the six result/profile pins against the saved index and reconciled counts from
the profiles with the returned counters and coverage records. It imported no
scientific module, regenerated no input or reference, executed no profile and
ran no repeated timing trial. Only this interpretation file was authored.

## Saved evidence and exact meaning of the pass

The [result index](../results/index.json) is 8,528 bytes, SHA256
`224b2c29a5a6b4a3f4ab5bfa5344124a0fe6720c6d63a652368a96fd6fbeff4e`.
It identifies source commit `7528347a34c6638429430268ad6cc9e4bcb6e5f0`, source
manifest `d404173845985fd2eef76c9526adefb981c1486a49f7b8aacd1a6e565cf9ba5f`,
767 preserved source pins, three complete calls and 45,455 suffix calls.
`accuracyQualified` and `capacityHurdlePassed` are both true.

The moving 64-drone control is the entire saved prepared-reference wire,
including coefficient endpoints and coverage. Its new file is also byte
identical to the saved control. Both 180-drone cases retain exact raw and
prepared words, exact stable-ID positive support against both saved producer
methods, and every independent root and signed rotor/collective/force/moment
box endpoint. New 192-bit pair intervals are contained by exact rational
inequalities in the saved 96-bit producer bounds. Independent saved 192-bit
pair equality is unavailable because those older independent records did not
store pair intervals. The older producer schema also lacks a saved solve
traversal order. Neither unavailable comparison is silently counted as passed.

No old control, full oracle or native/browser call was rerun. The previous
24-case qualification and saved audit remain prerequisites. This checkpoint
does not extend native error qualification or provide physical validation.

## Outer wall observations

All values below are seconds as saved, without subtracting instrumentation.
These outer phases are measured separately; they are not cProfile cumulative
times. Columns follow the actual fixed execution order.

| Outer phase | Fresh-a, 64 | Dense, 180 | Sparse, 180 |
|---|---:|---:|---:|
| Input and baseline loading | 0.005863165482878685 | 0.020704584196209908 | 0.008669999428093433 |
| One profiled regeneration | 2.5174198327586055 | 12.317360833287239 | 1.7540237503126264 |
| Profile serialization and write | 0.009220832958817482 | 0.006884874776005745 | 0.006372625008225441 |
| Full reference serialization and write | 0.00846733245998621 | 0.042237915098667145 | 0.009204832836985588 |
| Exact saved comparison and accounting | 0.0012408336624503136 | 0.02104749996215105 | 0.0014746664091944695 |

Module/constant setup was `0.01441966649144888` seconds. Closure verification
was `0.20223683305084705` seconds. The saved outer allocation observation was
`16.95629358291626` seconds, measured through closure verification before final
index serialization and stdout. It is not a process-exit wall measurement.
The three regeneration observations sum to `16.58880441635847` seconds.
Summing the named, non-overlapping outer phases, setup and closure verification
gives `16.946850078180432` seconds; the approximately 0.00944-second difference
is outer work not assigned to those phase fields. It is not a missing
scientific stage and is not distributed among functions.

Each profiled regeneration was below the prospective 60-second hurdle.
These are three single ordered observations, not means, medians, confidence
intervals or latency guarantees. cProfile charges and perturbs execution,
especially code with many small calls. There is no unprofiled companion run
or calibration from which to estimate that perturbation. Earlier all-pairs,
tree-first, prepared-reference, Node and browser clocks have different scopes,
inputs or instrumentation; no speedup ratio is inferred from them.

## Resident memory is a lifetime high-water mark

The final observed macOS `ru_maxrss` was **127,139,840 bytes = 121.25 MiB**,
below the separate 1 GiB hurdle of 1,073,741,824 bytes. This observation was
sampled through closure before the final index write. It is a process-lifetime
peak that includes earlier cases, imported tooling, baseline parsing and
serialization; it is not an isolated memory measurement for any case.

| Sampling point | Lifetime peak, bytes |
|---|---:|
| Before fresh-a | 79,953,920 |
| After fresh-a regeneration / case | 94,699,520 |
| Before dense | 94,699,520 |
| After dense regeneration | 101,318,656 |
| After dense case | 127,139,840 |
| Before / after sparse and through closure | 127,139,840 |

The unchanged value during sparse does not mean that sparse allocated no
memory. Likewise, subtracting adjacent readings would not yield per-scene
memory use. The hurdle is observational, not a hard OS memory cap, and cannot
be multiplied into a justified larger-N memory allowance.

## Workload represented by the saved wires

These counts are derived from complete saved pair, root and coverage arrays,
then checked against the index work counters. A logical pair here is one
receiver rotor/source-drone query, so the count is `4*N*(N-1)`.

| Saved count | Fresh-a, 64 | Dense, 180 | Sparse, 180 |
|---|---:|---:|---:|
| Logical rotor/source queries | 16,128 | 128,880 | 128,880 |
| Pairs covered by exact zero-node proofs | 8,720 | 94,173 | 125,540 |
| Evaluated suffix calls | 7,408 | 34,707 | 3,340 |
| Evaluated scalar zeros | 7,180 | 31,651 | 3,340 |
| Positive terms | 228 | 3,056 | 0 |
| Rejected / undecidable scalar terms | 0 / 0 | 0 / 0 | 0 / 0 |
| Receiver/rotor rows with positive terms | 123 | 600 | 0 |
| Receiver drones with positive terms | 34 | 150 | 0 |
| Saved root boxes | 256 | 720 | 720 |
| Nonpoint root boxes | 123 | 600 | 0 |
| Exact point roots equal to one | 133 | 120 | 720 |
| Zero terminals | 874 | 4,756 | 2,912 |
| Leaf terminals | 958 | 6,224 | 664 |
| Total terminals | 1,832 | 10,980 | 3,576 |
| Node visits / node-rule tests | 3,408 / 15,768 | 21,240 / 99,720 | 6,432 / 20,980 |

For every case, zero-node pair count plus scalar-zero count plus positive count
equals the complete logical count. Across the allocation there are 273,888
logical queries, 3,284 positive terms and 723 nonpoint boxes among 1,696 roots.

The zero-terminal rule counts also show why the two static grids are different
workloads. Dense uses 2,596 radial and 2,160 upstream terminals. Sparse uses
2,444 neighbor and 468 upstream terminals. Fresh-a uses 340 upstream,
252 near-outside and 282 radial terminals. A terminal covers a permutation
range; these terminal counts are not counts of individual zero pairs.

Dense therefore exercises nonzero coefficient evaluation and nontrivial
root/load propagation. Sparse chiefly exercises exclusion, binding checks and
the zero-input root path. Neither static upright grid spans moving arbitrary
orientations, near-domain decisions, global fallback or general positive
support patterns. Their inputs were already exposed, so this is a regression
and feasibility diagnostic rather than fresh confirmatory evidence.

## What the complete profiles say

The saved profiles contain 229 / 191 / 177 function records and
17,369,068 / 85,838,401 / 12,365,450 total function calls, respectively.
All caller edges were retained. The JSON's own-time totals are
`2.5171767000000003`, `12.316766124000013`, and `1.7297688010000005` seconds.
The prepared entry-point cumulative times are `2.5173614580000003`,
`12.317302709000002`, and `1.753965167` seconds. These profiler aggregates and
the separately observed outer walls are preserved as different measurements;
they are not forced to equal or used to infer unmeasured profiler overhead.

Own time excludes time attributed to called functions. Cumulative time
includes descendants and overlaps with their entries. The following are the
five largest **own-time** entries in each saved profile. Times are displayed
to nine decimal places; the linked JSON retains the original numbers.

| Case | Function | Total calls | Own seconds | Cumulative seconds |
|---|---|---:|---:|---:|
| Fresh-a | `prepared.snapshot` | 1,563,077 | 0.401097399 | 0.785425222 |
| Fresh-a | `builtins.isinstance` | 5,480,205 | 0.240484503 | 0.323690360 |
| Fresh-a | `math.gcd` | 1,241,367 | 0.236031646 | 0.236031646 |
| Fresh-a | `fractions.forward` | 643,902 | 0.138409921 | 0.803088325 |
| Fresh-a | `fractions._richcmp` | 369,935 | 0.134730452 | 0.285131398 |
| Dense | `prepared.snapshot` | 7,281,405 | 1.929684955 | 3.784770754 |
| Dense | `builtins.isinstance` | 26,325,889 | 1.202183690 | 1.658251925 |
| Dense | `math.gcd` | 6,118,785 | 0.785040157 | 0.785040157 |
| Dense | `fractions.forward` | 3,411,514 | 0.752152205 | 3.829725051 |
| Dense | `fractions._richcmp` | 2,058,601 | 0.719068945 | 1.568401383 |
| Sparse | `prepared.snapshot` | 757,069 | 0.203126315 | 0.395186221 |
| Sparse | `builtins.isinstance` | 3,166,855 | 0.162140563 | 0.248402957 |
| Sparse | `fractions._richcmp` | 455,269 | 0.157886569 | 0.346961274 |
| Sparse | `fractions.forward` | 516,206 | 0.107442990 | 0.497370426 |
| Sparse | `fractions._from_coprime_ints` | 595,479 | 0.091403345 | 0.123340942 |

`snapshot` is recursive: its primitive-call counts are 52,691 / 245,292 /
25,723, so the much larger total counts do not mean that many pair evaluations.
Its cumulative value includes snapshot descendants, sorting and type checks;
it must not be added to those functions' cumulative values.

The two nested `regenerate_scene` entries each have one call per case. They
are the prepared wrapper and its tree dispatcher, not two scene executions.
After those two enclosing entries, the five largest cumulative entries are:

| Case | Function | Cumulative seconds |
|---|---|---:|
| Fresh-a | `tree.visit` | 2.102760459 |
| Fresh-a | `tree.scan` | 1.514223101 |
| Fresh-a | `prepared.oracle_case` | 1.494210035 |
| Fresh-a | `fractions.forward` | 0.803088325 |
| Fresh-a | `prepared.snapshot` | 0.785425222 |
| Dense | `tree.visit` | 10.714766857 |
| Dense | `tree.scan` | 7.303022534 |
| Dense | `prepared.oracle_case` | 7.176649458 |
| Dense | `fractions.forward` | 3.829725051 |
| Dense | `prepared.snapshot` | 3.784770754 |
| Sparse | `tree.visit` | 1.520203295 |
| Sparse | `semantic.zero_rule` | 0.979450264 |
| Sparse | `tree.scan` | 0.524145084 |
| Sparse | `prepared.oracle_case` | 0.515478503 |
| Sparse | `semantic.times` | 0.513049452 |

These rows are a navigation guide into the call graph, not additive phases.
In particular, `visit` contains `scan`; `scan` contains the prepared oracle;
the oracle contains context/operand checks and the scalar suffix. Fraction
operations occur throughout several of these paths.

Selected routines make the remaining work easier to locate. Every cell below
is **cumulative seconds**, and the rows overlap.

| Routine | Fresh-a | Dense | Sparse |
|---|---:|---:|---:|
| Original `pair.prepare_one` | 0.069481960 | 0.004375467 | 0.004280466 |
| Original `pair.preparation_valid` | 0.015269748 | 0.037261671 | 0.037610957 |
| Prepared `_context` | 0.469944189 | 2.252155272 | 0.238906510 |
| Prepared `_lookup` | 0.375182051 | 1.828771804 | 0.175041240 |
| Prepared `_oracle_suffix` | 0.637588008 | 3.014569954 | 0.115303568 |
| Semantic `zero_rule` | 0.580544794 | 3.360346196 | 0.979450264 |
| Semantic `reference_roots` | 0.279984417 | 1.441433417 | 0.063594041 |
| Semantic `bisect_cubic` | 0.250361302 | 1.289480666 | 0.002861193 |

Repeated preparation is absent, but the reference still performs substantial
binding checks, exact node proofs, scalar arithmetic and root work. The dense
profile does not identify preparation as the dominant remaining cost. It
also does not establish that removing binding checks would be valid or that
their unprofiled cost is proportional to their cProfile share. Those checks
protect the qualified reuse contract. The upright static grids' low original
preparation time is not a general preparation estimate for rotated motion.

## Profile calls reconcile with the counters

The comparisons below use total function calls from the complete saved
profiles, never a new invocation. Each listed equality was checked.

| Profiled routine or identity | Fresh-a | Dense | Sparse |
|---|---:|---:|---:|
| Original `pair.prepare_one` | 64 | 180 | 180 |
| Original `pair.preparation_valid` | 64 | 180 | 180 |
| Prepared `oracle_case` = `_oracle_suffix` = saved suffix counter | 7,408 | 34,707 | 3,340 |
| Prepared `_lookup` = saved operand lookups = twice suffix count | 14,816 | 69,414 | 6,680 |
| Prepared `_context` = suffix count + twice drone count | 7,536 | 35,067 | 3,700 |
| Semantic `zero_rule` = node visits | 3,408 | 21,240 | 6,432 |
| Tree `scan` = leaf visits | 958 | 6,224 | 664 |
| Tree `add_terminal` = saved terminal count | 1,832 | 10,980 | 3,576 |
| Semantic `bisect_cubic` = twice root count | 512 | 1,440 | 1,440 |
| Semantic `source_box` = `load_boxes` = drone count | 64 | 180 | 180 |
| Semantic `reference_roots`, `global_guard`, `reconstruct_tree`, each | 1 | 1 | 1 |

The prepared preparation/validation wrappers also each have 64 / 180 / 180
calls. They call the original routines; their counts must not be added to
claim twice as many actual preparations. The original `pair.oracle_case`
does not appear in any profile. That absence, the exact suffix counts and the
frozen driver route agree with the reported zero full-oracle executions and
zero pair preparations.

The identical 1,440 `bisect_cubic` call counts for dense and sparse do not mean
equal bisection work. The frozen function returns `[1,1]` immediately when its
input is zero. Sparse has no positive terms, hence its empty row sums take
that exact-zero path. Dense has 600 nonpoint root boxes. The saved profiles
show a large difference in the routine's cumulative time, consistent with
those saved results and the source branch. The unchanged nonzero path still
uses the prescribed 128 bisections; this analysis executes none of them.

## What should be specified before any larger allocation

The practical conclusion is that one nonzero saved static case and
one sparse saved case fit the predeclared existing-cap pilot budget. That is a
useful prerequisite for designing a larger accuracy study. It is not an
authorization to raise the cap, weaken checks or implement another optimizer.
No next implementation is proposed or performed here.

A prospective scale contract should first state the claim and workload class.
It should distinguish exposed regressions from any independently selected
future moving cases, pin input encodings and raw words, retain an unfavorable
case as well as sparse cases, and specify orientation, force, domain/fallback
and positive-support coverage. Drone count alone does not describe the work.

The resource contract should account for exact node proofs, residual suffix
calls, positive support, root work, rational integer sizes, terminal records
and complete output size. It should reserve end-to-end time for evidence and
closure, specify one-use failure behavior, and keep accuracy qualification
separate from observed practical budgets. The dense full wire here is
5,709,049 bytes; complete output remains a real scaling cost even when
subtrees are pruned.

At 5,000 drones there are 24,995,000 directed drone pairs and 99,980,000 logical
rotor/source queries before exclusions. This is a counting identity, not a
prediction of scalar calls or elapsed time. These 180-drone profiles provide
no justified linear extrapolation to that workload. The current positive-term
cap and other admission limits also remain operative; proving a selected
large case fits is different from guaranteeing arbitrary large scenes.

Finally, the larger accuracy target needs its own independent evidence route.
It should state whether full prepared-word, pair-support, root and signed-load
records are saved and independently checked, and how actual delivered native
rotor/collective/world-force/world-moment outputs obtain the unchanged exact
1e-8 checks. Historical floating comparisons or a browser timing result do
not substitute for that route. Physical accuracy, coupled flight and
publication-level novelty remain separate unresolved questions.

## Source files for these observations

| Saved file | Bytes | SHA256 |
|---|---:|---|
| [Fresh profile](../results/fresh-a-t5.profile.json) | 92,782 | `d829790cbe46f180660d27e82815f72a238fe953c1ccf4574ef33f8c92fccbcf` |
| [Dense profile](../results/dense-180-filter-cost.profile.json) | 79,804 | `46bd32409063e8fb5e0d8d6c8d77efd489d8eea5aca3930c6db5ef4cb2b41753` |
| [Sparse profile](../results/sparse-180-filter-cost.profile.json) | 71,315 | `2c7aba9964077efe3af1d1874020d439f81b68dc9e21f59d989d02514f9d9c85` |
| [Fresh complete wire](../results/fresh-a-t5.json) | 1,148,972 | `21e1e66c71eaddaad98141fb58cfc1a768168ad411589d956af775e13c99ff2c` |
| [Dense complete wire](../results/dense-180-filter-cost.json) | 5,709,049 | `f8bdbe3f6cf1e9126a4eccded32b2d7ea8e736e234e1f1d9db70fe55c9a83c92` |
| [Sparse complete wire](../results/sparse-180-filter-cost.json) | 1,119,637 | `a26a2ed47ef61464ee3885198fe2fc8241a216d93faf0c5777d165cb8c89899d` |

The call-count interpretation also reads frozen
[`semantic-reference.py`](../../m31-native-fresh-transfer-2026-10-17/source/semantic-reference.py)
as text, particularly `reference_roots` and `bisect_cubic`, and the already
reviewed [driver](../source/run.py) and [design](../source/DESIGN.md). None of
those files is imported or modified by this interpretation.
