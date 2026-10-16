# Typed storage preserved the answers but missed the improvement target

We tested whether changing the storage of airflow interactions makes a complete coupled-load query faster after both implementations already use the same lean arithmetic. On the two new 5,000-drone states, the answer was **no useful advantage under our predeclared rule**: typed storage was essentially tied with ordinary storage. We close this storage-variant line and keep the negative result.

A is the unchanged all-pairs anchor. L uses lean scalar arithmetic and ordinary storage. T uses the same arithmetic with typed rows/chunks and ordered dependency assembly. Each query includes fresh construction, scaling, ordering, solve, residual checks and output consumption. The comparison does not omit construction cost.

| Fresh state | A median ms | L median ms | T median ms | Median paired T/L | T wins |
|---|---:|---:|---:|---:|---:|
| 1,000 drones · seed260103 |43.75|37.24|36.42|0.99490|3/6|
| 5,000 drones · seed260101 |525.94|476.51|478.96|0.99911|3/6|
| 5,000 drones · seed260102 |501.07|473.71|476.92|1.00189|3/6|

The fixed target required T/L≤0.90, at least five strict wins out of six, and median paired T/A≤1 on **each** 5,000-drone case. Both cases failed the first two conditions. T did beat A in all twelve 5,000-drone pairs, but L did too; that does not establish a benefit from T's additional storage mechanism. L/A paired medians were0.89035 and0.93397. Lean rewriting is already known from this project's earlier work, and no new algorithmic novelty is claimed.

Every measured duration is retained, including long observations: A reached1,015.23ms in the first5,000case and865.98ms in the second; T reached586.81ms in the first. These values were not discarded. Six repeated calls within one process are dependent observations. The experiment identifies no individual cause for timing variation: GC, scheduling and compiler behavior were not separately measured. The full ranges, paired differences and phase sums are in [analysis.json](results/analysis.json).

The evidence checks completed:24controls, four extra ownership builds, three new flights, nine qualification builds/solves and63complete queries (nine warmups,54measured). All same-runtime A/L/T classifications, coefficient arrays, graph/admission fields and solved loads agreed exactly. The three methods saved612million classification entries in total. The independent Python/NumPy checker reevaluated all204million A entries and checked exact L/T agreement, then verified the saved schedule and arithmetic: **16,239 checks passed**. Independent coefficient differences were at most1.78×10⁻¹⁵; independent log residuals at most3.75×10⁻¹⁶, within the inherited fixed tolerances.

The inputs are actual new local3DBoids/rigid-body records, not prescribed formations. They retain separation, alignment, cohesion, a shared broad route and avoidance. All three reached two seconds, with no recorded stop/failure. Their final height spans were approximately4.94–5.19m. These are short airflow-off probes: none reached the course finish, and no current load calculation fed back into flight. They do not establish mature flock behavior, difficult-obstacle passage, long-flight safety or physical accuracy.

Hardware: Apple M4,10physical/logical cores,24GiB RAM, arm64 Darwin25.5.0, Node24.19.0/V8 13.6.233.17-node.51, AC power, low-power mode off. Candidate174.297s; independent reviewer7.973s; both exit0 with no monitor errors/races. Candidate sampled peak RSS826,114,048bytes; external801,872KiB. This is whole-invocation memory, not separate L/T memory. Source-level typed-payload counters cannot measure L's ordinary-object memory or GC behavior.

What improved: the known lean arithmetic package was faster than A in all twelve5,000-drone timing pairs. What failed: T's storage package added no qualifying improvement beyond L. What was sacrificed numerically: no difference was observed in the frozen same-runtime comparisons; the physical model was unchanged and remains unvalidated. Queries still took roughly half a second, excluding flight, steering, rendering and transport. A browser real-time result and a publishable accuracy–computation contribution remain unresolved.

[Recorded Three.js replay](viewer/) · [Frozen protocol](PROTOCOL.md) · [Raw evidence](results/evidence.json) · [Independent review](results/independent-review.json) · [Claim ledger](RESULT-CLAIM-LEDGER.md) · [Literature ledger](LITERATURE-EXPERIMENT-LEDGER.md) · [Restart](POSTRUN-RESTART.md).

Source checkpoint: [ec066cc](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/ec066cc0d555393606ceb05e5e6e04e09d567020). Source manifest SHA256:942dab53d86315e401e1d3e8b1b2549b57572aabef4436ebeb68f144ce4513b5. The result manifest and separate publication receipt identify the exact saved result commit after publication. No scientific rerun or post-outcome tolerance/parameter change occurred.
