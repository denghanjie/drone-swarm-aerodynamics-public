# Independent saved-result evidence review

**Disposition: no evidence-binding blocker found. The predeclared keep gate fails.** All 116 retained outputs match the exact declared saved-F semantic baseline, but H is slower than F in all 24 measured pairs. The retained analysis reports median paired H/F **2.2822220357956775**, zero strict wins, and `keepGatePassed: false`. This supports “no worthwhile speed improvement demonstrated for this workload,” without a generalized performance or accuracy claim.

This review inspected retained source/report metadata, file hashes and lengths, actual semantic-output bytes, schedule and report bindings, and reported-count/timing consistency. It did not run a producer, scientific checker, exporter, or analyzer, decode old numerical shards again, regenerate an input, execute a browser, or change an old artifact. Hashing and comparison of already retained bytes are not another numerical trial. This review is the reviewer's sole new output for this inspection. Inspection took place after the successful attempt on 18 October 2026 at approximately 12:10–12:12 UTC.

## Published source and preserved provenance

| Item | Retained identity |
|---|---|
| Published execution source commit | `94ecec03c1260b7e63f5bbb1dce8345e1b2373b7` |
| Source-manifest base commit | `13bd59fbfb92649afdff3f71f6c460554107fcf5` |
| Source manifest | 14,953 B; SHA-256 `1a3fcbcf8c486cdfc34d02d7b3348c2d0f9574431f8fe509c9e65a0c72ef47fa` |
| Manifest closure | 67 distinct file pins; 7,193,511 referenced bytes |
| Publication receipt | 856 B; SHA-256 `24626e8cfa8411218d4e52dcbe141ab2982fb4341bd5624fe27b1926ee23ec13` |
| Public verification recorded | 12:08:57.515675 UTC, before the attempt start |

Every one of the 67 source-manifest pins independently rehashed successfully in this review, including the exported input/baseline, their provenance, frozen source, and reused dependencies. Paths stayed within the repository and no pinned file was a symlink. Manifest byte length/hash and pin count agree with the publication receipt. The receipt records both committed/local and remote/local equality for the exact public commit. This review checked the retained receipt and local bytes; it did not perform another network download.

The five reviewed timing sources and protocol retain the exact identities in `review/EVIDENCE-REVIEW.md` (14,025 B; SHA-256 `014cde99893ec699958ac8a611c3f96d480af57347d484223934f4721833d08f`). The independent protocol review is also preserved: 11,155 B; SHA-256 `0fe48604d1af4573b1f46b68f7cb759c3b9b79e6c094ce0f2c7df7fc1bc3c65c`. Neither earlier review was edited by this inspection.

The source manifest was created at 12:07:34.112562 UTC, permits 116 scientific queries, and declares the inclusion of saved evidence and the unmodified bundle. The public verification precedes the actual attempt start at 12:09:18.975193 UTC. The source-manifest base commit and published execution commit have different roles; they are not competing execution identities.

## Attempt, closure, and report pins

| File | Bytes | SHA-256 |
|---|---:|---|
| `results/attempt.json` | 120 | `352f4abbfa329dabcbf72850f44534586e9c8c9e7449825275d97a38d397ccd3` |
| `results/environment.json` | 532 | `12d9fbd33d4919784b90a01d00df01618caa239588ee193557e1d56b9355dc01` |
| `results/browser-summary.json` | 3,587 | `d92086e19a2ffb366b8dafb508911491e178b8799452c531dfb3a95db3a80546` |
| `results/browser-exit.json` | 193 | `3c77c3da15f0ce67bb3a3ca61d58a4262a17d2ed651fabe639a93e8f1fbd7dac` |
| `results/supervisor.json` | 248 | `11182ca2825b0021d87bfdf8a6aab993d6876c34279c37e70c68fb624388f7e7` |
| `results/analysis.json` | 18,882 | `a70864cda28798c32074f46579578917bf819dd42069d6be9ae17daece56d556` |
| `EXTERNAL-EXIT.json` | 161 | `4d181ba8a3fbe3b1665b94eedb37b236d880fd205ed153c754e4c4b022543c2b` |
| `ANALYSIS-EXIT.json` | 263 | `3cf7cebeed79ffd9f729867f5d467265a550ee42ac83e31d8759daaa29fa80d8` |

The immutable attempt record declares the start, 180-second maximum, 116-query maximum, and `status: started`. Successful completion is separately recorded by the browser summary, browser exit, and supervisor reports; this design does not rewrite the initial attempt record into a terminal status.

The browser reports one launch, 116 rows, `completed: true`, `contextClosed: true`, and root exit and close both `{code: 0, signal: null}`. Its wall value is 20,931 ms and finish time 12:09:39.941 UTC. The supervisor reports exit zero, null failure reason, 21.011124208569527 seconds, and finish at 12:09:39.991315 UTC. The external receipt records command session 96220, exit zero observed at 12:09:49.026453 UTC. Observation time is not an exact process-exit timestamp.

`EXTERNAL-EXIT.json` contains session/exit/time/scope metadata, not an embedded attempt-report hash. This review pins that retained receipt alongside the attempt and completion reports and relies on the parent's direct command observation for its session attribution. It does not invent a stronger self-contained cryptographic binding for that receipt. The browser environment itself binds the published source commit and manifest hash above.

The analysis exit receipt records exit zero, 0.157257666811347 seconds externally, empty stderr, and a stdout summary agreeing with the retained analysis values. The analyzer's own elapsed value is 0.13087791576981544 seconds; these are different timing boundaries. Neither was rerun by this reviewer.

Runtime metadata records Node v24.19.0, Chrome 155.0.8059.80, V8/JavaScript version 15.5.35.23, darwin arm64, and a headless Chrome user agent. Root process closure and the supervisor command's observed exit do not establish every operating-system helper's exit. The supervisor explicitly retains `allHelperExitVerified: false`.

## Exact output closure and correctness scope

The frozen input file is 343,903 B with SHA-256 `e007c459fd1ab1a796a27b6455f4ee3bfe27766fb63ff9e65a4f679a75b18d0f`. It is the exact saved projected first N1000 state exported from the prior qualified F record, not a regenerated initialization or a newly advanced state.

`expected.json` is 2,554,204 B with SHA-256 `e135b68c15c0198cc72c833c0b28d018353f016dcae30ab4cbe5e95d060cde1e`. Removing only its final newline gives the host comparison baseline: **2,554,203 B**, SHA-256 **`baee267d0d463ff059f8e61575c8a60f395d9713f9ac8a8a8325875f7c8408d7`**.

All 116 query rows pin the retained file `results/semantic-baee267d0d463ff059f8e61575c8a60f395d9713f9ac8a8a8325875f7c8408d7.json`. This review independently resolved every row's pin, checked the required content-addressed filename, read the referenced bytes, checked its length and SHA-256, and compared it to the frozen baseline bytes. **All 116 byte comparisons passed.** There is one unique semantic blob and no unreferenced additional semantic blob. Its sharing follows exact-byte deduplication by the frozen host source; it is not merely a producer's checksum assertion.

Every row also has `native-success`, `inputUnchanged: true`, `semanticEqual: true`, and `hostEqual: true`. The retained analyzer reports `complete: true`, `correctnessPassed: true`, `queriesChecked: 116`, and `measuredQueries: 96`. No failure artifact exists in the result inventory.

The exact compared projection includes status, reason, constants, raw input, IDs, prepared geometry, coefficients, solution, loads, consumption, and retained diagnostics. Remaining numeric values are normalized to exact binary64 hex. Method labels, timing, and tree-witness representation are outside the projection. The only diagnostic exclusions are the frozen four paths: build-phase timing, gathered-nonself-candidate work count, ordered screen visits, and screen component tests. The detailed source review records their exact names and the independent Python/browser normalization correspondence.

This establishes equality to the previously checked saved F evidence for this one input under those exclusions, including word-level zero signs in the selected scientific values. It does not create a new high-precision reference, independently reconstruct the full controller, advance an RK step, validate a trajectory, or establish physical accuracy. No new full tree certificates were retained or independently recertified per timing call. HC measures production of the witness in the call, while successful witness bodies are excluded from the retained semantic comparison. The earlier complete single-state certificate remains prior evidence.

The browser summary reports the fixed nine Buffer-compatibility control groups and all 56 named checks passing before scientific factories. These are retained adapter checks; this review inspected their saved metadata, not another execution of the controls. General Buffer API or NaN-payload equivalence is outside their scope.

## Schedule and independent metadata checks

| Query kind | Calls | Use |
|---|---:|---|
| Warm-up | 16 | Four blocks, retained but excluded from the decision |
| Measured | 96 | 24 complete four-arm blocks |
| Instrumented diagnostic | 4 | Final F, H, HC, H0 calls, excluded from the decision |
| Total | 116 | All require exact semantic agreement |

There are exactly 116 query files and 116 transfer files. Each query/transfer call number agrees. The warm/measured schedule matches the four cyclic orders F/H/H0/HC, H/HC/F/H0, HC/H0/H/F, and H0/F/HC/H. Each arm occupies each measured position exactly six times. The final diagnostic rows have the declared arm, block zero, and positions zero through three.

This review checked the rows' call/kind/block/position/arm identities against that schedule, successful statuses and equality flags, positive finite query times, and finite nonnegative native/phase/build/encode/compare/transfer/persistence times. Each of the 24 saved analysis-pair F and H times matches the corresponding retained query row, and every saved win flag agrees with H<F. Each saved diagnostic object in the analysis agrees with its source query row. This is saved metadata consistency inspection, not a rerun of `source/analyze.py` or the numerical producer.

## Recorded timing decision

| Arm | Outer median ms | Outer interquartile range ms | Native internal median ms |
|---|---:|---:|---:|
| F | 36.850 | 35.875–45.925 | 34.200 |
| H, witness disabled | 85.150 | 84.225–85.950 | 82.650 |
| HC, witness enabled | 90.100 | 89.500–90.925 | 87.550 |
| H0, no group omission | 106.350 | 104.875–107.550 | 103.800 |

The decision statistic is the **median of 24 paired ratios**, not the ratio of the two arm medians. The saved analysis reports:

- Median paired H/F: **2.2822220357956775**.
- Strict H wins: **0/24**; H is slower in every retained measured pair.
- Reported individual H/F ratios range from **1.5878003690666695** to **2.7205479504310923**.
- Median paired HC/H: **1.0577742764216473**.
- Median paired H0/F: **2.8786157666216834**.
- Keep gate: **false**, against the predeclared requirements of median H/F <=0.90 and at least 20 strict wins.

The analyzer's source, already reviewed and now rehashed, uses the standard even-N median and does not remove outliers or replace runs. This inspection checked the retained pair-to-row bindings and gate interpretation without repeating that analysis program.

The primary outer interval includes fresh decoding of input words and the submitted-input immutability check, in addition to the full native call. It is not solely the native internal timer. Both fields are retained. Encoding, semantic comparison, and host transfer/persistence occur afterward. Approximate retained encoding medians are 24.150/23.900/29.450/23.800 ms for F/H/HC/H0; semantic comparison medians are 12.800/12.650/12.950/12.750 ms. Transfer intervals are approximately 43–44 ms and already include persistence, whose medians are approximately 6.6–7.3 ms. Adding persistence again would double-count it. Phase medians must not be summed into a purported complete frame cost.

The diagnostic calls report:

| Arm | Tree build calls / ms | Gather calls / ms |
|---|---:|---:|
| F | 0 / 0 | 0 / 0 |
| H | 1 / 0.600 | 1,000 / 49.700 |
| HC | 1 / 0.600 | 1,000 / 54.400 |
| H0 | 1 / 0.600 | 1,000 / 65.200 |

These single instrumented diagnostics indicate substantial cost in the combined gather/traversal/sort/capture region. They do not isolate sorting from traversal, establish an asymptotic cause, or replace the uninstrumented measured decision. HC/H suggests that disabling witness capture alone does not remove the observed performance disadvantage; it is not a pure causal subtraction of otherwise identical timings.

The outcome concerns only the saved first projected N1000 state, this machine/runtime, one browser process, and the declared warmed schedule. F already applies component screening. It provides no generalized tree-versus-pair theorem, population inference, sustained flight/frame-rate result, or license to perform an unallocated optimization rerun.

## Retained bytes and privacy

The independently measured `results` inventory contains **239 files and 2,706,491 bytes**. The semantic blob accounts for 2,554,203 bytes; the other 238 result files account for 152,288 bytes. No additional semantic or failure file is present. The largest result file is the semantic blob.

The supervisor reports 5,681,636 public-package bytes and 8,786,725 private-execution bytes at its pre-report accounting point, or 14,468,361 bytes combined. That reported combined scope is below the declared 32 MiB public / 128 MiB private / 160 MiB combined allocations. This review did not independently inspect the private profile or logs and does not present the private count as a fresh measurement.

A later independent public-package snapshot at 12:10:50 UTC contained 269 files and 6,137,372 bytes. It includes post-attempt analysis/receipts and concurrently prepared saved UI artifacts, so it is not the supervisor's earlier accounting scope. This review file and subsequent packaging changes are outside that snapshot. The stable scientific result count above is the review's precise inventory claim; final publication packaging belongs to the parent. Disk allocation is not a hard memory cap or a proof of zero transient overshoot.

Scanning the retained public result JSON text found zero matches for the checked absolute home-directory prefixes, private/temp-directory prefixes, or common credential-assignment literals. The scan is not exhaustive secret detection. No private directory path, profile content, or private log body is published here.

## Closure

Source preservation, the 116-call schedule, every retained semantic-byte pin, analysis-to-query bindings, publication-before-launch ordering, and the available root/external exit observations agree. There is no evidence-integrity blocker to reporting this attempt's result. Correctness passed within the declared equality scope; the predeclared performance gate did not. The appropriate conclusion is to retain this version as a negative result for the tested workload, with any optimization or broader experiment requiring its own future allocation.
