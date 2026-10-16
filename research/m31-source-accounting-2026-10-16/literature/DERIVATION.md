# Analytic source-wake axial mean-momentum diagnostic

Prepared 2026-10-16 by static source reading and symbolic derivation. No frozen
module was imported or executed. No real-data score, simulation, numerical
integration, parameter search, browser/GPU experiment, or source change was made.
Any numerical audit proposed below remains unallocated and unexecuted.

The untruncated profile has a downstream-independent axial **mean-convective**
momentum flux. With the frozen geometry, that flux is approximately 0.72 times the
prescribed isolated-hover source thrust. This is an analytic model normalization
result, conditional on interpreting the scalar profile as mean axial velocity.
It is not a measured thrust discrepancy or, by itself, a conservation violation.

## Source mapping and notation

The frozen `source/host.cjs`, lines 29–33 and 119–128, and
`source/independent-frozen.source.txt`, lines 89–102 and 137–147, agree on:

| Symbol here | Frozen definition |
|---|---|
| `C` | `decay = 10.11` (the coefficient called `B` in the assignment) |
| `S` | `spread = 0.07668` |
| `o` | `origin = -5.817` |
| `h` | motor coordinate `0.028 m`; motor centers are `(±h, ±h)` |
| `D` | `2 sqrt(2) h`, the opposite-motor diagonal |
| `R` | one propeller radius, `0.023 m` |
| `Aprop` | `pi R²`, one propeller disk area |
| `T0` | prescribed isolated-hover weight `m g`, with `m = 0.027 kg` |
| `UH²` | `T0/(8 rho Aprop)` for four propellers |

The inherited source explicitly fixes amplitude from hover weight independently
of source motor states (`independent-frozen.source.txt`, lines 55–68). The profile
represents one source vehicle's merged wake; it is not four source-rotor profiles.

The paper normalizes lengths by motor distance `l` and velocity by `UH` (Eqs. 1,
7–8). Its Eq. 9 reports the fitted normalized product `B d = 10.11`, not a
standalone dimensional `B = 10.11`. Here `C` denotes that whole numerator, so no
additional propeller diameter should multiply it. The fitted profile, half-width,
and inverse-distance scaling appear in Eqs. 3–6 and VI-C. The smallest measured
vehicle is 230 g. Its omnidirectional probe measures speed, without directional
or Reynolds-stress measurements. These facts support the formula interpretation,
not a complete momentum balance. [Bauersfeld et al., arXiv v3, III–IV and VI](https://arxiv.org/html/2403.13321v3).

## Closed-form integral

Let `z` be downstream distance, `q = z/D - o > 0`, and

\[
 a=\sqrt2-1,\qquad U_c=\frac{C U_H}{q},\qquad b=S D q,
 \qquad \bar u_z(r,z)=\frac{U_c}{[1+a(r/b)^2]^2}.
\]

Here `a` is the profile constant, not the code's arm-coordinate variable. The
profile is axisymmetric, `b` is its half-velocity radius, and this calculation
extends the mathematical profile to every `r >= 0` without fades or projection.
For comparison with the inherited far-field fit, restrict `z/D >= 2.5`; the
symbolic cancellation below holds wherever `q > 0`.

For constant density, the downward axial momentum flux due to the mean velocity
through a plane normal to the source axis is

\[
 M_{\rm mean}(z)=\rho\int_{\mathbb R^2}\bar u_z^2\,dA
 =2\pi\rho U_c^2\int_0^\infty
       \frac{r\,dr}{[1+a(r/b)^2]^4}.
\]

Set `y = 1 + a(r/b)²`, so `r dr = b² dy/(2a)`. Therefore

\[
 M_{\rm mean}
 =\frac{\pi\rho U_c^2b^2}{a}\int_1^\infty y^{-4}\,dy
 =\boxed{\frac{\pi\rho U_c^2b^2}{3a}}
 =\boxed{\frac{\pi\rho C^2S^2D^2U_H^2}{3(\sqrt2-1)}}.
\]

The inverse-square centerline factor and square width cancel exactly. Neither
`z` nor the virtual origin remains. The units are force: density times velocity
squared times area. This is a squared-mean integral, not `rho integral <u_z²> dA`.

Substitute the four-propeller hover normalization:

\[
 \boxed{K:=\frac{M_{\rm mean}}{T_0}
 =\frac{\pi C^2S^2D^2}{24a A_{\rm prop}}
 =\frac{C^2S^2}{24(\sqrt2-1)}\left(\frac{D}{R}\right)^2.}
\]

For the frozen constants this becomes the exact desk expression

\[
 K=\frac{(10.11\cdot0.07668)^2\,8(0.028)^2}
          {24(\sqrt2-1)(0.023)^2}
  =\frac{784(0.7752348)^2(\sqrt2+1)}{1587}
  \ \text{(approximately }0.72\text{)}.
\]

No profile samples or numerical quadrature are needed for this result. `T0`
remains symbolic; no measured force or flow observations were scored.

## What the normalization can and cannot establish

**Geometry matters; mass alone cancels.** The mean-only equality
`M_mean = T0` would require

\[
 CS\,\frac{D}{R}=\sqrt{24(\sqrt2-1)}.
\]

Fixed `C,S` cannot enforce that equality for all independent `D/R` geometries.
Changing only mass from a larger vehicle to 27 g scales both `M_mean` and `T0`
equally and does not change `K`. Uniform geometric rescaling also preserves `K`.
Changing geometry ratios or using the fit outside its physical regime can matter.
The mass extrapolation is a separate validation gap, including potentially
different Reynolds-number and rotor/body effects; this algebra does not quantify it.

**The meaning of `D` must be resolved before calling it a bug.** The code's `D`
is definitely the diagonal of its square motor layout. The paper defines a motor
distance `l` and refers to Fig. 2 for geometry. The inherited access log explicitly
warns that diagonal-versus-edge arrows were not visually verified. The fresh
connector PDF screenshot requests returned markers without inspectable image
pixels here, so this note does not upgrade that geometry convention to verified.
[Paper Fig. 2 and III-D](https://arxiv.org/pdf/2403.13321v3).

For the same layout, replacing the diagonal by the adjacent-motor spacing `2h`
while retaining the numerical fit coefficients halves `K`. Replacing it by the
center-to-motor arm `sqrt(2)h` quarters `K`. Replacing it by propeller diameter
`2R` gives `K = C²S²/[6a]`. These are conditional geometric substitutions, not
recommended corrections or evidence of which convention the paper intended.

A pure change of normalization convention must transform the fit too. If
`D_new = k D`, the same physical field has `C_new = C/k`, `o_new = o/k`, and
unchanged `S`; then `C_new D_new = C D` and `K` is unchanged. Merely changing `D`
with the old coefficients changes the model, rather than fixing its notation.

**The denominator is the prescribed hover thrust.** If the actual nominal source
motor-thrust sum is `Tsrc > 0`, the frozen source instead implies
`M_mean/Tsrc = K T0/Tsrc`. Its amplitude has no source-motor feedback. Thus even
enforcing `K = 1` at hover would not make the wake track arbitrary source states.
This follows from the documented model choice; no source-state case was run.

## Why this is not a full thrust-conservation verdict

For a steady incompressible Reynolds-averaged control volume, after appropriate
hydrostatic/background subtraction, the axial momentum statement involves

\[
 F_z=\oint_{\partial V}\!
 \left[\rho(\bar u_z\bar u_j+\overline{u'_zu'_j})n_j
       +(\bar p-p_\infty)n_z-\bar\tau_{zj}n_j\right]dA.
\]

Unsteady storage must be added when the steady assumption fails. The derived
`M_mean` is only the mean-convective part on one downstream plane. A full balance
also needs axial turbulence flux, pressure, viscous terms where material, and
upstream/side contributions. Radial entrainment can transport axial momentum
through side boundaries via mean and turbulent cross-fluxes; transverse motion
cannot simply be added as a squared scalar speed on the axial plane.

The fitted scalar profile supplies neither these missing fields nor a proof that
they vanish. Interpreting a mean-speed fit as an axial mean component is itself an
assumption. Consequently `K < 1` identifies a mismatch with a **mean-only,
ambient-pressure, negligible-other-flux far-wake thrust surrogate**. It does not
show that a complete real flow violates conservation, establish the magnitude of
missing terms, or validate the extrapolated 27 g model.

The actual frozen implementation adds radial/downstream fades, finite cutoffs,
neighbor eligibility, and receiver-axis projection. These are interaction-model
choices, not a full conservative fluid control volume. Before projection, fades
bounded by one can only reduce this nonnegative squared-velocity integral. The
unfaded hard-radius result, useful as a later check, is

\[
 \frac{M_{\rm mean}(r\le\lambda b)}{M_{\rm mean}(r<\infty)}
 =1-(1+a\lambda^2)^{-3}.
\]

The implemented cubic radial fade was not integrated here. A receiver-dependent
projection should not be mistaken for a source velocity field over a whole plane.

## Possible next finite audit — not allocated

After verifying the geometric convention, a separately frozen numerical audit
could check a fixed small set of downstream stations against the analytic
untruncated integral and hard-radius fraction, then quantify only the declared
fade/truncation effect. It should keep three outputs distinct: numerical integration
error against a closed form, model normalization relative to `T0`, and any empirical
validation requiring new measurements. No fitted-parameter correction, real-data
score, or scientific launch is authorized by this derivation.

Local evidence paths and hashes are recorded in `SOURCE-RECEIPT.json`; they refer
to unchanged, read-only frozen source and inherited literature notes.
