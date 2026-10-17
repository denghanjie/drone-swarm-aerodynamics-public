# Native saved-load viewer source handoff

This is an isolated source-only draft for integration at `research/m31-native-load-baseline-2026-10-17/viewer/`. The projection adapter has not been run. No browser was launched and no scientific module was imported or executed. Existing port 8876 and published research files were untouched.

The source presents three separate facts: all 12 native calls returned; the original outer supervisor failed during cleanup with EPERM; and the later independent saved-record audit qualified all 12 retained calls. The original failure banner is visible in static HTML and remains visible when display or audit bindings fail. The separate audit cannot repair the original operational outcome.

The supplied `AUDIT-LINK.json` binds the actual saved audit at source commit `eb049deb66c4c7aee78826b2eecde8281d02a1b9`, manifest `7ca777cfe98e6498d8cc789244f3f3d14223a45f807c60c7e8a99913d64ac3c1`. Its 52,914-byte report is `e4b93e1b5d03f378b2d7ac254256fcb7deb2e3371dc4dd70136ec6c376974080`. Reading those files confirmed the actual schema, successful supervisor status, 12 qualified calls, six matching F/L parity rows, 14 named arithmetic fixtures and four named corruption checks. This source review does not repeat or extend that scientific audit.

The adapter reads saved native evidence, six raw input records, and the optional four audit records. It checks file pins, semantic input identities, raw ownership, fixed schedules, and exact load-word shapes. It copies saved pose words and actual delivered load words into a compact display file; it does not reconstruct any load. The adapter checks every read pin again before writing. Outputs are exclusive, and the single `app.js` binding marker is patched only after display and binding files are written. Existing outputs cause rejection rather than replacement. Omitting `--audit-binding` deliberately retains Pending and causes no audit requests.

The page verifies its binding and display hashes, then separately verifies all four audit records against their hashes. The audit gates cover publication identity, successful independent supervision, unchanged original failure, original evidence pins, fixed call and parity denominators, named fixtures and corruptions, normalized bounds, support, consumption and output arithmetic. Exact squared upper bounds must satisfy 1e-16 for each qualified category. Audit failure retains the valid native scene while showing pending/unavailable qualification. Native binding failure clears the scene and selected values.

All six snapshots and both methods are selectable. Bodies use decoded saved positions and quaternions. Arrow endpoints are computed only as `saved center + actual returned worldForce × displayScale`, at 1, 4 or 8 scene m/N. Drone glyphs are enlarged 3× and explicitly labeled. The renderer exposes the actual Float32 body positions and arrow upload buffer for later QA. No interpolation, model step, benchmark or certificate is claimed. Static source inspection cannot establish WebGL appearance or browser behavior; those remain pending the bounded plan in `BROWSER-QA-PLAN.md`.

The page uses the repository's existing Three.js and OrbitControls modules. It links the independent package's `SUMMARY.md`, `results/check-attempt.json`, and `results/check.json`; parent integration must create the summary at that stated path. No large native browser record, exact reference, solver, or original checker is fetched at page startup. The native browser file remains an explicit evidence download link.

After source acceptance, the parent can copy the five `viewer/` files to the agreed destination and authorize the administrative adapter explicitly:

```text
python3 viewer/build-display.py --root REPOSITORY_ROOT --output REPOSITORY_ROOT/research/m31-native-load-baseline-2026-10-17/viewer --audit-binding /tmp/m31-native-load-viewer-draft/AUDIT-LINK.json
```

That command is documented only. It was not executed in this source-only handoff. `STATIC-VALIDATION.json` records syntax/schema checks and `SOURCE-PINS.json` inventories the final draft.
