# Independent mathematical challenge: predicted-root polynomial defect

Date: 2026-10-16. Repository-relative package: `research/m31-root-defect-planning-2026-10-16`.

This review examines `PROSPECTIVE-SCOPE.md`, `DERIVATION-DRAFT.md`, and the inherited `research/m31-coupled-solve-2026-10-16/review/CONTRACT-CHALLENGE.md`. It is an analytical source review only. No code or scientific module was imported or executed, no target values or controls were evaluated, no coefficient or numerical bound was computed, no source was retrieved, and no numerical allocation was opened.

## Disposition

**The proposed exact-real enclosure is mathematically valid under the stated fixed nonnegative-coefficient contract.** No algebraic inequality or body-moment sign error was found. The local polynomial-defect factor and the global source-consistency factor are both needed for an arbitrary predicted rotor vector; the draft correctly includes both.

This establishes a conditional corollary of the inherited contraction result. It establishes neither a validated floating-point certificate nor useful tightness, runtime economy, a current-geometry approximation, physical validity, or novelty. Adoption of the derivation does not authorize a numerical test. Any subsequent numerical question still requires a separate prospective decision and freeze.

Two wording clarifications should be retained in the final derivation: make the inherited whole-domain admission/cap requirement explicit, and use “no cubic-root solves” rather than an unqualified “no roots” statement because the source construction and norms still require square-root arithmetic. Additional implementation limits below are conditions on any future certificate, not evidence that one currently exists.

## Assumptions required for the conclusion

For a finite vehicle/rotor population, require every nominal rotor force to be finite and strictly positive. For each vehicle, `S0_i = sum_r f0_ir` and `w_ir = f0_ir/S0_i` are exact positive quantities with `sum_r w_ir = 1`. Individual zero/negative loads are outside the inherited four-root contract; positive total load alone is insufficient.

The complete coefficient array must be finite, nonnegative, and fixed with respect to the unknown loads. It must represent the same current geometry, rotor ownership/order, current nominal motor quantities, axes, projections, and support definitions as the mathematical model being certified. For the inherited coefficient definition, current nominal loads enter the coefficient scaling as well as the weights. Updating only the weights while silently retaining incompatible coefficients does not satisfy this assumption.

An admitted zero interaction remains distinct from an unsupported/rejected interaction. A rejection must not become a zero coefficient. Discontinuous clipping, load-dependent coefficients, changing support, or changes of source-field shape are not covered by the contraction argument.

The inherited contract explicitly warns that baseline coefficient admission does not certify a runtime speed cap over all source amplitudes. To carry the bound over to a model that retains such guards, their validity must be established over the required domain—most directly the whole source cube used by the inherited theorem—or by a separately justified invariant-domain argument. Admission at the provisional candidate alone does not establish admission of the unknown fixed point or all states used in the proof. Without that connection, the derivation still bounds the frozen algebraic coefficient problem, but cannot be advertised as a certificate for a guarded model that may reject elsewhere.

Every proposed ratio must satisfy `0 < xhat_ir <= 1` before invoking this version of the theorem. Construct the exact provisional source from those ratios and the current weights:

`yhat_i = sqrt(sum_r w_ir * xhat_ir)`.

It follows that `0 < yhat_i <= 1`. A stale cached source, an unweighted rotor average, or an independently rounded source treated as mathematically exact does not satisfy this identity automatically. The previously rejected secant ratios above one remain outside this proposed certificate's declared candidate domain; the derivation does not authorize clipping or retroactive reclassification.

## Independent verification of the enclosure

For fixed finite `alpha >= 0`, define `P(x) = x^3 + alpha*x` on `x > 0`. Its unique positive unit-level root is `g(alpha)`, and

`d log P(x) / d log x = (3*x^3 + alpha*x)/(x^3 + alpha*x)`.

The denominator is positive and the derivative lies in `[1,3]`, including `alpha = 0`. Integrating with respect to `log x` between `xhat` and `g(alpha)` therefore gives

`|log xhat - log g(alpha)| <= |log P(xhat)|`.

No assumption that the candidate already solves a cubic is used. No logarithm of `alpha` is required, so admitted zero-coefficient rows cause no singularity in this argument.

At the exact candidate-derived source, set `alpha_hat_ir = sum_j a_irj*yhat_j`, `p_ir = P_ir(xhat_ir)`, and `xres_ir = g(alpha_hat_ir)`. Each `p_ir` is strictly positive in exact arithmetic. With `k_ir = max(p_ir, 1/p_ir)` and `K = max_ir k_ir`,

`xres_ir/k_ir <= xhat_ir <= k_ir*xres_ir`,

and consequently the same inequalities hold using the larger common factor `K`. Summing with the same positive current weights gives

`(1/K) * sum_r w_ir*xres_ir <= sum_r w_ir*xhat_ir <= K * sum_r w_ir*xres_ir`.

Taking square roots identifies the middle term with `yhat_i` and the outer sums with `F_i(yhat)`, yielding

`||log yhat - log F(yhat)||_infinity <= (1/2)*log K`.

The inherited map `G(z) = log F(exp z)` is a self-map and a contraction of factor at most `1/2` on the closed negative orthant of finite log coordinates. Its a posteriori residual estimate is

`||z - zstar||_infinity <= ||z-G(z)||_infinity/(1-1/2)`.

Applying it at `z = log yhat` proves

`||log yhat - log ystar||_infinity <= log K`.

For each rotor, the inherited log-root derivative row sum is

`sum_j |partial log x_ir / partial log y_j| = (1-x_ir^3)/(1+2*x_ir^3) <= 1`.

The straight segment between the two source log states stays in the domain. Thus

`|log xres_ir - log xstar_ir| <= log K`.

Combining this source error with the local polynomial defect proves

`|log xhat_ir - log xstar_ir| <= log k_ir + log K`,

and hence

`xhat_ir/(k_ir*K) <= xstar_ir <= min(1, xhat_ir*k_ir*K)`.

The intersection with the known exact upper bound one is justified; it is an enclosure operation, not clipping the candidate. The interval is nonempty under the stated candidate domain because its lower endpoint is at most `xhat_ir`, and its upper endpoint is at least `xhat_ir`. When all defects are exactly one, the exact source consistency and cubic equations imply the unique joint solution. This is a symbolic limiting-case check, not an executed control.

As an independent consistency check, composing the log-root map (Lipschitz constant at most one) with the log of the weighted source construction (constant at most one half) gives a rotor-space map with constant at most one half. Its global residual estimate yields `|log xhat_ir-log xstar_ir| <= 2*log K`. The proposed local factor `k_ir*K <= K^2` is consistent with and can refine that global bound. None of these arguments implies the resulting interval is tight enough to decide a useful load threshold.

## Rotor, collective-force, and body-moment propagation

For an enclosing exact interval `[l_ir,u_ir]` and a common current positive nominal force, the candidate-minus-solution thrust difference is enclosed by

`D_ir = [f0_ir*(xhat_ir-u_ir), f0_ir*(xhat_ir-l_ir)]`.

The endpoint order is correct because multiplication by `f0_ir > 0` preserves order. The maximum of the two endpoint magnitudes bounds absolute rotor error. These differences also equal differences of aerodynamic corrections when the same nominal thrust is subtracted from candidate and solution.

Let `[L_i,U_i] = sum_r D_ir` by interval addition and let `c_i` be the fixed current body-z column used for both world-force evaluations. The collective world-force error has the form `c_i*s_i` for `s_i` in that summed interval, so

`||force_error_i||_2 <= ||c_i||_2 * max(|L_i|, |U_i|)`.

For an exact unit quaternion and its exact rotation, `||c_i||_2 = 1`. A unit-norm tolerance on a saved binary64 quaternion does not make this equality exact. A future certificate must enclose the declared rotation/column arithmetic and its norm or account for normalization/attitude uncertainty. Using the actual column norm certifies that specified linear map; it does not certify an unknown physical attitude.

For fixed body-frame rotor coordinates `(x_r,y_r)`, the model's moment error is

`roll = sum_r y_r * D_ir`,

`pitch = -sum_r x_r * D_ir`.

Signed interval multiplication must reverse endpoint roles when its scalar is negative. With coordinate magnitude bounds `B_roll` and `B_pitch`, the conservative norm bound `sqrt(B_roll^2+B_pitch^2)` is sound. It remains conservative when the coordinate extrema are incompatible because they depend on the same rotor errors; losing that dependency can loosen the bound but cannot make this box-norm bound unsound.

The zero yaw component is an assumption of this aerodynamic correction model, with common nominal yaw canceling. It is not a conclusion that actual rotor/yaw physics has zero error. The result covers the specified shared-axis thrust and fixed-lever-arm model, not a general wrench with tilted rotor axes or additional aerodynamic moments.

Normalization by `mg/4`, `mg`, and `mgR`, with positive `mg` and `R = sqrt(2)*0.028 m`, preserves the inequalities. A numerical upper bound also needs conservative treatment of these denominators and the square root. No interval bound being valid implies it falls below a screening threshold.

## Numerical enclosure conditions

The draft correctly separates exact-real validity from rounded computation. A future implementation must enclose the exact `p_ir` produced by the stated model, including current coefficient construction or a clearly declared exact assembled-coefficient interpretation; positive-weight sums and their denominator; candidate-derived source square roots; alpha sums; products and cubics. Enclosing a polynomial evaluated at an unrelated rounded source is not enough unless the source-consistency error is also rigorously covered.

If `p_ir` lies in `[L_ir,U_ir]` with `0 < L_ir <= U_ir`, then

`kbar_ir = max(1, U_ir, 1/L_ir)`

is a safe upper bound for `k_ir` when computed outward. The reciprocal is controlled by the positive lower endpoint, not by `1/U_ir`. Let `Kbar = max_ir kbar_ir`. An outward lower evaluation of `xhat/(kbar*Kbar)` and outward upper evaluation of `min(1,xhat*kbar*Kbar)` then enclose the exact solution. Every subsequent signed interval operation, rotation-column norm, moment norm, and normalization must preserve enclosure. Nearest rounding alone supplies no such guarantee.

A nonpositive computed lower endpoint for `p`, underflow that destroys positivity, overflow, nonfinite input, failed coefficient admission, or invalid candidate must produce a named unqualified result under the proposed rule. Failure to obtain a positive numerical lower bound does not prove the exact polynomial is nonpositive; it means the numerical certificate was not established. Silently inserting zero, dropping interactions, changing support, or treating an overflowed quantity as a successful finite bound would invalidate the claim.

An exact-rational reference can treat specified binary64 inputs as exact rationals and bound square roots with rational/integer-square-root methods. If its inputs are already rounded assembled coefficients, it certifies that assembled coefficient model. It does not retroactively enclose the geometric/coefficient construction, its transcendental operations, measurement uncertainty, or an intended physical field. The target mathematical object and which construction errors are covered must be frozen before any reference comparison. No such reference or candidate implementation was inspected or exercised here.

The phrase “root-free” should consistently mean avoiding cubic-root evaluations or a new joint-root solve. Constructing `yhat`, enclosing norms, and normalizing moments still involve square roots and arithmetic. A safe exact-real formula is not automatically a cheap operational algorithm or a runtime certificate.

## Usefulness and next-stage boundary

The proposed check still needs the complete current coefficient set, a current source-amplitude construction, an alpha pass, and conservative interval/load arithmetic. It cannot use a stale matrix to certify a changed current matrix unless a separate coefficient-perturbation enclosure is supplied. The present proof supplies no temporal-geometry error term, intermediate-time guarantee, predictor-driven trajectory result, or threshold success evidence.

This mathematical review does not independently validate any inherited timing share or transfer a cost percentage across implementations. Avoiding cubic-root evaluations does not by itself establish that the measured bottleneck is reduced. Usefulness, tightness, rejection frequency, and operational cost remain prospective questions. Existing exact-real equations and the inherited contraction theorem are the basis of the result; no novelty or literature-priority conclusion follows.

## Reviewed identities

| Source document | SHA-256 |
| --- | --- |
| `PROSPECTIVE-SCOPE.md` | `128c18139ebfd217b5e15718c58280c0dff0b71b5193f2ee47251708526debca` |
| `DERIVATION-DRAFT.md` | `744aa89915f09558081600edfec39c2e28dfa70461ef1ea6b35ae11fb8ec276c` |
| Inherited `m31-coupled-solve-2026-10-16/review/CONTRACT-CHALLENGE.md` | `39fd45bf0070c76a40251f1519898ca7ca169978966d3bcfb052f66df82b4476` |
