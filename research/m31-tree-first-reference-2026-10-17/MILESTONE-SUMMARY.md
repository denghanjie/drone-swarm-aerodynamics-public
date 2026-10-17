# Same numerical answers, fewer individual checks

The tree-first exact reference matched the full reference on **all 24 fixed scenes**, while making **66.4% fewer scalar-oracle calls**: 26,570 instead of 79,008. Every positive coefficient interval, admitted root/load interval, and canonical admission/refusal decision matched exactly. This is a useful numerical checkpoint toward a more affordable trusted reference. It is not a new aerodynamic model, a measured speedup, or a publishable novelty claim.

Imagine checking whether every person in a distant room can affect one microphone. If a rigorous rule proves that the entire room contributes nothing, there is no need to inspect its occupants one by one. Here the rule is exact within our current mathematical model: groups are skipped only when their contribution is proved zero. All unproved groups are opened and their members checked individually.

## What we did

Before running anything, we published the fixed code, corpus, equality requirements, six deliberate faults and resource limits at source commit `e9c464b04b43e4f8dff5904bc657969d6ab1d3d6`. Its 585 file pins were verified against local and committed bytes and the exact public manifest. We then ran the old full reference and new tree reference once each on all 18 established static cases, four moving controls and both previously recorded 64-drone final flock states. None is an untouched holdout.

The comparison included dense and sparse groups, tilt, reordered identifiers, cutoff boundaries, unsupported near interactions and invalid inputs. Sixteen scenes were admitted by both references. Eight deliberately invalid/unsupported scenes produced the same canonical refusal. A matched refusal is correct handling of a test case; it is not an admitted physical configuration.

| Case or set | Full scalar calls | Tree scalar calls | Calls avoided |
|---|---:|---:|---:|
| All 24 scenes |79,008|26,570|52,438|
| Dense 64-drone lattice |16,128|4,992|11,136|
| Sparse 64-drone lattice |16,128|896|15,232|
| Saved flock A |16,128|7,408|8,720|
| Saved flock B |16,128|7,600|8,528|
| Failed global-guard fallback |24|24|0|

The 79,048 planned pairs include 40 pairs in three globally invalid inputs rejected before pair evaluation. They are retained in the denominator and account for the difference from 79,008 actual full-reference calls. The combined two-variant workload was 105,578 calls, below the 160,000 cap. The allocation completed in 23.603seconds, below its 600-second total reservation, with all 585 source pins preserved. Single ordered wall observations are operational diagnostics, not a benchmark.

All six prebound coverage faults were detected with their specified rejection codes. All 14 arithmetic fixtures, four saved browser-result audits and four existing load-law corruptions passed. The four browser checker reports were exactly unchanged. No browser scientific call or new simulation was run in this checkpoint.

## What this supports

For this exposed finite corpus, changing when we apply the exact group-zero proof avoided52,438 expensive scalar evaluations without changing the specified results. The work reduction depends strongly on geometry. The guard-fallback case saved nothing. Dense or difficult scenes can still require quadratic work; the new method is not an all-input scaling guarantee.

The validator expands the skipped members only in these small tests, checking each against the old full oracle. The actual dispatcher stores compact group ranges. It still repeats preparation in each residual scalar call, and its inherited tree builder temporarily allocates membership tuples. Root/load computation and exact-rational overhead also remain.

## What remains open

The new 3D viewer shows the two saved flock states with actual group/scalar coverage. It is a display of an earlier airflow-off Boids run plus later calculations. It does not establish coupled flight, physical accuracy, or interactive 5,000-drone performance.

The separate firmware-source investigation found both 32 g and 34 g controller mass settings and an inaccessible exact firmware commit. It could not establish per-flight mass, acceleration/gravity conventions or force-field meaning. Those measured data therefore remain inadmissible as verified physical-force labels. We have not fitted or scored an aerodynamic model against them.

A standard exact spatial hierarchy is not itself a novelty claim. The broader research remains incomplete. The next decision must weigh whether a bounded improvement to the independent reference enables a decisive accuracy–computation comparison, rather than treating further numerical housekeeping as evidence of physical progress.

The independent saved-only audit also passed: it checked all 52,438 omitted zero members, all 1,636 positive contributions, 1,724 root boxes and 4,741 signed load boxes, plus the source/result pins and journal. The repaired viewer passed 57 UI checks and 32 selections; the failed first mobile check is retained.

Read the [saved-result review](review/SAVED-RESULT-REVIEW.md), [claim ledger](CLAIM-EVIDENCE.md), [3D evidence view](viewer/), [raw index](results/index.json), [physical provenance findings](../m31-firmware-provenance-2026-10-17/FINDINGS.md) and [restart record](RESTART.md). UI QA is reported separately; its failures cannot alter the scientific outcome.
