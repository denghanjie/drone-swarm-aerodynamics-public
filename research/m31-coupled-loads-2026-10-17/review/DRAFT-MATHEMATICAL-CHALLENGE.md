# Source-only draft mathematical challenge

This note challenges `PROTOCOL-DRAFT.md` before candidate or checker execution. It records the mathematical obligations sent to the parent and independent checker author. It is not final implementation approval. No scientific code was imported or evaluated, no prior suite rerun, and no external operation performed.

## Conditional root-defect argument

The inherited result applies to complete fixed finite nonnegative coefficients and strictly positive nominal rotor forces. With exact `w_ir=f_ir/sum_r f_ir`, the weights sum exactly to one. For a recorded candidate satisfying `0<xhat_ir<=1`, its model source is exactly `yhat_i=sqrt(sum_r w_ir*xhat_ir)`. Native proposal sums, weights, midpoint coefficients, and sources are not these mathematical identities unless independently enclosed from the recorded operands.

The positive-root map `g(alpha)` for `x^3+alpha*x=1` is defined for every finite `alpha>=0`. Its log sensitivity to source amplitudes is at most one, and the coupled source map has log contraction at most one half. The polynomial logarithmic derivative lies in `[1,3]`. Therefore the adopted local factor `k_ir=max(p_ir,1/p_ir)`, global `K=max k_ir`, and enclosure `xhat/(k_ir*K) <= xstar <= min(1,xhat*k_ir*K)` remain valid for complete current rows. The parent must include both the local and global factors; retaining only a local residual factor would omit source inconsistency.

An outward defect interval `[L,U]` with `L>0` permits `kbar=max(1,U,1/L)` and `Kbar=max kbar`. The reciprocal uses the lower defect endpoint. The final lower root endpoint must be rounded downward, its upper endpoint upward, and intersection with the known upper bound one is sound. This intersection does not authorize clipping an invalid proposed candidate into the theorem's domain. Failure to prove a positive defect lower bound is a certificate refusal, not a proof that the exact positive defect is zero.

The theorem does not need acyclic geometry. Descending exact prepared-center z, then ascending stable integer ID, is a restriction of this operational/reference solver. Whole-domain pair admission over `0<y<=1` remains necessary before the algebraic solution is interpreted as a solution of the guarded current model.

## Challenge to the inherited body-moment wording

The inherited adopted corollary writes body roll as `sum y_r D_r` and pitch as `-sum x_r D_r`. These formulas are the special case with a body-frame lever `(x_r,y_r,0)` and force direction `(0,0,1)`. They do not by themselves establish the new world-moment formula, do not imply zero world-z moment, and do not permit replacing a saved near-unit axis by an ideal unit vector.

The new contract instead supplies exact dyadic prepared lever arms `o_ir` and actual prepared axis `a_i`. Define the fixed exact vector

`v_ir = o_ir × a_i`.

Then the shared-axis model's world moment is exactly

`M_i(x) = sum_r v_ir f_ir x_ir`.

For solution brackets `[l_ir,u_ir]`, set

`D_ir = f_ir * [xhat_ir-u_ir, xhat_ir-l_ir]`.

Since `f_ir>0`, this interval contains candidate-minus-solution rotor thrust. Componentwise signed interval multiplication and addition yield

`Delta M_ik in sum_r v_irk * D_ir`.

For each coordinate interval `[L_ik,U_ik]`, let `b_ik=max(abs(L_ik),abs(U_ik))`. The conservative Euclidean error bound is `sqrt(sum_k b_ik^2)`. Dependence between rotor errors or coordinates can make this box bound loose, but cannot invalidate it. Compute all three world coordinates and preserve the cross-product order; `axis × offset` reverses moment signs.

This proof requires neither exact unit length nor exact orthogonality of the supplied axis/offsets. It certifies the declared linear map. In exact arithmetic the moment is perpendicular to the supplied axis because each `o×a` is, but its world-z component need not vanish. No physical yaw conclusion follows. Lever arms are the separately prepared offsets, not `roundedRotorPoint - center`; the latter can differ after preparation rounding and would change the target model.

For collective error, sum the signed `D_ir`. World-force error is `a_i * sum D_ir`; either a full signed coordinate enclosure or `||a_i||*maxAbs(sum D_ir)` is sound. The latter must use the actual supplied axis norm, not one. The inherited body-frame roll/pitch formulas may be mentioned only as a special case of this explicit signed-linear derivation.

## Complete membership and priority obligations

1. Freeze the representation and range of stable integer IDs so uniqueness and equality are exact; a JavaScript `Number` representation requires safe-integer validation. Self exclusion comes from ID equality, with duplicate IDs rejected before they can remove real nonself interactions.
2. Freeze the empty-scene policy. Every drone, including an isolated one, needs global raw/prepared validation before self exclusion. Clarify whether globally invalid scenes retain zero pair records or full pair records; `4*N*(N-1)` complete coverage is required for globally prepared scenes. Do not claim enumeration completeness for an intentionally unenumerated invalid scene.
3. For globally valid scenes, retain all `(receiver input index, rotor, source input index)` nonself pairs in the prescribed order. Every positive row contribution uses the same current coefficients, exact nominal values, and recorded candidate-derived source. No rejected or unresolved interaction may become zero.
4. Count and order-check every `status=positive` pair, including intervals with lower coefficient endpoint zero. Its exact active-branch classification supplies positivity. A nonpositive interval lower endpoint does not erase an active interaction.
5. The first scene refusal selected by priority does not excuse validating later pair records. In particular, a permitted stress refusal must not hide another unexplained unresolved code elsewhere in that scene. Stress allowances are a prospective record-level restriction, not a blanket acceptance of arbitrary failures on named scenes.
6. Count actual positive interactions. The source-reviewed `>2,000,000` limit is an operational resource refusal, separate from domain rejection. A finite suite below the threshold supplies no empirical overflow-boundary coverage.
7. Stable IDs preserve ownership under input permutation. Input-order summation and native candidate arithmetic can produce different candidate bits or interval widths; the model identities and fixed acceptance obligations must remain bound to IDs. Do not infer or require bytewise permutation invariance unless separately specified.

## Output identities, norms, and tolerance decisions

The four categories should be explicit: rotor, collective, world force, and world moment. Normalize rotor absolute error by exact `mg/4`, collective absolute and world-force Euclidean errors by exact `mg`, and world-moment Euclidean error by exact `mg*R`. Here `mg` and `R` are the frozen supplied dyadics; multiplication/division and all square roots need outward treatment. Recomputing ideal `sqrt(2)*arm` or a different native-rounded normalization silently changes the declared units.

Candidate load identities refer to exact loads formed from the recorded binary64 `xhat`, supplied positive forces, and supplied geometry. Either emit those exact identities or rigorous enclosing intervals. A native-rounded candidate load cannot be silently substituted as the exact reference point for a signed error certificate. Candidate load generation and certificate evaluation must use identical ownership, geometry, nominal values, and candidate bits.

Per-drone maxima and scene maxima must conservatively aggregate the four normalized categories. Define `toleranceAchieved` from the certified upper endpoints and the frozen tolerance; valid but loose certificates remain explicit tolerance failures. Independent reference containment and tolerance achievement are different conclusions. A fixed finite reference uncertainty does not license guessed branch, root, or containment decisions.

## Topological-reference conditions

Every positive source must be earlier in the exact frozen order. For admitted scenes, induction on this order encloses the actual joint solution: interval source values enclose predecessor values, a complete nonnegative sum encloses each `alpha`, and `g(alpha)` decreases with `alpha`. Thus a root lower bound comes from the upper alpha endpoint and an upper root bound from the lower alpha endpoint. Exact rational polynomial comparisons maintain bisection brackets. When `alpha=0`, the exact root is one; an exact unit-level polynomial comparison may likewise collapse a bracket to its exact rational root.

Outward quantization of the independent geometric coefficient and source/root intervals preserves the original exact-real target. It must not redefine the coefficient as an interval midpoint or confuse a positive branch whose numerical lower bound is zero with an admitted zero. The checker should require returned candidate root/load certificates to contain the independent reference intervals while retaining any inability to establish that containment. The candidate's native 48-iteration/54-bisection proposal remains untrusted and must never consume reference roots.

## Pending implementation review

The algebraic extension is valid under these conditions. Final approval awaits the final protocol/model/contract, source candidate certificate and signed load arithmetic, and the independent reference sections. All draft corrections should remain prospective and preserved before the source freeze.
