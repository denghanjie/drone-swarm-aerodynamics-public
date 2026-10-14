# R6 milestone: all 100 recorded selector decisions match

**Accepted by the coordinator after independent semantic and resource reviews, for the fixed retained-record selector/timebase contract only.** The single attempt completed 23 nominal cases, 73 intended negative controls, and four positive controls. Every recorded decision matches its prescribed outcome. Child exit and the observed wrapper/tool exit are both 0. No retry was performed.

## What the result covers

This is a fixed retained-record selector/timebase contract. It selects saved evidence and checks prescribed identities; saved signatures are read, never recomputed. The recorded counters are zero for audit calls, model calls, integration steps, fixture imports, benchmarks and remote writes.

The historical 6400 tick at 1/6400 seconds maps to canonical tick 51200 on the 1/51200-second clock, with raw/anchor row 6400. The deliberately wrong row800 case rejects. Historical P1 ends at canonical tick 50768, exactly 3173/3200 seconds, anchor entry 25384. Its exact sparse raw row remains unavailable. Three correlated JSON witnesses are not an independent proof of signature/state association. Reverse-order and requested-duration controls use precomputed descriptors and do not reexecute the selector.

## Resource evidence

Before terminal receipt writing, the wrapper recorded 0.956736061 s wall, 1.462173 s whole-tree CPU, and 127,610,880 B conservative RSS. Complete conservative source-read accounting was 183,365,113 B. The separate exit-0 tool observation reported 0.974720483 s and a 1591 ms outer roundtrip including completion. These are bounded attempt observations, not performance or speedup evidence. The pinned wrapper performs additional checks after its terminal write; exit 0 supports their success, but exact post-write wall/CPU/RSS/read values were not retained. Memory relied on sampled tree RSS with margin and process high-water checks, not a cgroup guarantee.

The live checkpoint pair reserved 131,072 B. After the child was reaped, strict checking counted 7,754 actual pair bytes. This exact-pair rule follows the earlier [R5 documentation-to-result ledger](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/ba7c0340aa7fe3c6d4bd9b70265e0e7e5e3c7685/research/campaign-census-checkpoint-r5/postrun-literature/literature-experiment-ledger.json); its sources are API documentation, not research evidence or a proof of arbitrary concurrency. Live ordinary-file traversal is still not a general atomic snapshot. Overlapping study/campaign totals must not be added. Full source hashes were attested by the pinned child before/after, with unchanged metadata and no changed source paths. Independent review reconciled that attestation and current metadata without rereading every scientific payload; the detailed preservation inventory stays private.

## Inspect the selected public evidence

- [Sanitized aggregate and original-record hash commitments](EVIDENCE.json)
- [All 100 case decisions and original-receipt hashes](CASE-DECISIONS.json)
- [Unchanged selected candidate source](../implementation/selector-contract.cjs)
- [Actual-record-linked historical Three.js display](../postrun-demo/index.html)

The case index contains decision-only derivatives. Original receipts remain private; their hashes identify them but cannot make the withheld contents publicly re-verifiable. Full reproduction is incomplete without harness/configuration, retained records and private execution evidence. No full inventories, releases, raw checkpoints or runtime census contents are part of this selection.

Finite before/after checking is methodological inspiration, not formal translation validation. Verification, operational validation and detailed failure documentation remain distinct, as explained in the already verified [R3 methodology ledger](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/5293fba9093179096963784aa8fe765238259eb4/research/campaign-audit-successor-r3/postrun-literature/narrow/literature-experiment-ledger.json). No new literature review or physical-validation experiment is claimed.

Earlier R3 and R4 outcomes are unchanged. R6 establishes no full C1 equivalence, audit correctness, dynamic integration correctness, numerical accuracy, physics validity, speedup or scale feasibility. The replay is historical only. P1 displays through 0.990 s and then holds, with an actual historical stop at 0.9915625 s; no R6 flight was generated.
