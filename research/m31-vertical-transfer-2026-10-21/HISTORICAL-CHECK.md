# Historical check: unchanged vertical memory on the second exposed seed

21 October 2026. Source-only assessment based on retained reports, protocols, configuration/source text and publication receipts. No numerical code, model query, simulation or new external research acquisition was performed for this review. No frozen source or historical evidence was changed.

## Distinct question and prior exposure

The proposed diagnostic uses **N64, seed 2026102002, h = 0.005 and 0.0025 s, planned horizon 5 s**, with the unchanged vertical-memory intervention and full current aerodynamic coupling. Both saved original-controller counterparts already completed five seconds. This therefore asks whether the fixed intervention transfers to another previously exposed configuration without introducing a recorded model/contact/vehicle-limit failure, and how its finite paths differ from the saved comparator. It does not test rescue of an existing failure on this seed.

**No exact equivalent completed vertical-memory test on seed 2026102002 was identified in the inspected milestone records.** The prior vertical-memory protocol explicitly excluded it. However, this seed's original-controller coupled motion, nominal-load comparison and descent trace were already observed. It is not a new initialization, a held-out configuration or an independently drawn random trial. Selecting it after the first-seed result gives a bounded transfer/regression diagnostic, not a blind evaluation or population reliability experiment. The two resolutions share one configuration and are dependent numerical comparisons.

## Exact prior result and publication identity

The immediately preceding [vertical-memory summary](../m31-vertical-memory-2026-10-21/SUMMARY.md), [claim ledger](../m31-vertical-memory-2026-10-21/RESULT-CLAIMS.md) and [restart](../m31-vertical-memory-2026-10-21/RESTART-RESULT.md) report that seed 2026102001 reached five seconds at both resolutions with full coupling retained. Its original-controller paths had stopped at 4.6200 and 4.6175 s. The audit checked 12,000 attempted/successful native stages, 3,000 completed steps and 64,000 controller-memory rows. This was one outcome-selected configuration, not two independent successful flights; no inference about the then-excluded second seed was established.

The retained [public result receipt](../publication-receipts/m31-vertical-memory-result-2026-10-21.json) identifies:

- Result commit: `dbb8596098a7223d57fa7499df8ad76a171acf2f`.
- [Result manifest](../m31-vertical-memory-2026-10-21/result-manifest.json) SHA-256: `c6a00e16c356a72152b6f77c2ef510b51cb9ec78f31545de55ad8535b50a59a9`.
- 171 verified file pins; receipt reports both `remoteBytesEqualLocal: true` and `committedBytesEqualLocal: true`, observed at `2026-10-21T02:15:07.910379+00:00`.
- [Source publication receipt](../m31-vertical-memory-2026-10-21/source-publication.json): source commit `37a793a4b1fe4e66c96ee585ef7e08042b6c6262`, source-manifest SHA-256 `4f6daaa6261060f19740bbe5c64572239e68139a87c646a0d91c5dcb23e5d082`, 94 pins.

These are read from saved verification receipts, not newly fetched public bytes. The recorded verification scope is exact public-manifest retrieval plus local/committed pin comparison, not a full remote journal redownload.

The second seed's original-controller baseline is the saved t = 0–1 [Boids admission](../m31-boids-admission-2026-10-20/SUMMARY.md), followed by the exact-state [continuation](../m31-boids-continuation-2026-10-20/SUMMARY.md) to t = 5. Their result receipts identify commits `637c25294f162bea39970d12df0206f25dead889` and `a0f595f34a4f9ef8cef516caa0cde60053e0eade`, respectively: [admission receipt](../publication-receipts/m31-boids-admission-result-2026-10-20.json), [continuation receipt](../publication-receipts/m31-boids-continuation-result-2026-10-20.json). Both resolutions completed five seconds. Their existing source/audit limitations remain part of any comparison.

The [nominal-load comparison](../m31-nominal-comparison-2026-10-21/SUMMARY.md) also already used this seed; both nominal and coupled paths completed five seconds. Its [receipt](../publication-receipts/m31-nominal-comparison-result-2026-10-21.json) identifies result commit `d04ca0f763529ae694373da48b7aab48fd7fc0f8`. That study changed load selection, not the controller. The [descent trace](../m31-descent-trace-2026-10-20/SUMMARY.md) had already examined drone 17 in this configuration. The same drone ID across seeds does not make their different initial positions a matched control.

## Settings transferred without retuning

The prior [protocol](../m31-vertical-memory-2026-10-21/PROTOCOL.md), [configuration](../m31-vertical-memory-2026-10-21/config.json) and [controller source](../m31-vertical-memory-2026-10-21/source/motion.cjs) specify the intervention to retain:

- Separate acceleration-valued integral, previous vertical-velocity error and update count for every drone; initial integral/error positive zero and count zero.
- At the first controller update, zero increment. At subsequent 0.01 s updates, increment `(2.5 * 0.01) * previousError`; add it to the integral and clamp to [-5,+5] m/s². Then store current `desiredVz - actualVz` and increment the count.
- Exact target expression `z + ((2.5*desiredVz + 1.5*actualVz) + integral)/6`, passed to the unchanged inherited actuator controller. Preserve arithmetic grouping. The original net-acceleration and motor limits remain active.
- Current full F coupling, projected integration, Boids/route/avoidance logic, motor lag, geometry, nominal reaction-yaw policy and stopping rules remain unchanged. The controller uses its own path's state and request; it does not observe or invert native loads.

This is clamped controller memory, **not saturation-aware anti-windup**. The existing gain and bounds were fixed choices in the first diagnostic, not validated or optimal settings. Changing them in response to this transfer result would define a different experiment.

Preserve the existing 0–1 s and 1–5 s segmentation with each path's own physical and controller-memory state carried across the boundary. Do not reset the integral/error/count at t = 1, import another resolution's memory, or initialize from seed 2026102001's final memory. The first segment begins at this second seed's original physical state with the specified zero memory. The t = 0.99 error supplies the next update at t = 1 under the inherited recurrence. The 17 physical words alone are not a complete restart state.

## Earlier antecedents and claim boundaries

The prior [historical check](../m31-vertical-memory-2026-10-21/HISTORICAL-CHECK.md) documents fixed-height PD disturbance/wake tests, horizontal position-hold and gain-search studies, N16 force-only ablation and short N64 coupled/off qualification. Their supporting paths include [Step 2C](../../outputs/step-02c-results.md), [Step 3B](../../outputs/step-03b-results.md), [Step 3D](../../outputs/step-03d-results.md), [Step 3E](../../outputs/step-03e-results.md) and [N16 force ablation](../m31-force-ablation-2026-10-16/MILESTONE-SUMMARY.md). Integral control, load compensation and controller comparison are not new research ideas.

The narrow distinction here is transfer of an unchanged implemented intervention to a second exposed configuration. Completion at five seconds would preserve the old categorical completion outcome, not improve it. Higher altitude or a changed endpoint alone does not establish better tracking: each arm follows its own changing Boids request, and the older baseline export lacks fleet desired-velocity data needed for a matched fleet tracking-error comparison. Candidate own-reference statistics remain descriptive. Any early stop must retain its actual reason and missing suffix; compare only available common completed endpoints.

Do not pool paths across these two outcome-informed configurations into an independent success rate, characterize this as held-out/random evidence, or infer continuous-time stability, physical validity, safe real flight, optimal gains, a novel integral method, large-swarm feasibility or overall research completion. Relevant verified publications and reading limits are in [LITERATURE.md](LITERATURE.md).
