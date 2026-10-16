# Saved-record audit: typed sparse assembly

2026-10-16. Source commit `ec066cc0d555393606ceb05e5e6e04e09d567020`; source-manifest SHA-256 `942dab53d86315e401e1d3e8b1b2549b57572aabef4436ebeb68f144ce4513b5`.

**Reject the typed-assembly package under its frozen practical rule and close this line of incremental variants.** The exact saved-record arithmetic agrees with `analysis.json` and the independent review's timing analysis in every field. This audit passed 316/316 checks for schedule, raw/validated retention, paired statistics, phase sums, byte pins, completion and resource accounting. The separate saved numerical reviewer reports 16,239/16,239 checks passed with no errors; its numerical calculations were not rerun by this audit.

## Recomputed result

All durations are milliseconds. Ratios are medians of six block-paired ratios, not ratios of marginal medians.

| Fresh case | A median | L median | T median | Paired T/L | T/L wins | Paired T/A | Paired L/A | Practical rule |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| N1000, seed260103 | 43.752 | 37.244 | 36.424 | 0.9949037983 | 3/6 | 0.8325005587 | 0.8508496733 | Context only |
| N5000, seed260101 | 525.945 | 476.507 | 478.962 | 0.9991065789 | 3/6 | 0.8832429482 | 0.8903483901 | Fail |
| N5000, seed260102 | 501.069 | 473.707 | 476.916 | 1.0018898334 | 3/6 | 0.9348402418 | 0.9339665648 | Fail |

Each required N5000 case fails both the T/L median <= 0.90 requirement and the >= 5/6 strict-win requirement. Both satisfy the additional T/A <= 1 requirement, which cannot rescue failure of the primary contrast. T is about 0.089% lower than L in one paired median and about 0.189% higher in the other. These near-one values do not establish statistical equivalence or impossibility of a benefit elsewhere; they plainly fail the declared 10% engineering target here.

L beats A in all six N5000 pairs per case. Its paired medians correspond to approximately 10.97% and 6.60% lower duration. That supports the known shared lean implementation changes as a useful diagnostic on these two states; it does not support an incremental benefit from T's row/chunk/dependency assembly package. Neither L/A nor T/A should be presented as evidence that this storage mechanism is novel or successful.

## Completeness and outliers

The exact frozen schedule is present: 24 controls, 3 completed generations, 9 passing qualification bundles, 9 saved warmups and 54 measured full queries. All 63 raw records match their pinned bytes and the corresponding raw fields in both `evidence.json` and the individual validated records. Every measured call is used once in its case/method/block analysis. All validation flags pass. All recorded phase sums equal their totals exactly. No failed/partial evidence file is present.

The largest observations remain in the paired analysis, including A 1,015.234 ms (`call-014`, first N5000 seed, block0), A 865.984 ms (`call-016`, second N5000 seed, block0), A 770.389 ms (`call-023`, second seed, block1), and T 586.812 ms (`call-013`, first seed, block0). The second seed's first A call includes 66.413 ms in its admission phase. No trimming, deletion, warmup reclassification or replacement was used. The first N5000 A and T outliers share block0 but are separate sequential queries. The records do not identify GC, OS scheduling, JIT or another mechanism as their cause. Their presence limits causal attribution of phase differences, especially L/A's large early-block differences.

The measured N5000 median per-call geometry shares are approximately 94.4%–94.9% across A/L/T. This is the broad instrumented geometry phase, including its assembly work; it does not isolate Math.hypot, object allocation, sorting or copying. T removes the documented ordinary coefficient/Set construction but adds its own writes, storage and copies. At N5000, T reports 240,000 row-scratch bytes and 17 fixed chunks, containing 835,584 allocated payload bytes; the two saved states copy 818,568 and 820,464 bytes at each of the row-to-chunk and chunk-to-final stages. These are logical payload/copy counts. They do not measure L's JavaScript object heap or GC cost and cannot establish that T uses less actual memory.

## Resource and identity accounting

Both supervisors report exit0 and success, with no live-child monitor errors, sampling errors, exit races, termination cause or cleanup failure. Both identify the same frozen source commit and manifest. Every artifact recorded by each supervisor still matches its byte length and SHA-256; artifact byte sums reproduce their respective final directory totals.

| Record | Candidate | Independent reviewer |
| --- | ---: | ---: |
| Supervisor elapsed | 174.297 s / 900 s | 7.973 s / 180 s |
| External sampled peak RSS | 783.078 MiB | 194.766 MiB |
| RSS samples | 833 | 38 |
| Aggregate bytes at final measurement | 80,145,054 | 81,700,638 |
| Aggregate including that supervisor's record | 80,194,970 | 81,751,547 |

Candidate scientific writer bytes are exactly 80,144,931, reproducing `newScientificBytesBeforeEvidence + evidence.json bytes` and the review's scientific count; this is below the 184 MiB normal limit. Final combined log bytes are 156, below 4 MiB. All 301 scientific-directory files total 81,751,547 bytes including the reviewer run record, below 208 MiB. The review's `directoryBytesAtReview` value 80,195,010 is its earlier input snapshot after adding the review lock; it is not intended as the final post-review total.

Candidate internal sampled RSS is 787.844 MiB and Node's reported maxRSS converts to 801.625 MiB, also below 1.5 GiB. These values legitimately differ from external 0.2-second samples. They are whole-campaign measurements, including generation and full-symbol qualification, not per-method peak-memory comparisons. Sampling/cooperative limits and final acceptance checks do not establish hard real-time containment; final supervisor artifact hashing is outside its elapsed measurement.

Generation consumes 141.923 s in the saved generation clocks; qualification computation totals 3.550 s and all 63 query clocks total 23.545 s, of which 19.494 s is measured queries. These disjoint stage clocks explain much of the 174.297 s candidate allocation but are not a substitute for its supervisor clock and omit other work. The 174.297 s total should never be reported as the coefficient-query duration.

The environment is Apple M4, Node v24.19.0 / V8 13.6.233.17-node.51, no execution flags or NODE_OPTIONS, AC power and low-power mode0. One-minute load average rises from about2.14 to5.07. Those endpoint samples do not prove an idle host, isolate interference or explain outliers. Results are specific to this saved run.

## Scope and next evidence priority

The recorded correctness is strong numerical evidence for these three fixed poses: exact A/L/T same-runtime agreement, complete saved qualification tensors/CSR/solutions, and the separate independent numerical review. It remains a hypothetical source-total/ideal-power model. Fresh flights are two-second airflow-off trajectories; the computed coupled loads were never fed into their motion. Two N5000 seeds and six within-process repeats do not establish physical validity, mature-flock generalization, dynamic admissibility, closed-loop stability, or live5000-browser performance. Successful source and saved-result audits do not change those limits.

The frozen stopping rule determines the immediate action: retain this negative result, use L as the measured lean comparator where an exact CPU reference is needed, and do not retune chunk size, storage policy, seeds, repetitions or thresholds. Existing candidate/reviewer allocations remain consumed. No further scientific run is authorized by this recommendation.

**Recommended next evidence priority: establish the coupled model's validity and usefulness when loads actually affect motion, at a feasible, independently specified scale.** Begin with a source/literature-backed design that identifies a defensible external physical comparator or bounded validation observable, feedback integration, moving-pose admission/failure behavior, and fixed acceptance criteria. The key question is whether the coupled model produces stable and physically defensible loads and trajectories under real feedback, rather than whether another representation makes the same frozen-pose query marginally faster. An affordable small-scale result could answer that question; a large visually plausible replay could not. If physical comparison is unavailable, label the outcome as a numerical closed-loop diagnostic and keep the physical claim unresolved. Structural scalability or refresh-cadence work can follow a justified model/workload requirement; this timing result alone does not justify stale matrices, changed precision or another storage sweep.

## Audit artifacts and method

`ARITHMETIC.json` retains all recomputed statistics, the 63-call schedule checks, all input-file pins, per-case six raw durations and sequence IDs, largest calls, assembly metadata, resources, environmental records, and individual audit checks. `audit_saved.py` uses only Python standard-library JSON, arithmetic, file size and SHA-256 operations. It imports no campaign code and performs no geometry, root solve, simulation, query, timing rerun or heavy numerical work. Only isolated audit artifacts were written.
