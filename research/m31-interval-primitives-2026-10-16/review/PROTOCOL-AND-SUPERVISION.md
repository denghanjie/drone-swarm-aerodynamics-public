# Interval-primitive protocol/source review

2026-10-16. Initial source-only review. **Disposition: prefreeze changes required; supervisor and independent checker remain pending review.** No generator, primitive, checker, import, syntax evaluation, or numerical experiment was executed. No external operation occurred. This report will receive a separate addendum if corrected source and supervision become available; the initial findings and identities below are preserved.

## Findings requiring resolution before freeze

### P1 — low-bit LCG pairing structurally excludes entire control classes

`spec.json` and `run.cjs` use an unsigned 64-bit LCG with odd multiplier and odd increment. State parity therefore alternates on every draw. The seed is odd. The 128 generated binary64 draws and 128 × 3 interval-generation draws consume an even number of steps, leaving the pair-generation entry state odd. Each subsequent pair consumes two draws reduced modulo the even interval count 152. Its left index is consequently always even and its right index always odd.

This is an algebraic source observation, not an observed generator result. It excludes every same-index binary pair and all odd-left/even-right combinations. In particular, the explicit zero singleton at index 0 cannot occur as the right operand, and many explicit negative/range denominator cases cannot appear there. Other zero-containing denominators exist at odd indexes, but this review has not generated the schedule and does not claim whether they are selected.

Resolve with an explicit declared set of binary controls covering the required properties, independently of the pseudorandom pairs. Supplemental index draws should avoid direct reliance on the alternating lowest bit, for example by a documented upper-bit rule. Such a change removes this particular exclusion; it does not make samples statistically independent or uniform. Update counts and the independently regenerated declaration before source freeze. Do not add selected cases after seeing numerical outcomes.

The generated interval endpoint draws and shifts are also correlated: the three draws per interval inherit deterministic low-bit structure. The generated-bit portion is a finite deterministic stress sample, not a stratified or representative sample of binary64 exponents, signs, cancellation cases, or operation outcomes.

### P1 — completed case evidence exists only in memory until the final write

The runner collects all records in `rows`, then exclusively writes one final JSON document. An unexpected exception, external termination, timeout, or final write failure can leave no saved record of already completed cases. Exclusive publication prevents replacement but does not preserve completed-case progress.

For the intended failed-attempt/partial-evidence contract, add an exclusive append-only case journal or bounded durable checkpoints, with exact sequence and a final completion marker. The independent checker must distinguish complete qualification from an incomplete journal; no retry is implied. Retain the actual terminal supervisor record. Any partially written or unacknowledged final record must remain incomplete. Persistence overhead belongs inside this primitive campaign's wall budget, with no performance inference.

This is an evidence-retention concern, not a claim that the short primitive suite will time out.

## Count and allocation audit of the initial source

The declared arithmetic is internally consistent:

| Portion | Source allocation | Records |
|---|---|---:|
| Conversion | 32 explicit patterns + 128 generated patterns | 160 |
| Unary | 24 explicit intervals + 128 generated intervals; square then sqrt for each | 304 |
| Binary | 256 generated pairs; add, sub, mul, div for each | 1024 |
| Total | One ordered suite | 1488 |

The runner follows that order and checks the final record count. IDs are indexed by operation and input/pair ordinal. Named `Unqualified` failures are preserved as statuses and later cases continue; unexpected errors abort instead of being mislabeled numerical failures. No retries or adaptive resampling are present. The explicit specification is the shared declaration, not independent empirical evidence. Independent Python case regeneration can check runner fidelity to it, but cannot remove a flaw shared by that declaration.

The scientific allocation is one runner and one independent saved-result checker, each at most 120 seconds/1 GiB sampled group RSS/16 MiB output, subject to the source-publication gate. This is pending and was not exercised. Static inspection of `run.cjs` shows no child-subprocess API. The supervisor must establish the actual runtime, command, limits, group ownership, failure closure and source identity; those are not proven by the runner's self-reported runtime/source hashes.

## Meaningful controls and coverage

The explicit conversion/unary declarations cover useful distinctions: signed zero, subnormals, sign changes, normal boundaries, the representable magnitude boundary and just beyond it, maximum finite values, nonfinite patterns, nonnegative and negative-root domains, zero crossing, and wide/range-boundary intervals. This is source-level coverage of listed inputs, not a claim about their eventual outcomes.

The binary control declaration should explicitly include both operand orders where meaningful, zero as numerator and denominator, a denominator merely touching zero, a wholly negative denominator, nonzero singleton identities, opposite-sign products, cancellation, and allowed-result versus range-failure boundaries. Explicitly distinguish multiplication of independent interval operands from squaring the same unknown; their sharp ranges need not agree for a sign-crossing interval. Matching only generated pairs is insufficient evidence for these branches.

For checker fault injection, recommend six separate mutations, each passed through the same full validator:

1. Replace both output endpoints of the known exact-zero conversion with a strictly positive singleton, so the true value is excluded. This tests more than rejection of an otherwise sound wide interval.
2. Replace the known zero-conversion success status with a named failure status.
3. Remove one required record.
4. Duplicate a record while retaining a misleading total count or substituting for another ID.
5. Exchange two different ordered records.
6. Change a recorded input while retaining its original ID/result.

Check the unmodified evidence first. Every control must be deliberately wrong, reach the intended validator, and produce a recorded rejection; a generic parser crash or swallowed exception is not automatically a useful detection. Separate canonical-endpoint checks from mathematical inclusion checks in the report. The protocol permits exact minimal outward endpoints, so a widened result can be a contract mismatch without being an unsound enclosure.

Malformed interval/bits grammar is expressly outside the 1488 cases in the argument draft. Source-level grammar/length/range checks do not turn that omission into empirical interface coverage. Likewise, iteration-cap exhaustion and internal sqrt-check failure may be hard or impossible to reach through valid inputs; do not claim their dynamic enforcement was exercised unless a separately declared control actually does so. No extra tests are allocated by this recommendation.

## Independence and claim boundaries

The proposed Python Fraction/math.isqrt checker uses a different arithmetic substrate from JavaScript BigInt and its custom integer-root iteration. That is a useful prospective cross-check. Its own code is not yet available in this review, so input regeneration, strict schema/ID/order validation, exact status precedence, source pins, mutation checks, and fault-control effectiveness remain unverified.

The shared LCG/specification intentionally makes the case schedule reproducible. It does not provide statistically independent samples. The checker should derive rational expected values from its regenerated inputs and frozen declaration, not from runner-supplied expectations, and should avoid copying the candidate's rounding implementation where Python's independent exact operations suffice. No number of mirrored checks proves general correctness.

`interval.cjs` was read to ground the protocol interpretation. It freezes constructed interval objects, revalidates public arithmetic operands, bounds endpoint range, rejects zero-containing division and negative sqrt lower bounds, and checks its integer-root result before returning. This protocol review does not replace the independent mathematical review of those formulas. The runner's before/after encoding checks final observable input equality; it is not a general proof that no transient mutation or other side effect occurred.

The argument appropriately distinguishes source-reviewed general inclusion reasoning from finite qualification. It discloses lattice coarseness, named unsuccessful outcomes, absent native-math compatibility, and unknown BigInt cost. A pass could support these fixed primitive cases and the separately reviewed arithmetic argument. It cannot qualify complete preparation, geometric guards, row contractions, the coupled-root certificate, a browser implementation, 5000-drone throughput, aerodynamic prediction, or novelty. The original complete current-state accuracy–computation goal remains open.

## Exact initial reading inventory

All paths are relative to the public repository root. Five new checkpoint files were read; zero inherited content files. File-name listings and byte/hash reads added no target data. No parent file was edited.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-interval-primitives-2026-10-16/PROTOCOL-DRAFT.md` | 6226 | `15f86c9e11f7b69386b073219946539cbd66c59fe92b10b25936fdb53150a891` |
| `research/m31-interval-primitives-2026-10-16/ARITHMETIC-ARGUMENT-DRAFT.md` | 3364 | `12363b18045043f5d550850a1f9d329f698ff96b0a71914d08ea4c0e77b4aecb` |
| `research/m31-interval-primitives-2026-10-16/source/spec.json` | 1967 | `d8065903820d08a730489abea8d92d1bad735770818e9e6717ca5ff6ab6fb2e4` |
| `research/m31-interval-primitives-2026-10-16/source/run.cjs` | 2500 | `4b7e8b1ccf61ee2c6f6515db5e9cce3e27612e29a00fc6fd5e1b43785cbd4557` |
| `research/m31-interval-primitives-2026-10-16/source/interval.cjs` | 2815 | `73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3` |

Pending: corrected generator/retention design, actual checker source, supervisor source and closure contract. This initial report grants no execution clearance.

## Addendum 1 — first prefreeze corrections and initial supervisor

Source-only follow-up, 2026-10-16. The parent preserved initial source and supplied revised `spec.json`, `run.cjs`, a result contract, and initial `supervise.py`. No numerical work was performed.

**The initial pairing finding is resolved in this source revision.** The suite now declares 48 explicit binary pairs: all 24 explicit self pairs plus 24 selected boundary/operand-order pairs. It supplements these with 208 pairs indexed from the high 32 bits of each draw. Total binary pairs remain 256 and primitive records remain 1488. The explicit list guarantees examples of zero denominators, touching-zero denominators, wholly negative denominators, sign changes, self operands and magnitude boundaries. The former low-bit parity proof no longer constrains the supplemental indexes. No statistical-independence or full-domain-coverage claim follows.

**The initial all-in-memory retention finding is addressed.** The runner exclusively creates an append journal, writes a header and each full case row, synchronizes at the header, every 32 cases and completion, and retains the final exclusive summary document. The result contract requires matching journal/final rows and complete order. An interrupted journal can remain partial; records since the last sync are not promised crash durability. The completion marker precedes summary publication, so qualification must require both and their agreement. The current single `fs.writeSync` calls do not explicitly loop over short writes; later validation must fail closed on malformed/incomplete journal content. A write-all helper would make the retention implementation clearer.

The result contract distinguishes exact minimal outward endpoints from general enclosure soundness. Its statement that a one-unit mutation is a negative control is correct for the canonical-endpoint contract, but such a mutation can merely widen an interval. The eventual checker should still include a mutation that provably excludes a known exact result and label the two claims accurately.

### Initial supervisor findings, unresolved at this revision

1. **Finalization is outside the cap decision.** The monitor computes the resource decision before cleanup, full log reads/redaction, public log duplication, output hashing and the final supervision record. It later computes `wallSeconds` but does not compare that final value to 120 before setting success. Published logs and the final record can also increase output beyond the checked 16 MiB. Recheck final accounting, fail qualification on an exceeded cap, and preserve a bounded terminal failure record. The storage definition must say whether it is stage-owned or cumulative; the current scan includes earlier files in the common result directory.
2. **Source/runtime chain is incomplete.** Source-manifest pins and the publication receipt are checked only before launch. The checker-stage prerequisite tests the previous record's success/closed flags without matching its source identity or saved output/journal pins. No after-run source/runtime identity check or frozen runtime-executable identity is present. Self-reported Node versions and source hashes do not substitute for this chain. Bind the stages to the same source/receipt, mandatory source inventory, runtime and recorded command, and verify immutable saved inputs before admitting the checker.
3. **Polling promise exceeds implementation.** A `ps` call may take up to two seconds, followed by a 0.1-second sleep; this is not a sampling interval bounded by 0.1 seconds. Sampled RSS is not a true peak or kernel limit. Report observed sample intervals and monitoring failures, distinguish nominal sleep from actual cadence, and make the time decision include monitoring latency.
4. **Group ownership and closure need stronger treatment.** The `finally` block unconditionally signals a numeric process group even after the direct child may have exited. It retains no live guardian or start-identity check protecting that ownership assumption. The monitor observes current group membership only, not escaped descendants, and uses one immediate `killpg(...,0)` probe for absence. An immediate non-absence can conservatively reject a completed cleanup; an empty original group does not establish absence of escaped descendants. Preserve an ownership anchor through cleanup, verify the expected child/group lifecycle and require bounded fresh absence observations. Do not imply hostile-code isolation from sampled userspace monitoring.
5. **Terminal publication can itself fail.** Exceptions in final log redaction, hashing, absence probing or report writing occur inside `finally` without a bounded fallback record. Such an outcome must remain explicitly unqualified, with retained attempt/partial evidence, rather than allowing a missing report to be mistaken for clean closure. Review this alongside the final cap and source checks.

These are findings on the initial supervisor bytes below, not a claim about the parent's planned revision. The parent has indicated that a live group guardian, runtime/command pins, stage-chain checks, after-run checks and truthful final resource accounting will be added. Those changes require source inspection before disposition changes.

### Follow-up reading identities

Two revised files and two additional new files were read. Unique content paths so far: seven new checkpoint files, zero inherited files. Snapshots of this round are retained privately under the reviewer's `/tmp` directory; no original source is edited.

| Path within this checkpoint | Bytes | SHA-256 |
|---|---:|---|
| `source/spec.json` | 2550 | `73d539b2f6575e21b3f8c512ce79a4be22ff0b09c98c527cb18dfc06a6dc21f7` |
| `source/run.cjs` | 3054 | `172dd45d3f1fe06f3562e3908d16e3d4d759f0c5e1f769f4f9d46860f09fcd0b` |
| `source/result-contract.json` | 2805 | `c888bb0c7040b44848d50380de64211a4bb37f6584577a9f8726457354a16da6` |
| `source/supervise.py` | 6382 | `abde85e9336d5460d7ed49fa8e0d79fe34bd0ad577a5bbea584e322f0655a8f0` |

## Final addendum — 2026-10-17, Asia/Shanghai

**Final disposition: no remaining blocking static issue identified in the exact final protocol/source snapshot below, within this review's declared scope.** The earlier findings remain preserved above and are superseded only where a resolution is explicitly verified here. This is source review, not execution or evidence that an eventual campaign passes. Publication and independent remote verification of the final manifest remain prerequisites to the prospective numerical allocation.

### Verified resolutions

- The final specification keeps the corrected 48 explicit plus 208 supplemental binary pairs and the unchanged 1488-record total. It explicitly disclaims statistical independence. The result contract now describes IDs for all pairs, including the explicit controls.
- The final protocol requires the partial journal, full journal/final equality for baseline qualification, and six deliberate checker mutations. The runner's append/sync implementation is unchanged from Addendum 1; its partial-write/durability limits remain as stated there. Invalid journal content cannot qualify merely because the final summary exists.
- The final supervisor retains a separate live process-group guardian while the scientific child runs and is reaped. Release follows an observed absence of scientific group members. Group signals are conditioned on the guardian still being live; two post-exit group-absence probes are required by the source. The scope is explicitly reviewed code with sampled unexpected-descendant detection, not hostile-code isolation.
- The guardian's initial failure-emission path could itself fail before terminating its child. This was reported during the intermediate review. The final version makes failure emission best-effort and puts child termination/reaping in unconditional `finally` cleanup; it handles SIGTERM and ignores further SIGTERM during that cleanup. Cleanup no longer depends on successful lifecycle-file publication.
- Source and executable identities are checked before and after the stage. The final supervisor also compares the live manifest and publication-receipt bytes against its launch bytes, requires a unique manifest covering the mandatory protocol/arithmetic/runtime/executable sources, and checks the previous kernel supervision/output/journal before and after the checker. A prior kernel terminal-error record bars checker admission. This resolves the intermediate omission of manifest/receipt and prior-input postchecks.
- Runtime identity is explicitly executable-byte identity only. Node/V8 metadata comes from the runner; Python version/implementation metadata is now emitted by the checker. The exact public command templates are retained. Loaded system libraries are not pinned, consistently with the protocol.
- The frozen protocol defines supervised wall time through cleanup, log publication, source/runtime rechecks and output hashing, ending immediately before the separately required final metadata write. The supervisor checks that elapsed time against 120 seconds, accounts for current result-directory files and current private logs, reserves 64 KiB for its report, and enforces that report size. This is the adopted boundary, not the initial draft's ambiguous end point. Sampled RSS and actual maximum request gaps are reported; 0.05 seconds is a sleep duration, not a hard sampling guarantee.
- Finalization exceptions produce an outer best-effort terminal-error record with `success:false`, `closed:false` and closure unproven. A missing/failed final report remains unqualified. The source does not guarantee that storage failure will allow even the fallback file to be written; retained attempt/partial evidence and external status must preserve that limitation.

### Independent checker and fault-control relevance

The checker source was inspected without importing or running it. It independently regenerates the frozen input schedule, decodes binary64 into Python `Fraction`, derives rational operation images, and uses `math.isqrt` with squared comparisons for square-root endpoints. It checks the exact canonical outward endpoints and separately checks inclusion. It validates the manifest, required checker/spec/contract/runner pins, bounded JSON inputs without duplicate keys, record counts, IDs/order, operation/inputs, expected statuses, final input-equality flags and journal agreement. This is implementation diversity; the mathematical specification and deterministic schedule remain shared.

The six negative probes are source-level meaningful:

1. The minimum positive subnormal is strictly between zero and one lattice unit. Changing its recorded interval from `[0,1]` to `[1,1]` excludes its exact value; this is an inclusion failure, not merely a nonminimal wide interval.
2. The exact zero conversion is assigned an incorrect domain-failure status.
3. A required final record is removed.
4. A different row is replaced by a duplicate record.
5. Two distinct initial records are exchanged.
6. The zero input is changed to the positive subnormal while its original ID/output remain.

All six use the same `validate_core` as the baseline. Journal comparison is outside that validator, so an unchanged duplicate journal cannot alone make a numerical mutation appear detected. The baseline must pass before controls run, and all five control categories/six probes must reject for checker success. The checker returns a nonzero exit on a failed qualification or exclusive report-write failure. These conclusions concern the inspected control design; no probe was executed in this review.

### Retained limits and original goal

No script, module, parser, generator, checker, fault probe, runtime-identity command or scientific case was executed by this reviewer. Validation consisted only of reading source/prose, comparing source deltas, copying review snapshots and computing file hashes. No external retrieval, target-array access, new agent, or repository edit occurred. Eleven unique new-checkpoint content paths were read, with zero inherited content files; the inherited-file cap was not approached.

Remaining limitations are deliberate: finite deterministic cases do not prove universal correctness; malformed-input interface branches and emergency iteration paths are not empirically covered merely because their guards exist; input equality is a before/after observation; sampled userspace monitoring can miss transient peaks or short-lived/escaped processes; operating-system, guardian-loss and identity/signaling races are not eliminated; executable pins do not make the environment hermetic; and no cleanup/resource/fault-injection test has run. The independent arithmetic review remains responsible for the general mathematical argument. This checkpoint cannot replace current-geometry coefficient enclosure, coupled-load certification, complete browser cost, or physical validation work.

### Exact final snapshot

Paths below are relative to `research/m31-interval-primitives-2026-10-16/` in the public repository. All final bytes were copied into a source-review snapshot before delta inspection. The original drafts remain unchanged.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL-DRAFT.md` | 6226 | `15f86c9e11f7b69386b073219946539cbd66c59fe92b10b25936fdb53150a891` |
| `ARITHMETIC-ARGUMENT-DRAFT.md` | 3364 | `12363b18045043f5d550850a1f9d329f698ff96b0a71914d08ea4c0e77b4aecb` |
| `PROTOCOL.md` | 9660 | `c3b5faca9f9332277c2a8b8b4421f62f8c7f2496da430adfe7fc7debd950430e` |
| `runtime-pins.json` | 404 | `34dd9c5333c8fa945bd0667be7d042fc1eb09899895d942bf83b671c0b1a5b81` |
| `source/spec.json` | 2550 | `73d539b2f6575e21b3f8c512ce79a4be22ff0b09c98c527cb18dfc06a6dc21f7` |
| `source/run.cjs` | 3054 | `172dd45d3f1fe06f3562e3908d16e3d4d759f0c5e1f769f4f9d46860f09fcd0b` |
| `source/result-contract.json` | 2863 | `a41c1a936b3b4772e90de182abffd7b41dc552a0f217a15738015f5359a3d522` |
| `source/interval.cjs` | 2815 | `73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3` |
| `source/supervise.py` | 11202 | `bcba663a3391e7cfc0ebd2f0891c5ac6f23fe3cbbf1c626e4f4b7e5842c1c4fa` |
| `source/guardian.py` | 1656 | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |
| `source/check.py` | 30506 | `99e79de9747063825d3a6c8c0d2f8dc1e5fba6af8739204fa9b322184d96703c` |

Additional intermediate versions actually read before the final correction, besides those already recorded in the initial report/Addendum 1:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `source/supervise.py` | 9604 | `323b0421a80acf039c37c102652ca315d067ce16195ae080b89986370072476c` |
| `source/guardian.py` | 1383 | `a17b2cbb4ac82d5598625ab0f5addb6db7b213add6d6b218757d6b40b9c2434a` |
| `source/check.py` | 30335 | `9e054dc2ee021390fa1052f1927367cf2d91c120d688d93ca757ed08d4cc1a82` |

No other source, output, manifest or publication receipt was inspected in this task. The later source manifest and remote receipt must be checked by the publication gate; this report does not claim they already exist or have passed.
