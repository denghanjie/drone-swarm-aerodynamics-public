# One second of coupled Boids motion completed

20 October 2026. Computational research only; the broader research goal remains unfinished.

**All four planned 64-drone runs completed one simulated second.** The local flocking rules steered the drones, the airflow calculation used their current states at every integration stage, and the resulting forces and moments fed back into their motion. All 4,800 attempted force-evaluation stages were accepted by the current calculation. This extends the earlier all-stage 64-drone check from 0.02 seconds to a one-second horizon with two newly prescribed starting seeds.

In everyday terms: we let the simulated flock move on its own rules, instead of shifting its positions by hand, and the calculation kept working throughout these short trials.

The motion was not just a rigid cloud sliding across the screen. Individual centers moved up to about 0.69–0.70 metres from their starting positions; after removing the whole cloud's translation, the largest individual change was about 0.32–0.35 metres. The cloud also descended about 0.45 metres on average. That descent is an observation, not an identified fault or an aerodynamic effect isolated from the route guidance and controller. These runs do not demonstrate altitude holding or sustained flight stability.

| Starting seed | Steps tested | Planned time reached | Largest difference between resolutions at common endpoints |
|---|---|---|---|
| 2026102001 | 0.005 and 0.0025 s | 1.0 s in both | 0.0000002682 m |
| 2026102002 | 0.005 and 0.0025 s | 1.0 s in both | 0.0000003481 m |

Halving the time step changed the recorded positions very little on these paths. That is a numerical sensitivity result, not an error bound for the true trajectory and not evidence of physical accuracy. The two resolutions share their initial seed, and the many stages are dependent computations, not thousands of independent experiments.

The independent saved-data audit passed: 7,608 records, 307,200 derivative/load rows and 1,200 completed steps were checked for the declared bindings and arithmetic consistency. It did not rerun the airflow model, regenerate the controller, or independently validate aerodynamic forces against experiments. The inherited geometric checks reported no contact or vehicle-limit event; they are not a continuous-time or real-flight safety certificate. Final endpoints were not separately queried for aerodynamic admission.

The [Three.js replay](viewer/) now shows actual saved coupled motion, with four selectable runs, endpoint scrubbing and playback at one-fifth speed. All 1,204 initial/endpoint position buffers and displayed outcomes passed the recorded display checks; desktop and mobile screenshots were inspected. No simulation runs in the viewer.

The result supports a narrow useful conclusion: the current calculation can remain usable during these four short, moving 64-drone paths. It does not establish a new flocking algorithm, a speed improvement, 1,000/5,000-drone scalability, physical validity or a publishable breakthrough. The earlier failed large synthetic-motion experiment remains unchanged; this is neither a repaired version of it nor proof that its failure cannot recur.

The next distinct question should extend the duration of a fixed coupled workload before making large-swarm claims. It needs its own prospective protocol and an evidence-storage plan that preserves checks without excessive duplication. No new numerical allocation is opened by this recommendation.

All raw journal bytes are retained. For public GitHub storage they are split losslessly into ordered parts; [reconstruction instructions](RECONSTRUCT.md) recover the exact original gzip files. See [claim ledger](RESULT-CLAIMS.md), [prospective rules](PROTOCOL.md), [audit](audit/audit.json), [sources](LITERATURE.md), [display checks](UI-QA.md), and [restart](RESTART-RESULT.md).
