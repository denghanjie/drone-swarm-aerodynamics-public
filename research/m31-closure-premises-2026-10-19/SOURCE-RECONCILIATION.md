# What the published definitions do and do not support

Source-only reconciliation, 19 October 2026. No new measurement arithmetic or fitted parameter. Let c=sqrt(2)-1, b be the radial half-width, s=z-z0 and xi=r/b. These symbols denote the idealized axisymmetric model; the old front-rotor measurement plane also uses a signed in-plane coordinate, which must not be substituted for cylindrical r silently.

## 1. Printed expressions differ under shared definitions

RSS2025 p.7 Eq5 prints U=Uc/(1+c*xi²)². Eq6 prints V=(Uc/2)*(xi-xi³)/(1+xi²)². The accompanying text and Figs10–11 define xi by the local half-width. The later 2026 preprint §3.3 Eq9 includes S/2 and retains c in the corresponding cubic and denominator. Our closed crossstream implementation uses the latter expression with its previously fixed parameters.

For Uc=A/s and b=S*s, steady axisymmetric incompressibility and regularity at the axis give, analytically:

    U(R,z) = Uc * F(xi),    F(xi)=(1+c*xi²)^(-2)
    V_R(R,z) = -(1/R) integral_0^R r * partial_z U(r,z) dr
             = (Uc*S/2) * xi*(1-c*xi²)/(1+c*xi²)^2.

This follows the independently derived identity already preserved in the crossstream checkpoint. It is not a new measured result. Current code retains S/2 and c, and uses the correct radial-to-horizontal projection on the offset plane under no-mean-swirl assumptions.

The two printed shapes cannot be reconciled by only multiplying velocity: their nonzero roots are xi=1 versus xi=1/sqrt(c). Setting eta=sqrt(c)*xi changes the latter expression to [Uc*S/(2*sqrt(c))]*eta*(1-eta²)/(1+eta²)^2; it also changes the coordinate convention and coefficient. An unstated change of variable/velocity scale cannot be assumed. This is a source-expression/convention discrepancy, not proof of a typographical error, flawed measurements, or an implementation bug. We do not substitute Eq6 or drop S to improve the exposed residual.

Furthermore, the old paper uses in-plane x/half-width on a front-rotor cut. Our xi is cylindrical radius/half-width, followed by projection to measured x velocity. Even a consistently defined planar reference is not automatically a cylindrical radial field. The later paper's Eq9 comparison uses a diagonal cut and its own fitted parameters. It does not independently validate our earlier off-axis data or authorize importing its S.

## 2. Shape agreement does not verify the derivative relation

For a general axial model U(R,z)=Uc(z)F(R/b(z)), let I(xi)=integral_0^xi tF(t)dt. Integrating continuity gives

    V_R = -(b/xi) * [Uc' * I(xi) - Uc*(b'/b)*(xi²*F(xi)-2*I(xi))].

Thus lateral flow depends on changes of centerline strength and width with height, as well as their values. Our special formula imposes Uc'/Uc=-1/s and b'/b=1/s. Good axial prediction at sampled points alone is insufficient evidence for those derivatives. This analytic dependence explains why the existing axial success and lateral mismatch can coexist; it does not identify which assumption fails.

## 3. Observable and normalization checks

Bauersfeld et al. formulate a longitudinal mean jet profile but collect speed using an omnidirectional hot-ball probe (§IV-A). The present project treats the fitted scalar as a signed axial component before applying continuity. That is an additional modeling assumption; mean speed and a mean vector component need not coincide. No numerical magnitude-to-component correction is supported here.

The Brown static README explicitly calls u_piv axial/Ui and v_piv lateral/Ui. The single-vehicle plotting script displays those saved arrays directly. It does not expose their original dimensional conversion or preprocessing. The printed hover-induced scales agree algebraically across the papers when total/per-rotor thrust is handled consistently. The separate multi-vehicle plotting scripts do not establish the old single-field conversion. Hence the documentation supports a common declared unit for u and v, while actual calibration remains unresolved. Neither a factor-two correction nor a separate lateral gain follows.

The old archive uses l=32.5mm as its coordinate scale; the later preprint uses a center-to-motor arm length of46mm. The front-rotor and diagonal cuts differ. Converting definitions and proving data identity is necessary before transferring coordinates, thresholds or fitted constants. We do not treat them as interchangeable measurements.

## 4. The absent core and a test that may avoid it

For the retained old measurement plane Y=1, R=sqrt(X²+1)>=1. No point in this plane samples the axis or R<1. The full continuity integral starts at zero, so a data-only reconstruction from this plane requires an unmeasured-core extension. Near-axis projection V_R=(R/X)V_X is also singular at X=0. Nonzero swirl contributes to measured V_X, and nonaxisymmetric flow invalidates a simple cylindrical interpretation.

A finite annulus offers a more targeted question. Integrating continuity over R in[a,b] and z in[z1,z2] gives

    integral_z1^z2 [b*V_R(b,z)-a*V_R(a,z)] dz
      + integral_a^b R*[U(R,z2)-U(R,z1)] dR = 0.

The common 2pi factor cancels; this is the time-mean incompressible cylindrical balance. Differencing the two radial fluxes cancels the unknown contribution from R<a. A finite-height integral also avoids direct pointwise differentiation. This is standard conservation algebra, not a novel method or an executed test. It still requires a defensible mapping from the offset plane to cylindrical components, geometry support, numerical integration and measurement-error treatment. An empirical imbalance would not by itself identify which assumption or measurement is responsible. See NEXT-TEST.md.

## Decision

No source-supported correction to our implemented S/2 formula was established. Preserve the current model and the previous 84.03% opposite-direction residual finding. Develop a bounded annular-balance feasibility protocol before any numerical work; reject it if the available geometry or measurement provenance cannot support an interpretable comparison. Independent calibrated data remain the route to stronger physical validation.

Sources and verification provenance: LITERATURE.md; independent challenge/evidence reviews in review/. No old scientific or display allocation was rerun.
