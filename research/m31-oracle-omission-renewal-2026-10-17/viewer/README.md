# Oracle snapshot viewer — source-only draft v2

Copied from the first draft, which remains unchanged. Not executed, target-bound, syntax-tested or browser-QA'd in this delegation. No binding or display-data file is included. No scientific package or frozen file was edited. The parent owns review, integration, accepted-result binding and browser QA. See `CORRECTIONS.md` for the exact identity corrections and source-writer evidence.

Files: `index.html`, `style.css`, `scene.js`, `app.js`, `build-binding.py`. The scene and visual style reuse the prior normalizer replication viewer; `createReplay(...).setOverlays(segments)` adds amber world-coordinate line segments. This draft deliberately offers exact snapshots only, with no animation/interpolation or optional full-flight play.

## Integration after accepted analysis

1. Review these sources against the final frozen analyzer/checker schema. Copy the five viewer files into `research/m31-oracle-omission-renewal-2026-10-17/viewer/` in the public checkout after the parent accepts both analysis and independent check. Keep numerical sources/results unchanged. The separately allocated renewal keeps analysis schema `m31-oracle-omission-screen-v1`; a package-path change does not rename that schema.
2. Confirm source commit and manifest SHA-256 from accepted analyze/check attempts. Run the saved-data builder only then:

```sh
python3 research/m31-oracle-omission-renewal-2026-10-17/viewer/build-binding.py \
  --root REPOSITORY_ROOT \
  --output REPOSITORY_ROOT/research/m31-oracle-omission-renewal-2026-10-17/viewer \
  --source-commit ACCEPTED_ANALYSIS_SOURCE_COMMIT \
  --source-manifest-sha256 ACCEPTED_ANALYSIS_MANIFEST_SHA256
```

3. The builder verifies completed renewal stage attempts, output digests and the checker's successful schema/full verification counts; requires frozen input/reference file-byte pins; independently checks canonical envelope input identities; binds prior numerical/admission evidence independently of its failed speed gate; and matches each saved 0/5/10-second generation frame and slot to its input words. It copies prepared source centers and receiver rotor points from saved reference words and uses saved pair i/j directly as stable IDs. It writes compact `display-data.json`, its `binding.json`, and the binding digest into `app.js`. It imports no research code, recomputes no coefficients, reruns no selection and generates no poses.
4. Serve the repository root through the parent's existing approved viewer setup. Vendor imports use the same `outputs/step02b-source/vendor/` assets as the replication viewer. This `/tmp` draft is not a standalone hosted site. Do not alter localhost:8876 as part of this draft task.
5. Freeze/pin the final viewer files and compact display artifacts with the result checkpoint after QA. Input paths in binding/output remain repository-relative; no local private paths are emitted.

The builder is intentionally fail-closed and refuses existing `binding.json` or `display-data.json`. Preserve a failed/replaced display build and use a separately reviewed fresh directory; do not overwrite QA history. Renewal checker and runner source schemas were read for v2. Completed/zero-exit attempts are still required: merely finding analyze/check outputs does not establish acceptance after the renewal runner's post-output peak-RSS gate. This is an observational acceptance gate, not a hard memory ceiling; the viewer makes no memory-performance claim.

## Intended UI and future QA

- Six saved snapshots, three fixed tiers and T8/T2. The all-six table remains visible, including empty selections; no state or term denominator is removed. The 10% display is explicitly a count hurdle, never a speed or accuracy verdict.
- Amber links show every selected positive rotor–source term, without sampling or a silent visual cap. Endpoints come from source-center to receiver-rotor-point saved words. Aircraft glyphs are 3×; endpoints remain unscaled. Muted stems show aircraft axes, not selection links.
- Clear disclosures: oracle already knows exact-reference answers; no live approximation; prior flights had airflow off; proxy tiers are not achieved load tolerances; `1e-2` is not physical 1% accuracy; no wake-streamline interpretation.
- After binding, verify all 36 snapshot/tier/tree combinations against saved counts, including zero-link cases; check state times, both trees and nonmonotonic counts without smoothing. Inspect a few endpoint identities directly against pinned saved prepared words. Check overlay hiding changes no counts, snapshot changes clear stale links, and reset/orbit/zoom work.
- Confirm all 64 bodies match each exact saved frame, all six table rows remain, mobile layout scrolls its wide table, keyboard controls work, missing/mismatched binding fails closed, and a WebGL failure leaves the bound table readable.
- `window.__evidenceState` exposes the selected tier/tree and six summaries. `window.__viewState` exposes snapshot metadata, body count, selected/rendered link counts and up to eight endpoint samples for later display QA. These are display probes, not scientific validation.

Source-only inputs consulted: original oracle source/protocol and prior replication viewer sources for v1; renewal analyzer/checker/runner, moving-admission reference/checker writers, and prior replication generation/index/reference writers for v2. No saved `results/` file was opened. Existing desk memos remain proposals, not executed experiments.
