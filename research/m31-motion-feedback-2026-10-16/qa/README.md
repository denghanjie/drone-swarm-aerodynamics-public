# Viewer verification

Passed 43 automated checks with installed Playwright and Chrome 155.0.8059.80. Browser plugin not available. Flow: load paired evidence, choose all four cases, scrub/play/pause, change display scale, orbit/reset cameras, open evidence links, and inspect mobile layout. Desktop 1440×1000 and mobile 390×844. No page, network or console errors; no warnings. Screenshots are committed at the user's request for checkpoint traces.

| Check | Result |
|---|---|
| Correct URL/title, meaningful content, no framework overlay | Pass |
| Raw evidence verifies before rendering; all four cases in both panes | Pass |
| Frame synchronization, zero-effect control, 1.102 m final Boids contrast | Pass |
| Play/pause, scale, orbit, reset and evidence links | Pass |
| Mobile horizontal overflow | None |
| Desktop and mobile screenshots visually inspected | Pass |

Parent inspected boids-end.png and mobile.png: readable controls/disclosures, visible paired 3D scenes, no clipping. Exact recorded poses are shown at 0.1 s spacing without interpolation, at quarter-speed playback. This UI check does not validate the flight physics. Other browsers and touch gestures were not tested. See attempt-1/report.json and run.cjs for reproducible UI checks.
