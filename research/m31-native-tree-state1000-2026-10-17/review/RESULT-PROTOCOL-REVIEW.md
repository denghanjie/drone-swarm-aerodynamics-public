# Protocol and outcome review: single N1000 state

Conclusion: **the saved reports and independently checked metadata support the registered conditional pass for this one state; no protocol or accounting blocker was found.** They do not support high-precision N1000 accuracy, complete independent controller correctness, a trajectory/endpoint, physical validity or speedup. The sole scientific attempt is consumed, and its sources and outputs remain immutable.

This is the one saved-result review allocated in `review/RESULT-INSPECTION-PROTOCOL.md`, closed before 05:35 UTC. The reviewer read source/report text, parsed JSON and descriptor metadata, hashed files, counted bytes and performed arithmetic on reported values. No project module, initializer, native query, codec, scientific checker, reference routine or derivative was executed. Binary shards were only read as opaque bytes for hash/length checks; their numerical contents were not decoded. This report therefore independently reviews provenance, count and accounting consistency; it does not claim a second scientific proof execution.

## Attempt identity and closure

The reports bind source commit `7a30c960f431ef9b3e98ab307432edc586c6c862` and execution-manifest SHA-256 `e4a21305b0f6a228dcbcecee0c4672ec427a379ec491942ee9d272d983be8e3c`. The local execution manifest is 397,744 bytes. All **1,604** manifest pins were rehashed successfully during this review and again at closure.

The publication receipt records exact source verification at 05:19:19.082936 UTC, preceding attempt start at 05:19:38.163020 UTC. This review checked its source identity and ordering; it did not redownload the remote manifest. The published-source equality claim remains the separately recorded prelaunch verification, not a new network verification by this reviewer.

All three supervised stages are completed with exit code 0: retained metadata validation, browser and checker. Their saved output hashes match the attempt record. The browser records one launch/profile, complete=true, no errors, successful exit and close of the specific Chrome root, and preserved sources/inputs. The checker records complete=true, passed=true, no errors, sourcesPreserved=true and conditionalNativeQualified=true. The supervisor records firstFailure=null, preservationPassed=true and executionRetries=0.

`EXTERNAL-EXIT.json` independently records tool session 45337 exiting 0, binds the final attempt SHA and records one scientific launch with zero retries. Its observation time is 05:20:01.419191 UTC. The final attempt reports completion at 05:19:50.500256 UTC. `supervisorExitVerified:false` inside that attempt is honest: the supervisor cannot observe its own later process exit. The separate exit artifact supplies that external observation; its later observation timestamp must not be substituted for exact process duration. This reviewer inspected that artifact and did not personally observe or rerun the original tool session.

The explicit `allHelpersExitClaim:false` and `memoryLimitClaim:false` boundaries remain intact. Root exit/close and the externally observed supervisor exit are not proof that every possible browser helper exited. Process-lifetime RSS values are not renderer-tree peak memory or an enforced memory quota.

## Scope, count and proof interpretation

The registered and saved case is `tree-t0-n1000-a`, N=1000, seed 2026101741, stage `tree-t0-n1000-a-step0-k1`, with one captured first projected t0 state. The source-bound initializer was used once, with one controller update, one projection/evaluation stage and fixed F, H0, H order. There are zero integration steps, zero safety-continuation stages and zero fresh reference calls. Initializer/seed identity is established through the reviewed source and recorded provenance; this review does not independently replay the random stream.

The actual journal has exactly **22 contiguous rows**, in the required order: source, factories, twelve wiring controls, initial, controller, F/H0/H native records, stage, case-summary and driver-summary. There is no failure, driver-failure, step, endpoint, safety or reference row. The browser's kind counts and returned runtime counts agree with the journal. The single case reports completedSteps=0, completedStates=1 and derivativeRecords=1000.

The independent saved-evidence checker reports **1000 primary projections/drone rows and 17,000 derivative words**, one stage, zero steps and zero native references. Twelve wiring controls and fourteen arithmetic fixtures all pass. The six successful wiring derivatives are kept separate: totals including those fixtures are 1006 projections/drone rows and 17,102 derivative words, while the primary count remains 1000/17,000. Those fixtures do not supply additional N1000 scenes or independent high-precision load references.

The checker source requires full native-word agreement, actual H-load consumption, exact raw/projected/command bindings and the complete compact-tree certificate after independently reconstructed layout. The saved successful report states those gates passed. Its H0 and H layout subreports each cover all 1000 receivers; those subreports alone concern representation reconstruction, while the separate work/certificate fields carry the geometry omission proof. No sample-only claim is substituted for complete coverage.

For F and H0, the reported directed nonself pair count is **999,000**, with no omissions. For H, **627,164** such pairs remain and **371,836** are omitted, with **15,224 culls**. The identity 627,164 + 371,836 = 1000×999 holds. The omitted fraction is **37.2208208%**. H's layout gathered count is **628,164**, including 1000 self entries; subtracting them yields 627,164 nonself pairs. H0's layout gathered count is 1,000,000 including self, consistent with 999,000 nonself pairs. Thus the layout and work counts refer to different, reconcilable domains rather than contradictory counts.

H's gathered encodings are 962 bitmaps and 38 runs, totaling 1000 receivers; H0 has 1000 run encodings. The qualified layout is a full evidence representation, not a geometric approximation. Its exact reconstruction and tree certificate qualify this captured state's omission coverage, not a universal scene distribution.

The important claim boundaries remain explicit in the saved report: highPrecisionAccuracyValidated=false, controllerFullyRecomputed=false, rkEndpointValidated=false and freshReferenceCalls=0. Full agreement among F/H0/H can retain a common arithmetic/model error. Prior coupled64 high-precision qualification is pinned provenance and cannot become a fresh N1000 accuracy result. Controller checks bind saved state, IDs, commands and elementary targets without independently rebuilding neighborhood membership, steering, desired attitude or complete command law. Literal source/state/load words compare exactly; inherited rational derivative checks identify both zero signs numerically. No physical experiment, stable flight, collision avoidance, trajectory accuracy or long-horizon behavior was established.

## Timing accounting and performance limits

Reported query times are **F 62.9 ms, H0 141.4 ms and H 114.6 ms**, one observation each in the fixed F/H0/H order. The query boundary includes the common per-method input decoding/copying and normal native load/ID/status consumption, including each method's native tree/capture work where applicable. Native evidence encoding, layout work, semantic comparison and persistence follow that boundary and are separately measured.

| Recorded phase, ms | F | H0 | H |
| --- | ---: | ---: | ---: |
| Native query | 62.9 | 141.4 | 114.6 |
| Native evidence encoding | 25.5 | 25.9 | 32.5 |
| Layout encoding | 0.0 | 13.2 | 30.9 |
| Layout roundtrip/check | 0.0 | 10.7 | 28.1 |
| Semantic comparison | 0.0 | 22.9 | 21.8 |
| Record append envelope | 297.6 | 206.8 | 244.5 |
| Subtotal of those sequential recorded phases | 386.0 | 420.9 | 472.4 |

These subtotals are accounting summaries of instrumented phases, not standalone algorithm runtimes: common projection/controller work and other driver/browser work remain outside them, and F supplies the first semantic baseline. Across all three methods, query time sums to 318.9 ms, evidence encoding 83.9 ms, layout encoding 44.1 ms, layout roundtrip 38.8 ms, semantic comparison 44.7 ms and append envelopes 748.9 ms. Those sequential envelopes sum to 1,279.3 ms.

Within the append envelopes, reported serialization totals 343.8 ms and transfer totals 404.9 ms; persistence totals 269.864214 ms for the three native records. **Persistence overlaps transfer and is not an additional additive phase.** The approximately 0.2 ms difference between summed serialization+transfer and append envelopes is ordinary boundary/rounding overhead. The broader transport persistence total is 1069.122620 ms across all evidence writes and dedup checks; adding it to driver or transfer elapsed time would double-count it.

Common projection/input-evidence/binding-and-derivative times are 4.2/10.4/25.9 ms. Initializer time is 1.9 ms, controller 52.5 ms, wiring envelope 577.9 ms, case envelope 1854.8 ms and diagnostic driver/browser envelope 2479.4 ms. These are nested or differently scoped quantities, not a list to sum into wall time. Node's pre-index envelope is 4673.483291 ms; the outer browser child took 7.834580917 seconds, including broader process/runtime/source/closure overhead. Neither is a browser animation-frame time.

The supervisor reports 0.642821915 seconds for saved validation, 7.834580917 seconds for the browser child and 2.478847208 seconds for the checker. Browser+checker = 10.313428124 seconds. Shared setup/closure overhead is 2.043954084 seconds and includes saved validation; adding saved validation again would double-count it. Pre-final-report elapsed time is 12.357382125 seconds, below 360 seconds, with each child below its own limit. The timestamp excludes the final durable report write and interpreter exit, as the source explicitly states.

The raw observation has H/F query ratio **1.82194**: H took about 82.2% more query time than F here despite skipping 37.22% of candidate pairs. H/H0 is **0.81047**, but even that lower observed query time is not a replicated performance result. Fixed order, one state, one timing per method, warm-up/cache effects and instrumentation prohibit a general speedup or throughput claim. The larger H tree record and evidence phases also prevent treating pair-count reduction as an end-to-end performance reduction. No target FPS, realtime operation, N5000 result or scaling law follows.

## Independent descriptor and storage ledger

All 22 descriptor files were hashed against their journal pins. Their field stream binary lengths agree with descriptor totals, and every referenced chunk's actual byte length and hash agrees with its pin. There are **242 chunk references**, **112 unique shard files**, and exactly **22 descriptors**. The actual record/shard inventory equals the referenced set: no orphan evidence file or missing referenced file was found on this success path. This metadata check does not decode shard values or repeat the transport/layout qualification.

| Ledger | Bytes |
| --- | ---: |
| Unique retained shard bytes | 4,118,155 |
| Descriptor bytes | 86,327 |
| Actual unique retained evidence | **4,204,482** |
| Referenced body bytes before sharing | 6,959,587 |
| Cold actual evidence, including descriptors | **7,045,914** |
| Bytes avoided by exact sharing | 2,841,432 |
| Prospective complete-success cold bound | **137,225,341** |
| Actual cold evidence headroom below that bound | 130,179,427 |
| Unique evidence headroom below 160 MiB cap | 163,567,678 |

The two actual ledgers reconcile the store: newBytes=4,204,482 and deduplicatedBytes=2,841,432. The proper comparison to the no-sharing prospective bound is the **7,045,914-byte cold actual schedule**, not merely the unique stored bytes. Even without any sharing, this particular schedule fits by a large margin. That does not tighten the general 137,225,341-byte proof or justify reducing future evidence retention.

Individual native bodies are F 1,344,148 bytes, H0 1,463,217 bytes and H 1,864,358 bytes. Their coefficient streams are 196,311 bytes each, far below the proof's pessimistic 40,016,071-byte per-call coefficient allowance. H0's tree stream is 119,068 bytes and H's is 520,210 bytes, each below the 2,367,735-byte tree allowance. The complete derivative-stage body is 1,406,061 bytes, below its 1,469,588-byte bound. The 86,327 actual descriptor bytes are below the 1,086,976-byte descriptor allowance. These are actual data-dependent sizes under unchanged guards; no scientific sparsity assumption was retroactively substituted into the cold admission.

At the review observation, the scientific results directory contains **139 files and 4,237,290 bytes**: evidence 4,204,482; downstream summaries/journal 30,072; final run-attempt 2,736. Its largest file is 1,023,005 bytes, below both the 1 MiB shard ceiling and 32 MiB general ceiling. No public-result symlink was used.

The exact owned private-directory identity matches the attempt. A read-only lstat walk, without following symlinks or publishing any private path/body, found **200 private leaf files totaling 8,788,343 bytes**, zero symlinks and a largest file of 4,202,496 bytes. The three stage logs are empty and match their recorded zero-byte SHA pins. Final public+private bytes are **13,025,633**. This is **704 bytes above** the supervisor's 13,024,929-byte pre-final ledger; the final durable attempt write occurs after that ledger and the report explicitly excludes it from the earlier snapshot. The difference is not forced to zero or treated as missing evidence. With the additional 2 MiB closure reservation, 253,312,671 bytes remain below the 256 MiB cap.

The public/private figures describe the scientific attempt at inspection, not later review/viewer/export artifacts outside that results directory. They are logical byte counts, not filesystem allocation blocks, heap usage or physical memory. At closure, the complete 139-file public result snapshot SHA still matched the initial review snapshot, and all execution-manifest pins still matched.

## Preserved failure policy and allowed next inference

This attempt completed without a failure record or orphan shard. That observed success does not alter the registered rule for failed, refused, slow, malformed or storage-limited attempts: preserve every complete/partial output and orphan, record terminal failure, and do not retry, replace the seed, change source, raise caps or claim missing evidence as a pass. The prior failed larger browser probe remains a failure; this smaller registered single-state success does not retroactively rescue it. Arbitrary malformed failure snapshots are still outside the complete-success storage guarantee.

The defensible result statement is: **For this source-bound first projected N1000 state, the saved independent checker accepted complete F/H0/H native-word agreement, complete exact tree omission coverage and every delivered-load derivative row; the sole attempt completed within its fixed resource allocations.** This statement must travel with the stated accuracy/controller/trajectory/performance limits.

Within the separately declared post-run allocation, saved-evidence inspection and an actual-saved-state viewer may improve reviewability. A viewer is not additional scientific evidence and must not regenerate a scene or imply a trajectory. Any further scientific question needs a separately specified prospective protocol and authorization; the observed success supplies neither another attempt nor automatic permission to scale to N5000, integrate forward, add a reference or tune the seed. A future performance study would need its own fixed cases, repetitions and order policy before exposure; this review does not execute or authorize one.

## Reviewed report pins

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/run-attempt.json` | 2736 | `7b7c70d4503d2cc7af0c18c590b8d9a9577e76f5a656e0cd7fae81437bab2464` |
| `results/browser.json` | 13328 | `e30ba9765da753d39ad2b99d0ee8b8e25c561b1a3cff81f8660f18cc30b674f0` |
| `results/check.json` | 6326 | `b1a7d6144c24f25c7e6cc13e1a6617092da65310c797f8728d8eda2ff8626619` |
| `results/saved-validation.json` | 2483 | `64c78543054c3ab82439564c09095a35b3989bf49c652fca46c3416496d90cc4` |
| `results/browser-journal.jsonl` | 7935 | `c361dd403c87058ffa04f3f42be296eb1496d5f2b596fee6a1c10acab741ecf3` |
| `EXTERNAL-EXIT.json` | 465 | `030069a13fb5a9f12e3ac186d6de98e397d1726b1d11c0c5aeab17f3ffd99586` |
| `source-publication.json` | 875 | `f8bc85a50656ef72be9653bbe803929b01b6a19c343de1d8efc1fd35c0b84e15` |
| `source-manifest.json` | 397744 | `e4a21305b0f6a228dcbcecee0c4672ec427a379ec491942ee9d272d983be8e3c` |
| `review/RESULT-INSPECTION-PROTOCOL.md` | 1513 | `503be9258ba147d1d3bd3900d112e710d2d6adf7710df5dae9b653f59198b655` |

Public scientific-result inventory snapshot SHA-256: `34a1cee5a6f7c8b333f6d9a6b4ee720a9b45f0443f33182b76f7babab4fbfc43` (canonical JSON list of sorted path/bytes/SHA pins).

Review closed UTC: 2026-10-17T05:23:07.904445+00:00.
