# Static schema-edge test disposition

**Twenty inert predicate tests passed.** The operational saved checker, diagnostic, browser and experiment were never imported or invoked. This is pre-freeze source/schema verification, not a consumed saved-review invocation and not a transport result.

`run-inert-schema-tests.py` reads checker text with Python AST parsing and extracts identified pure expressions. A restricted interpreter permits only constants, inert dictionaries/sets, comparisons, boolean decisions, bounded comprehensions, and narrowly allowlisted pure helpers. It cannot execute operational imports, `main()`, paths, locks, timers, process launch or browser code from the checker. Exact source bytes, extracted text, AST structure and expression hashes are preserved in the accompanying artifacts.

The requested edge cases were covered:

| Edge | Observed pure-predicate behavior |
| --- | --- |
| Different producer wrapper fields | Extra metadata is allowed; a required shared-field mismatch is rejected. |
| Exact persistence with failed acknowledgement | Classified separately and remains within complete-observation review scope. |
| Completely observed failed fetch | Preserved as a failed transfer and remains within complete-observation review scope. |
| Incomplete trace | Honest incomplete flags remain consistent; overall outcome is incomplete and cannot pass this review scope. A falsely true completeness flag is rejected. |
| Extra application POST | Two sink POST entries violate the single-POST predicate. |
| Corrupt or mismatched payload | A post-record file change is rejected. An honestly recorded content mismatch is separate from byte-count completion; it is not a successful synthetic transfer. |
| Absent result | A manifest built from present files fails the required-evidence predicate when `results/result.json` is absent. Real filesystem-error handling was not simulated. |
| Nonzero external exit | Exit 1 is rejected; a completed exit 0 is the positive control; a yielded/incomplete tool session is rejected. |

## Pre-freeze regression and correction

The initial checker conflated the producer's `sink.complete` with expected-fixture equality. The producer sets this field when exactly 3,840 bytes were written and closed; those bytes need not match the predetermined fixture. The preserved old predicate rejected a coherently recorded wrong-content transfer. The corrected predicate instead binds the sink receipt to the independently read persisted bytes and digest, while expected-fixture equality and browser acknowledgement remain separate. Its event projection is checked explicitly.

The old checker is preserved as `check-records.pre-edge-test.py.txt`, SHA-256 `8ea847daae61421bc0291eb19cca48ae639971462fa01b6ca01e34ad74c58ade`. The tests record the original predicate's rejection and the corrected predicate's acceptance of the same coherent wrong-content observation. They also confirm that a changed file with the original saved metadata is rejected. No frozen diagnostic source or historical result was changed.

The tested corrected checker SHA-256 is `f58ceecf9fe13ded86697c7fc5a0ade7e9cf82ec60ab3a5479015d3e10588dbe`. `INERT-PREDICATES.json` contains its exact source pin and every extracted expression; `INERT-TEST-RESULTS.json` contains 20 outcomes, fixture identities, and the exact interpreter pin.

This disposition clears the tested pure schema decisions only. It does not claim end-to-end checker execution, source-independent empirical validation, private-trace verification, timing correctness, or any observed transport success. The real new evidence, separately frozen review source/manifest, actual single review invocation, and externally bound completion remain later gates. A failed operational review must still be preserved without retry.
