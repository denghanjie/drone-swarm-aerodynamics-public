# Preparation claims and open requirements

| Claim | Status and evidence | Limit / challenge |
|---|---|---|
| The independent fixed-byte reference agrees with a second arithmetic and encoding route. | Supported for the deterministic fixture by `review/PURE-TEST-RESULTS.json`, with implementation in `review/byte_primitives.py` and `review/test_pure_bytes.py`. | Mathematical/source preparation, not an observed GPU output. |
| The byte predicates reject the listed corruptions while distinguishing consistent wrong bytes from an expected-file substitution. | 33 pure cases passed in the independent preparation. Cases and exact files are retained. | Not an exhaustive verifier proof; the actual-file and lifecycle checker is not implemented. |
| The page's intended order preserves actual mapped bytes in separate ordinary memory before releasing the GPU mapping. | Source-review question; see the retained independent static review and final source pins. | Source order and page self-report do not independently observe GPU execution, hardware ownership or release. |
| A later return through this GPU path will match the fixed expected bytes after process closure. | Untested hypothesis. No GPU/browser/operational execution allocated or performed here. | Requires a fresh protocol/source freeze, admitted runtime, actual return and file, independent post-closure review and complete external observation. |
| The overall drone-swarm research now has a useful, physically meaningful approximation at 5,000 drones. | Unresolved; no support is added by this preparation. | Numerical-reference failures, measured-physics compatibility, useful approximation accuracy/cost and fresh confirmation remain separate requirements. |

This package must not be cited as a successful GPU readback, real-time simulation, reliability estimate, historical failure explanation or research breakthrough. The previous successful ordinary-memory transfer remains a separately scoped result at commit `468b980b94ad406257207767099ad06874ecfa73`.
