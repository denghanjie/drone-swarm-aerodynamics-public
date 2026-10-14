# R7 milestone: admission stopped before scientific work

R7 is terminal. The outer launch observer rejected the actual combined pipe capacity of **131,072 bytes** against its frozen **16,384-byte** admission ceiling. The rejection happened before the supervisor process was created. The root recorded exit 1. The exclusive outer attempt marker remains; there is no retry or resumption.

| Planned work | Completed |
|---|---:|
| Metadata adapter controls | 0 / 32 |
| Scientific B/C1 correctness cases | 0 / 229 |
| Serial correctness jobs | 0 / 18 |
| Independent correctness gate | 0 / 1 |
| Benchmarks | 0; permission remains false |

No audit/model calls, new physics run or scientific comparison occurred. The three inner result directories are absent. The exact observer source orders its capacity check before Popen; its retained observation states launched=false, directWait4=null and reapedProcessCount=0. This is an infrastructure admission failure, not evidence for or against C1 equivalence or speedup. The complete evidence and immutable record hashes are in [EVIDENCE.json](EVIDENCE.json).

## What the resource numbers mean

Recorded outer-process values before its observation write were 0.032898 CPU seconds, 12,582,912 bytes maximum RSS, and 0.042201549 seconds elapsed. The elapsed value does not include the final observation write and is not a supervisor launch-to-exit duration. Both retained child-output logs are empty. End-to-end supervisor duration and child wait4 measurements are unavailable because no supervisor was launched.

Several raw receipt fields are deliberately rejecting fallback values, not measurements: 420.01s correctness wall, 210.032898s correctness CPU, 210s finalization wall and 1,086,324,737B serial-tree RSS upper value. They combine missing-inner-record sentinels with the outer measurements. They must not be plotted or described as actual time/memory overruns. Zero child CPU/RSS aggregate fields likewise describe an empty reaped-child set. The root's tiny tool-reported chunk time is explicitly not end-to-end timing.

## Preservation and scientific status

Root's separate postrun verification checked all 230 frozen files and the complete 1,252-file, 173,884,973-byte external immutable census: names, sizes and hashes matched, with no frozen mismatches. This is postrun root verification, not a successful runtime supervisor finalization. Raw freeze/census inventories remain private; this report publishes only the finding and evidence identities.

The prepared bridge, 32 literal controls, unchanged B/C1 arithmetic, exact comparison semantics and 229-case coverage remain untested together. Historical run JSON and bracket clocks, original location/alias semantics, 16 floating display-time differences and the exact P1 witness rule received static review, but R7 supplied no runtime integration evidence. Untouched B remains an implementation comparator, not physical truth. R3/R4 failures and R5/R6 finite prerequisite results remain separate.

The useful finding is narrow: the observer's capacity assumption was not admissible in this environment. Its guard stopped before scientific entry. Static source review did not establish runtime capacity. No ceiling was silently enlarged, pipe resized, retry performed or failure erased.

## Next boundary

Preserve this terminal attempt and its failure. This report does not authorize a successor implementation, new experiment or benchmark. A future proposal must explicitly address the observed admission incompatibility before a separate review/release. Any historical 3D demonstration is a separate presentation of existing data and must not be labeled an R7 simulation result.

Methodological limits follow the verified [literature–experiment ledger](../LITERATURE-EXPERIMENT-LEDGER.md): detailed plus summary evidence, implementation verification distinct from physical validation, and no formal-proof claim from finite result checking. Planned tests are not reported as completed tests.
