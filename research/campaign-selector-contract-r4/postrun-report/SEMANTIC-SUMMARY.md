# R4 terminal outcome: incomplete

The one permitted attempt stopped after **8 completed nominal accept receipts** out of 100 planned cases. The wrapper returned a nonzero exit and killed the child after a missing temporary-checkpoint-file error. No retry was performed.

## Actual coverage

- 8 of 23 nominal cases have durable accept receipts. Each records an expected/actual descriptor match, exact retained-state witness equality and selection of an existing saved signature.
- The ninth nominal case has a durable checkpoint just before its case receipt. That checkpoint records the same checks, but no ninth completed receipt exists. It remains **interrupted**, not a ninth pass.
- 14 later nominal cases, all 73 negative controls and all 4 positive controls were unreached: 91 unreached cases, plus the interrupted ninth.

The checkpoint describes the last durable stage, not the exact interrupted process state. It contains no recorded semantic rejection. No child terminal result or completed final input-hash-preservation receipt exists.

## Cause and accounting limits

Source inspection strongly supports a race between live storage enumeration and the child's atomic checkpoint rename. The terminal receipt reports a missing temporary file, but contains no traceback identifying the exact enumeration call. This is an infrastructure interruption, not a completed test of the selector hypothesis.

Reported measurements before writing the terminal receipt were 0.357154 seconds wall time and 0.510175 CPU seconds. The conservative summed process RSS high-water was 84,267,008 bytes. These are interrupted-attempt measurements, not performance results.

The last observed/accounted read amount was 98,669,013 bytes. The final read interval is unknown and no complete read upper bound was recorded. Input metadata was unchanged and the prepared implementation/release records were hash-checked, but final historical-input content hashes were not confirmed. All-resource-compliance and full source-preservation claims would be unsupported.

## Interpretation and public scope

R4 did not satisfy its 100-case acceptance gate. Static pre-run approvals remain historical preparation evidence; they did not guarantee the live checkpoint/census interaction. R3's terminal failure is unchanged. No numerical/audit equivalence, physical validity, speedup or scalability claim follows.

This aggregate derivative omits raw state payloads, detailed file inventories, source hashes, runtime paths, workspace paths and private census information. Public reproduction remains incomplete, and broader inventory publication approval remains pending. No model or audit was run in this post-run review.
