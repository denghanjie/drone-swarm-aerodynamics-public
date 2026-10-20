# Independent saved-result review

20 October 2026. Checkpoint: `research/m31-descent-trace-2026-10-20`.

**Disposition: accepted as a bounded observational result, pending final result freeze and exact-public verification.** No result-level blocker was found. All four new allocations are closed and passed; this review opens none. Overall research remains unfinished.

I read the summary, claim ledger, restart/privacy/display notes, availability receipt, source-publication record, extraction and audit reports, all four supervisors, finalizer report, display gates/QA, viewer pins and selected saved result records. I inspected both screenshots. I wrote only this review; I did not rerun extraction, arithmetic, raw-journal scanning, auditing, finalization, browser verification or any model.

## Provenance and artifact binding

The source-publication receipt identifies commit `94ed4a45862a928a3b003afa64d30f6bc35d021c`, verified at `2026-10-20T14:37:19.113064+00:00`. The 129-pin source manifest is 27,609 bytes, SHA-256 `e9daac500d5b3539eda4bbf12628b4fc7a51f5da3234c9336a66cef5c475da83`. Its bytes still match that commit. The receipt records local/committed equality and separate retrieval of the exact-public manifest, not a complete remote journal download.

I rehashed all 54 non-part source-manifest entries, including every reviewed source, protocol, input descriptor, dependency, explanatory source and prior metadata file: all unchanged. The 75 journal parts had already been independently checked before launch and were checked by the successful phase gates; I did not redundantly rescan them here.

The audit binds the following artifacts, whose current lengths and hashes I independently verified:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/trace.jsonl` | 9,431,628 | `d92539aae901fa3f295f8dad403c06b92d98d44faa16d25ef8dbd5537f7bc9e7` |
| `results/view-data.json` | 1,155,978 | `a10ae9124b2d85d5c8017ea3686a34798ae41b031b766f02980c96e2768f46b4` |
| `results/report.json` | 14,670 | `b809748b02e928807d9a4619ddc6aa833c8cb1ade550516fd4326d3bf2cd44a4` |
| `audit/report.json` | 4,086 | `13b0ef0242038f87804aa61ae8a0210fd11a24401c4ba582a8b2213d98972d68` |

Extraction and audit trace/view pins agree. Every viewer pin matches its current artifact. The trace has exactly 1,924 ID-17 rows: 100 per original path and 362/362/400/400 continuation rows. Report, audit and closure counts agree; all eight journal receipts agree between extractor and auditor. The auditor reports four complete 64×17-word boundary checks.

Exported case summaries equal the report; first/last trace metrics equal their reported and exported values. Final endpoint states, status and reasons match the existing continuation index. The independent audit already reselected every controller/k1 pair and checked clocks, same-ID states/commands/loads, descriptors and summaries. Its shared byte/gzip/JSON reader and Python runtime remain disclosed limitations of independence.

## Closed allocations

| Phase | Wall seconds | Output bytes | Status |
| --- | ---: | ---: | --- |
| Extraction | 74.591644833 | 10,602,358 | Closed, passed |
| Audit | 48.096267416 | 4,086 | Closed, passed |
| Finalization | 2.272311250 | 32 | Closed, passed |
| Display | 10.666988041 | 494,959 | Closed, passed |

Each has one retained supervisor launch lock, return code zero, passing wall/output checks and one attempt in the closure record. Measured folder sizes equal supervisor and closure values. Viewer pins add 685 bytes, within their separate 64 KiB allowance. No phase failure file is present. Source publication, extraction, audit, finalization and both display gates report empty byte-read anomaly lists.

`UI-AVAILABILITY.json` separately records the owned browser/process group absent and the existing replay returning HTTP 200 after closure, without another browser launch. This is outside the measured display folder.

## Findings and interpretation

The reported observations match the saved result fields:

| Configuration, both resolutions | Samples | Desired velocity upward | Requested acceleration upward | Upward request with downward delivered acceleration |
| --- | ---: | ---: | ---: | ---: |
| `2026102001` | 462 | 90 | 430 | 207 |
| `2026102002` | 500 | 72 | 491 | 168 |

Initial nominal support is exactly 100% of weight in the saved descriptors. Delivered support is approximately 73.3027% and 71.9693%, with saved vertical accelerations −2.6190 and −2.7498 m/s². Initial vertical velocity is positive; the first sampled downward velocities are at 0.04 and 0.05 seconds. These are controller-grid observations, not exact continuous reversal times.

At the first configuration's last sampled update, approximately 4.61 seconds, desired vertical velocity is +0.250 m/s, actual velocity approximately −0.083 m/s, delivered support approximately 107.9%, and acceleration approximately +0.775 m/s². The saved endpoints are at 4.6200 and 4.6175 seconds, with center heights approximately 0.074745 and 0.074935 metres. Thus the earlier sample shows upward braking while descent persists before the previously established floor/vehicle stops. It does not show that support remained below weight until contact, nor provide a new force evaluation at contact.

The second configuration's last sampled update at 4.99 seconds has actual vertical velocity approximately +0.00926 m/s and delivered support approximately 102.6%; both endpoints reach 5 seconds.

The summary and claim ledger correctly separate desired motion, requested acceleration, command, delayed motor state and delivered model load. Nominal support is a same-state comparison, not a decoupled trajectory. The observations do not identify a unique cause, prove a controller defect or prescribe a successful cure. The paired resolutions and exposed configurations are not independent trials; ID 17 starts at different locations across configurations. No physical validation, safety, novelty or research-completion claim is supported.

## Display and privacy

The saved QA records seven passed groups, including all 5,775 joined endpoint buffers, all 1,924 held samples/timestamps, ID-17 focus, floor, controls, orbit/reset, corrupt-trace refusal and no recorded page/console/HTTP errors. Pre/post display gates passed.

Both screenshots visibly show the floor, highlighted drone and orange descent trail. Endpoint time 4.6200 seconds is distinguished from held sample time 4.6100 seconds. The 107.9% support card and negative velocity are consistent with the reported braking interpretation. Desktop text is clear; mobile cards and wrapped table remain readable. The small mobile chart is qualitative, as documented. Other drones appear as small dots; other factory obstacles are explicitly omitted. The enlarged halo is labeled as a visibility aid.

Screenshot identities:

- `ui/desktop.png`: 257,284 bytes; SHA-256 `341059c6651218f13ebc6ceab7af48cf7bf963f5116824276a1c487e39bfb109`.
- `ui/mobile.png`: 237,134 bytes; SHA-256 `8867db11391df7404201a28afd88f3366980db363c91116dbbffa9c0123a29f1`.

No unrelated private content was visible. The scoped text scan found no private absolute paths, private-key headers or tested common token patterns. This is not a universal secret-detection guarantee.

## Remaining publication and next-work boundary

Freeze and publish the complete result, this review and all closure/availability/privacy evidence; separately verify the exact-public result manifest and record its receipt. That final result-publication identity was not yet available during this review.

The proposed nominal-load intervention remains unexecuted. Before treating it as the next distinct experiment, perform the historical-duplicate check required by `RESTART-RESULT.md`, then establish a separately reviewed bounded protocol and public source freeze. Preserve the existing coupled baseline and all old failures. No new numerical allocation, tuning, physical claim or repetition is authorized by this result review.
