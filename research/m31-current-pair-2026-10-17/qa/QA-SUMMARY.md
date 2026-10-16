# Display-only QA closure

Both allocated display attempts are closed. No scientific kernel, fixture generator, independent oracle or new trajectory was rerun by display QA.

Attempt 01 failed before its checks: the locally vendored OrbitControls module imports the bare specifier `three`, and the new page lacked an import map. The browser reported this module-resolution error and the readiness wait timed out. Wall 35.809s. The failed report, exact tested viewer and QA source are retained.

Correction: add an explicit local `three` import mapping to the already pinned vendor module. Rebuild the display binding to match the corrected page. Add bounded screenshot capture on a failed display attempt. Neither scientific source nor numerical results changed.

Attempt 02 passed all 37 checks in 3.125s, with no console errors or warnings. It checked the 322 saved cases, pair canvas/case selection, visible statuses including invalid and unresolved inputs, explicit static/no-new-flight and airflow-off labels, 5,000-drone historical replay/playback, evidence links, mobile layout and fail-closed display behavior under corrupted bindings/model text and late historical-replay failure. Desktop/mobile pair and historical-swarm screenshots, exact tested viewer and QA source are retained.

The parent visually inspected desktop and mobile pair screenshots. Geometry, case selector, status and limitations are visible; default drone markers are small relative to the separation, with orbit/zoom available. Displayed interval endpoints are rounded for presentation and explicitly labelled; they are not substitute bounds. No third QA attempt is authorized or needed for this unchanged display.
