# Independent saved-evidence audit: interval primitives

Review date: 2026-10-17, Asia/Shanghai. Package: research/m31-interval-primitives-2026-10-16.

## Disposition

The inspected saved evidence supports successful qualification of the frozen finite primitive suite on its recorded Node/V8 and Python runtimes. The checker reports all 1,488 required records, zero baseline mismatches, agreement with every expected status count, complete journal agreement, and rejection of all six deliberate fault probes. Both supervised stages report successful, closed execution with exit code zero. Fresh local byte/length checks matched all 23 frozen source pins and all seven output/journal/published-log pins from the two supervision reports.

No contradiction requiring a rerun or a change of scientific result was found in this review. This is acceptance of the scoped saved evidence. It is not a new numerical analysis, an independent reevaluation of the primitive equations, or completion of the full M-current, browser, flight, physical-validation, scale, or publication-readiness goals.

## What was directly checked

I read the frozen protocol, adopted arithmetic argument, source-publication receipt, source manifest, independent checker report, two supervision reports, two attempt records, and two guardian lifecycle records. I inspected the saved primitive-result metadata, its array length, and seven selected records. I freshly hashed the source-manifest entries and the output/journal/log artifacts against their saved byte lengths and pins. A standalone metadata script used only standard-library file reading, JSON parsing, byte lengths, and SHA-256; it did not import package code or evaluate any primitive.

No source, result, or existing review was edited. No case generation, numerical reference, kernel execution, checker execution, scientific import, target-array access, external retrieval, or additional scientific attempt occurred. No runtime executable was freshly hashed in this review; the executable pins and pre/post identity checks below are assertions recorded by supervision. No remote publication fetch was repeated.

The inventory below distinguishes full content reads, selected saved-result inspection, and hash-only access. All accessed artifacts belong to this checkpoint; no inherited content file was newly read. The kernel's freshly matched SHA-256 is the same one examined in my earlier source-only mathematical review, so that reviewed source identity has not changed.

## Qualification includes correct refusal outcomes

The independent report records these matching expected/observed counts:

| Recorded status | Records | Interpretation |
| --- | ---: | --- |
| ok | 1,032 | A successful enclosing interval was returned and accepted by the independent validator. |
| unresolved-domain | 215 | The represented operation's declared domain did not permit a successful whole-interval result. |
| unresolved-range | 236 | The bounded lattice representation could not supply a permitted result for that case. |
| invalid-nonfinite | 5 | Nonfinite binary64 input was explicitly refused. |
| invalid-bits, invalid-interval, unresolved-iteration, unresolved-sqrt-check | 0 each | None recorded in this fixed suite; this does not add malformed-input coverage. |

These are 1,488 validated case outcomes, not 1,488 successful interval outputs. The 456 refusal/invalid outcomes are expected behavior under the frozen contract. They are not failed scientific runs or discrepancies hidden from the denominator. Conversely, primitive qualification does not imply that all those inputs would be usable by a later model certificate.

The saved result array directly has 1,488 entries. The frozen allocation declares 160 conversions, 304 unary cases, and 1,024 binary cases. The checker reports baselinePassed=true, passed=true, baselineErrorCount=0, errors=[], and totalRecords=expectedRecords=1488. Exact case identity/order, endpoint correctness, input immutability, and status expectations are acceptance assertions of that saved checker execution; this audit did not independently regenerate or numerically recheck the full suite.

The selected saved rows make the refusal interpretation concrete without recomputation:

- bits-0 and bits-1 record the two signed-zero input patterns as ok with integer endpoints [0,0].
- bits-2 records minimum positive subnormal bits 0000000000000001 as ok with endpoints [0,1], and bits-3 records the negative counterpart as [-1,0]. Endpoints are lattice integers, so the represented scale is 2^-96. Inclusion of zero is visible; these successful conversions do not preserve a useful strict-positivity certificate.
- sqrt-2 records input endpoints [-1,-1] and unresolved-domain.
- bits-21 records input 4ff0000000000001 and unresolved-range.
- bits-26 records input 7ff0000000000000 and invalid-nonfinite.

All seven selected rows record inputUnchanged=true. This selected inspection does not replace the full checker assertion for all input records.

## Fault controls and retained evidence

The checker report contains five fault-control categories and six concrete probes. Every category records executed=true and passed=true, and every probe records rejected=true:

1. A narrowed minimum-subnormal interval is rejected for both not-exact-outward-endpoints and rational-inclusion-failed at row 2.
2. A zero conversion mislabeled unresolved-domain is rejected, including a result-status error at row 0.
3. Removing the last record produces a record-count error.
4. Duplicating a record produces duplicate ID, order, and input errors.
5. Reordering the first two records produces order and input errors.
6. Altering the first input produces a record-input error.

These recorded failures address numerical and record-contract mutations; they are not merely journal-mismatch messages. They demonstrate the validator detected these six frozen mutations. They are not an exhaustive proof that any faulty implementation or record tampering will be detected.

The checker records a complete journal with 1,488 rows and journal.passed=true. I freshly verified both retained artifacts against their published pins:

- primitive-results.json: 812,099 bytes; SHA-256 934030da979dc7808f26bfbcbb02c09a858ecc1c9a753df1f8a1c63c4a3bbfeb.
- primitive-results.json.jsonl: 592,720 bytes; SHA-256 30a59f8d43419bcd55c422056d4da818130166486c14777e4863d556162f01e5.

The journal's semantic equality with final records remains a result of the saved checker. This audit verified its identity without replaying journal rows or evaluating cases. The independent-check.json hash also matches the checker supervision output pin.

## Publication identity and execution order

Both attempts and both supervision reports identify source commit 7f353dee5a1a06f15f4fc2cb85a20da3f653fd0c and source-manifest SHA-256 fb3585e2eb5340a456fac47ec35957be9a5fcdc1e44425990475c9e3de3858dd. The freshly read manifest is 5,266 bytes and matches the receipt's manifest identity. All 23 local entries match their frozen byte lengths and hashes.

The publication receipt records exact-commit HTTPS retrieval with TLS verification enabled, remoteBytesEqualLocal=true, and localAndCommittedSourcePinsVerified=23. It retains two prior connector transport failures with no returned content. Its verification time is 2026-10-16T17:51:55.728844+00:00. The kernel attempt starts at 17:51:58Z and the checker attempt at 17:52:06Z, in the required order after the recorded source gate. The receipt records scientificExecutionBeforeVerification=false. These are inspected provenance records; this review did not independently repeat the network or Git verification.

The two attempt markers each declare the sole attempt and prevention of retry. The saved artifacts contain one terminal kernel stage and one terminal checker stage. This audit accepts that bounded recorded execution history and does not claim a forensic survey of activity outside the package.

The saved runner metadata identifies Node v24.19.0, V8 13.6.233.17-node.51, darwin/arm64. The checker identifies CPython 3.12.14. Supervision records executable byte pins before/after both stages, with sourceAndRuntimeRechecked=true. Loaded system libraries are explicitly not pinned; this is not a hermetic-runtime claim. No browser execution is represented by these records.

## Terminal lifecycle and resource interpretation

| Recorded supervision field | Kernel | Checker |
| --- | ---: | ---: |
| success / closed | true / true | true / true |
| scientific child / guardian exit code | 0 / 0 | 0 / 0 |
| samples | 7 | 5 |
| peak sampled group RSS, bytes | 72,744,960 | 54,657,024 |
| maximum recorded sample gap, seconds | 0.08820133283734322 | 0.08270216640084982 |
| supervised wall seconds | 0.7840024176985025 | 0.6027210829779506 |
| output bytes before final report | 1,405,316 | 1,417,174 |

Each stage's declared limits are 120 seconds, 1,073,741,824 sampled RSS bytes, and 16,777,216 output bytes. No termination reason is recorded. Each supervision report records scientificChildAbsentBeforeRelease=true and childGroupAbsent=true. The separate guardian JSONL files record one scientific-child start and one exit with exitCode=0; the recorded guardian identity agrees with its supervision group identity. Both published stderr logs are empty and hash correctly.

The final supervision reports are present and are 2,691 and 2,737 bytes, within the separate 64 KiB final-report bound. The protocol explicitly ends supervised wall accounting immediately before that bounded final write. The reported output sizes are per-stage retained-directory accounting, not additive independent payload measurements.

These records support closed successful stages under the declared sampled supervision. They do not supply continuous peak memory, a throughput benchmark, or a hostile-process containment proof. Sampled group RSS may miss a transient peak and may count shared resident pages more than once. The saved closure reports expose aggregate absence booleans; this audit did not reconstruct distinct process snapshots or independently observe the process lifecycle. The protocol's retained-guardian mechanism and two post-exit absence checks remain frozen-supervisor obligations, not fresh observations made here.

## Relation to the arithmetic proof and broader goal

ADOPTED-ARITHMETIC.md correctly retains the fixed-lattice inclusion argument, checked integer square roots, the conservative 226-iteration source-level termination bound, and exact-BigInt premises. It also retains the reviewed limitations on encode inputs, named exceptions, and bounded conversion intermediates. Its pre-execution language describes the time of adoption; it is not a claim that the later recorded execution did not occur.

The finite qualification adds empirical support for the frozen cases on the recorded runtimes. It does not prove general inclusion from coverage alone. General inclusion rests on the previously reviewed algorithmic argument under its stated semantics and validated-input assumptions. No observed iteration maximum or BigInt production cost follows from this audit.

The result provides a primitive arithmetic foundation. It supplies no complete preparation/constant adapter, guarded geometric coefficient certificate, hierarchy, candidate solve, complete row/load enclosure, matched F/H/B comparison, 5,000-drone browser result, native-program equivalence, live coupled flight, physical validation, or novelty evidence. Tight primitive endpoints also do not imply tight downstream bounds after dependent computations. Correct refusal can still prevent later operational qualification.

Public-safe claim: the frozen fixed-lattice primitive suite completed its sole kernel/checker allocation, with all 1,488 saved expected outcomes accepted and all six declared fault probes rejected, while its retained stage reports show successful closure. Describe the result as finite primitive qualification plus a separately reviewed conditional arithmetic argument. Full research completion and any later executable integration remain separate gates.

## Exact postrun reading and hash inventory

The table below uses paths relative to research/m31-interval-primitives-2026-10-16. Full means content read in full; selected means only recorded metadata/array length and the seven rows named above were inspected; hash-only means bytes were read solely for length and SHA-256 verification. No package code was executed. The source/output pin verification performed 30 matching checks: 23 manifest entries and seven supervision output/journal/log entries. Additional metadata files were also hashed as shown.

| Relative path | Access | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| ADOPTED-ARITHMETIC.md | full | 2897 | 08a484a141604555bec2f01d747ea02245a529da4f92bb00eceeefe8d71fabed |
| ARITHMETIC-ARGUMENT-DRAFT.md | hash-only | 3364 | 12363b18045043f5d550850a1f9d329f698ff96b0a71914d08ea4c0e77b4aecb |
| PARENT-READING.json | hash-only | 622 | ea47b2fa7196b32e371b28b781d3953f1e4c95a123025eed85a8d601ac080601 |
| PREFREEZE-CHANGES.md | hash-only | 3054 | fda1e37191a920a910230786deb0e08bbb6733f09d93f7c6dd8df903525f5f27 |
| PROTOCOL-DRAFT.md | hash-only | 6226 | 15f86c9e11f7b69386b073219946539cbd66c59fe92b10b25936fdb53150a891 |
| PROTOCOL.md | full | 9660 | c3b5faca9f9332277c2a8b8b4421f62f8c7f2496da430adfe7fc7debd950430e |
| SOURCE-DECISION.md | hash-only | 1737 | 516bd164596498c9d28155ae3971aa2f58bfc5e7f6f9375eb3c7835d6d847b4e |
| SOURCE-PRIVACY.md | hash-only | 1759 | d9fb5aa074302bdbd5dcdf5a0edd890ea9f590f35a3b0a2d31a0df4faeac8cd5 |
| prefreeze/initial-source/result-contract.json | hash-only | 2445 | 0e4f9c20ecef5f950370eae6be32671cc0fdc46a1e36724732a524dcee567539 |
| prefreeze/initial-source/run.cjs | hash-only | 2500 | 4b7e8b1ccf61ee2c6f6515db5e9cce3e27612e29a00fc6fd5e1b43785cbd4557 |
| prefreeze/initial-source/spec.json | hash-only | 1967 | d8065903820d08a730489abea8d92d1bad735770818e9e6717ca5ff6ab6fb2e4 |
| prefreeze/supervisor-v1/supervise.py | hash-only | 6382 | abde85e9336d5460d7ed49fa8e0d79fe34bd0ad577a5bbea584e322f0655a8f0 |
| results/checker-attempt.json | full | 279 | 16c6523464b5a03cce96a936e572a88ca0c81e1920e1b34ee51d5ca76e5f962f |
| results/checker-guardian.jsonl | full | 111 | 4ca890c0bca1b4edd6a0a685b145ed418d01ee3dd1b38358b5998191723fbd9f |
| results/checker-stderr.log | hash-only | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| results/checker-stdout.log | hash-only | 68 | de2c0cb1ec351023376b9ef1f4a6d2e49c8e6b561d54b3e06357a249d113d4cf |
| results/checker-supervision.json | full | 2737 | 219351822bbe45566708ddb9351b718845f72a040c7afbb979688c84e1b7ff30 |
| results/independent-check.json | full | 8695 | 4b4111472f257f84c5139c7152b0dcd26e379fa3873557ba2d7009dd5c9cc5f3 |
| results/kernel-attempt.json | full | 278 | 8a532f7f35e93e5c8488ecdeabe58f00549bbaf9d21a1e353086f60fba242b2f |
| results/kernel-guardian.jsonl | full | 111 | 884ff021cd59b417e00dedcf47dd1d9ba2dd8b2405847f42fe9f0f4346652004 |
| results/kernel-stderr.log | hash-only | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| results/kernel-stdout.log | hash-only | 54 | 338c1ca460f46e231c42728fe815d0bd1e13b46d8ea20ce2e3ba21f09684bf63 |
| results/kernel-supervision.json | full | 2691 | dcdeacfeac28f78e3434b995d74e427efb2bebdf3be69b7039687cbe4c3e71d0 |
| results/primitive-results.json | selected | 812099 | 934030da979dc7808f26bfbcbb02c09a858ecc1c9a753df1f8a1c63c4a3bbfeb |
| results/primitive-results.json.jsonl | hash-only | 592720 | 30a59f8d43419bcd55c422056d4da818130166486c14777e4863d556162f01e5 |
| review/INDEPENDENT-CHECKER.md | hash-only | 8543 | c036efb8a27c1b0d1c5b1c4156413c5157047b994e440e93d0b4aba3a8ebc93d |
| review/MATHEMATICS.md | hash-only | 13991 | d7326aae9b3cbdea1bc251b3e5be4e668b3283b9e0fd67ca1cc42cfb2d26b425 |
| review/PROTOCOL-AND-SUPERVISION.md | hash-only | 25760 | a132b7a238baf6620e05f70f5887b9af9e40d069323a38ee76b2fc13aba29620 |
| runtime-pins.json | hash-only | 404 | 34dd9c5333c8fa945bd0667be7d042fc1eb09899895d942bf83b671c0b1a5b81 |
| source-manifest.json | full | 5266 | fb3585e2eb5340a456fac47ec35957be9a5fcdc1e44425990475c9e3de3858dd |
| source-publication.json | full | 830 | 44f0016f575980f34ce32baa1a1d8a441af52e86297ad94b8687d844db0beb15 |
| source/check.py | hash-only | 30506 | 99e79de9747063825d3a6c8c0d2f8dc1e5fba6af8739204fa9b322184d96703c |
| source/guardian.py | hash-only | 1656 | a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf |
| source/interval.cjs | hash-only | 2815 | 73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3 |
| source/result-contract.json | hash-only | 2863 | a41c1a936b3b4772e90de182abffd7b41dc552a0f217a15738015f5359a3d522 |
| source/run.cjs | hash-only | 3054 | 172dd45d3f1fe06f3562e3908d16e3d4d759f0c5e1f769f4f9d46860f09fcd0b |
| source/spec.json | hash-only | 2550 | 73d539b2f6575e21b3f8c512ce79a4be22ff0b09c98c527cb18dfc06a6dc21f7 |
| source/supervise.py | hash-only | 11202 | bcba663a3391e7cfc0ebd2f0891c5ac6f23fe3cbbf1c626e4f4b7e5842c1c4fa |

Inventory totals: 38 unique artifacts; 11 full content reads, 1 selected saved-result inspection, and 26 hash-only artifacts. No inherited content reads in this postrun review.
