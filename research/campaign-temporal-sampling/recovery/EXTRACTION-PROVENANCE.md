# Archival extraction provenance

`extract_embedded.py` and `format_json_candidates.cjs` preserve the recovery-time process. They are archival staging scripts, not portable commands for a repository checkout.

The extractor expects a sibling `attached-viewer/` folder with the original reattachment filename, plus `github/campaign-tree.json` and `github/recovered/`. The formatter expects staging extraction outputs under `recovered/`. That temporary layout is not included in the published checkout. These scripts may create or replace extraction manifests and outputs, so they must not be run over the published evidence directory as if they were read-only verification tools. Their historical timestamp and staging-path labels must not be mistaken for a new run or a final publication inventory.

The unchanged standalone viewer preserves the exact source bytes. `RECOVERY-MANIFEST.json` records source literal locations and hashes, while `JSON-FORMAT-RECONSTRUCTION.json` records restored JSON serialization and independently identified original objects. The final checkout file paths and identities are in [PUBLISHED-FILES.json](PUBLISHED-FILES.json). It excludes its own bytes to avoid a recursive self-hash; the Git tree supplies its own immutable object identity.

For portable offline verification and reconstruction of the retained dense transport parts, use the separately tested [reconstruction instructions](README-RECOVERY.md). This operation does not regenerate absent scientific records.
