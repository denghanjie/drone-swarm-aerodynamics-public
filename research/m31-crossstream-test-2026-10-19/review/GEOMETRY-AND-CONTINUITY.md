# Cross-stream geometry, sign and independent continuity derivation

19 October 2026. Source/analytic preparation only. No saved velocity payload was scored, no scientific source or MATLAB script executed, and no numerical controls run. The cross-stream sign is fixed before any component comparison.

## Source-supported sign and measurement plane

The official RSS paper §III-B, continuing on page 5, identifies v as the lateral x component and u as the axial z component, with Fig.3 supplying the coordinate orientation. It immediately specifies that u is positive toward the ground. Figure 3 on page 3 shows +x to the right and +z downward. Figure 4 on page 4 and its caption put the PIV sheet through the centers of the front two rotors. With the previously fixed Cartesian rotor half-spacing l, this is the plane y/l=1; choosing its reflected counterpart y/l=−1 would not change the radial x projection under the no-swirl assumption.

The released `static/README_static.txt` identifies x_piv and z_piv as x/l and z/l, u_piv as mean axial velocity/Ui, and v_piv as mean lateral velocity/Ui. The released `static/plot_FM_data.m` plots the single-source field directly as `contourf(x_piv, z_piv, v_piv, ...)`. It reverses only the vertical display direction with `YDir='reverse'`. It does not negate or exchange x_piv and v_piv and does not reverse the horizontal axis. Its signed color range is −0.20 to +0.20. Thus the public paper's +v along +x convention is retained by the published display workflow.

Figure 7d and page 6's prose provide a qualitative cross-check: the paper describes near-rotor motion inward, followed by an outward-spreading merged core; the plotted lateral sign reverses accordingly on either side of x=0. This is a reading of sign conventions and published qualitative statements, not a sign choice from new residuals, digitization of velocities, or payload scoring.

**Admission:** use measured v directly as the component along increasing X, and use the signed candidate with that same orientation. No post-result negation or magnitude-only comparison is permitted. This source chain supports a declared coordinate mapping. It does not independently reconstruct camera calibration or demonstrate the unavailable single-PIV preprocessing/sign-transform history. The README was updated 5 May 2026; identity with the original 2025 figure-generation release is not established. Those limits remain explicit.

Source identities:

| Source | Bytes | SHA-256 |
|---|---:|---|
| Official RSS 2025 PDF | previously pinned | `e821c65273015921437fafc7b35b4f669ec01f985d965c31d3feeecbffb94932` |
| `static/README_static.txt` | 4,960 | `2695a000f2beac1c2f84d645bf6c0b24ca879f5b7ecb8d9873e2b6cfd8e4de6b` |
| `static/plot_FM_data.m` | 2,489 | `f7d19ac69ca303ee1c39a5bfd5e36ec85a7d996b0e61adae46c204607150a8ab` |

Sources: Kiran, Ayanian and Breuer, *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, RSS 2025, [DOI 10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102), official PDF pp. 3–6; released archive [DOI 10.26300/64d4-wa17](https://doi.org/10.26300/64d4-wa17), archive SHA-256 `b495b7a224b3c1db9f15efd5a15815c586e4e11ea29d4df6edcbc25bf50554fa`.

The other two released PIV plotting scripts process different multi-vehicle velocity-magnitude arrays and do not establish the sign or normalization of the single-source lateral component. They are not used to choose a sign or calibration here.

## Independent analytic derivation

Use dimensionless Cartesian coordinates X=x/l, Y=y/l and Z=z/l, with Z positive downward. Write R=sqrt(X²+Y²), K=2sqrt(2), c=sqrt(2)−1, S=.07668 and s=Z+5.817K. The inherited gain g is constant in space. Then

    b=S*s,       Uc=g*10.11*K/s,
    ξ=R/b,       F(ξ)=(1+c*ξ²)^−2,
    U(R,Z)=Uc*F(ξ).

Under steady incompressible axisymmetry, axial U and radial V_R obey

    ∂U/∂Z + (1/R) ∂(R*V_R)/∂R = 0.

At fixed R, ∂Uc/∂Z=−Uc/s and ∂ξ/∂Z=−ξ/s, so

    ∂U/∂Z = −(Uc/s)*(F+ξ*F').

Regularity at the axis fixes the otherwise possible C(Z)/R integration term to zero. Integrating the divergence equation from 0 to R gives

    R*V_R = −∫₀ᴿ ρ*(∂U(ρ,Z)/∂Z) dρ
          = (Uc*b²/s) ∫₀^ξ t*(F(t)+t*F'(t)) dt.

By integration by parts and a direct antiderivative,

    ∫₀^ξ t*(F+t*F') dt = ξ²*F(ξ) − ∫₀^ξ t*F(t) dt,
    ∫₀^ξ t*F(t) dt = ξ²/[2*(1+c*ξ²)],

and hence

    V_R = (Uc*S/2) * ξ*(1−c*ξ²)/(1+c*ξ²)².

For the measured plane Y=1, R=sqrt(X²+1). With **zero mean azimuthal velocity**, the observed horizontal candidate is

    V_X = V_R * X/R.

This is exactly the proposed expression, including its sign and factor S/2. The factor of K enters the axial origin and amplitude through s and Uc; there is no additional K multiplying the final spreading-rate factor S. The result is odd in X, vanishes at X=0, and has radial zero at ξ=1/sqrt(c). The radial field changes from outward to inward beyond that zero; it must not be forced to have one sign throughout the admitted disk.

An algebraically independent implementation can use H=b²+cR²:

    U = Uc*b⁴/H²,
    V_R = (Uc*S/2)*R*b*(b²−cR²)/H²,
    V_X = (Uc*S/2)*X*b*(b²−cR²)/H².

These rational forms avoid computing V_X through the producer's ξ polynomial and projection sequence. They are suitable for the independently authored Decimal audit.

## Conditions on this completion

Continuity determines the radial component under the specified axial profile, regularity and axisymmetry. It does not determine azimuthal swirl. On Y=1, a nonzero V_theta would add `−V_theta/R` to V_X. Therefore the signed candidate is a no-mean-swirl completion, not a universally continuity-required total measured lateral velocity. Mean nonaxisymmetry could also change the result.

The measurement plane is off the source axis. Its in-plane derivative sum ∂V_X/∂X+∂U/∂Z need not vanish: the omitted ∂V_Y/∂Y contributes to the three-dimensional divergence. No planar divergence test should be substituted for the cylindrical continuity identity. In particular, X=0 on Y=1 is not the cylindrical axis, although the radial x projection still vanishes there.

The restriction ξ<=2 keeps both the evaluation point and every radius in the integral from 0 to R inside the unfaded profile. At the boundary the original smooth radial fade is one with zero derivative. The admitted axial domain is also before the physical axial fade/cutoff. This justifies the local formula without specifying a continuation through the finite-support taper. It does not establish global mass or momentum conservation, a Navier–Stokes solution, or the complete production vector field.

The inherited gain comes solely from the closed axial scale-transfer result. It must be pinned exactly and never re-estimated from lateral velocities. The axial scalar's original flow-magnitude interpretation, its use here as a downward axial field, the unverified reference-speed mapping, the model's three-dimensional axisymmetric extension and the absence of single-PIV preprocessing remain assumptions. Near records are descriptive because their axial values supplied the gain; primary lateral evaluation remains Z>=12 under the fixed core restriction. No conclusion is known at this preparation stage.
