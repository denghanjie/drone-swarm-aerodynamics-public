# Public source and display ledger

The numerical model/controller source is pinned to public commit1336f5c416875a9651f92b58b2ed06649f25b04e at [the public joint-stage campaign](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/1336f5c416875a9651f92b58b2ed06649f25b04e/research/campaign-joint-stage-reference). No private archive or new physical observation supplies this simulation.

The display data is a numerical JSON conversion of saved evidence only. Each reference frame contains exact position/quaternion components0,1,2,6,7,8,9 of the retained full17-state tensor. The remaining components are not needed for playback and are not displayed. Selected paired witnesses retain all17 components. Source tensor/comparison/witness SHA256 values are embedded in data.json. Conversion adds zero model calls; no amplitude normalization or smoothing is applied.

The separate physical caveat comes from the [2026 Kiran, Ayanian and Breuer preprint](https://arxiv.org/html/2608.30900v1) versus the unchanged [Bauersfeld model](https://arxiv.org/html/2403.13321v3). The amplitude screen is conditional on nominal inputs and unlike measurement quantities; it cannot turn this numerical reference into physical ground truth.

Shared Three.js comes from the existing public factorial-support viewer. No vendor blob or third-party source figure is duplicated. Browser rendering is unverified; static/data checks are recorded.
