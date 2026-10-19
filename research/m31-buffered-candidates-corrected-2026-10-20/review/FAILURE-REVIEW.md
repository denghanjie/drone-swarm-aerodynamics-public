# Independent saved-failure review

20 October 2026. This new result review reads the corrected attempt's saved files and existing source only. No scientific module, native query, original auditor or browser was executed. Frozen source, earlier reviews and result files were not edited.

## Verified execution record

The corrected attempt stopped after 31 native calls. Calls 1–24 are all twelve prescribed small F/C control pairs; calls 25–31 are candidate-only warmup stages 0–6 on the prescribed 1,000-drone inputs. The first six warmup stages returned native success. Warmup stage 6 returned `domain-refused`, reason `native-admission`, stage `build`, and the producer's required native-success assertion stopped the allocation.

All 31 journal references were checked against the actual saved semantic-file byte lengths and SHA-256 values. All twelve small control pairs reference identical complete semantic bytes, including stage 8's intended domain refusal and stage 11's duplicate-ID input refusal. Stage 10's far-coordinate control succeeded for both F and C. All 31 input-preservation flags and before/after hashes match the corresponding saved current inputs; canonical raw/ID associations match for every result that retained raw input. The duplicate-ID refusal correctly has null raw capture. The three candidate source files remain byte-identical to the original attempt.

The journal contains no large-input F query and no measured query. Stage 7 was not evaluated. No complete warmup-stream timing file, paired batch file or performance summary exists. The saved stage-7 input is a prescribed, unexecuted frame. The original 18-call failed attempt and this 31-call failed attempt total 49 native calls; neither unused budget is permission to continue either allocation.

## Exact meaning of the refusal

The saved stage-6 admission record has exactly `reasons: ["near-field"]`, `unsupportedNearCount: 186`, `invalidTermCount: 0` and `scaledCapViolationCount: 0`. The binary64 word for 186 is `4067400000000000`; symbol-count entry 4 agrees. The existing source assigns symbol 4 per receiver-rotor/source classification when the positive down-distance is below the model's near-field cutoff and radial distance is within its near-field radius. Admission uses that symbol count directly.

Therefore 186 is a count of unsupported rotor/source classifications. It is not a count of drones, distinct drone pairs, collisions or unsafe physical events. This computational model refuses that saved candidate query; the result is neither physical validation nor a flight-safety finding.

The recorded cache event at stage 6 is a box-exit rebuild, with two builds, five reuses and seven cache queries since the warmup reset. Those counters report that the displacement-triggered rebuild was reached. Full cache witnesses were only planned for controls and the first measured candidate stream; none exists for the large warmup sequence. These counters alone are not an independent proof of large-input candidate completeness.

There is no saved 1,000-drone F counterpart, including at the refused stage. Consequently this record cannot establish 1,000-drone F/C output equivalence, cannot demonstrate an observed F refusal at stage 6 and cannot by itself attribute the refusal to a candidate mismatch. The unchanged source provides context for the inherited model rule; it does not replace the missing finite paired outputs.

## Consequences and closure

The prospective correctness gate did not complete, and the performance panel never began. No speedup, paired median, strict-win count, performance ranking or useful-acceleration claim is supported. Saved control and partial-warmup durations must not be substituted for the frozen paired timing design. F remains the baseline.

The allocation is closed with exit code 1 and `closed-no-rerun` in its failure record. The unused original audit and display allocations must be closed unlaunched, as specified by the parent; this review does not consume or reopen them. A separate follow-up may verify and display the already saved failure evidence with zero native queries. It must label stages 0–5 as candidate-only successes, stage 6 as refused and stage 7 as unexecuted, and must not imply an integrated trajectory or completed timing comparison. No shrinking of the perturbations, replacement input, extra candidate variant or native retry is authorized by this review.

## Key saved identities

Paths are relative to the corrected experiment. The entire saved record remains available; this table identifies the journal, closure and refusal examined here.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| results/queries.jsonl | 74402 | 6906d908544f13ebbfd113a3a8808cd0b0b66fb1930de28d7bd2cfa5f8cc5f8c |
| results/failure.json | 186 | cf3740942a00bd6c82a0c0703e37d26d559b517885a592d358bcaad00e8c9560 |
| results/exit.json | 99 | 9ed00045e01b17f9e980f50422da9f896ce255446591a7e3e79d79502f121618 |
| results/semantic-5fbacdc58beec9571476fe209746d2c3108721788297425b921d352bbfce3b3a.json | 1899937 | 5fbacdc58beec9571476fe209746d2c3108721788297425b921d352bbfce3b3a |
| supervisor.json | 90 | 7afd73bdfa7c48ab643b28153e84fd847467e08b79b8c36b93186f47feac34c6 |

This saved-evidence review establishes the execution history and claim limits above. It is not the unlaunched full audit or an additional numerical experiment.
