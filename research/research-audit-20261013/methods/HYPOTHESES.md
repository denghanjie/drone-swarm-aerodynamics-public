# Two untested literature-grounded hypotheses

Status: proposed on 2026-10-13 after the frozen campaign. No experiment below has run, and neither hypothesis modifies earlier gates. Save and review a separate final experiment plan before execution. All computations remain CPU-only and bounded at N≤200. The numerical model, accepted-domain checks, all four rotor contributions, source ordering and update cadence remain fixed.

## H1, recommended: the modest whole-pipeline gain is partly a runtime-state effect

**Uncertainty.** The primary N=16 lean/previous-zero total-time ratio is 0.911; the independent ratio is 0.960 with an interval crossing 1. Existing stage accounting puts field work below one fifth of lean total time, while physics exceeds one half. All non-field code is identical between variants, but its measured times can vary with process/JIT/GC state and ordering.

**Competing explanations.**

- H1a: the field saving gives a stable incremental whole-pipeline improvement that survives process restarts; the total saving is mostly the field saving propagated through its workload share.
- H1b: much of the apparent total gain is process/order-dependent variation in unchanged stages; the field advantage can persist while the total practical-gain target fails.

**Literature basis.** Kalibera and Jones, sections 3, 6, 7 and 9: choose repetition at the level where variability arises rather than treating repeated inner calls as independent executions. This proposed design is our adaptation, not their published estimator. [Primary manuscript](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf).

**Small diagnostic protocol to freeze.**

1. Reuse both already-saved pipeline workloads separately: primary seed 4301 and independent seed 628791, N=16, 1 s, 400 physics steps and 100 field updates. No new count scaling and no implementation tuning. Establish exact initial-state equality and terminal full-state/held-field hashes using the same runner for every method.
2. Run a short dimensioning pilot in independently started Node processes. Retain every startup and warmup sample. Inspect run-sequence and lag behavior before setting a warmup rule for the confirmatory phase. Do not choose a warmup cutoff from whichever rule makes lean look fastest.
3. Bound the pilot to four processes per workload and twelve balanced method blocks per process. Each block compares frozen previous-zero and lean, plus a two-label lean/lean sham to estimate order effects in identical code. Deterministically randomize and balance label order. Use an exclusive serial window; do not parallelize benchmark processes.
4. Save a separate confirmatory plan after the pilot, using a fresh set of processes and unchanged warmup rule. Treat each process as a cluster. Report raw totals and stages, startup-inclusive and post-warmup results separately, paired ratios, between-process spread and process-cluster uncertainty. A small pilot alone is not a population-level speed claim.
5. Keep a five-minute pilot wall cap and a 45-second per-process cap. Stop and retain the failure on unequal work, mismatched hashes, nonfinite values, model-domain/contact failure or exhausted cap. If the pilot cannot establish a defensible measurement regime, report it as inconclusive; do not silently increase the budget.

**Falsification/decision rules.** The pre-existing practical target is at least 10% total saving with interval upper endpoint below 1. H1a's strong practical version fails if either workload fails that frozen confirmatory target. A smaller reproducible benefit may still exist and must be reported numerically. H1b is weakened if restarts/order/sham results show no material variation and saved total differences remain attributable to the field across workloads. Evidence of sizeable differences in identical-code stages or lean/lean sham labels supports H1b. If a sham differs by ≥5% median or obvious time trends remain, halt speed inference and diagnose the harness/runtime rather than crediting an algorithm.

**Stopping outcome.** A clear smaller-than-target or inconclusive incremental result closes this optimization question for these workloads; do not continue tuning until another improvement appears. This experiment addresses software attribution, not aerodynamic fidelity or mission success.

## H2, conditional: exact grid lifecycle overhead can exceed avoided kernel cost

**Competing explanations.** H2a: a reusable, timestamped bucket structure, refreshed on every field call, reduces allocation/clearing enough to improve exact field time. H2b: sorted neighbor production, bucket traversal and bookkeeping dominate so the added lifecycle logic yields no worthwhile gain, especially at N=100/200.

**Literature basis.** Teschner et al., section 4.2, PDF page 4, uses per-step bucket timestamps; sections 4.3 and 5 expose the traversal/occupancy tradeoff. This is inspiration for a future implementation, not evidence of benefit in this simulator. [Primary manuscript](https://cg.informatik.uni-freiburg.de/publications/2003_VMV_collisionDetectionHashing.pdf).

**Prospective comparison.** If H1 leaves a useful field-optimization goal, compare exactly one frozen grid-lifecycle variant against current lean and previous-zero, with original 1.5 m cell size, 3 m strict-radius predicate and ascending source order. Keep full cell keys initially; do not combine hashing, cell-size tuning and kernel changes. Rebuild membership from current positions every call. Reuse internal capacity only; caller-owned winds and mutated-state semantics remain unchanged.

**Tests and measurements.** First match the all-pairs oracle and current results on the existing domain, support boundaries, translated states, changed N, in-place mutations and output-ownership fixtures. Add epoch rollover/reinitialization and stale-bucket regressions in the new plan. Measure total field time including refreshed membership, bucket traversal, sorting, validation and output. Keep zero-field controls and dense/sparse/tilted cases; allocation counters are diagnostic, not a substitute for time. Only then use a fresh held-out set, a dimensioned serial timing protocol and a separate matched-work pipeline check.

**Falsification/decision.** Any omitted positive contribution, altered exception or output aliasing rejects the variant. If the frozen ≥10% field saving and upper ratio below 1 do not hold on both fresh seeds of a claimed family/count, that claim fails. A field pass without a whole-pipeline pass remains a field-only result. Stop at N≤200 and retain the negative result; do not claim linear scaling from a sparse case or borrow the paper's tetrahedral cell-size optimum.
