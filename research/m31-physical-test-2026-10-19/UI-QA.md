# Saved evidence view QA

User-facing view: http://127.0.0.1:8876/research/m31-physical-test-2026-10-19/viewer-v2/

The flow under test is: load saved result -> select each measured separation -> matching readings and rendered two-drone geometry -> orbit/reset -> responsive layout -> altered-data refusal. Browser plugin unavailable; used the already installed Playwright/Chrome for local automated testing, with no installations. Screenshots and test scripts are retained as explicitly requested research traces.

| Check | Result |
|---|---|
| Intended page identity / nonblank / no error overlay | Pass |
| Headline matches saved primary result | Pass |
| All11 selections match saved upper/lower measurements and predictions | Pass |
| Separation selection and camera orbit visibly change scene | Pass |
| 390px layout has no horizontal overflow | Pass |
| Corrupted evidence refused before scene appears | Pass |
| Page and console errors | None |
| Parent visual inspection of final desktop screenshot | Pass |
| Parent visual inspection of final mobile scene screenshot | Pass |

Desktop1280×1000; mobile390×844. The original ui/mobile.png full-page screenshot repeated the top viewport and is unusable visual evidence; it is preserved. The second attempt switched to viewport captures. ui-v2/mobile-top.png retained the previous scroll position and has a partial stale strip; despite its filename it does NOT document the mobile page top. Do not use it as proof. ui-v2/mobile-scene.png is clean and was inspected. The final desktop screenshot shows the full text, chart, scene and controls. Mobile header/full-page capture is not established by these screenshots; DOM/data/width checks and clean mobile scene coverage are established. No further display attempts were needed to substantiate the delivered scene and controls.

The viewer reads hash-bound saved results; no research model executes in it. Arrows show a common illustrative scale, rotor discs are schematic and the scene is a static reconstruction, not experimental flight video. Current view updates explanation/geometry for this physical checkpoint, not a new Boids flight trajectory. No scientific source/result bytes changed during display repair. Both UI supervisor exits0; initial and repaired artifacts remain distinct.
