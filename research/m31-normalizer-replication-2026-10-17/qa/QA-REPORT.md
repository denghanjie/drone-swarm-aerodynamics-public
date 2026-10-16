# Replication viewer QA

The viewer is bound to the actual saved replication result. It shows correctness and admission passed, benefit not passed, six of six states verified/certified, and zero of six states satisfying the registered benefit rule. Checker exit 1 and closed/normal-release supervision are displayed separately. Both new runs have 51 saved frames for 64 drones. No scientific source or result was edited and no scientific kernel/checker was rerun.

## Findings and bounded repairs

1. Attempt 01 stopped after eight wall values because the QA harness read rendered text inside a collapsed timing detail. The harness now expands each detail before checking visible values. The attempt and its script are retained.
2. Attempt 02 verified all 102 frames and all 48 wall values, then found that pending OrbitControls damping could carry motion into Reset view. The viewer now drains pending control deltas before restoring the saved-flight camera. This is a viewer-only fix. Pre-fix viewer/script evidence is retained.
3. Attempt 03 passed all 266 checks in 9,555 ms, within the 60-second bound. A supplementary mobile capture verified horizontal access to every evidence-table column. An immediate post-scroll screenshot briefly captured an unpainted table; settled screenshots and DOM/scroll evidence show the complete table. No additional app fix was needed.

## Environment and scope

- URL: `http://127.0.0.1:8876/research/m31-normalizer-replication-2026-10-17/viewer/`.
- Existing local server reused. Installed Playwright and Google Chrome used; no dependency installation.
- The in-app browser was attempted first and returned `Browser is not available: iab`. The parent explicitly authorized the installed Playwright fallback. Browser execution used the approved escalated context for local Chrome/localhost access.
- Viewports: desktop 1440×1050; mobile 390×844.
- Flow: bound evidence loads → six states and 24 pair rows → both saved flights → play/pause, seek, orbit, zoom, reset → desktop/mobile presentation → corrupted response rejection.
- The viewer's builder reads and pins saved JSON only. It imports no research modules. Browser code imports only display code and the existing Three.js/OrbitControls dependencies.

## Verification

| Check | Result |
|---|---|
| Page URL/title and meaningful screen | Passed |
| No framework error overlay | Passed |
| No browser errors or warnings on accepted evidence | Passed |
| Three distinct research gates; checker exit 1 remains separate | Passed |
| All six scheduled states retained | Passed |
| All 24 planned baseline/candidate pairs retained | Passed |
| All 48 complete-wall values equal saved check/index nanoseconds | Passed |
| All 102 frames: run, frame, time, 64 bodies, 448 words | Passed |
| All 19,584 rendered center components equal float32 rendering of saved binary64 positions | Passed |
| Run selection, exact scheduled seek, slider, play/pause | Passed |
| Orbit, zoom and repaired camera reset | Passed |
| Desktop/mobile page has no horizontal overflow | Passed |
| Mobile run, slider and playback | Passed |
| Mobile table scroll exposes admission, benefit and all pair counts | Passed |
| Eight corrupted binding/evidence responses withdraw claims and poses | Passed |
| Corruption keeps six states and 24 planned pair slots visible | Passed |
| No scientific source or unrelated-origin browser requests | Passed |
| No implicit historical replay substitution | Passed |
| Local targets for all five links exist | Passed |

Corruption tests intercept responses in separate browser pages; no saved evidence file is modified. The eight cases cover the binding plus all seven bound files: kernel attempt, kernel supervision, checker supervision, index, checker report and both generation records. Rejection leaves research gates unassessed, disables playback and renders no aircraft.

## Visual review

The existing validator viewer is the design reference, saved as `attempt-03/reference.png`. There is no new generated design concept: this work extends the existing viewer design system. `view_image` inspection was performed on the reference and the latest desktop, evidence, mobile replay/table and corruption screenshots.

| Comparison | Evidence and disposition |
|---|---|
| Palette and surfaces | The navy page/canvas, blue-gray panels, mint positive state and amber negative gate remain consistent with the reference. |
| Typography | Heading, body, table and control typography are readable and retain the reference hierarchy. Mobile title and controls wrap without overlap. |
| Layout and spacing | Desktop keeps the wide replay plus explanation/checkpoint rail. Mobile stacks the same content. The added three-gate strip is required by this task. |
| Real visual content | Visible aircraft use the new saved centers and attitudes; no generated or historical positions are substituted. Enlarged glyphs and thrust-axis styling are disclosed. |
| Controls and state | Run, play/pause, seek and reset use the reference control family; the current scheduled checkpoint is visible. Reset's residual-motion defect was repaired. |
| Evidence density | All six rows remain present. Four pairs per state are expandable. Mobile tables scroll horizontally rather than hiding columns or removing failed states. |
| Copy and claim separation | The visible heading, fixed-denominator explanation, airflow-off/posthoc disclosure and playback-versus-compute distinction are present. New copy implements the requested replication content; no unrelated marketing or performance claim was added. |
| Error state | Corruption visibly withdraws accepted data and replay while preserving the planned denominator. |

The implementation was faithfully checked against the reused design, with intentional changes for the three research gates, new six-state/24-pair evidence and separate operational record. No material visual mismatch remains in the inspected desktop/mobile states.

## Preservation and evidence

`PRESERVATION-CHECK.json` confirms 126 source/result files unchanged, unchanged membership, all 169 frozen source-manifest pins matching, and manifest bytes matching source commit `08ed31c184f88f95217dca689d3727c44c75e8c4`. The binding digest is `94fcd7ec8e8d72842119600e32d313c800bdd003f093bc7fd9ced3949d6e6489`.

- Main machine-readable result: `attempt-03/report.json`.
- Main screenshots: `attempt-03/desktop.png`, `desktop-evidence.png`, `corruption.png`.
- Legible mobile screenshots: `mobile-final/mobile-first-viewport.png`, `mobile-replay.png`, `mobile-evidence-settled.png`, `mobile-evidence-right.png`.
- Supplementary mobile evidence: `mobile-final/mobile-table-check.json`.
- Retained preparation: viewer `SOURCE-DRAFT-CHECK.json` and QA plan, labeled as prior source-only preparation.
- Key APIs: Chromium launch, page navigation, locators, select/input/click, canvas mouse/wheel, viewport changes, response interception and screenshots. No scientific entry point was invoked.

Remaining limits: one installed Chrome engine and two viewports; aircraft centers were numerically compared, while attitude use follows the saved-word renderer and was visually reviewed rather than separately extracting every rendered rotation matrix. No-new-poses fallback remains source-reviewed because this actual result contains both complete flights. The viewer does not establish physical validity, aerodynamic feedback, persistent-process/browser compute benefit, or between-snapshot admission.
