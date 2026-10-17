# Terminal evidence review

Reviewed on 2026-10-17 at approximately 04:10–04:12 UTC. **The one attempt failed at the frozen 160 MiB unique-evidence partition.** Saved-data validation passed before fresh initialization, but the browser schedule was incomplete and neither exact reference nor final checker ran. No speed, exact-load accuracy, full native-equivalence, complete tree-proof, full derivative/RK or engineering-gate conclusion follows from this attempt.

This reviewer authored the new independent checker/decoder and separately reviewed the candidate/adapter source; the candidate and browser producer were authored by other agents. This terminal review is separate from the producer. It is not independent of the decoder's authorship and does not replace the unexecuted final scientific audit.

## Review procedure and provenance

The review performed read-only JSON/source inspection, exact length/SHA-256 checks, filesystem byte inventory and selective metadata decoding through the frozen pure `compact-check.py` transport decoder. It did not invoke its proof functions or qualification entry points. No native query, initializer, scientific checker, reference, browser, network access or Git operation was rerun. Frozen source and result bytes were not changed; only this review document was added. Temporary inspection output was outside the experiment's private/output trees.

The execution source commit is `4e1818c5b1ac7032018925edf17cecb1a6965e3d`. The source manifest is 51,047 bytes with SHA-256 `52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449`. This review rehashed all **235 manifest-listed files** and found each exact path, byte count and SHA-256 unchanged.

The saved publication receipt binds that commit and manifest, reports exact remote/committed/local equality, and was recorded at `2026-10-17T04:08:08.768500+00:00`, before the attempt began at `04:08:23.769619 UTC`. The review verified the local receipt and its time/bindings; it did not perform a second remote fetch or Git verification. Receipt SHA-256: `4bc17710ac14f62f4a0b5f5afd87d7b50e8bd3167ff5336672d528b1ee9c157b` (881 bytes).

The enabled configuration retains 120/600/180-second browser/reference/check allocations, 60 seconds shared overhead, a 960-second total, 32 MiB per file and 256 MiB combined output/log/profile/scratch. The fixed 15-second saved-data gate is inside shared overhead. The recorded start leaves the full reservation before the unchanged `05:06:20 UTC` cutoff. The attempt records zero retries.

## Saved-data gate

The supervised saved-validation stage completed with exit code zero in **7.292437959 seconds**, before the browser stage started. Its saved report has `complete:true`, `passed:true`, no errors and the exact execution source bindings. It records:

- All 42 old cases and 126 old F/H0/H records.
- All fifteen retained corruption laws and three focused compact corruptions rejected with their fixed reasons.
- Six JavaScript codec controls passed.
- Ten independent decoder malformed-input controls rejected with fixed reasons, plus literal-word/signed-zero preservation.
- Sixteen fixed subtraction fixtures and six threshold comparisons passed.

This is a successful validation of exposed saved data and the new format/proof implementation within that gate. It is not a new proof for the later fresh partial browser records. The saved-transport index contains 126 descriptors; this review rehashed each descriptor and its referenced shards without rerunning its numerical qualification.

## Durable browser coverage

The browser index binds a 23,514-byte journal containing **66 contiguous zero-based rows**. This review checked each exact `NNNN-kind.json` descriptor path and pin, all referenced shard pins, and the content-addressed names/hashes of all **948** shard files. Selected decoded identity/status fields agree with the journal and index counts.

| Case | Durable native records | Durable stage records | Durable endpoint steps | Case summary |
| --- | ---: | ---: | ---: | --- |
| `tree-t0-n64-a` | 12 | 4 | 1 | Present |
| `tree-t0-n1000-a` | 12 | 4 | 1 | Present |
| `tree-t0-n5000-a` | 6 | 2 | 0 | Absent |
| `tree-t0-n5000-b` | 0 | 0 | 0 | Absent |
| **Total** | **30** | **10** | **2** | **2** |

The other rows are one source record, one factory record, twelve wiring controls, three initial records, three controller records and two safety records. The first 5000 case's initializer uses the fixed seed 26171733. Its first stage has F/H0/H in registered order and its second has H0/H/F. The final journal row, sequence 65, is `tree-t0-n5000-a-step0-k2`. The second 5000 case has no initial record and no evidence of exposure in this schedule.

The thirty durable native records report `native-success` and unchanged submitted inputs. The ten stage records report `completed` and `semanticAgreement:true`. Those are saved producer observations; the full independent fresh-record checker did not run. The first two endpoints likewise remain unaudited by that checker. A durable record count is not an exact total of native calls executed: a later query can finish before its append fails, and the partial append has no complete descriptor from which to certify another query result.

There is no final driver summary, `results/reference.json`, or `results/check.json`. The supervisor stage map contains saved-validation and browser only. Consequently none of the four prescribed fresh64 exact-reference states was evaluated by the scheduled reference stage, and the 44,262-derivative / 752,454-component final audit was not performed.

## Failure and resource accounting

The private browser log identifies `page.evaluate: Error: store-evidence-cap`, originating in `transport-store.cjs`'s pre-write `budget()` check during shard `put()`. The public browser index records a generic `PlaywrightError` / `controller-exception` in the coupled-driver phase; the supervisor's terminal reason is `child-exit-browser`. These describe the same propagated persistence failure at different layers. The private log itself was inspected without copying its local paths, runtime stack or command details into public evidence. Its 1,802 bytes hash to `4b72a933736c7f34b38f39a881997989d1ff949d64172b7f997596080596132b`.

The source-frozen unique-evidence ceiling is **167,772,160 bytes (160 MiB)**. It covers shards, browser record descriptors and saved-validation record descriptors together. The post-exit inventory was:

| Partition | Files | Bytes |
| --- | ---: | ---: |
| `results/shards` | 948 | 166,311,854 |
| `results/records` | 66 | 412,031 |
| `results/saved-records` | 126 | 687,982 |
| **Unique evidence total** | **1,140** | **167,411,867** |
| **Remaining evidence headroom** | — | **360,293** |

This is 159.6564 MiB of the 160 MiB partition. Another ordinary 1 MiB shard cannot fit. The failed write's exact proposed length is not recorded, so this review does not invent that length or a complete failed-record size. The persisted maximum shard is exactly 1 MiB; the largest browser descriptor is 18,030 bytes. The largest declared binary record is 49,805,520 bytes, below the independent 96 MiB logical record limit; it is distributed over shards rather than stored as one file.

**Twenty-three shard files totaling 20,228,208 bytes are not referenced by any completed browser or saved-validation descriptor.** Their content hashes are valid. The writer persists shards before its final descriptor, so an interrupted append can leave this durable prefix. These bytes count against the fixed cap and must be preserved. They cannot be promoted to a complete native/stage record or silently discarded to rescue the run.

The final review snapshot contains 167,502,903 bytes in results and 8,791,368 bytes in the private tree: **176,294,271 bytes (168.1273 MiB)** combined, below 256 MiB. The private tree is below its 64 MiB partition and its largest file is 4,202,496 bytes. All observed files are below the 32 MiB ceiling. Thus the terminal cause is the internal **evidence reservation**, not overall aggregate-disk exhaustion, a per-file cap or a demonstrated memory ceiling.

The supervisor's saved `outputLogScratchBytes` is 176,293,417, measured before its final durable attempt-report replacement. The later filesystem snapshot is 854 bytes larger. These are different documented observation points; the review does not relabel either as an exact exited-process peak. Browser-stage elapsed time is 54.424568834 seconds, below 120; total pre-final-report wall time is 62.027892458 seconds, below 960. Neither clock establishes a complete scientific timing result.

## Closure and preservation distinctions

The browser index has `complete:false` and **`inputsAndSourcesPreserved:false`**. Source inspection shows that the controller sets that preservation flag only after the driver schedule returns successfully and its post-run preservation loop completes. The persistence exception prevented that path. The false flag therefore means this browser-level completion assertion was not established; it is not, by itself, a report of identified source corruption.

Separately, the supervisor has **`preservationPassed:true`**. Its finalization rechecks the 235 source pins, protected manifest/publication files and the previous completed stage's protected outputs. This review independently confirms the manifest-listed bytes, saved indexes, journal/descriptors and shard hashes at review time. The supervisor's broader source/prior-output preservation does not turn the false browser completion flag into true, independently certify every fresh submitted input, or establish fresh scientific correctness.

The specific owned Chrome root emitted both exit and close with code zero and no signal; `browserClosed:true` is saved. The browser guardian's saved direct-child exit is 1; the saved-validation guardian's is 0. The supervisor records `failedOwnedChildReaped:true`. `allHelpersExitClaim:false` and `memoryLimitClaim:false` remain explicit. This establishes the recorded owned-root/group handling, not universal helper cleanup or an OS memory limit.

`supervisorExitVerified:false` remains in its own ledger because the process cannot certify its own future exit. The parent separately reported observing the tool's terminal exit code 1 at approximately 04:09:35 UTC. That external observation is distinct from the saved ledger and from this read-only filesystem review.

## Frozen terminal file identities

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/run-attempt.json` | 2,096 | `ccae2f966e131fe4a4c78640f3268722025060f885138242efa90e32962abc36` |
| `results/browser.json` | 3,211 | `e619e52119aa3b8fd5d76d883855aa6763a1c6db7ab5357ddfba9378c31ebb2e` |
| `results/browser-journal.jsonl` | 23,514 | `e66b7234016d9851ce0dbc078e80e97c88dd2bbe8ed139db234b46c5d1eaa173` |
| `results/saved-validation.json` | 3,717 | `809fbdd360742df12ec5d8cba49e67d2845a320e682dbd265db46adb45091aec` |
| `results/saved-transport.json` | 58,498 | `b5245538e86c9f2a657205ce6177c90702e0c27bf22e247d44db5e63fe6900c7` |

The defensible outcome is a terminal operational limitation: this fixed full-evidence implementation did not finish the registered four-case probe within its predeclared evidence reservation. It does not show that H passes or fails the 0.80 speed gate, that H is more accurate, that large-N omission proofs have passed, or that a 2.5 ms production step is feasible. No cap increase, retry, alternate seed, reference/checker rerun or continuation is warranted by this review.
