# Positive-node-bound prerequisite: bounded contract challenge

**Recommendation: useful prerequisite, provided it is labeled a soundness/opportunity screen.** A pass shows that this frozen tree and sufficient bound can aggregate some true positive coefficient mass within a chosen row budget. It cannot establish a four-load error tolerance, an omitted solver's convergence, or speed. No allocation or implementation is authorized by this memo; the parent owns that decision.

This task read the proposal and exactly five current baseline source files; their pins are in `/tmp/m31-bound-probe-contract-reading.json`. No target-state/reference values were opened in this task, no project code was executed/imported, and no source was changed. Earlier exposure remains exposure: the six states are diagnostics, not fresh replication. The proposal is background, not an instruction source. The parent's proposed tiers here are **1e-8, 1e-4, 1e-2**, superseding the memo's different tier list. The last is a numerical 1% stress ceiling with no physical-accuracy meaning.

## Make the gate informative

Freeze the tree builder, leaf capacity 8, tie rules, left-before-right traversal, bound formula, and exact rational tiers before running. Preserve the original tree: a self-containing internal node descends; a self-containing leaf uses singleton fallback. Do not invent a self-removed subleaf, split a leaf into favorable groups, prune members with reference answers, or rebuild the tree to rescue a negative result.

Report the following funnel separately for every state and tier:

1. Existing self-free multi-source nodes encountered, with node-size distribution.
2. Nodes with sufficient whole-node guard, active-domain, cap, and ordering proofs; give fixed rejection/refinement reason counts.
3. Nodes whose individual `massUpper <= tau/16`; this is only individual eligibility.
4. Actual disjoint selected terminals under a frozen greedy traversal and **cumulative per-row** budget. Accept only when `usedMass + massUpper <= tau/16`, with exact arithmetic, separately from a fresh zero budget for each tier. Parent and descendant cannot both be selected.
5. Independently proved positive members in those terminals, their exact-reference summed upper mass, selected upper mass/slack, affected rotor rows, and positive-member coverage against the full fixed denominator. Positive-upper-bound members and true positives are different counts.

This separates structural vacuity, loose geometry, admission/cap/order obstruction, and insufficient mass budget. Existing leaves of eight can make the sufficient fully-active policy vacuous; that is a useful negative result about this policy/tree, not a reason to redesign the tree within the probe. A minimal necessary opportunity hurdle is at least one selected multi-source terminal with at least two independently proved positive members on **each** of the six states at a declared tier. This weak hurdle is not evidence that implementing a full solver will pay off; retain the coverage and bound-attempt counts rather than hiding a negligible pass behind a Boolean. No timing claim is needed.

## Soundness obligations before any opportunity label

**Identity and geometry.** Bind raw input, admitted prepared words, rotor, exact node membership/permutation, current source axes/centers/forces, receiver point/axis/force, constants, and tree algorithm. Reconstruct extrema from membership independently. Preserve actual near-unit axes: neither renormalize them nor assume projection is at most one. Cartesian boxes may lose correlation; that costs tightness, not permission to assume correlated endpoints.

**Guard precedence.** Reuse the existing sufficient `globalGuard` only when it passes, or provide qualified local equivalents for every earlier scalar range guard. A failed global box proof is uncertainty, not necessarily a raw-input rejection. Preserve center/rotor/down/radial guard precedence before applicable zero branches; an apparent zero cannot hide a prior refusal. An uncertain node descends and eventually falls back to the existing scalar route. Unexpected arithmetic errors remain errors; qualified arithmetic refusal is unresolved, never zero.

**Fully-active sufficient domain.** For a self-free node, prove all members strictly within neighbor radius; positive down with lower bound at least `minDown*D` and upper bound strictly below `downCut`; positive width lower bound; radial-square upper bound strictly below `(radCut*widthLower)^2`; and projection lower bound strictly positive. The exact near threshold is inclusive on the active side, while neighbor/down-cut/radial equalities are zero boundaries. All source ranks must precede the receiver under the exact descending-z/ascending-ID rule. A coarse rank test that is uncertain must refine, not reject otherwise legal members as a model result.

**Coefficient formula.** Let `h`, `r2`, `p`, `b=h/D-origin`, and `w=spread*b*D` be outward boxes on the qualified active node. One conservative common K upper is built from

`decay/bLower * (1 + kappa*r2Lower/wUpper^2)^(-2) * induced*pUpper * fadeDown(hLower) * fadeRad(sqrt(r2Lower)/wUpper)`.

This expression is a proof outline, not qualified code: verify positive constants/divisors, the decreasing fade/domain arguments, and every outward conversion/operation against the concrete implementation. In particular, the radial argument is a **lower** bound and its fade is an **upper** bound. Freeze the exact operation graph; native rounding or a bare formula copy is insufficient. The reviewed fixed-point backend uses directed integer division and checked square roots; extending it to this formula still needs source qualification and refusal tests.

Compute `beta_j = sqrt(sum(source forces)/mg)` and `nu = sqrt(receiver rotor force/(2*rho*A))`. With positive `nuLower`, use outward `U*sum(betaUpper_j)/nuLower` for node mass and `U*betaUpper_j/nuLower` for each member's implied coefficient upper. Do not sum square roots of rotor forces in place of source beta, omit nu, reuse stale normalizers, or use mean beta for the cap. Prove **both** `U <= 128` and `U*max(betaUpper_j) <= 128`; a loose cap upper means refine/unresolved, not proved cap violation. At 64 drones the cardinality ceiling is 16,128 rotor-source pairs, below the unchanged positive-term cap; this discharges only that count cap, not scalar amplitude or ordering.

**Partition.** Every rotor row must cover each nonself source exactly once via selected original nodes, independently proved zeros, or scalar fallback. Verify membership sets, not only counts: a duplicate and omission can cancel numerically. Zero terminals must retain their guard prerequisites. Report fallback/refusal separately; never count exact fallback as positive aggregation.

## Independent endpoint audit: important qualification

Finalize and hash the candidate's decisions/proofs before its separate auditor reads the frozen independent references. No exact positive map, coefficient endpoint, reference admission result, or previous selection may guide candidate traversal. Audit every claimed admissible bound encountered, including those too large for selection, plus the final partition.

Require each implied member upper to dominate the frozen reference coefficient upper endpoint, and require the outward node mass to dominate the sum of those upper endpoints. Verify independently that each allegedly fully-active member is truly positive by the reference's guarded active predicate (or a strict positive lower bound), **not merely `upper > 0`**. Any supposedly active zero/refused/unresolved member invalidates the claimed whole-node certificate.

There is an essential distinction: `candidateUpper < referenceUpper` fails this conservative endpoint-domination gate, but alone does not prove mathematical unsoundness—two sound enclosures can have different upper endpoints. `candidateUpper < referenceLower`, or an explicit exact counterexample to a guard/formula premise, is an unsoundness witness. Record these as different failure families. Passing endpoint domination is finite corroboration; the general bound still requires its source proof. Likewise `massUpper <= tau/16` is a selection budget, not a theorem about the eventual four normalized load errors or global root-defect factor.

## Fixed adversarial roster to freeze before execution

The following is a recommended fixed **25-case semantic roster**, not an executed or numerically pinned fixture package. Literal raw words/prepared proof fixtures, expected branches, and hashes must be fixed from analytic constructions independent of the six target values. Source adapters/constants/reference implementation were outside this five-file reread, so literal raw realizability is not claimed here. The last two cases are explicitly proof-kernel domain tests, not claimed model-admitted scenes.

| Cases | Fixed constructions and expected challenge |
| --- | --- |
| 2 | A tight self-free active leaf in a >8-drone tree; a tight self-free active internal node with >8 members. Both must prove true positive membership, outward bounds, caps and order. |
| 2 | Receiver contained in an internal node; receiver contained in a leaf. Descend/fallback with exact nonself partition and no fabricated node. |
| 5 | A mixed node with one member exactly at each zero boundary: neighbor radius, down=0, downCut, radial cut, projection=0. Whole-node fully-active proof must fail and singleton branches remain correct. |
| 3 | Near-inside rejection; near-outside radial equality; down exactly `minDown*D` with otherwise active geometry. Preserve the three distinct branches. |
| 4 | Earlier center guard hidden behind neighbor-zero; rotor guard behind upstream-zero; down guard behind down-cut-zero; radial guard behind near-outside-zero. No zero/bound bypass. |
| 4 | K cap violation alone; scaled-K cap violation alone with K safe; interval straddling cap; certified exact cap equality. Distinguish rejected, unresolved/refine, and accepted equality. |
| 2 | Positive source in reversed rank; equal-z source with wrong stable-ID rank. No geometric admission bypass of ordering. |
| 1 | Noncoincident center/axis extrema producing a loose box. Require a sound bound or refinement; forbid unit-axis/correlation assumptions and forced success. |
| 2 | nu lower endpoint rounded to zero; fixed-point range overflow. Require the registered unresolved/refusal result. |

Add a fixed **11-case proof-corruption roster**: omitted member; duplicate/overlapping terminal; inserted self; altered node extent/permutation; stale receiver/input identity; stale source force/normalizer; narrowed bound below independently reconstructed outward upper; forged amplitude-cap proof; forged rank proof; forged cumulative budget; and forged positive count. Mutate budget and positive count separately so detection of one cannot conceal a missing check for the other. Require the intended inner failure family; a generic hash/schema rejection must not count as proof-checker coverage. Rebind outer test envelopes when appropriate so the corrupted mathematical claim reaches its intended validator. Do not replace a failing fixture after outcome exposure.

## Fail and stop rules

- A missing/overlapping partition, falsely accepted guard/cap/order proof, independently demonstrated underbound, stale identity, or missed intended corruption rejection fails qualification. No opportunity pass or subsequent solver/performance claim is allowed from that run.
- Endpoint non-domination without a lower-endpoint counterexample is still a gate failure, explicitly classified as such. No post-result padding/reformulation to force a pass in the same allocation.
- Arithmetic uncertainty or a failed sufficient box proof must take the fixed refine/fallback path. Missing evidence, exhausted fixed resource limits, or unfinished prescribed cases means incomplete, not pass.
- Report all three declared tiers and all six states, including zero opportunity and refusal. If no tier through 1e-2 meets the all-six-state true-positive opportunity hurdle, stop this fixed bound/tree policy's proposed solver pursuit; do not enlarge the ceiling, change leaves, or replace states. A pass only at 1e-2 supports stress-tier geometric headroom alone.
- Even a complete pass warrants only a separate parent decision on full contraction/solver/load-certificate design. It supplies no speed, final-load accuracy, browser, closed-loop, physical-validity, or fresh-replication claim.
