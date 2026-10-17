# Browser QA — renewal saved-data viewer

**Passed.** Attempt 03 completed 551 checks in 7.772 seconds using installed Google Chrome 155.0.8059.80 through Playwright 1.62.1. The viewer URL remained `http://localhost:8876/research/m31-oracle-omission-renewal-2026-10-17/viewer/`. The server was neither started nor changed.

## Scope and result

- All 36 snapshot / proxy-tier / tree combinations matched the accepted saved analysis, including all six table rows, denominators, percentages and selected-tree work counts.
- All 64 rendered drone centers matched the saved binary64 pose words after the renderer's Float32 conversion at every combination: 2,304 body checks and 6,912 coordinate checks.
- Only `run-b-t10 / 1e-2 / T2` displayed links: 2 of 163 positive terms. Every other combination displayed zero links.
- Both last-state links used stable source IDs 30 and 4, receiver ID 8, rotor index 3. Their endpoints matched the saved prepared source centers and receiver rotor point. The first 12 components actually uploaded to the WebGL overlay buffer also matched the expected Float32 endpoint coordinates.
- Overlay hiding retained the selected count while hiding both links; restoring overlays restored both. Switching snapshots cleared stale links. The last table-row control returned to the exact 10-second state.
- Orbit and wheel zoom changed the rendered canvas. Reset restored the original canvas screenshot byte for byte.
- Desktop (1440 × 1050) and mobile (390 × 844) rendered without page-level horizontal overflow. Mobile controls worked, and horizontal table scrolling exposed the final columns while retaining all six rows.
- Separately replacing `binding.json` and `display-data.json` with `{}` withdrew numerical claims and poses, disabled controls, and retained six placeholder rows. Neither case displayed a visible scene canvas.
- The primary viewer emitted no console warnings, console errors or page errors. Its nine recorded requests were local display assets/data only; no scientific source request occurred.

This is saved-display QA. It does not add a scientific run, certify load accuracy, establish a speed benefit, or demonstrate 5,000-drone/browser feasibility. Mobile checks used a resized desktop Chrome viewport; physical touch devices and other browser engines were not tested.

## Preserved attempts

| Attempt | Duration | Outcome |
| --- | ---: | --- |
| 01 | 0.076 s | Stopped before opening the viewer: the default Playwright headless-shell executable was absent. |
| 02 | 0.108 s | Stopped before opening the viewer: installed Chrome aborted under the filesystem sandbox. |
| 03 | 7.772 s | Passed using the installed Chrome channel with authorized local browser launch outside the sandbox. |

Every attempt remained below 60 seconds and retained its script, viewer-source snapshot, report and before/after immutable inventory. No dependency was installed. The sole QA-script adjustment selected the installed Chrome channel. **No viewer repair was needed.**

## Screenshot inspection

All 14 PNGs in `attempt-03/` were opened and visually inspected.

- `desktop-first-viewport.png` and `desktop-selected-overlay.png`: readable title, status, controls and disclosures; the 64-drone scene rendered; amber links appeared for the sole nonempty selection.
- `desktop-evidence.png`: all six table rows, their denominators and the last-state 2 / 163 result were legible. The count and diagnostic caveats remained visible.
- `controls-before.png`, `controls-orbit.png`, `controls-zoom.png` and `controls-reset.png`: camera rotation and zoom visibly changed the view; reset returned to the original framing.
- `mobile-first-viewport.png` and `mobile-overlay.png`: text and controls wrapped within the narrow viewport; the scene and both amber links remained visible. The scene occurs below the introductory content and is accessible by normal vertical scrolling.
- `mobile-table-left.png` and `mobile-table-right.png`: the wide table uses its own horizontal scroll area. Both ends were accessible; header text wraps extensively but stays readable. All six rows remained present.
- `corrupt-binding.png` and `corrupt-display-data.png`: clear evidence-unavailable banner, withdrawn counts, disabled controls and empty scene with rejection text.
- `reference-replication.png`: the renewal retained the prior viewer's dark teal panels, mint glyphs, typography and evidence hierarchy. The renewal uses fixed saved snapshots and amber coefficient links.

No blocking visual defect was found in these captures.

## Preservation and evidence

`IMMUTABLE-BEFORE.json` and every attempt's before/after inventory compare the 61 frozen source/input pins, the source manifest and four accepted result files. All comparisons passed. The final administrative inventory is `FINAL-PRESERVATION.json`.

Accepted viewer data digests also remained unchanged:

- `binding.json`: `8be075947e19308f885b9e2caef6218db0fcef26e381efa92b66d27d4373c297`
- `display-data.json`: `dc368b8248a2694b8ce2763bbfe8cd286338b84ad01ce1dfda6a2533e2c166fb`

Machine-readable checks and exact endpoint values are in `attempt-03/report.json`; launch failures are in the first two attempt reports. `ARTIFACT-MANIFEST.json` lists QA artifact sizes and SHA-256 hashes, excluding itself. No scientific source or result file was modified or rerun during QA.

## Public log sanitization

Before publication, personal home and temporary browser-profile paths in the two failed-launch reports were replaced with placeholders. Original reports and the prepublication QA manifest remain private. All failure outcomes and scientific data are preserved. `PUBLICATION-SANITIZATION.json` records original and public hashes; the QA manifest binds the public bytes.
