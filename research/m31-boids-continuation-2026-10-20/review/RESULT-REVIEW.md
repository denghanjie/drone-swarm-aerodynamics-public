# Independent saved-result review

20 October 2026. Checkpoint: `research/m31-boids-continuation-2026-10-20`. This review follows the closed storage, native, saved-evidence audit and display allocations.

**Disposition: the saved evidence supports the reported finite continuation result and its stated limitations. No substantive result-reporting blocker was found. Final manifest coverage, publication and a separate exact-public verification receipt remain required; this document does not declare publication complete.**

Both first-seed paths stopped on the recorded drone 17 floor/vehicle condition; both second-seed paths completed the planned horizon. Every attempted native stage was admitted. The distinction between a passing evidence audit, two completed paths and two model-event stops is preserved in the report.

## Review activity and boundaries

The reviewer read the retained source, receipts, index, audit/export, inspection excerpts, result documents and both screenshots. Independent byte verification streamed all ordered physical parts, checked every compressed part and aggregate identity, decoded the gzip members without materializing a duplicate journal, and checked raw aggregate identities and JSON-line counts. It parsed only the initial and terminal records needed for the provenance/outcome checks and the exact final safety excerpts.

This review did not run the producer, synthetic storage fixtures, auditor, finalizer, UI checks or an archive allocation. It did not import scientific modules, make a native query, initialize a path or recompute controller, native-root, projection, derivative, RK or contact arithmetic. The full scientific arithmetic verdict remains the result of the single closed saved-evidence audit. Byte decoding and comparison of existing artifacts did not reopen that allocation.

Only this review document was written by the reviewer. All frozen sources and prior review documents were preserved.

## Source and prior-state binding

The executed source commit is `e9d1d09d83b31c7d346473165a4e112061aae933`. Its source manifest is 10,389 bytes with SHA-256 `eb9865cb485c13b32843108f37016ad7723d0c04c23be3c8830c362e5141d963`. All 51 pinned current local files still match their byte lengths, SHA-256 values and exact Git blobs at that commit. The source-publication receipt names that same commit/manifest, 51 verified pins and both successful public/local and committed/local byte comparisons.

The source receipt records verification at `2026-10-20T12:06:54.816205+00:00`; the producer launch records `2026-10-20T12:08:25.283Z`. The source gate therefore precedes the recorded producer launch. This reviewer checked the retained receipt and committed bytes rather than making another network request.

The saved audit binds the same source commit and manifest, the producer index, native supervisor/exit and storage qualification/supervisor receipts. The viewer export and final viewer pins bind to that audit and its exact `viewerPin`. No repinning of changed data was found.

The prior checkpoint remains result commit `637c25294f162bea39970d12df0206f25dead889`, with the fixed 20,563-byte result manifest and retained publication receipt. The seven selected prior index/audit/internal-exit/supervisor/allocation-closure files still match the source manifest, their prior manifest pins and the new audit's recorded prior evidence.

Independent decoding of each new journal's first JSON line showed exact equality of its complete initial input object to the corresponding prior case's `finalInput`. This comparison covers all 64 IDs and all 17 saved word strings, including signed-zero representation. Each resolution retained its own prior endpoint. No reset, new initialization or replayed first second is represented by these records.

## Closed allocations and caps

All four supervisor receipts have return code zero, no timeout, `allocationWallPassed: true` and `outputCapPassed: true`. All four permanent supervisor launch locks remain present. The closure ledger agrees with those receipts and records one attempt per phase.

| Phase | External measured seconds | Actual saved bytes | Declared success limit / cap |
| --- | ---: | ---: | --- |
| Storage qualification | 0.558167916 | 1,020,490 | 20 s / 8 MiB |
| Native producer | 228.95165370799998 | 1,884,403,390 | 1,200 s / 3 GiB |
| Saved-evidence audit | 264.926575834 | 17,988,885 | 1,200 s / 64 MiB |
| Display | 6.308155708 | 369,238 | 150 s / 16 MiB |

The byte totals were independently counted from each phase's directory and agree exactly with the supervisor receipts. The producer and audit internal exits are closed with exit code zero and remain below their internal wall limits. The producer index is complete without a failure field; no late audit failure file exists. The storage receipt passes seven checks and records zero scientific calls. The UI receipt passes seven groups with an empty error list.

These times are allocation-wall evidence, not a performance benchmark. No speedup, throughput comparison or scaling result follows.

## Outcomes and retained stopping evidence

| Case | Completed additional steps | Attempted native stages | Additional nominal time | Original nominal time | Outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| Seed 2026102001, h=0.005 | 724 | 2,896 | 3.6200 s | 4.6200 s | Recorded endpoint floor/vehicle stop |
| Seed 2026102001, h=0.0025 | 1,447 | 5,788 | 3.6175 s | 4.6175 s | Recorded endpoint floor/vehicle stop |
| Seed 2026102002, h=0.005 | 800 | 3,200 | 4.0000 s | 5.0000 s | Planned horizon completed |
| Seed 2026102002, h=0.0025 | 1,600 | 6,400 | 4.0000 s | 5.0000 s | Planned horizon completed |

Each decoded case-end record exactly matches its index entry apart from the separate journal descriptor. The initial/final viewer positions also match direct decoding of the corresponding prior/index state words. Frame counts equal completed steps plus the initial frame. Only the two stopped cases have a final `safetyPassed: false` endpoint; all four `refusedFrame` values are null.

The two inspection excerpts were independently compared byte for byte with the actual penultimate JSON lines of their decoded logical journals:

- Coarse first-seed journal: sequence 4706, safety step index 723, `pass: false`. Its issues are `vehicle-model-limit` for ID 17 and `obstacle-contact` for ID 17 with hit ID `floor` and saved clearance `-0.0002548790621844238`.
- Fine first-seed journal: sequence 9044, safety step index 1446, `pass: false`. Its issues are `vehicle-model-limit` for ID 17 and `obstacle-contact` for ID 17 with hit ID `floor` and saved clearance `-0.00006486042203775189`.

Neither excerpt lists a drone-to-drone contact or another drone. Their saved sequence numbers, quote hashes and logical compressed-source hashes agree with `inspection/provenance.json`. The terminal safety records for the two completed second-seed cases have `pass: true` and empty issue lists.

These exact excerpts support the report's floor/vehicle classification. They remain outputs of the inherited endpoint and swept-geometry checks. This review did not independently reconstruct the contact geometry, locate a continuous-time impact, or establish real-world collision. The 0.0025-second difference between nominal stopping times is not an event-location error bound.

The completed endpoint is retained when the safety check stops a path. It receives no separate native query. All-stage native admission therefore does not certify the final endpoint, safe flight, altitude holding or physical acceptability.

## Archive and record integrity

The results directory contains exactly the expected 57 physical parts and three metadata files: launch, index and exit. No duplicate whole gzip journal or unexpected result file was found. Every part is at most 32 MiB, with the prescribed ordered name and contiguous offset. Every part's local size/hash and each concatenated compressed stream's size/hash match the index and audit descriptors.

| Logical journal | Parts | Compressed bytes | Decoded raw bytes | JSON lines |
| --- | ---: | ---: | ---: | ---: |
| `seed2026102001-h005.jsonl.gz` | 9 | 301,820,074 | 952,573,498 | 4,708 |
| `seed2026102001-h0025.jsonl.gz` | 18 | 593,355,356 | 1,884,028,603 | 9,046 |
| `seed2026102002-h005.jsonl.gz` | 10 | 333,342,499 | 1,051,955,591 | 5,202 |
| `seed2026102002-h0025.jsonl.gz` | 20 | 655,785,205 | 2,082,014,353 | 10,002 |
| **Total** | **57** | **1,884,303,134** | **5,970,572,045** | **28,958** |

All four raw aggregate SHA-256 values also matched after independent byte decoding through complete gzip-member termination. Part boundaries were treated only as physical storage boundaries. No rounding, new serialization or reconstruction file was introduced.

The aggregate compressed identities are:

| Case | SHA-256 |
| --- | --- |
| First seed, h=0.005 | `144901137feacc02e02409c97d8500f5b0ea82e03f3ef9c394bb123c3ab2ef04` |
| First seed, h=0.0025 | `e77fe7abb170257259e9d3c721f7645cf2c79c7547c1c29673c24ac86e6acf44` |
| Second seed, h=0.005 | `3db3612b0d5acdc2cf822143d49f523ae1ab0dfb985bea5c5921ccfa099d27a1` |
| Second seed, h=0.0025 | `65fa83d316b9e8b24cddbbced2d3fefe114a232c0edcb8574126966c06ba3aee` |

The aggregate raw identities are:

| Case | SHA-256 |
| --- | --- |
| First seed, h=0.005 | `1fc4cba5a13fe24c3ea08e91c1b5589daceea582685343d9346787c0ed427e27` |
| First seed, h=0.0025 | `ec575521ec157523406c32f1ea8009504a45dc18b8404fce0734d27ad448667e` |
| Second seed, h=0.005 | `c29cb9495ff66fd67325d49c31a83aec915c1acaf542b0012a9e6ad5d26036f2` |
| Second seed, h=0.0025 | `960faa54fc1c79d261661403b7a3e1e3ba4d0651ad9e517589a898ef3573a4fb` |

## Saved-audit result and limits

The passing audit reports:

- 28,958 records, 1,524 controller records, 4,571 completed steps and 4,571 safety records.
- 18,284 attempted and successful native stages, zero refused native stages.
- 1,170,176 derivative rows and separately 1,170,176 native-load rows; 1,462,720 projection rows.
- 8,502,060 square-root comparisons, zero observed one-ULP differences and no refused-stage projection-norm reconstruction.
- Four prescribed cases, two horizon completions, two stops and two unsafe completed endpoints.

The index totals, case totals and export counts agree. The report correctly separates `evidenceIntegrityPassed: true`, `allAttemptedNativeStagesAdmitted: true` and `allPrescribedPathsCompleted: false`.

The audit's pass is confined to its frozen binary64 consistency contract. The controller law, neighbor membership, native geometry coefficients, native root solve, residual model and contact geometry were not independently regenerated. Zero observed one-ULP differences does not prove correctly rounded exact-rational square roots or cross-runtime identity. Neither the native source nor the passing arithmetic audit establishes physical truth.

## Quantitative reporting

The reported additional descent agrees with the saved prospective descriptors. The four mean vertical displacements, in case order, are:

`-1.75066387049894`, `-1.7499223181511687`, `-1.8406125707607988`, and `-1.8406125218278118` metres.

They begin at each saved one-second endpoint. The summary's approximately 1.75 m and 1.84 m downward changes are appropriate. They are not total displacements from original initialization and do not isolate steering, control, motor response or aerodynamic causation.

Each stopped path records 362 controller updates, 23,168 vehicle-command records, zero saved saturation flags, 361 directed-neighbor set comparisons, 666 additions and 956 removals. Directed neighbor count changes from 1,740 to 1,450. Each completed path records 400 updates, 25,600 command records, four saturation flags, 399 set comparisons, 724 additions and 900 removals; its directed count changes from 1,582 to 1,406. The changes balance the starting and final counts.

Those neighbor values count repeated directed events between successive saved controller updates, not unique pairs, within-step changes or aerodynamic positive-edge turnover. The saturation values are recorded flags, not a physical actuator-limit assessment or integrated saturation duration. Their small values do not rule out a controller or model limitation.

The saved completed-endpoint body-axis z minima are approximately 0.93178791, 0.93178801, 0.93658778 and 0.93658616 in case order. They remain the declared numerical orientation descriptor, without angle conversion or a safety threshold.

The common-endpoint center differences reported by the saved audit are:

| Seed | Matched endpoint count including start | Common additional nominal horizon | Maximum center difference | Inherited initial maximum |
| --- | ---: | ---: | ---: | ---: |
| 2026102001 | 724 | 3.615 s | `1.436658218234768e-5` m | `2.6729588264384066e-7` m |
| 2026102002 | 801 | 4.000 s | `7.790500784454056e-6` m | `3.4806844784153284e-7` m |

The first pair's comparison ends before either terminal stopping endpoint because their terminal step times do not form a common coarse/fine endpoint. The summary appropriately uses the common prefix and includes inherited initial differences. These values do not establish a convergence order, true trajectory-error bound, physical accuracy or timestep-independent contact time.

## Display review

The audit export is 17,965,977 bytes and contains 725, 1,448, 801 and 1,601 initial/completed endpoint frames, respectively: 4,575 total. Its SHA-256 is `9fb85d0569c69acfaf5dd0eb810b74262e2bd473d0c3985e49ae593473bfa6f1`. The audit's viewer pin, finalizer output and locally rehashed export agree exactly.

The closed UI record reports all 4,575 saved position-buffer checks, four outcome rows, playback, orbit/reset, desktop/mobile overflow checks, corrupted-export refusal and absence of page/console/HTTP errors. The check uses float32 position-buffer conversion, not GPU pixel readback. No native-refused trial occurred, so that branch was not empirically exercised; both unsafe-endpoint cases did exercise the stopped-endpoint labels.

The reviewer independently inspected `ui/desktop.png` and `ui/mobile.png`. Both visibly show two of four paths completed, the selected first-seed stopped path, its 724 completed steps and 2,896 attempted stages, the retained unsafe endpoint, and the explanation that displayed time is continuation-relative. The physical-model limitation is prominent. Text, controls and the four-row outcome table are readable without visible page clipping.

The recorded dots and trails are visible but small at default zoom. The images contain no drawn floor/factory geometry, individual ID labels or highlighted drone 17. The page alone cannot support the floor classification; the exact journal excerpts do. These limitations are accurately disclosed in `SUMMARY.md` and `UI-QA.md`. No visual repair or additional display run is required to preserve the present result.

The reviewer did not reopen the page, repeat UI actions or independently repeat the parent's process-absence/HTTP check. Those claims are explicitly attributed to the parent in the QA document and accompanied by the closed supervisor evidence.

## Reporting, privacy and publication

The summary and claim ledger retain all four cases, the distinction between model admission and stopped motion, the inherited initial discrepancies and the absence of an isolated descent cause. They do not claim controller defect, aerodynamic causation, physical validity, safe flight, novel flocking, speedup, large-swarm scalability or completion of the overall research goal.

The proposed next question is observational tracing of saved vertical steering, targets, loads and motion before any parameter change. The restart documents do not open a new numerical allocation and correctly require a separately specified intervention for causal claims. The global restart diff adds a new 12-line entry without deleting or changing its historical entries.

Both independently inspected screenshots show only the research page, without unrelated application content or visible personal material. A scoped scan of 55 current text files found no personal absolute-path strings, private-key headers or common credential-token patterns. Compressed bytes and image pixels were not treated as text. This is a limited privacy review, not an exhaustive secret-detection guarantee; the final staged package still needs the publication-stage inspection.

Publishing the unchanged raw parts in explicitly incomplete batches of at most 448 MiB is a transport/packaging choice and does not require rerunning science. Intermediate batch commits must not be represented as the complete result. The final result manifest must cover all 57 parts, metadata, gates, locks, storage fixtures, audit/export, viewer pins, screenshots, exact inspection excerpts/provenance, current reporting and restart documents, and this review, alongside the required frozen source/provenance files. The final publication receipt belongs outside that immutable manifest to avoid self-reference.

At this review boundary no final result manifest existed. Local integrity and reporting are accepted subject to independent final manifest coverage/hash verification, successful publication, and a separate exact-commit public-manifest receipt. A publication interruption must preserve the existing bytes and closed allocations; it is not grounds to repeat numerical work.

## Selected reviewed artifact identities

Paths are relative to this checkpoint. Full per-part identities remain in the verified index and audit. These selected hashes identify the artifacts assessed here before adding this review.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/index.json` | 99576 | `6e9b86ece5b9896b67d56070bbddfe8fc7339a026d3703272910357c55d64d0b` |
| `audit/audit.json` | 22542 | `0b6b609f91de107ff5b53ab80a3ab3c69095bec2e3fb77474e1cac7c665bce3c` |
| `audit/viewer-data.json` | 17965977 | `9fb85d0569c69acfaf5dd0eb810b74262e2bd473d0c3985e49ae593473bfa6f1` |
| `viewer/pins.json` | 612 | `88f648f488b099b6cc7a75662f39ffe38b4ce5cc17de7c40cc1f33e1c9089915` |
| `inspection/provenance.json` | 951 | `815b31fb544cb7f0398792107b800e20cc6aac48e04378630eb4c613eb412dfb` |
| `inspection/seed2026102001-h005-last-safety.json` | 217 | `7beacd2de41aa6cd12bce68108aa0d86cfa2251c38b4c05e7c6d71c0c5e5388d` |
| `inspection/seed2026102001-h0025-last-safety.json` | 219 | `a91e8e28fd87c1c56c0926ef557d08e47c2bed95207b2c1cb3bc07f88e641078` |
| `ui/qa.json` | 489 | `58e5b02eec0412d26b8673c2f5f6c4c008e305b4efb2a48a547c6eb855bfa3ff` |
| `ui/desktop.png` | 187126 | `c23b3590bc40bc95c49058c221b1061152ea459a3f12b2f78c55561f6980fcaa` |
| `ui/mobile.png` | 181555 | `f98cb228f6d056abae5640cf0b9d16ac6e7607e81a77b0d3b5827c0ec87c4de3` |
| `ALLOCATION-CLOSURE.json` | 857 | `1285e89cb73f2cebe737807239ee3542a5c2246cfe68c26fd3f625455016ff69` |
| `SUMMARY.md` | 5206 | `09907df48a6b2ec77f44994f3eeb6acd77cd12cfd8db55fb377f2bcef41832be` |
| `RESULT-CLAIMS.md` | 1923 | `d538dd0d8610b7a4a1236d0458d38dfafcd8631c9fd02d3839c03b88b54cf612` |
| `UI-QA.md` | 1253 | `d554b82ca538c5d818366961975f17cb4bbb6ee687e17ff2a481fc6d0adac4e4` |
| `PRIVACY-RESULT.md` | 980 | `2ac6140a5874611f745b1715114ed5d79a28dbacfa1380b341af5bf472bfd9ec` |
| `RESTART-RESULT.md` | 2588 | `d3f6e1f345c8cec2f2cdf82e32399c281e7645c996fd620227910440129bea51` |

The accepted result is limited and concrete: the native calculation admitted all prescribed attempted stages along this additional interval, while one of the two exposed starting configurations reached the recorded floor/vehicle limit at both tested resolutions. Preserve that limitation and every closed allocation when proceeding to publication or a separately defined next question.
