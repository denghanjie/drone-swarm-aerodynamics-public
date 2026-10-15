# Reproduction and evidence layout

Original source freeze88dc542604d902909b7cc96c0bd0ca93b88cab0c; SHA of freeze.json855f71dc0f8993ed1fb51eb5e882cfe9c07c5bb5f37ea275e4705bf33114516c. Original science is closed; never rerun in this evidence directory or change its caps/source/raw. Independent reproduction belongs in a new isolated checkout at the source freeze with its own provenance/output records. Verify all66direct input/source hashes first.

Node24.19.0/Python3.9.6/AppleM4/Darwin25.5.0arm64 were used. No scientific npm dependency installation. With Node on PATH, the original command was:

```sh
RESEARCH_SOURCE_COMMIT=88dc542604d902909b7cc96c0bd0ca93b88cab0c python3 research/m31-source-omission-2026-10-16/source/run-step.py --id bounded-omission --timeout 300 -- node research/m31-source-omission-2026-10-16/source/experiment.cjs
```

Read PROTOCOL.md, schema.json and PREFLIGHT-RESOLUTIONS.md first. Every f64 row has17Float64LE values, with distinct load and state layouts in schema.json. Historical inputs reference original exact pose slices and retained independent full loads; new/fixture exact states are retained before evaluation. Per-receiver decisions contain2bits/source (zlib deflate/base64), SHA256, ascending positive-bound list and upward summed bound. New/fixture audit rows contain retained independent positive-omission terms, zero-inspection counters, root diagnostics and full load row. Scalar/domain/case/timing results are separate. All240raw files must be retained even when not listed recursively by raw/result.json; final manifest is complete.

Frozen query attempts are conservatively charged full shapes before execution, including expected invalid cases. Actual field counters appear in completed call records. Dedicated timing records exclude I/checking/persistence; do not pool correctness-call elapsed times with benchmark repeats. The warmup is rep0; reported statistics use reps1..5. No confidence intervals are inferred from those technical repeats.

Serve the repository root over local HTTP and open research/m31-source-omission-2026-10-16/viewer/. Three.js is vendored. WebGL/Web Crypto/DecompressionStream are required. Viewer data includes direct saved-file hashes; source/build-viewer-data.py only reformats historical independent scalar rows for display. No fields, geometry regeneration, root solving or timing occurs in that postrun builder. The displayed spatial relationships refer to the selected receiver; orange links are bookkeeping lines, not measured streamlines. Invalid fixtures show poses without invented force predictions.
