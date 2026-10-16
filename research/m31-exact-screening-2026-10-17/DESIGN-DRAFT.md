# Exact current-state spatial screening: prospective next checkpoint

Parent published checkpoint9b5fa707c1727f37caa04d812aa41cfc4f211ae2 (resultb35f3a2fea26b41b5a1b2bfdd2fe88e691080e57). Previous turn made progress: complete small-group current-state load certificates were independently checked and publicly verified. All previous scientific/display allocations are closed. This fresh package is source-only planning; it currently authorizes no numerical execution.

## Purpose and common comparison

Qualify an exact source hierarchy against a complete pair calculation under the same prepared-operands M-current load contract, before a later full-cost scalability comparison. This advances the original5,000-drone local3D Boids/dynamics/mutual-aerodynamics accuracy–computation goal; neither finite static qualification nor a saved3D view completes it.

Both methods start from raw current state and pay their own complete preparation/global validation. Both use one shared prepared-operand pair kernel, identical coefficient arithmetic, native proposal recipe and root/load certificate arithmetic. The old implementation's repeated preparation inside every pair must not be present only in the baseline. A separately authored oracle validates the new prepared-pair adaptation. Preserve all branch precedence, positive-source ordering and actual positive-term cap. Build and proof work are charged to the hierarchical method; no free prepared tree, baseline answer or admission oracle.

The qualification contract needs input/prepared identities, model status, compact complete source partitions, positive coefficients, fixed candidate bits, enclosing rotor/collective/world-force/world-moment loads and exact1e-8 normalized error decisions. Exact legacy zero-reason arrays are not required. Both methods have identical output/scientific obligations. A skipped set must be proved entirely zero in the original guarded model. No positive omission or approximate kernel is allocated.

## Proposed global guard certificate and fallback

After validating every drone, form exact rational bounding boxes of all prepared centers, axes and all prepared receiver rotor points. Prove all center component differences <=257 and center squared-distance upper <=512². With D=source-center-box minus receiver-point-box, prove max-absolute each displacement component <=258. Enclose H=D dot source-axis-box and prove max-absolute H<=1024. Enclose E=D-H*axis-box and prove sum_k maxabs(E_k)²<=2048². All operations are exact rational interval operations over supplied dyadics, not rounded native bounds or ideal-unit-axis assumptions.

A passed global certificate discharges these magnitude guards for every nonself pair, including those not center-eligible. It does not discharge preparation, near-field rejection, width, caps, positive ordering or term budget. If any global box proof is insufficient, the hierarchy method falls back to complete scalar pair evaluation for the scene; the fallback pays its attempted preparation/build/proof work and retains the reason. Insufficient proof is not a physical/model rejection. This preserves the high-priority guard behavior. The complete baseline always evaluates every nonself pair after global preparation succeeds.

## Deterministic tree

Source universe is all stable-ID drones. Build a median binary tree on prepared centers. At each node choose largest exact center span, ties x then y then z; sort by that exact coordinate, ties ascending stable ID; split floor(n/2). Leaf capacity8. Node IDs are preorder. Each node stores exact center/axis bounds and source membership/count; internal children partition it exactly. Bounds and membership are rebuilt from the current input each call. The checker independently reconstructs the same tree. No cached/stale input.

For each receiver/rotor, traverse from root. A node containing self may be safely skipped only with a proved-zero condition for all members; the certified source universe still excludes self. At a leaf, call the shared scalar pair kernel for every nonself member. Keep evaluated singleton outcomes; after all queries, collect positive singleton edges in receiver/rotor/input-source order before the common proposal/certificate calculation, avoiding method-dependent positive summation order. Full traversal continues after scalar refusal, so complete status accounting remains checkable.

## Conservative proposed node-zero rules

Only when the global guard certificate passes, use exact rational node intervals. Let C=node center box, A=node axis box, receiver center c, prepared rotor point p, and receiver axis b. Center distance lower is the sum of coordinate interval absolute-minimum squares for C-c. D=C-p; H=D dot A; E=D-H*A; R2_lower=sum coordinate absolute-minimum squares. Width interval W=(spread*(H/Dconst-origin))*Dconst uses frozen exact constants. This preserves the actual near-unit axes and interval dependence conservatively.

Try rules in a fixed declared order:

1. neighbor: center-distance lower >=neighbor². Every pair reaches exact neighbor zero after global center guards.
2. upstream: H.upper<=0. Pairs outside center support are already zero; eligible pairs reach upstream zero after discharged guards.
3. down-cut: H.lower>=downCut. Same mixed-support reasoning.
4. near-outside: H.upper<minDown*Dconst AND R2_lower>=nearRad². Pairs with H<=0 are upstream zero; positive H lies strictly in the near slab and outside its rejected radius, hence zero. This rule does not call projection early.
5. radial: H.lower>=minDown*Dconst AND W.lower>0 AND R2_lower>=radCut²*W.upper². Eligible downstream pairs below the cutoff pass near rejection and width, then radial zero; larger H is down-cut zero.

If no rule proves zero, descend or evaluate a leaf. Do not use projection screening in this first implementation, do not accept uncertain zero, do not skip possible cap rejection for active pairs. Tree arithmetic overflow/invalidity gives named fallback/refusal under frozen rules, never a zero result.

## Qualification design still to freeze

Fresh finite scenes must include multicolumn dense and sparse3D groups, rotated unequal-force groups, permutation, node-boundary cases, near/cap/order rejection, global invalidity and global-proof failure with complete fallback. No original closed suite is rerun. Proposed maximum64drones, fixed source leaf size8, unchanged48×54 native proposal and96-bit certificate; independent192-bit coefficient/source and128-bisection topological reference.

Before any numerical evaluation, freeze exact scenes, expected output schema, coverage/guard/tree evidence, controls, iteration and wall/RSS/output limits. Candidate controls must target missing source subtree, false zero proof, wrong tree membership/bounds, stale input, altered positive coefficient, load/root/error corruption and scene coverage; use proved witnesses and the same core validator. Distinguish model admission, proof success, fallback, certificate validity and tolerance.

This first experiment may report proved-zero coverage and scalar evaluation counts as algorithmic work evidence. They are not wall-clock speedup, total-cost savings, physical accuracy or novelty. A later timed allocation must include preparation/build/admission/traversal/scalar evaluation/solve/certificate/output and fallback consistently across methods. Historical timed queries already excluded dense diagnostic tensors.

Proposed fresh budgets: parent<=24 inherited content reads; each of the existing3reviewers<=16 inherited files plus this package, no external operations. Sole kernel<=300s, sole checker<=600s, sampled RSS<=1GiB, aggregate result/current-private-log budget<=64MiB,64KiB report reserve; source freeze/publication/exact-commit remote verification before either run. These are drafts until final preregistration. Up to2display-only QA attempts<=60s; new Three.js saved tree/group diagnostic plus clearly separate historical airflow-off replay link. No paid service/install/contact/submission, no new agents.
