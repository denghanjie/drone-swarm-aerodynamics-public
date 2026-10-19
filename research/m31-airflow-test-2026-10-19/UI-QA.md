# Three.js evidence view verification

Flow: local evidence view loads → choose measured/model/fitted/error view → colors reflect saved readings → orbit/reset → mobile → refuse changed evidence.

Browser plugin not available; existing Playwright and installed Chrome used without installation. URL: http://127.0.0.1:8876/research/m31-airflow-test-2026-10-19/viewer-v2/ . Viewports1280×1000 and390×844.

Attempt1 completed the scene, metric, all4modes, orbit/reset, mobile and corruption-refusal checks, but overall failed because of a resource404. Its original test recorded console text without resource URL, so that log does not conclusively identify which request failed. Retain original viewer/source/ui/ and results/ui-* outputs. Do not call it a clean pass.

Attempt2 is a separate allowed display repair: viewer-v2 adds an explicit inline icon, clarifies selection bands and the outline's unmeasured area; source/ui-v2.cjs records failing HTTP URLs as well as console errors. No scientific source, result, selected cells, scores or frozen viewer files changed. Supervisor retains its own distinct lock/output; no scientific rerun. Attempt2 passed all7check groups, with zero console/page/HTTP errors. Parent visually inspected desktop full-page and mobile scene captures; initial mobile top/scene evidence also showed correct wrapping. No third attempt is required or allocated for this completed milestone.

| Check | Result |
|---|---|
| Page identity, meaningful content, no error overlay | Pass |
| Both overall metrics and3bins match saved evidence | Pass |
| All4modes change actual rendered plane | Pass |
| Orbit and reset respond | Pass |
| Desktop/mobile, no horizontal overflow | Pass |
| Altered evidence refused before rendering | Pass |
| Console/page/HTTP health | Pass on attempt2 |

Evidence: ui-v2/qa.json, desktop.png, mobile-top.png, mobile-scene.png, u.png,a.png,b.png,residualA.png. Source sequence uses installed Playwright chromium.launch, page.goto, selectOption, screenshots, mouse orbit, viewport change, route corruption and page.reload. Data are fetched with exact SHA256/byte binding; no scientific prediction runs in the browser. Remaining limits: two tested viewport sizes and installed Chrome only; no validation of other browsers/accessibility configurations, full3D physical fields or flight.
