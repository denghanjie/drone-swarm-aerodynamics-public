# R6: fixed-record selector contract accepted

The sole released R6 attempt completed all 100 planned cases: 23 nominal accepts, 73 expected rejections and four positive controls. There were no unexpected failures, skipped cases or retries. Both the child and supervising wrapper exited successfully. Independent review reconciled every case's order, declared mutation, expected decision and actual decision with the frozen plan.

## What the records establish

- All 23 nominal event descriptors match the predeclared literal expectations. Exact rational clock arithmetic, raw-row cadence, schedule-specific anchor positions and byte offsets agree.
- Historical tick 6,400 at a 1/6,400-second quantum is one second: canonical tick 51,200, raw row 6,400 and anchor entry 6,400. The deliberately wrong row-800 interpretation was rejected.
- Current-clock tick 51,200 already represents one second. Multiplying it by eight was rejected. Clock metadata remains mandatory at tick zero: missing/wrong-clock controls also rejected for all 11 initial selectors.
- The partial P1 endpoint remains tick 50,768, or exactly 3,173/3,200 seconds, at anchor entry 25,384. Its requested one-second horizon does not replace the actual endpoint. An exact sparse raw row is unavailable. The two P1 selectors each retain three matching, correlated JSON representations; these are weaker witnesses than an independent raw row.
- All 21 other nominal selectors record exact 2,176-byte equality with their declared raw-row witness. Saved 32-byte signatures were selected and read; none were recomputed.
- Equivalent rational clocks preserve the nominal results. The reverse-order and requested-duration controls use precomputed descriptors, so they do not establish a fresh selector execution in another order.

## Terminal integrity and coordination

The final durable checkpoint records case 100 and all 100 completed receipts. After the child was reaped, the current checkpoint was a regular, single-link 7,754-byte file within its limit; the temporary checkpoint name was absent. All 69 input identities matched the child's complete before/after verification record. Small release-pinned preparation and predecessor reference files were independently checked during this review. The large scientific input set was not rehashed again by the reviewer.

This execution completed using the bounded two-name checkpoint reservation. Ordinary files can still grow during a live census, so live totals are not atomic whole-tree snapshots. Prospective output allocation, serial pre-write guards and strict terminal checks remain part of the accepted composition. One successful execution does not prove every possible filesystem interleaving safe.

The recorded pre-terminal-receipt measurements were about 0.957 seconds wall time, 1.462 seconds total process CPU, 127,610,880 bytes conservative summed process-highwater RSS and 183,365,113 bytes conservatively accounted source reads, within the released limits. The observed wrapper exit confirms its post-write checks passed; the final success-path measurement values were not separately saved. These are accounting observations, not a speed comparison.

## Scope and gaps

Acceptance is limited to the selector/timebase contract on these fixed retained records. It establishes no full C1 equivalence, audit correctness, dynamic integration correctness, physical validation, performance improvement or scale feasibility. Correlated P1 JSON witnesses do not independently prove signature/state association. The records report zero audit/model calls, fixture-runner imports, integration steps, benchmarks and remote writes; this is supported by the reviewed pinned implementation, not an independent syscall trace.

Original records were not rewritten for this review. Predecessor checks cover selected pinned references rather than a new whole-history hash census. This aggregate summary omits detailed scientific inventories, private runtime/census information and binary payloads. Any public subset therefore provides incomplete reproduction materials.
