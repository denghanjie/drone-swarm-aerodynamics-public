# Independent exact-airflow verification

This directory contains independent model-relative correctness checks, adversarial fixtures, serial performance measurements and replay identity checks for the same-equation airflow campaign. It does not establish physical accuracy, flight safety or large-swarm feasibility.

Place it at `research/campaign-exact-efficiency/robustness` in the pinned repository. The adapter then finds historical and current source without network access. Alternatively set `EXACT_REPO_ROOT` to that repository root. Numerical scripts need Node.js built-ins; replay packing/identity checks use Python's standard library.

## Reproduction

- `node checks.cjs` runs eight tiny deterministic checks.
- `timeout 60s node checks.cjs --full` runs the final 85-fixture suite, metamorphic checks, reusable-workspace ownership checks and isolated malformed/range-input tests.
- `node audit-primary-timing.cjs` independently recomputes primary raw timing statistics. It does not rerun benchmark algorithms.
- `timeout 290s python3 run-independent-batch.py --serial-lease` reproduces the frozen independent batch only when no other CPU-heavy task is running. Its source-hash guard must match the frozen candidate. Each job has its own 60-second external limit, and the whole batch stops on its first failure.
- `node audit-pipeline-boids.cjs` checks primary pipeline arithmetic, recorded endpoints and recomputed fresh fields without rerunning trajectories.
- `python3 check-replay.py ..` checks raw saved records against the standalone HTML and source. It is not browser/rendering QA.
- `python3 check-offline-package.py .. --output raw/reproduced-offline-package-audit.json` checks inline/module syntax and bundled link coverage without launching a browser.

Read `PLAN.md`, `AMENDMENTS.md` and `FINDINGS.md` before running further experiments. Do not interpret the serial-window flag as an automatic resource grant. Source hashes and the distinction between original and portable copies are recorded in `MANIFEST.json` when staging.

## Evidence

`raw/independent-checks.json` is the refreshed final functional result. `raw/development-v0-*.json` retains the initial independent-suite version, which lacked explicit huge-coordinate regressions. Its actual candidate hash is the already-corrected A2 hash, as explained in the append-only chronology correction; the original candidate failure is separately retained by the physics review.

`raw/independent-field-*.json` and `raw/independent-pipeline-*.json` retain every paired repetition, all fixtures, source identity, checksums and failure status. Machine/runtime/process observations are explicitly withheld from public copies while original records are retained separately. `raw/independent-batch-ledger.json` records all fifteen bounded jobs. `raw/primary-timing-audit.json` audits the thirty primary timing files without replacing them. Numerical results from different harness scopes are not pooled.

The fixed source rejects position components outside ±1,000,000 m as a declared numerical API domain. This deliberately differs from unsafe inherited behavior. Model-domain checks for near wake and excessive tilt remain separate.
