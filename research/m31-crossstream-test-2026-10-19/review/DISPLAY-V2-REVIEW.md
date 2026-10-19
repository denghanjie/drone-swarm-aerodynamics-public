# Static review: separate display-v2 readability allocation

19 October 2026. **Accepted for separate display source freeze and exact-public verification before one bounded display-v2 launch. No static blocker found.** This review does not reopen the completed evaluator, scientific audit or first UI allocation. It does not claim that the revised display has run or that its legibility has been visually verified.

Review consisted solely of reading the contract, viewer, checker and supervisor source and inspecting file metadata/hashes. No viewer execution, browser check, numerical recomputation, fit, pairing or scientific import was performed by this reviewer. The first UI's seven automated check groups passed; the parent separately reported from its screenshots that lateral arrows were too small for comfortable comparison. The distinct revision addresses that observed display issue while preserving the original viewer, frozen source and first UI outputs.

The new viewer's result pin is exactly the closed 2,291,932-byte comparison with SHA-256 `1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a`. The viewer validates size/hash before rendering and reads the saved measured component, candidate, residual, inclusion and metrics. It does not re-evaluate a wake, fit a parameter, recompute scientific scores, interpolate a flow field or create a new pairing. Formatting and color-range/glyph calculations are display operations on saved values.

All 3,240 saved point positions remain on the same off-axis measurement plane. Point glyph size changes from .007 to .0025 in scene coordinates. Sparse arrows now use original row%24==0 and column%24==0, together with prior inclusion and the existing nonzero glyph threshold, instead of selection by array position. This is a coordinate/index-only drawing rule. It changes which arrows are drawn, not which measurements enter any saved metric. The checker derives the corresponding expected arrow count from the saved records, including legitimate zero-arrow cases.

Arrow direction remains the sign of the selected saved x component. Total length is abs(value)*4 and the page explicitly labels 4m per reference-speed unit as an enlarged display scale. The head length and width depend on the same absolute value and are capped. No common arrow length is substituted for magnitude. This glyph scale is not a dimensional airspeed conversion, physical advection time, particle trajectory or new flow measurement. Measured/candidate colors retain a shared flow range; residual color range remains separately labeled. Selection mode and excluded-point colors remain distinct.

The inherited gain, whole-field RMS normalization, fixed bands, exposure statement, no-swirl/core assumptions, unresolved airspeed conversion and limits on three-dimensional/force/flight claims remain visible. The introduction now says the motion is implied by a symmetric spreading jet, which is consistent with the conditional closure. No new scientific success claim is introduced by larger arrows.

The checker keeps the seven declared groups: meaningful loaded/rendered page, saved gain/metric/count/band text, four modes with expected sparse arrows and distinct renders, orbit/reset response, desktop/mobile captures and horizontal layout, corrupted-result refusal before rendering, and console/page/HTTP health. Its screenshots go to the distinct ui-v2 directory. The UI check source and separate supervisor do not invoke evaluator or audit code.

The new supervisor has its own permanent display-v2-supervisor.lock and exclusive stdout/stderr creation. It runs only ui-v2.cjs under the fixed external 60-second limit. Its saved-byte observation covers results plus both ui and ui-v2 folders under the aggregate 32 MiB cap, includes receipt reserve, terminates the child process group on breach and checks elapsed/output limits again after exit. A failure consumes this display invocation and must remain recorded; this review permits no repeat or change after a failed run.

Before launch, the parent must bind these exact files and this review to a separate immutable display manifest together with the original source pins and saved scientific/first-UI provenance, publish it and complete exact-public verification. The current viewer checks saved-result identity but does not itself perform this external source-publication gate; orchestration must enforce it. After the sole run, inspect the retained desktop/mobile and mode images for actual arrow readability, sign visibility and overlap, in addition to reading the automated receipt. Static source acceptance and a later automated pass alone do not settle the reported visual issue.

The original scientific outcome, all saved predictions/metrics and their passing audit remain the ones reviewed in RESULT-REVIEW.md. No causal claim about residual structure, new left/right comparison, production adoption or broader goal completion is covered by this display allocation.

## Reviewed identities

Paths are relative to this checkpoint package. Any change requires static review before launch.

| File | Bytes | SHA-256 |
|---|---:|---|
| `DISPLAY-V2.md` | 1654 | `716e85575d727dd1b482388aa115cbde87270aeefa8bc1770a54a026f3f71555` |
| `source/ui-v2.cjs` | 5292 | `691e620ff38dfa2e013107b3ca33a1ea7f657894fbeea92a0fdf11c6ef4ffd60` |
| `source/supervise-display-v2.py` | 1601 | `d6f68bc1d6ebf08be08dddfe29145b75413d3719fb7401fdb4e4c0fbb721fd6e` |
| `viewer-v2/app.js` | 6867 | `f4d5f8fe36421c3c9b6a070a6402ffed4fb2e1f45376169746c5931faf029b96` |
| `viewer-v2/index.html` | 5352 | `fffaf2af6379fb2d517989bd859fab8602a027331db7b1eeff63619b5fad951d` |
| `viewer-v2/pins.json` | 103 | `0e9bc5272c984e917a673ebcdf05e51c82f2b87709d7308710164e224aa42686` |
