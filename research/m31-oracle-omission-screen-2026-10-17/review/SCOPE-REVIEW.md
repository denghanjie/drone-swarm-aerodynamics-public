# Scope review: oracle coefficient-mass ceiling

**Support this narrower prerequisite**, with the interpretation and controls below frozen before analysis. It asks whether even ideal coefficient knowledge leaves enough positive-term headroom under a fixed proxy to justify developing bounds. It avoids prematurely building a solver, approximation or new load interface. The six replication states are exposed diagnostic cases; this is not independent replication or evidence about unobserved moving states.

This is a desk review of the parent's proposal. No raw values, source imports or scientific execution were used. Earlier memos remain unexecuted proposals. The parent will preregister any allocation separately.

## The singleton ceiling is valid under precise definitions

Use the complete M-current **normalized coefficients** `a_irj = K_irj * beta_j / nu_ir`, not unscaled K. For each nonself rotor row, let the independently qualified oracle enclose each actual positive coefficient by `[l_j,u_j]`. With `delta = tau/16`, sort all actual-positive members by `max(0,l_j)` and find the largest prefix whose lower-endpoint sum is at most delta.

This is a genuine optimistic cardinality ceiling for that row: every actually feasible subset has a lower-endpoint sum no larger than its true coefficient sum, and the smallest lower endpoints minimize that lower sum for a given number of terms. The ceiling ignores grouping, admission-proof cost and other implementation constraints, which makes it optimistic rather than deployable.

**Include actual-positive members whose interval lower endpoint is zero.** Dropping them because their LOWER coefficient is not strictly positive could invalidate the ceiling. Establish “actual positive” from the qualified exact-model classification/strict branch premises, not merely `upper > 0`, which can also describe uncertain or zero contributions. Preserve any unresolved classifications as unresolved; do not drop them from consideration and announce a valid ceiling.

Use exact integer/rational endpoint sums and exact budget comparisons, with deterministic ID tie breaks. The six-state identity, coefficient/model identity, oracle qualification and reference uncertainty must be pinned. Do not rerun a solver or regenerate flight to fill gaps in an existing artifact without a separate decision.

## The tree results are fixed-policy coverage, not ceilings

For T8/T2, sum oracle UPPER normalized coefficients over each nonself node set, allowing proved zeros. Count its actual positive members separately. Freeze the precise traversal: attempt the current node; accept if it has at least two actual-positive members and fits the remaining row budget; otherwise visit left then right. Once a node is accepted, do not count descendants. Self exclusion precedes scoring, mass sums and positive-member counts.

Accepted disjoint nodes then meet the coefficient-mass proxy, assuming the oracle enclosures are sound. Under the model's `0 < y_j <= 1`, their omitted contraction would also be bounded by that mass. This is a limited mathematical implication; it is not a load-error certificate.

Left-first greedy coverage need not maximize the number of omitted terms among all allowed node selections. Therefore T8/T2 failure cannot establish that no useful grouped selection exists. Call these **oracle-informed fixed-policy results**. Moreover, summing already known exact coefficient enclosures bypasses precisely the node-bound/admission machinery whose future cost and looseness are unknown. It is an intentionally favorable diagnostic, not an implementable speed result.

One inexpensive additional control would sharpen attribution: sort singleton UPPER coefficients and compute their budget-feasible prefix. If LOWER-singleton coverage is high but UPPER-singleton coverage is low, interval uncertainty can explain the gap. If both singleton measures are high but T8/T2 coverage is low, grouping/greedy restrictions are implicated. Without this control, report the gap as combined effects; do not assign it solely to tree granularity. This control remains coefficient metadata analysis, not a new solver.

## Denominators and continuation

For each state, retain all actual-positive nonself rotor-source terms in the coverage denominator, including terms never eligible for a selected node. Preserve every row and all six states in the accounting. Report zero-positive rows/states explicitly with an undefined percentage, rather than treating them as a pass or silently removing their existence. Give per-state results; pooled coverage can conceal a poor state.

The 10% figure may be a predeclared **engineering continuation trigger only**. Freeze whether it applies to each positive-bearing state or another stated aggregation before reading results; per-state reporting is required either way. A singleton LOWER ceiling below the trigger is a strong negative result for that fixed coefficient-mass budget and trigger. A ceiling above it merely fails to rule out headroom. T8/T2 exceeding it supports investigating actual bound construction, whose proof cost may still erase all benefit. No term-coverage percentage is a theorem about runtime savings.

Use `tau = 1e-8, 1e-4, 1e-2` as fixed prospective numerical tiers. Here `tau/16` is only a row coefficient-mass proxy. There is no candidate construction, complete contraction certificate, global `Kbar` propagation or physical-load validation. Consequently this analysis **cannot certify any of those load tolerances**, including the existing `1e-8` target. The `1e-2` tier does not establish physical 1% accuracy, relative error in each true load, trajectory accuracy or flight safety. No coefficients are actually omitted from a simulation, and no speed, 5,000-drone or browser-performance claim follows.
