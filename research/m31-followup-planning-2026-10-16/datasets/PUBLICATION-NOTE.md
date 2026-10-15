# Public artifact allowlist and transformations

Only this `public/` directory is proposed for public integration. It is a separate desk-review package, not an addition to a frozen transport-campaign manifest.

The allowlisted scientific notes are `COMPATIBILITY-MATRIX.md`, `SOURCES-AND-MANIFESTS.json` and `SOURCE-SECTIONS.md`. Supporting artifacts are:

- `nanobench-pinned-manifest.json`: reduced directory entries, retaining exact paths, byte sizes, Git blob IDs and public download URLs.
- `nanobench-commit-projection.json`: commit/date/root-tree/parent identities; author and committer names, emails and account metadata omitted.
- `nanobench-tree-projection.json`: exact paths, modes, object types, sizes and blob/tree identities; API wrapper/action/account metadata omitted.
- `zenodo-17457069-projection.json` and `zenodo-13837470-projection.json`: selected public scientific metadata, creator attribution, license, provider description/use notice, and file manifest. Owner/account IDs and unrelated management metadata omitted.
- `nanobench-README.md`, `nanobench-LICENSE`, `A1b_multisine_sysid_rep1_metadata.yaml`, and `C4_battery_drain_rep1_metadata.yaml`: unmodified public repository text, each verified against its Git blob ID.

This note and `SHA256SUMS` complete the allowlist. Upstream licenses/notices are retained; the projections do not replace or broaden data licenses. No data-archive or CSV payload is included.

An initial connector request addressed the recursive tree by commit ID. Its wrapper labeled the top-level SHA as that commit ID, although the entries reconstruct the correct tree. A second request explicitly addressed tree `789b1a57d1908a81e46647d9eded7a310a0d7bf6` and returned that tree SHA with an identical entry array and `truncated=false`. The public tree projection uses this second response. Independent audit reconstructed all 33 tree objects, including the root matching the commit's tree identity; raw wrappers are not needed for public integration.

Raw Zenodo API responses, initial connector wrapper, intermediate commit/tree files, and drafts outside `public/` are **excluded**. The stated transformations are metadata reductions, not alterations to observations. No scientific data analysis, model fit, source execution or experiment was performed.
