# Current-pair protocol and supervision source review

Date: 2026-10-17, Asia/Shanghai. Reviewer: existing protocol/supervision reviewer. Scope: the new `m31-current-pair-v1` prospective allocation, constant/preparation decision, finite case declaration, saved-evidence interface, and reuse of the retained-guardian supervisor. No external retrieval, scientific code execution/import, fixture generation, numerical reference evaluation, resource probe, fault injection, target-array access, or additional agent was used.

This reviewer owns the new `source/supervise.py` adaptation and `source/guardian.py` copy. The report therefore records source authorship and inspection of those changes, not an independent audit of the reviewer's own edits. The mathematical reviewer owns the general target/arithmetic argument; the separately authored checker supplies a distinct implementation after publication. Source inspection cannot establish that a future execution or negative control passes.

## Initial disposition and remaining source gate

The prospective constant-encoding and rounded-preparation choices are approved as a specification decision, with the enforcement requirements below. The 322-case finite allocation and the two-stage/no-retry structure are acceptable within their stated limits. No remaining issue is identified in the narrow supervisor adaptation, which preserves the inherited controls.

At this initial writing, the final `PROTOCOL.md`, `MODEL.md`, runtime pins and independent checker are not yet reviewed here. Final source disposition and an exact final inventory will be added before publication. This initial section is not a source-publication receipt and does not authorize numerical execution.

## Constant and preparation decision

A finite expression graph with explicit binary64 round-to-nearest ties-to-even operations uniquely specifies constants before execution. It is legitimate to freeze that graph prospectively and materialize the hexadecimal encodings during the sole runner execution, provided the independent checker derives every required literal and expression result from exact rational/rounding rules and rejects any mismatch. The recorded result must never choose the target constant retroactively. In particular, inspecting `Math.sqrt` at the two adapter sites is not a proof that its answers are correctly rounded; exact reference comparisons are the qualification gate. The fixed PI encoding is part of that prospective definition.

The adapter's cross-product operation graph and each rounded center-plus-offset define the prepared values. The checker must independently reproduce the exact resulting bits, including signed zero. The subsequent predicates use those values as exact dyadics. The norm test `(base-t)^2 <= sum(v_i^2) <= (base+t)^2` is valid for the declared positive base and smaller nonnegative tolerance. For quaternion and axis base 1, it represents the two-sided norm band exactly; the earlier symmetric bound on `sum(q_i^2)-1` would not. The offset band uses the frozen R and geometry tolerance. No ideal quaternion rotation accuracy, native `hypot` accuracy or exact unit-axis assumption follows from this preparation choice.

The contract requires all raw components finite and both sets of forces positive before preparation; it requires all prepared components finite and all exact geometry predicates valid before self or geometric-zero exits. Consequently a `self` flag cannot bypass invalid preparation. The `self-invalid` and `near-before-projection` declarations are relevant ordering controls. Source inspection of the adapter agrees with this declared early ordering. The point coordinates are independently rounded center-plus-offset outputs, so a large common translation may change rotor displacement; the `large-translation` case is a probe of that declared model, not a translation-invariance claim.

## Finite allocation and coverage limits

The declaration contains 322 standalone two-state queries: 280 axis-aligned grid records (ten vertical positions, seven lateral positions, four receiver rotor indices), 20 attitude records (five declared attitude choices, each with four rotors), and 22 named special records. The special IDs are `self`, `self-invalid`, `invalid-quaternion`, `zero-force`, `negative-force`, `nan-input`, `inf-input`, `center-component-guard`, `center-norm-guard`, `neighbor-boundary`, `asymmetric`, `scaled-cap`, `tiny-force`, `huge-force`, `projection-zero`, `near-before-projection`, `near-exact-radial`, `near-outside`, `large-translation`, `radial-fade`, `radial-cut`, and `down-before-radial`. This is an enumerated deterministic suite. There is no random-sampling, independence or exhaustive-coverage assertion.

The current contract limits permitted unresolved stress outcomes to `tiny-force` and `huge-force`. Those outcomes remain unqualified queries and must be counted and explained. A protocol-conformant run with one or two such outcomes cannot be described as qualification of all 322 queries. All 320 ordinary queries must be resolved, and every reported resolved outcome must satisfy the independently checked exact target/status or containment rule. A sound positive result or a proved target rejection for a stress record is also allowed. A checker reference that cannot decide the relevant target is visible failure to qualify, not a new exception. No post-result case changes, adaptive precision or additional execution are allowed.

Several names indicate intended probes, not facts proved by their names. In particular, `center-norm-guard` has coordinate displacements 258 and reaches the preceding component guard. More generally, the center norm bound 512 cannot fail after each of its three components is bounded by 257, since `3*257^2 < 512^2`. That branch's presence cannot be called an independently exercised guard. Likewise, a decimal labeled near or exact radial does not by itself establish equality to a rounded-expression boundary. Coverage claims should identify the checker-observed exact branch in the eventual evidence and retain cases that share geometry or branches as separate declared records. No new cases are proposed on the basis of runtime results.

## Runner and saved-evidence interface

The runner maps the fixed decimal/nonfinite fixture strings to binary64 input bits, applies the declared overrides and keeps the specified ID order. It retains the full raw input, prepared bit evidence and result for every completed query. It writes an exclusive `pair-results.json.jsonl` journal: header, one record per completed query, and a completion count. It syncs the header, every 16 records and completion. It checks the final record count and writes the final result file exclusively. Its emitted source hashes cover the spec, result contract, lattice arithmetic, rational helpers, adapter, pair implementation and runner; those hashes are evidence to compare with the source manifest, not a replacement for manifest checks.

The final saved-result checker invocation remains:

```text
PYTHON PACKAGE/source/check.py --spec PACKAGE/source/spec.json --input PACKAGE/results/pair-results.json --manifest PACKAGE/source-manifest.json --output PACKAGE/results/independent-check.json --root REPOSITORY_ROOT
```

The journal path is the input path plus `.jsonl`. Baseline qualification must require complete journal/final equality and exact declared counts/IDs/order/inputs. Numerical negative controls must go through the same core evidence validator independently of journal comparison. Seven declared probes cover an unsound positive interval, wrong branch, altered prepared operand, missing record, duplicate record, reorder and changed raw input. Duplication and reordering are distinct probes. Controls need genuine semantic or evidence corruption, not merely a different but still valid enclosing interval.

The runner's individual `fs.writeSync` calls retain the inherited lack of an explicit short-write loop. A truncated/malformed journal must fail qualification; fsync cadence does not imply durable storage of every case after a crash. Unexpected exceptions before the next journal row remain a failed stage with retained earlier evidence, not a hidden resolved case. No durability or corruption control has been executed in this review.

## Supervisor adaptation and preserved controls

The guardian is copied byte-for-byte from the closed interval-primitive checkpoint. The supervisor changes only the mandatory source list, the kernel result basename, and the matching checker argument/template. `MODEL.md` replaces the primitive arithmetic argument in the mandatory list, and the new rational/adapter/pair sources are included. Required files are:

```text
PROTOCOL.md
MODEL.md
runtime-pins.json
source/spec.json
source/result-contract.json
source/interval.cjs
source/rational.cjs
source/adapter.cjs
source/pair.cjs
source/run.cjs
source/check.py
source/guardian.py
source/supervise.py
```

Source-only comparison confirms that the original supervision logic is preserved:

- Manifest entries are unique and cover mandatory files. The source-publication receipt must assert remote/local byte equality and the matching manifest digest. All listed source pins and the actual Node/Python executable bytes are checked before launch. The exact manifest and receipt bytes, source pins and executable pins are checked again after the stage.
- Exclusive stage attempt files prevent an overwrite/retry in the same preserved allocation. The checker is admitted only after a successful, closed kernel stage with matching source commit/manifest and unchanged saved output/journal. A kernel terminal-error record bars checker admission. Kernel output, journal and supervision identities are checked again after the checker. The publication receipt is an external attestation consumed by this code; the supervisor does not itself retrieve remote source.
- The live guardian retains process-group ownership until the scientific child has been reaped and the supervisor observes no scientific group member, then receives release. Guardian error logging is best-effort; cleanup is in `finally`, independent of a successful event write. Signals are sent only while the guardian is observed live. Two post-exit group-absence probes are required. Reviewed candidate modules contain no subprocess-launch facility. The checker must satisfy the same no-subprocess condition.
- Each stage has 120 seconds supervised wall time, sampled group RSS capped at 1 GiB, and 16 MiB of accounted output. The nominal sleep is 0.05 seconds; actual maximum request gaps are reported. Output accounting includes current result-directory files and current private stdout/stderr, including prior-stage result files during the checker. Current raw logs and their published redacted copies are both counted. Unexpected sampled group members and observed escaping descendants trigger failure.
- The adopted wall boundary includes start, sampling, cleanup, log publication and identity/output postchecks, and ends before the separately bounded final report write. A 64 KiB report allowance is reserved and enforced. Successful qualification requires final report publication; a missing or failed finalization cannot qualify. The outer error path attempts a terminal-error record with success and closure false. Storage failure may prevent even that fallback from being saved.
- Private logs are retained with raw hashes. Published logs replace repository/private/runtime path prefixes and record both raw and published sizes/digests. This substitution is not a general privacy audit; publication still needs the parent's privacy review.

These are sampled userspace controls for reviewed children, not a hard operating-system resource sandbox or hostile-code containment guarantee. They can miss transient peaks or short-lived/escaped processes, and they retain operating-system, guardian-loss and identity/signaling races. Runtime pins cover executables, not every loaded library. No runtime, cleanup, cap, timing or fault behavior has been demonstrated by this source-only adaptation. Supervisor success means the stage process/closure/output conditions held; the independent checker report and declared scientific criteria remain necessary for scientific qualification.

## Claim limits and next gate

This checkpoint can establish recorded per-query preparation/status/containment checks against the declared target. It cannot establish universal correctness from a finite suite, a complete row bound, ordered positive-term count, coupled-load certificate, present-geometry hierarchy performance, 5,000-drone browser throughput, physical validity or novelty. The eventual milestone page must keep its historical airflow-off replay clearly separate from new pair evidence. No new flight or scientific browser allocation is implied by display QA.

Before the sole numerical allocation, freeze the reviewed protocol/model/spec/contract/code/runtime identities; retain prefreeze corrections; publish and independently verify the exact-commit source manifest; then admit kernel and saved-result checker in order. A failed attempted stage is retained and closed. Unstarted dependent stages remain unspent. The source-publication and runtime outcomes have not been observed by this reviewer.

## Reading inventory at initial writing

Exactly three inherited content files were read, within the cap of twelve. No `AGENTS.md` existed at the checked ancestor/package paths. All other content read is in this new package. File listing, hashing, source copying, textual comparison and authoring were the only tooling operations; candidate/checker code was not imported or evaluated.

| Inherited path relative to repository | SHA-256 |
|---|---|
| `research/m31-interval-primitives-2026-10-16/PROTOCOL.md` | `c3b5faca9f9332277c2a8b8b4421f62f8c7f2496da430adfe7fc7debd950430e` |
| `research/m31-interval-primitives-2026-10-16/source/supervise.py` | `bcba663a3391e7cfc0ebd2f0891c5ac6f23fe3cbbf1c626e4f4b7e5842c1c4fa` |
| `research/m31-interval-primitives-2026-10-16/source/guardian.py` | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |

Initial new-package content reads/snapshots, relative to this package:

| Path | SHA-256 |
|---|---|
| `PROTOCOL-DRAFT.md` | `ce3c69ab343ffb1a44d73cd3700a4fffbf0ffbaadf3c66c507a8b17c103f0323` |
| `source/spec.json` | `49ca3fef52dd0a12df8696db4c40ba43c155eba91533675ec6261cb4f61d66ab` |
| `source/result-contract.json` | `9e93428f7f32611d678d710c9d3957191a156bafcbfb9d17d384d55338c16508` |
| `source/interval.cjs` | `73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3` |
| `source/rational.cjs` | `de2adde5459d37cc537709f7a488605d9c21d8eedf022efc0a3e9461d4d97333` |
| `source/adapter.cjs` | `5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145` |
| `source/pair.cjs` | `e9fb2f4d7e4d1da09f53c082cf09a3b01c906a9d77642ae333319118b2f568cc` |
| `source/run.cjs` | `26f36b36ff66fb7a2c8a8ccdf8cf3850fb7a48213d9265a4795de16157081f28` |
| `source/guardian.py` | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |
| `source/supervise.py` | `1c9f61f2e42cace199ca5ce80eaeae5f124562a63d2bb620529ce060b457a87f` |

## Addendum 1 — final protocol/model and current no-blocker disposition

The final `PROTOCOL.md`, `MODEL.md`, runtime-pin declaration and refreshed contract have now been read. **No blocking issue is identified in the reviewed protocol, constant/preparation choice, finite allocation or supervisor/guardian adaptation at the identities below.** This remains a source-only disposition. The complete independent checker is still being authored; its journal/source/coverage/fault gate will receive a separate additive source review before the source-publication gate can close.

The final protocol now states the exact 322-case breakdown, the 320 ordinary/two stress distinction, `verificationPassed` versus `fullQualification`, canonical nonfinite/signed-zero input semantics, the unreachable center-norm guard and the limited meaning of boundary names. It preserves the wall boundary, final-report reservation, sampled-resource limits, executable-only runtime pins, closed allocations and failed-stage evidence requirements. The model explicitly adopts the constant encoding algorithm, rounded point semantics, actual near-unit axes, exact force sums, conservative cap decisions and fixed reference precision. These choices are approved for this prospective limited target; none implies universal or physical qualification.

The refreshed result contract explicitly declares the displacement direction and canonical raw encodings. Its later whitelist of unresolved branch strings is restricted by the separate two-stress-ID policy; it does not authorize unresolved ordinary cases or turn any unresolved query into a usable certificate. These are prospective source clarifications. The initial contract snapshot is retained by the parent, and the earlier reading identity above is preserved.

At the parent's request, the protocol's display scope was clarified to allow a Three.js pair-geometry diagnostic derived only from saved raw/prepared evidence, recorded statuses and intervals, beside the unchanged historical airflow-off replay. Display coordinate conversion/rendering is allowed; re-running preparation, pair/reference calculations or trajectories is excluded. The parent's appended clarification additionally requires illustrative marker labels and disclaims browser coefficient qualification. The reviewer made the closure-paragraph clarification and then ceased protocol editing. The reviewed pre-clarification final protocol was 10,955 bytes, SHA-256 `598080f79eff2b02937f272aef430d8acb0a58dd6abdd8098a0fc791089742a8`; its snapshot is retained privately. The displayed diagnostic itself is not yet inspected here.

The inherited reading count remains three (9,660-byte prior protocol, 11,202-byte prior supervisor, 1,656-byte prior guardian; identities above). Fourteen distinct new-package source/document paths have now been read, excluding this authored report. The checker entry below is explicitly only its then-current 152-line helper prefix, not a completed checker review. No source manifest, publication receipt, scientific output or runtime executable bytes were read by this reviewer. Runtime pins were read as declarations, not independently verified against the local executables. Metadata-only file hashing/copying does not execute the numerical programs.

| Reviewed path relative to this package | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL-DRAFT.md` | 7922 | `ce3c69ab343ffb1a44d73cd3700a4fffbf0ffbaadf3c66c507a8b17c103f0323` |
| `PROTOCOL.md` | 11432 | `6ab6409b2f9e68a7add693c5151c5904a1107dca1840ce87b217b20cd0db4295` |
| `MODEL.md` | 4754 | `542978ef7f69f76c8b241631d15a823acf974c61e6feee18576a83beffb8403b` |
| `runtime-pins.json` | 248 | `842b2522133ed499f4706e071b09f3d100c5f4ed3f41d0fd135736c4dc191087` |
| `source/spec.json` | 47250 | `49ca3fef52dd0a12df8696db4c40ba43c155eba91533675ec6261cb4f61d66ab` |
| `source/result-contract.json` | 3843 | `06236c082b0b754ce8fc68c4455c4a0088c66a0f4c6fa4260fc8fa013612760c` |
| `source/interval.cjs` | 2815 | `73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3` |
| `source/rational.cjs` | 1188 | `de2adde5459d37cc537709f7a488605d9c21d8eedf022efc0a3e9461d4d97333` |
| `source/adapter.cjs` | 2400 | `5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145` |
| `source/pair.cjs` | 3579 | `e9fb2f4d7e4d1da09f53c082cf09a3b01c906a9d77642ae333319118b2f568cc` |
| `source/run.cjs` | 1993 | `26f36b36ff66fb7a2c8a8ccdf8cf3850fb7a48213d9265a4795de16157081f28` |
| `source/guardian.py` | 1656 | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |
| `source/supervise.py` | 11235 | `1c9f61f2e42cace199ca5ce80eaeae5f124562a63d2bb620529ce060b457a87f` |
| `source/check.py` (incomplete helper prefix only) | 5404 | `eef664afb60d4f39ec27e03d235c2bd243ee7139d4c55b8976291b11edc62df8` |

## Addendum 2 — stress exception narrowed before execution

The independent mathematical review identified that merely limiting the broad unresolved vocabulary to two stress IDs could still excuse an internal `invalid-bits` or `invalid-interval` defect. The parent has prospectively narrowed the contract with `allowedStressUnresolved`: only `tiny-force` with branch `normalizer`, and `huge-force` with branch `unresolved-range`, may be accepted as declared unqualified stress refusals. Every other unresolved case/branch combination must fail verification. This supersedes the earlier broad-whitelist interpretation in Addendum 1; the earlier discussion is retained as review history. The correction does not qualify either refused query for use and does not permit a false zero or false rejection. The reviewed contract version has SHA-256 `be32e10be8065ade07754b8d3aa1a20f70e77ab19ce6133f0665537241f3f589`. Checker enforcement of this exact map remains part of the pending final source review. No numerical evidence guided this correction.

## Final addendum — completed checker and exact final source disposition

**Final disposition: no remaining blocking static issue is identified in this review's protocol, allocation, constant/preparation gate, supervision and checker-evidence scope for the exact source snapshot below.** The constant/preparation choice is explicitly approved on the conditions already stated. The earlier findings, scope limits and authorship distinction remain in force. This is not a numerical pass, runtime-safety demonstration, publication receipt or approval to bypass the independent exact-commit publication gate.

The completed 952-line checker was read as source. Its earlier helper prefix is unchanged; the remaining source covers exact binary64 rounding and preparation, exact-rational/fixed192 reference construction, coverage/status/containment validation, journaling, seven negative controls and CLI/report handling. The final protocol has additionally incorporated the narrowed stress exception; its earlier text is unchanged. No source/checker/constant graph, reference, fixture or mutation was evaluated.

### Verified source-level gates

- The checker has no candidate imports or subprocess-launch code. It independently reconstructs all declared raw inputs from the pinned specification, checks the 322-case count, unique declared IDs and exact rotor/override grammar, and compares every saved ID/order/input and prepared record. JSON equality distinguishes booleans, integers and floats. Duplicate JSON keys, nonfinite JSON numeric tokens, malformed bit strings, excessive input/source sizes and noncanonical endpoint strings are rejected. Missing/extra/duplicate/reordered records cannot be hidden by aggregate counts.
- Its literal/RN arithmetic uses exact `Fraction`, integer quotient/remainder and ties-to-even. The two constant square roots use a search over ordered representable positive values, exact squared comparisons and squared midpoint tie decisions. The entire emitted constant table must equal the independently constructed graph; source hash reports must equal pins from the verified manifest. Prepared bits are independently reconstructed with signed-zero-aware operations before exact geometry/status comparisons. These are source-design findings, not observed constant values.
- The exact branches and declared preparation precedence are checked separately from enclosure comparisons. For positive records, each of K, scaledK, beta, nu and coefficient must have canonical ordered fixed96 endpoints within the representation range, a nonnegative lower endpoint, and contain the whole corresponding independent reference interval. In addition, candidate K and scaledK upper endpoints must be at most 128 and candidate nu lower endpoint strictly positive. Thus a very wide interval containing the reference cannot certify the cap or a usable normalizer merely by inclusion. Width diagnostics are explicitly descriptive and do not introduce a result-dependent acceptance tolerance.
- `read_contract` requires the exact two-entry stress map, and `validate_core` checks both the stress ID and its allowed branch. It rejects a stress refusal before an exact early zero/preparation/geometry branch, and ordinary unresolved records always fail. `invalid-bits`, `invalid-interval`, cap/domain/iteration failures and any other unexpected unresolved combination cannot borrow the stress exception. A permitted refusal remains `qualified:false`. Reference-undecidable stress evidence is visible and cannot make `fullQualification` true. A resolved candidate against an undecidable reference fails qualification. `ordinaryQualifiedRecords` must equal 320; `fullQualification` additionally requires all 322 records qualified.
- Baseline journaling is separately mandatory: at most 16 MiB, exactly 324 lines, exact schema/spec header, 322 row records equal to the final saved rows and exact completion count. Malformed/partial/different journal evidence fails final verification even if the numerical core would otherwise pass. Source manifest checks include bounded canonical repository paths, unique entries, file bytes/hashes, the checker/spec/contract and all seven candidate source files. The enclosing supervisor adds the mandatory protocol/model/runtime/guardian/supervisor list and prior-stage/postrun rechecks; the checker alone is not represented as the entire publication/identity gate.
- All seven negative probes call the same `validate_core` used for baseline evidence. That validator contains no journal comparison, so a numerical mutation is not detected solely because its duplicate journal stayed unchanged. The positive-interval probe selects a reference coefficient with strictly positive lower bound and replaces its candidate interval by `[0,0]`, which excludes the target. The branch probe changes the valid self exclusion to neighbor. The prepared probe flips a bit of a receiver point; the raw-input probe flips a bit of an initial receiver center input. The remaining probes remove the last required row, duplicate the first row into the second, and exchange the first two distinct rows. These are genuine evidence/semantic errors. A valid baseline and suitable witnesses are required; all seven must be executed and rejected. No probe has actually run in this source review.
- Final `verificationPassed` requires the baseline, journal and all seven controls; `fullQualification` additionally requires all 322 queries qualified. The CLI returns nonzero for failed verification or exclusive report-write failure. Reports preserve reference and observed statuses, unqualified counts, per-case evidence, constants and source provenance. The supervisor's process success is consequently distinct from full finite qualification, especially for the two prospective stress refusals.

### Final inventory and remaining responsibilities

The completed checker adds no inherited content file. Final reading count is **three inherited files and fourteen new-package source/document paths**, excluding this authored report. The initial/intermediate identities above remain preserved; the final checker replaces only the incomplete-prefix entry in the current disposition. Mathematical generality remains the separate mathematical review's responsibility. The diagnostic viewer, scientific outputs, manifest/publication receipt, runtime executable bytes and remote source were not inspected here. The parent must freeze/publish and independently verify final source bytes before the sole kernel/checker stages; no such verification is implied by these hashes.

| Final reviewed path relative to this package | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL-DRAFT.md` | 7922 | `ce3c69ab343ffb1a44d73cd3700a4fffbf0ffbaadf3c66c507a8b17c103f0323` |
| `PROTOCOL.md` | 11862 | `5c5b736ff8c5a96098e71f0ed12025c773ae2bd5638ec809ba3e4241d46eccb9` |
| `MODEL.md` | 4754 | `542978ef7f69f76c8b241631d15a823acf974c61e6feee18576a83beffb8403b` |
| `runtime-pins.json` | 248 | `842b2522133ed499f4706e071b09f3d100c5f4ed3f41d0fd135736c4dc191087` |
| `source/spec.json` | 47250 | `49ca3fef52dd0a12df8696db4c40ba43c155eba91533675ec6261cb4f61d66ab` |
| `source/result-contract.json` | 3976 | `be32e10be8065ade07754b8d3aa1a20f70e77ab19ce6133f0665537241f3f589` |
| `source/interval.cjs` | 2815 | `73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3` |
| `source/rational.cjs` | 1188 | `de2adde5459d37cc537709f7a488605d9c21d8eedf022efc0a3e9461d4d97333` |
| `source/adapter.cjs` | 2400 | `5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145` |
| `source/pair.cjs` | 3579 | `e9fb2f4d7e4d1da09f53c082cf09a3b01c906a9d77642ae333319118b2f568cc` |
| `source/run.cjs` | 1993 | `26f36b36ff66fb7a2c8a8ccdf8cf3850fb7a48213d9265a4795de16157081f28` |
| `source/guardian.py` | 1656 | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |
| `source/supervise.py` | 11235 | `1c9f61f2e42cace199ca5ce80eaeae5f124562a63d2bb620529ce060b457a87f` |
| `source/check.py` | 44757 | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
