# Saved renewal result: contract audit

## Finding

The reviewed saved evidence supports a pass for the eight frozen harmless launch-mechanism cases. No contradiction with the accepted error-retention, readiness, authorization, cleanup or bounded-output contract was found within this audit's 16-file scope. This is current evidence suitable for the next integration-design discussion. It does not qualify the old scientific supervisor or authorize a scientific rerun.

The saved checker reports `passed: true`, eight passed case slots, an empty error list and 0.0626564584672451 seconds. The run index records no fatal failure and 1.425086040981114 seconds. The parent separately reports both command exits as 0 and both launches through explicitly `require_escalated` tool calls. Those external dispatch records are not independently inspected in this file audit.

## Scope and pinned reading inventory

Exactly 16 distinct input files were read and hashed: checker report, run index, run attempt, source-publication receipt, all eight case reports, and four raw event files for sampler-nonzero, sampler-malformed, delayed-ready and child-timeout. No source import, harness/checker execution, live process query, reproduction or scientific work occurred in this review.

The complete inventory, exact bytes/SHA256 values, cross-pin comparisons and derived timing facts are saved in `RESULT-CONTRACT-READING.json`: 11,349 bytes, SHA256 `8285baaf00a813bbc4cb7bb957c0ac0fca989d7fdacc1db7e5a74393c9bcabf8`.

All 14 selected inputs that have saved checker pins match those pins. All 13 selected inputs that have run-index pins also match. The four selected raw event arrays exactly match their corresponding report copies. The remaining event copies were read in the case reports; their equality to raw files is supported by the saved checker, rather than by additional raw-file reads in this capped audit. No files beyond the 16 selected inputs were independently rehashed here.

| Core input | Bytes | SHA256 |
| --- | ---: | --- |
| `results/check.json` | 11843 | `5bd8bc32def811fe21ee08a89b14bdcc4b7bd6a38b59e6b5b9d3e07215997bfd` |
| `results/index.json` | 10796 | `aff4dd14a076be33242f04932ca878399b51570256ac9b0d41e891aed5c07e55` |
| `results/attempt.json` | 689 | `4b2c42d714c8ae7eb4253df1e6225efd2f7df199569c01565b0a644fba50fde7` |
| `source-publication.json` | 885 | `40a177dbcf97c54ddc1788007134f11e475de12aead5571557f2374bcd59bb2d` |

## Source, attempt and environment binding

Every reviewed case report, the index, attempt and checker agree on source commit `fbc38529363acb32fb9f11643a421606435d304a`, manifest SHA256 `c4224571bbac5ef10e61cedef7bb8e834ebb7068766477e63cbabae2e302bd69`, config SHA256 `d5ab7cd5f24885babcfc89a0d9f430162e2fd47a94b8f8340ebb67dc51c36d3e`, supervisor PID/PGID 36406 and execution context `tool-require-escalated`. The saved runtime binding is 18,058,560 bytes with SHA256 `7a314947596fc484d4ec36ffc28e843b78d6d749c68736f8b5c24e7333f418eb`.

The publication receipt identifies the same exact source commit and manifest, reports 16 verified source pins, and records verification at `2026-10-16T23:18:56.529814+00:00`. The sole-attempt marker records start at `2026-10-16T23:19:03.998034+00:00`, after that receipt and before the renewed `2026-10-17T01:00:00Z` cutoff. No older allocation is substituted for this attempt. This audit read the receipt and saved bindings; it did not reopen the source manifest or reverify its 16 source files.

The environment string remains a caller attestation, not a sandbox detector. The external escalation evidence is retained separately by the parent. Accordingly, the real process-inspection capability observed here applies to this reported escalated launch and pinned runtime; it does not establish process inspection in the earlier default sandbox.

## Expected negative failures remain primary

All five negative cases retain exactly the expected primary cause and the separate secondary record `missing-inert-output`. No cleanup, closure, event-parse or other unexpected secondary failure appears. Missing output has not replaced the originating error.

| Case | Saved primary | Secondary | Guardian exit / release | Wall seconds |
| --- | --- | --- | --- | ---: |
| capability | null | none | No guardian; administrative closure | 0.013263 |
| normal | null | none | 0 / normal | 0.157274 |
| child-exit7 | `child-exit`, child exit 7 | missing output | 0 / normal | 0.167243 |
| sampler-nonzero | `sampler-nonzero`, return 13 | missing output | -9 / forced | 0.094449 |
| sampler-malformed | `sampler-malformed`, return 0, ValueError | missing output | -9 / forced | 0.105997 |
| delayed-ready | null | none | 0 / normal | 0.378705 |
| child-timeout | `child-timeout`, deadline 0.3 seconds | missing output | -9 / forced | 0.415577 |
| early-guardian-exit | `guardian-exit-before-release`, exit 5 | missing output | 5 / no release | 0.084793 |

Both sampler failures preserve `operation: process-sample` and `injected: true`. The nonzero case retains the exact stderr `INJECTED process inspection failure`. The malformed case retains `INJECTED MALFORMED ROW`, `ValueError` and `malformed-numeric-row`. Their real leader observations precede the injected failure boundary; both have null authorization and no child-start event. The raw event files show only guardian-start, ready and the expected signalled-cleanup event. These are deliberate synthetic outcomes, not observations of the old sandbox failure.

The child-exit7 case retains the same child's exit 7 event while still completing normal release. The early-guardian-exit case records only guardian-start and early-exit, null authorization, no ready or child event, and guardian exit 5. The timeout case retains its timeout first failure while separately recording cleanup of child PID 36446 with exit -15 and guardian PID 36443 with exit -9.

## Authorization order and closure

Exactly four cases record a child start: normal, child-exit7, delayed-ready and child-timeout. In each report, guardian readiness precedes the saved owned-leader observation, which precedes authorization, which precedes the recorded child-start event. Each leader observation identifies the guardian as its process-group leader and supervisor 36406 as its parent. No reviewed child-start event occurs before authorization.

| Launched case | Authorization to recorded child start |
| --- | ---: |
| normal | 1.412667 ms |
| child-exit7 | 1.599125 ms |
| delayed-ready | 1.455875 ms |
| child-timeout | 1.592208 ms |

The delayed-ready raw log records 210.428625 ms from guardian-start to ready, exceeding the fixed 200 ms delay. Authorization follows ready by 25.245917 ms. The timeout first-failure timestamp is 308.210375 ms after authorization, exceeding the fixed 300 ms threshold, and precedes guardian-failure and the same-child cleanup exit event. These are event-time differences, not estimates from total case duration.

All seven guarded cases record a guardian wait status and two `absent: true` group probes. Both probes follow the final recorded guardian event; their timestamps are ordered. The three normal-release cases also retain the matching child exit, a release observation containing only the retained leader, a released event and guardian exit 0. The five negative cases retain their required missing-output accounting without suppressing closure facts. The capability slot creates no child group and correctly has no guardian probes.

Saved case intervals are ordered and nonoverlapping. The largest recorded case duration is 0.41557700000703335 seconds, below the five-second including-cleanup bound. The largest guarded sampled group RSS is 37,732,352 bytes in child-timeout. The capability slot records a positive supervisor sample of 40,665,088 bytes; both are below 134,217,728 bytes. These are sampled observations, not unsampled memory-peak guarantees.

The checker's saved complete-tree pin list, plus the independently hashed checker report itself, describes 40 result files totaling 43,010 bytes. The listed report/event/log sizes fit their respective limits, including empty stdout/stderr logs. Full-tree set closure is supported by the saved checker; this audit did not expand the 16-file selection into another complete filesystem scan.

## Permitted conclusion

The exposed harmless suite provides current operational evidence for retained first-error diagnostics, readiness gating, owned-leader observation, authorized child launch, expected negative handling and recorded cleanup in the reported escalated environment. It supports designing a future integration with these mechanisms. Such integration would still need its own reviewed source and allocation; this audit does not apply the result retroactively to any prior supervisor.

The earlier normalizer failure remains a consumed scientific attempt with an unresolved specific OS cause. The synthetic errors here do not resolve it. The saved checker explicitly sets `scientificQualification`, `historicalRootCauseEstablished` and `scientificRerunAuthorized` to false; this audit agrees. No new simulator behavior, aerodynamic accuracy, speedup, physical validity, scale capability or 3D flight trajectory was evaluated. All original scientific allocations remain closed.
