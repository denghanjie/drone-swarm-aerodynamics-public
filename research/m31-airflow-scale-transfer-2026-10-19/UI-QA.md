# Three.js evidence view check

Target flow: load → distinguish fitting/evaluation regions → choose measured, original, corrected and error displays → orbit/reset → mobile → refuse altered evidence.

Browser plugin unavailable; used existing Playwright and installed Chrome without installation. Local URL http://127.0.0.1:8876/research/m31-airflow-scale-transfer-2026-10-19/viewer/ . Desktop1280×1000, mobile390×844. The first and only display invocation passed seven groups in2.419seconds, with no console/page/HTTP errors, timeout or output breach. Parent visually inspected desktop full-page, mobile top and mobile scene. Captures show readable wrapping, rendered measurement plane and separate near/far colors. Minor tight spacing around some numbers remains readable; no substantive clipping or overlap observed.

| Check | Result |
|---|---|
| Page identity, meaningful content, no error overlay, rendered3D | Pass |
| Both gains, primary metrics and two evaluation bands match saved data | Pass |
| All six mode states/legends; visible rendering change | Pass |
| Orbit and reset | Pass |
| Mobile top/scene, no horizontal overflow | Pass |
| Changed evidence refused before rendering | Pass |
| Console/page/HTTP health | Pass |

Exact-record binding uses SHA256 and byte count. UI computes colors/formatting only, never scientific predictions. Mode snapshots are allowed to be identical when saved values legitimately coincide; distinct mode state/legend is still checked. Sources: source/ui.cjs and source/supervise.py. Evidence: ui/qa.json, desktop.png,mobile-top.png,mobile-scene.png and six mode captures. No repairs or further UI attempts required. Remaining limits: two viewport sizes in installed Chrome; no other-browser/accessibility certification or physical/flight validation.
