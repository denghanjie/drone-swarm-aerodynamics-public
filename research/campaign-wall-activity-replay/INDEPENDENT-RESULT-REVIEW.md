Public edition: witness names below identify the original archived artifacts. All decoded witness values are available in [WITNESSES.json](WITNESSES.json); no binary is distributed. Runtime details are summarized in [PROVENANCE.json](PROVENANCE.json).

# Independent saved-evidence review
2026-10-15 UTC. VERIFIED within the declared sampled scope; no controller, initializer, wake or dynamics rerun.

RESULT.json SHA256 7d667d68d2fcc7b7d86dcfde873def39f29336b5dacf91f4924f48b2d4c88402; witnesses.f64 SHA256 0ea6f881125000fa07aafbb0006bf1b7085d0824f0590209266e5f30197afda5. All nine freeze entries and 15 functional source bodies match their retained hashes.

Coverage is 50 pre-control frames, ticks 0..25088 by 512, excluding terminal frame 50. Receipts record 50 original plus 50 instrumented controller returns, 800 observed vehicle calls and 4,800 post-pass speed tests. Independent geometry arithmetic on the saved states and all 34 published boxes reproduces 402 wall rows (302 vehicle-ticks) and 7,460 ordered pair rows: six passes give 2,412 wall and 44,760 pair tests, totaling 47,172.

All wall fires/corrections and post-pass speed changes are zero. Pair fires total 697 versus 677 nonzero changes; rounding can make a fired correction unchanged. Maximum pair correction is 0.2539216624752528 m/s. Decoded all 13 witnesses: complete nonoverlapping byte coverage, finite values, actual 17-entry wall normals, source-geometry IDs/normals/lower bounds, branch predicates, before/after projection, slacks and norms agree within 1.39e-16. Every retained maximum equals its aggregate.

The unchanged runner asserts exact all-returned-output binary64 parity and input nonmutation for all 50 frames; 50 distinct equal-output hashes are retained. Full outputs and dense pass tapes are absent, so parity, global maxima and zero-activity coverage are supported by the reviewed instrumentation rather than independently regenerated here.

Exit 0; outer wall 0.354 s. The earlier missing-/usr/bin/time wrapper stopped before launch. Raw outputs 10,189 B; no timeout or truncation. This diagnoses sampled early passes only; event-stress remains EVENT_EXPOSURE_INSUFFICIENT. No net trajectory causality or physical validation follows.
