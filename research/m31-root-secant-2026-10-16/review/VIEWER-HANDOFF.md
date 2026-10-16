# Root-secant viewer scaffold

Static source only. No browser, screenshot, JavaScript execution, scientific
import, input/result scoring or UI QA was performed. The current result binding
is intentionally `ready:false`: the page displays a pending state and enables no
event/error controls. Existing M31 typography/colors and local Three.js assets
are reused; no dependency, image service, network acquisition or install was used.

Copy app.js, scene.js, index.html, style.css and binding.json to the package's
viewer directory. URLs are authored for that public location, not this isolated
delivery directory. This scaffold does not include the 15.8 MB source input.

## Binding contract

The seven exact keys in `binding.json.artifacts` are `config`, `events`, `summary`,
`independentReview`, `candidateRun`, `reviewRun` and `source`. Every entry has an
exact relative `url`, positive integer `bytes`, lowercase 64-character `sha256`,
and `format` (`jsonl` only for events; `json` for the others). The app checks every
response before parsing and refuses alternate paths. Finalize all pins from saved
bytes and only then set `ready:true`. The binding is the trust root for data;
HTML/JS/CSS and existing vendor modules should be covered by the package/source
manifest, rather than a circular self-hash in this binding.

The source URL is
`../../m31-ratio-reuse-2026-10-16/results/boids16-reuse10ms-0.00125.json`.
It matches the repository-relative input path recorded in config/summary. Source
identity and all 201 saved pose shapes/event times are checked. No original
trajectory is copied into the new package.

`reviewFields` maps the two confirmed direct independent-review fields, `pass`
and `complete`. Missing or false
fields keep the viewer locked and are shown as unresolved/failed, respectively.
There is no schema guessing or fallback from candidate success to reviewer pass.
The independent record must have kind `independent-saved-root-secant-review`, an
empty failures array, and scientificPass/decision exactly matching the summary.
Both supervisor records independently require `supervisorSuccess:true`,
`closed:true`, and `returncode:0`. Audit counts are deliberately not displayed.
Scientific rejection is a valid completed result and does not lock the viewer
when integrity/audit checks pass. A failed or incomplete audit does lock it.

## Completed saved result

The result files were read as data after the parent confirmed both supervised
invocations had closed. No scientific code was imported or run. The viewer reads
the following values from the bound records; they are not hard-coded UI data.

- Summary complete: true; scientificPass: false; decision:
  `rejected-fixed-secant`.
- Primary diagnostic coverage: 200 / 200 scored, including finite invalid-domain
  values; 4 invalid roots across 4 events. This is not 200 valid approximations.
- Prediction diagnostic maxima (rotor, force, moment):
  0.018768458299923737, 0.00993811376408624, 0.004127670070010363.
- Hold diagnostic maxima: 0.034641310306829855, 0.022282031285058564,
  0.010175726666147102. All three saved absolute gates fail the 0.001 limits;
  all three saved maximum comparisons are no worse than hold. The latter does
  not override the absolute or domain rejection.
- The 199 secondary secant targets also miss all three absolute screens;
  excluding startup cannot recover qualification.
- Independent review complete/pass: true; both supervisor records are
  closed/successful with returncode 0. Audit success is distinct from scientific
  success. The check count is deliberately absent from the rendered UI.
- Invalid-root locations are events 31–34, drone 3, rotor 0, above one. The UI
  reads these locations directly from each saved event and preserves its warning
  in hold mode.

The parent must still fill the six unset output/config artifact pins and set
`ready:true`; the source pin is already supplied. No outputs or original input
were copied into this scaffold. No viewer/browser execution or QA was performed.

## Saved fields used

- Source: `events[index].states` (16 × 17), `index`, `t`, `status`; positions at 0..2,
  original quaternions at 6..9. No interpolation, normalization or new flight.
- Target JSONL: all 200 rows, `index`, `t`, `method`, `validRoots`, `invalidRoots`,
  `scoreStatus`, `scoreReason`, and `errors.predict/hold`. Colors read saved
  `rotor[16][4]`, `force[16]`, `moment[16]`; current event readouts use saved
  `maxima/argmax`. No load/error/gate recomputation occurs in the browser.
- Summary: `primary`, `secondarySecantOnly`, `scientificPass`, `decision`,
  `complete`, `inputAdmission`, `input`. Primary gate/maximum/coverage displays are
  the saved fields. Startup comes from target row 1, secondary means 199 events,
  and the complete primary includes 200. Null complete-set maxima remain unscored;
  finite-only diagnostics are displayed separately if coverage is incomplete.
- Review and closures: direct status fields above. Their absence never supplies
  optimistic demo data.

In rotor view, rings use per-rotor saved values and body color uses the largest
of the four saved values as a visualization mapping. Force/moment views use each
drone's saved scalar norm error. Threshold color is 0.001 and high-error color
saturates at 0.005. Prediction-domain violations override affected rotor/body
color with magenta. Hold mode retains a textual prediction-invalid warning.
Initialization t0 is gray and explicitly not a zero-error target.

Playback advances one recorded 10 ms event every 40 ms (quarter-speed, discrete).
All 201 events are reachable, including initialization and terminal audit. The
all-event table exposes all 200 positive target rows. Drag/zoom and reset are
local camera interactions. Changing model size does not change the saved centers
or quaternions. Rotor radii/center offsets follow the stored model constants;
the central body is a schematic drawing. No synthetic example values are embedded.

## Parent QA still required

After pinning actual outputs, confirm the reviewer field mapping, source/result
schema, desktop/mobile layout, startup and terminal navigation, all 200 event
buttons, mode/metric/size/reset/play controls, invalid-root highlighting,
incomplete/null handling, audit-failure handling and intentional corruption
refusal. Capture and inspect the actual page. This handoff makes no claim that
browser behavior, WebGL rendering or visual quality has been tested.
