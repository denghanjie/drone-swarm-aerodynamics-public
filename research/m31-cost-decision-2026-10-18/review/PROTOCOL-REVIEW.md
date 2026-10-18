# Static protocol and source review

Reviewer: `/root/m31_protocol_challenge`. Review closed 2026-10-18T12:06:19Z.

## Disposition

**Accept the pinned scientific source below for the single registered, bounded comparison. No remaining source blocker was found in the final revisions.** Launch remains subject to the protocol's pending source-manifest freeze, public publication and exact public-byte verification. This review does not assert that those gates have occurred, that the experiment has run, or that it has passed.

The authorization is the new 18 October allocation, 2026-10-18T11:57:26Z through 2026-10-18T13:57:26Z. It is not an extension of the consumed 17 October attempt. The comparison is confined to the exact previously saved projected N1000 state and the unmodified published native kernels. No initializer, projection, controller, derivative, integration or new numerical reference is authorized by this review.

This reviewer performed static text inspection, file metadata and SHA256 checks only; the only new file written by this reviewer is this review. The reviewer did not import or execute project modules, invoke a numerical producer or codec, launch a browser, or run tests. The parent separately performed the authorized saved-only export once. The exported files are pinned below; this review is not a second export or a runtime validation of that export.

## Scientific and timing design

The four arms have a coherent purpose: F is the existing screened pair scan; H is the tree with witness capture disabled; HC is the same tree with capture enabled; H0 is the tree with omission disabled and capture disabled. F is not described as a deliberately naive all-rotor evaluation.

The orders are `F H H0 HC`, `H HC F H0`, `HC H0 H F`, and `H0 F HC H`. Four warm blocks produce 16 calls; 24 measured blocks produce 96 calls; four final instrumented diagnostics produce four calls. The maximum is exactly 116, and each measured arm occupies each position six times. Warm and instrumented calls are retained and checked but excluded from the primary statistic. There are no retries, filtered outliers, forced garbage collection or adaptive repetitions.

The primary timer starts before fresh hexadecimal-to-binary64 input decoding and ends after the complete native query and the submitted-input immutability check. It includes the native input, geometry, tree, admission, solve, residual, load and consumption work. Encoding, semantic projection/comparison, transport and persistence occur outside that timer. Native internal phases are secondary measurements. Diagnostic wrappers are installed only after the first 112 calls, wrap `tree.build` and `tree.gather`, are restored in `finally`, and do not enter the primary decision. The gather wrapper combines traversal, sorting and any capture work; it does not separately identify their individual costs.

The decision is fully specified: retain this version for further investigation only when all 116 correctness gates pass, all 24 paired H/F ratios exist, the median paired ratio is at most 0.90, and at least 20 pairs have strict H < F. The even-sample median averages the middle two sorted ratios; ties are not wins. HC/H and H0/F are diagnostic comparisons. The result cannot support a population, different-state, different-size, machine-independent, trajectory, physical-accuracy or browser-frame-rate claim.

## Saved-evidence bridge and retained outputs

The export binds the prior result manifest SHA256 `59be1b771384587262d9925742e7ae9bb865b15b952cb3f2e23ea9d4b075749d`, requires the passed single-stage case `tree-t0-n1000-a`, and pins its F descriptor SHA256 `2c1dacc72cb00ab1685233fd2385518e6df66993bd0175f3e8b3d2f858e50bd9`. It reads saved F raw IDs and state words directly through the frozen saved-data resolver; it does not regenerate or reproject the state. Bytecode writing is suppressed.

The selected semantic keys are `diagnostics`, `status`, `reason`, `constants`, `raw`, `ids`, `prepared`, `coefficients`, `solution`, `loads`, and `consumption`. Scientific diagnostics are retained with exactly four historical exclusions:

- `diagnostics.buildPhasesMs`
- `diagnostics.geometryWork.gatheredNonselfCandidates`
- `diagnostics.screen.orderedPairVisits`
- `diagnostics.screen.componentTests`

The Python side converts exact numeric types `int` and `float` through big-endian binary64 packing while preserving booleans. The browser side converts JavaScript numbers through binary64 DataView bytes. Existing scientific hexadecimal words remain words. Sorted canonical JSON agrees for the keys and data used here, including the saved signed-zero words. All selected keys and successful native status are required. This is an exact semantic equality bridge to previously checked evidence, not an independent physical reference.

Every call sends the complete actual canonical semantic bytes to the host outside timing. The host compares actual bytes with the exported expected bytes and retains a content-addressed actual-output blob; reuse requires exact existing-byte agreement. Each call pins that blob. Independent analysis rereads each referenced blob and checks its hash, byte length and exact equality, rather than trusting only a producer checksum or boolean. Successful calls may share one blob only because their complete canonical bytes are identical.

The repaired failure path catches encoding failure, retains present semantic fields, sends the actual failure body, persists available semantic and failure evidence before terminating, and permits absent timing/diagnostic fields. The failed-call semantic plus additional body budget is 12 MiB. If the additional body exceeds that budget, a body-limit receipt replaces it; no complete-failure-body claim is warranted. An oversized semantic body itself terminates at the bound. Arbitrary throwing or malformed paths do not guarantee full capture. There is no retry after any such failure.

HC measures in-query witness production cost without retaining new witness bodies. The old complete witnesses remain immutable and linked. This experiment does not establish a newly checked tree proof for each timed query.

## Operational controls and analysis gate

The scientific launch wrapper verifies the source-publication gate, manifest digest, remote/local byte-equality result and pinned source files. It patches the child-process spawn boundary before Playwright is loaded, requires exactly one configured Chrome launch and places that Chrome root in the Node process group with `detached:false`. The normal path awaits browser-context closure and the observed Chrome-root close event. Actual Node/browser/platform/architecture metadata is recorded; the browser identity comes from CDP `Browser.getVersion`.

The supervisor's watchdog kill occurs only while its Node leader is unreaped. The unsafe post-reap process-group signal was removed. Final wall-clock, disk and absolute-cutoff checks occur again after child exit. The analysis requires the observed Chrome-root exit and close records both to be exactly `{code:0, signal:null}`. These controls do not establish an all-helper-process guarantee. Abrupt abnormal Node death cannot establish root/helper cleanup and must remain a failed attempt; external process inspection may be needed. There is no hard OS-memory limit.

The allocation is one export at most 30 seconds, one browser attempt at most 180 seconds, one analysis at most 30 seconds, and a separately bounded saved-only UI check at most 90 seconds. Export and analysis time limits are enforced by the parent's external wrappers, not by this review. Browser launch cutoff is 2026-10-18T13:54:26Z. The browser also has a local 170-second guard and the absolute cycle-end guard. Exclusive locks/directories prevent replacement attempts.

Admission requires expected projection below 4 MiB, input below 1 MiB, existing bundle below 2 MiB and the prepared package below 12 MiB. The public package is bounded at 32 MiB, the private profile/log area at 128 MiB, and the combined area at 160 MiB. The 0.2-second disk monitor is a logical growth guard, not an atomic disk quota. Successful storage is one actual semantic blob below 4 MiB plus 116 bounded query/transfer rows below 1 MiB. Transport and in-memory data are not counted as disk storage.

The independent analysis checks the exact 116 query and transfer files, their call binding, absence of `failure.json`, all warm/measured/diagnostic positions, finite recorded phases, every semantic blob, the registered decision calculation, and post-run source-manifest hashes. This is an appropriately narrow gate for the proposed observation. No runtime pass is inferred from static inspection.

## Exact reviewed snapshot

Paths are relative to `research/m31-cost-decision-2026-10-18`. The source files and protocol were statically reviewed; exported data are hash-pinned evidence inputs. Any subsequent change to these bytes requires a corresponding review update before relying on this disposition.

| Path | Bytes | SHA256 |
|---|---:|---|
| `PROTOCOL.md` | 7581 | `23722fbf799ea52972a17b1d35d41913d47864fb2dd41171e3c8131ca529ee27` |
| `source/export.py` | 3414 | `5f3069485d0ca5df1419a1b4eaccf79168e9775e5fc62fa28c4807622489e791` |
| `source/browser.js` | 11856 | `de39b438747f4c598531285f93120f1f155c35c0b48c924f6ee67c4760a535da` |
| `source/run.cjs` | 4930 | `57674c93abc8ab55d77804b2bcf8121bf70315ac3a4762f9e7f6c21dbac70339` |
| `source/supervise.py` | 2230 | `acfe8a2edad33ddeae1e1da5006483d98156d6f41d62aa0947abdf14241f0236` |
| `source/analyze.py` | 5239 | `8a3db4eb15901e6e58616c2d45349bc530c09ee1650a1121953653f2ac8714f7` |
| `viewer/blank.html` | 192 | `05b029e096a151368fb2221ea8fdc94ddf9f3a9fedc5ce3a48fc644bfe051924` |
| `EXPORT.json` | 5478 | `89fe9502d2b99f678f4c193ed0a632d7cbdbebb686ee9b9bd3a8dbaf0f0df5a0` |
| `expected.json` | 2554204 | `e135b68c15c0198cc72c833c0b28d018353f016dcae30ab4cbe5e95d060cde1e` |
| `input-words.json` | 343903 | `e007c459fd1ab1a796a27b6455f4ee3bfe27766fb63ff9e65a4f679a75b18d0f` |

The final protocol adds a separate saved-result UI allocation. Its added paragraph does not change the scientific schedule or gate. The following newly added display files were inventoried by hash only and are outside this finite primary scientific-source review; their presence is not a UI correctness or safety attestation:

| Path | Bytes | SHA256 |
|---|---:|---|
| `source/ui.cjs` | 3522 | `901feb558c44933ae03a896d0b4ad1e4072c8c855a93faee2660631e3ba07d5b` |
| `viewer/app.js` | 4643 | `334c1fe1872885eac39275c7dc588aef4f459b6eef76fdd305cc6b1aa5eff4a9` |
| `viewer/index.html` | 3863 | `14d48357c4de03d3a3b43d9bb17176695926db697bb50f96dacb6d067e73a8f4` |

## Remaining gates

No additional scientific source repair is requested. The parent must finish the already registered manifest/publication/byte-verification prerequisites before the one launch, then apply the bounded runtime and independent-analysis gates. This acceptance does not expand the allocation or authorize another attempt if one fails. The operational and inferential limitations above must remain visible in the eventual report.
