# Desk review: oracle coefficient-mass ceiling

**Accept this as a cheaper first diagnostic, with the qualifications below.** The lower-endpoint calculation can prove that a count target is impossible under the stated per-row coefficient-mass proxy. The upper-endpoint tree selections provide oracle-assisted feasible examples under that proxy. Neither establishes load accuracy, an implementable bound, or speed. This review opens no target values, runs/imports no scientific code, creates no allocation, and changes no earlier proposal or source.

## The ceiling is rigorous if every true positive is included

For one fixed rotor row, let its independently established true positive coefficients be `c_1,...,c_m`, with saved sound bounds `l_j <= c_j <= u_j`. Use `L_j=max(0,l_j)` because coefficients are nonnegative. Include **every true positive**, including one whose lower endpoint is zero; do not interpret “positive lower endpoints” as dropping such terms. True-positive identity comes from the frozen reference's guarded predicate, not `u_j>0` or `l_j>0` alone.

For budget `b=tau/16`, sort all `L_j` nondecreasing and define

`k* = max { k in {0,...,m}: sum_{j=1}^k L_(j) <= b }`.

For any omitted subset S of size k satisfying the actual coefficient-mass proxy,

`sum_{j=1}^k L_(j) <= sum_{j in S} L_j <= sum_{j in S} c_j <= b`.

Therefore `k <= k*`. This requires no independence assumptions and is valid even when the reference intervals are wide. Wide/zero lower bounds can make it very optimistic; they cannot make the ceiling underestimate the possible count. Conversely, `k*` is **not** an achievable count, because fitting lower endpoints does not establish fitting actual coefficients.

Use exact rational comparisons and sums. The budgets are respectively `1/1600000000`, `1/160000`, and `1/1600`; binary64 literals are not the decision boundary. Source-ID tie breaking makes the printed prefix deterministic but does not change its cardinality. Check both maximality conditions: the fitting prefix is within budget and, unless k*=m, the next prefix exceeds budget.

Compute this separately for every rotor row, then sum k* across rows. The sum is a state-level optimistic ceiling because each row has its own budget. Do not pool all coefficients and substitute a global budget, and do not average row percentages. The state fraction is `sum(row ceilings) / total true-positive rotor-source terms`. A zero denominator is vacuous/NA, not an opportunity pass.

This is a ceiling for omissions that satisfy the **coefficient-mass** constraint. An eventual solver exploiting smaller candidate source ratios or a different error theorem might not be subject to that constraint; this diagnostic cannot rule out those policies.

## What the whole-node selections can legitimately show

For an original node C in a row, `U(C)=sum_{j in C} u_j` is a sound upper bound on its actual coefficient mass. Include every nonself member and every independently admitted zero, whose coefficient is exactly zero. Never infer a zero merely from a missing record unless the pinned reference schema explicitly certifies complete implicit-zero coverage. Refused, unresolved, malformed, missing, or inconsistent reference statuses invalidate the diagnostic rather than disappearing from its denominator.

If selected nodes are pairwise disjoint and their accumulated U is at most b, their actual omitted mass is at most b. Counting their independently established positive members is therefore a feasible **oracle** count under this proxy. It is a lower bound on the best feasible grouped count, not a maximum or upper ceiling. The references have already paid for all scalar answers, guards, normalizers and positivity information. This is deliberately optimistic bookkeeping, not a procedure that avoids that work.

Freeze this precise greedy rule for both trees: visit left first; only a self-free whole node with at least two true-positive members is a useful selectable candidate; accept it if `usedUpper+U(C)<=b`, charge that sum, and do not visit descendants. Otherwise descend if children exist. Zero-only and one-positive nodes do not consume the useful-group budget. At an unselected leaf, stop; no synthetic subleaf or self-removed group. Record uncovered/retained members so the final selected/retained/zero partition is complete and disjoint. If a different one-positive spending policy is desired, freeze and name it explicitly: it can change later selections despite contributing no useful group.

Count useful groups, their sizes and zero/positive composition, selected positive terms, their fraction of all positive terms, cumulative upper mass, and unused budget. Do not count admitted zeros as avoided positive work. Group/node counts are not interchangeable with positive-term counts.

## T8 versus T2: fair, but greedy counts need not increase

Keep T8 exactly as previously defined. Declare T2 prospectively as a separate **oracle structural sensitivity** using the same exact saved prepared-center rationals, axis-span tie rule, exact center/ID ordering, midpoint split, and left-first order, with only stopping capacity changed to two. Establish that every T8 node's member set exists in the refined tree; node IDs and contiguous permutation offsets can change. In the reviewed builder, longest-span ties choose the first coordinate, center ties use stable ID, and split position is floor(n/2). Bind those rules and the initial member identities explicitly.

T2 is a newly declared refinement, not a previously qualified approximation. Its geometric/statistical input remains the same six exposed states. Preserve T8 results and the earlier unexecuted bound proposal; do not add capacities, tree reorderings, or per-row best-of choices after viewing outcomes.

The optimal grouped count cannot decrease when the available node family is enlarged while retaining all old nodes. **The frozen left-first greedy count can decrease:** newly affordable descendants early in traversal can consume budget that T8 would have saved for a later node containing more positives. Such a decrease is not an arithmetic failure and must not be concealed by reporting only the better tree. Neither greedy result should be described as the best possible grouping. The singleton lower-endpoint ceiling remains an upper bound on both trees' feasible positive counts.

## Hurdle and interpretation

Treat 10% as a prospectively chosen engineering count screen, not a statistically or physically derived threshold. Decide comparisons exactly: “below 10%” means `10*sum(row ceilings) < positiveTermCount`; equality is not below. Show all six states at all three tiers, with a fixed denominator independent of tree, threshold and selection outcome.

- If the optimistic singleton ceiling is below 10% on **all six states**, the stated proxy has less than 10% positive-term count headroom everywhere in this diagnostic panel, even before grouping and proof costs.
- If it is below 10% on **any one state**, an all-six-state requirement of at least 10% positive-term omissions is impossible at that tier. This is a different and stricter policy decision than the preceding all-states-small summary; freeze which gate controls further work.
- A ceiling at least 10% is only an absence of this impossibility result. It might reflect loose lower endpoints. A tree selection reaching 10% supplies an oracle construction under the mass proxy, still without a practical geometric bound or cost evidence. Positive terms can have unequal evaluation costs, and fixed preparation/solver/output costs remain, so 10% of terms does not predict 10% runtime savings.
- If the 1e-2 stress tier fails an all-six-state hurdle, tighter tiers cannot rescue the singleton ceiling because k* is monotone in b. Report the tighter tiers anyway. Do not assume the greedy tree selections themselves are monotone in the tier, for the same budget-consumption reason as above.

The proposal's “large ceiling justifies only the next source design” is appropriately restrained. I recommend using **any-state impossibility** if the downstream ambition explicitly requires success on every state, while still reporting the all-states-small diagnosis separately. No new seed, replacement state, speed claim, final-load claim, or physical interpretation follows from either outcome.

## Small source-freeze checks

Before execution, require independent saved-data validation of complete pair identity/status/interval maps and pin all references, state identities and builder rules. Arithmetic fixtures should cover a true positive with zero lower bound, budget equality and one-unit overflow, tied endpoints, large rational denominators, and zero-positive rows. Selection fixtures should cover self-containing leaves, overlapping parent/child attempts, one-positive nodes that must not spend budget, and a nested-tree example where greedy coverage decreases. These are audit-tool qualification checks, not scalar/model recomputations.

Stop on invalid reference coverage, inconsistent endpoints, wrong exact arithmetic, incorrect denominator, overlap/self inclusion, or unjustified feasibility claims. Resource exhaustion or unfinished rows yields incomplete results. Keep “rigorous optimistic count ceiling,” “oracle feasible grouped count,” and “unexecuted practical bound proposal” as three distinct outputs. The parent retains the source-freeze and allocation decision.
