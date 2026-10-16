# Display verification

The final display run passed **99 checks**, with no recorded console warnings/errors. It covered the 10 saved planes in all 3 modes, all 410 profile records in numeric tables, all 5 source-state selections, 20 witness rows, orbit/reset, mobile layout and refusal of a deliberately corrupted evidence response. Six screenshots preserve the final display states. This is presentation verification; no scientific source or campaign was executed by QA.

The Browser plugin was not available. The already installed Playwright 1.62.1 and Chrome 155.0.8059.80 were used with Node 24.19.0 against the existing localhost server. Desktop viewport: 1440 × 1000; mobile layout: 390 × 844. A mobile viewport is not a test of physical touch hardware. The target flow and 45-second per-script deadline were recorded in [VIEWER-QA-PLAN.md](VIEWER-QA-PLAN.md) before execution.

| Check | Final result |
|---|---|
| Page identity, content and absence of framework overlay | Pass |
| Both saved-file byte lengths and SHA-256 bindings | Pass |
| Plane/mode controls and saved numeric values | Pass |
| Source selectors and unchanged scene after each selection | Pass |
| WebGL canvas, orbit and camera reset | Pass |
| Mobile width and canvas | Pass |
| Corrupted result hash stops numeric display | Pass |
| Console health and browser close | Pass |

All attempts are retained. Attempt 1 failed during sandboxed browser launch, before any page check; its launch log reports SIGABRT and cleanup. Attempt 2 ran outside the filesystem sandbox, passed 77 checks, then failed in the **QA script**, which used `innerText` to read JSON inside a collapsed disclosure. The script was corrected to use `textContent`; no viewer or scientific code changed. Attempt 3 passed all 99 checks and closed the browser in `finally`. These were the initial attempt and two necessary corrections allowed by the plan. No session remains running from the QA calls.

The root inspected desktop, mobile, zero-cutoff and corruption-refusal screenshots. Text and controls fit the tested widths. Small in-scene labels have the same values available in readable HTML text/tables. No claim is made for other browsers, screen readers, real mobile GPUs, interactive performance, simulation speed or fluid validity.

Exact scripts, per-attempt results and screenshots are in [qa/](qa/). `qa/IMPORT.json` records the only public transformations: temporary browser-profile paths, private QA-script paths and ephemeral process IDs in failure logs were replaced by role labels. Scientific values and screenshots were not transformed. Private originals are retained outside the public repository.

To reproduce display QA in a separate output directory, supply the existing Node, Playwright and Chrome paths through the environment and invoke `qa/qa-attempt-3.cjs CHECKPOINT_DIRECTORY OUTPUT_DIRECTORY`. No installation is required. The script assumes the documented localhost URL. Do not overwrite the saved attempts.

Final screenshots: [desktop](qa/attempt-3/desktop.png), [3D scene](qa/attempt-3/desktop-scene.png), [zero cutoff](qa/attempt-3/zero-cutoff.png), [mobile](qa/attempt-3/mobile.png), [mobile scene](qa/attempt-3/mobile-scene.png), [corrupted evidence refused](qa/attempt-3/corruption-refused.png).
