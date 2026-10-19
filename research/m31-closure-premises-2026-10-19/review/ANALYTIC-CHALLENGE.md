# M31 closure-premise challenge — source-only checkpoint

19 October 2026. Independent protocol reviewer. Static source reading, visual inspection of an already-rendered PDF page, and analytic reasoning only. No numerical science, fits, scores, raw-data decoding, source execution, or browser QA. Frozen prior files were not edited.

**Finding:** the fixed axial profile and implemented radial closure are derivative-consistent under their stated assumptions. The RSS2025 Eq. (6) expression differs from the half-width closure explicitly printed in 2026 Eq. (9). This identifies a published-expression/convention discrepancy to document, not a justified coefficient correction, a defective experiment, or permission to substitute the expression that might fit better.

## 1. Derivatives, not axial value agreement, determine this closure

The existing [geometry and continuity note](../../m31-crossstream-test-2026-10-19/review/GEOMETRY-AND-CONTINUITY.md) fixes

    K = 2√2,  c = √2−1,  S = .07668,
    s = Z + 5.817K,  b = Ss,
    A = Uc = g·10.11K/s,  g = .5450089857597356,
    ξ = R/b,  F(ξ) = (1+cξ²)⁻²,  U(R,Z) = A(Z)F(ξ).

For arbitrary differentiable A(Z), b(Z), steady axisymmetric incompressible continuity and regularity at R=0 give the following analytic identity (primes on A,b mean derivatives in Z):

    I(ξ) = ∫₀^ξ tF(t)dt = ξ²/[2(1+cξ²)],
    V_R = −R⁻¹ ∫₀ᴿ ρ ∂_Z U(ρ,Z)dρ
        = A b′ ξF − (bA′ + 2Ab′) I/ξ.

The fixed A′=−A/s and b′=S therefore give exactly

    V_R = (AS/2) ξ(1−cξ²)/(1+cξ²)².

On Y=1, R=√(X²+1), and zero mean swirl gives V_X=V_R X/R. K already enters s and A; there is no additional K in b′ or the final spread coefficient. The result is local to the admitted unfaded domain. Axial value agreement alone does not verify A′, b′, the missing-core extension, or the physical applicability of these assumptions.

## 2. Exact source comparison

**RSS2025:** [§III-B2, Eqs. (2)–(6)](https://arxiv.org/html/2507.09463v1), with Eqs. (5)–(6) visually confirmed on [official PDF p. 7](https://www.roboticsproceedings.org/rss21/p102.pdf#page=7). Eq. (2) defines half-width; Eqs. (3)–(4) give linear width and inverse-distance centerline speed. Eq. (5) is F above, whereas Eq. (6) prints

    v/uc = (1/2)(ξ−ξ³)/(1+ξ²)².

The following definition and Fig. 10/11 axes use half-width-scaled lateral position, ξ=x/r_half. §III-B identifies v as the x component; Fig. 4 locates the measurement sheet through the front rotors. The PDF identity already pinned in the prior review is SHA-256 `e821c65273015921437fafc7b35b4f669ec01f985d965c31d3feeecbffb94932`.

**2026:** [§3.2 Eqs. (2)–(4), §3.3 Eqs. (8)–(9), Fig. 7](https://arxiv.org/html/2608.30900v1) explicitly uses local uc and ξ=r/r_half for the diagonal cut, and prints

    v/uc = (S/2)(ξ−cξ³)/(1+cξ²)².

Its fitted S=.088 and §2 motor-arm length l=46 mm belong to that experiment. Neither those values nor its similarity threshold can be imported into the present fixed model and old Cartesian half-spacing convention.

**Reviewer inference:** under the same half-width radial interpretation, the noncentral zeros are ξ=1 in RSS Eq. (6) and ξ=1/√c in the current/2026 closure. A multiplier cannot reconcile the functions. Setting η=√c ξ transforms the latter into

    v/uc = S/(2√c) · (η−η³)/(1+η²)².

Matching RSS Eq. (6) would still require an additional normalization or a different slope convention; the inspected passage states neither. Moreover, RSS's in-plane x coordinate/component and the present cylindrical R followed by projection are distinct observables. The printed formula cannot simply replace V_R or V_X. This review establishes neither the authors' intended alternate convention nor a proved typographical error.

## 3. Normalization and geometry remain open premises

[RSS2025 §III-B Eq. (1)](https://arxiv.org/html/2507.09463v1) gives Ui=√[Fz/(2ρAn)], with A one rotor area and n propellers. [2026 §2 Eq. (1)](https://arxiv.org/html/2608.30900v1) gives Ui=√[T/(2ρπR_rotor²)]=√[mg/(8ρπR_rotor²)], T=mg/4. These are algebraically the same disk-induced convention for four rotors in hover. Their numerical prose does not justify a factor-two correction. The unavailable singlePIV preprocessing chain remains unverified; separate multiPIV scripts do not establish it.

Y=1 samples only R≥1, so X=0 is not the cylindrical axis. The regular-axis integral needs the unseen R<1 core. No planar divergence test can replace three-dimensional continuity, and continuity alone does not remove swirl. Treating the inherited scalar speed model as downward axial velocity is also a modeling premise. These are the limits identified by the frozen [lateral result's next decision](../../m31-lateral-symmetry-2026-10-19/review/RESULT-REVIEW.md).

## 4. What could justify a separate prospective numerical test

- A recovered singlePIV processing/calibration chain or authoritative source clarification could establish a concrete component, coordinate, or normalization correction before scoring it.
- A predeclared physical hypothesis about axial evolution or geometry, with evidence beyond the exposed residual, could justify a bounded diagnostic. It would need fixed support, uncertainty treatment, interpolation/derivative rules, and explicit core, axisymmetry, and swirl assumptions.
- An annular continuity balance could avoid inventing core flux. For fixed radii R2>R1≥1, analytic continuity gives

      ∫z1^z2 [R2 V_R(R2,z)−R1 V_R(R1,z)] dz
        + ∫R1^R2 R[U(R,z2)−U(R,z1)] dR = 0.

  This cancels the unknown interior contribution. It still requires conditional axisymmetry/no swirl, fixed quadrature and support, and conversion V_R=v_x R/X only away from X=0. Stitching, measurement error, and coordinate uncertainty need a prospective treatment. Failure would not isolate its cause or disprove incompressibility. This is an analytic option only; no protocol or execution is authorized here.

The source checkpoint supports retaining the existing formula and unresolved physical premises. It supports no new score, lateral gain, production adoption, receiving-force claim, or swarm validation.
