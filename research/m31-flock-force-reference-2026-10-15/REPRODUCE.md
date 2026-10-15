# Reproduce or inspect this checkpoint

Original source freeze: `89c3b14e6d59f2446d257bd106e3af4bbcb029c6`. Original campaign is closed. Do not rerun in this evidence directory, edit frozen files or alter raw results. Independent reproduction must use a fresh isolated checkout at the source freeze and its own provenance records; verify all file sizes/SHA256s in freeze.json first.

Runtime: Node24.19.0, Python3.9.6, AppleM4, Darwin25.5.0 arm64. No scientific npm dependencies. Original command, with Node on PATH:

```sh
RESEARCH_SOURCE_COMMIT=89c3b14e6d59f2446d257bd106e3af4bbcb029c6 python3 research/m31-flock-force-reference-2026-10-15/source/run-step.py --id static-reference --timeout 300 -- node research/m31-flock-force-reference-2026-10-15/source/experiment.cjs
```

Read PROTOCOL.md, schema.json and preflight resolutions first. Each Float64 binary is little-endian. Each snapshot has four 16-value rotor rows and one 35-value vehicle row per drone, with exact field names in schema.json. Raw receiver NDJSON records retain input/output identity, per-receiver counters and prior geometry hashes. The independent reviewer and all original launch/results are retained under results/. Its one original invocation used --authorized-after-science; archive copies are evidence, not an invitation to rerun in the original campaign.

The independent review's original scientific-budget copy intentionally says terminal=false: it records the supervisor state before closure. The current budget adds review accounting and marks the campaign terminal. No raw or frozen scientific file was changed.

Serve the repository root locally and open research/m31-flock-force-reference-2026-10-15/viewer/. Vendored Three.js, WebGL and Web Crypto are required. The viewer checks byte hashes for original poses and raw load files. It renders exact snapshots, with glyphs enlarged3× and a thrust arrow scaled5m/N. It interpolates neither poses nor loads and performs no live physics. The postrun source/build-viewer-data.py hashes and packages saved evidence without a scientific evaluation.
