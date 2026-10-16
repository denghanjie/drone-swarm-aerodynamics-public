# Oracle omission renewal: operational delta review

**Disposition: accepted for the exact pins below. No material blocker identified in this bounded operational delta.** Source freeze/public verification, dispatch authorization, and postrun evidence remain separate gates. This is not a new audit of unchanged scientific arithmetic or the independent checker's complete implementation.

Paths are relative to `research/m31-oracle-omission-renewal-2026-10-17/`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `source/analyze.py` | 10400 | `50cd4111f107fcd99bf9cadcf098a4f2b298eec319ce0930cb0473150b2921e9` |
| `source/check.py` | 29219 | `20a938686dd602a0818e23011f47a4cd96c68054a8e5f66a380de0754b28c86c` |
| `source/run.py` | 5678 | `29375475368458409139b36d05f7d2e597d1145dce5e37a49f1e6097dcbc9e72` |
| `PROTOCOL.md` | 9410 | `58124b6e24df57448841e9b165e0c709a7b97e20c22569855a7f16bfbbe9acd5` |

Static file comparison confirms that the analyzer is byte-identical to its failed predecessor. The checker diff is exactly one `PACKAGE` constant replacement; its algorithms, fixtures, and controls are unchanged. The checker still reads the renewal's `results/analyze.json`, while frozen reference inputs remain in the completed replication package. The runner was read in full, its delta inspected, and the renewal protocol read in full. No target values were read and no project import, execution, AST evaluation, test, setter trial, or numerical recomputation occurred in this review.

## Diagnostic basis and correction

The saved predecessor diagnostic `review/RESOURCE-SETTER-DIAGNOSTIC.json` is 1,308 bytes, SHA-256 `8a08a7fa38c0f8b0e7fccb77ec03d32a1e8ec6436baf67c2a570c05c5de5d6a1`. It records three separate harmless setter calls: CPU `(60,61)` succeeds, DATA `(536870912,536870912)` raises `ValueError: current limit exceeds maximum limit`, and FSIZE `(16777216,16777216)` succeeds. This reviewer read that saved diagnostic and did not reproduce it.

The renewal removes only the unsupported DATA setter. It preserves the alarm, CPU soft/hard limits, file-size limit, exclusive attempt/result creation, pin/runtime verification, output hash binding, atomic final attempt replacement, failure handling, and launch cutoff. The protocol identifies the prior allocation as closed and the predecessor source/failure as preserved; this review does not recast that failed setup as a successful scientific attempt.

## Memory semantics are now observational

The new condition is `ru_maxrss > 536870912` causing `observed-peak-rss-acceptance-gate` before exit code 0 is assigned. Equality is accepted. The check occurs after output serialization, write, fsync, digest readback, and output-size recording, so those operations are included in the OS high-water observation. On the specified macOS host, `ru_maxrss` is measured in bytes. This interpretation is platform-specific and is not a portability claim.

An over-threshold otherwise successful analyzer or checker is changed to failed by the existing exception path and cannot produce an accepted successful attempt. A checker already reporting failure remains failed without needing the memory gate to override its primary failure. The final report's `peakRssBytes` is a later observation in `finally`; the acceptance comparison itself is the earlier post-output sample. Final attempt metadata/serialization overhead is excluded from acceptance, as disclosed. The later reported high-water value must not be confused with a second enforced threshold.

This is a real change in operational protection: there is **no enforced memory ceiling**. A high peak can occur before retrospective rejection, and a process that cannot finish may leave incomplete evidence. The protocol and `resourceScope` explicitly state that limitation. It is consequently appropriate to call the 512 MiB value an acceptance gate, not a replacement hard cap or proof that memory never exceeded it. The six-state oracle rules, exact budgets, denominators, hurdles, fixtures and selection algorithms have not changed.

The existing 90-second signal-guard limitations also remain: no strict whole-process deadline or power-loss-proof completion is claimed, and final reporting is not guaranteed after interruption. No new environment trial or full scientific source re-audit is needed to support this narrow delta disposition. Actual stage completion and observed resource acceptance still require their own saved evidence.
