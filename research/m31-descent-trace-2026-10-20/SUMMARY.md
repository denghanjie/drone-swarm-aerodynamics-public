# The drone was braking, but still reached the floor

20 October 2026. Computational-only milestone; overall research unfinished.

**We now have a more specific account of the recorded descent.** At the start, the model supplied only about 73% of drone 17's weight in upward force in the first configuration, and about 72% in the second. Near the first configuration's floor stop, the drone was receiving upward acceleration but was still moving downward. An upward push does not instantly reverse a downward motion, just as braking does not instantly stop a moving car.

This trace reads the existing runs from their original beginning. It adds no new flight simulation, changes no gains and makes zero native airflow calls. An independently written checker verified every one of the 1,924 selected controller/k1 pairs, their exact source-record identities, scalar descriptors and four full-state continuation boundaries.

## What the records show

At original time zero, drone 17 in both configurations had a nominal motor state that would provide 100% of weight at its saved upright orientation. The coupled model instead delivered 73.3027% and 71.9693% of weight, with saved vertical accelerations −2.6190 and −2.7498 m/s². This is a direct force/acceleration relation inside the implemented model. It does not validate that magnitude of aerodynamic loss in real air, nor isolate its contribution to the later floor stop.

The first sampled downward velocities occur at 0.04 s and 0.05 s, respectively. These are first observations on the 0.01-second controller-sampling grid, not exact continuous reversal times. For the first configuration, the desired vertical velocity is positive at 90 of 462 updates, while requested net upward acceleration is positive at 430. Those are different questions: a controller can ask for upward acceleration while trying to descend more slowly. Local flocking, route guidance and avoidance are combined in the saved desired velocity; this trace does not separate their contributions.

|Configuration|Integration step|Saved updates|Desired vertical velocity positive|Upward acceleration requested while delivered acceleration negative|
|---|---:|---:|---:|---:|
|2026102001|.005 s|462|90|207|
|2026102001|.0025 s|462|90|207|
|2026102002|.005 s|500|72|168|
|2026102002|.0025 s|500|72|168|

The matching counts across resolutions describe these same exposed initial configurations. They are not four independent trials or a general success/failure rate. Counts are sampled events, not continuous durations.

At the last sampled controller update of the stopped configuration, original t ≈ 4.61 s, the drone was asked to move upward at about 0.250 m/s, but was still descending at about 0.083 m/s. Delivered upward force was about 107.9% of weight, corresponding to upward acceleration about 0.775 m/s². The already published floor stops occur at 4.6200 and 4.6175 s. The final endpoint has no newly evaluated force: these force values belong to the earlier sampled update. This evidence supports a recorded failure to arrest descent before the stop, not a claim that lift stayed insufficient until contact.

The other configuration's last sampled update, t = 4.99 s, shows a small positive vertical velocity about 0.00926 m/s and upward force about 102.6% of weight. Its saved path completes 5 s. The same ID starts at a different location in this configuration, so it is not a matched control.

## What this narrows down

There are at least three interacting quantities to separate: the requested vertical motion, the motor's delayed response, and the force reduction imposed by the coupled model. The trace retains command totals, nominal motor totals, saved orientation, delivered force and acceleration. Its nominal-force comparison uses the same recorded state and orientation; it is not a flight rerun with aerodynamic coupling removed. A newly updated command is paired with k1 before motor state responds to that update.

**Next distinct experiment:** preserve these coupled results and make a single-change comparison with nominal rotor loads instead of the coupled aerodynamic loads, from the same original initial states, with unchanged Boids, controller, geometry, seeds, resolutions and finite horizon. This could test the total effect of the implemented coupling on these paths, including downstream changes in flocking. It would not validate the aerodynamic law or prove which controller modification is best. That intervention is proposed only; no new execution allocation is opened by this result.

## Evidence and visible result

The [Three.js view](viewer/) now joins the original and continuation endpoints, highlights drone 17, draws its full saved trail and the modeled floor, and labels the actual timestamp of held controller values. All 5,775 joined endpoint buffers, all 1,924 selected samples, floor/highlight, controls, corrupt-data refusal and desktop/mobile captures passed the single display allocation. Both captures were visually inspected. Other factory obstacles are omitted; the large wire halo is a visibility aid, not the body radius. Force-chart segments connect sampled values and do not evaluate intermediate forces.

[Exact excerpts](results/trace.jsonl), [observational report](results/report.json), [independent audit](audit/report.json), [prospective protocol](PROTOCOL.md), [claim boundaries](RESULT-CLAIMS.md), [literature scope](LITERATURE.md) and [restart](RESTART-RESULT.md) preserve the trace. All original raw journals remain unchanged in their earlier published checkpoints. No physical validation, causal cure, safety, novelty or speedup is claimed. Final public identity is recorded separately under publication-receipts after verification.
