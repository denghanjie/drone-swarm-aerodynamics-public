# Failed-launch page verification

The flow under test was: failed-launch status page → historical run selection, scrubbing, playback and orbit → truthful status text and saved-pose display. Browser plugin not available; the existing Playwright installation and Chrome were used. No dependencies were installed and no scientific code was invoked.

Attempt 01 passed 228 checks in 5793 ms. Both historical runs and all 102 pose frames were checked: 19,584 rendered center components matched the Float32 representation of the saved binary64 positions. These are display checks, not new physical or numerical simulation results. The parent visually inspected both screenshots after the automated run.

| Check | Outcome |
| --- | --- |
| Correct URL/title and meaningful page | Passed |
| Failed launch vs untested scientific claims | Passed |
| Historical-only disclosure | Passed |
| Framework overlay | None found |
| Application errors / browser warnings | None recorded |
| Run selector, 102 frames, playback, orbit/reset | Passed |
| Desktop 1440×1050 and mobile 390×844 | Passed; no horizontal overflow |
| Navigation links | Passed |
| Five deliberately corrupted fetched resources | Each hid the claims and replay |

Entry URL: http://127.0.0.1:8876/research/m31-normalizer-ablation-2026-10-17/viewer/

Evidence: attempt-01/report.json, desktop.png and mobile.png. Reproducible driver: run.cjs, using existing Playwright through NODE_PATH and RESEARCH_ROOT/RESEARCH_QA_OUTPUT/RESEARCH_CHROME environment variables. The output directory must be new; the driver preserves an exclusive attempt record.

The unchanged historical iframe owns its own evidence verification. The new parent additionally binds the historical viewer assets and its binding document, plus this attempt's publication/attempt/supervision documents. Fail-closed tests cover five routes, not every possible byte corruption. QA checks historical positions, controls and labeling; it does not independently recompute attitudes, physics, aerodynamic forces or certificates. Other browsers and devices were not tested. A dedicated Browser plugin would improve integrated inspection in future UI work; it was not installed here.
