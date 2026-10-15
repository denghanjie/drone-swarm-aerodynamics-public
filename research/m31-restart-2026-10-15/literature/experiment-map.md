# Literature–experiment links

Use this alongside the [annotated source ledger](annotated-ledger.md), [bibliography](sources.bib) and [access log](source-access-log.md). Those records contain bibliographic status, exact reading locations and limits. No external code or dataset was imported for this checkpoint. No publication's reported result is treated as a result of our implementation.

| Source keys | Material use here | Implementation / experiment link | Adaptation result |
|---|---|---|---|
| `reynolds1987boids`, `vasarhelyi2018flocking` | Define local flocking and distinguish neighbor rules, route guidance, dynamic constraints and planar versus volumetric evidence. | Existing M31 source at base `c591ce2`; C05 in [claims](../claims.md); audit of shared route and local terms. | Source inspection completed; no reproduction of either paper and no new Boids advantage experiment. |
| `kiran2025interactions` | Motivate separate force/moment response, offsets, dynamic cases and careful actuation matching. | Physical-validation track in [plan](../protocol/bounded-restart-plan.md); C06. | Proposal only. Raw dataset unavailable; percentage inconsistency remains unresolved and is not a calibration target. |
| `bauersfeld2024jetv3` | Candidate inexpensive mean wake field; preserve length definition and operating envelope. | Existing historical wake work is prior context; future small aerodynamic tranche in plan. | No fresh fit, calibration or measured validation. Numerical model use must remain conditional. |
| `gielis2024aggregate` | Test aggregation rather than assume pairwise superposition; powered receiver measurements matter. | Separate later aggregation question in plan, after receiver-model comparison. | Proposal only; no nonlinear model trained or claimed superior here. |
| `shi2022neuralswarm2` | Learned vertical-force model as a relevant future baseline; distinguish general equations from actual learned outputs. | C06/C09, future receiver-response comparison in plan. | No code reproduction or adaptation executed. Does not validate six-component force/moment prediction. |
| `nyland2007nbody` | Optimized direct evaluation as a fair computational baseline. | Future CPU/WebGPU correctness and timing gates in plan. | Proposal only. No CUDA timing transferred to WebGPU. |
| `green2010particles` | Separate complete finite-radius neighbor enumeration from dropping nonzero distant interactions; audit occupancy. | Existing M31 grid inspection; future same-kernel brute-force baseline. | No new spatial-pruning algorithm or speedup result. Later DOT pruning work already exists and is prior context. |

Next-tranche diagnostic IDs D1–D6 and conditional L1–L4 are our proposed experiments, not published experiments. Their implementations and outcome links will be added only after their own source freeze and actual execution. Hypotheses, changes, failures and null results must all be retained.
