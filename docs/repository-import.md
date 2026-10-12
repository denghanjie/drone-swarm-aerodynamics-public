# Public research export

This repository publishes research through milestone 32 as a sanitized snapshot with fresh Git history. The original local records and their private GitHub repository are retained separately. Neither that Git history nor its evidence archive is copied into this publication.

The public copy removes machine-specific paths, saved browser/GPU/CPU/OS/runtime identities, and host-memory/load records. Scientific trajectories, controls, model parameters, measured compute times, negative results and research limitations remain. The [change inventory](public-export-changes.json) records original and public hashes without recording redacted values. Removal of host specifications limits independent interpretation of hardware-specific timings.

The current `outputs/research-manifest.json` is regenerated for the sanitized snapshot. Historical manifests and source hashes remain provenance records of the original experiments: their checks can differ for the explicitly listed sanitized files. Do not interpret those differences as fresh experimental validation or silently erase them. Original private copies remain the source of the unsanitized historical evidence.

Git contains source, reports and small artifacts, including the current Three.js demo. Large JSON and Float64 files are bundled in release `v0.1.0-public`; each public member and the compressed archive are pinned in `data/research-data-manifest.json`. The archive uses relative paths and normalized ownership and timestamps. Restore it with `scripts/fetch-research-data.py`, then verify using `outputs/research-reproduce.py`.

The export does not modify the physical solver. One historical verification helper now invokes `node` through PATH instead of a private absolute executable location. Reports describing old machine environments explicitly mark those details as withheld. Numerical data have not been rerun for this publication.

Future experiments can collect local metadata again. Review all new commits and release assets before publishing them. Never upload the original private evidence bundle to this repository.
