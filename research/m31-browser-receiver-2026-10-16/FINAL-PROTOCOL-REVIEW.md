# Receiver f32: final static reconciliation

2026-10-16. Scope: reconciliation of this reviewer's prior numerical, reference, metadata and source-provenance findings in `<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16`.

**Disposition: all prior findings in this scoped review are resolved in the inspected snapshot. No further numerical/provenance blocker was found.** The draft is ready for its final freeze/publication verification, subject to the separately assigned process-containment review. This is a static disposition, not a numerical pass, capability result, or authorization to launch before the protocol's remaining prerequisites are met.

No scientific module was imported or executed. No input matrix/audit values or scalar-probe values were inspected in this reconciliation. No root, shader, browser, field, flight, benchmark or numerical checker was run. Inspection was limited to source/document text, the config's domain/gates/limits section, runtime metadata and file hashes. The numerical constant-encoding artifact was hashed, not recomputed. No repository files were changed.

## Prior findings and resolution

| Prior finding | Current static evidence | Disposition |
|---|---|---|
| Positive inputs could accept returned alpha=0 in host metadata checks | `compareRecord` now requires `alpha>0` for positive Uq. | Resolved. |
| Code 2 did not verify absence of the strict threshold stop | Code 2 now requires both twelve updates and `step>=Math.fround(1e-15)`. Code 1 requires the strict converse. | Resolved; cap termination still needs all accuracy gates. |
| Protocol update wording could imply computing the step after overwriting x | Protocol explicitly computes `abs(next-oldX)`, assigns updated x, then tests the saved step. Shader math is unchanged. | Resolved. |
| Copied GPU bytes could be discarded by a later error-scope/loss failure | Browser returns copied raw words with a pending validation result. Driver writes `*-gpu.u32` and readback metadata before awaiting `finishReceiverBatch`, then saves/checks API status. The whole sequence remains inside the batch deadline. | Resolved; failed API qualification prevents reference attribution/acceptance. |
| Initialization rejection could lose already collected adapter/compiler evidence | Phase/adapter/compiler/shader evidence is retained in browser state; pipeline rejection has a structured result; the driver's bounded failure read saves available evidence or explicitly records unavailability. | Resolved within the declared failure model. |
| Attempted dispatch count could be confused with actual submission | Protocol calls the charged count an attempt reservation. Browser records `submitted` after `queue.submit` returns, with groups and byte counts; readback/failure evidence retains it when available. | Resolved; an attempt is not successful completion. |
| Served HTML/host JS were not tied to the frozen source | Exact routes fulfill browser.html, browser.js and receiver.wgsl directly from pinned local bytes. Source contract and actual request hashes are retained; shader content is also reconciled before dispatch. | Resolved; the runner no longer depends on unchecked server responses. |
| Only adapter limits were recorded/checked | Initialization now records/checks actual-device storage binding, buffer and dispatch limits as well as adapter limits. | Resolved for this fixed layout. |
| Runtime identity was only loosely specified | Driver verifies Node and Playwright entry/package/core-bundle pins and exact Chrome version; protocol/runtime metadata expressly limit the scope of these pins. | Resolved without claiming a complete browser/transitive-code inventory. |
| Earlier proposal counts could be mistaken for the final experiment | PREFLIGHT-RESOLUTIONS.md preserves the earlier design as history and explicitly supersedes its three dispatches/72,096 new roots. | Resolved. |

The receiver shader and independent solver hashes are unchanged from the preceding reviewed snapshot. The revised guards/evidence handling have not introduced an alternate numerical solver, additional probe, extra GPU dispatch, changed root tolerance, changed force gate or timing comparison.

## Numerical and accounting disposition retained

R remains saved independent-I evidence for 24,000 exposed reused items, plus 32 newly scheduled scalar references. Q solves at the binary64 quotient of decoded packed U/vi; A solves directly at returned alpha. Source/constant packing, alpha division, Newton arithmetic and final force-product errors remain separately reconstructible. No old root or field is recomputed to obtain the reused R values.

The gates remain delivered G/R rotor error ≤1e-7 N, G/A root error ≤1e-6, host cubic residual at returned alpha ≤2e-6, and represented power ratio at decoded Uq/viq ≤2e-6. The old 1e-12 N rotor comparison and original-model power deviation remain separately labeled diagnostics. These choices qualify neither the old binary64 standard nor physical adequacy.

Complete-success accounting remains four dispatches, 24,032 valid roots plus five invalid guards, 24,192 launched lanes including 155 padding lanes, at most 288,384 GPU Newton updates, and 48,096 newly scheduled host roots reserving 4,617,216 iterations. Field and integration counts remain zero. This is receiver-only feasibility on the recorded environment and fixed suite; no wake, geometry, source summation, body/world GPU assembly, speed or coupled-flight claim follows.

## Remaining procedural prerequisites and review boundary

The consumed-file freeze/publication verification is still a separate prerequisite. This review did not verify saved scientific input values, execute the runtime pin checks, establish actual browser capability, or inspect a completed run. The final freeze must cover all consumed reference/source/runtime metadata described by the protocol, and its exact published identity must be independently verified before the sole attempt.

Detached-process registry and supervisor containment are assigned to the separate evidence reviewer. This document does not certify that mechanism. Earlier draft/design/static reviews should remain unchanged as historical snapshots; this note and PREFLIGHT-RESOLUTIONS.md record their resolution. The disposition below applies to these hashes, not to an unreviewed future revision.

## Snapshot hashes

| File | SHA-256 |
|---|---|
| PROTOCOL.md | 82739b37b12a1bf340f25c117e4f56184adc1c69677273c5069c62e77490cdca |
| config.json | 2d89e2cecc048a9427555818507079eb1410836ca38bc04961e867d89b6c29ce |
| schema.json | 9a8d8d440360c3c19f48a28eea5e58cc9535e47e947bc850994db1477747964b |
| source/receiver.wgsl | dc64e23b3905d635f0d1de4d56233c2380455e89c2f50ee5a59c67baca6f1555 |
| source/browser.js | 1476e9984454cad29f989d015355d2f41164ff2906b9aad3817abc1382435483 |
| source/reference.cjs | 4628e2a3a4d843868810bea070153fe22798cfe3e73fd483492ca329558d497d |
| source/experiment.cjs | f49aa4ac2e533a83987354818266ccb6810f5f6061aba7f41660d9fdf3dba045 |
| source/browser.html | 30821edc65a0ac3d8ee739b7342897142aecf4be1ec3b55a29361f5ac7f04834 |
| runtime-provenance.json | 499b92433a9cf249c026b3f9c7d1edf5d03328c089ad90a6dc04095892f727ae |
| constant-encoding.json | a3cab7f30b4490308464d1016bbe19539a8d197fb77076860f523c484c54005e |
| DESIGN-CHALLENGE.md, historical | 6a87d0fd146d019c34e1eac3d814d08c5c9e926fc2921031ac1b882194df6aa5 |
| INITIAL-STATIC-REVIEW.md, historical | ff86b2e63de430b383a0365ff8b0fbd4e3159f24028d61b2dff3b99287cac65c |
| PREFLIGHT-RESOLUTIONS.md | 83f8f96cad33d11e5251dc7ac30ed464634649c9dfb668691b84d0c359ed38bc |

Primary inspected files: [protocol](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/PROTOCOL.md), [driver](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/source/experiment.cjs), [browser host](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/source/browser.js), and [resolved draft differences](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/PREFLIGHT-RESOLUTIONS.md).
