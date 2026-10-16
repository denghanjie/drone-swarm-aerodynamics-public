# Reproduction

Use Python 3 (standard library only) on a Unix-like environment providing resource and signal. No installation was needed. Fetch the two exact text inputs from the official URLs in config.json into a private directory, observing the source's citation/reuse terms. Verify SHA-256. Keep the full source tables and complete derived rows private; public output is aggregate only.

From the repository root:

```sh
python3 research/m31-gws-receiver-transfer-2026-10-16/analyze.py --test
python3 research/m31-gws-receiver-transfer-2026-10-16/analyze.py --config research/m31-gws-receiver-transfer-2026-10-16/config.json --static PRIVATE_STATIC_TXT --axial PRIVATE_AXIAL_TXT --public-output NEW_AGGREGATE_JSON --private-output PRIVATE_NEW_ROWS_JSON
```

The command refuses output overwrites, pins input contents, limits CPU/wall time to 15 seconds, computes all three declared baselines and records source/input/result hashes. Source-commit provenance changes when reproduced at a later packaging commit; compare scientific fields separately. No stochastic seed or timing study exists. The public aggregate excludes complete row predictors/residuals; the independent reviewer can inspect retained private evidence locally.
