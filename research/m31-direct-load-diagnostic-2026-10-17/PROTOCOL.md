# Direct-load diagnostic — prospective exploratory protocol

Status: SOURCE PREPARATION ONLY. Not allocated or executed until source and independent review are frozen, published and exact-public verified. No prior allocation is reopened.

## Question

Does deleting the weakest tenth of positive interactions preserve calculated rotor forces, total force and turning effects in the six previously studied snapshots? If so, does the existing conservative certificate recognize that accuracy? This separates approximation error from error-bound slack before spending effort on a practical selector.

The preceding oracle screen established that the fixed per-row tau/16 coefficient-mass budget permits less than 10% omission in every tested state, even at the loosest tier. This new test deliberately changes the rule; it cannot revise that negative finding.

## Fixed experiment

Reuse all six exposed 64-drone snapshots from the normalizer replication. These are dependent diagnostic states from two airflow-off Boids flights, not new independent trials or holdout confirmation. No scene, controller, physics parameter or trajectory changes. Exactly two proposals per state: full coefficients and deletion of ceil(P/10) positive rotor–source terms. Sort exact saved coefficient upper endpoints, then receiver ID, rotor index and source ID. Include every declared positive term, even with zero lower endpoint. No tree prerequisite, per-row budget, mask tuning or fraction sweep.

Use saved independently verified coefficient intervals as an explicitly paid-for oracle. Start all candidate rotor ratios at one. Freeze 48 simultaneous updates with 54 cubic-root bisections; no reference-root warm start. Native arithmetic proposes values only. Exact rational and outward interval arithmetic audits the resulting binary64 values. Ratios multiply nominal rotor thrust directly; they are not squared. Exact normalized source-force weights sum to one.

The frozen producer source and source configuration define conversion, ordering, square-root enclosure precision and exact output schema. Any source corrections before freeze remain recorded in review notes. No target experiment may execute during source preparation.

## Three comparisons of the same candidate

A compares candidate load values with saved full-model reference intervals. For each category retain lower and upper normalized error bounds, not midpoint truth. B encloses the complete contraction at the same candidate and propagates the existing local/global root-defect certificate into signed load boxes. C is only for the omission candidate: retain exact interval contributions for kept terms and replace each omitted row sum by zero lower bound and its full candidate-dependent upper bound. Re-solving for B or C would confound the comparison and is prohibited.

Report rotor error normalized by mg/4; collective and Euclidean world-force error by mg; Euclidean world-moment error by mg R. Report each category's worst value across all drones/rotors, with every state retained. Also record omitted coefficient mass at y=1 and candidate-dependent y for every row. No timing or physical-accuracy claim follows from these oracle-assisted measurements.

For A, upper error <= tolerance passes, lower error > tolerance definitely fails, and overlap is unresolved. B/C are certificate-sufficiency tests: an upper bound above tolerance means not certified, not necessarily inaccurate. Never call certificate failure a measured physical-force failure.

## Decision fixed before results

Primary numerical threshold is 1e-8 in all four categories and all six states. 1e-4 is a looser diagnostic; 1e-2 is stress only. These are normalization-relative numerical tolerances, not experimentally justified physical tolerances.

1. Full control must pass A at 1e-8 on every state. Otherwise omission attribution is invalid and the candidate/control procedure needs a new investigation.
2. If omitted A does not pass strict accuracy, do not advance this fixed proposal under the strict contract. A definite A failure even at 1e-2 stops this fixed route outright. No same-allocation tuning.
3. A pass with B not certified isolates conservative root/load certificate slack at that tier. A and B pass with C not certified isolates additional upper-only omission slack.
4. Only A/B/C all passing strict accuracy justifies a separately registered practical selector and complete-cost comparison. Passing a looser tier requires an explicit new numerical contract decision; never retroactively call it strict success.

No pooled average can override a failed/unresolved state. No confidence interval or population claim is assigned to these six reused snapshots. Success is accuracy headroom only, not avoided work, online certification, browser scaling, physical validation or novelty.

## Bounded execution and failures

One producer and one independent checker, each single use. Source-pinned runtime; exclusive attempt marker before import; CPU 120s soft/121s hard, 180s alarm and 16 MiB per output. OS peak RSS <=512 MiB is checked after output generation, not enforced as a memory ceiling. The alarm excludes interpreter startup and final teardown; final usage snapshot precedes final attempt serialization. Tool polling does not extend the deadline. Launch cutoff 2026-10-17 02:00 UTC. Incomplete, rejected or oversized attempts remain evidence; no automatic retry, precision extension, schedule change or replacement state.

Source-derived analytic fixtures and deliberately corrupted saved records will test arithmetic inclusion, masks, candidate identity, signed propagation and decision rules. Independent checking must not import producer routines. Parent reviews both sources before allocation. Save source hashes and output binding; publish a privacy-reviewed result checkpoint and an actual-record Three.js update after acceptance or failure.

## Interpretation and provenance

See the predecessor decision memo, M-current adopted design and its verified literature ledger for inherited mathematics and scope. This experiment introduces no external algorithm or novelty claim. Existing theory is conditional on the supplied prepared values and declared exact-real aerodynamic model. It does not validate the wake model against experiments or certify legacy JavaScript arithmetic. The original eight-step roadmap remains the organizing framework; this work continues approximation/evaluation gates toward the 5,000-drone goal.

## Final arithmetic specification before freeze

Coefficient conversion is float((aL+aU)/2) with the midpoint formed as an exact rational and rounded once. Native reductions are explicit left folds, coefficient accumulation uses input-source order, and Python math.sqrt proposes source ratios. This is not historical JavaScript bit equivalence. Exact audit square roots use integer-square tests on the fixed2^-192 grid. Root-defect endpoints are computed exactly and then rounded outward to that grid before signed load propagation; no other root precision search is allowed. B/C statuses are pass or not-certified only, while A preserves pass/definite-fail/unresolved. All256 omission diagnostic rows are present per state. The detailed output schema and arithmetic inclusion argument are in review/PRODUCER-SOURCE-PROOF.md.

Resource accounting is specific to the pinned macOS runtime: ru_maxrss reports bytes. Dispatcher rejects other platforms rather than silently treating their units as bytes. Porting requires a separate declared execution contract.
