# Historical check: vertical tracking with controller memory

21 October 2026. Source-only historical assessment. This review reads retained reports, protocols, verification ledgers and controller source; it imports or executes no scientific module, launches no numerical experiment and acquires no new external research. Earlier records remain unchanged.

## Finding and selected scope

**No completed integral vertical-velocity intervention was identified within the inspected scope.** The history already contains fixed-altitude PD tests, horizontal position-hold interventions, a horizontal/attitude gain search, force/moment ablations and nominal-versus-coupled Boids comparisons. Those must not be presented as new questions.

The selected next diagnostic is narrower: retain the current coupled aerodynamic loads and test one prospectively specified vertical-tracking memory intervention on **N64, exposed seed 2026102001, h = 0.005 and 0.0025 s, with a planned five-second horizon**. This seed was selected because its already observed coupled paths reached the modeled floor at original times 4.6200 and 4.6175 s. The proposed two resolutions are two dependent numerical paths from one configuration, not two independent trials. Seed 2026102002 is outside this allocation.

This is explicitly an **outcome-selected diagnostic**. Neither successful completion nor failure supplies a population success rate, an independent confirmation, a general controller guarantee or evidence that integral control is novel. The review is bounded to the named records and targeted text searches, not an exhaustive repository or published-prior-art audit.

## What has already been tested

| Retained study | Completed intervention and outcome | Difference from the selected question |
| --- | --- | --- |
| [Step 2C: known downward force](../../outputs/step-02c-results.md) | The unchanged fixed-height PD controller receives a known vertical force pulse during [4,8) s. It explicitly has no integral correction or disturbance feedforward. A 20%-weight load produces approximately 0.327 m altitude offset, matching the declared equilibrium relation. Low thrust produces a large descent in a model without ground contact. | Basic height holding under load and its proportional offset are already demonstrated. This is a single-drone prescribed-force test, not integral tracking of a Boids vertical-velocity request under current F. |
| [Step 3B: one-way wake](../../outputs/step-03b-results.md) | A fixed upper source affects a dynamically integrated receiver with a 1 m altitude target. The PD controller has no integral correction; aligned and offset cases retain altitude loss. | Earlier height holding under a modeled wake exists, but the source is fixed, the model and yaw policy are older, and no current N64 mutual-coupling or integral intervention is tested. Historical magnitudes are not transferable to the present paths. |
| [Step 3D: controller sensitivity](../../outputs/step-03d-results.md) | Added horizontal position feedback to a two-by-two controller/aerodynamic comparison. The altitude loop remained unchanged; no integral action or aerodynamic feedforward was added. Default horizontal RMS improvement was small and peak pitch increased. | Position holding here means horizontal return, not vertical integral tracking. |
| [Step 3E: gain search and local stability](../../outputs/step-03e-results.md) | Searched 27 combinations of horizontal position gain, horizontal velocity gain and angular-rate damping, with attitude gain fixed. Selected gains reduced tilt but worsened horizontal RMS; both tested uneven-rotor hover equilibria were locally unstable. Other model parameters and command caps were unchanged. | Gain tuning and local hover-stability analysis already exist. This did not add vertical controller memory, and its limited grid did not prove that no stabilizing controller exists. |
| [N16 motion feedback](../m31-motion-feedback-2026-10-16/MILESTONE-SUMMARY.md) and [force ablation](../m31-force-ablation-2026-10-16/MILESTONE-SUMMARY.md) | Completed off/full comparisons and a force-only arm that suppresses added aerodynamic roll/pitch torque. Full versus force-only sampled position discrepancy was about 0.511 m over 2 s; final mean heights were nearly equal, approximately 3.6554 and 3.6546 m. Controller settings were retained. | Removing torque is already tested. It neither adds integral tracking nor isolates a controller cure. Less tilt did not imply better position tracking. |
| [Current N64 qualification](../m31-coupled-stage-qualification-2026-10-17/SUMMARY.md) | Completed matched coupled/off branches for 0.02 s from exposed fresh-a-t5, with the current projected adapter and two controller updates. | Current-adapter N64 feedback and off/full wiring are established antecedents; no vertical-memory intervention was used. |
| [Coupled continuation](../m31-boids-continuation-2026-10-20/SUMMARY.md), [descent trace](../m31-descent-trace-2026-10-20/SUMMARY.md) and [nominal comparison](../m31-nominal-comparison-2026-10-21/SUMMARY.md) | Seed 2026102001's coupled paths stopped on drone 17/floor at 4.6200/4.6175 s; its matched nominal-load paths reached 5 s. The trace found initial delivered upward force below weight and upward acceleration while still descending near the stop. The nominal comparison retained the original controller and changed load selection. | Establishes the exposed within-model failure and the total effect of switching load selection. It does not establish which controller intervention will work, isolate one mechanism, or validate the magnitude of the modeled airflow effect. |

The older [controller/airflow interpretation](../../outputs/research-controller-and-airflow-interpretation.md) already explicitly identifies the absence of dedicated integral or model-based downwash compensation. It retains the results as sensitivity evidence for an uncompensated baseline, not proof of physical impossibility.

## Current controller and the distinct diagnostic

The inspected [current control wrapper](../m31-boids-admission-2026-10-20/source/motion.cjs) constructs

`targetZ = z + (2.5 * desiredVz + 1.5 * vz) / 6`.

The inherited [flight controller](../../outputs/step02c-source/physics.cjs) requests vertical acceleration `g + clamp(6 * (targetZ - z) - 4 * vz, -4, 5)`. Algebraically, before limits, the combined request is `g + 2.5 * (desiredVz - vz)`. This simplification is explanatory algebra, not a claim that alternate expression orders yield identical binary64 words. The wrapper contains no accumulator and reads its own path's current Boids/avoidance request.

The narrow question is:

> On this one exposed failing configuration, does a fixed bounded memory correction to the existing vertical-velocity tracking error alter the recorded descent and floor/vehicle-limit outcome while the current full aerodynamic coupling remains active?

A fixed-height target would change the vertical task supplied by Boids. Tracking the existing desired vertical velocity preserves that task and tests the missing memory mechanism more directly. The candidate must be specified prospectively: one gain, accumulator initialization/update order, limits and anti-windup behavior, uniformly applied across drones. This note neither chooses numerical tuning values nor establishes that any choice will succeed. A parameter search or a drone-17-only modification would be a different diagnostic.

An accumulator introduces controller state beyond the existing 17 physical words per drone. Its exact saved values and update/hold schedule must be part of evidence and restart state. In particular, a one-second segment boundary must not silently reset this memory. The previous stateless-controller continuation argument cannot be reused unchanged.

The preserved coupled comparator covers original t = 0–1 in [Boids admission](../m31-boids-admission-2026-10-20/PROTOCOL.md), then an exact-state continuation. Compare available common completed prefixes and categorical stopping outcomes; retain the baseline's missing post-stop suffix. Outcome comparisons do not require inventing a five-second baseline endpoint. Record tracking error, memory/correction, clipping, nominal/delivered loads and stopping evidence so that completion alone is not interpreted as improved tracking or general safety.

Published antecedents and reading limitations are in [LITERATURE.md](LITERATURE.md). The historical distinction is a new bounded implementation diagnostic on an exposed failure, not a claim of novel integral control, physical validation, optimality, large-swarm scalability or overall research completion.
