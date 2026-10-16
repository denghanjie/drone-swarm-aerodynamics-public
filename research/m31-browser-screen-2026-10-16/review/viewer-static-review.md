# Browser viewer static presentation-contract review

Scope: `research/m31-browser-screen-2026-10-16/viewer/{derive.py,app.js,scene.js,index.html}`, their current binding/display metadata, and the necessary frozen config/schema, seal, stage/audit/analysis summaries and generation metadata. No scientific source was executed, no reviewer was rerun, no trajectory or solver was recomputed, no browser was launched by this reviewer, and no frozen file was edited. Root separately owns rendered Playwright QA. Paths below are repository-relative and public-safe.

The actual saved display agrees with the sealed evidence. Two fail-closed presentation issues require correction before accepting the viewer's verification contract; an additional exact-coverage check should accompany the second fix. These findings concern presentation validation, not the already completed scientific result.

## Findings

### P2 — A later selected-record failure leaves the passing headline visible

Location: `research/m31-browser-screen-2026-10-16/viewer/app.js:24`, `:50`, `:64`; header placement in `viewer/index.html:3`.

`main()` installs the qualified headline and lead before selected generation/pose/load verification. If one of those later fetches or hashes fails, `fail()` hides only `#content`. The header is outside that section, so “The improvement survives three Chrome repetitions” and the passing lead remain visible above “Display stopped.” The same outcome occurs after an initially successful load followed by a failed case selection. This is a concrete late-failure path; the scientific seal is unaffected.

Correction: reset or hide the result-bearing header/lead in `fail()`, stop replay, and keep all result content hidden until the selected evidence has passed. Add a rendered QA case where the pose or load request fails after the passing header was installed. Parent confirmed this finding and will preserve the initial QA before patching.

### P2 — Fresh viewer hashes are not checked against the frozen seal/artifact chain

Locations: `viewer/derive.py:10–12`, `:29–35`, `:52`; `viewer/app.js:11–20`, `:50–52`.

`derive.py` computes new pins for whatever records currently occupy the expected paths; `app.js` verifies those freshly generated pins. Neither code path requires the pinned audit/analysis/stage/closure records to match `qualification.inputs`, nor requires selected generation metadata, pose bytes and load metadata to match the frozen `reviewRun.artifacts` inventory. Consequently, a post-seal record edit followed by re-running only the presentation derivation can acquire matching viewer pins while retaining the original seal's Boolean pass. This is not a defect observed in today's data: metadata-only comparison confirmed that all current relevant binding pins match `qualification.inputs`, and every selected generation/pose/load pin belongs to the sealed review inventory.

Correction: before claiming verified evidence, require each seal-covered binding entry's path/bytes/hash to match its `qualification.inputs` entry; require the full mandatory seal-covered entry set. Then use the sealed review-run inventory to bind configuration, per-process evidence and every selected generation/pose/load pin. Continue checking actual fetched bytes against these pins. This is metadata-chain validation and needs no scientific rerun. Source-commit/manifest identity consistency should remain required.

### P3 — Require exact case/process identities, not only counts

Locations: `viewer/derive.py:28`, `viewer/app.js:23`, `:26–32`.

The current data has all three distinct configured cases and exactly `p0,p1,p2` for each. The validator, however, permits omitted display cases, and its process checks require length three without checking unique exact process IDs. `derive.py` silently skips a missing generation metadata file even when the campaign's seal qualifies. A freshly regenerated display could therefore omit a case or repeat one process entry, retain its passing headline, and pass these structural checks; the three-row table would show missing processes as unavailable. This is not fastest-process selection in the delivered data, but it leaves the full-campaign presentation contract weaker than stated.

Correction: for a verified campaign, require the ordered/unique configured case-ID set and the exact unique process-ID set `p0,p1,p2` in analysis and in every displayed case. Require the selected generation metadata to match case ID/count/seed, `complete:true`, 26frames, width `1+7N`, and cadence0.2. The original sealed record pins then bind the actual binary frame times already checked scientifically.

## Confirmed source behavior and current metadata

- Generation metadata for all three cases records `complete:true`, 26individual frames, `recording:{cadence:0.2,streamed:true}`, and times `[0,0.2,...,4.8,5]`. Concatenated widths are7001 for N1000 and35001 for N5000. Display `poses` metadata equals the saved generation metadata.
- `scene.js:11` uses frame stride `1+7N`, skips the first time scalar, then reads XYZ plus XYZW quaternion for every vehicle. `showFrame()` reads the timestamp from the same selected frame. No interpolation, generator, aerodynamic solver or synthetic movement appears in the viewer.
- Playback increments one saved frame every400ms, consistent with the displayed nominal0.5× playback of0.2s frames. The default view is the final frame. Drone display scaling preserves vehicle-center positions; rotor/body glyph dimensions scale for visibility.
- Final-pose load coloring is enabled only when qualified saved loads exist. The load comes from a fixed p0/L qualification record rather than a fastest process. The caption explicitly names p0, states cross-process checked equality, and labels these as predictions rather than measured thrust loss. Nonfinal frames remain uniformly blue and explicitly state airflow loads were not integrated.
- All three displayed cases contain `p0,p1,p2` in order. Every displayed timing summary/pair object equals the corresponding saved analysis object. The table always iterates p0,p1,p2; the process dropdown changes detail bars only. There is no fastest-process search or filtering.
- Saved analysis contains three complete processes,42validated calls each,126total calls, and six separate primary N5000 cells. All six recorded primary decisions pass. The N1000 cells remain present and are explicitly contextual in the decision text; their failed primary-style thresholds are not used to rescue or reject the joint N5000 rule.
- The app accepts practical status from the terminal seal rather than from the reviewer's intentionally null `practicalRulePass`. Current analysis has `independentAuditPass:true`, `performanceRulePass:true`, `practicalRulePass:null`, `requiresReviewSupervisorClosure:true`; the terminal seal has `sealSuccess:true`, `evidenceQualified:true`, `practicalRulePass:true`, no failure reasons and all closure gates true.
- The current independent audit records57,572checks, no errors and126validated timing records. All three stage summaries record successful closure, absent child and owned groups, zero return code and no surviving owned processes. These summaries were read as metadata only; no independent scientific reanalysis was performed here.
- Scope wording consistently distinguishes five-second airflow-off Boids replay, a separate final-pose load query, fixed warmed Chrome queries, and physical accuracy/live-swarm rate/novelty. The page excludes rendering, flight integration and transport from query timing and calls observed min–max ranges descriptive rather than confidence intervals. No broader scientific claim was found in these four files.

## Reviewed source pins

| Repository-relative path | Bytes | SHA256 |
|---|---:|---|
| `research/m31-browser-screen-2026-10-16/viewer/derive.py` |4651|`8824fd7483ba034d71943df05ac76b80cbd72723c3f51108a8098425873e3f79`|
| `research/m31-browser-screen-2026-10-16/viewer/app.js` |9022|`9c64034da5f4e9f58a8f06167b19c9bfa703677245f64c7c6fe3f8115a94b1a8`|
| `research/m31-browser-screen-2026-10-16/viewer/scene.js` |3875|`58718dc7452be35c1c3ba0a179b3f9398305e81dceb117466219b269b4ee88e7`|
| `research/m31-browser-screen-2026-10-16/viewer/index.html` |5217|`9bade1050d1343f09831b799f96bc9c0ac73441d6af6a69a0efdcbf7a566f528`|
| `research/m31-browser-screen-2026-10-16/viewer/binding.json` |2627|`737c9db4d964e98004646bfbec0758a2e6666dcf7ab9e195df4b9f2d18daf647`|
| `research/m31-browser-screen-2026-10-16/viewer/display.json` |191487|`d888807ad31c2709a4e6b53999e409f2155e6d00c97d9a26eb7efa1d41837842`|

## Frozen evidence pins used for metadata comparison

Source commit: `3a2b9e3ceca3798f56596617dc483c45a09a309c`.

| Repository-relative path | Bytes | SHA256 |
|---|---:|---|
| `research/m31-browser-screen-2026-10-16/results/qualification.json` |2493|`726ca7a865911d73f38303a33df480896f8dce3e363d4c9de028cc5e84fa8834`|
| `research/m31-browser-screen-2026-10-16/results/analysis.json` |214734|`9aa517d2a3eaae3d1f0d00f8a4ea972781ae42952b7e9631323201f1e0803c04`|
| `research/m31-browser-screen-2026-10-16/results/independent-review.json` |6473244|`91db762e8d670af1b9648bdef54b798b86b72b1717e28d57bb9545892434dba2`|
| `research/m31-browser-screen-2026-10-16/results/review-run.json` |120004|`dfac8c5ae25506c0b77bf0b4bd794b76cd135e82ad2d806c07a0320468846eca`|
| `research/m31-browser-screen-2026-10-16/REQUIRED-SCHEMA.json` |39493|`08c92f3bfb3a610262080f7cd97cb5079ff43accdb7a1a9bb86346720b8a0637`|

The report applies to the reviewed presentation hashes above. Root's forthcoming presentation fixes and expanded rendered QA require their own updated pins; frozen scientific code and records must remain unchanged.
