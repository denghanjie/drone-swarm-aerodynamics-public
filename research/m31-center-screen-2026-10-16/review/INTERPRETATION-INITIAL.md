# Saved-claims interpretation review

Disposition: **consistent with the saved evidence; no blocking claims defect found.**

Reviewed package: `research/m31-center-screen-2026-10-16`.

This is a bounded review of three authored notes and five saved JSON artifacts. It compares the interpretation with saved gates, summaries, timing records, closure metadata, and stated limitations. It does not perform numerical reanalysis, rerun an experiment, import scientific code, read historical result sets, verify the viewer, or edit scientific outputs. Values below are copied from saved fields, not recomputed statistics. Viewer QA remains separate.

## Gate interpretation

`results/qualification.json` is the final authority for terminal qualification. It records `sealSuccess: true`, `evidenceQualified: true`, `practicalRulePass: true`, `performanceRulePass: true`, no failure reasons, and decision `qualified-finite-runtime-center-screen`. Its candidate closure, review closure, independent review, and performance-rule-availability gates are all true. It records no numerical reanalysis and zero additional scientific invocations.

The notes correctly use this completed seal. The null `practicalRulePass` and `reviewSupervisorClosure` fields in the in-child analysis are expected pending-terminal states, not contradictory final failures. The saved independent-review limitations explicitly explain this distinction.

Both supervisor records have return code 0, `closed: true`, `childGroupAbsent: true`, `runtimeIdentityVerified: true`, and `supervisorSuccess: true`; monitor errors, exit races, and signals are empty. Candidate elapsed time is 154.97735629044473 seconds and sampled peak RSS is 819380224 bytes. Review elapsed time is 9.0169997503981 seconds and sampled peak RSS is 188825600 bytes. These agree with the ledger's rounded figures. Both supervisor records explicitly identify their elapsed times as non-performance measurements.

The seal and both supervisors agree on source commit `9404ce3d578636ea0ee69b54626b1b8e7c1a7057` and source-manifest SHA-256 `b6758206e9efecad05890be7130b202339d58cd2e127b521b1ccf058579c3a78`. This review establishes agreement of saved source identities; it does not independently repeat source execution, repository publication, or remote commit verification.

## Performance and adverse evidence

The saved analysis supports the table and finite primary-case conclusion in the milestone and ledger:

| Saved case | L median, ms | F median, ms | Median paired F/L | Strict F wins | Performance rule |
|---|---:|---:|---:|---:|---|
| n1000-s261601-t2 | 36.31249999998545 | 45.10320850000426 | 1.0401845974905095 | 2/6 | false; not a required primary case |
| n5000-s261602-t2 | 478.9472709999973 | 369.3466254999803 | 0.7193143011022549 | 5/6 | true |
| n5000-s261603-t2 | 480.1067710000061 | 303.3828125 | 0.6608170544811809 | 6/6 | true |

The N1000 slowdown is visible and is not silently promoted to a win. The lost primary pair is also preserved: block 3 of `n5000-s261602-t2` has saved F/L ratio 1.4799628458407814 and saved difference +229.25833300003433 ms. The statement that both primary cases passed refers to the frozen case-level rule, not a win on every pair.

The stated substantial timing variability is supported by the saved values. For `n5000-s261602-t2`, saved L total-time minimum/maximum are 440.2850000000035/957.3484579999931 ms and F minimum/maximum are 293.2425000000221/739.6472079999803 ms. For `n5000-s261603-t2`, saved L minimum/maximum are 445.1120419999934/804.7026249999763 ms. The notes retain the six paired within-process repeats and do not treat them as independent process replications, a population sample, or evidence of a particular scheduler/GC cause.

The milestone explicitly distinguishes the median of paired ratios from the ratio of separate medians. The reported percentage descriptions are interpretations of the saved paired-ratio statistic; this review did not recalculate percentages.

The F screen-count records preserve 24995000 ordered-pair visits in both primary cases while reporting 20661016 and 20650692 skipped center-norm calls, respectively. The notes correctly limit this to skipped center norms, retain the ordered-pair work, and avoid an asymptotic or operation-count-only speed claim.

## Correctness and scope of inference

The saved independent review is complete and passing, with `candidateComplete: true`, `checkCount: 18458`, and an empty error list. Saved coverage reports 42 validated timing records out of 42 expected, 48 expected controls, and three expected fresh cases. All three saved qualification summaries pass. The case analysis has true exact-output-equality, omitted-pair, controls/ownership, generation, timing-schedule, and candidate-closure gates. The notes accurately describe this as finite evidence and describe the check count as named groups rather than independent scalar observations.

The ledger retains the material limitation that transient timed arrays were compared inside the candidate process and were not all independently persisted. This interpretation does not turn the successful saved audit into reconstruction of every transient array or a proof of all future aliasing behavior.

The summary, ledger, and next-question note keep the result within a fixed runtime, three saved states, two primary seeds, and one process. They retain the airflow-off generation and final-pose-only model-query limits. They do not claim physical aerodynamic validation, integrated coupled flight, portable/browser/GPU performance, real-time end-to-end behavior, general floating-point equivalence, unseen-state guarantees, novelty, or a publication-ready breakthrough. The recorded remaining query cost and excluded pipeline stages support those restrictions.

`NEXT-QUESTION.md` frames external validity and fresh-process testing as future questions and allocates no additional run. It leaves physical-data and independently verified literature comparisons unresolved and does not reopen closed access or experimental work. The historical result-bearing arithmetic-file exposure is retained in the ledger and the saved review limitations; there is no blind or unexposed-design claim.

## Actionable claims defects

**None required to preserve the current bounded conclusion.**

One optional wording improvement is available at `MILESTONE-SUMMARY.md:3`: replace “at least 10% lower paired query time” with “a median paired F/L time ratio at most 0.90.” The current later table and explanation already identify the statistic and disclose the lost pair, so this is a clarity edit rather than a contradictory or unsupported claim. A precise complete formulation is: “Both primary cases met the frozen rule: a median paired F/L time ratio at most 0.90 and at least five strict F wins in six comparisons.”

## Source identities

The first three identities were recorded when the authored notes were read; the five JSON identities identify the saved artifacts inspected for this review. Paths are relative to the reviewed package.

| Source | SHA-256 |
|---|---|
| `MILESTONE-SUMMARY.md` | `840316f4feb8de8389747ef7ee6fdb5c170611d82a912721b072d39aa22f7497` |
| `RESULT-CLAIM-LEDGER.md` | `e2679c3768e7141ee06fbf0f515e39dee70515be7e6516950860fff509f5a2af` |
| `NEXT-QUESTION.md` | `e29e9ac0eb60a0cff5e9a3bddf87ba803eeb95957313fa64d3e5d7bbe95dd36c` |
| `results/qualification.json` | `b5cd9fa6f32b4798767c047c01fa713303fae8d65d259b0b3ae2b6e7f3599a95` |
| `results/analysis.json` | `57d35512dccd94ff16bacdc4b27980f5caa8ac114b9778d0f046be0d92149588` |
| `results/candidate-run.json` | `a18388d708b0838d26c00d2c3dcec318f1011a1160fcf2b730e4d9a4b21b88a9` |
| `results/review-run.json` | `eb67d5f6f048bc81906f18b546d522037ef4ad7bcbaf6dd6d08c00da04d949ed` |
| `results/independent-review.json` | `d3879416ae85b3102aa36d099e5a6369bf1bc7c87c69f1cd0a4e2cf3db9960ec` |
