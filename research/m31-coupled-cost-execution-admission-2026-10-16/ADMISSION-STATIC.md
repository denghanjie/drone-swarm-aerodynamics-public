# Echo-only admission: source review

Source-only review, 2026-10-16. Reviewed `source/admit.py` and `PROTOCOL.md` in `research/m31-coupled-cost-execution-admission-2026-10-16`. No admission invocation, Node payload, scientific module, model calculation, saved-record checker or timing experiment was executed by this review. No public numerical source or result was edited. Both preceding allocations remain closed.

**Disposition:** no remaining blocking source finding for the stated, narrow two-context infrastructure experiment. This is readiness for source freeze and the separately authorized diagnostic, not a runtime admission result or authorization for scientific execution.

Reviewed SHA-256 values:

- `source/admit.py`: `cc008fec83531293a8de56b84eac8bd137a4953c3b1d3aae5483c303233ad972`
- `PROTOCOL.md`: `bad74366b3f35add4ed545b9675251e53cbc74fb6ffb45e7e575d51797528098`

The manifest present during review predates the final edits. As already planned, regenerate it after incorporating this note, publish the checkpoint, and independently verify the exact remote manifest and local/committed source pins before dispatch. This note does not attest to that future verification.

## Findings resolved

- Optimized Python is rejected before the lock, so optimization cannot silently disable the assertion-based source checks. Nonempty `NODE_OPTIONS` is also rejected before the lock, preventing that inherited preload mechanism from expanding the fixed payload.
- Node and Python executable hashes are read before consuming the invocation lock. A hash-read failure therefore does not consume a diagnostic invocation.
- Commit provenance is explicitly coordinator-supplied verification metadata; the script checks the supplied manifest digest and local file pins, rather than claiming an internal Git/remote verification.
- Normal journal events remain fatal on write/flush/fsync failure and identify the failure as `journal-write-for:<event>`. A failed required pre-operation event therefore stops the main path before its next process operation.
- Exception and cleanup paths use `safe_event`: logging failure records `journalErrors`, revokes admission and does not replace the primary recorded exception or prevent the attempted child cleanup/final JSON. Cleanup operation failures also revoke admission. The previous path that could report success despite cleanup failure is removed.
- The protocol accurately describes operation-specific waits and the child watchdog, and explicitly disclaims a hard whole-invocation wall cap over hashing, process creation and filesystem operations.

## Scope and interpretation

The embedded Node source only emits fixed READY/DONE tokens and waits for ACK under a watchdog. READY precedes the single attempted RSS helper; DONE is emitted only after the parent releases the child. The script contains no scientific imports or state paths. The inspected manifest inventory contains only protocol/review/source files. Exclusive per-context locks bound the planned experiment to one invocation in each declared context; coordinating those labels with actual tool/approval receipts remains an external obligation.

Admission requires the exact handshake, positive integer RSS, exact DONE output, zero child status and empty stderr. Caught main, cleanup or handler-journal exceptions leave admission false. Accept an invocation only with its normal successful supervisor completion and complete evidence; a missing or partial result is not admission. Ordinary file-open/write/close failures can still prevent final evidence persistence, so retention is best effort, not an absolute guarantee.

Compare only demonstrated process operations in the actual permission context. This payload does not exercise scientific work, sustained monitoring, future process-group cleanup or a full allocation wall watchdog. Cleanup byte counts may repeat output cached by `communicate`; they are not additional output events. Echo success cannot establish scientific validity, predict a future campaign's completion, or repair the closed campaign's missing results.

The historical PermissionError remains unlocalized: the saved null return code and empty logs do not prove that Node never started or that no transient scientific computation occurred. Neither diagnostic outcome changes that limitation or reopens the previous allocations.
