# Static challenge of the four-rotor coupled contract

This additive note scrutinizes the parent's proposed mathematical contract. No code or model was executed, no data were evaluated, and no repository source was edited. The per-rotor contract below replaces the earlier note's proposed averaged-inflow/total-disk numerical question; its geometric ordering and counterexample derivations remain separate.

**Finding:** the proposed ordinary sup-norm contraction certificate is valid. There is also a stronger guarantee for this exact fixed-coefficient contract: in log coordinates, the map is globally Lipschitz with constant at most one half. Thus its cyclic fixed point exists and is unique even when the proposed ordinary bound is at least one. This conclusion depends on the assumptions and domains below; it establishes no physical validity, novelty, or identification with fixed PWM or shaft power.

## Domain and source hypothesis

For vehicle `i` and each of its four retained receiver rotors `r`, require

`f0_ir > 0`, `T0_i = sum_r f0_ir > 0`, `w_ir = f0_ir/T0_i`,

with fixed finite `rho>0`, disk area `A>0`, and hover reference `mg>0`. Merely requiring `T0_i>0` is insufficient: a zero individual `f0_ir` makes the proposed coefficient denominator undefined. To keep all four original roots, the finite numerical question must restrict every nominal rotor thrust to be positive. An extension to inactive rotors would need an explicit zero-force rule and omitted inactive root; all-off vehicles with `T0_i=0` also need a separate representation. Negative nominal thrust is outside this contract.

Let `K_irj` be fixed, finite, nonnegative scalar inflow coefficients, in speed units, at receiver rotor `r`, with `K_iri=0`. A zero coefficient must denote an admitted zero interaction. An unsupported near-field rejection cannot silently become a zero coefficient. Axes, rotor offsets, support, receiver projection and aggregation by summing admitted source inflows are frozen during the solve.

Define

`a_irj = K_irj sqrt(T0_j/mg) / sqrt(f0_ir/(2 rho A))`,

`alpha_ir(y) = sum_j a_irj y_j`,

`x_ir(y) = g(alpha_ir(y))`,

`F_i(y) = sqrt(sum_r w_ir x_ir(y))`,

where `g(alpha)` is the unique positive root of `x^3 + alpha x - 1 = 0` for `alpha>=0`.

All `a_irj` and `alpha_ir` are dimensionless. The root exists uniquely because the cubic is continuous and strictly increasing on the positive half-line, is negative at zero and nonnegative at one. Thus `0<g(alpha)<=1` for every finite `alpha>=0`. It follows that `F` is continuous and maps `[0,1]^N` into `(0,1]^N`.

At a fixed point, `T_i = sum_r f0_ir x_ir = T0_i y_i^2`. The proposed source amplitude is algebraically consistent with a total-effective-thrust scaling:

`sqrt(T0_j/mg) y_j = sqrt(T_j/mg)`.

That equality does not validate the source hypothesis. Scaling the old fixed hover field by total effective thrust assumes its shape, support and axis remain unchanged, and discards effects of unequal source-rotor loading on the field. Four distinct receiver inflows and roots are retained; they are never replaced by their average or by a single total-disk receiver root. The original ideal-power receiver law remains an explicitly assumed local closure.

Baseline-admitted `K` alone does not prove that every scaled trial state satisfies the original runtime speed cap. If that cap or another rejection rule is retained, certify it over the whole solve domain or handle rejection outside this mathematical contract. Discontinuous clipping, state-dependent support, or coefficients that depend on thrust are not covered by the proofs below. The source amplitude on the cube is bounded by `sqrt(T0_j/mg)`; this provides a direct prospective guard check.

## The proposed ordinary contraction bound is correct

Implicit differentiation, using `alpha=(1-x^3)/x`, gives

`g'(alpha) = -x/(3x^2+alpha) = -x^2/(1+2x^3)`.

For `h(alpha)=sqrt(g(alpha))`,

`|h'(alpha)| = x^(3/2) / [2(1+2x^3)]`.

Put `t=x^(3/2)` in `(0,1]`. The function `t/[2(1+2t^2)]` has its maximum at `t=1/sqrt(2)`, giving exactly

`|h'(alpha)| <= 1/(4 sqrt(2))`.

Let `s_ir=sum_j a_irj`. The reverse triangle inequality for the weighted Euclidean norm gives, for any `y,z` in the cube,

`|F_i(y)-F_i(z)| <= (1/(4 sqrt(2))) sqrt(sum_r w_ir s_ir^2) ||y-z||_infinity`.

Therefore both the tighter certificate

`L = max_i sqrt(sum_r w_ir s_ir^2)/(4 sqrt(2))`

and the proposed conservative certificate

`L_max = max_(i,r) s_ir/(4 sqrt(2))`

are valid, with `L<=L_max`. If the chosen certified bound is below one, Banach's theorem gives a unique fixed point, convergence of Picard iteration from any cube point, and

`||y-y_star||_infinity <= epsilon/(1-L)`,

where `epsilon=||y-F(y)||_infinity` is the residual against the exact mathematical map. If the map evaluation has certified sup-norm error `eta_F`, replace the numerator by `computed_epsilon + eta_F`. A rounded numerical estimate of `L` must be bounded conservatively before using `1-L` as an error certificate.

## Stronger log-space contraction for this exact contract

For `z_i<=0`, define `G(z)=log(F(exp(z)))`, componentwise. This is well-defined because `F_i>0`, and it maps the closed complete set `(-infinity,0]^N` into itself. No evaluation outside the original thrust-ratio cube is needed.

Write `S_i=sum_r w_ir x_ir=F_i^2`. Every partial derivative of `F_i` is nonpositive. Applying the chain rule and summing absolute derivatives gives

`sum_j |partial G_i/partial z_j|`

`= [sum_r w_ir (-g'(alpha_ir)) alpha_ir] / (2 S_i)`

`= [sum_r w_ir x_ir (1-x_ir^3)/(1+2x_ir^3)] / [2 sum_r w_ir x_ir]`

`<= 1/2`.

This remains valid when an `alpha_ir` is zero: its contribution to the numerator is zero. The derivative bound along a straight segment of log states yields

`||G(z)-G(v)||_infinity <= (1/2) ||z-v||_infinity`.

Consequently the fixed point is unique and exists for every finite nonnegative coefficient array in the stated contract, independent of whether the ordinary `L` is below one. There cannot be an additional fixed point on a zero-coordinate boundary because every `F_i` is strictly positive. The no-self-term restriction is respected; the mathematical log bound does not require it.

Picard iteration of `F` is conjugate to Picard iteration of `G`. From a strictly positive cube state it converges in log norm with factor at most one half. Starting with any zero coordinates requires just one exact `F` evaluation before log coordinates are defined. This is a mathematical convergence statement; numerical root accuracy, underflow and guard admission still need explicit handling.

For a positive candidate, let `r_log=||log(y)-log(F(y))||_infinity`. Then

`D := ||log(y)-log(y_star)||_infinity <= 2 r_log`.

If the evaluated map has a certified log error `eta_logF`, the usable bound is

`D <= 2 (computed_r_log + eta_logF)`.

Thus failure of the ordinary `L<1` certificate is not evidence of multiple solutions or solver infeasibility for this particular model. The log certificate is available instead.

## Per-rotor force error and consistency checks

The physical-unit quantity returned by each retained receiver root is `f_ir(y)=f0_ir g(alpha_ir(y))`. It must be distinguished from the provisional source total `T0_i y_i^2` before convergence.

For an ordinary state-error bound `delta>=||y-y_star||_infinity`, the sharper derivative inequality

`|g'(alpha)| = x^2/(1+2x^3) <= 1/3`

holds on `0<x<=1` (its maximum is at `x=1`). Therefore

`|f_ir(y)-f_ir(y_star)| <= (f0_ir/3) s_ir delta`.

With a certified root-evaluation error `eta_x,ir`, add `f0_ir eta_x,ir` to that bound. Summing these absolute rotor bounds bounds the error of the reconstructed total receiver thrust. The provisional source total instead obeys

`|T0_i y_i^2 - T0_i y_star_i^2| <= 2 T0_i delta`.

Even before reference to the solution, the force/source consistency mismatch is exactly

`|T0_i y_i^2 - sum_r f_ir(y)| = T0_i |y_i^2-F_i(y)^2|`

`<= 2 T0_i |y_i-F_i(y)|`.

A solver should not label source totals and reconstructed rotor-force totals as identical until this mismatch is controlled.

The log certificate offers a relative per-rotor bound without dividing by `1-L`. The sum of absolute log derivatives of each rotor root is

`sum_j |partial log(x_ir)/partial log(y_j)|`

`= (1-x_ir^3)/(1+2x_ir^3) <= 1`.

Hence `exp(-D) <= f_ir(y)/f_ir(y_star) <= exp(D)`. In particular,

`|f_ir(y)-f_ir(y_star)|/f_ir(y_star) <= exp(D)-1`.

This same multiplicative interval holds for the sum of the recomputed rotor forces. For the provisional source total `T0_i y_i^2`, the interval is instead `exp(-2D)` to `exp(2D)`. A certified log error `eta_logx,ir` in the reported root adds to `D` in the per-rotor exponent. A positive enclosing root bracket can certify that log error; a cubic residual alone is not automatically a force or log-error bound. The independently checked residual must include inner-root evaluation error rather than treating it as exact.

## Implication for the distinct ladder-plus-hexagon question

The downstream geometric DAG condition from the earlier note still permits a direct descending-height pass: each vehicle computes its four local inflows and four unique roots once its upstream source thrusts are known, then sums those forces to set its source amplitude. This claim needs a fully admitted coefficient set, including explicit handling of near-field rejection.

On a cyclic hexagon, the four-root system remains implicit, but this specific assumed contract now has an analytical existence, uniqueness and Picard-convergence guarantee in log coordinates. A later finite comparison can therefore ask whether the exact implementation reaches a predeclared **per-rotor force-error certificate**, and at what bounded work, for a frozen ladder and hexagon. It should retain the four roots, use independent residual checking, report source/receiver consistency, and keep inner-root errors in the certificate. Geometry, rotor frames, nominal forces, coefficient admission, initialization, tolerances and compute limits must be frozen before that separate allocation. This note performs and allocates no numerical experiment.
