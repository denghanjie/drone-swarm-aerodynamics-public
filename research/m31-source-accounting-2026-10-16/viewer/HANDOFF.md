# Source-accounting viewer handoff

Prepared as inert static source on 2026-10-16. No browser, server, scene, JavaScript
runtime, automated QA, screenshot, or scientific source was launched by the author.
The root owns integration, result review, binding creation, and the separately
bounded display QA. This is an unrendered handoff, not a browser-verification claim.

## Install location and files

Copy `index.html`, `style.css`, `data.js`, `app.js`, and `scene.js` into:

`research/m31-source-accounting-2026-10-16/viewer/`

Keep this note and `DESIGN-AND-LIMITATIONS.md` as preparation records if useful.
No package manager, build step, new vendor, external asset, or runtime dependency
installation is needed. The existing local Three.js modules resolve from
`../../../outputs/step02b-source/vendor/`. The import map maps the bare `three`
specifier used by `OrbitControls.js` to the same existing `three.module.js`.

Root must create `viewer/binding.json` only after saved-result review:

```json
{
  "version": 1,
  "files": [
    {"path": "results/result.json", "bytes": 123, "sha256": "actual 64-character lowercase SHA-256"},
    {"path": "results/witness-stdout.json", "bytes": 456, "sha256": "actual 64-character lowercase SHA-256"}
  ]
}
```

The two byte counts above illustrate schema only; they are not evidence or a
ready-to-use binding. No binding or mock result is included in this handoff.
Paths are checkpoint-relative. The loader permits exactly these two paths,
checks their byte lengths and SHA-256 digests before parsing their UTF-8 JSON,
then checks the declared schema. All numerical sections remain hidden if any
required input is missing, changed, malformed, or inconsistent with the schema.
No evidence fallback, retry, or regeneration exists.

Open through HTTPS or localhost HTTP so `crypto.subtle` is available. A direct
`file:` opening is not supported. A changed binding is a new binding, not an
independent source of trust. Hash matching does not validate the science.

## Visible behavior

- The 3D scene repeats the **410 saved radial records** (10 planes × 41 samples)
  azimuthally as static colored slices. There are no fluid particles, trajectories,
  downstream interpolation, field evaluators, or camera animation.
- Default mode is `bothFades`; the default plane is the saved 0.6 m plane. The
  other modes directly select saved `radialOnlyMps` and `untruncatedMps` values.
- A selected-plane SVG compares all three saved profiles, and a native table
  exposes all 41 samples. A second table contains the ten saved J records.
- Zero-valued annuli are omitted. The selected sampling-extent ring is dashed and
  explicitly not a support boundary. At s >= 2.5 m the both-fades profile is
  labeled empty; untruncated and radial-only reference modes are distinguished.
- Near-source s/D < 2.5 is labeled unavailable. The 2.5D guide performs only a
  geometric placement using saved D. No missing near-source values are generated.
- The source-state selector highlights four rows in an expandable table of
  all **20 actual saved pair outputs**. Its event handler never updates the scene.
  Saved motor arrays, total, independence assertion, and stimulus assertion are
  displayed. The selected full JSON record is available in a disclosure.
- Inflow values in the witness table use the saved number's full JS string
  representation. Other table values show eight significant digits with full
  values in cell titles; downloadable original JSON remains linked.
- Links point to the actual protocol, two result files, source definitions,
  summary, full report, source freeze, binding, and historical
  `../../../outputs/research-results.html`. A data-URI favicon avoids an implicit
  external favicon request.
- The opening leads with the recorded fixed-position source-state result.
  Radial retention is a display percentage of the saved squared-speed retention
  value, labeled not thrust. The normalization ratio remains under technical
  detail with `id="summary-ratio"`; the twenty-row witness table is collapsed by
  default while selected motor-state values and all four saved receiver inflows
  remain visible.
- Render events occur only on scene initialization, control changes, resizing,
  plane/mode changes, and reset. No animation frame loop or timers are present.

## Preparation observations; no runtime QA

The public protocol and `source/audit.py`/`source/witness.cjs` were read. After root
reported scientific completion, the saved result header/profile schema and witness
records were read to confirm the adapters' field names. No result was recomputed.
Text inspection located only the declared local evidence fetches and verified that
the scene has no source-state amplitude path, integration code, source `fade`
function, or animation scheduler. These observations are not executed tests.

For the root's bounded QA, the important paths are: verified load; plane/mode
selection including empty both-fades planes; all five witness selections without
changing the scene; responsive numeric-table access; user-controlled camera/reset;
and failure to display on a deliberately mismatched hash in an isolated display
copy. Check renderer availability and console errors. Any such QA must remain
separate from science and must not invoke `audit.py`, `witness.cjs`, or a campaign.

No automated QA script is supplied or run. The author has not assessed rendered
layout, frame cost, WebGL availability, keyboard/touch behavior, or screenshot
fidelity. Root should record the actual results of its bounded display check.
