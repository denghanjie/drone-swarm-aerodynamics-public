# AUDIT-C1-R3: results-only checkpoint

**Partial audit; terminal status `integrity_blocked`.** The one-shot attempt began on 2026-10-14 at 05:41:00 UTC. The synthetic job passed all 81 cases. The next job stopped with “Available endpoint original signature mismatch” after 20 paired observations and 19 completed historical-anchor checks.

The retained-data diagnosis identifies mixed historical/current tick units. The actual one-second state was compared with an earlier-time anchor. Captured baseline and candidate outputs agree, but that does not turn the incomplete audit into a pass.

One of 82 jobs passed, one failed, and 80 never started. The independent full correctness gate and all 64 performance jobs were unrun. There is no full-corpus correctness, speedup, new-flight, qualified-reference, or physical-validation conclusion. No retry was made.

- [Results-only milestone](postrun-report/MILESTONE.narrow.md)
- [Selected-record Three.js presentation](postrun-demo/index.narrow.html)
- [Event-only anchor diagnosis](postrun-diagnosis/public-narrow/ANCHOR-DIAGNOSIS.md)
- [Summary-only retained-evidence review](postrun-review/REVIEW.narrow.md)
- [Focused literature supplement](postrun-literature/narrow/README.md)
- [Original synthetic receipt](implementation/results/receipts/synthetic.json), [original failed-state receipt](implementation/results/receipts/saved-json-states.json), and [original final accounting](robustness-review/results/FINAL-ACCOUNTING.json)

This is a separate results-only publication derivative while broader inventory publication remains pending. Detailed source/input/runtime/validation inventories and the raw failure capture are outside this subset. It is incomplete for full reproduction. Original records, local presentations, and prior publication derivatives are preserved; scientific results have not changed.

[Results-only publication scope notice](publication-review/PUBLIC-RESULTS-ONLY-NOTICE.md).
