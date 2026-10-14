# Current status: AUDIT-C1 attempt terminally blocked

The one-shot launch began at **2026-10-14 04:53:51 UTC** and ended as **`integrity_blocked`** during performance-schedule verification, before any numerical child launched. All **82 configured children** and the independent correctness gate were unrun. No exact-equivalence result, speedup measurement, new flight trajectory or physical validation was produced. The release permits no retry.

- [Postrun milestone](postrun-report/MILESTONE.md): the terminal outcome and limits on conclusions.
- [Actual-record-linked Three.js demonstration](postrun-demo/index.html): the rejection receipts alongside the unmodified historical replay.
- [Schedule diagnosis](postrun-diagnosis/REPORT.md): the supervisor's block-6 order differs from the prescribed schedule.
- [Machine-readable evidence](postrun-report/EVIDENCE.json): exact original receipt identities and source fields.
- [Static display checks](postrun-report/STATIC-CHECKS.json): syntax and link verification only; no browser run.
- Original receipts: [start marker](robustness-review/results/WINDOW-STARTED.json), [supervisor](robustness-review/results/SUPERVISOR.json), [final accounting](robustness-review/results/FINAL-ACCOUNTING.json).

The frozen [README](README.md), [original demo](demo/index.html) and other prospective documents intentionally retain their historical pre-execution wording. They were not rewritten after the attempt. This new status page and the separate postrun files explain the actual outcome without changing frozen evidence.

The embedded Three.js paths come from the earlier campaign, which remains incomplete and unqualified. The new wrapper generates no trajectories. A future experiment requires a separately authorized prospective review and release while preserving this consumed attempt and failure evidence.
