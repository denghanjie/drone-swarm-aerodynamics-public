# Static disposition of the sole runtime saved-review failure

The sole saved review of `research/m31-body-runtime-replication-2026-10-16` is terminal **FAILED**. Its saved checker reports 846 checks, `completed:false`, `integrityVerified:false`, `terminalFailureVerified:false`, `decisionVerified:false`, and `qualified:false`. Its error is `saved-three-pipeline-admission`. This later static diagnosis does not replace that executed result, complete the remaining review, or authorize a retry.

All paths below are relative to this campaign directory. The scientific source commit is `f12d8c836e7b991ec33e6de662d00ed05dcce33e`; the scientific freeze is `c0c6b2fda84567a76025b2e5f06832cbc1dd5811c23a246df5623f46baf8f8a9`; the review freeze is `c8f16d4c2b7ba0b3c2185c948c0ffbbd7208c0edd860915a6490d4ee7fcce42f`.

## Narrow static diagnosis

The first condition at `review/source/check-records.py:203` is whole-object equality:

```python
capability == worker['capability']
```

The frozen producer at `source/experiment.cjs:92` deliberately saves different envelopes:

```javascript
write('capability.json',{browserVersion:out.browserVersion,...capability});out.capability=capability;
```

A direct structural comparison of the two saved JSON objects found:

- `raw/capability.json` has exactly one additional key: `browserVersion`.
- `results/result.json`'s nested `capability` has no additional keys.
- Every shared field is exactly equal.
- The raw `browserVersion` is `155.0.8059.80`, matching the sibling `browserVersion` in `results/result.json`.

The whole-object comparison is therefore false by the producer's saved schema. Python short-circuits the predicate before its later admission clauses. The error code does not establish failed pipeline admission; it identifies a checker assumption that confuses a version-bearing raw envelope with an unwrapped nested capability object. The saved capability itself records `supported:true`, `compiled:true`, `stage:"ready"`, and three pipeline creations, consistent with the earlier static science disposition.

The prior independent static clearance missed this envelope mismatch. That clearance remains preserved as historical evidence; this memo records the missed assumption explicitly. No frozen checker, producer, evidence, lock, or prior challenge was edited. Only source text and saved JSON were inspected. No checker, sealer, numerical implementation, browser, shader, reference solver, transport probe, or binary decoder was executed for this diagnosis.

## Executed result and its limits

The count of 846 includes the rejected `require` call. The checker did not reach subsequent GPU failure, lifecycle, phase-accounting, or final mutation checks. Their outcomes cannot be inferred from this static diagnosis, and this memo is not a substitute integrity review.

The saved observer records one checker invocation, actual checker exit 1, complete pipe capture, and confirmed reap. The saved caller records one observer invocation, actual observer exit 1, complete pipe capture, confirmed reap, and an observer interval of `0.073793666` seconds. `publication/review-capture-execution.json` preserves actual capture exit 1 and a completed tool session. Thus capture, observer, and checker all exited 1.

Output accounting is complete: the observer accounts for 3,585 bytes; the final capture accounts for 6,502 bytes. The outer `Checker summary binding` and `Actual full review integrity conjunction` errors propagate the unsuccessful checker result. These closure, timing, summary-binding, and accounting facts do not upgrade the failed integrity result. Later publication receipts are provenance, not additional charged review output.

The scientific attempt separately remains terminal and unqualified: its first GPU control dispatch was submitted, the browser reported `TypeError: Failed to fetch`, and the required 3,840-byte output was not persisted. No main-family or GPU-accuracy conclusion is available. The transport cause remains unknown. This static checker diagnosis neither explains nor reverses the scientific runtime failure.

No additional review or scientific run, source repair, new budget, or third runtime campaign follows from this disposition. The original cutoff remains `2026-10-15T23:00:00Z` (07:00 Shanghai on 2026-10-16).

## Terminal record identities

| Campaign-relative record | Bytes | SHA-256 |
| --- | ---: | --- |
| `review/results/review.json` | 660 | `ba8c3833027d60373d0b4e7ff9721dac71ba09ec493a6d0e864894b1b600647e` |
| `review/results/budget.json` | 2,051 | `18775331f28a3313b58f979236cb96829d915b38e0804c35cf2299f27e25e94e` |
| `review/results/capture.json` | 2,113 | `0e7f4d1d115dc6fcc0a6ae68309dee7be4f0e06572d3d871dfbc7b11c5740075` |
| `publication/review-capture-output.json` | 748 | `d13c7b6f9a1775d1e0e651505d0bc9388733ca6d0dabe87e5f226026e98e8928` |
| `publication/review-capture-execution.json` | 1,994 | `4a0fb558acd26bbf53a2636d11b04fc2a644e89663aa4edd57cc963a8ce2c137` |

These identities were computed by reading bytes only. They identify the inspected terminal records and do not claim that the failed saved review verified their full integrity conjunction.
