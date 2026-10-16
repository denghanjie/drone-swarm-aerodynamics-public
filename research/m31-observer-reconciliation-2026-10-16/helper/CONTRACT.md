# Retained-snapshot reconciliation proposal

Static helper only, prepared 2026-10-16. No operational integration, live process
inspection, browser launch, GPU work, or retry of the terminal failed trial.

## Purpose and evidence boundary

The frozen observer reads a registry, takes a process snapshot, recursively finds
descendants, and throws when a reachable row belongs to an unadmitted group. Its
known-group closure predicate does not retain that offending observation. The
independent failure audit therefore leaves closure of every offending descendant
unresolved; it does not establish that a survivor existed.

`reconcile.py` adds a pure classification and retention rule suitable for separate
review. It does not modify or import that observer. It cannot diagnose whether the
failed trial involved registration timing or a genuinely unadmitted group.

## Caller contract

1. Perform the initial bounded registry read, retain one process snapshot, and
   perform one bounded registry refresh. All I/O, bounds, registry validation,
   exact ownership validation, and failure handling remain outside this helper.
2. Construct an immutable `Snapshot` containing the retained rows' PID, PPID, and
   PGID. Its nonempty label identifies the private snapshot evidence. Use a fresh
   label for each captured snapshot. Labels are not process birth tokens.
3. Supply `ValidatedCoverage` before and after refresh, both bound to the same
   retained snapshot. Each group is a caller assertion that exact ownership
   evidence covers its rows in that snapshot. A bare registry ID, ancestry, PID,
   PGID, executable name, or command resemblance alone is insufficient. The helper
   does not establish or verify ownership. It rejects different snapshot values.
4. Use `after=None` if the refresh provides no usable validated coverage. The
   helper preserves prior exact coverage. If a partial refresh yields some valid
   admissions, the caller may supply them, but registry completeness remains an
   independent closure condition outside the helper.
5. Initialize the ledger to `()` once per invocation. Every subsequent call must
   supply the previous result's **entire** ledger; the argument has no default.
   Persist the result privately before treating the sample as complete. On any
   parse, validation, allocation, persistence, or helper exception, the caller must
   leave whole-observed closure unresolved/false. A pure helper cannot enforce
   correct ledger threading or durable storage by its caller.
6. Keep known-group closure separately. `closure_permitted(known_group_closure)`
   adds only the necessary empty-ledger gate. `True` is conditional permission
   under the caller's existing complete closure predicate, not a proof that every
   process was sampled or that ancestry proves ownership.

## Classification and permanent taint

The union of before/after validated groups seeds reachability in the same retained
snapshot. Recursion follows PPID only to identify observations to retain, never to
admit ownership. Rows outside before coverage are classified as either
`covered_after_refresh` or `still_unadmitted`. These are snapshot classifications,
not claims about the cause or timing of registration.

Every still-unadmitted row appends its original snapshot label and immutable
PID/PPID/PGID row to the ledger. The helper never filters, truncates, clears, or
relabels earlier records. Even a later snapshot containing the same numeric IDs,
later exact admission, apparent disappearance, or a terminal state cannot clear a
record. There is no discharge/recovery API. Repeated calls on the same snapshot
may retain duplicate records; this cannot remove the closure veto.

The result contains observations and coverage classifications only. It does not
produce signal targets, grant signal authority, or change the existing exact
ownership requirement for signaling. Any eventual caller must perform its own
fresh, independently authorized signaling checks; this helper supplies none.

## Limitations

- Current `ps` fields lack a process birth/start token. This helper deliberately
  provides no cross-snapshot process-instance identity or PID-reuse inference.
- A process may be born and exit between snapshots, or ancestry may change. An
  empty ledger cannot prove completeness beyond observed reachable rows.
- Each ledger entry permanently prevents whole-observed closure for the invocation,
  even if the process actually exited later. This conservative unresolved state is
  intentional; known-group closure may still be reported separately.
- There is no ledger cap. The pure caller owns invocation/resource bounds and must
  stop fail-closed on exhaustion; dropping observations to fit a cap is forbidden.
  Reachability uses a small fixed-point scan, not an optimized process graph.
- Frozen dataclasses and tuple/frozenset validation prevent ordinary mutation;
  they are not a security boundary against a malicious Python caller.
- Synthetic tests and AST inspection do not establish operating-system behavior,
  identity guarantees, process cleanup, or successful operational integration.

## Frozen reference (read only)

Repository-relative trial: `research/m31-gpu-readback-trial-2026-10-16/`

- Source commit: `e0ee811bd1f3cf22ea40c6a56a0d974dabbfc7b2`
- Freeze SHA-256: `8557a275d8387bfe5e1aa0ceddbad784b392f558e1c4c7d16721b3cbe06a66fa`
- Observer SHA-256: `aacb3daa611f7f3893b27ebf0b6bed0ff2a434d7042d1d10f429e833cf31069e`
- Audit: `publication/independent-failure-audit.json`

No frozen source or evidence was edited. This proposal does not repair, resume,
retry, reclassify, or authorize another run of that terminal trial.
