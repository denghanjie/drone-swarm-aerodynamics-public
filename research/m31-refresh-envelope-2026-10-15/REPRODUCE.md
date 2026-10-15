# Reproduction and evidence reading

Frozen source commit: `f56909390c4875db5a9241ba6bc79596b84628a6`. Node v24.19.0; Python 3.9.6 supervisor; Apple M4, Darwin 25.5.0 arm64. Source and dependency hashes are in freeze.json. Existing local vendor Three.js is used only for display. No dependency installation.

The campaign is terminal. Never overwrite raw evidence or rerun in this checkout. Numerical reproduction requires a separate disposable checkout at the pre-execution source commit and a separately accounted invocation:

```sh
RESEARCH_SOURCE_COMMIT=f56909390c4875db5a9241ba6bc79596b84628a6 python3 research/m31-refresh-envelope-2026-10-15/source/run-step.py --id envelope-challenge --timeout 120 -- node research/m31-refresh-envelope-2026-10-15/source/experiment.cjs
```

No repeat is authorized by this completed checkpoint. Technical timings will vary across runs. The supervisor and exclusive start marker reject recorded job IDs and preserve failures. All frozen protocol/source bytes remain unchanged.

`raw/samples.ndjson` contains 4,001 ordered ticks at 0.25 ms, prescribed receiver position/velocity, and each method's four rotor inflows plus total modeled thrust/roll/pitch. `left` contains the pre-refresh value at that exact pose; there is no left limit at time zero. `bound.intervals` uses reference-minus-held signs. Absolute peak/RMS metrics are insensitive to sign. `raw/envelope-decisions.json` includes all attempted horizons and accepted detailed bounds. The terminal refresh is counted, but has no subsequent horizon. All 36 timing files include one warmup and five rotated-order recorded repetitions per method; checksums match saved primary-grid loads exactly.

The independent verifier in `source/recompute-saved.py` accepts repository root as its sole argument, writes `/tmp/m31-envelope-review.json`, and performs arithmetic on saved JSON only. Do not confuse this with rerunning the model. The review reports its original script hash; copying the file does not change it. The checker-correction note identifies the unavailable original first JSON and any reconstructed artifacts honestly.

Serve repository root with `python3 -m http.server 8876 --bind 127.0.0.1`, then open `/research/m31-refresh-envelope-2026-10-15/viewer/`. The viewer hashes result and samples before enabling controls. The demonstration is prescribed-pose/model-load replay, not flight simulation or a performance benchmark. The delivery manifest excludes itself and lists all other checkpoint payload files.
