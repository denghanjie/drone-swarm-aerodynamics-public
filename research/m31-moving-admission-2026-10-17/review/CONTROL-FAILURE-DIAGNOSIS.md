# Closed-allocation control failure diagnosis

The `false-zero-active-leaf` corruption was rejected, but by `filter-work-counter-reconstruction` before the intended node-zero proof checks. This is a defect in the mutation recipe's isolation of its intended failure, not evidence that a false zero node was accepted. The preregistered checker correctly retained `intendedCoreFailure:false`, overall `passed:false`, `advancement:false`, and exit code1. Those saved decisions remain authoritative.

This diagnosis uses only saved JSON, frozen source text, and byte hashes. No scientific module was imported, no mutated record was generated or evaluated, no oracle or checker was invoked, no source was repaired, and neither closed allocation was reopened. The counter trace below is source-level bookkeeping from recorded values, not a new scientific reconstruction.

## Saved outcome and closure

The saved `results/check.json` records six reached states, six independently verified states, six model-admitted states and six certified states. Its nontriviality result is informative and its four fixed implementation controls pass. Nineteen of the twenty corruption controls report their intended failure; `false-zero-active-leaf` is the sole exception. These are recorded conditional findings, not a complete preregistered admission pass.

The kernel supervision report has `closed:true`, `success:true`, `exitCode:0`; the checker report has `closed:true`, `success:false`, `exitCode:1`. Both record guardian exit0, absent scientific child/group, source/runtime rechecks and no termination reason. The observed checker failure is therefore its explicit control qualification failure, not a recorded timeout or resource termination. This does not extend any claim beyond the saved reports.

Frozen source commit: `2a957d2b0bb26e731c8cd184bc13f51f673e9a0d`.

Frozen source-manifest SHA256: `37a865330bbb86d0aef03dd3de775b830d7398abe69717b80c64860d4a8caa21`.

## Exact source path to the short circuit

The saved control identifies scene `positive`, receiver `i:0`, rotor `r:0`, source `j:1`, node0. The first saved query is a mixed leaf containing a positive singleton for source1 and one natural fast-zero record `{j:2,branch:"radial"}`. It has `zeroCount:1`. The original saved method work includes `scalarPairs:8`, `filterZeros:4`, and `exactScalarCalls:4`.

The frozen recipe at `source/check.py:769–773` replaces the entire selected leaf terminal with `{kind:"zero",node:0,rule:"neighbor",count:2}`. Replacement discards both the positive entry and that terminal's `filterZeros` list. The recipe does not change the method work object. The clone and validation call are at lines720–726; the original saved record is untouched.

The filter wrapper's `kind == "zero"` path at lines279–282 checks the terminal's field shape, appends it to the normalized hierarchy terminal list and continues. It deliberately leaves the substantive node proof to the inherited semantic validator. Because the replacement has no fast-zero list, it contributes nothing to the wrapper's `total_zeros` accumulation at lines301–313. The other three fast-zero records remain. The wrapper still uses the independently constructed original hierarchy plan's `scalarPairs:8`.

Consequently the wrapper's expected added filter fields at lines321–324 become:

| Field | Unchanged clone reports | Wrapper expectation after terminal replacement |
|---|---:|---:|
|filterZeros|4|3|
|exactScalarCalls|4|5 (=8−3)|

This mismatch raises `filter-work-counter-reconstruction` at line325. The subsequent call to `semantic.validate_method` at line329 is never reached for this mutation. In the unchanged `source/semantic-reference.py`, the intended `node-zero-rule` and `node-zero-oracle-member` checks are at lines677–681. Their presence in source is not a claim that this failed control executed them.

The expected failure families are frozen as `["node-zero-rule","node-zero-oracle-member"]` in both `source/result-contract.json` and checker `RECIPES` at line677. `run_mutation` records only the first exception and compares it with those prefixes at lines696–709. The recorded counter error matches neither, so `rejected:true` coexists correctly with `intendedCoreFailure:false`. Lines1218–1219 require every corruption control's intended failure; lines1231–1234 therefore block both overall integrity pass and advancement.

The causal interaction is specific: the mixed positive control intentionally supplies a natural fast-zero witness, and whole-leaf replacement removes that witness's list without maintaining the wrapper's two derived filter counters. The recipe therefore tests an incidental counter inconsistency before it can test its designated node proof.

## Narrow future recommendation

Keep the present source, contract, output, attempt records and failure decision unchanged. Do not add `filter-work-counter-reconstruction` to this control's accepted failure families after seeing the result: that would weaken the preregistered node-proof target and reclassify a failed test retrospectively.

For a separately authorized future source package, the smallest proposed repair is confined to this mutation recipe: when replacing its fixed positive leaf, also maintain the two wrapper-derived counters for the removed fast-zero list—decrease the clone's `filterZeros` by that list's length and increase `exactScalarCalls` by the same length. Keep the original independently expected hierarchy work counters, positive scientific witness, false node claim and intended node-proof failure families. The purpose is to remove the incidental wrapper-counter failure so that the designated node-proof validator can be reached.

That proposal has not been implemented or evaluated here. It needs a new explicit recipe, independent source review and a fresh authorized allocation before any claim that the corrected control succeeds. It gives no basis for repairing or rerunning this closed allocation, altering its checker exit code, or advancing the present experiment. Viewer and publication closeout should display the preserved failed qualification alongside the six conditional per-state certification records.

## Exact reviewed pins

Paths are relative to this package. Frozen source rows below also match their saved source-manifest rows.

| File | Bytes | SHA256 |
|---|---:|---|
|`source/check.py`|68149|`084f4f45aa353f7a7d8adc5c4a78eae4b09ee83fb2119741b01a317225d3fa69`|
|`source/result-contract.json`|9872|`f9dea13a77a04a2a974caf5ffec06125b6fcb506eb23e9d34266fe2494e8a7c3`|
|`source/semantic-reference.py`|39634|`ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c`|
|`source-manifest.json`|10425|`37a865330bbb86d0aef03dd3de775b830d7398abe69717b80c64860d4a8caa21`|
|`results/check.json`|31917|`9991d6a3d60d7d0e58f69d0074947b38453013246b2c63ecfa3bf26a7086eb6d`|
|`results/controls/positive.json`|13549|`210deaeb19fda489d06fade1bb978999083b3c4c74d15943d856ed07a433ba78`|
|`results/checker-attempt.json`|422|`f4b98d31589dc0c8ddeca9bba45b58a716d2db52de35699a5b77c360839d68ac`|
|`results/kernel-supervision.json`|10032|`1c7111780d7da4315f502da70de447bb14ecdd3e5ad02a2a5565d8b87707e6e6`|
|`results/checker-supervision.json`|14898|`1086c03e34f19f580c9e78637de3d6918e63f9339f6d7a0cd47837eeb8c43c43`|
|`review/CHECKER-READING.json`|3932|`73526c79fbf5e245a6140e1a0ca8fe9f367d5f2514bc35a40c47c5d177ceb1d6`|

## Reading inventory delta

`review/CONTROL-FAILURE-DIAGNOSIS-READING.json` records the ten files touched for this diagnosis, their exact byte pins, whether they were source-inspected, JSON-inspected or hash-only, and their limited purpose. The inherited-source inventory remains11of20: the sole inherited source revisited here is the already-inventoried unchanged semantic helper. The frozen checker/contract were authored in this package, and the newly inspected saved result/manifest records are distinguished from inherited source. No additional candidate, generator, pair-helper, or runner source was opened. An initial path discovery found no package in the separately named public worktree; no content was read or written there. Only this diagnosis and its inventory were created in the corrected checkpoint worktree.
