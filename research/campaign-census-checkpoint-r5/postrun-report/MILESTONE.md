# R5 milestone: tested checkpoint accounting coordination

## Result

All 21 prescribed outcomes matched: 10 accepts, 11 expected control errors, zero unexpected outcomes. One attempt, zero retries. Independent semantic and resource reviews supported the final coordinator acceptance, restricted to the fixed interleavings and trusted-writer prerequisites. Nine prescribed hook actions were exercised. The reviewers checked 54 retained fixture files against exact authored contents, totaling 132,809 payload bytes.

## What was tested

The candidate reserves a fixed bound for exactly two registered checkpoint filenames while the trusted writer is active, without statting those transient names. Unrelated files retain strict checks. After the writer stops, the exact checkpoint pair is checked for expected presence, regular single-link type, and size bounds, then actual pair bytes are counted. The injected metadata controls remain labeled in their original receipts. This is a targeted unit protocol, not a general concurrent-filesystem snapshot guarantee.

The legacy race produced its expected FileNotFoundError. Missing unrelated/required files, sibling lookalikes, metadata/type/link faults and oversized writes received their specified error outcomes. Passing means matching each prescribed decision, including these deliberate errors.

## Actual records and resources

Read the [sanitized final acceptance](EVIDENCE.json), [unchanged child result](../results/attempt-001/result.json), [unchanged parent observation](../results/attempt-001/PARENT-OBSERVATION.json), and the 21 original case links in the [display](../postrun-demo/index.html). The original pending acceptance fields predate the later reviewed coordinator decision; they were not rewritten.

Parent exit was 0, with no timeout. Launch-to-child-reap was 0.066656105 s; final child CPU was 0.068349 s; reaped-child maximum RSS was 12,320,768 B. Instrumented payload upper bounds were 330,834 B read and 152,936 B written. These are resource observations from this attempt, not a throughput or speedup benchmark. The recorded 614 ms outer tool roundtrip separately supports the 10 s bound, but is not an internal final-write timestamp. RSS is not a whole-OS aggregate guarantee. Interpreter/library I/O is outside payload counters; parent CPU ends before the last parent write.

Run-end retained storage was 251,584 B before later launch/postrun records. Later preparation and reviews remain counted against the R5 storage allocation; they are not backfilled into the attempt's counters.

## Reproduction and remaining boundary

The finite public selection includes the [census implementation](../implementation/census.py), [literal oracle](../implementation/oracle.json), actual case/result/parent receipts, and separately written postrun summary and literature notes. It excludes driver/configuration/fixtures, private inventories, release/runtime details and raw predecessor checkpoints. Full reproduction is therefore incomplete. The census source's SOURCE-LEDGER.json mention refers to an original preparation ledger that is not in this public selection; the separate postrun literature notes explain its documentary basis.

R5 has not been integrated into the R4 wrapper. R4 remains terminal with eight completed cases. No selector retry, new scientific test, trajectory, physics validation, accuracy result, or speed claim follows from R5.

The Three.js display shows prior records only. P1 has 100 saved display frames through 0.990 s, and holds its last pose afterward; its actual historical accepted stop was 0.9915625 s. A prospective compact standalone would retain all those frames and the unchanged historical rendering code. It requires a separate build release.
