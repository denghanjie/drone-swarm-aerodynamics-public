# Replication recorded-flight viewer — bound saved evidence

This viewer is bound to seven saved replication files from source commit `08ed31c184f88f95217dca689d3727c44c75e8c4`. Both runs contain 51 actual saved frames for 64 drones. All six states are independently verified and certified; all six fail the registered benefit gate. The viewer keeps those outcomes separate from checker exit 1 and closed process supervision. No scientific work was rerun to build or test this display.

The source adapts the validator/moving viewer's dark layout, Three.js aircraft geometry, binary64 pose decoder, camera bounds, orbit controls and playback. This is an extension of that existing design system, not a new visual concept. Geometry depicts actual recorded pose words only. No image-generation concept, generated flight, aerodynamic solver or scientific module is used.

## Files

- `index.html`, `style.css`: compact three-gate summary, recorded-flight view, six-state table, six expandable four-pair timing tables, execution/provenance section.
- `scene.js`: display-only Three.js renderer. Glyph size is 3×; centers and attitudes remain saved values. No interpolation or synthetic pose fallback.
- `app.js`: hash-checking saved-data display adapter, six-state fixed denominator, separate correctness/admission/benefit gates, all four complete-wall pairs for every state, explicit missing/refusal behavior.
- `build-binding.py`: a data-only builder prepared for the later results signal. It reads known saved JSON files and emits a hash-bound binding; it imports no research modules and calls no scientific computation. It was invoked once for the saved replication results; `binding.json` is pinned by `app.js`.
- `QA-PLAN.md`: original deferred QA checklist; completed evidence is in `../qa/QA-REPORT.md` and the retained attempt directories.

## Binding and retained preparation instructions

The parent authorized copy and binding after both stages closed. The original draft was copied into `research/m31-normalizer-replication-2026-10-17/viewer/` under that instruction. The relative vendor imports resolve to the existing `outputs/step02b-source/vendor/three.module.js` and `OrbitControls.js` in the repository. Do not serve this `/tmp` directory as a pretend bound viewer.

The builder was invoked with the repository root and copied viewer directory. The builder requires a real kernel-attempt marker, validates new package/source identity, preserves the six scheduled states, and only includes actual saved files. No existing binding is overwritten. Parent review and immutable artifact pins precede public publication and browser QA.

If the kernel saves partial results, missing records and pairs stay missing. A failed benefit gate does not hide a saved independent correctness result. A scientific checker exit code 1 can be the expected consequence of a false research gate; the viewer displays saved stage status separately. The browser does not recompute scientific correctness or the benefit verdict.

If there are no new pose frames at all, show a labeled link to the historical validator replay. Do not embed or silently substitute historical frames. If just one new run has poses, only that run is playable; the other remains unavailable.

## Data and claims

Pinned inputs are the kernel attempt, optional kernel/checker supervision, optional index/checker report, and optional new run-a/run-b generation records. Full-wall numbers come from index call descriptors; saved ratio/median/win/benefit values come from the checker. Where both are present, the viewer compares the pair's saved nanoseconds. All source identity fields must agree. Generation IDs, seeds, airflow-off configuration and frame dimensions are checked before display.

Scientific truth remains in the source artifacts and independent checker. This viewer verifies display bindings; it does not replace a numerical validator or make novelty, physical-validity, feedback, browser-performance or large-swarm claims.

## Verified display

The installed-Playwright fallback was used after the in-app browser reported unavailable. Final bounded QA passed 266 checks in 9.555 seconds, including all 102 frames / 19,584 rendered center components, 48 complete-wall values, desktop/mobile controls and eight digest-corruption cases. A camera-reset damping defect was fixed in this viewer only. A supplementary mobile capture verified horizontal access to all table columns. See the retained report for screenshot review and limitations.
