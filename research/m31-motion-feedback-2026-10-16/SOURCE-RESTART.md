# Frozen source execution

Before execution, verify the exact published source manifest against GitHub and every local/committed pin. Use the installed Node and Python/NumPy only. No dependency installation or new acquisition. Commands (from repository root; supply verified values):

```
python3 research/m31-motion-feedback-2026-10-16/source/run.py candidate NODE_EXECUTABLE MANIFEST_SHA SOURCE_COMMIT
python3 research/m31-motion-feedback-2026-10-16/source/run.py review PYTHON_EXECUTABLE MANIFEST_SHA SOURCE_COMMIT
```

Each consumes an exclusive results invocation lock. Do not delete locks or retry failures. One continuous supervisor measures wall time; separate process clocks are never subtracted. Candidate limits300s wall/280s cooperative,768MiB sampled RSS,32MiB total evidence. Review120s. No overlapping scientific/QA workloads. Failure and negative outcomes remain saved. Display QA is separate and runs no solver.

For later external reproduction use a separate checkout at the frozen source commit, not this campaign's consumed result directories. Keep localhost8876 running. No public research conclusion until saved-only review and publication checks. The previous physical access and storage allocations remain closed.
