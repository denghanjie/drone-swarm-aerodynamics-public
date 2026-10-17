# Browser scaling probe: evidence-storage boundary

The saved-record harness passed, but the browser probe stopped at its fixed evidence-storage limit during the first 5,000-drone case. **This experiment did not establish a speed improvement or complete the numerical qualification.** The failure and partial output are preserved; there was no retry.

We asked whether excluding whole distant groups could reduce the cost of the complete audited aerodynamic query while retaining the original calculations. The fixed plan used four new initial scenes, one 0.0025-second flight step each, and three methods: original F, tree H, and tree-with-omissions-disabled H0. The public source checkpoint preceded execution.

## What actually happened

| Stage | Recorded outcome |
| --- | --- |
| Saved-record harness | Passed all 42 prior cases / 126 complete payload roundtrips, original arithmetic/corruption controls and new compact/decoder controls in 7.29 seconds. |
| Browser | Retained 66 complete journal entries, including 30 native records and ten stage records. Stopped with `store-evidence-cap`. |
| 64 and 1,000 drones | Each has four saved stage records and one saved endpoint. These fresh results did not receive the planned independent reference/full checker. |
| First 5,000-drone case | Two complete stage records and their six native records were saved. No accepted endpoint was recorded. |
| Second 5,000-drone case | No initialization record exists. |
| Exact reference and full checker | Neither stage launched. No cost-gate or accuracy pass is available. |

“30 native records” counts durable complete records; it is not a claim that only 30 queries executed. A later query can run before its record fails to persist. The partial shards are retained rather than treated as completed evidence.

The evidence partition contained **167,411,867 bytes** against its fixed **167,772,160-byte (160 MiB)** cap, leaving 360,293 bytes. That partition is stricter than the 256 MiB combined allowance for evidence, logs, scratch and closure. The next shard could not fit. Twenty-three shards, totaling 20,228,208 bytes, lack a complete record descriptor after the interrupted write. They remain part of the failure record.

The complete supervisor attempt lasted about 62 seconds before its final report. Its external tool exit was observed as code 1. The supervisor recorded preserved source/prerequisite artifacts and reaped its failed owned child. Chrome's recorded root exit and close were both code 0. These observations do not assert that every possible helper process was independently enumerated.

## What you can see

The [Three.js inspector](viewer/index.html) shows the actual first-query positions for all three reached cases, including 5,000 drones, plus the two available smaller-case endpoints. Receiver selection shows recorded retained candidates and omitted groups. The 5,000-drone view is an initial state, not an evolved flock. No trajectory is invented or interpolated. The page states that the full independent check did not run.

## What this means for the research

The new lossless evidence representation passed its fixed small saved-data qualification. Its present storage budget is insufficient for the complete prescribed browser experiment. This establishes an operational limitation of this audit path; it does not establish that the tree is fast, slow, accurate at 5,000 drones, or physically valid.

The next useful step is to diagnose and qualify a more economical evidence layout on these already saved bytes before proposing another fresh scientific run. Keep the original arithmetic, complete evidence, negative records and fixed-cap discipline. See the independent reviews and [next experiment proposal](review/NEXT-EXPERIMENT.md). The overall research goal remains incomplete.

No new novelty or physical-validation claim follows. Established spatial filtering and conservative arithmetic remain the methods cited in [LITERATURE.md](LITERATURE.md).

Source commit: `4e1818c5b1ac7032018925edf17cecb1a6965e3d`. Source manifest: `52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449`. Exact-public source verification preceded the attempt. Result publication and UI verification are recorded separately.
