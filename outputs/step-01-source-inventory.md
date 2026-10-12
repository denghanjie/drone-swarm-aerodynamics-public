# Step 1 — Source and data inventory

Checked 10 October 2026. “Published,” “publicly linked,” “retrieved,” and “validated” are different statuses.

| Source | Role | What was checked | Remaining work |
|---|---|---|---|
| [gym-pybullet-drones CF2X parameters](https://github.com/learnsyslab/gym-pybullet-drones/blob/main/gym_pybullet_drones/assets/cf2x.urdf) | Starting vehicle model | Public parameter contents inspected; contains mass, inertia, geometry, and aerodynamic coefficients. | Pin commit; trace parameter provenance and units before implementation. |
| [gym-pybullet-drones physics code](https://github.com/learnsyslab/gym-pybullet-drones/blob/main/gym_pybullet_drones/envs/BaseAviary.py) | Reference equations and simple downwash baseline | Public source inspected during research. | Check coefficient validity range and numerical behavior; the analytical expression must not be extrapolated blindly to vanishing separations. |
| [Repository license](https://github.com/learnsyslab/gym-pybullet-drones/blob/main/LICENSE) | Code reuse | MIT license inspected. | Preserve notices with reused code; inspect separately sourced assets before redistribution. |
| [Kiran, Ayanian & Breuer, RSS 2025](https://www.roboticsproceedings.org/rss21/p102.html) / [full text](https://arxiv.org/html/2507.09463v1) | Independent pairwise aerodynamic evidence | Paper describes measured forces, moments, and flow fields for Crazyflie interactions, including dynamic cases. It reports a 32.5 mm characteristic arm length, requiring reconciliation with our baseline. | Check exact experimental geometry, operating points, and data conventions. Mounted measurements constrain interaction predictions, not full free-flight controller behavior. |
| [Dataset DOI](https://doi.org/10.26300/64d4-wa17) / [Brown landing page](https://repository.library.brown.edu/studio/item/bdr:rnnfmt6u/) | Preferred pairwise measurements | Paper links an open-access dataset; DOI redirect identifies Brown item. | Retrieval failed through web tools; shell DNS failed; browser attempt timed out. Files, schema, license, and completeness were NOT inspected. Paper license does not establish dataset license. |
| [Neural-Swarm2 paper](https://arxiv.org/abs/2012.05457) / [author repository](https://github.com/aerorobotics/neural-swarm) | Established learned interaction baseline | Public README inspected; training expects data in data/training and refers to additional Box files. | Public access to complete training data and reuse terms not established. No top-level license was visible in the inspected listing; do not assume permission to redistribute code. No weights or training run verified. |
| [Aggregate downwash study](https://arxiv.org/abs/2312.03488) | Evidence concerning nonlinear combinations | Public paper inspected; small-formation measurements and learned aggregation described. | Usable raw-data/code distribution and terms not located in this check. Learned small-neighbor models do not automatically generalize to dense crowds. |

## Decisions from this inventory

Use the documented CF2X model for mechanics and software verification. Treat physical validation as a separate milestone requiring configuration matching. Do not silently combine a nominal vehicle's inertia, another study's force model, and a third study's actuator response and call the result validated.

Prefer the RSS 2025 data for pairwise force/moment checks if retrieval and terms can be resolved. A paper's plotted curves can support a limited reproduction, with digitization uncertainty, but are weaker than independently withheld raw measurements. They cannot substitute for aggregate interaction measurements.

For a learned model, split data by complete run/configuration before preprocessing and fitting. Preserve a held-out test set; do not fit and validate against the same published curve. If aggregate data remain inaccessible, restrict the first study to pairwise approximation sensitivity and computational performance; label large-swarm aerodynamic claims as conditional.

## Evidence still needed

1. Downloadable dataset files, metadata, and reuse terms.
2. Exact mapping between experimental and simulated configurations.
3. Independent single-drone transient measurements or a clearly qualified verification-only baseline.
4. An aggregate reference if we want to claim accuracy with several interacting neighbors.
5. Browser/adapter benchmark and pinned source versions before implementation comparisons.

No physical validation, code reproduction, or performance benchmark has been completed in Step 1.
