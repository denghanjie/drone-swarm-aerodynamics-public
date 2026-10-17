# Source-only cross-review: one N1000 projected state

Review conclusion: **no source integration blocker found in the reviewed revision**. This is a source and metadata review, not an execution result or authorization. The fresh state, initializer, native methods, layout codecs, browser, scientific checker and high-precision reference were not run by this reviewer. The review used text reads, ordinary file hashes, JSON metadata parsing and AST extraction of literal pin data. No old package was modified and no new results directory was created.

Reviewer: `m31_protocol_challenge`, independently reviewing the parent-owned supervisor/controller/metadata gate and auditor-owned support/check interface. This reviewer also authored the browser producer; producer details below therefore establish integration agreement, not a second independent implementation review of that producer.

## Disabled state and supervision

The inspected `config.json` has `executionAllowed:false`, `authorization:null` and `launchCutoffUtc:null`. `science-config.json` identifies a disabled source draft. `run.py` reads configuration and calls its authorization gate before creating the results directory or spawning any child. Controller, group runner, metadata validator and checker support each independently reject the current disabled configuration. No bypass, retry, cap increase or fallback launch was found.

The registered stage order is browser then check; metadata-only saved-validation precedes browser within the shared overhead budget. The exact reservation is 360 seconds: 120 seconds browser, 180 seconds check and 60 seconds setup/closure, with the 15-second saved-validation allocation charged to shared overhead. The supervisor rejects less than the full reservation, uses fixed stage source paths, launches Python in isolated/no-bytecode mode and binds all children to the live attempt token. The checker now additionally requires the attempt's exact browser/check order and exactly saved-validation/browser/check stage keys.

The controller launches exactly one pinned Chrome root/profile, captures root exit and close listeners before Playwright can resolve launch, and requires successful root closure for completion. The group guardian remains unreaped until release, allowing failure cleanup to target the owned group. These source conditions support the stated root-only closure boundary; they do not establish that every helper exited or provide a memory cap. No operational closure occurred in this source review.

Logical output limits agree across supervisor, store and checker support: 32 MiB general file limit, 256 MiB combined allowance, 160 MiB evidence, 64 MiB private output, 30 MiB remaining public output and 2 MiB finalization reservation. Successful evidence is sharded; this does not authorize larger per-file payloads. Terminal failure may retain an incomplete prefix, as explicitly stated by the storage admission. Controller errors, deadline failures and failed children remain terminal; no complete successful report is accepted for them.

## Single-state contract and exact records

Science configuration, browser driver and checker agree on the sole case `tree-t0-n1000-a`, N=1000, seed 2026101741 and one fixed method order F, H0, H. The unchanged initializer is called once. The driver captures the original state and controller commands, projects that same state once and requests one complete derivative stage. The primary stage is `tree-t0-n1000-a-step0-k1`; original time, relative time and dt are the positive-zero words. Integration duration and steps are zero. The adapter no longer exposes an RK step, and the driver has no endpoint or safety continuation.

The successful journal contract is exactly:

| Sequence | Record kind | Count |
| --- | --- | ---: |
| 0 | source | 1 |
| 1 | factories | 1 |
| 2–13 | wiring-control | 12 |
| 14 | initial | 1 |
| 15 | controller | 1 |
| 16–18 | native, in F/H0/H order | 3 |
| 19 | stage | 1 |
| 20 | case-summary | 1 |
| 21 | driver-summary | 1 |

The checker requires this exact 22-kind sequence, the same eight runtime counts and a single case summary with completedSteps=0, completedStates=1, derivativeRecords=1000 and the matching stage ID. It rejects an invented final endpoint. Initial/controller/native/stage and summary schema names retained by the producer agree with checker expectations. The controller's enclosing browser report uses the new state1000 schema expected by support.closed_browser.

Initial finite state words and IDs 0–999 are bound to the controller input and stage rawBeforeProjection. Saved commands are bound to the stage commands and derivative rows. Native records bind case/stage/order and the common input hash, and nativeRefs bind their actual persisted pins. The saved-word derivative audit counts exactly 1000 primary drone rows and 17,000 derivative words. The twelve unchanged wiring groups add exactly six accepted one-drone rows, producing totals of 1006 projections/drone rows and 17,102 derivative words; they do not increase primary stage/reference counts. Fourteen inherited arithmetic fixtures remain disclosed pure checker controls.

## Layout, timings and native evidence

The adapter's qualified layout import is top-level. The checker startup factory order places layout immediately after browser-adapter and before physics, matching the resulting first-execution order. Browser and builder list the same 19 source modules. Source-event pin/offset checks bind original module bytes to actual bundle slices before factory execution; the checker requires the complete allowlist and exact observed factory order.

The original native query and native.encodeEvidence boundaries are retained. Only a present tree field is replaced by the qualified column representation; all original non-tree fields are retained. The producer reconstructs and compares the old compact tree before semantic comparison. F has no tree field and zero layout costs. Query timing remains the original query/copy/consumption boundary and does not acquire codec or persistence work.

The native record's exact five auditTiming keys agree with the stage query timing projection: queryWallMs, encodeWallMs, semanticCompareWallMs, layoutEncodeWallMs and layoutRoundtripWallMs. Append, serialization, transfer and persistence times are separately recorded and journal-bound. The checker requires finite nonnegative values and explicitly requires both F layout times to be zero. The driver-stage and native-stage timing bindings agree; no speed gate is present.

The independent checker expands the qualified column layout using the frozen Python helper, restores canonical gathered runs/literals and ordered culls, compares representation structure and then separately applies the raw-state-derived full compact certificate. The layout-qualified subreport is explicitly representation-only. Reconstruction does not replace the independent tree/coverage proof. Full F/H0/H native payload comparison excludes only registered method/tree/timing/metadata and method-dependent work counters; original retained non-tree arrays and words are checked completely. H's delivered load words bind the derivative consumption.

## Imports, references and helper interfaces

No high-precision reference stage exists in run.py/config, and validate-saved.py uses only standard-library file/metadata operations. The checker's freshReferenceCalls remains zero. Its call path invokes frozen transport decoding, layout comparison, compact-tree certificates, native shape/consumption checks, delivered-word derivative arithmetic, wiring checks and tiny arithmetic fixtures. It does not invoke StageAudit's reference-check or RK-step methods, an initializer, controller regeneration, native query or a prior checkpoint's CLI/main.

The six frozen Python helper files were inspected for their import/top-level patterns and rehashed against support.MODULES. Their guarded CLI bodies are not invoked by support.module. Ordinary constants, regular expressions and rational constants created at import are not hidden scene/reference execution. The bundled reference-excerpt.cjs provides the inherited ordinary binary64 pair-term functions; its filename does not introduce a high-precision oracle stage.

The old compact Resolver correctly takes all current record/shard paths from support.PACKAGE rather than a frozen old package path. The new support supplies its required pin readers, guard, schema/shape validators and canonicalization methods. The old StageAudit constructor obtains native_check and coverage_check through the same fixed module gate; the new main calls only its applicable saved-word arithmetic interface. No unresolved support interface was found.

## Metadata and publication boundary

The metadata-only prerequisite validator checks exactly coupled64, native-tree42 and saved-layout156. It requires their three root pins, successful prior check/attempt status, matching prior source identities and inclusion of each prior result-manifest closure in the new source manifest. All new manifest pins are hashed before and after validation. The final metadata-validator addition also requires at least fifteen admission source pins, checks each exact pin against the execution manifest and rehashes its actual bytes; the current admission has fifteen such source pins plus its proof pin, so this interface matches. The checker binds this completed preflight output and the same prerequisite roots; it additionally fixes the precise prior coupled64/layout results and their limited claim scope.

Read/hash verification in this review matched all six frozen Python helper hashes, the qualified layout.cjs hash, all nine retained prerequisite root pins and all sixteen admission proof/source pins. The three retained reports have complete/passed=true and their attempts have status=completed. These were metadata reads, not qualification reruns. This review did not independently replay or rederive the storage proof. Its admitted cold complete-success bound is 137,225,341 evidence bytes and 237,888,637 combined bytes, with no content-sharing assumption and no complete malformed-failure-capture promise.

At the review's metadata check, no source-manifest.json, source-publication.json, generated browser bundle or results directory existed. Consequently, final whole-manifest completeness, generated bundle slice identity, syntactic checks, actual committed/remote publication equality and any runtime behavior remain parent-owned later gates. The runtime source rechecks publication receipts and source bytes; the receipt's committed/remote equality assertions still require the actual separate publication verification. This review does not claim those pending gates have passed.

The permitted later success language remains conditional native agreement and saved-word derivative correctness for this single state. High-precision N1000 accuracy, complete independent controller correctness, integration/RK endpoint, trajectory, N5000 performance and speedup remain unestablished.

## Reviewed revision pins

The following byte identities record the reviewed revisions. Source edits after these pins require corresponding integration re-review. This review itself is excluded to avoid self-reference.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `config.json` | 1773 | `6deae4af1afd09735041d4280f94824c4ef26f14e3f92628ebc951e9a9dbe0c1` |
| `runtime.json` | 6621 | `c8eedbcd49bf15440d7242b8fbbaa957f1b693dbc01061d5bd2219859e9005f1` |
| `source/science-config.json` | 8365 | `476f0be0d76748087189b07d22a21da4770295f7a5f3d2981971c8362fd2020c` |
| `source/run.py` | 16100 | `57af680d4959f3ef402d625cd66be5441a2263ae08bf34686d461040574f9b5a` |
| `source/group-runner.py` | 3181 | `5b4e22611b30c44e6a4a6026318d51d065855bfb40cd13143f4bdb78fea2c33a` |
| `source/controller.cjs` | 20230 | `5fadb362f8080f2f2bb2bf040929d2b00fa03a6d4ec2050bc06df9067490d3b5` |
| `source/validate-saved.py` | 7496 | `f76d958c608c103c19527f04cb741460dd73a6d2c59f1dbc6231a1db50321d1c` |
| `source/support.py` | 14053 | `3c81ef45abe84193e781b3ed76e36308277e33fb2d8283c36206f238bc34874e` |
| `source/check.py` | 29560 | `9e60651b84f77a93ce274d88480f479613917210e458d44a7ff1ec6159bf8b29` |
| `source/browser-adapter.cjs` | 14856 | `66834f82600caa35d9417baaafc8b3b57276f8a47a4ad25ef8f3aefa0905e990` |
| `source/browser-driver.cjs` | 13837 | `7b70df3a987ade0966320fe759352bfae80e3e0350cab98429497780bce2412d` |
| `source/browser.js` | 16972 | `612a9ea9078cd1d7a3774b509b651bfae4bed9a28126cb48b8ee15a02aeffe6e` |
| `source/build-bundle.py` | 5054 | `92da0840e08d8864ceee18321d55d15b9c1b5507a96233339fa8430ed4e6b9b1` |
| `source/transport-store.cjs` | 3603 | `9c8c47f22f3042367cf024e317d7b12b6ab7533d2e9b24f3e22fdea7154960b8` |
| `prerequisites.json` | 2860 | `9aa9afcc13068d6a7f33d3df391a82d07ca102cd7250380f95f7c2b0701e6536` |
| `review/STORAGE-ADMISSION.json` | 5127 | `ad97fb3ba2d4c3d5d7beee20c23bbc757535149dfdc00644567a4396674818e1` |
| `review/STORAGE-ADMISSION.md` | 15938 | `dc1ea5490de4154d119f009fda0742cdf174048a82fbfdea4297bbb655b7091e` |

Review closed UTC: 2026-10-17T04:55:10.921425+00:00.
