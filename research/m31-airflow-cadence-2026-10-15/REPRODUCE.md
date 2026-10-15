# Reproduction

Source commit before outcome: `fd857ed1f5a4662ff98635e1998b53944b98738a`. Dependencies: Node v24.19.0; Python3.9.6 supervisor; existing CommonJS files listed by `freeze.json`. No package installation. Host: Apple M4, Darwin25.5.0 arm64. Independent oracle imports none of the original model implementation.

To repeat numerically, use a new disposable checkout at that source commit. It precedes results and has no start marker. Never rerun in this completed checkpoint or overwrite its raw evidence. A reproduction is a separately accounted campaign, not continuation of the closed one.

```sh
RESEARCH_SOURCE_COMMIT=fd857ed1f5a4662ff98635e1998b53944b98738a python3 research/m31-airflow-cadence-2026-10-15/source/run-step.py --id cadence-pilot --timeout 120 -- node research/m31-airflow-cadence-2026-10-15/source/experiment.cjs
```

Do not expect identical performance timings on another run. Numerical outputs are compared at the declared SI tolerances; timed-run query checksums are exactly checked against the same run's retained primary samples. The once-only marker and supervisor retain failures. No outcome-driven patches/retries are permitted in this protocol.

All 3.2 MB of raw JSON are committed. `lateral-pass.json` and `offset-approach.json` contain exact prescribed input positions and four treatments for all 2,001 ticks. Time=tick×0.0005 s. Wrench order is total thrust N, roll/pitch/nominal-yaw N·m. `left` holds old inflows at the current exact refresh pose before replacement; t=0 has none. RMS uses ordinary uniform samples; peaks additionally include all left limits. Input velocities/orientations/thrusts are fully specified in config and source. This is not a saved flight trajectory.

For the viewer, serve the repository root using `python3 -m http.server 8876 --bind 127.0.0.1` and open `/research/m31-airflow-cadence-2026-10-15/viewer/`. It hashes the exact raw records against `viewer/index.json`, then draws recorded poses/inflows. Moving its slider or playing the recording does not execute flight dynamics or establish simulation performance.

The independent saved-record verifier is `source/recompute-saved.py`; invoke it with the repository root as its sole argument. It writes `/tmp/m31-cadence-review.json`, recomputes metrics and accounting from retained JSON, and does not call any aerodynamic or dynamics implementation. Its own timing will vary. The saved review preserves the original verifier hash.
