# Draft: from source boxes to complete current row contractions

Status: unreviewed conditional exact-real derivation. No computation, example evaluation, performance observation or new physical evidence. Do not implement or claim a certified browser result from this draft. The original draft remains immutable after reviewers receive it; resolutions belong in ADOPTED-DESIGN.

## 1. Numerical target must be explicit

The inherited root-defect corollary concerns an exact-real algebraic model with complete fixed nonnegative coefficients and weights summing to one. The legacy JavaScript builder produces rounded coefficients using Math.hypot, square roots, branch decisions and rounded nominal sums. These are different reference objects. An exact-real enclosure of a geometric formula is not automatically an enclosure of every native Math.hypot implementation or its branch decisions.

The derivation below targets the declared geometric formula in exact real arithmetic on declared current prepared positions/rotor points/axes and positive nominal forces/constants. Treat any supplied binary64 endpoint as its exact real value. Define nominal totals as exact sums and weights w_ir=f_ir/sum_r f_ir. Prepared coordinates and axes may be non-unit; use their actual values throughout. Preparation itself is outside this conditional derivation unless its rounding is enclosed. This target must not silently replace the inherited binary64-coefficient contract. Before execution, either provide a verified bridge enclosing that actual computation, or explicitly adopt and independently requalify a mathematical-model reference with a separate legacy discrepancy report. No such operational choice is adopted here.

Let h=d·a_j, e=d−h*a_j, r=||e||, where d=c_j−p_ir uses source center c_j and receiver rotor point p_ir. The exact inherited shape on its active branch is

    W(h)=spread*(h−origin*D)
    K_irj = induced * decay/(h/D−origin)
             * [1+κ*(r/W(h))²]^(-2)
             * fade(downFade,downCut,h)
             * fade(radFade,radCut,r/W(h))
             * max(0,a_i·a_j),  κ=sqrt2minus1>0.

Constants are the project's declared positive constants, with origin<0. fade(s,t,v) is one for v≤s, zero for v≥t, and (1−u)²(1+2u), u=(v−s)/(t−s), between them. For s<t its derivative inside is −6u(1−u)/(t−s)≤0. Thus it is nonnegative and nonincreasing. This is algebra, not a newly validated wake law.

The coefficient is a_irj=K_irj*β_j/ν_ir with β_j=sqrt(S0_j/mg)>0 and ν_ir=sqrt(f_ir/(2ρA))>0. Nonself membership, center-neighbor support, near-field rejection and guard branches are prerequisites; the active formula does not define rejected cases.

## 2. Current node geometry

For a source node C, store component intervals for centers c_j and axes a_j enclosing all its current members, plus source IDs/order ranges and nominal information. No average-axis replacement. For each receiver rotor p_ir, interval subtraction gives a box Δ enclosing every d. Natural interval dot/product operations give H enclosing d·a_j and E enclosing d−(d·a_j)*a_j. Dependencies may make these boxes wide; inclusion remains valid. Do not use an orthogonal-projection identity requiring exactly unit axes.

For an interval box E_k=[l_k,u_k], define b_k=0 if it contains zero, otherwise min(|l_k|,|u_k|), and B_k=max(|l_k|,|u_k|). Then

    sqrt(sum_k b_k²) ≤ ||e|| ≤ sqrt(sum_k B_k²).

Denote these bounds rL,rU. Derive projection bounds PL,PU for max(0,a_i·a_j) using the actual receiver axis. Bounds computed with floating arithmetic need outward rounding; ordinary endpoint arithmetic is not an implementation proof.

Self interaction must be removed exactly. A node containing i can be split or have an independently validated self-free aggregate; no accidental self coefficient is allowed. Each source belongs to exactly one retained singleton or omitted node in a row. No overlap/double counting and no missing membership.

## 3. Admission before omission

For each node/receiver, first enclose the branches in their original precedence. A far-neighbor exit is allowed only after the preceding center guard is proven safe. A zero projection does not bypass near-field or invalid-geometry checks. A node whose down interval crosses the unsupported near-field slab cannot be treated as zero merely because an active-branch upper estimate is small.

Conservative allowed dispositions are:

1. Certified original zero branch with all preceding guards discharged; zero contribution and no positive edge.
2. Certified nonrejected active/zero mixture with an upper coefficient bound, whole-source-cube scaled-cap bound, and permitted descending-order membership for every possibly positive edge.
3. Unresolved: split/refine or evaluate exact singletons; if still unsupported, reject/fallback under the declared contract.

For clarity, the simple formula below requires the stronger active enclosure hL≥minDown*D, hU<downCut, positive W(hL), finite geometry/normalization and admitted center bounds. Radial cutoff or projection zero can be included because K≥0 and the upper estimate also covers their zero value. Require Kupper≤128 and Kupper*max_C β_j≤128 to discharge unscaled/scaled term caps over y_j∈(0,1]. Failure of an upper-bound test means uncertainty/refinement, not proof that an actual coefficient violates a cap.

Prove all potentially positive members precede the receiver in the declared descending-z/ascending-ID order, or refine to resolve them. An omitted positive edge must not hide a cycle/order violation. Count/resource guards need an explicit rule too; omission cannot silently remove the original positive-term budget or turn a rejected input into an accepted one. Exact rejection-reason counts may demand extra work and are an interface question, not an aerodynamic theorem.

## 4. A conservative common shape bound

Under the active enclosure above, let WL=W(hL)>0, WU=W(hU), qL=rL/WU≥0 and qU=rU/WL. The following upper bound covers each admitted member, including admitted cutoff zeros:

    U_irC = induced * decay/(hL/D−origin)
             / [1+κ*qL²]²
             * fade(downFade,downCut,hL)
             * fade(radFade,radCut,qL) * PU.

Reason: 1/(h/D−origin) and the down fade decrease with h; r/W(h)≥rL/WU; radial attenuation and radial fade decrease with that ratio; projection≤PU. Every factor is nonnegative, so separate upper bounds can be multiplied. The bounding extremes need not occur at the same source; this can loosen the bound but cannot invalidate it.

A strictly positive lower bound requires every member to be on the admitted active branch (center eligibility as well as h/radial support, and no self). In that case replace hL by hU, qL by qU, and PU by PL in the analogous expression. Otherwise use zero. This draft does not assume that a positive lower bound is available or useful.

## 5. Node summaries and candidate-dependent contraction

For any candidate 0<xhat_ir≤1, form exact candidate-derived yhat_j=sqrt(sum_r w_jr*xhat_jr). Define a current node sum

    B_C = sum_{j in C} β_j*yhat_j.

With outward intervals for β and yhat, one bottom-up aggregate pass can enclose B_C without constructing receiver-source coefficients. If the node shape satisfies 0≤K_irj≤U_irC for all its nonself admitted members, then

    0 ≤ sum_{j in C} a_irj*yhat_j ≤ U_irC*B_C/ν_ir.

A common lower shape bound can similarly supply a lower row contribution, but zero is always conservative. Combine disjoint omitted-node contributions with independently enclosed retained-singleton contributions to obtain [sL_ir,sU_ir] containing the COMPLETE current row contraction. Rebuild/reaggregate from current geometry and current candidate; stale geometry or independently chosen source amplitudes do not satisfy the assertion.

This offers a conditional bridge: the bound uses node geometry and a source aggregate rather than every omitted coefficient. It does not prove fewer visited nodes, smaller bounds or lower total work. Adversarial geometry can force singleton refinement everywhere. Creating the hierarchy and all aggregates, including a second candidate-dependent pass if needed, belongs inside complete query cost.

## 6. Use the existing defect corollary, without losing its assumptions

Enclose p_ir=xhat_ir³+xhat_ir*s_ir as [L_ir,U_ir] with L_ir>0. With outward kbar_ir=max(1,U_ir,1/L_ir) and Kbar=max_ir kbar_ir, the inherited conditional result yields

    xhat_ir/(kbar_ir*Kbar) ≤ xstar_ir ≤ min(1,xhat_ir*kbar_ir*Kbar).

Use exact current weights and candidate-derived source amplitudes, or enclosures that rigorously include them. Enclose all rounding in this evaluation. A single loose row can inflate Kbar and every resulting interval. Do not infer useful tightness from existence of an enclosure. Numerical reference uncertainty also needs its own bound before observed discrepancies can test a certificate.

Propagate intervals to rotor forces, collective force and moments as in the adopted root-defect note, using signed lever arms and the actual rotation column. The physical model and long-horizon flight are not validated by this local statement.

## 7. Open operational gates

Before an executable protocol: resolve mathematical-versus-legacy target; prove whole-domain admission and rejection treatment; choose outward arithmetic with a sound square-root/norm policy; independently verify bound soundness; specify stable hierarchy/member ordering and self handling; define exact-H and F-derived matched interfaces; include all refinement/fallback/certificate work; freeze development versus prospective evaluation and stopping/resource budgets. None of those is replaced by this algebraic draft. No benchmark, bound-tightness experiment, 5,000-drone result or novelty claim follows.
