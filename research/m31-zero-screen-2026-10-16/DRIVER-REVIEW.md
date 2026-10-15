# Static review of the unexecuted E/L zero-screen draft

Reviewed 2026-10-16 (Shanghai). Repository: <REPOSITORY_ROOT>. Campaign: research/m31-zero-screen-2026-10-16. Reviewer: m31_evidence_audit.

## Disposition

The inspected revised driver/control/config/schema/protocol are consistent with the proposed bounded experiment. Two failure-evidence blockers were identified and repaired during this static review; the revised source was reread. No unresolved implementation/accounting blocker was found in this snapshot. This is not final launch clearance: the historical DOT comparison is still pending, and the final source/protocol/dependency freeze, publication, independent exact-pin verification and supervisor/ledger review remain outstanding. No claim of observed numerical correctness, speed or novelty follows.

This review used source text, file reads, byte hashes and declared-size arithmetic only. It did not import/execute a scientific module, generate fixtures/lattices, compute scientific geometry/fields/roots, invoke a checker or benchmark, modify repository files, prepare the saved reviewer, or launch any scientific process. Existing challenge documents remain unchanged.

## Snapshot

| File | Bytes | SHA256 |
| --- | ---: | --- |
| config.json | 2420 | 02218a9db1c452e4a6ebcfb9feb91484394f27a9ab23c89ab4781c4253ce86a9 |
| schema.json | 1705 | 4211bd6440fe4aa5ce3c89c27dcc2bb2c35934e05c8f2d01a2f457cb4c0c0e3b |
| source/experiment.cjs | 21394 | c7c9fe0b20be101b09d0240b93c24a9a7c017594eda79fb12107b066b1acfae6 |
| source/control.cjs | 7281 | e029139f71a7eaca1ca1e4f175eac0313060ae9aa1670c7e773ac077dcd73725 |
| PROTOCOL.md | 12319 | 791e321f7b17f695085d732a592049c0426cd24a42f387c03dd2d53d82a0eb79 |
| DRAFT-STATUS.md | 1378 | 368b56607089ef1cc7caca36511cdc6ea88aefa95551e74965c5a5ab7e4e56c7 |
| CONTROL-NOTE.md | 9880 | f69213b8a6c360428f946abbf70aca6dbb4d079f0ce15378c833ba1393d2f06a |

The initial experiment draft was 20,824 bytes, SHA256 e3ab90a725e0fd7bd0c12a59b0f481c543bd6e4068ec091a87f7db80674bcfc7. The next 20,824-byte version, SHA256 f99bb07ab98e53c5eddbc1193cb9ed63d9e1e46d245ee21c50b43562e111e30a, moved current attempted-call context before charge. The reviewed final snapshot above includes the witness and timing-summary repairs.

## Repairs verified by source inspection

1. exactRows used Object.is but previously serialized only numeric values/full rows through JSON. A mismatch between positive and negative zero would therefore lose its distinguishing evidence. The revised function encodes both failing full rows as Float64LE/base64; checksum mismatches encode both scalar bit patterns. These buffers are constructed only on failure. Runtime equality still uses Object.is. This also preserves numerical encodings that JSON would otherwise collapse; it does not relax admission or finite-output gates.
2. The timed-record gate previously saved only input/repetition/method/receiver IDs. Successful timed matrices/masks are intentionally not duplicated, so the actual failed timed mask/record would not be recoverable. The revised gate retains first-failure actual/reference mask bytes and record scalars in its diagnostic detail. Evidence remains subject to the declared bounded failure policy.
3. The protocol now accurately states that each returned matrix is saved before its subsequent comparisons. M/Z/E/L comparisons precede the one scheduled I pass. It no longer implies all five matrices exist before that first comparison.
4. timingConclusions now explicitly emits median/minimum/maximum for every measured method from the existing eight blocks. No additional timing pass was added.
5. Current call context is set before precharge, so a cap failure identifies the attempted call rather than the prior completed call.

## Static implementation observations

The four model/grid dependency paths are identical to frozen Z. New exactTerm and loadRows are byte-identical to Z: exactTerm is 857 bytes, SHA256 6a9781a362f828106d532c1533bda9fd9a0c0f277791c03af22db181ddeec168; loadRows is 271 bytes, SHA256 0f47d083d363fa21d4ec9ea9780e6fabff5df85d8562a2851f982679007aa9b4. These extracted helper fingerprints exclude their following separator newline/function.

E retains the d0/r0/lo/hi/rlo expression order, geometry allowance, domain-first fallback, strict near skip, dH/half/qlo and radial/projection zero predicates. It removes dL and the positive-bound magnitude/inflation/selection tail, with the retained result still a two-property object. E/Z consequently measures removal of the full positive-policy/shadow package and its reporting costs, not an isolated scalar expression.

L moves only radial residual/r0/rlo evaluation past the first downstream-zero branch. The downstream interval computations and predicates are identical. The surviving branch computes E's exact radial expressions before near-domain fallback. Projection remains eager in the caller. The shared field body retains global tilt admission, rotated offset/radius and axis/operator norms, grid/neighbor order, all four exact rotor evaluations for retained categories, accumulation and load/checksum paths. Both classifiers increment the same downstream-exit counter at the same logical branch. Both always construct category masks/records during measured calls. No extra helper/source/field call is used for verification.

The per-receiver/aggregate centerRadialHypotCalls values are derived operation counts from candidate counts and same-pass downstreamZeroExits. They are not independent geometric replay or hardware counters, and the protocol says so. E/L differ in that derived count; their other counters/masks are required equal.

## Driver gates and evidence

Each correctness input has the ordered methods M,Z,E,L,I. Each complete production matrix is saved as Float64LE before its comparison. Expected rejection is required to agree among all five methods, and the saved source of the 24 fixtures remains fixed. Domain streams preserve completed prefixes; they are not asserted complete.

For complete inputs, E/L category masks must be byte-equal. Code3 maps to retained2 for the actual-mask comparison with Z; Z shadow-selected3 must specifically map to E/L remaining-retained3. Category/conservation/work and fallback counts are checked; Z does not expose fallback identities, and the protocol does not claim to compare those identities. E and L rows/checksums must each match Z with Object.is. All four full implementations also face unchanged independent precision/range/root/power qualification. Timing outputs/records/counters must match their own correctness references.

The one I pass uses the already-produced terms and classifications to inspect every shared claimed-zero rotor slot. The runtime accepts support codes {1,2,4,5,6,7}, requires term===0, and retains an ordered [source,rotor,term] exception for every claimed-zero code7 slot. The full 4N code stream, length/hash, code counts, eligible/contribution counts, zeroInspections, exceptions, roots and full row are saved per completed receiver. Current full term/code buffers enter failure context and are released after successful retention. A saved-only reviewer must enforce the stricter reconstruction rule: codes {1,2,4,5,6}, or code7 plus its unique exact-zero exception; code0/3 are not zero certificates. It must validate complete eligibility/length/hash/order/padding/conservation and exhaustive exception coverage without scientific replay. These are still recorded oracle semantics, not independently regenerated physical truth.

The warmup order MZLE and eight measured orders MZLE,ZEML,ELZM,LMEZ repeated twice match config and protocol. Both E/Z and L/E use the median of paired ratios, averaging sorted entries4 and5, and strict faster counts. The joint criterion is median<=0.95 and at least7/8 wins separately on both fresh inputs. Numerical completion and cost criteria are separate: criterion failure may be a completed negative result. Timing records are retained before timing validations; successful full timed matrices remain omitted as disclosed.

## Exact reservations

The declared sizes, including full-shape reservation for expected early rejects, give:

| Reservation | Exact total | Cap |
| --- | ---: | ---: |
| Field calls | 202 | 202 |
| I ordered nonself center slots | 25,994,070 | 26,000,000 |
| Z/E/L screen slots | 779,820,210 | 780,000,000 |
| Rotor source slots | 4,263,017,400 | 4,300,000,000 |
| Rotor-law slots | 985,040 | 1,000,000 |
| Integration steps | 0 | 0 |

This is 26×5 correctness calls plus72 timing calls. The 24 fixtures contain52 state rows and70 ordered nonself pairs; fresh inputs contain6,000 rows and25,994,000 pairs. Each screened method reserves259,940,070 slots. Expected charges and ordered-case/method/timing checks match these totals. No spare field call exists; no diagnostic field/root repeat is authorized.

Storage remains conditional on compression: nominal states+five outputs+three masks+full oracle code bytes total128,439,091 bytes before framing/roots/audits/timings. Normal writes must remain below130,023,424 bytes; the separate4,194,304-byte reserve is inside134,217,728 total raw bytes. Per-write bounds, cooperative guards and bounded failure serialization are present. If full failure context cannot fit, it is explicitly incomplete with original byte count/hash and a smaller terminal context. This is an allowed terminal incomplete result, not permission to trim or retry. The prospective external supervisor must enforce total cap/time/process-group/launch-lock rules independently.

## Outstanding before launch

Incorporate and review the remote later-DOT lean/support/reuse history and exact-zero optimization comparison. E must not be represented as a new zero-only method; the inspected downstream-first pattern also does not establish novelty for L. Then freeze all consumed sources, dependencies, config, schema, protocol, prior-work provenance and reviewer disclosures; publish and independently verify exact pins. Review the supervisor/sole-invocation ledger at the final version. Stop-new-launch deadline remains2026-10-15T23:00:00Z. No trial, retry, seed replacement or added scientific diagnostic is cleared by this note.
