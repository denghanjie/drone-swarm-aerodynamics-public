# Viewer QA

Flow: open the physical-evidence status page, load the prior exact 5,000-drone recording, scrub, play/pause, orbit/reset and inspect evidence links. Browser plugin not available; the existing frontend-testing-debugging skill's installed Playwright/Chrome fallback was used. No dependency installed.

Attempt1 failed before any page check: sandboxed Chrome exited SIGABRT with EPERM during cleanup. Its raw launch log remains private; the public report removes temporary paths/PIDs. Attempt2 used the authorized process escalation and passed24 checks with zero console/network errors and zero warnings. Viewports1440×1000 and390×844. Desktop and mobile-scene screenshots were visually inspected: no clipping or horizontal overflow, clear recorded-reuse/airflow-off disclosures, visible 3D cloud. Playback changes exact saved frames; it is not a live model benchmark. Evidence links resolve. Other devices/browsers remain untested.

Run qa/run.cjs with the installed Node and Playwright, RESEARCH_CHROME naming installed Chrome and RESEARCH_QA_OUTPUT naming a fresh output directory. QA may be repeated after display changes; it performs no scientific evaluation. Source access allocation remains closed.
