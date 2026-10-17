# Native-load viewer QA closeout

Attempt 02 passed all 198 checks and the complete fixed schedule in 16.380440083 s of supervised wall time. Attempt 01 remains failed; its harness-only closed-details read error and exact repair diff are retained. No viewer, scientific source, projection or numerical record changed between attempts.

Environment: installed Chrome 155.0.8059.80 through Playwright 1.62.1, desktop 1440 × 1050 and narrow 390 × 844, one fresh private profile per attempt. Browser plugin was unavailable. Existing localhost port 8876 server remained PID 48039; no restart occurred. The Browser plugin can be installed for future integrated browser work.

| Check | Result |
| --- | --- |
| Page identity, meaningful screen, no framework overlay | Pass |
| All 12 state/method combinations, 64 centers and force endpoints each | Pass |
| Exact projection of all 8,448 returned load words and six raw pose mappings | Pass |
| Actual WebGL shaft uploads and draw counts; scaled endpoint formula | Pass |
| Selected load words, exact field addresses and saved audit rows | Pass |
| Scale 1/4/8, arrows hide/show, stable ID, orbit/reset, table navigation | Pass |
| All six outcome rows, separate original failure and independent audit | Pass |
| Two isolated corrupt native/audit tabs and stale-value clearing | Pass |
| Mobile selectors, bounded controls and horizontal table access | Pass |
| All 20 local evidence links, including MILESTONE-SUMMARY.md | Pass |
| Page errors, console warnings and failed requests | Zero in all three scenarios |
| All 340 frozen sources, numerical records and viewer files | Byte-identical before/after both attempts |

Attempt 02 used graceful Browser.close, confirmed the owned root/controller exit 0, reaped it, and removed its private profile. No forced termination or process-group signal was used. QA child and outer supervisor exited 0. The recorded artifact volume was approximately 1.84 MB, within the 32 MiB cap. This supports the recorded viewer presentation only; it does not add a scientific calculation, benchmark, physical validation or certificate. The original native supervisor failure remains failed, while the separate saved-record audit remains its own qualified result.

Visual inspection of the two retained screenshots shows the permanent red failure disclosure, distinct green saved-audit result, scaled gold thrust arrows, readable desktop controls and a narrow layout with internal table scrolling. Only these two final screenshots were captured in attempt 02. Parent inspection remains independent.

The tested flow was viewer load → all six saved snapshots × F/L → scale/ID/visibility/camera controls → narrow layout → evidence links → native/audit corruption → clearing stale values. Source preparation used syntax checks; execution used the environment-configured Python supervisor and Node QA source, with no private runtime fallback paths.

Remaining limits: one named Chrome version, two viewport sizes and the six retained states. No additional browser attempts are needed after this pass. Full helper-process attestation or an enforced memory ceiling is not claimed.

Artifacts: `attempt02/report.json`, `attempt02/attempt.json`, `attempt02/desktop.png`, `attempt02/mobile.png`, both immutable snapshots, exact `QA-HARNESS-DIFF.patch`, and preserved failed `attempt01/`.
