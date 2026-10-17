# Reproduction contract

This is a source-preparation checkpoint until source freeze, public verification and reviewed single-use allocation. Historical source/result files remain immutable.

Runtime: Python executable SHA256 7a314947596fc484d4ec36ffc28e843b78d6d749c68736f8b5c24e7333f418eb (18,058,560 bytes), stdlib only. Run with -I -B. Source manifest binds every consumed file. Producer entry point is source/analyze.py:run(root); independent checker is source/check.py:run(root). Neither is imported before manifest and runtime checks.

After the exact source commit and source-manifest SHA256 are known, bounded authorized dispatch uses:

    RESEARCH_EXECUTION_CONTEXT=tool-require-escalated PYTHON -I -B research/m31-direct-load-diagnostic-2026-10-17/source/run.py analyze MANIFEST_SHA SOURCE_COMMIT
    RESEARCH_EXECUTION_CONTEXT=tool-require-escalated PYTHON -I -B research/m31-direct-load-diagnostic-2026-10-17/source/run.py check MANIFEST_SHA SOURCE_COMMIT

PYTHON means the verified pinned executable, not an arbitrary interpreter. The attestation records the actual tool launch context; do not set it for a different context. The checker requires successful producer output bound to the same source identity. Source publication receipt is an operational prerequisite created after freeze, not a self-referential manifest pin.

Each stage consumes its exclusive attempt marker even on failure. CPU120/121s, wall alarm180s, output16MiB, observed peakRSS512MiB acceptance; cutoff2026-10-17 02:00UTC. Alarm scope excludes interpreter startup and teardown. Do not reopen a consumed attempt, replace records, extend precision or change the mask after seeing outcomes. A separate reproduction needs an explicitly new allocation and new output directory, with deviations declared; none is automatically authorized by these instructions.

Output timing measures oracle diagnostic processing, not simulation performance. Six reused snapshots cannot establish new-condition robustness or real-world accuracy.

Host scope: macOS/Darwin only for this allocation; ru_maxrss is interpreted in Darwin byte units and dispatcher rejects other platforms.
