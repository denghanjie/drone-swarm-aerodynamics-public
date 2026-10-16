# Saved control-repair interpretation

The new qualification report records success for the previously exposed, immutable corpus: all 21 corruption controls reached their registered failure family; all 10 baseline records have empty error lists; all six scheduled states were reached, independently verified, model-admitted and certified. The report sets `passed`, `exposedCorpusQualificationPassed`, `recordIntegrityPassed` and `fixedControlsPassed` to `true`, with `errors: []`. The ten baseline records include four fixed controls, whose intended outcomes differ; this is not a claim that all ten are positive certifications.

This note interprets saved reports and the previously reviewed repair. It performs no new evaluation, numerical import, source investigation or implementation.

## What the three control outcomes establish

| Allocation and control | Observed rejection | Intended family reached? | Interpretation |
| --- | --- | --- | --- |
| Original `false-zero-active-leaf` | `filter-work-counter-reconstruction` | No | The wrapper rejected inconsistent work counters before the intended node-zero semantic check. The original allocation failed its registered control criterion. |
| New `false-zero-active-leaf` | `node-zero-rule` | Yes | With the corruption's work counters made internally consistent, the full wrapper reaches and rejects the false zero claim at the registered semantic layer. |
| New `false-zero-counter-interception` | `filter-work-counter-reconstruction` | Yes | The original malformed-counter path remains a separate regression, with the counter family now explicitly registered as its target. |

The same positive witness is used: scene `positive`, `i=0`, `r=0`, `j=1`, node `0`, with the same positive coefficient interval in the saved reports. The repaired recipe replaces the same mixed leaf, which contains a positive entry and one natural fast-zero member. Removing that member changes the wrapper's reconstructed work from `filterZeros=4` / `exactScalarCalls=4` to `3` / `5`. The original recipe retained `4` / `4`, so the counter check intercepted it. The corrected recipe decrements `filterZeros` by the removed list length and increments `exactScalarCalls` by that length; the saved new witness records `removedFilterZeros=1`.

The corrected semantic recipe and the counter-interception regression use independent pristine copies. The repaired semantic recipe still runs through the full wrapper. Its observed `node-zero-rule` error satisfies one of the registered alternatives (`node-zero-rule`, `node-zero-oracle-member`); the report does not claim that both errors occurred. Together with the 19 previously successful recipes, these two distinct targets account for the 21 successful controls.

## Historical result remains failed

The old `results/check.json` is byte-identical to its published pin below and still records `passed: false` and `advancement: false`. It retains 19/20 intended corruption-control failures and its original counter-interception error. The new report independently preserves `historicalOriginalPassed: false` and `historicalOriginalAdvancement: false`.

This separate qualification closes the exposed-corpus control gap under its own frozen source. It does not rewrite the old result, rerun either flight, establish a fresh replication, or authorize browser transfer. The new report explicitly records `freshReplication: false` and `transferAuthorized: false`. Generalization to unseen states, physical validity, feedback flight and real-time browser scale remain outside this evidence.

## Exact bindings

New qualification source commit: `a5f0b2092965b536bd7f096194303f510f787356`.

Original source commit: `2a957d2b0bb26e731c8cd184bc13f51f673e9a0d`. Original published result commit: `5a5efeef2d216188fa93a8034c4573d7327c5411`; original result-manifest SHA256: `e60a5bf356f9f27bf31f79fc3274c0c37675353f1b8b0de20a1a6fc1b69487d8`.

Paths below are relative to the named package. Hashes were checked as opaque bytes; source bodies were not read for this interpretation.

| Package | File | Bytes | SHA256 |
| --- | --- | ---: | --- |
| New qualification | `results/qualification.json` | 33837 | `d3249e923b6b96daf316b04f693a9e16f9f29b3b1ea02f55e74dbf1f6788ff04` |
| New qualification | `source/qualify.py` | 48885 | `fd3c20618a4f893c6e90c39c23a309b1830530367384fa4392d2562f85f969cd` |
| New qualification | `source/config.json` | 1515 | `70eb6bb3b3faddf5ffa356cce3c2768303477a884ea985a85563ce041b02f9e7` |
| New qualification | `source/result-contract.json` | 9307 | `f343f93fdb3e4fef0399663e20cc02998923b7b3db730f2ae7c2a611e92d755e` |
| New qualification | `source-manifest.json` | 30815 | `102a500c818a5bb4652374c3c8621b7acc7bd42b0db53692646e942de8e27c3b` |
| Original moving admission | `results/check.json` | 31917 | `9991d6a3d60d7d0e58f69d0074947b38453013246b2c63ecfa3bf26a7086eb6d` |
| Original moving admission | `source/check.py` | 68149 | `084f4f45aa353f7a7d8adc5c4a78eae4b09ee83fb2119741b01a317225d3fa69` |
| Original moving admission | `source-manifest.json` | 10425 | `37a865330bbb86d0aef03dd3de775b830d7398abe69717b80c64860d4a8caa21` |

The packages are `research/m31-validator-qualification-2026-10-17` and `research/m31-moving-admission-2026-10-17`. The companion `CONTROL-REPAIR-RESULT-READING.json` records this interpretation's reading delta, exact pins and non-execution boundary.

## Narrow future source question

After the viewer and public result are closed, a separate source-only audit could ask: can exact source-normalization preparation and per-receiver rotor/self terms be computed once per captured state and reused within the exact backend, while preserving the binary64 operation graph, branch priority, candidate words, full coverage and certificates?

This is an untested audit question, not an identified bottleneck, a speedup claim or authorization to implement. Existing whole-stage durations and individual saved calls do not establish a stable backend benchmark or a primitive-level profile. Any later change or performance claim would need its own prospective equivalence, work-accounting and timing protocol. No further source reading or scientific execution is part of this closeout.
