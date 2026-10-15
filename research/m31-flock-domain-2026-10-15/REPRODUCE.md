# Reproduce the geometry-only checkpoint

The source freeze is e23e053dfe31ce98163b7e0b6d1a28d849d7e9f3. Existing invocation records are immutable: **do not rerun in this evidence directory**. Reproduction belongs in an isolated checkout at the source freeze with a new output location/record, preserving the original. No npm dependency installation is needed for the scientific driver.

Runtime used: Node24.19.0, Python3.9.6, Darwin25.5.0 arm64 on AppleM4. CPU/memory records are execution diagnostics, not device performance claims. Scientific source, exact input files and SHA256s appear in freeze.json. Verify every size/hash first. Before the original launch the exact freeze bytes were fetched independently from GitHub and matched locally.

Original command (Node available on PATH):

```sh
RESEARCH_SOURCE_COMMIT=e23e053dfe31ce98163b7e0b6d1a28d849d7e9f3 python3 research/m31-flock-domain-2026-10-15/source/run-step.py --id domain-census --timeout 300 -- node research/m31-flock-domain-2026-10-15/source/experiment.cjs
```

Read PROTOCOL.md and PREFLIGHT-RESOLUTIONS.md before reproducing. The protocol forbids field/force/dynamics evaluation, a second invocation, enlarged caps, post-exposure patches or tolerance changes in the original campaign. Older advisory design proposals were resolved before freeze; the final protocol/config govern.

Each raw receiver stream has one JSON row per original vehicle ID, in ascending order. Inflate codesDeflateBase64 using zlib deflate, check its SHA256 against both recorded hashes, and interpret byte4*source+rotor using protocol codes0–7. Self entries are included as0; separate self/outside-center counts are in summaries. Code3 coordinates are saved; code4 identities are complete but their geometry values are not retained. The independent saved-data review does not rerun geometry.

Serve the repository root with any local static HTTP server, then open research/m31-flock-domain-2026-10-15/viewer/. Three.js is vendored. The viewer verifies original pose, result, per-snapshot raw and selected code hashes. It shows exact poses only and requires a browser supporting WebGL, Web Crypto and DecompressionStream. The viewer does no physics and supplies no simulation speed measurement.
