# Draft mathematical review: exact source screening

**The proposed global guard certificate, five node-zero predicates, and median-tree construction are conditionally sound.** No algebraic counterexample was found under exact rational interval arithmetic on the actual prepared dyadics. The status-order, partition-count, and fallback clarifications below should be frozen before implementation or execution. This is design review, not approval of an implementation, qualification result, or speedup claim.

I read five inherited files, including only lines 1–52 of the coupled implementation; the inventory records exact paths, hashes, and scopes. No scientific module was imported or evaluated, no numerical case or earlier suite was run, no external operation occurred, and no agent was created.

## Guard discharge and conservative failure

For an interval `J=[l,u]`, use `maxabs(J)=max(|l|,|u|)` and `minabs(J)=0` when it contains zero, otherwise `min(|l|,|u|)`. Sums of squared component maxima upper-bound squared vector norms; sums of squared component minima lower-bound them. Component extrema need not occur at one member: that loses tightness, not inclusion.

After every raw/prepared drone has been validated, the proposed global center, receiver-point, and source-axis boxes contain every operand used by every nonself pair. Natural interval subtraction, multiplication, and addition therefore enclose `d`, `h=d dot a`, and the actual residual `e=d-h*a`. The stated upper bounds discharge the center component/norm, rotor component, down-magnitude, and radial-magnitude guards. Equality is safe because the inherited guards reject strictly greater magnitudes. This argument does not assume an exactly unit axis, use `||d||²-h²`, or reconstruct a prepared point from center plus offset.

The proof is intentionally stronger than necessary: it bounds all pairs, including those for which an earlier zero branch would prevent a later guard from being reached. Insufficient global proof must select complete scalar fallback, not model rejection or zero. Failed enclosure construction, stale membership, and resource failure must remain separately named administrative/proof failures; an inability to prove a bound is not an exact guard violation. Freeze whether these failures select full fallback or an unqualified resource outcome, and retain all attempted work in the hierarchy's cost.

Global preparation and identity validation precede both screening and self exclusion. The global certificate does not discharge near-field rejection, positive width, caps, positive-source ordering, or the positive-term cap. The refactored prepared-pair helper must preserve those checks and the original guard order. Both methods must use the same current prepared operands and pay their own preparation; removing repeated preparation only from the hierarchy would change the comparison boundary.

The center norm condition is redundant once each component difference is at most 257: `3*257² < 512²`. Keeping both checks is harmless, but no isolated center-norm rejection coverage should be inferred under those simultaneous component conditions.

## Five zero predicates

Let `T=minDown*Dconst`, with the frozen positive `Dconst`, `spread`, `neighbor`, `nearRad`, and `radCut`. Node center/axis boxes and the actual receiver center/point define the draft's `H`, `E`, radial-squared lower bound, and width interval. All comparisons below are exact and apply only after global guard discharge succeeds.

| Rule | Why every nonself member is zero |
| --- | --- |
| Neighbor: center-distance lower `>=neighbor²` | Every member passes the discharged center guards and reaches neighbor zero. |
| Upstream: `H.upper<=0` | Members outside center support already reach neighbor zero; center-eligible members pass discharged displacement/down guards and reach upstream zero. |
| Down-cut: `H.lower>=downCut` | Center-ineligible members are neighbor zero; eligible members reach down-cut zero after the discharged guards. |
| Near-outside: `H.upper<T` and radial-squared lower `>=nearRad²` | Center-ineligible members are zero. Eligible members with `h<=0` are upstream zero; any member reaching the positive near slab has `h<T` and radius outside the strictly rejected radius, hence near-outside zero. Any earlier down-cut zero remains harmless. The strict upper comparison and non-strict radius comparison match the scalar branches. |
| Radial: `H.lower>=T`, `W.lower>0`, and radial-squared lower `>=radCut²*W.upper²` | Center-ineligible or down-cut members are already zero. Remaining eligible downstream members cannot take near rejection, have positive actual width, and satisfy `r²>=radCut²*w²`, since `0<w<=W.upper`; they reach radial zero. Equality is included by the inherited cutoff. |

The natural interval residual `D-H*A` retains the supplied near-unit axes correctly. The radial rule's `W.lower>0` also makes squaring its upper endpoint order-preserving. A failed predicate supplies no zero conclusion; descend or evaluate. Projection screening is properly absent because an early projection zero could hide near rejection. The five proved branches all precede active coefficient/cap evaluation, so correctly screening them cannot hide an active cap rejection.

A node proof may cover members with different original scalar zero branches. Its label must mean **proof predicate**, not a claim that every member took that named scalar branch. This is compatible with the proposed contract that omits exact legacy zero-reason arrays.

## Exact tree and self membership

Unique exact stable IDs, exact coordinate spans, the fixed x/y/z span tie-break, coordinate-then-ID sorting, and a `floor(n/2)` split determine the proposed tree. For nodes larger than capacity eight, both children are nonempty and strictly smaller, so recursion terminates. Freeze left-before-right preorder IDs and a canonical serialized membership order; these details should not depend on incidental sort stability or raw input permutation.

The checker should reconstruct membership and bounds from the current prepared input, not accept stored counts as a substitute. Require root membership equal to the full source-ID set, child sets disjoint with union equal to the parent, and exact current center/axis bounds. Per receiver/rotor, stopped nodes and evaluated leaf singletons must form a disjoint complete partition of the **nonself** source universe. A count equality alone can conceal a duplicated source and a missing source.

The draft's requirement to prove a self-containing node zero for all members is safe and conservative. Its covered nonself membership is nevertheless `node.members minus {receiverID}`, and its count is `node.count-1` when self is present. Self must not become an evaluated nonself singleton or a positive/zero contribution in the partition count. A proved-zero node stops descent; it cannot also contribute descendants. An isolated valid drone has an empty nonself partition, but still needs global preparation. Retain the nonempty-scene policy and exact unique-ID validation before tree construction.

Tree membership, global bounds, node proofs, scalar outcomes, and common load certificate must all refer to the same current operands. The independent prepared-pair adaptation review is required; shared baseline/hierarchy agreement alone could preserve a shared helper defect.

## Status precedence and exact positive rows

**Required clarification:** full traversal is necessary but does not itself preserve the inherited first-refusal witness. Tree visit order differs from receiver/rotor/input-source order. After traversal, sort evaluated singleton outcomes by the original input tuple before selecting the first proved pair rejection, then the first unresolved pair, then the first positive ordering violation, then the actual-positive-term resource outcome. Global preparation retains its earlier priority. Alternatively, explicitly declare another common prospective interface for both methods; do not change only the hierarchy's witness rule.

Proved-zero nodes remove no possible rejection, unresolved interaction, or positive edge. Thus sorting the retained singleton outcomes restores the inherited scene priority without expanding skipped zeros. Positive singleton edges must likewise be assembled in receiver/rotor/input-source order before the shared proposal and certificate arithmetic. Count every positive classification even when its coefficient interval has lower endpoint zero. The actual positive-term count is exact only after all required pair outcomes are resolved; unresolved interactions must never be counted as admitted zeros.

Complete scalar fallback must retain the same status, coverage, cap, ordering, and load obligations as the baseline. Its attempt/proof failure is an additional hierarchy diagnostic, not a replacement model status. No early return on a tree-visited refusal may leave the source partition incomplete while claiming successful coverage.

## Prospective qualification boundary

Freeze independent controls for false-zero proof, subtree omission, overlapping membership, wrong bounds, stale current input, and positive/load corruption. Boundary declarations should exercise the actual strict/non-strict inequalities; descriptive scene names or rounded decimal identities do not by themselves prove a boundary. The 2,000,000-positive-term limit needs separate source review and cannot acquire threshold coverage from a maximum-64-drone suite.

Proved-zero coverage and scalar-evaluation counts are algorithmic work records. They do not establish total-cost savings: preparation, tree construction, bound computation, traversal, certificate generation, output, and fallback remain charged. The design advances the exact-screening stage of the original 5,000-drone/full-cost goal; it does not establish physical accuracy, dynamics, scalability, novelty, or completion of that goal. No numerical execution is authorized by this review.
