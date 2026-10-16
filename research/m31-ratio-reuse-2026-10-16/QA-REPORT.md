# Three.js replay verification

Summary: paired full/reuse recordings render with exact raw-data hashes, all three integration grids, synchronized frames and explicit failed accuracy gates. Final QA passed53checks, zero console/page/HTTP errors and zero warnings. Attempt1 passed52checks; visual inspection motivated a sideways-scroll cue for the narrow table and an additional mobile interaction check. Both attempts are preserved. No scientific source or raw numerical record changed.

Environment: local port8876, installed Chrome155.0.8059.80 through existing Playwright; desktop1440x1000, mobile390x844, altered-evidence1000x800. Browser plugin not available, so the documented installed Playwright path was used. No browser dependency was installed. The flow under test is: open ratio-reuse viewer -> inspect failed decision -> select grids and scrub/play/pause -> orbit/scale/reset -> inspect evidence/mobile gates -> reject altered raw data.

| Check | Result and evidence |
|---|---|
| Page identity and nonblank screen | Pass; expected URL/title/heading, two WebGL canvases |
| Framework overlay / console health | Pass; no overlay, no relevant errors/warnings or failed HTTP requests |
| Data and decision | Pass; audit count, six completions, position maximum and all24failed cells match saved results |
| Interactions | Pass; all3grids, exact initial/final time/position contrast, play/pause, both scale controls, orbit/reset |
| Evidence | Pass; all visible links return200; corrupted analysis bytes stop display and disable playback |
| Responsive layout | Pass; no page overflow; results table scrolls on mobile and has an explicit cue |
| Screenshots | Parent visually inspected final grid-0.00125-end.png, mobile-gates.png and altered-evidence.png; initial desktop/mobile also inspected |

Commands use existing Node/Playwright with RESEARCH_CHROME and RESEARCH_QA_OUTPUT, running qa/run.cjs from repository root. Final trace: qa/attempt-2/report.json. Screenshots are intentionally committed at the user's request for regression records. Viewer fetches and hashes complete raw files sequentially, retaining only displayed sample poses, to limit concurrent parsing memory. It imports no aerodynamic or flight solver. Common spatial bounds and enlarged display models preserve recorded positions; frames are not interpolated.

Remaining risk: one installed desktop Chrome, two normal viewports and a synthetic corruption case. No exhaustive device/browser/accessibility/performance test, no live simulation verification and no physical validation. The Browser plugin may improve future in-app QA access; it was unnecessary for this completed installed-browser verification.
