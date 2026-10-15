# Saved wake evidence viewer QA

The saved-data Three.js viewer passes its final UI checks. It shows the independently verified numerical failure, the actual source contributions, and the unexecuted serial stage. It does not run a scientific model.

Environment: http://127.0.0.1:8876/research/m31-browser-wake-slice-2026-10-16/viewer/ ; Chrome155.0.8059.40, Playwright1.62.1, desktop1440×1080 and mobile390×844. Browser plugin not available; installed Playwright was the documented fallback. Existing server/vendor files reused; no dependencies installed. The user requested committed milestone traces and screenshots.

Flow under test: load saved evidence → select receiver/rotor/source and display mode → inspect original values, numerical failure and unavailable reduction → switch between focused contributors and the full5000pose cloud.

|Check|Result|
|---|---|
|Page identity and meaningful content|PASS|
|Framework overlay / console health|PASS; no relevant errors in final run|
|Recorded negative result and missing serial output|PASS|
|All16rotors, first/self/last/largest-error sources|PASS;65source cases and195R/Q/Tvalue/status comparisons|
|Saved sums and exact-certificate display components|PASS; decisions read from retained reports|
|Three color modes, links, focus/whole camera controls|PASS; focus hides unrelated glyphs, whole restores5000|
|Evidence/navigation links|PASS|
|Mobile page overflow and controls|PASS; wide tables scroll within their own region|
|Intercepted corrupt term bytes|PASS; explicit checksum rejection, no scene unlocked|
|Visual inspection|PASS; final desktop focus/whole and mobile screenshots inspected|

Final script reports491checks,195pairchecks,65sourcecases,16receiver–rotor pairs,0errors. The script and machine report are viewer-qa.cjs/viewer-qa.json. Sources are bound by the result manifest. These UI comparisons are not a second scientific validation invocation.

Preserved findings: first UI run timed out before readiness because OrbitControls' bare three import lacked an import map. A diagnostic browser read captured the error and viewer-loading-failure.png. The page now maps the local Three.js vendor and uses a data favicon. The second run passed489checks; screenshot inspection then revealed that unrelated enlarged glyphs obscured local contributors. The final UI-only visibility change filters those glyphs in focused mode, clearly labels that filter and restores all poses in whole mode. Earlier reports and screenshots remain under viewer-qa-attempt-1/2.json and before-focus-filter-*.png. No scientific bytes, tolerance, selected IDs or reviewer code changed.

The final source also replaces 'saved flock' with 'saved scene' and explicitly says the planned reduction was skipped. The original static viewer inventory is retained as preparation provenance, not as the final-byte inventory. The result manifest binds the final code.

Remaining limits: one browser and two viewport sizes; canvas source-picking/orbit/zoom were implemented but not exercised by the automated script. Only the real absent-reduction state and one intercepted corrupt-term fixture were tested; other planned corrupted-review/partial-reference fixtures were not executed. Successful UI checks do not establish physics, timing, portability or fleet-wide accuracy.

Screenshots: desktop-focused.png, desktop-whole.png, mobile-focused.png. They show static evidence, not simulated flight.
