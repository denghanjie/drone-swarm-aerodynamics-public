# Source-only review of the matched-cost draft

Reviewer: `m31_verified_literature`. Date: 2026-10-17. Reviewed draft: `DESIGN-DRAFT.md`, 6,212 bytes, SHA-256 `c2f0c3aab1f8123be344facb96d92f6a184ef727e560c6697c85b6ceadfb7ca9`.

**Disposition: accept the bounded research direction; do not yet freeze or authorize execution.** The six fresh dense/sparse scenes at 64, 125 and 216 drones, matched raw-word boundary, four balanced measured pairs and retained warmups form a useful descriptive comparison. Final timing semantics, trial identity rules, static artifact bounds and peak-live-object scheduling need to be explicit before source acceptance. No speedup, runtime forecast or admission result follows from this source review.

This review read six inherited source files, listed with hashes and read scope in `PROTOCOL-DRAFT-READING.json`; the cap is 16. It ran only file inspection, hashing and static integer accounting. It imported or executed no scientific source, generated no numerical result, fetched no literature, reran no old control, installed nothing and spawned no agent. Supervisor and guardian remain unchanged.

## 1. Count the whole allocation

The declared one-pass arithmetic is correct:

| Quantity | Static count |
| --- | ---: |
| Six-scene drone count | 2 × (64 + 125 + 216) = 810 |
| Pairs for a 64-drone method call | 4 × 64 × 63 = 16,128 |
| Pairs for a 125-drone method call | 4 × 125 × 124 = 62,000 |
| Pairs for a 216-drone method call | 4 × 216 × 215 = 185,760 |
| Six-scene logical pairs per method, one pass | 527,776 |
| Warmup plus measured calls per method/scene | 1 + 4 = 5 |
| Total method invocations | 6 × 2 × 5 = 60 |
| Whole-allocation logical pairs per method | 2,638,880 |
| Whole-allocation logical pairs, both methods | 5,277,760 |
| Both-method warmup logical pairs | 1,055,552 |
| Both-method measured logical pairs | 4,222,208 |

Logical pair obligations are not scalar query counts: hierarchy proofs may cover many pairs. Keep these distinct from measured work. Freeze scene order, warmup order, invocation sequence numbers, the A/B mapping and the exact four pair orders. `AB, BA, BA, AB` gives each method two first positions and two second positions, but it is neither randomized nor a claim that host drift cancels.

## 2. Make the method boundary executable and auditable

Use a synchronous method wrapper whose first timestamp precedes method-specific work. A suitable four-part partition is preparation; guard/tree/proof construction; traversal/scalar assembly; canonical admission/proposal/certificate completion. The final protocol should identify every operation's owner and exact source boundaries, including:

- Raw-word decoding, preparation, exact rational maps, index maps and counters. Each method pays its own copies. Raw state/identity/domain checks must either be included per method or explicitly classified as shared harness checks; no hidden baseline-only preparation is acceptable.
- All global guard tests, successful tree construction and wire construction, failed-guard fallback selection, traversal, scalar calls, implicit-zero/entry record construction and work counting.
- Canonical ordering/sorting, rejection/unresolved/resource precedence and witnesses, positive-term limit, load proposal, root/load certification and complete returned scientific record construction.
- Early returns. Every refusal or resource result still gets a complete reconciled timing record; it must not vanish from the saved allocation or be substituted by a later run.

Let consecutive boundaries be `t0 <= t1 <= t2 <= t3 <= t4`, with `total = t4 - t0` and phases the four consecutive differences. Persist exact integer nanoseconds as canonical decimal strings. The checker should enforce nonnegative integers and exact phase-sum equality, not floating-point tolerances. Skipped stages need a declared zero-duration/boundary convention; optional hierarchy-only work must not leave an unaccounted gap. Boundary-clock overhead is part of the measurement instrument and should be applied consistently, without subtracting a guessed cost.

The shared literal-to-word conversion, module/runtime initialization and final serialization/hash/write operations are outside this declared raw-words-to-completed-record measure. Declare all such exclusions and retain separately identified harness costs. Do not describe this as application, browser or decimal-ingestion end-to-end time. Timed internal proof/record construction must not be deferred into the excluded serializer. No per-pair clock, asynchronous work, unallocated forced-GC pass, performance-dependent retry or outlier removal is needed.

## 3. Retain warmups, bind repeated results and limit claims

Both warmups are real computations. Retain their method/scene identity, sequence position, outcome, full phase durations, selected work counts and scientific digest. Freeze warmup order before running. A common V8 process shares JIT, caches and heap/GC state across methods and scenes, even when raw preparation is independent; warmups and ABBA ordering do not remove those effects. Freeze process lifetime and the exact method-call schedule as part of the measurement setup.

Define one canonical scientific encoding, preferably separate from the timing sidecar. Specify key order, array order, integer/string representation, newline policy and all excluded timing/runtime fields. Choose the retained full record prospectively, for example the first warmup record for each method/scene. Each of the five digests for that method/scene must match a fresh digest of those saved bytes. Preserve all trial identities, outcomes and counts; any mismatch fails the cycle. Do not select an agreeable later record. Cross-method equality applies to the declared common scientific projection, separately from each method's assembly/tree/work payload.

An independent checker can recompute the saved records' hashes, validate the exact trial schedule and bindings, and independently check the mathematics of the retained record. It cannot remeasure historical clocks or prove from digest assertions alone that all invocations happened. The source-pinned runner is the timing instrument, with supervision/provenance as supporting evidence. Keep this trust boundary explicit.

For each of the four measured pairs, define the ratio direction, for example `complete_ns / hierarchy_ns` (greater than one favors hierarchy), and retain both numerator and denominator. Specify the zero-denominator policy before running. Report all four ratios and each method's median; for four values the median is the mean of the two central sorted observations. If also reporting a ratio of medians or median of paired ratios, label it exactly: these summaries need not agree. Missing/failing trials remain visible and prevent a complete qualified timing comparison. Four observations support a descriptive result for this fixed suite/environment, with no confidence, host-independent performance, 5,000-drone, dynamic-flight, physical-validation or novelty claim.

## 4. The inherited wire caps do not yet establish feasibility

The inherited contract permits 384 bytes per nonzero entry, 96 KiB per load and 1 KiB per certificate row. Composing those allowances over all available slots yields:

| Component in one retained paired six-scene set | Conservative cap composition |
| --- | ---: |
| Entry slots: 2 × 527,776 × 384 | 405,331,968 bytes (386.55 MiB) |
| Method/drone load slots: 2 × 810 × 98,304 | 159,252,480 bytes (151.88 MiB) |
| Certificate row slots: 2 × 810 × 4 × 1,024 | 6,635,520 bytes (6.33 MiB) |

These are loose fieldwise upper-bound components, **not predicted actual sizes, lower bounds, or a proof that all maxima are simultaneously attainable**. They show that merely inheriting these caps does not prove a 128 MiB document fits. One 216-drone paired record's entry-slot allowance alone is 142,663,680 bytes (136.05 MiB), so splitting by scene also requires tighter bounds rather than an assumption that every scene fits 128 MiB.

Most logical pairs may in fact be implicit zeros, positive coefficients may use shorter strings, and fixed geometry may admit stronger analytic bounds. Such bounds must be derived prospectively from schema/source/literal structure, not from an unauthorized numerical probe or an assumed favorable outcome. The current inherited runner stores each full record in both the result and JSONL journal; duplication must enter aggregate accounting. Even a better entry bound must also include load rationals, certificate rows, tree nodes, prepared/input records, query/terminal wrappers, timing records, source metadata, checker reference evidence, controls and report/log overhead.

Before freeze, provide either justified tighter field/count bounds and a fitting layout, or prospectively revised artifact/aggregate limits. A compact timing journal plus one scientific copy may reduce duplication if its integrity contract is independently checked. Keep the requested six scene sizes. Freeze filenames, cardinalities and size limits together so a supervisor cannot overlook new shard files. Checker per-input limits and source/spec limits must agree with the new layout.

## 5. RSS and wall limits need explicit schedules, not a forecast

The inherited kernel accumulates all scene records in `records` and serializes a second complete document at the end. Merely avoiding ten retained copies per scene is insufficient: retain only the chosen scientific records required by the declared layout, serialize/stream them outside the method interval, release other trial records promptly, and account for serialization strings/buffers. Avoid carrying all six large scientific records live if scene-at-a-time persistence can meet the same evidence contract. Release is a source-level lifetime decision; JavaScript collection and RSS return remain runtime behavior.

The inherited checker eagerly regenerates and retains every scene's full pair oracle, lookup, tree/plans and load reference before loading the full candidate document. Each inherited negative control deep-copies that document. These patterns need deliberate adaptation. A scene-at-a-time checker can preserve full pair membership, independent coefficients/zeros, tree/proofs, roots and loads while bounding live references to one scene. Save compact per-scene findings and reference evidence, then release its full oracle. Mutate/check one relevant scene for scientific controls instead of repeatedly deep-copying the full suite. Keep global missing/duplicate/reorder checks as an independent complete-manifest pass. Ensure new control scheduling neither silently multiplies full-oracle computations nor weakens their scope.

The largest declared scene has 185,760 logical pair obligations in the independent oracle. Source inspection can establish this live cardinality and removal of avoidable all-scene duplication; it does not prove CPython/V8 peak RSS below 1 GiB without a defensible object/temporary bound. Describe 1 GiB as the sampled group termination limit, not a measured or guaranteed peak-memory forecast. Likewise 1,800 seconds is the allocated ceiling, not evidence of expected completion. The kernel ceiling covers all 60 calls plus harness work; the checker ceiling includes full references, controls, serialization and finalization as defined by supervision. A timeout/resource outcome closes the sole allocation without an adaptive rerun.

## 6. Supervision effects and prefreeze conditions

The inherited supervisor sleeps nominally 0.05 seconds between samples and invokes `ps` to inspect the owned process group. Actual gaps include sampling and scheduling overhead; retain sample count, maximum sample gap, peak sampled group RSS, wall time and termination/closure evidence. The sampled group includes the retained guardian and scientific child, not every observer or host process. Short RSS peaks between samples are not ruled out. Supervisor `ps`, guardian activity, host scheduling and GC pauses can affect observed method time. Record runtime/OS/architecture facts and the monitoring policy. Do not subtract unmeasured interference or claim full host isolation. Keep authoring/review agents, audits, builds and browser QA idle throughout timed execution.

After design acceptance, reconcile all supervisor/guardian filenames, source/runtime pins, required-source list, artifact caps and deadlines with the new package. The old supervisor uses kernel/checker limits of 300/600 seconds and guardian limits of 310/610 seconds; it cannot enforce the proposed allocation unchanged. Preserve retained group ownership, exclusive attempt markers, source/runtime pre/post checks, fail-closed terminal evidence and cleanup semantics. Define whether the aggregate/log budget includes retained private raw logs from both stages as well as their public copies; the inherited checker-stage counter includes current-stage private logs but not the preceding stage's private raw logs. Count all outputs promised by the chosen scope and reserve space for both final reports and failure records.

Freeze a small new control list with deterministic witnesses and targeted error families. In addition to scientific corruption and global record integrity, cover missing/duplicate/reordered trial identity, changed scientific digest, inconsistent counters, negative/noncanonical times, and phase-sum/total inconsistencies. A control must fail its intended semantic or timing check, not merely a cross-method inequality or unrelated earlier check. An internally consistent forged duration cannot be independently disproved offline; do not overstate what timing controls establish. Missing witnesses fail the declared control coverage.

A final source review should verify these settled choices against the protocol, spec, contract, runner, checker and adapted supervision. Then source freeze, privacy review, publication and exact-commit remote verification must precede any numerical call. This review is not that final source gate and grants no numerical or display execution.
