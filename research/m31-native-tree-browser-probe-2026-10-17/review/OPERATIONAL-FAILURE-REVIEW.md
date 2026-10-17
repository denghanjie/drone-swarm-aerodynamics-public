# Operational review of the terminal evidence-storage failure

Review basis: read-only inspection of the frozen attempt, descriptors, journal, shard bytes, source text, and a private-log snapshot on 2026-10-17. Public-file hash inventory completed at 04:11:10 UTC; storage inventory was taken at 04:10:39 UTC. This reviewer authored the transport, controller, and supervision source and is not an independent scientific checker. No project module was imported or executed, and no test, scientific calculation, browser launch, checker rerun, or retry was performed for this review. Only standard-library saved-data parsing, byte hashing, and filesystem accounting were used. Source and results remain unchanged.

The attempt is a **terminal operational failure**. The private browser log identifies `store-evidence-cap`; the public supervisor records `child-exit-browser`. The fixed 160 MiB evidence partition was exhausted while transmitting another record, although the 256 MiB aggregate allowance was not exhausted. The retained files do not establish completion of the registered browser schedule, fresh reference acceptance, checker acceptance, native semantic equivalence, or a speed result.

## Attempt and reason binding

The attempt binds source commit `4e1818c5b1ac7032018925edf17cecb1a6965e3d` and source-manifest SHA-256 `52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449` (51,047 bytes). Its timeline is:

| Saved event | Evidence |
|---|---|
| Supervisor start | 2026-10-17 04:08:23.769619 UTC |
| Saved-data validation | Completed, exit 0; 7.292437959462404 seconds charged to shared overhead |
| Browser stage | Failed; recorded stage wall time 54.42456883378327 seconds |
| Supervisor final report | `status: failed`, `executionRetries: 0`; 04:09:25.782802 UTC |
| External process observation | Parent reports supervisor exit 1 observed at 04:09:35 UTC; this review did not repeat that observation |

The private browser log is 1,802 bytes, SHA-256 `4b72a933736c7f34b38f39a881997989d1ff949d64172b7f997596080596132b`. Its sanitized failure is:

```text
page.evaluate: Error: store-evidence-cap
transport-store.cjs: need -> budget -> write -> put
controller.cjs: page.evaluate
```

The log's absolute paths and raw contents are not published. The error chain identifies the evidence-budget guard on a new shard write. In `transport-store.cjs`, `budget(add)` checks `evidence() + add <= 160 * 1048576` before the aggregate predicate; `write` calls it before opening the new file. Thus this failure did not authorize borrowing from another partition. The exact rejected packet length is not logged and is not reconstructed here.

The browser index contains a generic `controller-exception` / `PlaywrightError`, because the wrapped page exception is not a short permitted error-code string. The fallback records that error in `browser.json`; there is no durable journal failure record. The driver's source explicitly rethrows a failed persistence operation instead of relabelling it a completed scientific failure record. These facts explain why the precise storage reason comes from the pinned private log rather than the public error-code field.

## Exact storage accounting

All sizes below are logical `stat`/`lstat` bytes, matching the supervisor's accounting convention, not filesystem allocated blocks or memory usage. MiB means 1,048,576 bytes. Private symlinks, if present, would be counted by `lstat` without following them; this snapshot contains none. No public result symlinks were found.

| Fixed allocation | Limit, bytes | Retained bytes | Remaining within allocation |
|---|---:|---:|---:|
| Evidence: `shards`, `records`, `saved-records` | 167,772,160 (160 MiB) | **167,411,867** | **360,293** |
| Entire private tree: profile, logs, supervision files | 67,108,864 (64 MiB) | 8,791,368 | 58,317,496 |
| Other public outputs, excluding attempt report | 31,457,280 (30 MiB) | 88,940 | 31,368,340 |
| Attempt/finalization allowance | 2,097,152 (2 MiB) | 2,096 final attempt-report bytes | 2,095,056 nominal allocation balance |
| Aggregate | **268,435,456 (256 MiB)** | **176,294,271** | **92,141,185** |

The aggregate write guard additionally reserves 2,097,152 bytes above extant files, so the snapshot's headroom under that conservative predicate is 90,044,033 bytes. This does not change the independent evidence limit. A standard 1 MiB nonfinal shard could not fit within the evidence partition's 360,293-byte balance. The log proves a refused new-shard write; it does not identify that particular shard's length.

The 1,145 public result files total 167,502,903 bytes:

| Public category | Files | Bytes |
|---|---:|---:|
| Binary shards | 948 | 166,311,854 |
| Saved-data record descriptors | 126 | 687,982 |
| Browser record descriptors | 66 | 412,031 |
| Root output files | 5 | 91,036 |

The largest public file is 1,048,576 bytes. The 201 private files total 8,791,368 bytes: profile files 8,787,506; private root files 3,768; the two retained supervisor-directory file pairs 47 bytes each. The largest private file is 4,202,496 bytes. These observed files are below the fixed 32 MiB per-file limit. The failure reason is the aggregate evidence partition, not one oversized file, the private partition, or the overall 256 MiB allowance.

The supervisor's `outputLogScratchBytes` is 176,293,417, taken before its final durable report write. The later snapshot is 854 bytes larger. These are different observation points; the review does not claim byte-exact failure-time private usage or attribute all 854 bytes to a particular write. Both counts remain far below 256 MiB. Neither count measures process memory.

The saved-validation stage already occupied 1,382,683 evidence bytes: 687,982 descriptor bytes plus 694,701 bytes of distinct shards reachable from those descriptors. The browser store's reported `newBytes: 166029184` reconciles exactly to the increase in evidence bytes: 167,411,867 minus 1,382,683. Its `deduplicatedBytes: 40671014` is a producer counter; the review does not treat it as an independently replayed transfer count. Source text requires full byte equality with an existing shard before deduplication.

## Retained complete records and unfinished transmission

Every one of the 66 journal rows has its matching persisted descriptor and exact recorded byte count/SHA-256. All 126 saved-data descriptor pins also match the saved transport index. Across all 192 descriptors, all 3,111 shard references resolve to their declared byte counts and SHA-256; all 948 stored shard filenames match the SHA-256 of their actual bytes. These are storage-integrity observations, not a scientific-checker pass or a fresh validation of the logical payloads.

| Shard reachability from complete descriptors | Files | Bytes |
|---|---:|---:|
| Saved-data descriptors only | 419 | 693,962 |
| Browser descriptors only | 497 | 145,388,945 |
| Shared by both descriptor groups | 9 | 739 |
| Referenced by either group, total | **925** | **146,083,646** |
| Referenced by neither group | **23** | **20,228,208** |
| Stored shards, total | **948** | **166,311,854** |

The 23 unreferenced shards are retained partial-transmission material. Their individual bytes are intact and content addressed, but no complete record descriptor establishes their ordered fields, full record coverage, or durable record acknowledgement. They must not be counted as another complete native query or scientific failure record. They are included in the evidence partition and have not been deleted or reclassified. A shard's hash is not a replacement for the absent record descriptor.

The write ordering explains this state: browser `encodeRecord` sends shards while constructing a descriptor; only after that operation succeeds does `__appendTreeRecord` persist the descriptor and append/fsync its journal row. A later refused shard can therefore leave earlier shards from that record on disk without an acknowledged record. There is no completed descriptor after sequence 65 and no `driver-summary` or `driver-failure` row.

The 66 durable browser rows are 1 source, 1 factories, 12 wiring-control, 3 initial, 3 controller, **30 native**, **10 stage**, 2 step, 2 safety, and 2 case-summary records. Metadata-only decoding of retained case/stage/method fields shows 12 native records for N=64, 12 for N=1000, and 6 for the first N=5000 case. The last descriptor is `0065-stage.json`, identifying `tree-t0-n5000-a-step0-k2`. The first two cases have the recorded case-summary sequence; the first N=5000 case has only its first two stage sequences. This is retained record coverage, not an independent correctness claim. The second N=5000 case is not represented by an initial record.

The fixed next scheduled slot is H at `tree-t0-n5000-a-step0-k3`. That is source-defined schedule context, not proof that a complete third-stage H result was retained. The unreferenced shards cannot supply the missing durable record or the remaining registered schedule.

The descriptor byte counts show why the retained evidence grew quickly:

| Complete native descriptor | Method | Full logical binary stream bytes | Tree-field stream bytes |
|---|---|---:|---:|
| `0058-native.json` (N=5000, k1) | F | 6,765,421 | No tree field |
| `0059-native.json` (N=5000, k1) | H0 | 7,701,348 | 935,926 |
| `0060-native.json` (N=5000, k1) | H | **49,796,102** | **43,030,681** |
| `0062-native.json` (N=5000, k2) | H0 | 7,701,368 | 935,926 |
| `0063-native.json` (N=5000, k2) | H | **49,805,520** | **43,040,079** |
| `0064-native.json` (N=5000, k2) | F | 6,765,441 | No tree field |

These are logical encoded lengths read from stored descriptors, not disjoint disk allocations: content-addressed chunks can be shared. The first N=5000 case's 10 complete descriptors reference 118,913,967 shard bytes first encountered after the prior saved/browser records, plus 92,820 descriptor bytes. The tree field is the dominant logical field in the two shown H records. No claim about the still-unretained records' sizes, numerical values, cull efficacy, or performance follows from that observation.

## Closure and claim limits

`browser.json` records `complete: false`, one Chrome launch/profile, browser close, and specific Chrome-root exit and close events with code 0 and null signal/error. The supervisor records `failedOwnedChildReaped: true` and `preservationPassed: true`. Its `supervisorExitVerified: false` remains an honest self-report limitation; the parent supplied the separate exit-1 observation. Neither file claims that every browser helper exited or that an OS memory limit was enforced.

The browser's `inputsAndSourcesPreserved: false` indicates that its successful post-driver preservation path was not reached. It is not itself evidence of a detected mutation. The enclosing supervisor separately reports preservation passed. This review hashed the retained output set and checked its storage pins; it did not rerun the enclosing preservation or numerical checker.

The saved-data validation report is `complete: true`, `passed: true` for 42 frozen cases / 126 prior records, plus its saved-data controls. That gate precedes the fresh browser probe and cannot qualify the partial fresh evidence. Reference and checker stages have no attempt entries or result files. The registered 16-stage / 48-native-record schedule is incomplete. No reference accuracy, method equivalence, speedup, standalone frame cost, final safety outcome, or completed-step result is established by this failed attempt.

## Bounded source-only options for a separate design

The current attempt is closed and frozen. The following are prospective design choices only, with no implementation, execution, changed cap, or implied launch authorization:

1. **Pack the full tree certificate structurally.** The existing codec already compacts gathered indices and interns exactly equal leaf lists. Its H culls still appear as repeated objects with node/axis/side/difference fields inside each receiver. A new versioned schema could retain every actual cull in typed columns with receiver offsets, integer node/axis/side values, and exact eight-byte difference words. It must preserve order, all evidence, signed-zero/word semantics, exact expansion, unknown-field rejection, and independent decoder checks. The observed 43 MB H tree streams identify a worthwhile target; no compression ratio or fit is claimed without a separately reviewed saved-data assessment.

2. **Separate independently shareable tree components.** Whole-tree fields include both common geometry and method-specific traversal evidence, which prevents whole-field equality when either portion differs. Versioned references for actual node geometry, canonical IDs, leaf lists, and per-arm traversal streams may expose more byte-identical sharing within a stage. A hash may select a candidate only; each reused component must still pass full byte equality. Do not infer equality across arms or stages, omit records, recompute evidence from a different source, or replace coefficients/certificates with summaries. Any added dictionary and reference metadata counts against the same evidence allowance.

3. **Reserve a complete record before accepting its first new shard.** A bounded record manifest can support a conservative reservation for all new shard bytes, descriptor bytes, and the journal acknowledgement. Tentative evidence remains charged to the evidence ledger; moving it into private scratch must not bypass the 160 MiB limit. Exact-byte dedup may credit the reservation only after comparison. This can make a refusal occur before a record leaves unreferenced shards, improving failure accounting. It does not shrink the scientific evidence or prove the full schedule fits. The current partial shards stay frozen.

4. **Require a source-level storage envelope before proposing another attempt.** Account jointly for saved-data artifacts, all methods and stages, worst permitted coefficient/certificate counts, dictionaries, descriptors, journal, private files, downstream reference/check results, and closure. Keep 256 MiB total, 32 MiB per file, and the registered time budget fixed. Compression and observed dedup must not be assumed for an all-admitted-input bound. If the unchanged scientific schedule cannot fit a defensible envelope, leave it disabled. A smaller scientific question would need a separate explicit preregistration and review; it cannot be presented as completion or rescue of this attempt.

The most direct next source-only analysis is a lossless structural tree-certificate schema plus a conservative byte ledger. That work must retain the complete evidence obligations and independently account for data that do not deduplicate. Unused private/downstream reservations and deletion of partial artifacts are not remedies for this closed attempt.

## Reproducible evidence pins

| Retained public artifact | Bytes | SHA-256 |
|---|---:|---|
| `results/run-attempt.json` | 2,096 | `ccae2f966e131fe4a4c78640f3268722025060f885138242efa90e32962abc36` |
| `results/browser.json` | 3,211 | `e619e52119aa3b8fd5d76d883855aa6763a1c6db7ab5357ddfba9378c31ebb2e` |
| `results/browser-journal.jsonl` | 23,514 | `e66b7234016d9851ce0dbc078e80e97c88dd2bbe8ed139db234b46c5d1eaa173` |
| `results/saved-transport.json` | 58,498 | `b5245538e86c9f2a657205ce6177c90702e0c27bf22e247d44db5e63fe6900c7` |
| `results/saved-validation.json` | 3,717 | `809fbdd360742df12ec5d8cba49e67d2845a320e682dbd265db46adb45091aec` |

The canonical inventory of all 1,145 public result files has SHA-256 `4869d783a1ff1e08612d953cb8bfe089f51eafe3396f467afbfd9069dd381698`. Its deterministic representation is: files sorted by repository-relative POSIX path; each entry has `path`, `bytes`, `sha256`; the list is serialized with Python `json.dumps(..., sort_keys=True, separators=(',', ':'))` and one final newline. This inventory covers 167,502,903 retained bytes. It is a review accounting digest, not an execution-manifest replacement.

Relevant inspected source pins are `transport-store.cjs` SHA-256 `ab9683bddbd57d5f68764c3993293ba62d4775922055e872ab3caa852f55f8ba`, `transport.cjs` `ad5cc73b6bac321eb78deea82602d67fc8452cc204cc2e1d3b5a7ed84bef7e57`, `controller.cjs` `89c7bb8cbb4981ebf00431eea480bc3c2a86a99aafbd2945d399070a178beaa9`, and `run.py` `7ed098bb88037d46874880483e36100bf1aef04d44aaf565c27ef5c48231840a`. Parent owns publication and the complete frozen-artifact receipt.
