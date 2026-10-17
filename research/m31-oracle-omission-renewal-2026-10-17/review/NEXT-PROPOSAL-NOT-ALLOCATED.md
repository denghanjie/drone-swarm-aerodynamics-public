# Decision after the negative coefficient-mass screen

Recommendation: consider one bounded, oracle-assisted direct load-error diagnostic before designing another geometric selector. Its hypothesis is: a fixed omission of at least 10% of positive terms can preserve all four final-load tolerances, even though the fixed tau/16, y=1 proxy rejected useful omission. This is an accuracy-headroom question, not a speed experiment. This memo allocates nothing and authorizes no execution.

The parent reports the renewed screen completed and passed its checker, with all six stress-tier optimistic omission ceilings below 10%. I have not independently audited those outputs here. That closes the fixed proxy under that allocation; it does not determine actual load error under a different, explicitly declared proposal.

## Minimal proposal and control

Use the same six already exposed small states and exact-real prepared-word model. Freeze one mask rule before viewing new outcomes. For each state with P reference-positive terms, omit exactly ceil(P/10), ordered by saved independent coefficient upper endpoint, then receiver stable ID, rotor index, and source stable ID. Retain the existing declared positivity rule, including positives whose lower endpoint is zero. This is a global mask; there is no per-row tau/16 budget or tree-group prerequisite.

Produce exactly two native candidates per state:

1. Full-coefficient, zero-deletion control.
2. The fixed 10%-deletion proposal.

Both start from all ones and use the same frozen iteration/bisection schedule and coefficient-to-native conversion. Use full or retained reference-coefficient midpoints as proposal inputs; do not warm-start from reference roots or loads. This is oracle assistance: coefficient construction has already been paid for, and these candidates need not be bit-identical to the earlier baseline. Do not tune the schedule, fraction, ranking, or mask after seeing errors.

## Three audits of the identical candidate

A. Independent final-load comparison. Compare candidate-induced loads against independently verified full-model load enclosures for that exact state. Compute outward lower and upper bounds on the error, preserving rotor, collective, world-force, and world-moment definitions and their existing normalizations. Reference midpoints are not truth. Upper error at or below tolerance passes; lower error above tolerance definitely fails; overlap is unresolved. No automatic precision extension follows an unresolved comparison.

B. Full-contraction current-bound certificate. For the same candidate, evaluate candidate-dependent y with the declared exact normalized weights; enclose every full coefficient-times-y contribution. Apply the existing local kbar, global Kbar, root bounds, and signed load propagation. This deliberately pays all scalar costs offline. Compare its four final error bounds with A. One bad row can enlarge global Kbar and widen every root enclosure; a root-ratio statistic alone is not the load decision.

C. Upper-only omission certificate. For the identical omitted candidate and fixed mask, keep interval contributions for retained terms and replace the omitted contribution in each row by [0, sum(a_upper*y_upper)], using outward arithmetic. Apply the same root/load chain as B without re-solving. This isolates the additional uncertainty from upper-only omission, before practical geometric-node slack. It is not a universally optimal enclosure, and finite-width reference endpoints do not prove every practical bound must be worse.

Audit A and B for the full control and the omitted proposal; C is the omitted-proposal audit. Also report each row's omitted sum(a) and sum(a*y(candidate)) enclosures as a descriptive y=1 diagnostic. Do not use those observed values to revise the mask.

## Decisive gate and stopping branches

The primary threshold remains 1e-8. Name 1e-4 separately as a looser numerical diagnostic and 1e-2 as stress only; neither is an adopted physical tolerance. Require every state and each output category to pass, with no pooled average. A gate fails to pass if any result is unresolved.

- The full native control must pass A at 1e-8. Otherwise stop: the proposed native schedule/reference comparison is not an adequate control, and the result cannot attribute failure to omission.
- If omitted A does not pass at 1e-8, there is no strict-accuracy basis to advance this fixed proposal. A definite A failure even at 1e-2 on any state stops this fixed selection/solver route outright. Neither conclusion disproves every approximation; neither licenses a smaller-fraction or divisor search in the same allocation.
- If A passes but B does not, the existing full-contraction root/load certificate cannot certify the independently verified accuracy at that threshold. Investigate that certificate only if the parent chooses this branch.
- If A and B pass but C does not, upper-only omission uncertainty is the next obstacle. A geometric selector has not yet been justified.
- If A, B, and C all pass at 1e-8, advance only to a separately reviewed practical selector/solver and complete-cost experiment. Passing at a looser diagnostic tier requires an explicit tolerance/contract decision before any implementation branch.

These branches compare the same candidate at the same threshold. They diagnose this fixed experiment; they do not establish a general impossibility or a new online guarantee. End with a branch decision, without a post-result parameter sweep.

## Preserve the original objective

The target remains useful 5,000-drone browser computation. Neither positive-term count savings nor oracle-assisted small-state accuracy establishes runtime, browser scalability, or closed-loop accuracy. Do not advertise timing of the oracle proposal as avoided work. A future speed gate must begin from the same raw input, count selection, coefficient work, proof, serialization, and fallback costs, and beat the strongest accepted exact comparator on disjoint small-N holdout before extrapolation.

A native approximate solver with offline independent verification is a legitimate separate research branch. It does not silently satisfy Q-current's per-query candidate bounds, tolerance decision, and admission/partition/cap provenance. Changing that interface requires an explicit contract decision.

## Source basis and scope

Desk reading only: `research/m31-current-bound-design-2026-10-16/ADOPTED-DESIGN.md` (10,420 bytes; SHA256 702d64e84c3fc12fdc9e85cb59abf4dd00e8df010647e1567a47eed49ee5387c) and `research/m31-normalizer-replication-2026-10-17/source/baseline/loads.cjs` (5,348 bytes; SHA256 c3fa665a8512ad0c9a73f964b26014c3ad329ee73b68589a61404a3d54ab8a4b). Pins are inherited from the prior review, not newly rehashed here. No new numerical inputs/results/references were read; no scientific imports, tests, execution, allocation, or frozen-source changes were made.
