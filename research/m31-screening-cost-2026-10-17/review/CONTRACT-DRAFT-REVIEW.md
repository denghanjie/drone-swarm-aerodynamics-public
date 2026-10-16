# Independent cost-cycle contract review — source only

Reviewer: `m31_protocol_challenge`. Date: 2026-10-17.

Status: recommendations for the parent to settle before implementation and source freeze. This review does not authorize scientific execution and does not establish feasibility, admission, correctness, or speedup by experiment. Read inventory: `PROTOCOL-READING.json`.

## Review basis and conclusion

Read the fresh `DESIGN-DRAFT.md` and two inherited files: the prior result contract and relevant portions of the independent checker. No new candidate implementation was read. No scientific imports, numerical evaluation, fixture/checker/kernel execution, old controls, external operations, or new agents were used.

The proposed complete raw-words-to-method-record timing boundary is suitable for a descriptive comparison if its complete accounting and trial identity are frozen. A scene-at-a-time independent checker can preserve every logical pair and every implicit-zero/model check. However, merely changing reference generation to a loop is insufficient if the full result or control clones remain materialized. The storage layout, digest encoding, timing ledger, fixed controls, and revised evidence limits need exact contractual definitions.

The six declared scene sizes imply, by integer count arithmetic, 810 drones and 527,776 nonself rotor/source outcomes per method: `2 * 4 * (64*63 + 125*124 + 216*215)`. There are 1,055,552 outcomes across the two methods; one 216-drone scene contains 185,760 outcomes per method. Counts are not independent evidence that any omitted result is zero.

## Required scene-at-a-time schedule

1. Verify frozen source/spec/contract pins, bounded run header, and the lightweight ordered six-scene index. Parse JSON with duplicate-key rejection and exact allowed fields; enforce byte/count limits before large allocations.
2. Load exactly one full paired scene record using its index descriptor. Verify the descriptor's scene identity, file byte length and hash, and the retained raw words against the frozen scene literals/raw-input contract.
3. Independently reconstruct this scene's prepared data and exact geometry. Evaluate every declared nonself rotor/source pair with the frozen independent scalar oracle, including all pairs that the candidate compressed into node or scalar zeros. Record fixed-192 coefficients for positives and exact domain outcomes for all others.
4. Construct only this scene's exact tree/assembly plans, fixed-128 reference roots and load evidence. A current-scene lookup may point into the current-scene oracle rather than copy it. Do not substitute candidate agreement, tree proof alone, cardinality, sampled pairs, or successful admission for the pair oracle.
5. Independently validate both methods: raw/prepared identity, global guard, exact tree membership/extrema/order, terminal coverage, canonical source order, every omitted scalar entry, every member of every zero node, coefficients, rejected/unresolved outcomes, canonical status, work, solve/certificate, exact candidate loads, complete returned load boxes and normalized errors. Only then compare cross-method common scientific data.
6. Recompute context-bound hashes of the two retained method records. Check all ten trial identities, timestamps, counters, and hashes against these records. Compute descriptive paired ratios and medians from all four declared measured repetitions.
7. Apply the fresh controls assigned prospectively to the current scene, one mutation at a time. Use the same semantic validation entry point and the same current-scene oracle. Release each mutation before the next. Coverage/index controls operate on lightweight descriptors, not full scientific documents.
8. Emit a bounded compact scene report and any explicitly contracted reference evidence; retain only aggregate integer counters, small digest/descriptor metadata, and bounded control witnesses.
9. Release the scene record, oracle, lookup, plans, roots, loads, clones, and any closure capturing them before reading the next scene. Keep no list of all reference scenes, scene reports containing full references, or pending mutations retaining scene graphs.
10. After the final scene, require exact scene/trial/control coverage, reconcile aggregate counters and budgets, and finalize a small index/report. A missing required control witness or any scene failure fails qualification.

This schedule bounds the reference population to 185,760 pair records rather than 527,776. It is an allocation schedule, not a proof of a 1 GiB RSS peak. Object representation, the two retained method records, input parsing, exact arithmetic intermediates, and one clone still require fail-closed runtime resource enforcement. A smaller representation is acceptable only when it retains each independently classified status and any exact coefficient/domain witness needed by the same checks.

### Preferred storage contract

Use six full paired scene JSON files plus one small authoritative result index. Each descriptor includes ordered scene ID, relative allowlisted path, exact byte length, SHA-256, two method digests and the bounded trial ledger (or a separate uniquely referenced ledger file). The index pins the common schema, spec/source manifest and constants. Paths cannot escape the attempt directory; duplicate paths/IDs, extra/missing/reordered descriptors and trailing/unreferenced scientific records fail.

Write each scene once using exclusive creation and finish durability before journaling its descriptor. The journal stores the same bounded descriptor after a completed scene rather than a second copy of the full scientific payload. On partial failure retain completed files/descriptors and failure state; never relabel a partial set as a successful result. The checker validates descriptor-to-file, descriptor-to-journal and complete final coverage. Partial-file cleanup and exclusive attempt semantics remain parent responsibilities to specify.

Authoritative scene JSONL is also possible if line sizes are bounded and the checker reads one line at a time. A monolithic multi-scene JSON result is acceptable only with an explicitly bounded streaming parser. Calling `json.load` once and then iterating scenes does not meet this schedule.

The kernel must also release nonrepresentative trial output after hashing and retain at most the current scene's representative pair. Serialization/hash may temporarily create another scene-sized string; this is part of the harness memory budget even though outside method timing.

## Trial timing contract

Freeze warmup order as `AB`, then measured pairs `AB, BA, BA, AB`, with A=`complete`, B=`hierarchy`. Per-scene calls are therefore exactly ten; the run has sixty method calls. Warmups retain all timing/digest/work fields and are excluded only from descriptive measured summaries.

For each call retain:

- Global sequence, scene ID, phase (`warmup` or `measured`), declared repetition index, method name, and pair/order position.
- `startNs` and `endNs` as canonical decimal integer strings relative to one monotonic run origin, plus `totalNs`.
- The fixed named phase offsets, `scientificDigest`, common digest if retained, and the exact contracted work counters.

Proposed phase boundaries, identical in number and order for both methods: `start=0`, `prepared`, `proofBuild`, `pairAssembly`, `returned=total`. The method calls hooks only after prepared exact-cache construction, after guard/proof/tree work, and after complete pair assembly/canonical pair admission; the final phase includes solve/certificate and remaining method-record construction. The outer end stamp occurs only after the complete synchronous method returns. The parent should freeze exact names and what work belongs before each hook. Complete mode must still stamp the corresponding proof/build boundary, even if that phase performs less work.

Require `endNs-startNs == totalNs > 0`, `0 <= prepared <= proofBuild <= pairAssembly <= totalNs`, fixed keys/hook count, and exact stage differences summing to total. Zero-duration individual stages need not fail; a positive entire method interval is required. The per-call start/end ledger must be serial and nonoverlapping in the declared actual order, including warmups and scene transitions. No timestamp or hook overhead is subtracted. All hook calls and the outer stamps belong to the observed method boundary.

Raw-word validation and preparation are paid independently by each method. Shared literal-to-word conversion is outside the method boundary and has a separately retained harness interval. Final serialization and hash are also outside both methods with separately reported harness elapsed cost. Internal compact scientific/proof-output construction remains inside. Source review must establish that no asynchronous method work survives return; internally consistent timestamps alone cannot establish that fact.

Define four-run median exactly as `(sorted[1]+sorted[2])/2`. Keep it as an exact rational or half-integer. Paired ratios must identify the numerator and denominator (recommend `completeNs/hierarchyNs`), retain exact integer operands, and include every measured pair. Rounded display values derive from those operands. Report the two medians and their ratio separately from per-pair ratios; do not conflate a ratio of medians with a median of ratios. No adaptive repeats, outlier removal, best-run selection, or general speedup claim follows.

## Digest binding contract

Do not define the binding merely as “compact JSON.” JavaScript insertion-order serialization and Python defaults can differ. Freeze either a language-independent canonical serialization or a fully specified schema-order encoder. Recommended canonical form:

- UTF-8 JSON; recursively lexicographically sorted ASCII object keys; array order preserved; no whitespace; no duplicate keys.
- All numeric JSON values must be exact safe integers. No floating-point numbers, negative zero, NaN, or Infinity. Binary64 data use the already-contracted raw hex words; exact fractions/fixed-point/timestamps use validated canonical integer strings.
- Restrict the scientific/context strings to the contract's ASCII alphabet, or specify escaping fully. For ASCII strings, use ordinary JSON string escaping with lowercase `\\u00xx` for controls lacking short escapes and no slash escaping. The chosen Node and Python encoders must have the same precise rule.

The method digest preimage is a canonical envelope containing an explicit digest-domain/schema version, frozen spec SHA-256, frozen source-manifest identity, scene ID, raw-input digest, method name, and the complete unchanged scientific method record. The whole method record includes prepared data, assembly/proofs/work, canonical result, solve, and certificate. No timing, run origin, runtime-dependent durations, or trial sequence belongs in scientific identity.

The raw-input digest covers the complete raw-word input including fields that do not influence this model's output; a prepared-data digest alone can miss those fields. Source/spec identity may be a frozen manifest digest rather than embedding the entire manifest, but the exact identity must be pinned in the contract and recomputed.

Method-specific digests will normally differ between complete and hierarchy. Define a separate common scientific payload/digest containing prepared data, canonical result, canonically ordered positive entries, solve and certificate; exclude method name and method-specific assembly/work. Compare these common values only after both semantic validators independently pass. A common digest is not a replacement for those validators.

For every trial, the checker recomputes the expected method digest from the retained representative and frozen context, then requires exact equality. The representative must be a prospectively named trial (recommend the first measured call for each method); no best-trial selection. Trial work counters equal the independently reconstructed representative counters. A reported common digest, if present, is also recomputed, never merely compared between trials.

Binding all trials to a saved representative detects a reported differing output without retaining all repeated records. It does not cryptographically attest that repeated computation occurred or that the recorded elapsed time is truthful. Execution provenance rests on frozen synchronous source, the declared exclusive attempt, chronological journal/supervisor evidence and runtime pins. State that limit explicitly in the result.

## Proposed fresh controls: exactly 15

This is a new control set for the six fresh scenes. Do not invoke the previous negative-controls routine or rerun old fixtures. Select the first qualifying witness by frozen scene order, then hierarchy method, input receiver, rotor, terminal order, and source input index; root/load witnesses use input drone then component. Retain only a small witness plus scene ID and mutation identity. Selection must be deterministic before execution, with no post-result substitutions. If a witness is absent across the six scenes, fail control coverage.

| # | Control | Mutation and independent required failure |
|---|---|---|
| 1 | Omitted positive singleton | Remove the first positive scalar entry and increment `zeroCount`, preserving coverage/count arithmetic. The independent oracle must reject that newly implicit zero. |
| 2 | False node zero | Replace a hierarchy leaf containing an oracle-positive member with a zero terminal covering the same members; choose a frozen rule. Require independent proof/positive-member failure, not a changed terminal count. |
| 3 | False zero coefficient | Replace a positive coefficient by `[0,0]` only where fixed-192 reference lower bound is strictly positive. Require coefficient containment failure. |
| 4 | False unit root | Replace an affected returned root by `[1,1]` only where independent reference upper bound is strictly below one. Require corollary/root/reference containment failure. |
| 5 | Candidate bit corruption | Flip one least-significant candidate bit for a frozen admissible affected root, retaining the exact candidate load records. Require exact candidate identity failure; require the mutated word to remain finite in `(0,1]` so range rejection is not the only failure. |
| 6 | Candidate load identity | Change one exact candidate load rational by a fixed exact increment while preserving rational canonicality and wire bounds. Require exact candidate-derived load identity failure. A fixed first rotor component is sufficient. |
| 7 | Full returned load box | Replace a selected returned load interval by a valid ordered singleton strictly excluding a fixed-192/fixed-128 reference endpoint. Require independent or full returned-root-box load containment failure. Freeze a bounded construction and witness before execution. |
| 8 | False zero error | Set a selected rotor error upper bound to zero only when the exact candidate lies strictly outside the independent reference root interval. Retain the strictly positive exact normalized load gap and require error-bound failure. |
| 9 | Missing scene descriptor | Remove the final scene descriptor from the small index. Require exact scene count/coverage failure. |
| 10 | Duplicate scene descriptor | Replace the second descriptor by a copy of the first. Require duplicate identity/coverage failure. |
| 11 | Reordered scene descriptors | Exchange the first two distinct descriptors. Require declared scene-order failure. |
| 12 | Timing partition mismatch | Change one interior phase offset within legal range, without updating its reported stage duration (or change total while retaining endpoints). Require the frozen timing reconciliation family. Mutation recipe must target one chosen redundancy. |
| 13 | Trial order mismatch | Swap the method identities/order slots of a fixed measured pair while retaining each call's otherwise valid timing and scientific binding. Require actual declared AB/BA schedule failure, not digest mismatch alone. |
| 14 | Trial digest binding | Change one measured trial's method digest to a different valid 64-hex digest, leaving its representative/context intact. Require recomputed representative-binding failure. |
| 15 | Trial work mismatch | Change one declared trial counter by one while leaving the representative and digest correct. Require independently reconstructed work/counter mismatch. |

Controls 1–8 must reach the semantic core despite the intentional scientific mutation. Either recompute the affected representative and trial hashes in the disposable scene clone using the same frozen canonical encoder, or run the same semantic validator before digest/equality checks and require the named semantic error family. The latter avoids reserializing every large clone, but its validation order must be explicit. No control counts as effective solely because a file hash, trial digest, cross-method comparison, or generic exception rejects it.

Control 13 swaps the complete trial objects, then assigns the declared physical sequence/time positions consistently so each trial retains its method/context digest and work identity; alternatively change the declared order field in a ledger whose actual method sequence remains fixed. The exact frozen recipe must cause the schedule validator to be the intended failure. Controls 9–11 need no reference regeneration. Each control uses one bounded local mutation and releases it immediately.

The baseline checker still validates every exact tree/guard/proof and every model condition even though this small new control set does not mutate every possible field. Controls demonstrate selected failure sensitivity; they are not a completeness proof.

## Output and memory budget gaps to close prospectively

The inherited generic wire allowances do not establish the proposed new budgets:

- `1,055,552 * 384` bytes for hypothetical paired nonzero entries is about 405 MB before queries, loads, trees, headers or trials; it exceeds a 128 MiB result limit.
- `810 * 2 * 98,304` bytes for inherited per-method load-record allowances is about 159 MB, also exceeding 128 MiB before other fields.
- A generated full reference with 30 rational endpoints per drone and the inherited 4,096-character numerator and denominator allowances can exceed 200 MB before JSON structure, so a 96 MiB checker allowance is not justified by those caps.

These are upper-envelope counterexamples, not predictions of actual output. Do not evaluate the scenes merely to discover a convenient size. A streamable layout controls peak materialization but does not itself reduce aggregate bytes. The parent must choose and freeze tighter independently justified fixed-scene bounds, compact report fields, larger prospective limits, or explicit fail-closed per-file/aggregate limits with failure accepted as a possible outcome.

For these upright moderate-force literal scenes, generated reference roots are fixed-128 dyadics, source force intervals are fixed-192 dyadics, and upright axes/offset products keep reference load endpoints dyadic. A generated-reference rational cap of 256 characters appears conservative, but must be established by a source/math bound on magnitudes, exponent accumulation, and exact constants before it is relied upon. Keep generated-evidence bounds separate from candidate-input parser allowances; shortening emitted reference values must never round away evidence or weaken containment checks. Reject over-cap evidence rather than truncate it.

A result-index/journal limit can be much smaller than a scientific-scene limit. Freeze aggregate accounting across all scene files, index, journal, checker evidence and logs; do not count only the small final index as the result. Bound a control witness independently from the large mutated object. If the checker emits full reference evidence, stream it per scene or to bounded separate files rather than accumulating it in one returned report object.

The proposed 1,800-second allocations and 1 GiB sampled process-group RSS remain unverified feasibility limits. Guardian overrun/refusal is a valid failed attempt, not permission for retries, relaxed checks or additional executions. Reports must distinguish sampled RSS from a certified continuous peak.

## Decisions required before implementation

1. Authoritative six-scene storage/index/journal layout and full byte-accounting rules.
2. Exact canonical encoder, digest domain/context, common payload and representative-trial selection.
3. Warmup order, trial fields, phase names/boundaries, ledger redundancy, harness intervals and descriptive summary arithmetic.
4. Exact 15 fresh control names/recipes, intended failure families, semantic-before-digest ordering and missing-witness policy.
5. Revised per-scene/aggregate/report/reference caps with static justification or explicit fail-closed outcome semantics.

After these choices, the independent checker can be authored without reading new candidate implementation. Final source-only review, immutable freeze, publication and exact remote verification remain prerequisites to the parent's separately authorized single executions.

## Superseding concrete agreement draft

The initial recommendations above are retained as the pre-settlement review. The parent subsequently accepted scene-file streaming, first-measured representatives, context-bound digests, the fixed 60-call order and 15 fresh controls. `RESULT-CONTRACT-DRAFT.json` is the concrete contract proposed for final agreement and incorporation; it supersedes earlier optional encodings, names and caps in this note.

Settled packaging: `results/timing-index.json` and its `.jsonl` journal are each at most 8 MiB; each paired `results/scenes/<declaredSceneID>.json` is at most 64 MiB; all scientific shards plus a first-mismatch anomaly share a 128 MiB limit. `independent-check.json` plus `reference-scenes/*` share 96 MiB. Metadata and all kernel/checker private/public log copies share 16 MiB. All outputs remain under the 384 MiB aggregate cap. The math review supplied a conditional successful-science envelope of 104,162,304 bytes, largest paired scene 57,880,576 bytes, load record 9,322 bytes below 12 KiB, and reference evidence below 25.7 MB. These envelopes require the separately frozen prepared-point rounding/support proof and field accounting; they do not establish peak RSS or execution feasibility. Reserve enough anomaly capacity for the largest single method record before a timing call, rather than assuming the paired-scene bound proves that reserve.

Settled offsets: `prepared`, `spatial`, `assembled`, `completed`. `assembled` ends after query assembly, canonical nonzero sorting and stable-ID conversion; canonical admission and common solve/load certification are in the tail. `completed` is the outer return stamp. The canonical digest alphabet is **printable ASCII only**, eliminating nonportable string escape cases. Domain/envelope keys are fixed in the JSON draft. Harness serialization/hash timing has explicit scope, separate from method cost and unmeasured file/journal orchestration.

The 256-character rational cap is now limited to the enumerated reference/control sites in the JSON draft. Source-only bounds cover fixed-128 roots, fixed-192 coefficient witnesses, upright reference moments, exact candidate loads, bounded native-bit mutation, candidate-load plus-one mutation, rotor-load containment witness, normalized error gap, tree endpoints and timing ratios. A toggled native LSB can increase the candidate denominator from the original midpoint bound of `2^55` to `2^107`; this is still comfortably inside the cap and is explicitly included. The math reviewer supplied the remaining normalized-gap proof: `mg=M/2^54`, `2^52<M<2^53`; `force=F/2^57`, `|F|<2^54`; `gap=G/2^128`, `|G|<=2^128`. The normalized gap is `F*G*2^56/(2^185*M)`, whose numerator and denominator are below `2^238` before reduction. No unquantized oracle expression or prior failed-guard witness is emitted under this allocation.

The exact controls now use a positive independent rotor-load interval and mutate its returned box to `[0,0]`; trial-order mutation swaps the first measured pair's complete ledger rows and runs schedule validation first; stage corruption adds one to the first measured preparation stage without changing offsets. Candidate exact load identity is validated before row defect/root checks within the same certificate validator so the candidate-bit control reaches its intended failure family. All mathematical acceptance checks remain mandatory.

The two reviewer JSON files were parsed for syntax using only standard JSON/path utilities. No scientific module was imported or executed. Inherited distinct files remain **2 of 16**.

One explicit failure-precedence choice is proposed for parent agreement: an arbitrary erroneous mismatch record need not satisfy successful-output size bounds. If a complete anomaly cannot fit the per-file/scientific/aggregate cap, declare `anomaly-retention-resource`, retain bounded digests and required/available byte evidence, and report the missing full anomaly. Do not truncate scientific evidence or relax the byte cap. This remains a failed allocation with no retry; complete anomaly retention must not be falsely claimed.
