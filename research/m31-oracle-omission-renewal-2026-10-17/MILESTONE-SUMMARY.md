# This omission budget leaves too little work to skip

We asked an optimistic question before building a complicated shortcut: **if we already knew every aerodynamic interaction exactly, how many small interactions could we omit within our chosen budget?** Across all six saved drone states, the answer was below our10% screening target—even at the loosest tested budget.

This is useful negative evidence. It tells us to stop building this particular omission policy and examine the relationship between omitted interactions and the final force errors more directly. It does not show that aerodynamic approximation is impossible.

| Saved state | Nonzero interactions | Maximum count at loosest budget | Fraction | Existing tree | Finer tree |
|---|---:|---:|---:|---:|---:|
| A,0seconds |389|5|1.29%|0|0|
| A,5seconds |252|8|3.17%|0|0|
| A,10seconds |192|6|3.13%|0|0|
| B,0seconds |394|9|2.28%|0|0|
| B,5seconds |256|7|2.73%|0|0|
| B,10seconds |163|12|7.36%|0|2|

The existing tree groups up to eight sources per leaf; the finer tree uses two. The table counts positive rotor–source interactions, not drones, groups, frames or saved milliseconds. The tree columns use a fixed greedy policy and are feasible examples, not optimal tree results. Every state and all three budgets remain in [the complete results](analysis/summary.json).

At the strictest tier, no nonzero interaction fits the budget. At the middle tier, only0–3 fit per state. At the loosest tier, even allowing individual choices without grouping cannot reach10%. Lower-endpoint ceilings and upper-endpoint feasible counts agree in all4,608 row/tier cases, so interval uncertainty does not explain the small count allowance in this panel.

**What the budget means:** each receiver rotor gets a fixed coefficient-mass allowance of tau/16, with tau=1e-8,1e-4,1e-2. This is a conservative screening rule. We have not shown that it is necessary or sufficient for our desired final force accuracy. The loosest tier is not a claim of1% physical accuracy. A different error rule, source-load weighting or approximation could have a different trade-off; that requires a separate experiment.

The independent checker validated96,768 saved rotor–source pairs,1,536 rows and9,216 tree selections. The analyzer's nine analytic fixtures, the checker's19 fixtures and14 deliberate corruptions passed. Both stages completed normally. They took about1.11 and1.34seconds, respectively; these are analysis costs, not evidence of simulation speed. Reported OS peak memory was about91.3 and86.1MB. Memory acceptance was checked after output generation, not enforced as a hard ceiling.

The [updated Three.js view](viewer/) shows the six actual saved snapshots and the selected interaction links. It includes empty selections and the two links in the last state at the loosest T2 setting. The flight data are reused from the two earlier64-drone Boids flights, with aerodynamic feedback off. Amber links represent coefficient bookkeeping, not wake streamlines. No new flight or live approximation ran.

An earlier launch failed before the calculation because macOS rejected a resource setting. That attempt remains intact in [the predecessor package](../m31-oracle-omission-screen-2026-10-17/MILESTONE-SUMMARY.md). The separately registered renewal changed only the operational memory contract and its own checker path; the calculation and scientific rules remained identical.

The decision is limited to these six exposed states and this fixed budget rule. It provides no physical validation, browser speedup,5,000-drone demonstration, novelty or publication-ready contribution. Within the original eight-step framework, it advances approximation screening and evaluation. The next question is whether a direct final-load error test reveals useful headroom that this proxy suppresses.

[Protocol](PROTOCOL.md) · [Independent numerical accounting](results/check.json) · [Claims](CLAIM-LEDGER.md) · [Reproduction](REPRODUCTION.md) · [Restart](RESTART.md) · [Frozen source](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/ea2c963ea9a3e9af1eecaaeefe3739bf0082d0d5). The result manifest and publication receipt identify the final public result.
