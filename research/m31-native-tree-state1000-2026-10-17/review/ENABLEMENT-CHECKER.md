# Checker enablement review

Reviewed 2026-10-17 following the explicit human renewal recorded in `EXECUTION-AUTHORIZATION.json`. **Disposition: no enablement blocker found in the reviewed revision.** This covers the authorization/configuration delta, unchanged checker/helper/scientific source, retained prerequisite closure, storage-admission bindings and absence of a new scientific result. It is not an execution result or a claim that the later runtime gates have passed.

The reviewer read source and JSON metadata, compared committed blobs, extracted literal helper pins with AST parsing, inventoried files and independently rehashed retained bytes. No scientific source was imported, no codec/checker/control was run, and no initializer, native query, reference or browser was executed. No implementation file was edited. This review writes only `review/ENABLEMENT-CHECKER.md`.

## Effective authorization and preserved draft

The historical disabled draft is commit `75a761f9503334cefe57eab20fa84e5cbf569a12`, with draft manifest SHA-256 `6de7defdbe1a5e84ac99f471fe80e3b9c2ca6a88fcca0faa6f2af38d78774468`. The current `draft-manifest.json` is byte-identical to that commit. Its exact hash is bound by both the effective configuration's `reviewedSourceManifestSha256` and the new authorization record.

`disabled-draft-config.json` is byte-for-byte identical to `config.json` at the disabled commit: 1,773 bytes, SHA-256 `6deae4af1afd09735041d4280f94824c4ef26f14e3f92628ebc951e9a9dbe0c1`. It retains `executionAllowed:false`, null authorization and null cutoff. The historical draft manifest's canonical config pin is verified against this preserved disabled copy, not incorrectly against the newly enabled config.

The only changed top-level canonical configuration fields are `executionAllowed`, `authorization`, `launchCutoffUtc` and descriptive `scope`. The parent corrected the initially stale “Disabled source-only draft” wording in the effective scope during this review. The actual scientific scope, stage paths/order, counts, resources and completion assertions remain identical to the disabled configuration.

The effective window is exactly **2026-10-17 05:15:28–07:15:28 UTC**, two hours, or **13:15:28–15:15:28 Asia/Shanghai**. Its basis is explicitly the first tool-clock observation after the human reply, not an invented message timestamp. Configuration and authorization agree on both times and the reviewed draft hash. The recorded scope is one bounded N1000 test, inspection of its saved evidence and publication of the outcome. It grants one scientific attempt, zero scientific retries and no resumption of the expired overnight automation.

The reservation remains **360 seconds: browser 120, checker 180, shared overhead/closure 60**. Metadata-only saved-validation has fifteen seconds within that overhead. The supervisor checks that the full reservation remains before opening a fresh attempt; all subsequent guards use the same absolute cutoff and inherited monotonic deadlines. The latest wall-clock start compatible with a full reservation is 07:09:28 UTC, subject to the source/publication/private/runtime gates. No active execution guard contains the expired 05:06:20 cutoff; the guards read the effective canonical configuration.

`source/science-config.json` retains its historical `source-only-disabled-draft` status, and preserved draft documentation such as `RESTART.md` retains the older window and disabled-state description. These are immutable provenance. `EXECUTION-PROTOCOL.md` and the effective canonical authorization identify the new window; the historical status string is not an execution gate. There is no basis to silently extend this new cutoff or derive another attempt from an old document.

## Unchanged source and checker interface

All **21 files under `source/`** were compared byte-for-byte with the disabled commit. None changed. This includes the checker, support, science configuration, metadata validator, supervisor/controller, browser producer, transport/layout, bundle builder, generated bundle and bundle metadata. `runtime.json` also remains byte-identical. The changed configuration enables the previously reviewed implementation; it does not substitute another algorithm or relax a checker condition.

The six frozen Python helper pins in `support.MODULES` were extracted as literal metadata and independently rehashed, with no mismatch. The qualified JavaScript layout hash also remains unchanged. The generated bundle's 19 source slices match their complete original bytes, offsets and pinned identities; no bundle factory was evaluated. Prior static syntax checks remain bound to the same source bytes. This review did not rerun source entry points or existing qualification controls.

The unchanged checker still requires exactly 22 journal rows and one case: N=1000, seed 2026101741, t=0, F/H0/H order, `tree-t0-n1000-a-step0-k1`, zero integration duration/steps/dt. It independently reconstructs both column-layout trees before checking complete raw-state-derived tree/cull coverage and compares the complete registered native payloads. It binds actual H delivered-load words to all **1000 primary derivative rows / 17,000 words**. Twelve fixed wiring controls and fourteen arithmetic fixtures remain required; six accepted fixture derivative rows are kept separate from primary coverage.

The checker/support interfaces, publication receipt fields, live token/stage gates, exact attempt stage keys, browser-root completion assertions and output-preservation paths remain those of the reviewed draft. The report continues to limit a success to `conditionalNativeQualified:true`, while `highPrecisionAccuracyValidated`, `controllerFullyRecomputed` and `rkEndpointValidated` remain false, and fresh reference calls remain zero. Controller state/ID/command/elementary-target binding is not relabeled as independent neighbor membership, Boids steering or complete command-law reconstruction.

## Retained prerequisite closure

All **1,597 historical draft file pins**, representing **217,168,968 referenced logical bytes**, were independently rehashed without a mismatch. The canonical historical config was checked through its preserved disabled copy as described above. All other pinned file bytes remain at their recorded paths.

The three retained prerequisite root triplets were rehashed, and every file listed in each prior result manifest was separately rehashed and checked for exact inclusion in the historical draft manifest:

| Prerequisite | Result-manifest file entries | Referenced bytes | Check/attempt binding |
| --- | ---: | ---: | --- |
| `coupled64` | 159 | 56,454,256 | complete/passed; completed attempt; source identities agree |
| `native-tree42` | 186 | 8,359,084 | complete/passed; completed attempt; source identities agree |
| `saved-layout156` | 1,206 | 152,041,225 | complete/passed; completed attempt; source identities agree |

These are manifest-entry counts and byte sums, not additive unique totals across overlapping closures. All nine check/attempt/result-manifest root pins match. `prerequisites.json` is unchanged and orders exactly `coupled64`, `native-tree42`, `saved-layout156`. The metadata validator still requires their exact root bindings and full closure inclusion in the eventual execution manifest, and hashes that manifest's files before and after its work. No prior producer, checker, codec or control was rerun in this review.

The explicit prior coupled64 and saved-layout hashes used by the checker still match their successful retained reports. Prior N64 accuracy/reference evidence remains a named control and is not new N1000 evidence. The saved-layout report retains `scientificValidated:false`; enabling this checkpoint does not alter that older result or rescue the earlier failed browser probe.

## Storage admission and unchanged resources

The storage-admission JSON, proof document and all **fifteen source pins plus the proof pin** were independently rehashed and checked against the historical draft manifest. None differs from the reviewed source. Thus the admission is still bound to the actual code and fixed schedule rather than a stale producer revision.

The retained bound arithmetic reconciles without executing `storage-bound.py`: all body bounds sum to **136,138,365 bytes**; 22 descriptors at 49,408 bytes add **1,086,976**; complete-success evidence is therefore **137,225,341 bytes**, below 160 MiB by **30,546,819 bytes**. Adding the full 64 MiB private, 30 MiB downstream and 2 MiB closure allowances gives **237,888,637 bytes**, below the 256 MiB aggregate by the same margin. No deduplication, expected sparsity, changed seed or reduced two-million-positive-term guard is credited.

This is still the registered `cold-complete-success-evidence-no-sharing` bound. It is not a guarantee that arbitrary malformed failure snapshots fit completely; those paths retain their bounded partial prefix and must fail rather than retry or raise caps. It also does not bound memory, predict completion time, or establish a scientific result. The unchanged hard envelope is 32 MiB per general file, 1 MiB shards, 2 MiB descriptors, 160 MiB evidence, 64 MiB private, 30 MiB downstream and 2 MiB finalization within 256 MiB. Private symlinks are accounted by their own `lstat` bytes without following targets; public-result symlinks remain rejected.

The metadata gate still requires admitted storage and exact proof/source inclusion in the eventual execution manifest. The checker binds the successful metadata-validation report and admission root. Final execution-manifest completeness is a later parent freeze gate; this enablement review does not treat the historical draft manifest as the executable one.

## No new result and pending launch gates

At the review's inventory and hash checks, **no `results/` directory, `source-manifest.json` or `source-publication.json` existed for this checkpoint**. Earlier viewer QA artifacts are preserved display-only evidence; they are not a scientific attempt or new-state output. The available evidence supports an unexposed enabled source revision, not runtime qualification. This statement is scoped to the inspected checkout and retained metadata, not a claim about an authoritative global execution registry.

The parent must still freeze the enabled canonical configuration, authorization/protocol, preserved disabled configuration, all unchanged source/runtime/prerequisite/admission dependencies and enablement reviews into the new execution manifest; commit/publish it; and verify the exact public bytes before the sole launch. A publication receipt must bind the actual enabled-source commit/manifest/path/bytes/pin count and precede attempt creation. Runtime identity, fresh private/profile/result paths, live stage tokens, the remaining full reservation and external supervisor exit observation remain live checks. No publication equality, runtime success or future result is asserted here.

After the attempt, every raw/partial output and external exit must remain preserved. Any later saved-evidence inspection or UI-only validation requires its separately recorded prospective allocation within this same window and may not rerun the scientific calculation. An exposed source defect or negative outcome does not authorize a second scientific attempt.

## Reviewed byte identities

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Effective `config.json` | 2,049 | `53f85429d2a289ef2767ad7dd526fdac58f3bf2e69caa1c2bb6821b988ba4d96` |
| `disabled-draft-config.json` | 1,773 | `6deae4af1afd09735041d4280f94824c4ef26f14e3f92628ebc951e9a9dbe0c1` |
| `EXECUTION-AUTHORIZATION.json` | 925 | `a043801bf2c16d37bdda0d781fb21bfaf5b941ae8d9eef8a033fb2622039ba63` |
| `EXECUTION-PROTOCOL.md` | 1,712 | `98b762497e7b9dfa0f42e1c21a8a9db00b326f2b61b3330b34de6bdfb4eec1d0` |
| `draft-manifest.json` | 395,925 | `6de7defdbe1a5e84ac99f471fe80e3b9c2ca6a88fcca0faa6f2af38d78774468` |
| `prerequisites.json` | 2,860 | `9aa9afcc13068d6a7f33d3df391a82d07ca102cd7250380f95f7c2b0701e6536` |
| `review/STORAGE-ADMISSION.json` | 5,127 | `ad97fb3ba2d4c3d5d7beee20c23bbc757535149dfdc00644567a4396674818e1` |
| `review/STORAGE-ADMISSION.md` | 15,938 | `dc1ea5490de4154d119f009fda0742cdf174048a82fbfdea4297bbb655b7091e` |
| `source/check.py` | 29,560 | `9e60651b84f77a93ce274d88480f479613917210e458d44a7ff1ec6159bf8b29` |
| `source/support.py` | 14,053 | `3c81ef45abe84193e781b3ed76e36308277e33fb2d8283c36206f238bc34874e` |
| `source/science-config.json` | 8,365 | `476f0be0d76748087189b07d22a21da4770295f7a5f3d2981971c8362fd2020c` |
| `source/validate-saved.py` | 7,496 | `f76d958c608c103c19527f04cb741460dd73a6d2c59f1dbc6231a1db50321d1c` |
| `source/run.py` | 16,100 | `57af680d4959f3ef402d625cd66be5441a2263ae08bf34686d461040574f9b5a` |

There is no unresolved source/checker enablement blocker in these reviewed bytes. The uncompleted publication and launch checks are deliberate remaining gates, not a reason to claim execution or verification prematurely.
