# Reproduction and saved-evidence schema

Frozen source commit 661bb14c99521ef2b1d3350600e202b4fb44d5b9. Node 24.19.0 and Python 3.9.6; Apple M4, Darwin 25.5.0 arm64. `freeze.json` lists exact scientific source/configuration/protocol/dependency hashes. No dependency installation.

This campaign is complete and must not be rerun or overwritten. Reproduction requires a separately accounted disposable checkout at the source commit:

```sh
RESEARCH_SOURCE_COMMIT=661bb14c99521ef2b1d3350600e202b4fb44d5b9 python3 research/m31-predictor-stress-2026-10-15/source/run-step.py --id predictor-stress --timeout 120 -- node research/m31-predictor-stress-2026-10-15/source/experiment.cjs
```

A successful recorded invocation rejects automatic retries. Technical timings will vary. Protocol/source edits after results require a new campaign, not changing this evidence.

Six raw NDJSON files each retain 4001 ticks. Time=tick×0.00025s. `states` contains every vehicle's 17 components: position3,velocity3,quaternionxyzw4,body rate3,nominal motor thrust4. Vehicle0 is the primary receiver. `referenceAllWinds` and `independentAllWinds` store all vehicles×four rotor inflows; `independentReceiverLoads` is body thrust/roll/pitch. `values` contains five variants, four receiver0 winds, three receiver0 loads, refresh flags and optional old value at that exact update boundary. Both initial sample and terminal refresh are included; initial has no left limit. Angular/linear inputs are prescribed, not integrated flight.

Each `*-accuracy.json` preserves metrics, startup/reversal signed extrema, independent discrepancy maxima and primary-grid checksum. `result.json` adds timing summaries and all18 prospective comparison decisions. There are 180 raw timing files: 30 warmup and 150 recorded records, rotating case and method order. Checksums equal the retained primary-grid samples exactly. No independent data enter the timed model calls.

The independent `source/recompute-saved.py` accepts repository root as its argument. It reads retained JSON only and does not invoke fields, cases, dynamics, model roots or benchmarks. Its recorded report and script hash are in results. Reverification is distinct from rerunning the experiment.

Serve repository root using `python3 -m http.server 8876 --bind 127.0.0.1`, then open `/research/m31-predictor-stress-2026-10-15/viewer/`. It checks each file's SHA256 against viewer/index.json before enabling controls. The 3D viewer interpolates no scientific trajectories; its slider selects exact saved ticks. The delivery manifest lists all payload files other than itself.
