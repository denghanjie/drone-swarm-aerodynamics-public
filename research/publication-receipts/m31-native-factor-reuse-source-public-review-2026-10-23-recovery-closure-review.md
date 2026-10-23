# Native factor reuse public-byte recovery closure

The separately authorized raw-CDN recovery closed **failed**. None of the eight missing inputs was recovered. The original source gate remains at **66/74** verified file pins, with **207,305,212 bytes** across eight input pins still lacking complete public-byte proof. No composite success receipt was created.

- Recovery: 16 requests, two per file, peak concurrency two; 3,424,392 captured bytes; 416.282142 seconds; zero requests remaining.
- Recovery failures: 12 outer 45-second timeouts (nine after HTTP 200 headers, three without a parsed HTTP status), plus four curl SSL connection timeouts. No underlying network cause is established.
- Original acquisition: all 24 failures remain unchanged: 22 attempt timeouts and two nonzero cancelled streams. All 40 failed public attempts remain in separate journals.
- Closure: receipt/journal event equality, consecutive numbering, request start/end pairing, exact byte accounting and the two-transfer limit were read back separately. All 74 frozen pins plus the source manifest were freshly rehashed as opaque bytes; all 75 length/SHA-256/Git blob identities matched.
- All four scientific/display allocations were unstarted at recovery start, recovery end, and this readback. No model, controls, auditor, benchmark, archive decompression, log aggregation or UI allocation ran.

The first readback classification assertion omitted the three no-status outer timeouts; the retained events were inspected and the classification corrected. This administrative correction did not rerun recovery or science.

This review confirms administrative closure, **not source-gate success or a numerical result**. Further public-byte recovery needs a separately specified and authorized procedure.

Receipt: `research/publication-receipts/m31-native-factor-reuse-source-public-review-2026-10-23-recovery-failure.json` (119980 bytes), SHA-256 `d9818febe1df1b215545c3f006a7cdee4aaa865bb9bdea30f30ee64def3f5a47`.

Journal: `research/publication-receipts/m31-native-factor-reuse-source-public-review-2026-10-23-recovery-events.jsonl` (68639 bytes), SHA-256 `7bd24a8afc26f0b0364a90cca9f2685894758463dd6798113872e32623ddc75c`.
