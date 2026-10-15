# Saved-state wall-activity audit addendum

**All 2,412 wall projection tests were inactive; pair avoidance produced 677 nonzero corrections.** Exact original/instrumented controller-output parity passed on all 50 pre-control reference states.

Read the [audit report](REPORT.md), [literal result edition](RESULT.json), [decoded witnesses](WITNESSES.json), [independent review](INDEPENDENT-RESULT-REVIEW.md), [prospective plan edition](PLAN.md), [exact instrumentation patch](instrumentation.json), [source identities](SOURCE-IDENTITIES.json), and [execution provenance](PROVENANCE.json).

This is an audit addendum to [event-stress commit f163221](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/f1632213839104990eed9ec9c29600d2360d52cf). That campaign remains EVENT_EXPOSURE_INSUFFICIENT. The later replay neither regenerates flight nor supplies the absent required events. No net trajectory causality or physical validation follows. The published event-stress failure-writer erratum still applies.

## Viewer update
The [event-stress viewer](../campaign-predictor-event-stress/demo/index.html#controller-replay) gains a plainly labeled, static saved-replay panel. Its Three.js playback, app.js and data.json are unchanged. Browser rendering of this update is unverified; the panel and links are statically checked. All audit findings are readable without WebGL.

The staged `demo/index.html` must replace **research/campaign-predictor-event-stress/demo/index.html**, not be installed beneath this addendum. All other staged files belong in **research/campaign-wall-activity-replay/**. The export manifest specifies each destination. No vendor or trajectory data is copied.

## Evidence and privacy
Public editions are labeled and originals identified by SHA256. Aggregates and parity hashes are unchanged; binary witnesses are decoded into readable JSON with bit-exact numerical round trips. Raw tensors, opaque binaries, host logs, workspace paths and private release records are excluded. The compact export is an audit record, not a standalone reproduction bundle: complete returned controller outputs were not retained, and parity is supported by the reviewed instrumentation plus its saved per-state hashes. One actual replay completed; a missing timing wrapper was resolved before the first execution, with no experiment retry.
