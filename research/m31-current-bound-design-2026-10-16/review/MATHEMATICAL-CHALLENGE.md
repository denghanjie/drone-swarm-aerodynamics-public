# Independent mathematical challenge: current-geometry row enclosures

2026-10-16. Package under review: research/m31-current-bound-design-2026-10-16.

## Disposition and scope

The interval-box construction, common product upper bound, nonnegative node-aggregate bridge, and use of the inherited root-defect corollary are mathematically sound under the explicitly conditional exact-real contract. I found no algebraic counterexample to those statements. They do not yet constitute a certified implementation or a complete admission algorithm.

Adoption should retain explicit conditions on the numerical target, original branch precedence, global input validity, complete membership, whole-source-domain guards, exact current weights, and candidate consistency. The most important clarifications are listed below. Several are already identified as open gates by the draft; this review does not turn an acknowledged open gate into an observed failure.

This was a bounded desk review. I read ten content files in full: three files authored in the present checkpoint and seven inherited files. This is below fourteen even if all ten are conservatively counted against that cap. Filename listings and unsuccessful AGENTS.md existence checks read no additional content. The inventory at the end records the paths and hashes actually inspected. No target array, numerical result dataset, scientific import, evaluator, symbolic algebra program, numerical example, old campaign/reviewer, external source, or new agent was used. Shell activity was limited to listing, reading, hashing source/prose, and writing this review. Mathematical arguments below are reasoning, not executed experiments.

## 1. The exact target is a necessary premise, not a cosmetic choice

The draft correctly separates its geometric exact-real model from the inherited rounded coefficient model. Its active-branch simplifications are algebraically valid for the exact-real target: W(h) = spread * (h - origin * D) equals spread * (h/D - origin) * D when D is positive. The two radial ratios in the historical source also coincide in exact arithmetic. Reassociation does not establish their binary64 equivalence.

A later protocol must identify the actual constants, prepared source centers, receiver rotor points, source/receiver axes, and nominal forces. In particular, it must say whether constants such as D, induced, and sqrt2minus1 denote frozen supplied values or exact expressions. The historical source constructs several constants through rounded square roots and products. It forms each rotor point by a rounded center-plus-offset addition. Interpreting those operands as exact reals and doing a new exact sum does not automatically recover the historical rounded rotor point.

The target can consistently take specified prepared values as exact inputs, as the draft proposes. That leaves preparation outside the claim. Alternatively, preparation can be enclosed. Either route needs an explicit identity before evaluation. A certificate for geometric exact-real coefficients cannot be described as a certificate for the legacy assembled binary64 coefficients without a separately proved construction/branch bridge. Branch boundaries make this particularly consequential: changing the target can change support or rejection, not merely perturb a coefficient smoothly.

## 2. Interval geometry survives dependency and non-unit axes

For every member j, componentwise interval subtraction encloses d_j = c_j - p_ir. Interval multiplication and addition then enclose h_j = d_j dot a_j. The interval vector E = Delta - H * A encloses e_j = d_j - h_j * a_j even though h, d, and a are dependent. Reusing an interval occurrence as though it were independent enlarges the represented set; the actual dependent tuple remains in that set. No independence assumption is needed for inclusion.

For each component interval [l_k,u_k], the proposed b_k is the minimum possible absolute component and B_k the maximum. Thus b_k squared <= e_k squared <= B_k squared for every represented vector, and summation followed by the increasing nonnegative square root proves the proposed rL and rU. The bound can be wide when the component extrema cannot occur together. That is a tightness limitation, not a soundness defect.

With the actual fixed receiver axis, an enclosing dot-product interval [dL,dU] gives PL = max(0,dL) and PU = max(0,dU). If the receiver axis itself is uncertain, its interval must participate in that dot-product enclosure. One must not replace PU with one unless a separate bound establishes that value.

For non-unit source axes, e is not generally perpendicular to the axis. In fact, e dot a = h * (1 - norm(a) squared), and norm(e) squared = norm(d) squared - 2*h squared + h squared*norm(a) squared. Therefore the unit-axis identity norm(e) squared = norm(d) squared - h squared is unavailable. The draft's direct component enclosure avoids this error and preserves the formula actually being studied. Normalizing an axis or substituting an average axis would change that formula.

The statement that the algebra handles non-unit axes must not waive legacy input admission. The inspected preparation separately checks quaternion, axis, and rotor-offset properties within declared tolerances. Arbitrary finite non-unit axes can satisfy the mathematical enclosure argument while failing the legacy input contract. A final design should state both facts explicitly.

## 3. Product upper bound: valid, with strict domain qualifications

For admitted active members, h lies in [hL,hU], r lies in [rL,rU], and W is increasing and positive. Consequently W(hL) <= W(h) <= W(hU), so

    rL / W(hU) <= r/W(h) <= rU / W(hL).

The left side is qL and the right side qU. The axial inverse factor and down fade are nonincreasing in h on the stated domain. The radial attenuation and radial fade are nonincreasing in q >= 0. Projection is nonnegative and at most PU. Each selected factor is a nonnegative upper bound for the corresponding factor of every member, so their product is an upper bound. The extrema need not belong to one source. Correlations between h, r, projection, and source position do not invalidate multiplication of nonnegative upper bounds.

The fade derivative given in the draft is correct on its transition interval, and its constant outer pieces preserve nonnegativity and monotonicity. This requires start < end. A later implementation must freeze or validate those constant relationships, as well as positive D, spread, decay, induced, and kappa. No assertion about monotonicity of the complete kernel as a single function of h is required or implied: the radial ratio also changes with h.

Zero radial-support or zero-projection members may be included in an upper-bound node if they are otherwise admitted; zero <= U then covers them. A branch-unresolved member is different. The upper formula is not an authorization to evaluate an active expression through a preceding rejection.

The analogous lower product is sound only when its factors are lower bounds for every actual member and no member can be an admitted zero or rejected case. Strict positivity of that lower expression additionally needs PL > 0, a strictly positive down fade at hU, and a strictly positive radial fade at qU. In the stated constants this includes hU < downCut and qU < radCut. Even if every discrete member is positive, a loose box can have PL = 0 or qU >= radCut and yield only zero. The final note should distinguish necessary active membership from sufficient interval tests for a strictly positive common lower bound. Zero remains a valid fallback lower bound.

Floating endpoints must be directed consistently: rL and qL need lower enclosures, rU and qU upper enclosures, W(hL) a certified positive lower bound where used as a denominator, and W(hU) an upper bound where used for qL. Uncertain constants must be enclosed in the directions appropriate to each factor. Ordinary endpoint evaluation, including ordinary square roots or a native norm call without a proved error enclosure, does not establish those properties.

## 4. Admission is the main unresolved bridge

The draft's phrase finite geometry/normalization and admitted center bounds should be expanded or linked to a complete predicate. Finite alone does not discharge the inherited finite magnitude guards. Source inspection establishes this branch order:

1. Remove self interactions by identity. Global preparation/nominal validity remains a prerequisite for acceptance of the query.
2. For nonself center displacement, enforce finite center norm, center norm <= 512, and every component magnitude <= 257 before using the center-neighbor zero exit at norm >= neighbor.
3. For a center-eligible receiver rotor, enforce finite displacement and component magnitudes <= 258; then finite down coordinate with absolute value <= 1024.
4. Only then use down <= 0 or down >= downCut as admitted zero exits.
5. On the intervening down branch, enforce finite radial norm <= 2048 before testing near field. The unsupported condition is the conjunction 0 < h < minDown*D and r < nearRad. The same down slab with r >= nearRad is an admitted zero branch.
6. On the remaining branch, establish positive finite width before the radial-support zero exit; projection and speed checks follow at their original locations. Active speed must be finite, nonnegative, and <= 128, and projection finite.

Thus a projection interval bounded above by zero cannot bypass an unresolved near-field or radial validity test. A geometrically far source cannot bypass an earlier center guard. An interval that crosses a threshold is uncertainty; it is not evidence of rejection or acceptance. Original inclusive/strict endpoints also matter. The simple active formula assumes the stronger hL >= minDown*D and hU < downCut and does not by itself cover an arbitrary mixture spanning the lower slab or the down cutoff. Such a mixture needs an explicit branch-union proof or refinement.

The draft is appropriately conservative about refining unresolved cases. If an upper enclosure fails a cap, that establishes failure to certify from that enclosure, not an actual cap violation. A fallback/refinement result must preserve that distinction. Exact rejection reasons and counts may require resolving more members than a binary admitted/rejected proof, and can change the operational cost.

For the positive-term count guard, a safe sufficient test can sum retained positive terms and upper counts of possibly positive omitted members over all rotor rows. If this total is within the original 2,000,000 guard, the guard is discharged. If it exceeds the guard, refinement or exact counting may still establish acceptance. The upper count itself is not the actual positive count. Returning a successful omitted query while silently dropping this guard would change the legacy domain.

Descending-z/ascending-ID eligibility must be proved for every possibly positive edge if the operational solver contract is retained. A positive source-axis down coordinate does not imply a positive world-z separation for tilted axes or rotor offsets. Height ties must use the stated ID rule. The inherited log-contraction theorem itself permits cycles and does not require descending order. Ordering is a separate legacy solver/interface restriction; failing it does not refute the algebraic existence or uniqueness result.

## 5. Whole-source-domain cap checks and fixed coefficients

For the adopted positive-weight model, any rotor-ratio vector in (0,1] produces a source amplitude y_j in (0,1]. Therefore, for a fixed nonnegative K_irj <= U_irC,

    K_irj <= U_irC,
    K_irj * beta_j * y_j <= U_irC * max_(j in C) beta_j.

The two proposed <= 128 upper tests are sufficient to discharge the unscaled and scaled per-source term caps throughout the positive source cube. Their independence from the particular candidate is essential. Testing U times a candidate-specific amplitude aggregate alone would not prove this domain property. The same proof extends to the closed cube boundary for cap purposes, although the logarithmic proof uses positive coordinates.

This cap reasoning depends on all nominal rotor forces being strictly positive, exact totals being positive, exact weights summing to one, and beta being the current nominal scaling. Zero individual rotor force is not repaired by a positive vehicle total: the receiver normalization would be undefined. The nominal quantities enter coefficients as well as weights; updating one while retaining incompatible old values violates the contract.

The mathematical coefficients must be fixed independently of unknown loads. A hierarchy or aggregate may be chosen using the candidate without changing those underlying coefficients, provided its enclosure still contains the contraction of that same complete coefficient system. Replacing the physical shape/support with a candidate-dependent approximate matrix, or treating rejected values as zero, is outside this argument.

The per-term caps do not by themselves certify a floating implementation's aggregate, coefficient division by a small receiver normalization, or polynomial evaluation against overflow/underflow. All such operations need their own enclosure and named unqualified outcomes. In the exact finite-population real model, finite coefficients and positive normalization suffice for finite row sums; that fact is not a binary64 range guarantee.

## 6. The node aggregate bridge is a genuine conditional reduction

Let t_j = beta_j * yhat_j >= 0 for the single declared candidate. If every nonself member satisfies 0 <= K_irj <= U_irC, then multiplying by t_j and summing proves

    0 <= sum_(j in C) K_irj*t_j <= U_irC * sum_(j in C) t_j.

Dividing by the positive receiver normalization yields the proposed coefficient-contraction bound. Correlation of beta or yhat with node geometry is harmless because the inequality holds separately for every member. No statistical independence is asserted. An interval upper bound for B_C and a positive interval lower bound for the receiver normalization preserve the upper inequality when arithmetic is outward. A common lower shape bound requires the stronger conditions described above.

The row partition should explicitly be a partition of the complete nonself source universe. Each nonself source is accounted for once as a retained singleton, an omitted node member, or a proved zero with its admission evidence. No source may be lost because it is absent from an approximate neighbor enumeration. Self membership must be removed consistently from the shape/admission proof and aggregate. If a whole-node aggregate is reduced by a self amplitude, the subtraction also needs a sound enclosure; ordinary subtraction of two rounded totals is not an exact self-free aggregate.

All row contractions used for one root-defect certificate must correspond to the same current geometry, nominal quantities, and candidate rotor vector. If the candidate is updated during a sweep, affected aggregates and row bounds must be rebuilt or otherwise rigorously updated before they are combined into one certificate. A collection of individually sound bounds at different candidate states does not enclose the polynomial system at one candidate.

A bottom-up source aggregation can enclose all node sums without materializing all receiver-source coefficients. That is a formal data-dependency observation. It proves neither that useful receiver nodes can be accepted nor that query work is subquadratic. Candidate construction, hierarchy construction/update, guard proofs, exact singleton work, refinement, fallback, aggregation, complete row coverage, outward arithmetic, and output validation all belong to the complete proposed query.

## 7. Root-defect corollary applies to the complete contraction

For the same current fixed finite nonnegative coefficients and exact positive weights, the inherited map has the stated one-half log-space contraction and one-Lipschitz log-root dependence. These hypotheses do not require a small ordinary row-sum contraction constant. They do require a well-defined fixed coefficient problem throughout the claimed domain.

Given a valid candidate 0 < xhat_ir <= 1 and its exact weighted-square-root amplitudes, a complete enclosure of s_ir encloses p_ir = xhat_ir cubed + xhat_ir*s_ir. Dependencies between the candidate's rotor value and its derived source amplitudes do not invalidate interval inclusion. A numerical implementation must enclose those shared quantities, not substitute an unrelated rounded amplitude as an exact identity.

If 0 < L_ir <= p_ir <= U_ir, then p_ir <= U_ir and 1/p_ir <= 1/L_ir. Consequently kbar_ir = max(1,U_ir,1/L_ir) is a valid upper bound for max(p_ir,1/p_ir). Taking the maximum across every rotor gives Kbar. The proposed outward enclosure

    xhat_ir/(kbar_ir*Kbar) <= xstar_ir
    xstar_ir <= min(1, xhat_ir*kbar_ir*Kbar)

then follows from the inherited corollary. Using a lower contraction of zero is conservative when no better lower bound is available. Exact positivity of xhat implies exact p > 0, but a computed nonpositive L means the numerical proof has not been established. It does not authorize silently substituting zero, clipping the candidate, or skipping a row.

A single weak row can enlarge the global factor and degrade every interval. A complete valid enclosure need not meet any useful rotor/load tolerance. The adopted signed rotor-force, collective-force, and moment propagation remains conditional on the same nominal forces, lever arms, and actual rotation column; near-unit saved geometry must not be treated as exactly orthonormal. None of this validates physical airflow or long-horizon flight.

## Required clarifications for the separate adopted note

- Keep the exact-real target separate from the legacy binary64 target, and freeze constant/preparation identities before any later evaluation.
- Expand the simple active-enclosure shorthand to include the original magnitude guards, global input validity, full branch precedence, resource count, and whole-domain cap obligations. An unresolved predicate is not a rejection fact or an admitted zero.
- State sufficient interval conditions for a strictly positive lower bound; active discrete membership alone may yield a zero box lower bound.
- State that each row accounts for every nonself source exactly once and that every row bound in one certificate uses the same complete current candidate.
- Distinguish legacy descending-order admission from the broader mathematical contraction theorem.
- Preserve the status as a conditional derivation. Useful tightness, cost, asymptotic scaling, browser speed, physical validity, and novelty remain unobserved.

The inspected query clarification is consistent with the kernel source: the timed F query uses fullSymbols=false. This review does not remeasure any prior run or infer a new saving from dense-symbol removal. A prospective changed load/certificate interface must compare complete matched tasks.

## Exact reading inventory

All paths below are repository-relative. SHA-256 values were read with each file; no source file was edited. The first three are this checkpoint's authored documents; the remaining seven are inherited content. All ten were read in full.

| Path | SHA-256 |
| --- | --- |
| research/m31-current-bound-design-2026-10-16/PROSPECTIVE-SCOPE.md | fc13783c7331466becb0649db86b57455d9401ee2556a3698da1e58ae2f13461 |
| research/m31-current-bound-design-2026-10-16/DERIVATION-DRAFT.md | e1bd9faf15a76f5b8b2acccb4bdce34b6f5fdc0bf292cbabb079127b606fb014 |
| research/m31-current-bound-design-2026-10-16/QUERY-CONTRACT-CLARIFICATION.md | f34915372d63570c4ebb419b5130ac015e887f8a696ea7f7e38fea2575dd2585 |
| research/m31-root-defect-planning-2026-10-16/ADOPTED-DERIVATION.md | dd1afefb4cefb4f10176cb2ba2fae25024e28116ce7c78d73fa152e3ea29104c |
| research/m31-root-defect-planning-2026-10-16/DERIVATION-DRAFT.md | 744aa89915f09558081600edfec39c2e28dfa70461ef1ea6b35ae11fb8ec276c |
| research/m31-root-defect-planning-2026-10-16/review/MATHEMATICAL-CHALLENGE.md | 58337af18dab0d73e0b389dc01d1e1c90649c8d7cc45e84ab70ed9eefb18e59d |
| research/m31-coupled-solve-2026-10-16/review/CONTRACT-CHALLENGE.md | 39fd45bf0070c76a40251f1519898ca7ca169978966d3bcfb052f66df82b4476 |
| research/m31-browser-screen-2026-10-16/source/kernel.cjs | efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8 |
| research/m31-browser-screen-2026-10-16/source/reference-excerpt.cjs | ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e |
| research/m31-browser-screen-2026-10-16/source/anchor-kernel.cjs | c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a |
