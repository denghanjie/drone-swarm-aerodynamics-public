# Display checks and the preserved capture anomaly

Original display: exit 0 in 2.253313 seconds; seven automated groups passed, including 72 coverage/height/azimuth states. Existing Playwright/Chrome was used because Browser plugin was not available. Viewports 1280x1000 and 390x844. No installations.

| Check | Saved outcome |
|---|---|
| Public pins, page identity and proposal-only labels | Pass |
| Three modes, three heights, eight angles | 72 states pass; planned counts 1/1/48 and arrows 2/3/3 |
| Orbit/reset and no horizontal overflow | Pass on tested viewports |
| Corrupt proposal refusal | Pass before scene creation |
| Console/page/HTTP errors | None recorded |
| Desktop and mobile-scene images | Parent inspected; readable |
| Original mobile-top image | Repeated strip visible; retained and not certified clean |

The visual anomaly's cause is unestablished. No app source changed. A separate publicly frozen capture-only check opened a fresh 390x844 page, waited for the renderer and three animation frames, and saved one full-page screenshot. Exit0 in 0.881000 seconds, four groups passed. Parent inspected capture-ui/mobile-full.png: no repeated strip is visible. This supports that captured state; it neither proves the old anomaly's cause nor certifies every device or viewport capture. No original control sweep was repeated.

The intended interaction flow is load → select measurement coverage/height/angle → orbit/reset → mobile → altered-proposal refusal. Source entry points: source/ui.cjs and separately source/mobile-capture.cjs, each executed once under its own immutable lock/output directory. Both monitored time/output cutoffs were respected. Execution durations are display-check timings, not aerodynamic simulation performance.

Evidence is in ui/qa.json, results/ui-supervisor.json, capture-ui/qa.json, capture-results/ui-supervisor.json and four retained PNGs. Parent saw no framework error screen; this is a static page. Full scientific validity, calibration, future equipment feasibility and other browsers/devices remain untested. The schematic provides no velocity data or new predictions.
