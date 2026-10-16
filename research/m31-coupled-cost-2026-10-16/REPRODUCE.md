# Reproduction and restart

Source freeze pins every source file and referenced input/reference record by repository-relative path, byte count and SHA256. Published source commit and remote-manifest digest are supplied to source/run.py; it verifies local/committed pins and uses an exclusive invocation lock. Do not remove locks or rerun a closed allocation. Use a new explicitly scoped package/checkout for independent reproduction.

Requirements: little-endian Node with standard built-ins; Python3 and NumPy for saved-record review; git; Darwin ps/pmset/sysctl environment queries. Missing power/physical-core observations are unknown, not invented. No package install is required on the measured machine. Exact Node/V8/executable hash/hardware/kernel recorded in evidence.

From the source commit, after independent remote manifest verification:

```sh
python3 research/m31-coupled-cost-2026-10-16/source/run.py candidate NODE_EXECUTABLE VERIFIED_MANIFEST_SHA SOURCE_COMMIT
python3 research/m31-coupled-cost-2026-10-16/source/run.py review PYTHON_EXECUTABLE VERIFIED_MANIFEST_SHA SOURCE_COMMIT
```

Use actual interpreter paths locally; public records omit them. Candidate300s/review60s, one each. Review only saved outputs, not a scientific rerun. Stdout/stderr and source commit are captured by the supervisor. Unexpected failures and incomplete prefixes stay saved. The background static server on port8876 is independent; do not stop it.

Follow POSTRUN-RESTART.md after scoring. Keep source and result publication receipts in research/publication-receipts so frozen manifests are not rewritten. Screenshots/UI checks belong to a later separate viewer QA record; they cannot repair scientific failures.
