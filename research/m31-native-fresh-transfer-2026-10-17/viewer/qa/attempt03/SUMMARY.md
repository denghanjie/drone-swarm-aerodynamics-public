# Fresh-transfer viewer camera QA — attempt 03

Attempt 03 passed its focused camera, frustum and control checks. The author inspected the original desktop and mobile screenshots: the complete swarm and saved force arrows fit both scenes, including the mobile final view that clipped in attempt 01. The parent independently inspected both original screenshots and accepted the fit; that signoff was confirmed in the handoff message.

## Recorded execution

- Exactly one explicitly authorized attempt 03; no automatic retry and no new scientific imports, execution or recomputation.
- Supervisor outer wall: 14.045836166478693 seconds; child and supervisor exit code 0. Browser work receipt: 9,437 ms.
- 154 checks passed; 104 frame views cover all 52 recorded frames at both viewports. All 24 final combinations passed: two runs × F/L × scales 1/4/8 × desktop/mobile. There are 27 force/frustum checks, including resize and screenshot states.
- Maximum padded absolute XY NDC was 0.7055962716056126 for glyphs and 0.6571457202424568 for saved-force geometry, below the 0.995 limit. Homogeneous positive-w and depth checks passed.
- Chrome 155.0.8059.80 and Playwright 1.62.1. No recorded page errors, console warnings or failed requests.
- Graceful Browser.close; the owned Chrome root emitted exit and close with code 0 and null signals and was reaped. No forced termination; private profile removed. The existing localhost:8876 HTTP server (PID 48039) was left untouched.

The allocation was 120 seconds outer wall, 95 seconds work, a 110-second child timeout with at most 9 seconds fallback, and 16 MiB aggregate artifacts/per-file child limit. Private-profile scratch was separate. These receipts do not claim an enforced memory ceiling, hard containment or observation of every browser helper exit.

## Preservation and sources

All 519 protected files match both immutable snapshots and their current bytes at finalization. The pre-launch allocation and accepted attempt 03 source pins were checked again. The camera-fixed viewer, prior attempts and scientific evidence are unchanged. Only this attempt's SUMMARY.md, FINAL-PRESERVATION.json and ARTIFACT-MANIFEST.json were added during finalization.

- Accepted attempt source inventory SHA-256: `558ab850310ba326bdca61a3d4b1f57217b53161905a51d23b37b3abb753344e`
- Accepted protocol SHA-256: `4e6361cca9ca393b643a04fbf21c6d3288cdf1bebf34a922e830ccb54c72c6e5`
- Allocation SHA-256: `12f67430522d0ca70a6a392ba07b26d86a3371fab1294b2bb6cce0b9fe7b1924`
- Report SHA-256: `142f02269437d1c381e3a389534a3efe57903ba85d9f54cacdf40887c03932bb`
- Attempt receipt SHA-256: `4f48620b64a25c2a0106e4ae6d889062c1e7765a8a566e94da273541e01ffcaf`
- Both immutable snapshot SHA-256 values: `788b357181e2b05044ff33d51e84968964a78678ae89f7c58d7b09ab5a96aaf3`

The viewer consumes pinned saved poses, quaternions, forces and loads. Its labels remain F screened and L lean baseline, both full contribution. These examples skipped no center-norm calls; no speed claim is supported. Original retained supervision remains failed; the independent fresh saved review is a separate record. Attempt 03 did not rerun scientific generation, reference, browser computation or checking.

## Screenshots

- [Desktop](desktop.png): 696,968 bytes; SHA-256 `f8250aef79e0c9785358bbe0b28e1e6ffe2298c1ed36cc1e59f21c666823f78c`.
- [Mobile](mobile.png): 569,988 bytes; SHA-256 `5fd8f134a0bb9327d0f3783db14fc204e812d234d602a35b3dd5d3852d071082`.

Both were inspected at original image detail. Text and controls remain readable; page/table behavior is consistent with the previous functional QA. The parent confirmed independent inspection of both original screenshots and accepted the fit.

## Attempt lineage

1. Attempt 01 passed 192 functional checks in 18.812501458 seconds, including recorded frames, final calls, links and stale/corrupt clearing. Visual inspection found clipping in the mobile final B scene. Original viewer sources and all receipts were preserved before the camera fix.
2. Attempt 02 failed in 7.294242415577173 seconds at its desktop resize aspect assertion, before frame/final-combination/screenshot coverage. It incorrectly compared integer clientWidth/clientHeight with the renderer's fractional getBoundingClientRect dimensions at 1e-10 tolerance. Its failure and evidence remain unchanged. Attempt 02 itself did not record the actual dimension values and supplies no camera pass.
3. Attempt 03 changed only the harness dimension comparison, recorded both dimensions, and updated attempt identity/preservation closure. It used the unchanged camera-fixed viewer. The desktop aspect was 2.0926388888888887 from 941.6875 × 450 CSS pixels, while integer client size was 942 × 450. Mobile aspect was 1.0787878787878789 from 356 × 330. The corrected comparison and full focused coverage passed.

No further browser launch, science run, commit or publication was performed for this handoff. The artifact manifest lists every attempt 03 file except itself with byte counts and SHA-256 hashes.
