# Current-pair saved-result audit

Disposition: **ACCEPT the saved evidence as internally consistent with the frozen source and the recorded finite-pair checker outcome.** This is a saved-evidence audit, not a new scientific execution or an independent recomputation of the oracle. The supported result is `verificationPassed=true`, with **320 ordinary records qualified and two stress records unqualified**. `fullQualification=false` must remain visible in every summary.

No source-frozen file was changed. No candidate or checker was imported or executed, no reference geometry or coefficient was recomputed, no scientific fixture was generated, and no external lookup or remote verification was repeated. The only authored files are this report and `review/SAVED-RESULT-PINS.json`.

## Method and bounded reading

I parsed the 13 core result files: the candidate output, its journal, the independent-check report, and each stage's attempt, supervision, guardian, stdout, and stderr files. I also read the package's source-publication record, source manifest, case-ID/specification metadata, result contract, and runtime-pin metadata. There were no inherited semantic reads. All 37 source-manifest paths were hashed and compared with local Git objects; their scientific source was not executed or semantically re-reviewed here.

A fourteenth result path, `results/fresh-closure-check.json`, appeared while package administration continued. I recorded only its path, length, and hash; I did not inspect or endorse its conclusion. An initial audit-only assumption that the directory would contain exactly 13 result files was replaced with the relevant check that all 13 required core files exist. An additional administrative file is not evidence of a scientific retry.

The companion JSON records 50 passing administrative checks, every evidence pin, all 37 source-byte comparisons, the two stress dispositions, the fault-control records, and the recorded supervision measurements. These checks are byte identity, JSON/data consistency, count reconciliation, and local source-chain checks. They do not reproduce the scientific validator.

## Frozen-source and publication chain

The source commit is `6ed4471c2dc7e920a1a63d16eafb6bdb9616a9da`, whose local Git parent agrees with the manifest's `b92f361888ca8bb1f9030f374a33de69dd78661a`.

The 7,813-byte source manifest has SHA-256 `0c060673654bbda87fc3be69c442d0bad2d48f7b2005f415a0128000048ce012` and Git blob `0616cee08033b07b7499c8df60fb6d737d3bed7b`. I independently checked both identities, equality with the local exact-commit manifest blob, and every one of the 37 file pins against both current bytes and exact-commit bytes. All agree. The checker report's 37 `verifiedSources` entries agree exactly with the frozen manifest; the candidate's seven emitted source pins agree with the corresponding manifest entries.

The preserved publication record states that a separate exact-commit HTTPS download matched the local manifest, with certificate verification enabled, at `2026-10-16T18:14:05.265986+00:00`. The kernel attempt is timestamped `18:14:07Z` and the checker attempt `18:14:14Z`, both after that recorded verification. This audit confirms internal source identity and timestamp ordering; **the remote download and its timing remain recorded provenance, not a newly repeated network observation**. The attempt records and both supervision reports bind the same source commit and manifest hash.

The package's runtime-pin metadata agrees exactly with both supervision reports. I did not hash the runtime executables afresh. Their execution identity and the `sourceAndRuntimeRechecked=true` assertions remain recorded supervision evidence.

## Saved records and qualification

All 322 candidate record IDs are unique and appear in exactly the frozen specification's order. The check report has the same 322 IDs, with candidate status and branch labels matching every saved candidate record. The JSONL journal has a matching header, 322 record entries structurally identical to the candidate records, and one matching completion footer: 324 lines in total. The journal's saved hash, byte count, and row count agree with both supervision and checker metadata.

| Saved classification | Candidate records | Recorded reference records |
| --- | ---: | ---: |
| Positive | 92 | 92 |
| Zero | 189 | 189 |
| Rejected | 39 | 40 |
| Unresolved | 2 | 0 |
| Reference-undecidable | 0 | 1 |
| Total | 322 | 322 |

I independently counted these labels from the saved per-case data; they agree with the aggregate fields. All 320 ordinary records have matching candidate/reference status and branch labels, `verified=true`, and `qualified=true`. This includes correctly classified rejection records; “qualified” does not mean that all 320 cases are admitted positive physical interactions.

All 25 candidate constant encodings exactly equal the saved checker's `expectedConstantEncodings`. That is an independently checked comparison between saved artifacts. Correct rounding, raw-input regeneration, preparation semantics, branch correctness, and interval enclosure remain the recorded checker conclusions supported by the separately reviewed source; they were not recomputed here.

The baseline report contains zero errors and records `baselineVerificationPassed=true`. Its overall `passed=true` and `verificationPassed=true` agree with 320 qualified ordinary cases, the two prospectively allowed stress refusals, and the seven successful negative controls. These fields do **not** supersede `fullQualification=false`.

| Stress ID | Candidate result | Recorded reference result | Qualification |
| --- | --- | --- | --- |
| `tiny-force` | `unresolved / normalizer` | `reference-undecidable / normalizer` | Unqualified |
| `huge-force` | `unresolved / unresolved-range` | `rejected / cap` | Unqualified |

These are exactly the two IDs and refusal codes permitted by the frozen `allowedStressUnresolved` map. Both are marked `unqualifiedReason=declared-stress-refusal`. The tiny-force report stores a normalizer enclosure whose lower endpoint is zero; the fixed reference therefore does not establish the required positive lower bound. This does not assert that the exact physical normalizer is zero. The huge-force report records a reference cap rejection while the candidate refuses on arithmetic range. That permitted refusal remains unqualified: it cannot be counted as a candidate cap proof or converted into a resolved rejection.

The recorded coefficient-width diagnostics are descriptive and introduce no bound-width qualification. Neither `verified=true` on a permitted stress refusal nor an ordinary rejection label should be described as a universally valid coefficient certificate.

## Recorded negative controls

All seven names match the frozen contract, with `executed=true`, `rejected=true`, nonempty errors, and error counts equal to the saved error-list lengths:

| Control | Saved errors | Principal recorded rejection |
| --- | ---: | --- |
| `unsound-positive-interval` | 2 | Coefficient reference containment, row 112 |
| `wrong-branch` | 2 | Target branch precedence, row 300 |
| `altered-prepared` | 2 | Prepared operation graph, row 112 |
| `missing-case` | 2 | Record count |
| `duplicate-case` | 4 | Duplicate ID, order, and raw input, row 1 |
| `reordered-cases` | 5 | Order and raw input, rows 0 and 1 |
| `altered-input` | 2 | Raw input regeneration, row 0 |

Each also records an ordinary-qualification-count failure. These are preserved observations from the sole checker run, not controls rerun by this audit. They establish the recorded response to these seven mutations, not exhaustiveness against every possible defect.

## Supervision and saved output integrity

Both attempt records declare the sole attempt. Each guardian log records exactly one scientific child start and one matching child exit with code zero. Guardian identifiers match the supervision process-group identifiers. Both supervision reports record `success=true`, `closed=true`, child and guardian exit codes zero, no termination reason, scientific-child absence before guardian release, and final child-group absence. The kernel and checker stdout summaries match their saved artifacts; both stderr files are empty.

| Recorded measurement | Kernel | Checker |
| --- | ---: | ---: |
| Wall seconds | 0.554337834008038 | 0.5339858755469322 |
| Peak sampled group RSS, bytes | 93,175,808 | 65,224,704 |
| Samples | 6 | 6 |
| Maximum sample gap, seconds | 0.08065016660839319 | 0.06921562552452087 |
| Output bytes before report | 2,287,078 | 2,767,106 |

The recorded limits agree with the frozen allocation: one kernel attempt and one checker attempt, each at most 120 seconds, sampled RSS at most 1,073,741,824 bytes, and output at most 16,777,216 bytes. The saved measurements are below those limits. These are recorded supervision measurements, not a benchmark, an independently reconstructed process history, or a hard instantaneous memory bound. The supervision reports expressly limit containment to reviewed children that spawn no subprocesses; they do not claim hostile-code or escaped-descendant isolation.

Every published log's size and hash agree with the corresponding supervision pin. The recorded raw and published digests are identical for all four logs. The candidate, journal, and checker output hashes likewise agree with their recorded pins. Private raw-log retention was not independently inspected.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `source-publication.json` | 818 | `2c436c56b6fcdd5a7cb293fb82ba314e89af57f9c29bcd71d2d0c860e11d320b` |
| `results/pair-results.json` | 1,511,774 | `c04f48318992dcf7cb6ffed9eefc6bc3aef93fb2025b7c916208ccfe53883675` |
| `results/pair-results.json.jsonl` | 774,883 | `32a55372b14fdbb64c8d6d983fa92ba49ec7d7fe7868e202f77e08cbdd643453` |
| `results/independent-check.json` | 476,965 | `688826dab19c5ae790dd6cae7e70db4a1a7030f2517a24c75b9f65edd45247c9` |

## Publication boundary

No saved-evidence inconsistency blocks reporting the finite result with its limitations. A defensible statement is: **the single saved kernel run produced 322 records; the single saved independent checker run verified the prescribed finite protocol, qualified all 320 ordinary records, retained two unqualified stress refusals, and rejected all seven declared fault probes.** This audit additionally confirms the saved-file identities, journal equality, count reconciliation, and unchanged exact-commit source chain.

This does not establish complete receiver rows, aggregated loads, hierarchy bounds, a load certificate, browser qualification, a 5,000-drone run, general-domain correctness, physical fidelity, or novelty. The two stress records remain unresolved by the candidate, and full finite qualification was not achieved. No new execution or retry is authorized or proposed by this review.
