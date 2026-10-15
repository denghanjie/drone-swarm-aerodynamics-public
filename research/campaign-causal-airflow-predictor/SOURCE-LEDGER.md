# Sources and evidence ledger

Checked 2026-10-15. This bounded test applies established causal extrapolation to a fixed public model; it is not an exhaustive novelty search.

- Ben Khaled-El Feki et al., CHOPtrey, SIMULATION 93(3):185–200 (2017), DOI [10.1177/0037549716684026](https://doi.org/10.1177/0037549716684026). Read [author version v2](https://arxiv.org/html/1610.09261v2), §§3.4.2, 4.1, 5.2–5.3 and 7.2: past-sample polynomial prediction, contextual history/reset and constant-hold fallback already exist. Its examples do not validate drone wakes or guarantee hybrid-system stability.
- Chen, Ran, Wu and Jacobson, Multibody System Dynamics 52:255–279 (2021), DOI [10.1007/s11044-021-09785-x](https://link.springer.com/article/10.1007/s11044-021-09785-x). Read §§2.1–2.2: coupling-error analysis assumes LTI subsystems and discusses low-frequency behavior/aliasing and stability. Those assumptions do not prove order for this nonlinear clamped swarm.

The pinned [public joint-stage source](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/1336f5c416875a9651f92b58b2ed06649f25b04e/research/campaign-joint-stage-reference) supplies genuine local-3D Boids and the unchanged aerodynamic approximation. Source identities are in the public export's SOURCE-MAP.json.

Physical limitations remain separate: the [Bauersfeld model](https://arxiv.org/html/2403.13321v3) is a mean-hover approximation; the [2026 Kiran, Ayanian and Breuer preprint](https://arxiv.org/html/2608.30900v1) uses a different measured velocity observable. The prior six-marker screen found a nominal amplitude discrepancy, not quantified physical uncertainty.

Display data is decoded only from saved Float64 evidence. Joint poses retain components 0,1,2,6,7,8,9; selected witnesses retain all 17 components. Hashes identify original archived tensors. No model calls, interpolated states, private R8 inputs, external figure copies or new empirical measurements enter the viewer. The shared Three.js file is reused from the public support-factorial package.
