# Historical check: paired half-step sensitivity

21 October 2026. Documentation-only review; no raw-data reads, numerical execution, external research acquisition or new seed search. Historical source and results remain unchanged.

The proposed checkpoint runs four **new h = 0.0025 s paths**: original and unchanged vertical-memory controllers for each exposed N64 seed 2026102101/2026102102, five seconds with the existing 1 + 4 s segmentation and full coupling. It compares them with saved h = 0.005 s outputs; no coarse path is rerun. These seeds and their coarse outcomes are now exposed. This is a timestep-sensitivity diagnostic, not independent replication, new-seed evidence or a proof of convergence.

## Exact completed comparator

The [coarse summary](../m31-unseen-pairs-2026-10-21/SUMMARY.md) and [claim ledger](../m31-unseen-pairs-2026-10-21/RESULT-CLAIMS.md) report:

- Seed 2026102101 original controller: native near-field refusal at trial time 3.620 s; last completed endpoint 3.615 s. This is not an observed collision. Memory reached 5 s.
- Seed 2026102102: both controllers reached 5 s.
- Own-request vertical MAE was lower with memory over the available common controller samples. Each arm followed its own changing request; no common-target guarantee was established. That checkpoint expressly ran no resolution comparison.

The [public receipt](../publication-receipts/m31-unseen-pairs-result-2026-10-21.json) identifies result commit `73e8bae5261d01f4ffe79ad566f191df58d9b9fb`, [manifest](../m31-unseen-pairs-2026-10-21/result-manifest.json) SHA-256 `1237252ed0ee0799982dcd89365272ae8c4ee1c330d7cd5377af183dc8b3abe5`, 150 pins and both equality flags true. Final receipt publication is at commit `ad94cfd90c0e9d2af1c09d7c437d451aaecbee3d`. The saved verification covers the public manifest and specified key files plus local/committed pins, not a full remote raw-data redownload. This review performs no fresh remote verification.

Earlier [first-seed memory](../m31-vertical-memory-2026-10-21/SUMMARY.md) and [second-seed transfer](../m31-vertical-transfer-2026-10-21/SUMMARY.md) already compared 0.005/0.0025 s memory paths on seeds 2026102001/2026102002. Their agreement does not certify these different paths. [Prior historical notes](../m31-vertical-memory-2026-10-21/HISTORICAL-CHECK.md) preserve fixed-height PD, horizontal-controller/gain and force-ablation antecedents. Neither controller comparison nor integral action is new.

## Interpretation fixed before the fine outcomes

Retain both controller implementations, all gains/limits, control cadence, load model and stopping rules. Each fine path starts from its matched original physical state; memory starts as specified and carries its own integral, previous error and update count across t = 1. Do not transplant coarse evolved states or reset segment memory.

Report categorical outcomes and actual attempted/refused versus completed times first. Compare per-arm coarse/fine positions only at common completed endpoints and controller descriptors at common controller indices. Within each resolution, pair original/memory own-request MAE over their common saved indices. Also describe the controller-effect difference over a **four-way common window** for each seed, shared by both arms at both resolutions, with its sample count and end explicit. Different evolving own-requests remain different references; changing comparison windows must not masquerade as an effect change. Missing suffixes remain missing.

Two step sizes describe observed sensitivity, not integration order, continuous-event location, a rigorous trajectory error bound or physical accuracy. A changed refusal or completion category is a retained numerical/model-domain finding. Four new paths are dependent comparisons of two fixed configurations, not population trials. No general safety/stability, optimality, novelty, scalability or overall-completion claim follows.
