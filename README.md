# Drone Swarm Aerodynamics — Public Research Snapshot

Research into **which approximations of mutual aerodynamic interaction preserve useful physical predictions while enabling locally controlled 3D drone flocks within browser compute budgets**, scaling toward 5,000 drones using WebGPU.

This is an ongoing research record, including unsuccessful experiments. The historical numerical pipeline runs offline on CPU; a new receiver-only component has also been evaluated on actual browser WebGPU. Three.js displays recorded trajectories and numerical evidence. A validated 5,000-drone, airflow-coupled WebGPU simulation has **not** been demonstrated.

![Visible airflow in the milestone 32 lab](outputs/milestone-32-flock.png)

## Current Milestone 31 restart

Latest ancillary work: [the observer source checkpoint](research/m31-observer-reconciliation-2026-10-16/MILESTONE-SUMMARY.md) demonstrates a possible registration timing failure with synthetic cases and preserves unresolved ownership through a pure candidate helper. It is not operationally integrated. The [latest actual GPU trial](research/m31-gpu-readback-trial-2026-10-16/MILESTONE-SUMMARY.md) failed before saved output; its [Three.js evidence view](research/m31-gpu-readback-trial-2026-10-16/viewer/) remains the current visible result. Physical source coupling remains unresolved. Earlier records below are preserved history.

The additive research branch preserves all historical milestones and later work. The latest [synthetic transport diagnostic](research/m31-transport-diagnostic-2026-10-16/README.md) recorded a browser-reported Local Network Access permission error before any sink HTTP request entry. Its new public records passed their separate saved review; delivery itself failed. The [Three.js evidence diagram](research/m31-transport-diagnostic-2026-10-16/viewer/) displays the actual saved stages. Read the [plain-language milestone summary](research/m31-transport-diagnostic-2026-10-16/MILESTONE-SUMMARY.md) and [restart index](research/OVERNIGHT-RESTART.md).

The prior [runtime replication](research/m31-body-runtime-replication-2026-10-16/README.md) passed browser/GPU admission, but failed to persist its first GPU control output. No main-family body-load query ran. The new synthetic diagnostic does not establish that historical failure's cause or repair its missing output. The prior [published checkpoint](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/22ca9e45cfe777def90dcab03530ba00055d3e99) remains immutable.
The preceding [body-load attempt](research/m31-body-load-2026-10-16/README.md) stopped at a browser-version mismatch before GPU/main-family work. Its saved-record audit passed 12,793 checks; the original scientific failure remains unchanged. The separate [physical source-contract review](research/m31-source-contract-planning-2026-10-16/README.md) motivates a test against independent thrust/flow measurements, which remain missing.

The latest replication's [saved review](research/m31-body-runtime-replication-2026-10-16/INDEPENDENT-SAVED-REVIEW.md) also failed on a checker metadata-shape assumption. Its failed report and unexecuted later checks remain preserved; no aggregate integrity pass or scientific qualification is claimed.

The preceding [coordinate-origin diagnostic](research/m31-coordinate-origin-2026-10-16/README.md) selected no candidate. Its independent review failed two bookkeeping checks; the checker error and immutable failed review remain disclosed.

The earlier [GPU receiver component](research/m31-browser-receiver-2026-10-16/README.md) passed its finite new allocation, while the [wake-slice gate](research/m31-browser-wake-slice-2026-10-16/README.md) failed. The [exact-zero experiment](research/m31-zero-screen-2026-10-16/README.md) retained a negative performance result. None demonstrates a complete coupled GPU swarm. The [restart index](research/OVERNIGHT-RESTART.md) links the preserved campaigns and terminal budgets.

## Historical snapshot and roadmap

- [Research direction and assessment of proposed trade-offs](outputs/research-tradeoff-assessment.md)
- [Original eight-step roadmap](outputs/research-roadmap.md)
- [Current research status](outputs/research-final-report.md)
- [Historical milestone 32: visible airflow and numerical diagnosis](outputs/milestone-32-summary.md)
- [Stage history, including failures](outputs/research-stage-log.md)
- [Physical-validation requirements](outputs/research-physical-validation-gate-2026-10-12.md)

## View the 3D lab

Clone this repository, then run from its root:

```sh
python3 -m http.server 8875 --bind 127.0.0.1
```

Open <http://127.0.0.1:8875/outputs/research-results.html>. The latest airflow lab and its small demonstration dataset are included in Git. Earlier large-flock replays require the evidence bundle below. The static server binds only to this computer. GitHub does not execute these HTML simulations in its file viewer.

The latest lab shows historical 50-drone coupled recordings and a two-drone explanation. Plumes represent the modeled mean wake; moving dots indicate direction, not resolved fluid trajectories. Numeric fields are reconstructed at exact saved poses, not measured or historically held loads.

## Restore the complete research evidence

Requirements: Python **3.9+** and GitHub CLI (`gh`) for automatic downloads. You can also download the public release asset manually without GitHub CLI. Node.js is needed only to rerun numerical experiments. Some older plotting stages also require Matplotlib; see their saved requirements.

```sh
gh auth login
python3 scripts/fetch-research-data.py
python3 outputs/research-reproduce.py
```

Large JSON records and binary trajectories are stored in the versioned `v0.1.0-public` release, not Git history. The [bundle inventory](data/research-data-manifest.json) pins each file and the compressed archive with SHA-256. The restore helper preserves differing local files rather than overwriting them. Allow approximately 2 GB for the restored evidence, plus download/extraction space.

For a manually downloaded [release asset](https://github.com/denghanjie/drone-swarm-aerodynamics-public/releases/tag/v0.1.0-public):

```sh
python3 scripts/fetch-research-data.py --archive /path/to/research-data-v0.1.0-public.tar.gz
```

The public `outputs/research-manifest.json` was regenerated after documented metadata sanitization: verify it after restoring the bundle. Running its verifier on a source-only clone will correctly report missing large files.

## Reproduce the latest experiments

After restoring all evidence:

```sh
python3 outputs/research-reproduce.py --stage 32 --node node
```

This first verifies the saved snapshot, copies it into a new `work/reproduction-*` directory, and reruns the six bounded numerical continuations, airflow-data generation and reporting. It does not overwrite the original experiment files. The copied tree requires additional disk space. Full earlier stages can take hours; select them explicitly using `--help`.

Quick evidence verification without running experiments:

```sh
python3 scripts/fetch-research-data.py --verify-only
python3 outputs/research-reproduce.py
```

## Current findings and limits

- Local 3D Boids plus shared route guidance and the wall-priority controller completed the prescribed missions with up to 5,000 drones **with airflow off**.
- All three milestone 31 trajectory-refinement checks failed the frozen 1 cm criterion. Passage success does not establish accurate trajectories or general safety.
- Milestone 32 isolated sensitivity to inherited state differences in one selected interval. It is a diagnosis, not a controller fix or proof of chaos.
- Corrected exploratory wake coupling exists. Receiver response, overlapping wakes and real-flight accuracy still need independent validation. Historical coupled failures remain recorded.
- The intended contribution is a measured accuracy–computation trade-off. Novelty, physical validity, low-end hardware feasibility and real-time WebGPU performance remain unestablished.

## Repository structure

|Path|Contents|
|---|---|
|`outputs/`|Reports, protocols, numerical source snapshots, Three.js labs and retained results|
|`outputs/milestone-*-source/`|Versioned experiment implementations and per-run records|
|`outputs/archive-before-*/`|Historical delivery snapshots; standalone live labs are at `outputs/milestone-*-lab.html`|
|`data/research-data-manifest.json`|Inventory and checksums of release-bundled evidence|
|`scripts/`|Evidence packaging and verified restoration|
|`docs/`|Repository packaging/provenance notes|
|`work/`|Ignored local scratch files, installed plotting dependencies and reproductions|

The historical export began with fresh Git history and removed or replaced local machine paths, browser/GPU/CPU/OS/runtime identity and host-memory/load metadata. Scientific trajectories and model parameters were preserved; see its [privacy audit](docs/public-release-audit.md) and [change inventory](docs/public-export-changes.json). Older embedded manifests describe original private records, so their hashes may differ for listed sanitized files. The top-level output manifest verifies that historical snapshot. Hardware-specific comparisons from that export are limited by its withheld specifications.

New research checkpoints retain the nonprivate hardware descriptions, software versions, executable hashes and resource observations needed to interpret their experiments. Their own manifests and privacy disclosures define the retained scope. Private home paths, process identities, browser profiles, transport authority, user chats, authentication files and local environments remain excluded.

No open-source license has been selected for original project material. Third-party files retain their existing notices; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
