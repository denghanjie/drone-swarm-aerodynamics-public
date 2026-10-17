# Independent spatial exact-reference bridge: source feasibility

2026-10-17. Source-only inspection; no scientific imports, fixtures, execution or frozen-package edits.

**A reusable exact hierarchy already exists, but the current independent reference does not use it to save oracle work.** A bounded dispatcher/coverage refactor is credible. Simply enabling a hierarchy flag, importing the filtered producer, or lifting a drone-count constant is not. No source evidence establishes that the result would be affordable at5,000.

## What the fresh reference actually computes

`fresh-transfer/source/reference.py` calls `semantic.regenerate_scene` once for each of four moving controls and two N=64 targets, using `RawWordHelper` only to interpret raw binary64 words. The wrapper enforces cap180; the inherited scene helper independently enforces216. Neither authorizes5,000.

`regenerate_scene`:

1. Reconstructs constant/prepared binary64 words and validates every drone; converts centers, source axes and actual rounded rotor points to exact rationals.
2. Builds a global guard and, if it passes, an exact median tree.
3. Nevertheless invokes `pair-reference.py:oracle_case` for **every** nonself receiver/rotor/source combination, retaining both a full `pairs` list and `lookup` dictionary. Each oracle call reparses both raw rows, prepares and validates both drones again, then applies exact branch predicates and fixed192 interval construction. Existing rotation caches do not remove all this repetition and are not a5,000-drone scaling argument.
4. Applies rejection/uncertainty/order/cap precedence, computes independent roots with192-bit coefficients/source boxes and128 bisections per endpoint, and propagates signed rotor/collective/force/moment boxes.
5. Finally constructs **both** complete and hierarchy assembly plans. The hierarchy plan checks every proposed omitted member against the already-computed oracle and expands coverage lists. Thus the tree currently verifies candidate work; it does not accelerate the independent scene oracle.

All functions in filter-cost's semantic-reference.py are text-identical to the current fresh helper. Reusing that file alone changes nothing. Its CJS `methods.cjs` does perform tree-first traversal, prepared-operand scalar queries and optional binary64 zero filtering, but its positive path uses the producer's fixed96 machinery. Importing it would neither preserve the independent Python192 reference nor provide independent evidence for itself.

## Minimum useful change

Add a **new isolated Python scene dispatcher**, retaining the frozen old all-pair helper as the small-corpus comparison oracle. Reuse the already reviewed Python rational box operations, `global_guard`, `reconstruct_tree`, `zero_rule`,192 quantization, root bisection and signed load propagation.

Prepare/validate once at scene level. Apply exact node-zero proofs before scalar evaluation. Descend uncertain nodes, call the unchanged192 `oracle_case` on residual nonself leaf members, and retain only scalar outcomes plus explicit group-zero proof records. This first version changes orchestration and coverage, not positive arithmetic. It still repeats preparation in residual oracle calls; that cost must remain disclosed.

A separately reviewed, small subsequent extraction can expose the Python oracle's **prepared-operand suffix**, preserving exact expression/branch order while avoiding repeated raw decode/preparation. The existing CJS prepared-pair interface is a useful design precedent, not code to substitute for the independent arithmetic. Lazy same-argument caches for source beta and receiver-rotor nu, or sharing an identical center predicate across four rotors, are further exact reuse opportunities. Cache results/errors at their original use point: eager evaluation can turn an otherwise zero pair into a premature refusal. Do not bundle these optimizations with the first coverage change unless their source/equality review is explicit.

The output/checker schema must also change. Current fresh serialization requires a dense per-pair record and `evaluatedPairs==plannedPairs`; its checker walks those records. New fields must distinguish logical pairs, node-proved zeros, scalar evaluations and complete coverage. Keep the same positive coefficient/root/load boxes and strict1e-8 comparison law. Do not expand every proved zero back into a dictionary/list merely to satisfy the old schema; that would retain quadratic memory and much quadratic work.

## Concrete proof and coverage invariants

- **Same model operands.** Exact boxes contain the actual admitted prepared binary64 centers, axes and rounded `center+offset` points. Keep rounded constant graph values. Do not normalize near-unit axes to exact unit length, replace the residual by an orthogonal-projection shortcut, or use ideal unrounded rotor points.
- **Guard precedence.** The existing global proof bounds all relevant exact expressions: center components<=257, center norm²<=512², rotor displacement components<=258, absolute down<=1024, residual norm²<=2048². A false proof selects unchanged complete scalar fallback; it is not a model rejection or permission to skip. A bounded large attempt may stop as resource/unresolved rather than finish that fallback, but cannot label it admitted. Administrative exceptions remain failures.
- **Existing five zero rules.** With `h` the interval of displacement·source-axis, `r²_lo` the lower bound of the actual squared residual, and `w=(spread*(h/D-origin))*D`: neighbor lower distance²>=neighbor²; h.upper<=0; h.lower>=downCut; h.upper<minDown*D AND r²_lo>=nearRad²; or h.lower>=minDown*D, w.lower>0 AND r²_lo>=radCut²*w.upper². Preserve all strict/non-strict boundaries. These rules prove zero; they cannot suppress unsupported near-field or invalid/scaled-cap cases. Unproved nodes must descend.
- **Tree identity.** Unique stable IDs; exact largest-span split with xyz ties, coordinate then ID order, floor midpoint, leaf capacity8 and deterministic preorder/left-first traversal. Every child range partitions its parent in a single permutation. Self may be included conservatively in a proof box but is excluded from pair membership/counts.
- **Compact coverage, not counts alone.** For each receiver/rotor, terminals must be a disjoint complete partition of permutation positions except that receiver's one position. Verify ranges and a unique inverse permutation, not only `zeroPairs+scalarPairs=4N(N−1)`: a duplicate and omission can cancel numerically. Use node ranges/counts with one self adjustment; avoid constructing every zero member list and flattened `covered` list as the current planner does. Scalar leaf outcomes must be unique and ordered. Small validation can expand the partition to compare every member.
- **Proof label versus scalar branch.** A node's zero rule is a proof reason, not necessarily every member's first scalar zero branch. For example, a group upstream proof can cover a member that individually exits at neighbor first. Preserve this distinction in the schema. For actually evaluated scalar pairs, retain exact status/branch. If the optional scalar filter is later introduced, it must also prove every earlier branch false before asserting a specific zero branch.
- **All positive/rejected/undecidable work remains.** Reconstruct canonical receiver/rotor/source order before selecting first rejection, then uncertainty, then backward positive edge and positive-term cap. Stable-ID conversion must not confuse input indices, tree positions and IDs. Admit only with complete coverage and every positive source earlier in the exact descending-height/stable-ID order. Do not early-return a partial tree walk as a complete scene. The existing recursive graph DFS is another shape hazard at5,000; use the proven forward-rank property for admitted graphs or a reviewed iterative graph check, not an unchecked recursion-limit increase.
- **Independent arithmetic unchanged.** Positive coefficients use the same outward192 quantization; sources192; roots128 endpoint bisections; signed loads preserve axis and lever signs. Zero proofs remove only zero contributions. The positive map and source order therefore remain the same. Precision/refinement and positive-term caps are not adaptive rescue knobs.

The existing scalar `zero-filter.cjs` offers further reuse only after this dispatcher is qualified. It uses outward neighboring-binary64 endpoints, no square root, same-word preparation and exact fallback for ambiguity/overflow/underflow-related refusal. It already preserves scalar branch priority. Its speed and coverage after tree pruning are workload-dependent. Keeping the independent reference exact-rational-first avoids importing the producer's fast filter as a trusted oracle. A later independently implemented/proved filter would need its own primitive and false-zero controls.

## Bounded small-corpus validation, for a later explicit allocation

Freeze exactly24 existing scenes: the entire18-scene exact-screening corpus (maximum64), the four unchanged moving controls, and both fresh64 targets. This retains singleton, dense/sparse, tilt, ID permutation, cutoff equality, near/cap/order/global-invalid and global-proof-fallback cases. No new seed or favorable subset. The specifications account for79,048 planned logical nonself rotor-source pairs per variant before global refusals; this is a workload bound, not executed science.

Run the frozen full oracle and new dispatcher once each per scene, at most160,000 scalar-oracle calls across both variants, with no browser, simulation, timing repetitions or5,000-state evaluation. Compare raw/prepared words, global outcomes/canonical witnesses, positive IDs and coefficient endpoints, roots and all signed load boxes exactly where the unchanged arithmetic promises identity. Independently expand every pruned terminal in this small test and require every corresponding full-oracle status zero; preserve proof-rule/scalar-branch distinction. Require the strict native-load checker verdicts remain unchanged on the two fresh records.

Retain14 arithmetic fixtures and four existing load-law corruptions. Add exactly six prebound coverage corruptions: false positive-to-zero proof, dropped source, duplicate/omitted ranges with equal totals, forged node bound, guard-bypass zero, and index/ID substitution. Bind witnesses to the fixed corpus before publication; missing witnesses fail, not trigger searches. Run one saved-only review. A tentative ceiling is600 s validation,180 s review,900 s total,32 MiB/file and256 MiB combined new evidence/logs, with bounded cleanup and no cap expansion/retry. Source preparation does not allocate this plan; do not squeeze it into the remaining time before03:00UTC without a separate completed freeze and allocation.

## Likely5,000 bottlenecks and priority limit

Complete enumeration would mean99,980,000 rotor-source pairs and enormous Python object/JSON overhead. Tree-first coverage can eliminate much of that in extended geometry, but no worst-case subquadratic guarantee follows: dense groups, loose tilted-axis boxes or failed global guards can force full scalar work. Exact Fraction bounding, sorting, repeated leaf preparation and positive coefficients remain expensive; the saved native≈68,000 positive terms are not measured exact leaf/filter counts for the new traversal. Current normalizer/cap ambiguities and interval widths can still leave a state unresolved.

At5,000 there are20,000 rotor roots; two128-step endpoint bisections imply an upper workload of5.12million rational cubic iterations before zero-alpha shortcuts, plus source square roots and signed load propagation. Compact sparse output is necessary but does not remove that cost. The two-million-positive-term ceiling is an administrative bound, not an affordable target. No runtime, memory or success claim is made from these counts. A later size increase must be a new contract with measured small-state work/memory and a justified finite reservation, not a literal cap edit.

Keep this bridge to one source-feasibility decision and one bounded small validation cycle before reassessing value. Parent's verified Neural-Swarm2 reading (arXiv2012.05457v2, journal DOI10.1109/TRO.2021.3098436) makes the physical gap concrete:34/67g vehicles required PWM/voltage calibration and motor delay identification; trajectory-derived vertical-force labels, relative velocity and multi-neighbor effects mattered; performance degraded at larger neighbor counts. It does not validate our27g four-rotor torque law or5,000 swarms. Code/data documentation is not proof the external data are accessible, licensed or compatible.

Therefore numerical enclosure work should enable a trustworthy comparison, not indefinitely displace a parallel evidence-admission decision: identify compatible measured quantities/calibration/splits and whether velocity/multi-neighbor observations can test the current law. Do not collect or fit anything under this note. If the physical comparison remains unsupported, label subsequent computations as conditional-model engineering; a tighter arithmetic tolerance cannot repair model error.

## Source anchors

Repository root: `REPOSITORY`.

- Fresh `source/reference.py`; `semantic-reference.py:158–215,378–605,644–728`; `pair-reference.py:345–391,471–557`.
- Filter-cost `source/{methods,tree,boxes,pair-prepared,zero-filter,binary64-interval}.cjs`; its semantic helper functions match fresh exactly by source comparison.
- Exact-screening `review/SOURCE-MATHEMATICS.md`, `PROTOCOL.md`, `MILESTONE-SUMMARY.md`, `source/spec.json`; filter-design `review/NUMERICAL-DESIGN-AUDIT.md` and protocol.
- `research/m31-next-direction-2026-10-17/LITERATURE-UPDATE.md`, preserving Neural-Swarm2's verified version/read scope and physical/data-access limits.

Only source/text reads, structural spec inspection and document writing/hashing were performed. No scientific module was imported or evaluated.
