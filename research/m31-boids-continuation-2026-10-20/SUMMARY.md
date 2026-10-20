# Longer motion exposes a modeled floor contact

20 October 2026. Computational-only research; overall goal remains unfinished.

**One starting configuration reached the modeled floor near 4.62 seconds total in both time-step versions. The other reached the planned 5 seconds in both versions.** The airflow calculation itself accepted every attempted stage. This distinguishes the current trajectory/controller limitation from an airflow-calculation refusal.

In plain language: letting the simulated flock move longer exposed a concrete problem. One drone descended far enough to touch the model's floor. The calculation kept working, but that does not mean the resulting motion was acceptable.

We continued all four previously saved 64-drone endpoints from original t = 1, without reinitialization, replaying the completed first second, resetting the fine path to the coarse path or changing model/control parameters. The fixed plan allowed four additional seconds. These are exposed trajectories, not four independent trials.

| Starting seed | Step size | Additional time reached | Total nominal time | Recorded outcome |
| --- | --- | --- | --- | --- |
|2026102001|0.005s|3.6200s|4.6200s|Drone 17: floor contact and vehicle-model limit|
|2026102001|0.0025s|3.6175s|4.6175s|Drone 17: floor contact and vehicle-model limit|
|2026102002|0.005s|4.0000s|5.0000s|Planned horizon completed|
|2026102002|0.0025s|4.0000s|5.0000s|Planned horizon completed|

The two stop records name the same drone and the floor; neither lists a drone-to-drone contact. Exact quoted records and their journal provenance are in [inspection](inspection/provenance.json). This is the implemented endpoint/swept-geometry result, not an independently measured real-world collision or a continuous-time event-location bound. The final endpoint is retained even when its safety check stops the run.

The cloud continued descending during this new interval: mean vertical changes were approximately −1.75 m for the stopped configuration and −1.84 m for the other. These figures begin at the saved one-second endpoint. The cause remains unisolated: steering targets, controller response and delivered aerodynamic loads were not separated by this experiment. Neither a controller defect nor an aerodynamic cause is established merely by the downward motion.

The movement was accompanied by changing local relations. Each stopped path recorded 666 directed neighbor additions and 956 removals across consecutive controller updates; each completed path recorded 724 additions and 900 removals. These are event counts, not distinct-pair totals or proof of a novel emergent mechanism. Saved saturation flags numbered 0 of 23,168 vehicle-command records in each stopped path, and 4 of 25,600 in each completed path. Those flags do not identify or exclude a physical cause of descent.

All 18,284 attempted native stages were admitted. The saved-data audit passed 28,958 journal records, 4,571 completed steps and 1,170,176 derivative/load rows. Its 8,502,060 square-root comparisons found zero observed one-ULP differences. The audit checks the declared arithmetic and evidence bindings; it does not independently regenerate the controller, native force law, contact geometry or physical truth.

Maximum coarse/fine center differences at common completed endpoints were approximately 0.00001437 m and 0.000007791 m. These include inherited initial discrepancies. Comparisons end at the common prefix; the stopped pair has no invented suffix. Small numerical differences and similar stop times do not establish physical accuracy, an exact trajectory-error bound or safe flight.

The [Three.js replay](viewer/) shows all four saved continuations. Its clock is relative to the continuation: add 1 second for original time. All 4,575 initial/completed endpoint buffers, controls, desktop/mobile layouts and corrupt-data refusal passed the fixed display checks. The viewer renders centers and trails, not the factory/floor geometry or a highlighted drone 17; use the cited stop records for the floor-contact classification. No scientific model runs in the page.

**Conclusion:** the current native calculation remained usable along these longer discrete paths, while one configuration reached a recorded floor limit. This is a useful computational limitation to investigate, not a publishable novelty or physical-validation result. Prior failures remain intact.

**Next question:** trace drone 17's saved vertical steering request, controller target, nominal/delivered loads and resulting motion before changing the controller or scaling up. Observational tracing can locate where the downward command/response appears; a causal claim would still need a separately defined intervention. No new numerical allocation is opened here.

Every raw JSON-line byte remains recoverable from the ordered compressed parts. See [reconstruction](RECONSTRUCT.md), [claims](RESULT-CLAIMS.md), [prospective protocol](PROTOCOL.md), [audit](audit/audit.json), [verified literature](LITERATURE.md), [display QA](UI-QA.md) and [restart](RESTART-RESULT.md). Final public identity is recorded separately in the publication-receipts directory after verification.
