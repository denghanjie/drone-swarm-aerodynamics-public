# Three.js viewer QA

Passed 46 automated checks with installed Playwright and Chrome 155.0.8059.80. Browser plugin not available; installed browser/runtime used without installation. User requested committed traces. Desktop 1440×1000; mobile 390×844. No console/page/network errors or warnings. Parent visually inspected full-force-end.png and mobile.png: both scenes and controls are visible, text is readable, no clipping or horizontal overflow.

Flow: load verified recordings → choose each of full/force-only, off/force-only and off/full → scrub from identical initial positions to saved last-frame contrasts → play/pause → change scale → orbit/reset → open all evidence links → inspect mobile. The raw end-frame differences are independently calculated from saved JSON in the QA script, without loading a scientific solver.

| Check | Result |
|---|---|
| Correct URL/title, nonblank content, no framework overlay | Pass |
| Model/physical limits and synthetic-load disclosure | Pass |
| Completion/audit/contrast values match saved analysis | Pass |
| All three comparison labels, instance counts and synchronized frames | Pass |
| Play/pause, scale, orbit/reset | Pass |
| Evidence links, desktop/mobile screenshots, no overflow | Pass |
| Console/page/network health | Pass |

See run.cjs and attempt-1/report.json. Screenshots are in attempt-1/. Actual playback is at quarter speed with 0.1 s saved pose samples, no interpolation and a 4× default model-size exaggeration. Common spatial bounds are shared across all arms. View changes do not change scientific states. These checks establish rendering/interaction behavior only; other browsers, touch gestures and physical flight were not tested.
