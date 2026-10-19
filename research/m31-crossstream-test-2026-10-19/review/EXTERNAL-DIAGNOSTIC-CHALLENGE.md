# External diagnostic challenge and admissible next comparison

19 October 2026. Static methodological review for Milestone 31. No numerical model evaluation, integration, ratio calculation, fit, score, raw-data decoding, scientific import, numerical control or browser check was performed by this reviewer.

## Decision: reject the proposed Wolf two-flux numerical benchmark

Primary source: Wolf et al., *Volumetric wake investigation of a free-flying quadcopter using Shake-The-Box Lagrangian particle tracking*, Experiments in Fluids 65, 152 (2024), [publisher article](https://link.springer.com/article/10.1007/s00348-024-03880-3), especially §§2.1, 3.1–3.2.

The paper studies a DJI Mavic 2 Pro with rotor diameter 0.22 m, unequal front/back lateral spacing, rotor height offsets and tilted axes. Its D denotes rotor diameter and R rotor radius. A centered 5R-cube control volume has its bottom at 2.5R, with reported bottom outflow magnitude 1324 g/s. Moving the bottom to 5R while retaining horizontal boundaries gives 1466 g/s. The sides thereby lengthen. The often-mentioned 900 g/s near the rotor plane is an actuator-disk estimate. The measured field remains nonaxisymmetric downstream. FlowFit imposes incompressible continuity in reconstruction.

These measurements do not furnish an admissible current score. The project's kernel is admitted only at z >= 2.5 D_motor, where D_motor denotes the applicable motor-center/body length, not the paper's rotor diameter. In the measured airframe the motor-center span exceeds a rotor diameter. Thus even the farther 5R bottom lies upstream of that admission; the 2.5R bottom is nearer still. A disabled or excluded near-field kernel must not be repurposed into a numerical prediction simply because the source reports a convenient integral.

An amplitude-invariant ratio would not repair the mismatch. It removes a common multiplicative scale under its own assumptions, but not the wrong length convention, different airframe geometry, near-field jet merger, finite horizontal aperture, unequal loading, rotor cant or displaced wake center. Integrating over a different physical region would also change the tested quantity. The two reported bottoms belong to differently tall control volumes; their difference is not a direct observation of an unrestricted whole-plane flux increase without accounting for those boundaries.

The small reconstructed net control-volume residual cannot independently validate the continuity law already imposed by FlowFit. It can describe reconstruction consistency. Conversely, discrepancy with a simplified model cannot isolate a failure of that law, of entrainment physics, or of a single wake coefficient.

Record this as a concrete external-search exclusion, not as a failed model test and not as proof no usable independent dataset exists. Wolf remains valuable evidence of three-dimensional entrainment, asymmetric structure and practical measurement methods. A later independent benchmark needs compatible motor geometry and length definitions, a verified downstream domain, dimensional velocity or flux with clear calibration, documented integration boundaries and accessible values adequate for an auditable comparison. No source values should be retuned to make them fit current admission.

## Stronger immediate diagnostic: hold the axial gain and test a saved component

The existing 3,240 saved RSS cases contain signed lateral v that was not used in the axial gain fit. Their use can challenge a new component without another fit, but remains an exposed, same-experiment comparison. It is neither an independent experiment nor a blind validation set.

Keep the prior gain exactly g=0.5450089857597356. Retain the original coordinates X=x/l, Z=z/l, l=0.0325 m and the rotor-row plane Y=y/l=1. With K=2sqrt(2), S=0.07668, c=sqrt(2)-1, s=Z+5.817K, b=S*s, Uc=g*10.11K/s and xi=sqrt(X^2+1)/b, the proposed unfaded axial field is U=Uc/(1+c*xi^2)^2. The closure gives

    V_R = Uc*(S/2)*(xi-c*xi^3)/(1+c*xi^2)^2,
    V_X = V_R*X/sqrt(X^2+1).

This result follows from steady incompressible axisymmetry, regularity at the cylindrical axis and the chosen axial profile; converting it to the total measured x component additionally assumes zero mean azimuthal velocity. On Y=1 a nonzero V_theta contributes -V_theta/R. Continuity alone therefore does not uniquely prescribe the measured cross-stream component.

The candidate is signed and odd in X. Its radial field can change from outward to inward, so magnitude-only scoring or sign reversal would destroy the intended test. X=0 in this plane is not the cylindrical axis; V_X vanishes there by projection, while V_R need not. The two-dimensional in-plane divergence need not vanish because the omitted y derivative contributes.

Restrict to xi<=2 using geometry alone. Every radius in the continuity integral from the regular axis to the admitted point then lies in the unfaded field. Extending the expression through or beyond the 2..3 radial fade would require a separate derivation of that faded field. This is a local core completion, not a proof of global mass or momentum conservation or a complete finite-support production vector field.

The alternate identity V_X=ca*(S/2)*(X/b)*(1-c*xi^2), where ca is the prior gain-corrected axial prediction at that point, makes the gain/axial connection transparent. It must not be used to fit a new lateral scale, width, origin, offset or sign. A separately authored rational/Decimal calculation can audit the same fixed closure without importing producer code.

## Source attribution and interpretation

Kiran, Ayanian and Breuer, [*The Structure of Merging Turbulent Jets Beneath a Small Quadrotor*, arXiv:2608.30900v1](https://arxiv.org/html/2608.30900v1), §3.3 Eqs. 8–9, give the corresponding half-width axial and cross-stream shapes. Their fitted spreading value and radial arm length belong to that paper, not to the old archive's Cartesian half-spacing. Their self-similarity height cannot simply be copied into the old Z coordinate. Borrow the known relation while retaining this project's fixed parameters and stated limitations.

The earlier [RSS 2025 paper](https://arxiv.org/html/2507.09463v1) prints a different Eq. 6. Cite the later equation or the explicit independent derivation, rather than treating this expression as a literal reproduction of the older equation. The source-backed +v along +x convention and unflipped archive plot support the declared comparison orientation; unavailable single-PIV preprocessing still prevents independently reconstructing instrument calibration or its transform history.

Primary farther-region discrepancy against the zero-lateral baseline is descriptive. Improvement would support further testing of this particular closure on these saved values, without establishing dimensional calibration, axisymmetry, no swirl, full vector fidelity, receiving-drone force or safe flocking. Failure would expose a mismatch under the combined closure and measurement assumptions; it would not uniquely identify which assumption failed. No numerical outcome is known at this review stage.
