# M31 replication integration contract review

Date: 2026-10-17

Disposition: **STATIC SOURCE GATE ACCEPTED for the exact pins below. No remaining material integration blocker identified.** This disposition covers the reviewed lifecycle, failure reporting, output closure, and checker consumption contracts. Source publication and verification, and authorization of any later scientific allocation, remain separate gates.

## Scope and exact inputs

The review covered all of `source/supervise.py` and `source/guardian.py`, the new lifecycle consumer and its integration into `source/check.py`, and the implementing agent's integration note. The checker inspection covered attempt identity, lifecycle evidence, consumed input pins, and final source/runtime rechecks. It did not repeat the separate review of unchanged scientific algorithms or the parent's acceptance of the 20 scientific/allocation pins.

Paths below are relative to `research/m31-normalizer-replication-2026-10-17/`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `source/check.py` | 50039 | `8fa3aa3af9da4714c32235ae15a794bc7ac810a11e0e3e54f7454c5877a33b74` |
| `source/supervise.py` | 45435 | `25e143081816beac1f973133a63007819d7fa21ab9bb10b87f6ddfe944619359` |
| `source/guardian.py` | 5810 | `a4afdbb265d8a375cafb576b6770b04b36ca3342016b3a7b36c21d88bef90885` |
| `review/INTEGRATION-REVIEW.md` | 6836 | `09badea508789b2141dab63c0f3e831171bcba00f477a8135d95ea20442158fc` |

The continued review rechecked these exact file hashes before writing this record. No reviewed source was edited by this reviewer.

## Lifecycle contract

The source establishes the required sequence: guardian startup, ready event, positive owned-leader observation, durable authorization, child start, child exit, leader-only release observation, waited guardian status, and two timestamped group-absence probes.

- The guardian exclusively creates and fsyncs its event file before recording `guardian-start` and `ready`, then waits for the start instruction. The supervisor requires the ready guardian to be its direct child, to have positive sampled RSS and PID equal to PGID, and to be the sole member of that group before authorization.
- The supervisor samples real `/bin/ps` numeric fields using a strict four-token ASCII decimal grammar. Authorization is written and fsynced after the positive observation. It binds stage, source commit, manifest, configuration, cutoff, context, guardian and supervisor identities, and the observed leader and timestamps.
- The guardian validates that authorization and checks the cutoff immediately before the scientific child `Popen`. The final checker binds kernel-attempt supervisor PID and PGID to the supervision report and requires supervisor start time to precede or equal guardian startup.
- Normal release requires recorded child exit and a real observation containing only the retained, positive-RSS guardian leader. The observation is saved. The supervisor requires the guardian wait status and then records two timestamped `killpg(..., 0)` absence probes.
- Nonzero group signals are restricted to the retained guardian while observed alive. The guardian handles owned-group TERM, child wait, and KILL on failure. The explicit no-group-created path has narrower cleanup evidence and cannot produce success.

The checker consumes an exact five-event roster, requires complete newline-terminated raw events and equality with the report copy, checks identities and ordering, validates the authorization hash and copy, and checks the saved release-only-leader observation, guardian completion, two absence probes, and resource conditions.

## First-failure durability and output closure

`firstFailure` and `terminationReason` are assigned once. First and secondary failures are appended and fsynced to a separate bounded 64 KiB failure journal. Persistence failure is explicitly represented and prevents success. A missing output is secondary and cannot replace an earlier primary failure. Terminal fallback recovers the durable first failure when possible; incomplete reporting fails closed.

Success requires a closed kernel stage, zero kernel and guardian exit codes, no terminal-error marker, an empty failure journal, and no first or secondary error. The event, authorization, and failure files are included in metadata accounting and evidence pins. Output handling retains the stage and combined limits: kernel 192 MiB, checker 64 MiB, metadata plus private/public logs 16 MiB, and 272 MiB combined. Per-stage time remains 600 seconds, the guardian bound 610 seconds, and sampled group RSS 1 GiB.

The final lifecycle check additionally requires the reported peak RSS to cover both saved positive-leader and release RSS observations. This closes the inconsistency in which a bounded but understated peak could otherwise coexist with larger saved observations.

## Checker pin consumption and launch binding

The lifecycle inputs enter the checker's common `pins` collection. At completion the checker rehashes every consumed pin, emits `inputPins`, and rechecks source and runtime facts. The lifecycle authorization, raw events, and failure journal are therefore consumed and subject to final consistency checks rather than merely listed by the supervisor.

The reviewed integration retains exact source receipt, manifest, local and Git-committed bytes, HEAD, and runtime checks; exclusive attempt markers prevent repetition, and source/runtime/prior evidence are rechecked after each stage. The supervisor requires isolated Python and the explicit `tool-require-escalated` context label, rejects loader injection, and clears Node/Python preload variables. The context label remains a **caller attestation**; it is not an independent sandbox detector.

The source names the new allocation `m31-normalizer-replication-v1`, fresh seeds `26171021` and `26171022`, and cutoff `2026-10-17T01:00:00Z`. Recording those values here neither extends the cutoff nor authorizes a run.

## Findings resolved in the accepted checker

Three material findings raised during this review are resolved in the pinned final checker:

1. `lifecycle-peak-covers-saved-observations` requires peak RSS to cover saved leader and release RSS, each converted from KiB to bytes.
2. `kernel-attempt-supervisor-binding` requires the kernel supervision PID and PGID to equal the corresponding kernel-attempt values.
3. `lifecycle-supervisor-before-guardian` requires `startedMonotonicNs` to be no later than guardian startup.

No further material blocker remains within the assigned integration scope.

## Evidence limits

This is a static source review. This reviewer did not execute or import the harness, guardian, supervisor, checker, or scientific code; did not run tests, a live process sampler, reproductions, or reruns; and did not create or authorize a scientific attempt. Ordinary text reads, file hashes, and creation of this review record are the only closeout operations.

The earlier harmless launch-qualification renewal supplies finite operational evidence for its own saved cases. It does not dynamically qualify this larger integration, prove the historical root cause, or establish a retroactive scientific pass. Scientific logic acceptance, publication verification, allocation authorization, and any subsequent runtime evidence must be assessed through their own gates.
