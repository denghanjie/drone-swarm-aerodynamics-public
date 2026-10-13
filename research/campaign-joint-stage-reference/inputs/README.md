# Dense inputs acquired for proposed follow-on work

These are newly materialized copies of historical byte arrays, not new simulation outputs. Acquisition used four public, immutable raw GitHub URLs at commit `b9bd5065d02561920af27468f5e4740b301bd174` in `denghanjie/drone-swarm-aerodynamics-public`.

## Files

- `parts/`: four original dense gzip transport parts, preserving the inventory filenames and bytes.
- `arrays/s840131-p1-a4.dense.f64`: 13,928,576 uncompressed bytes; SHA-256 `282a31372479630585fa087e0e5d7cbfde6c565ba3cfe146e72fe28f8881af49`.
- `arrays/s840137-p1-a4.dense.f64`: 13,928,576 uncompressed bytes; SHA-256 `0264220304fa02d7e14f9983beb818b3edc5ad3cba7a2f1372a2e73633c46954`.
- `metadata/`: newly authored wrappers containing the original full nested dense sidecar objects and their recovery provenance. These wrappers are not the original lost standalone sidecar bytes.
- `INPUT-ACQUISITION.json`: exact URLs, HTTP transfer receipts, all original part/dense identities, mapping, and verification results.
- `INSTALLED-INPUT-VERIFICATION.json`: independent post-install re-read and hash/length checks.
- `http/`: public HTTP response headers for the four successful transfers.

Each array is little-endian Float64 bytes with original shape `[6401, 16, 17]`, cadence 0.00015625 seconds, and full field names in its metadata wrapper. Float values were not interpreted during acquisition.

The compressed streams were decoded directly across their ordered parts; no extra joined `.gz` file was retained. Every part's Git blob identity and size, both original whole compressed SHA-256/Git identities, and both original uncompressed SHA-256/byte lengths passed. The gzip streams terminated cleanly. Parts were preserved as agreed for the proposed study's input budget.

Storage: arrays 27,857,152 bytes; parts 26,736,688 bytes; total retained data 54,593,840 bytes, plus small receipts and metadata. This input step performs no field evaluation, trajectory integration, numerical diagnostic, gate recomputation, or simulation. Any subsequent numerical work needs its own approved plan and budget.

The GitHub MCP blob reader's gzip decoding limitation is a format issue. These bytes were acquired through authorized public shell HTTPS reads, with normal TLS verification and no credentials.
