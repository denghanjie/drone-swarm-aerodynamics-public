# Independent static review of the separate display recovery

23 October 2026. **Statically acceptable for one separately frozen display-only allocation**, subject to the exact recovery manifest and independent public verification. No recovery, browser, numerical diagnostic, control, auditor or model was executed during this review. The original failed UI allocation remains closed and is not relabeled or reopened.

## Established failure and remaining uncertainty

The saved original `ui/qa.json` records four completed groups: page/clip identity, all 1,920 historical position/status/count records with refusal labels, aggregate/limit labels, and all 1,920 new diagnostic annotations. It then records the unchanged-camera assertion at original `source/ui.cjs` line 15. The original code did not reach its desktop/mobile screenshots, overflow assertions or altered-evidence rejection check. The completed four groups do not amount to an original full UI pass.

Original input code used the center of `#scene` without scrolling the canvas into view or recording viewport/hit-test evidence. An off-screen or otherwise mistargeted mouse sequence is a plausible explanation, not an established cause. The failed receipt has no old target rectangle or pointer-hit evidence. A successful corrected sequence could establish that sequence works; it cannot retrospectively identify the old failure's cause.

## Recovery delta and interaction evidence

The final `ui-recovery.cjs` retains the original data/label, playback/selector/slider/focus/toggle, screenshot/overflow and changed-evidence checks. It writes to a separate exclusive `ui-recovery/` directory. It does not edit or overwrite the viewer, original script, original UI output or numerical evidence.

The drag now targets `#scene canvas` explicitly. It scrolls that element into view and waits two animation frames before obtaining its rectangle, viewport dimensions, scroll position, start point and fixed end point. The end remains a single prescribed 70-pixel horizontal/30-pixel vertical displacement, delivered in eight steps. Both endpoints must lie in the viewport and `elementFromPoint` must identify the exact canvas at both endpoints. Target evidence is saved before that assertion, so a targeting failure retains its measured geometry.

It saves the camera before input, performs one genuine pointer drag, waits two frames, and saves the resulting camera. Both camera arrays must contain three finite values, and at least one coordinate must change by more than the prospectively fixed 1e-6. This avoids accepting only insignificant numerical drift and does not set the camera directly to manufacture a pass. The visible reset control is then clicked; its resulting camera is saved and checked against the earlier position within 1e-10 per component.

An early recovery draft calculated camera movement with `Math.hypot`, conflicting with the protocol's literal prohibition on new norm calls. Before freeze, that was replaced with finite-array and absolute-coordinate-difference comparisons. The reviewed script has no direct `Math.hypot` call and imports only standard Node utilities and Playwright. It imports no candidate, producer, scientific model, certificate or independent auditor module. Display/rendering arithmetic and reading existing records do not constitute a new scientific result.

The new interaction records are `pointer-target.json`, `camera-before.json`, `camera-after.json` and `camera-reset.json`. The fixed sequence has no adaptive drag retry, relaxed-on-failure threshold, alternate target search or direct camera manipulation. A failure remains a failed new attempt with its available records retained.

## Coverage and publication prerequisites

This recovery elects to recheck all 1,920 earlier records and all 1,920 new annotations once, rather than relying solely on their earlier passing UI groups. These are comparisons and rendering of saved, hash-bound evidence. No distance/certificate calculation, native query, controller/integrator, audit or finalizer is invoked.

The copied checks retain the historical refused trial, finite-only/no-speedup wording, playback, focus and threshold illustrations. After orbit/reset, they require desktop/mobile overflow checks and screenshots, then intentionally replace the served diagnostic-stage response and require evidence-identity rejection with no canvas. Browser/page/HTTP errors remain failure conditions. Parent inspection of both saved screenshots is still required; static review cannot determine their actual appearance.

The new manifest must bind the complete original source and input inventories, original source manifest and publication gate, all successful producer/audit/finalizer evidence, original failed UI lock/supervisor/QA records, viewer pins, the recovery protocol/scripts and this review. It must exclude itself, the later publication gate and future recovery outputs. Public verification must establish those precise bytes before launch. This review does not substitute for that identity gate.

The recovery supervisor checks the recovery publication receipt and every listed local byte pin before spawning the browser checker. It requires successful original producer/audit/finalizer supervisor records, a closed original UI failure, and absence of a prior recovery output directory. The browser checker separately validates the original source-publication flags/source hashes and the viewer evidence pins before opening the page. Thus the recovery uses its own publication gate as well as the unchanged original evidence gates.

## Separate allocation and failure behavior

The supervisor creates `ui-recovery-supervisor-launch.lock` exclusively before dispatch. It checks the installed Node executable size/hash, removes inherited Node/Python override variables, declares the bundled package location, and launches a new child process group. It monitors the 150-second/16-MiB allocation, terminates the child group on failure/limit, and writes a separate exclusive supervisor closure. The checker also uses an exclusive output directory, a 145-second internal stop and a 512-KiB output reserve for its final QA record.

Those bounds include display work only and are not performance measurements. A hard kill or physical write failure can leave incomplete evidence and must not be reported as a pass. The supervisor's failed closure and preserved lock prevent reuse. The unpinned Python, Playwright and browser environment limitations remain explicit. No second attempt, new scientific execution or old-allocation reopening is authorized by this recovery protocol.

## Result-claim wording inspected separately

The current `SUMMARY.md` and `RESULT-CLAIMS.md` clearly distinguish proposed omissions from operations actually saved; conditional mathematics from unresolved installed-runtime conformance; per-stage aggregate consistency from historical per-pair equality; and numerical results from the original failed display attempt. They still describe recovery as pending. This reading assesses claim scope only. Exact numerical result identities/counts and final display outcome belong to the dedicated saved-result review after closure and are not independently verified by this recovery-source review.

## Exact reviewed identities

Paths are relative to `research/m31-radial-certificate-2026-10-23/`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `DISPLAY-RECOVERY-PROTOCOL.md` | 2,760 | `2f9d07b7421b4a241859cedfa3dec2c3cf0edbf6f98df91efb6fe8634280febf` |
| `source/ui-recovery.cjs` | 10,202 | `0616ee480da93f1c67ddad33ff4be723280278d86409197feb15885d2c715fee` |
| `source/supervise-ui-recovery.py` | 4,215 | `d34e0dec2d1b3f1a1475401675c82d23cc4b9be15fe0b4f82c55f48030b2f271` |
| Original `source/ui.cjs` | 9,102 | `a8a431116a1b6fe44e908664e7fecb6ba95b470c148b2c16013fb91da412a9a7` |
| Original `ui/qa.json` | 552 | `c5075140eb7bf67dfd096ee8c9c81c67b8ac8d6f361ddbffd8c1831148aeb3a3` |

The original UI source still matches its original frozen identity. Any subsequent recovery source/contract edit needs a static delta review before publication and launch. No remaining material defect was identified for this fixed display-only recovery. Universal numerical correctness, full-native equivalence, speed, physics and safety claims remain outside its scope.
