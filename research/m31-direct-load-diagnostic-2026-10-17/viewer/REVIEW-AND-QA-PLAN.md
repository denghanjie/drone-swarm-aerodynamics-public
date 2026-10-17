# Direct-load viewer draft — source review before builder execution

Status: **source-only draft, builder not executed**. No `binding.json` or `display-data.json` has been generated. Files are staged here for parent review before copying to the package viewer directory. Scientific modules were neither imported nor rerun; no candidate, frozen source/input or accepted result was modified. Python AST parsing and JavaScript syntax-only checking passed.

## Display contract

- Retain the accepted oracle-renewal visual system and unchanged `scene.js`. The six actual saved snapshots use the original input-order pose words, matched against prior generation frames and slots. No pose interpolation, new trajectory or force-driven motion.
- Default to the fixed omission proposal. Amber segments represent exactly the saved omitted positive `(receiver stable ID, rotor index, source stable ID)` mask. Endpoints come from saved prepared source centers and receiver rotor points. ID lookup is independent of positional array index. The full control shows zero omitted links. Tolerance changes never change a mask.
- Keep six rows at every tolerance and category. The overview includes full A/B and omitted A/B/C. Its statuses apply to all four load categories; the selected category controls the error interval/upper-bound shown beneath each status. A second table shows every category for the selected state and candidate. Full C is explicitly not applicable.
- Preserve exact rational error intervals and saved decisions in the compact projection. Rounded scientific-notation labels are display formatting only; exact intervals remain available in cell titles and an expandable JSON view. No threshold decision is recomputed from rounded display values.
- Distinguish integrity-check success, A numerical accuracy, and B/C certificate sufficiency. Show strict failure in all six omission cases and retain the stress failures. Explicitly disclose reused dependent states, airflow-off recorded flight, oracle-assisted post-hoc loads, no live physics, no speed/scale claim, and no physical 1% interpretation of the stress tolerance.

## Builder review points

`build-binding.py` uses standard-library JSON/hash/path operations only. It contains no dynamic scientific import, solver call, coefficient computation, candidate update, mask selection or proof recomputation. It copies saved summaries after requiring exact agreement with the accepted independent checker outcomes.

The builder pins the accepted source commit `ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf`, source manifest `93d26849dcd0a86d18b254f8eb5babc3d13e0f46d08efc92dfc2bc5cef79635b`, and all four accepted result byte hashes. It verifies all 159 source/input pins before and after preparation, completed attempt/output bindings, checker completeness, publication receipt identity, and checker input/reference hashes. Prior index/check/generation/input/reference files are checked against frozen pins. The canonical semantic input envelope hash is kept separate from the input file-byte hash.

All validation occurs before output. The only write targets are fresh `viewer/display-data.json`, fresh `viewer/binding.json`, and the single binding-hash marker in `viewer/app.js`. The output directory must be the canonical package viewer directory; existing display builds are refused. Partial build artifacts must be preserved and reviewed rather than overwritten. Source and result records are read only.

The browser validates the fixed binding SHA, compact-data SHA/size, source identity, six-state schedule, pose/ID mapping, mask geometry and audit structure before displaying claims or poses. Failure disables controls, withdraws numerical claims, hides the scene and retains six placeholder rows. Browser requests are limited to binding/display data and local rendering assets; provenance file links load only when explicitly followed.

## Proposed approved build command

After parent source review and approval, copy the five viewer files and builder to `research/m31-direct-load-diagnostic-2026-10-17/viewer/`, then invoke the builder with the explicit repository root, that viewer directory, accepted commit and manifest hash. This document does not execute that command or allocate another scientific attempt.

## Bounded actual-browser QA after build acceptance

Use the existing localhost server without starting or modifying it. Preserve each attempt under the package `qa/` directory, with maximum 60 seconds per attempt and at most three viewer-only repair attempts. Use the installed Chrome/Playwright fallback if Browser/IAB remains unavailable; no installation is needed.

1. Verify all 36 state/candidate/tier combinations: 64 rendered centers against saved pose words, fixed omission link counts, exact candidate identity, all four selected-detail category decisions and preserved six-row overview. Check all link endpoints for each of the six masks against saved stable-ID reference geometry, including actual uploaded Float32 line coordinates.
2. Verify all 12 tier/category overview projections against accepted saved A/B/C summaries, intervals and status labels. At stress retain both failed A states; at strict retain all six A failures. Confirm full A/B outcomes and explicit full-C absence.
3. Exercise snapshot buttons, proposal/tier/category controls, overlay hiding/restoring, stale-link clearing, orbit, zoom and reset. Mask counts must be independent of tolerance; pose words must be independent of candidate selection.
4. Inspect desktop/mobile screenshots, readable controls and tables, table scrolling, meaningful scene rendering, console errors/warnings and local-only display requests. Capture both strict failure and stress mixed-outcome views.
5. Corrupt binding and compact data separately; verify every numerical claim and pose is withdrawn with six overview placeholder rows and disabled controls. Preserve failures and screenshots.
6. Compare all 159 immutable pins and four accepted result hashes before/after QA. Inspect screenshots manually and record browser/viewport limitations. No science reruns, candidate changes or threshold tuning.

Parent owns milestone summaries, next-decision prose and publication. This draft adds only the saved-evidence viewer.
