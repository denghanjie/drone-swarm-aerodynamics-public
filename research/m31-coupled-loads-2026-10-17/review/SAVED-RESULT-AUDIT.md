# Saved coupled-load result audit

**ACCEPT the saved evidence as internally consistent. All 61 administrative checks passed.** The recorded result is **11 certified load solutions passing all four declared tolerances, six verified rejection outcomes, and two unqualified stress scenes**. `verificationPassed=true` and `tolerancePassed=true` coexist with **`fullQualification=false`**. The 17 qualified ordinary outcomes include the six rejections; they are not 17 load solutions.

This audit parsed saved artifacts, reconciled identities/order/counters, compared recorded error maxima and tolerance decisions, and checked hashes against local Git objects. It did not import or execute scientific modules, regenerate geometry or roots, recompute the oracle/certificates, repeat a control, retrieve external material, or edit frozen files. No inherited semantic read was added; the cycle remains at 9 of 16 inherited files. Manifest paths outside the new package were hashed only.

## Source and evidence identity

The source commit is `0e184452f0ccc5fbe02c8c5491ee849259b74a26`, with parent `f84f365f268a805de4e2bd432e68ce33d87d129b`. The 11,725-byte manifest has SHA-256 `7995d9a9c8625031654f63bbf96f2ec83ea9496be5d273b388f349eed6d80593` and Git blob `8dabd05b901a9d8117b472224db9609446225773`.

I checked the manifest's own identities and all **56 source pins** against both current files and the local exact-commit objects. Every comparison matched. The checker's 56-source list and the candidate's eight source hashes agree with that manifest. All 25 emitted constant encodings equal the saved checker's expected encodings. This is saved-byte agreement; their scientific correctness was not recomputed here.

The preserved publication record states that the separate exact-commit HTTPS manifest verification completed at `2026-10-16T18:38:25.676308+00:00`, after source freeze and before either attempt. Kernel and checker attempt timestamps are respectively `18:38:39Z` and `18:38:53Z`. I verified these saved identities and timestamp ordering; I did not repeat the remote retrieval.

| Main saved artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/coupled-results.json` | 2,238,747 | `7b39795554646fd9a917153cddcee3bd91a94f39524f7b29920a19885febc1dd` |
| `results/coupled-results.json.jsonl` | 1,007,669 | `0f3234cdb536c635b9da8e35f21621a0e868e64ab33dd428c4713b2aecb30538` |
| `results/independent-check.json` | 426,483 | `31a87e09d88762a80533485303fbf286b7769a30a1d6e5f1fd73a96add4844a9` |

`SAVED-RESULT-PINS.json` records all evidence identities, the 56 source comparisons, 61 checks, per-scene summaries, controls, and supervision observations.

## Coverage and outcomes

All nineteen scene IDs are unique and match the specification and checker order. The journal has a matching header, nineteen structurally identical scene records, and a matching completion footer: 21 lines. For every globally prepared scene, the saved stable-ID/rotor pair list is complete, unique, and in the declared input order.

| Saved scene outcome | Count |
| --- | ---: |
| Certified; tolerance achieved | 11 |
| Rejected; rejection verified | 6 |
| Unresolved; unqualified | 2 |

The six rejections are `near-rejection`, `invalid-isolated`, `invalid-global-pair`, `scaled-cap`, `center-range`, and `upward-order`. Their saved candidate and reference branches agree. Ordering is an operational-domain rejection, not evidence of a failed general contraction theorem.

There are **2,632 planned and 2,624 observed pairs**. The difference is exactly the eight planned pairs of `invalid-global-pair`, whose saved preparation fails and whose explicit stop reason is `global-preparation`. `invalid-isolated` has the same stop reason but zero planned pairs. Other scenes retain all pairs, including refused scenes.

The observed pair statuses reconcile to **1,001 positive + 1,602 zero + 16 rejected + 5 unresolved = 2,624**. The 1,001 positives count all scenes; 994 belong to certified scenes. The eleven load certificates contain 276 rotor rows with the required ownership/order. Saved per-load error upper values, scene maxima, checker maxima, and exact integer tolerance decisions agree. This compares stored bounds; it does not recompute their scientific validity or treat them as measured physical errors.

The baseline checker records zero errors. All ordinary expected classes agree with the recorded reference. The two stress differences remain explicit:

| Scene | Candidate | Recorded reference | Qualification |
| --- | --- | --- | --- |
| `tiny-force` | `unresolved / pair-normalizer` | `reference-undecidable / pair-normalizer` | Unqualified |
| `huge-force` | `unresolved / pair-unresolved-range` | `rejected / pair-cap` | Unqualified |

The five unresolved pair identities exactly match the frozen allowlist: tiny-force receiver 0/rotor 0/source 1, and huge-force receiver 0/source 1/rotors 0–3. Both stress records correctly retain `expectedClassAgrees=false` against the independent reference class. A permitted refusal is not a candidate cap proof, and no causal diagnosis of the internal arithmetic failure is inferred from its code.

## Controls and closure

All nine frozen controls are recorded as executed and rejected, with consistent nonempty error lists: missing positive pair, false unit root, altered candidate, false zero error, altered lever arm, altered stable ID, missing scene, duplicate scene, and reordered scenes. The saved root and nonzero-error controls include the independent witness records. This audit checked their names, presence, dispositions, and error counts; it did not rerun their mutations or recompute their witness proofs.

Both stages record success, closure, child and guardian exit codes zero, no termination reason, scientific-child absence before guardian release, final group absence, and unchanged source/runtime checks. Each guardian log has one child start and its matching successful exit. Both stderr logs are empty; stdout summaries agree with the artifacts. Published log hashes and recorded raw-log hashes agree with the saved bytes. Runtime-pin fields match the frozen runtime metadata; runtime executables and private raw-log retention were not freshly inspected.

| Recorded supervision | Kernel | Checker |
| --- | ---: | ---: |
| Wall seconds | 1.8293305421248078 | 2.0215101670473814 |
| Peak sampled group RSS, bytes | 92,422,144 | 101,171,200 |
| Samples | 22 | 26 |
| Maximum sample gap, seconds | 0.12690025009214878 | 0.08373850025236607 |
| Aggregate output bytes before report | 3,246,947 | 3,676,499 |

The output counters reconstruct exactly from saved artifact sizes and the recorded current-stage raw-log sizes. Both final supervision reports fit the 64 KiB reserve. Recorded wall time, sampled RSS, and aggregate output are below the frozen 180-second, 1-GiB sampled-RSS, and 32-MiB limits. These are supervision records, not throughput evidence, hard instantaneous memory bounds, or a newly reconstructed process history.

No saved-evidence inconsistency blocks publication of this finite result with its limits. It establishes recorded qualification of eleven static small-group M-current load solutions and correct refusal accounting for the remaining cases. It does not establish physical accuracy, dynamics, browser scientific execution, 5,000-drone scale, comparative total cost, or novelty. The two stress scenes remain unqualified, and full-suite qualification was not achieved.
