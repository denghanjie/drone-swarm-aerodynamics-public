# Operational result review: saved tree-witness layout

Reviewed 2026-10-17 after the single supervised attempt. **The saved results support successful completion of this fixed saved-data layout qualification.** Both stages exited zero; all 156 selected records and fixed controls passed in the recorded independent checker; both predeclared tree-size targets passed; the measured runtime evidence stayed below the fixed time and byte ceilings. The external supervisor-exit receipt records exit zero. The prior browser experiment remains failed.

This review used source/JSON/descriptor reads, exact file hashes, filesystem byte accounting and private-log metadata only. It did not import or execute a codec, candidate, checker, supervisor, browser, reference or numerical producer, and did not retry any stage. The only file written by this review is this document. Reconstruction findings below are the independently authored checker's saved results, checked against its reviewed source and bound artifacts; this review did not rerun reconstruction.

## Source, authorization and input bindings

The execution manifest is SHA-256 `eb7d1fda53791a919d64b06590299276f91f67afbaf9d444c219ffff829b368f`, 241,585 bytes, at source commit `b19aadc9a4157ad7c2bcba67856baf1d0c9096c6`. The publication receipt binds that exact manifest size/hash, commit, 928 verified file pins, and committed/remote byte equality. Its verification timestamp, `04:36:53.643070 UTC`, precedes the attempt marker by 12.988807 seconds. This review checked the local receipt and manifest bindings; it did not perform a new network or Git verification.

All **928 execution-manifest files**, totaling 123,107,535 bytes, were rehashed during this review with no size/hash/path mismatch. The enabled configuration's reviewed-draft hash matches `reviewed-source-manifest.json` (`032e2e35911bcd2763aab84ab38c8a8ccd99b5eb67a1931da55b0fb0cb66ea01`). Compared with that reviewed manifest, the execution manifest adds only the enabled `config.json` and `reviewed-source-manifest.json`; no existing pinned file is removed or changed. The checker and supervisor remain the exact versions identified in `review/CROSS-REVIEW.md`.

The input index is 53,584 bytes, SHA-256 `7fb8fbe9c954a6a62db623061fd6b1296d534760fcdb45eb05b97d6759050920`. Direct metadata comparison confirms its order is exactly the 126 saved-transport rows followed by the 30 durable `native` journal rows. All candidate and checker rows match their source index, origin, original sequence and source descriptor pin. Their method, tree-presence state, original/new byte counts and output descriptor pins also agree, with no row mismatch.

Tree presence is reported across all 156 records as **52 absent, 8 explicit null, and 96 objects**. The 104 present trees correspond to 104 new descriptors. Every candidate row records its logical roundtrip, and every checker row records `layoutQualified:true` and `scientificValidated:false`. The independent checker's own source—not a producer equality flag—defines the reconstruction and exact type/word/sequence comparison.

All old source/input pins selected by this experiment still match. The original browser attempt report still says `failed`, and its evidence partition remains 167,411,867 bytes, matching the prior failure accounting. This review made no write to that package and does not reclassify any unreferenced shard or incomplete query as a complete result.

## Completion, timing and exit evidence

The attempt marker is `2026-10-17T04:37:06.631877+00:00`; 1,753.368123 seconds remained before the fixed `05:06:20 UTC` cutoff, exceeding the required full 300-second reservation. Reviewed supervisor source checks that full reservation before output creation and keeps setup within its unextended monotonic total deadline.

| Allocation | Saved observed duration | Fixed ceiling |
| --- | ---: | ---: |
| Candidate direct child | 11.474448835 s | 120 s |
| Independent checker direct child | 28.529199792 s | 120 s |
| Child durations combined | 40.003648627 s | 240 s allocated |
| Setup/closure overhead at pre-final timestamp | 0.755064456 s | 60 s |
| Supervisor pre-final-report duration | 40.758713000 s | 300 s total |

Both stage entries are `completed`, have `exitCode:0`, and pin the exact current candidate/check report bytes. The attempt has `status:completed`, `firstFailure:null`, `executionRetries:0`, and `preservationPassed:true`. Candidate and checker separately record input/source preservation. The final report timestamp is `04:37:47.086700 UTC`.

The pre-final duration does not include the later final-ledger write or interpreter exit. `review/SUPERVISOR-EXIT.json` records the parent's external observation of terminal `exit_code:0` from exec session **25320**, observed at `04:38:29.170727 UTC`, and binds the exact final attempt report. This supplies the external exit evidence that the self-ledger deliberately does not claim: its `supervisorExitVerified` remains false. The observed closure is well before the absolute cutoff. No supervisor-process RSS value is interpreted as total memory or a memory limit, and no additional descendant-termination guarantee is inferred.

## Byte ceilings and complete output inventory

This review enumerated all evidence files and checked their descriptor pins, lengths and hashes. The output reference union equals the physical evidence-file set exactly: **217 files**, comprising 113 shards and 104 descriptors. There are no unreferenced evidence files, missing referenced files, hash mismatches or result symlinks.

| Runtime output partition at review | Bytes | Fixed ceiling |
| --- | ---: | ---: |
| 113 unique shard files | 23,159,547 | Included in evidence |
| 104 record descriptors | 50,420 | Included in evidence |
| **Evidence subtotal** | **23,209,967** | **58,720,256 (56 MiB)** |
| Candidate plus checker public reports | 177,454 | 2,097,152 (2 MiB) |
| Final attempt ledger | 1,891 | 2,097,152 finalization allowance |
| Private directory files | 0 | 4,194,304 (4 MiB) |
| **Current public results plus private files** | **23,389,312** | **67,108,864 (64 MiB)** |
| Current total plus reserved 2 MiB closure space | 25,486,464 | 67,108,864 |

The private directory was read-only inspected at the parent's supplied location. It contains exactly two ordinary nonsymlink files, `candidate.log` and `check.log`, both zero bytes; their hashes match the ledger's empty-log hash. No private path is published here.

The largest result file is 1,048,576 bytes, equal to the shard limit and below the 32 MiB per-file limit. The largest descriptor is 2,547 bytes. Candidate/check report sizes are 80,696 and 96,758 bytes, respectively, below the 2 MiB index/report ceiling.

The attempt's `outputLogScratchBytes` is 23,388,759 bytes at its pre-final-report accounting point. The current total is 553 bytes larger after the final ledger replacement. This timestamp difference is not a cap discrepancy: the final total remains far below every applicable ceiling and the closure reserve. The runtime budget excludes unchanged read-only old inputs; it does not establish that copying those inputs or adding omitted future browser-stage evidence would fit.

The logical sum of new tree streams is 23,162,035 bytes. Actual unique shard bytes are 2,488 bytes lower, matching the candidate's recorded exact-byte deduplication count. Adding 50,420 descriptor bytes yields the independently observed 23,209,967-byte physical evidence subtotal. Logical size and physical storage therefore reconcile without treating deduplication as free or ignoring descriptors.

## Fixed controls and size targets

The eight candidate control IDs and their order match the frozen configuration exactly, with all eight `passed:true`. The independent report's seventeen control IDs and order also match: one preserved positive fixture, followed by all sixteen required malformed-layout mutations rejected with their fixed source-defined reasons. Its `errors` list is empty. These are saved representation controls; no new scientific query is included.

Both target rows match the fixed browser journal sequences and independent descriptor byte counts:

| Original sequence | Original H tree stream | New tree stream | New/original | Required |
| --- | ---: | ---: | ---: | ---: |
| 60 (N5000-a k1 H) | 43,030,681 B | 9,498,259 B | 22.0732249% | ≤50% |
| 63 (N5000-a k2 H) | 43,040,079 B | 9,499,571 B | 22.0714534% | ≤50% |

Thus each observed target tree shrank by about **77.93%** in logical tagged-stream bytes. Across the full fixed corpus, original tree streams total 101,342,629 bytes and new tree streams total 23,162,035 bytes, or 22.8551748% of the original logical total. Those totals include absent/null/object accounting as defined by the protocol and are not full-native or full-browser storage totals.

The independent report has `complete:true`, `passed:true`, `layoutQualified:true`, `storageTargetPassed:true`, and `scientificValidated:false`. Candidate and checker agree on both target records and all size rows. The reviewed source enforces all-record reconstruction and both targets; the recorded success is not a selected passing subset.

## Claim limits

The result is a successful lossless tree-witness representation qualification on the **already exposed fixed corpus**. Its operational evidence supports the fixed byte/time gates and saved reconstruction/control results above. It does not establish physical validity, native numerical correctness, new exact-reference acceptance, geometric omission correctness, derivative/RK correctness, browser/query speed, standalone frame cost, or held-out generalization.

Only tree fields were re-encoded; all other full-native fields remain pinned input-only evidence. The measured output therefore does not prove that the original complete 16-stage/48-query browser attempt fits its 160 MiB evidence allocation, nor that unseen large-case witnesses have these sizes. The original terminal storage failure is not rescued or retried. No cap, threshold, input set, source or result was changed by this review. Viewer/UI QA is outside this operational review.

## Result anchors

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/run-attempt.json` | 1,891 | `3db0e7768031fb58e92a6f2474cbbf8cadba3c70583ea7b1d74f98c9f3a409f2` |
| `results/candidate.json` | 80,696 | `dd90cea8a40566d30ed3f9ea0b086dafe74a050416ce939a81cd4e02b767f161` |
| `results/check.json` | 96,758 | `0ee78af6bcf73fb28a181c9a8f8c00d43c90887c2c69ae9894f12a37d61e903c` |
| `source-publication.json` | 870 | `4d0b55d70cc701df1faa5084bc899a77f69fd90e1e51e045ab683ba2292866bc` |
| `review/SUPERVISOR-EXIT.json` | 507 | `8b15e920802bf61f27a8c7279a2711061b29bc860dce5b5a5a415eb60e874f78` |

This operational review leaves all result and source bytes unchanged.
