# Independent mathematical review: bounded source omission

Date: 2026-10-16. **Static derivation and source inspection only.** No module imports, case generation, geometry evaluations, fields, roots, tests or benchmarks were run. The derivations below are for exact real arithmetic unless an explicitly stated numerical allowance is added. They are not a floating-point certification or physical validation.

## Disposition

The receiver Lipschitz constant `L=f0/(3*vi0)`, the uniform signed roll/pitch bound `2*a*L*B`, and the proposed center-derived source envelope are mathematically valid under the assumptions listed below. The strict near-domain and support branches in the inspected candidate follow the required order. The main outstanding qualification is numerical: nextUp on the final bound and its accumulated total does not prove that all earlier geometry/profile operations enclosed their exact values. A finite empirical challenge may test the declared margins; it must not be called a universal conservative floating-point certificate.

## 1. Receiver response: root, monotonicity and sharp global Lipschitz constant

Fix `f0>0`, `rho>0`, `A>0` and `vi0=sqrt(f0/(2*rho*A))>0`. For nonnegative scalar inflow U, define alpha=U/vi0 and the positive root x of

`g(x,alpha)=x^3+alpha*x−1=0`.

For alpha>=0, g(0)=-1 and g(1)=alpha. It is strictly increasing on positive x, so there is exactly one root in(0,1]. At alpha=0 the root is1. The derivative at every root is `3*x^2+alpha>0`, so implicit differentiation is valid, including the one-sided derivative at alpha=0:

`dx/dalpha=−x/(3*x^2+alpha)`.

At a root, `alpha=1/x−x^2`, hence

`|dx/dalpha|=x^2/(1+2*x^3)`.

The derivative of this last expression with respect to x is

`2*x*(1−x^3)/(1+2*x^3)^2 >= 0` for0<x<=1.

Its maximum is therefore1/3 at x=1. With f(U)=f0*x(U/vi0),

`−f0/(3*vi0) <= df/dU < 0`,

and the mean-value theorem gives `|f(U1)−f(U2)|<=L*|U1−U2|` for all finite U1,U2>=0, with **L=f0/(3*vi0)**. The constant is sharp as a global bound because equality is approached for arbitrarily small inflow differences at U=0. It is usually loose at large inflow.

If omitted nonnegative source terms sum to E_k at rotor k, then U_retained=U_full−E_k>=0. Therefore

`0<=delta_f[k]=f(U_retained)−f(U_full)<=L*E_k`.

Required assumptions: the same positive nominal f0 and receiver law in both calculations; fixed poses/axes; linear addition of nonnegative scalar source terms; no source-strength feedback, motor update or compensating control after omission. For unequal nominal motor thrusts, use each rotor's own L_k. At f0=0, f is identically0 but the displayed formula for L is undefined; handle that case separately. Negative inflow, a different overlap rule or a different actuator law is outside this derivation.

This proves the exact cubic response, not the monotonicity or error bound of a fixed-iteration floating-point Newton implementation. The latter still needs its frozen residual/root comparison and numerical allowances.

## 2. Signed body moment bound

For rotor order(++),(-+),(--),(+-), the body moments are

`tauX=a*(f[0]+f[1]−f[2]−f[3])`,

`tauY=a*(−f[0]+f[1]+f[2]−f[3])`.

Let `0<=delta_f[k]<=b_k`. The correct signed intervals are

`delta_tauX in [−a*(b_2+b_3), a*(b_0+b_1)]`,

`delta_tauY in [−a*(b_0+b_3), a*(b_1+b_2)]`,

and `delta_T in [0,sum(b_k)]`.

A uniform source envelope gives E_k<=B and b_k=L*B. Thus

`0<=delta_T<=4*L*B`,

`|delta_tauX|<=2*a*L*B`, `|delta_tauY|<=2*a*L*B`.

The factor2a is justified by the one-sided rotor-thrust errors. Applying an unsigned triangle inequality to all four signed terms would give the looser4a bound. Conversely, assuming common-mode errors or cancellation would be unjustified: all four omitted inflows need not be equal.

The component bound is sharp for the independent interval information: setting the two positive-lever rotor errors to b and the two negative-lever errors to0 reaches2ab. The two component maxima cannot generally occur simultaneously. In fact, let A=delta_f[0]−delta_f[2] and C=delta_f[1]−delta_f[3]. Then `(delta_tauX,delta_tauY)=a*(A+C,C−A)`, with |A|,|C|<=b, so

`sqrt(delta_tauX^2+delta_tauY^2)<=2*a*b`.

This sharper joint norm bound is optional; the proposed component gates remain valid. Modeled yaw stays at nominal zero, rather than the drag-moment component of the effective-thrust wrench.

In exact arithmetic, world force error equals receiver axis times delta_T. World moment error equals the same fixed body-to-world map applied to the body moment error. With unnormalized numerical quaternions, use the actual axis/map norms; do not assume a perfectly norm-preserving rotation. Gravity and gyroscopic terms are not part of these load errors.

### Two-sided numerical reserve

If total per-rotor arithmetic uncertainty is ±eta in the *difference* between candidate and reference, the valid interval becomes `delta_f[k] in [−eta, L*B+eta]`. Then

`delta_T in [−4*eta, 4*L*B+4*eta]`,

`|delta_tauX|,|delta_tauY| <= 2*a*L*B + 4*a*eta`.

The reserve is **4a*eta**, not2a*eta. The inspected Bcap expression subtracts the correct4a*eta from each moment target, and4eta from the thrust target. Eta must cover the combined field/accumulation/response comparison error, including both paths where appropriate; a tolerance for one root is not automatically such a bound. A prior finite reference comparison does not prove eta for unseen inputs.

## 3. Geometry envelope without assuming exact quaternion normalization

Let c=p_source−p_receiver, source axis n, and actual receiving rotor offset v_k. Choose l_i so that `||v_k||<=l_i` for all four rotors. Let s=||n|| and P=I−n*n^T. Define

`d0=c·n`, `r0=||P*c||`.

For each rotor, d_k=(c−v_k)·n and r_k=||P*(c−v_k)||. Cauchy–Schwarz gives

`d0−s*l_i <= d_k <= d0+s*l_i`.

P is symmetric, with eigenvalues1,1,1−s², hence its operator norm is `pNorm=max(1,|1−s²|)`. The reverse triangle inequality gives

`r_k>=max(0,r0−pNorm*l_i)`.

These statements remain valid when n is not unit and P is not an orthogonal projector. Replacing s or pNorm by1 without justification can break the proof. Likewise, the ideal arm length sqrt(2)*a cannot replace the maximum actual rotated offset for an unnormalized quaternion. A1e-10 input norm tolerance permits more geometric distortion than a generic1e-12m pad alone necessarily covers. The inspected candidate explicitly computes the actual offset norms and axis norms, which addresses this real-arithmetic assumption.

There remains a floating-point detail: production constructs a world rotor point by rounding p_receiver+rotatedOffset, then rounds sourcePoint−rotorPoint. That is not literally identical to evaluating c−v_k with exact arithmetic on separately rounded intermediates. Coordinate addition/subtraction, dot products and norms must be included in the numerical margin or interval analysis. A large common translation is a useful challenge because cancellation/absolute spacing can change arithmetic without changing ideal relative geometry.

## 4. Far-wake source upper bound

Use d−,d+,r− from the preceding enclosure, widened as specified by the numerical contract. Once domain ambiguity is handled, intersect with the far branch:

`dL=max(d−,2.5D)`, `dH=min(d+,2.5m)`.

For a nonempty interval and d<2.5m, write the source term as

`w(d,r)=projection*vi0*C(d)*F(d)*Q(r/H(d))`,

where `C(d)=10.11/(d/D+5.817)`, `H(d)=0.07668*(d+5.817D)`, and `Q(q)=radialFade(q)/(1+(sqrt(2)−1)*q²)^2`.

On d>=2.5D, C is positive/decreasing, H is positive/increasing, and downstream fade F is nonnegative/nonincreasing. For q>=0, the radial profile has derivative `−4*(sqrt(2)−1)*q/(1+(sqrt(2)−1)*q²)^3<=0`; radial fade is also nonnegative/nonincreasing. Their product Q is nonincreasing. Since `r_k/H(d_k)>=r−/H(dH)`, each retained rotor term is bounded by

`projection*vi0*C(dL)*F(dL)*Q(r−/H(dH))`.

The projection is constant across the receiver's four rotor points, nonnegative, and must remain the actual source/receiver-axis dot product clamped only below at0. No bound of1 is assumed. The full wake need not decrease with downstream distance; this proof bounds its separate nonnegative factors, and their different maximizing points intentionally make the result potentially loose.

Summing valid upper bounds over omitted sources gives a bound for each receiving rotor's omitted inflow because the scalar superposition is linear and nonnegative. It is a bound on omitted contributions, not evidence that their physical superposition is correct.

## 5. Strict branch edges and domain fallback

- d+<=0 proves every rotor takes the nonpositive-downstream zero branch. Equality is zero.
- d−>=2.5m proves every rotor takes the downstream-cutoff zero branch. Equality is zero.
- The interval can enter the near slab exactly when d+>0 and d−<2.5D. If also r−<0.15m, an exception is possible and must be resolved by exact four-rotor geometry before omission.
- r−>=0.15m excludes the near-radius exception; equality is safe because the original exception uses strict `<0.15`.
- After near-domain safety is established, d+<2.5D proves there is no far contribution. **d+=2.5D cannot be culled**: the far branch includes its lower boundary.
- If the far interval reduces to the single point dL=dH=2.5D, treat it as potentially nonzero. Do not use dL>=dH as a generic empty-interval test. The upper2.5m endpoint is excluded, but including it for the maximum half-width is a conservative overestimate.
- qLower>=3 proves radial cutoff for every far rotor; equality is zero under the original `radial>=3*halfWidth` branch. A computed lower ratio rounded upward across3 would invalidate this argument, so outward/numerical treatment matters at this edge.
- A zero projection does not remove a prior near-wake exception. Check near-domain safety before projection or radial-source pruning. For exactly unit axes both within20° of vertical, projection is actually positive; zero-projection cases should not be mislabeled attainable valid20° unit-quaternion fixtures.
- Preserve the strict center-distance<3m candidate rule. Source-center culling outside this radius is part of the unchanged model, not part of the new approximation's error budget.

Source-first exact fallback may discover a different first invalid tuple from the original rotor-first traversal. Domain-reject agreement is valid if claimed; exact exception ordering requires additional matching logic. The candidate must not claim both without checking.

## 6. Static candidate observations and challenges for the driver review

Read `research/m31-source-omission-2026-10-16/source/candidate.cjs` and `cases.cjs` without importing them. The candidate implements the stated n-norm/radial-operator envelope, domain-before-pruning order, signed-budget reserve, ascending-ID greedy rule, same-pass exact retained terms and rebuilt-per-query decisions. The matched M path skips bound-only preprocessing; this is a fair control for whether omission offsets its added overhead. nextUp increments the positive Float64 bit pattern correctly, handles zero by the least positive value, and upward accumulation encloses an ordinary finite addition. At the largest finite input its result is infinity; callers must not misdescribe this as a finite-output guarantee.

nextUp is applied only after an ordinary computed source bound. It does not retrospectively make dL/dH/rLower, axis norms, square roots, fade arithmetic or their products outward-rounded. The explicit margins remain engineering assumptions checked by the experiment. A rounded expanded cubic fade should not be assumed nonnegative merely from its real formula; inspect/guard finite evaluated terms or include a justified numerical deviation. The candidate's f0-derived vi0 and original field's hover expression are algebraically equal but may have different binary64 evaluation grouping, so exact bitwise reference equality is not presumed.

The initial `multipleWeak` fixture used sources(±0.7,±0.2,1) and did not construct positive support. The revised source inspected before exposure uses(±0.31,±0.12,1). For each source, its nearest receiving rotor has radial distance `sqrt((0.31−0.028)^2+(0.12−0.028)^2)<0.3m`, while `3H(1)>0.3m`; its downstream coordinate is1m and its projection is1. Thus each of the four sources has at least one strictly positive supported contribution at the central receiver in the ideal construction. Same-height source-to-source pairs have downstream0 and cannot trigger the near-domain error. This repairs the positive-support coverage gap without promising a particular omitted set, near-capacity sum or exhausted budget. Near-radius equality being agreement-only remains appropriate because decimal construction and subtraction can straddle the exact binary branch.

The actual protocol inspected on2026-10-16 specifies24actual fixtures,152attempted field queries and700000shape-charged receiver solves. It correctly separates exact mathematical derivations from frozen empirical floating-point allowances, body-budget acceptance from descriptive world errors, and correctness from cost. The inspected PREFLIGHT-RESOLUTIONS.md explicitly supersedes the original DESIGN-REVIEW proposal's16-fixture/120-call/650000receiver counts and guaranteed budget-exhaustion wording. It also discloses that the fixed fixtures do not include huge common translations, so world-coordinate addition/cancellation at such magnitudes is not challenged. These scope dispositions are resolved, with no request for more tests after the matrix is fixed.

This review clears the mathematics and inspected candidate for the stated finite numerical challenge. It does not itself clear driver completeness, evidence persistence, resource enforcement, freeze provenance, or launch; an independent evidence reviewer handles those. No campaign execution or empirical passing result is asserted.
