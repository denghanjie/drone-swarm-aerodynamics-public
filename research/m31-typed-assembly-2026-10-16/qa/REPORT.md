# Recorded replay QA

Flow: open the fresh Boids viewer, select all three cases, scrub/play/pause the exact recorded frames, check final-only load coloring, change display size, orbit/reset the camera, inspect mobile and open evidence links.

Browser plugin not available; the installed Playwright and Chrome were used through the approved host path. No browser dependency was installed. This was performed after candidate and numerical reviewer exit, so it did not overlap their timings. URL:http://127.0.0.1:8876/research/m31-typed-assembly-2026-10-16/viewer/ . Desktop1440×1000 and mobile390×844.

| Check | Result |
|---|---|
| Page identity, meaningful content, no framework overlay | Pass |
| Exact selected pose/load record hashes | Pass |
| Three cases and all declared drone instances | Pass |
| Scrub, play, pause; earlier frames lack load claims | Pass |
| Display scale, camera orbit, reset | Pass |
| Mobile horizontal fit and readable scene | Pass |
| Console, warnings and HTTP responses | Zero errors/warnings |
| Evidence links | All tested links returned successfully |

44checks passed on the first attempt. Screenshots in attempt-1 were visually inspected: the full three-dimensional starting cloud is visible on desktop/mobile, with record/playback controls and explicit short-horizon/airflow-off disclosures. The cloud remains close to its initial arrangement after only two seconds; the viewer makes no mature flock claim. Load colors are subtle on this tested case and are not amplified to manufacture a dramatic effect.

Run qa/run.cjs with the bundled Node, NODE_PATH pointing to installed dependencies, RESEARCH_CHROME pointing to installed Chrome and RESEARCH_QA_OUTPUT pointing to a new output directory. No scientific solver is imported or executed by this page or QA script. Browser playback speed, screenshots and instance counts are not computational-performance measurements. Other devices, browsers and viewports remain untested.
