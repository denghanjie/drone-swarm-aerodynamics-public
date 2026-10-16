# Runtime admission result

Two prospective echo-only invocations were completed; both allowances are now closed. They imported no scientific code and evaluated no drone state.

| Context | Observed path | Result |
|---|---|---|
| Default sandbox | Node launched and exact READY was read. The ps sampling launch raised PermissionError/errno1. Child was killed/reaped with−9. | Not admitted. |
| Ordinarily approved host | Exact READY, successful45,824KiB RSS sample, DONE accepted by the frozen predicate, child and cleanup exit0, no recorded error. | Admitted for this narrow process path. |

Source402158183fc5db02e2b64e2efd1c2fdf66262299; source manifest48df6d2b576c3b41986c1e7a0e0cb5de132a2b5e3bd661abc0a1ec85a3ee32f1 was independently retrieved before execution. Both contexts have identical Node/Python executable hashes. Event arrays match the flushed journals:8sandbox events,10host events. See results/*.json and *.jsonl and ADMISSION-RESULT-REVIEW.md.

These observations justify using approved host execution for a separately preregistered cost allocation. They do not prove the exact site of the previous allocation's unmarked error, that no child briefly ran then, or that a full scientific workload will fit resource/correctness constraints. The elapsed durations are infrastructure bookkeeping, not performance comparisons. Supplied context labels rely on the tool invocation receipts; the script does not independently introspect sandbox policy.

No retry of either diagnostic context. Preserve all locks/source/results. The replacement numerical allocation has separate outputs and budgets and reuses unchanged numerical sources and the same exposed cases; it must not be described as fresh scenario confirmation. The original failure remains public. Source/result data are synthetic process markers and public hashes; no private paths/PIDs/host identifiers or raw environment were saved.
