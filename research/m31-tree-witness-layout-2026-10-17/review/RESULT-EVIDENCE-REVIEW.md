# Saved-layout result evidence review

Reviewed 2026-10-17 after the single supervised saved-data attempt. **Disposition: the retained evidence supports the registered saved-tree layout qualification and both development-data size targets.** The candidate and independent checker completed successfully, all 156 selected records are represented in their original order, and the two retained N=5000 H tree streams are approximately 22.07% of their original sizes. This is a representation result. `scientificValidated` remains false throughout the check report.

This review used standard-library JSON metadata reads, file inventories, SHA-256 rehashing and arithmetic over saved descriptor/report fields. It did not import or execute any project module, rerun a codec/checker, launch a browser, perform a native query or reference calculation, or change frozen source/results or the prior package. The only file written by this review is this document. Complete logical reconstruction is evidence from the separately executed, source-frozen Python checker; the present review independently verifies its retained bindings, controls, sizes and accounting rather than claiming a second decode run.

## Attempt and publication identity

Execution source commit: `b19aadc9a4157ad7c2bcba67856baf1d0c9096c6`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `source-manifest.json` | 241,585 | `eb7d1fda53791a919d64b06590299276f91f67afbaf9d444c219ffff829b368f` |
| `source-publication.json` | 870 | `4d0b55d70cc701df1faa5084bc899a77f69fd90e1e51e045ab683ba2292866bc` |
| `input-index.json` | 53,584 | `7fb8fbe9c954a6a62db623061fd6b1296d534760fcdb45eb05b97d6759050920` |
| `input-manifest.json` | 236,647 | `37e1ad75a0c212764c7fe1f0c749cf2fc5c1278fc12150366a5417feed42d967` |
| `results/candidate.json` | 80,696 | `dd90cea8a40566d30ed3f9ea0b086dafe74a050416ce939a81cd4e02b767f161` |
| `results/check.json` | 96,758 | `0ee78af6bcf73fb28a181c9a8f8c00d43c90887c2c69ae9894f12a37d61e903c` |
| `results/run-attempt.json` | 1,891 | `3db0e7768031fb58e92a6f2474cbbf8cadba3c70583ea7b1d74f98c9f3a409f2` |
| `review/SUPERVISOR-EXIT.json` | 507 | `8b15e920802bf61f27a8c7279a2711061b29bc860dce5b5a5a415eb60e874f78` |

The execution manifest's **928 file pins**, representing 123,107,535 referenced bytes, were rehashed with no mismatch. The saved publication receipt binds this exact commit, manifest path/hash/byte count and 928 verified pins. It records committed/local and remote/local byte equality at `04:36:53.643070 UTC`, before attempt start at `04:37:06.631877 UTC`. This review checked that saved receipt and its bindings; it did not perform a new remote fetch.

Both stage report files match the byte counts and SHA-256 identities retained by the supervisor. Both reports have matching source commit/manifest, `complete:true` and `passed:true`. The terminal attempt has `status:"completed"`, no first failure, `executionRetries:0` and `preservationPassed:true`. Its immutable `supervisorExitVerified:false` correctly avoids a self-certification claim. The separate parent-authored exit receipt binds the terminal attempt and records external exec session 25320 returning exit code 0, observed at `04:38:29.170727 UTC`.

## Exact input and output closure

The input sequence was independently reconstructed from the old saved-transport index and native journal rows. It is exactly 126 saved rows followed by 30 durable browser-native rows, with consecutive combined indices 0–155 and original source sequences preserved. The 126 saved rows comprise 42 each of F, H0 and H; the 30 browser rows comprise ten each. Candidate and checker rows match every selected original descriptor pin and each other.

The input manifest is the exact **905-file closure**: three frozen anchors, 156 original full-record descriptors and 746 unique referenced shards, totaling **122,408,637 bytes**. Every selected descriptor's fields were traversed as metadata to collect all referenced shard pins, including unchanged non-tree fields. This independently reconstructed set equals the input manifest and is included in the execution manifest. No extra failed-append shard or unrelated journal row enters the selected corpus.

The prior attempt anchor remains the failed browser probe at source commit `4e1818c5b1ac7032018925edf17cecb1a6965e3d`, manifest `52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449`. Its three input-anchor hashes match the frozen protocol. The old failed result is not changed or promoted by this qualification.

All 156 report rows bind source index/origin/sequence, original descriptor, method, tree state, new descriptor or absence, and original/new tree-field stream sizes. The original and new binary size values were independently read from their retained descriptor metadata; chunk byte sums match the new streams. There are **52 absent trees, eight explicit null trees and 96 object trees**. The 52 absent trees produce no descriptor. All 104 present trees have new descriptors containing exactly the `tree` field.

The new evidence closure contains exactly **104 descriptors and 113 unique shards**, 217 files total. Every pin was rehashed successfully. The actual records/shards inventory equals the union referenced by the 104 descriptors; no unreferenced evidence file was found. The complete results tree contains these 217 files plus the candidate, checker and attempt reports, 220 files total. Unchanged native fields remain bound by the original input descriptors/shards and are not rewritten as newly validated output.

## Retained comparison and control evidence

Every checker row has `layoutQualified:true` and `scientificValidated:false`. The top-level checker also has `layoutQualified:true`, `storageTargetPassed:true`, `sourceAndInputPinsPreserved:true`, `scientificValidated:false` and an empty errors array. Saved comparison counts sum to **29,082 receivers, 547,641 culls and 65,491,939 gathered indices**. The retained corpus uses 15,272 run encodings and 13,810 bitmap encodings. Literal encoding is exercised by fixed controls rather than occurring among these retained gathered encodings.

These counts describe the saved checker's complete comparisons; they do not turn reconstruction into a scientific omission proof or certify the correctness of the old witnesses. The comparison contract preserves all logical base fields, scalar types and literal words, plus receiver/cull/gather/dictionary/node array order. Object property enumeration order is explicitly outside that equivalence contract. The pure binary reader is reused from the pinned old implementation; the layout reconstruction/comparison is independently authored Python rather than a second independent implementation of the entire transport grammar.

The eight saved candidate controls match the frozen exact order and all have `passed:true`: `literal-selection`, `run-selection`, `bitmap-boundary-roundtrip`, `empty-roundtrip`, `duplicate-source-rejected`, `bitmap-tail-rejected`, `wrong-count-rejected`, `noncanonical-choice-rejected`.

The independent control list matches the frozen identities, order, statuses and exact rejection reasons. Its positive `fixed-three-encodings-and-literal-zero` result is `preserved`; the following sixteen mutations are `rejected`:

| Mutation | Saved exact rejection reason |
| --- | --- |
| `noncanonical-choice` | `layout-gather-canonical-cost` |
| `padding` | `layout-bitmap-padding` |
| `offset-end` | `layout-offset-endpoints` |
| `offset-order` | `layout-offset-order` |
| `cull-code` | `layout-cull-equality` |
| `difference-word` | `layout-cull-equality` |
| `receiver-order` | `layout-receiver-order` |
| `gather-order` | `layout-index-order` |
| `gather-count` | `layout-gather-cardinality` |
| `leaf-reference` | `layout-leaf-reference` |
| `unknown-field` | `layout-fields` |
| `base-literal-word` | `layout-base-equality` |
| `cull-order` | `layout-cull-order` |
| `run-overlap` | `layout-run-order` |
| `bitmap-width` | `layout-bitmap-width` |
| `boolean-id` | `layout-receiver-range` |

These are fixed representation fixtures and corruptions, not fresh swarm states, scientific queries or held-out samples. This review matched the saved evidence against the complete lists and reasons, rather than accepting a reported control count alone.

## Both registered N=5000 H targets

The candidate and checker target lists agree exactly and contain only original journal sequences **60 and 63**, at combined indices **152 and 154**, in that order. They bind the two retained H trees at N=5000, not a selected pair chosen after measuring compression.

| Combined index / journal sequence | Original tree bytes | New tree bytes | New/original | Reduction | `old - 2*new` |
| --- | ---: | ---: | ---: | ---: | ---: |
| 152 / 60 | 43,030,681 | 9,498,259 | 22.073225% | 77.926775% | 24,034,163 |
| 154 / 63 | 43,040,079 | 9,499,571 | 22.071453% | 77.928547% | 24,040,937 |

Both integer margins are positive, independently confirming `2*newTreeBinaryBytes <= originalTreeBinaryBytes`. Each target has 5,000 receiver rows using bitmap gathered encodings; the saved checker reports 244,426 / 244,539 culls and 4,465,669 / 4,465,576 gathered indices respectively.

Sequence 60 binds original `0060-native.json` (18,030 bytes, SHA-256 `2de86534c7a94a61d59cdd1d00d0997c556c6cce25ea422e3b051521a35286d8`) to new `152-tree.json` (2,547 bytes, SHA-256 `a5ec6ca4fa9ae7d3bc7a307d10942a2843b6a1b5178cb74809c6e2b27001be4c`). Sequence 63 binds original `0063-native.json` (18,029 bytes, SHA-256 `5df442eb0730ed58e4ffa4b6d9e849b6308c35338ec7c16a69b06e2078f550a1`) to new `154-tree.json` (2,547 bytes, SHA-256 `90db9f51cc4e77cf510c34fe0ef255411151a3fc20daf1056a8f687eb794cd73`). Full package-relative paths remain in the pinned index/check report.

Across all 156 rows, logical tree streams total **101,342,629 original bytes versus 23,162,035 new bytes**, a ratio of **22.855175%** and reduction of **77.144825%**. This aggregate is not a per-record guarantee: 68 rows shrink, 28 grow and 60 are equal (the 52 absent and eight null cases). The frozen half-size gate applies specifically to the two N=5000 H trees.

## Physical accounting and execution limits

Logical stream totals include repeated references; physical shard totals count each retained file once. The candidate's saved `deduplicatedBytes` is **2,488**, exactly the difference between the new logical tree-stream total 23,162,035 and the unique shard total 23,159,547. Candidate `newBytes` is **23,209,967**, equal to unique shards plus descriptors. Its value is recorded before adding the candidate report itself, and should not be read as the complete results-directory size.

| Retained execution allocation | Observed bytes | Fixed limit |
| --- | ---: | ---: |
| 113 unique new shards | 23,159,547 | Included in evidence partition |
| 104 new descriptors | 50,420 | Included in evidence partition |
| Evidence subtotal | **23,209,967** | **58,720,256 (56 MiB)** |
| Candidate + checker reports | **177,454** | **2,097,152 (2 MiB) other public** |
| Private tree | **0** | **4,194,304 (4 MiB)** |
| Terminal attempt report | **1,891** | **2,097,152 (2 MiB) finalization allocation** |
| Final results + private total | **23,389,312** | **67,108,864 (64 MiB)** |

The private tree was independently inventoried: exactly `candidate.log` and `check.log`, both zero bytes, both with the empty-file SHA-256 recorded by the supervisor. No symlink or additional private file was found. The largest retained result file is 1,048,576 bytes, within the 1 MiB shard and 32 MiB general file caps. The largest descriptor is 2,547 bytes; both index/report files are below their 2 MiB cap. Evidence has 35,510,289 bytes of partition headroom. Final retained results/private bytes leave 43,719,552 bytes below 64 MiB, and adding the conservative 2 MiB closure reserve still remains below that bound.

The supervisor's `outputLogScratchBytes:23388759` is a **pre-final-report** measurement. The independently counted terminal total is 553 bytes larger. The fixed source measures usage before adding terminal ledger fields and rewriting `run-attempt.json`; the final ledger is 1,891 bytes versus the 1,338 bytes implied at that measurement point. With the private tree confirmed empty and all other retained files independently reconciled, this difference is consistent with the documented final-ledger growth, not missing evidence. The frozen ledger was not rewritten to hide the timestamp distinction.

These physical totals cover the supervised execution's results directory and private tree at review time. Read-only old inputs are excluded as registered. Source packaging and later viewer/review artifacts are outside this execution-output measurement; it is not a total for all repository or post-execution files.

| Time evidence | Observed | Fixed limit / interpretation |
| --- | ---: | --- |
| Candidate supervised child wall | 11.474449 s | 120 s |
| Checker supervised child wall | 28.529200 s | 120 s |
| Summed child wall | 40.003649 s | Stage total |
| Shared overhead and closure | 0.755064 s | 60 s |
| Supervisor pre-final-report elapsed | 40.758713 s | 300 s reservation |

Both stages exit 0. The terminal pre-final timestamp is `04:37:47.086700 UTC`; external exit was observed at `04:38:29.170727 UTC`, before the unchanged `05:06:20 UTC` cutoff. The later observation time is not the exact process-exit instant. Saved source checks the deadline again after writing the terminal ledger, and the external receipt records successful exit. Candidate-reported wall/persistence timings describe this saved-data encoding operation only; they provide no browser/native speed claim.

The supervisor retains `allDescendantsExitClaim:false` and `memoryLimitClaim:false`. Its recorded peak RSS of 26,951,680 bytes is scoped to the macOS supervisor process lifetime, not aggregate child memory or an enforced memory ceiling. Disk accounting is a polling monitor plus writer guards, not an atomic operating-system aggregate quota. No retry is recorded or authorized by this result.

## Permitted conclusion and remaining limits

The saved evidence supports exact lossless layout qualification of the 156 preselected tree representations, the complete fixed control suite, both registered half-size targets, and compliance with the bounded execution-output and timing envelope as recorded and externally closed. The source and old-input preservation evidence is consistent with the independently rehashed retained bytes.

This uses exposed development data. It does not establish held-out compression performance, native numerical correctness, scientific omission bounds, controller/derivative/RK accuracy, reference acceptance, browser speed, a complete fresh browser-stage result, or that a future full attempt fits the old 160 MiB evidence partition. The earlier browser attempt remains failed. A saved-only viewer must retain each original input binding and label the representation `layoutQualified:true` with `scientificValidated:false`; viewer interaction or display checks are separate from this evidence review.
