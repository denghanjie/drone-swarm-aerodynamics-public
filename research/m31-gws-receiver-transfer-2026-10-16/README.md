# M31: exposed GWS receiver transfer

Completed descriptive comparison, source `ffec6dccee9def5acc473cd907417d09533bc636`. The original 14-row run was already exposed. The law and nominal-RPM baseline bridge were tested together; no fitting or new holdout claim.

Read [plain-language findings](MILESTONE-SUMMARY.md), [exact aggregates](results/aggregate.json), [claim ledger](RESULT-CLAIM-LEDGER.md), and [next decision](NEXT-DECISION.md). The primary interpolated-baseline RMS CT gap is 0.0319503 (51.8834% of baseline) across all 14 conditions; the secondary is 0.0126928 (20.6115%) across the nine reported-positive conditions. These do not establish statistical significance, original-model failure or physical adequacy.

One scoring invocation completed 42 roots / 2058 bisection iterations. One independent review passed 71 checks with a different root formula; display QA passed 16 checks. Both science/review allocations are closed. [Three.js evidence view](viewer/) is a static graph of actual aggregate records, with the historical Boids replay linked.

Source files and their 18-entry manifest remain unchanged. [Reproduction](REPRODUCE.md) requires official source inputs stored privately; [result reproduction notes](RESULT-REPRODUCTION.md) include the independent reviewer. See [final privacy review](FINAL-PRIVACY-REVIEW.md), [manifest](manifest.json), and [restart](POSTRUN-RESTART.md). Publication verification is recorded separately in `research/publication-receipts/m31-gws-receiver-transfer-2026-10-16.json` once completed.
