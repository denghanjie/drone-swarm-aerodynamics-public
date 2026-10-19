# M31 next empirical diagnostic: source review

19 October 2026. Reviewer: `/root/m31_verified_literature`. Scope: literature and released schema only. No PIV arrays decoded, no wake values computed, no scores or fits produced. Historical physical-test files were not changed.

**Recommendation:** compare the frozen single-source airflow against the released single-Crazyflie mean axial PIV field. This separates a wake-field discrepancy from the receiver cubic/control-law discrepancy. Keep the published RSS planar fit as a same-data descriptive benchmark. This test cannot identify a two-way interaction closure.

## Verified normalization and measurement plane

1. Kiran, Ayanian and Breuer, RSS2025, official PDF pp.6–7: Fig.8 plots `r_half/l` against `z/l`; Fig.9 plots axial `u/Ui` against `z/l`. Table I gives `(Bd,S,z0)=(9.508,0.0667,-6.0585)`. Eq.3 is half-width growth and Eq.4 is inverse centerline decay with normalized initial velocity set to 1. Thus this tuple belongs to the paper's `l=0.0325m` coordinates, not directly to Bauersfeld's motor-distance coordinates. Table I's juxtaposition does not supply a common dimensional normalization. [Official paper](https://www.roboticsproceedings.org/rss21/p102.pdf), [primary HTML §III-B2](https://arxiv.org/html/2507.09463v1#S3.SS2.SSS2).
2. Fig.4 (official PDF p.4), its caption and §II-A2 place the laser plane through the **front two rotor centers**. Combining this with the already reviewed square layout `(±l,±l)` gives plane `y/l=+1`; the opposite sign gives the same axisymmetric radius. For measured `X=x/l`, the current 3D model must use `r/l=sqrt(X²+1)`. The measured `X=0` line is not the vehicle's true 3D axis. This offset is a geometric inference from the documented apparatus, not a pixel measurement.
3. RSS Eq.2 defines the half-width from the measured lateral centerline; Fig.10 explicitly labels `ξ=x/r_half`, and Eq.5 uses that ξ. Its empirical planar profile therefore uses `|X|`, not `sqrt(X²+1)`. Replacing its lateral argument with the true 3D radius would create a different, unvalidated model. [Fig.4 and §II-A2](https://arxiv.org/html/2507.09463v1#S2.SS1.SSS2), [Eq.5 and Fig.10](https://arxiv.org/html/2507.09463v1#S3.SS2.SSS2).
4. Bauersfeld et al. §III-D explicitly normalize length by motor distance; §VI-B Eq.9 gives `(10.11,0.07668,-5.817)`, and §VI-C applies these after coordinate normalization and restores the induced-velocity scale afterward. Its source probe measures omnidirectional speed (§IV-A), an important limitation when testing the M31 use of that profile as signed axial velocity. [Primary manuscript](https://arxiv.org/html/2403.13321v3#S3.SS4).

## Algebraic specification, not an evaluated prediction

Write `Q=z/l`, `k=D/l=2sqrt(2)`, and `g(t)=[1+(sqrt(2)-1)t²]^-2`.

- RSS planar reconstruction: `aK(Q)=9.508/(Q+6.0585)`, `hK(Q)=0.0667(Q+6.0585)`, `uK/Ui=aK*g(X/hK)`.
- Bauersfeld profile at the real plane: `aB(Q)=10.11/(Q/k+5.817)`, `hB(Q)=0.07668(Q+5.817k)` in units of l, and `UB/UH=aB*g(sqrt(X²+1)/hB)` before M31's additional fades.
- Converting the RSS tuple alone into D units changes its numerator to `9.508/k` and virtual origin to `-6.0585/k`; S is unchanged. Do not multiply Bd by another propeller diameter. This unit conversion does **not** make its planar fit a 3D field.

Use Eq.4's reciprocal functional form; the paper's nearby wording calls the decay linear. Preserve this source inconsistency rather than silently fitting or repairing it. Verify any reconstruction against the stated equations and report mismatches transparently.

## Released schema and proposed discriminating endpoint

The official static README states that `x_piv,z_piv` are normalized by l, `u_piv` is mean axial velocity/Ui and `v_piv` is mean lateral velocity/Ui. The paper makes positive axial velocity point downward. Separate multi-vehicle files contain velocity magnitudes and should not replace this single-wake target. The archive inventory identifies the four single-PIV files, but no trial-level single-PIV arrays. [Dataset DOI](https://doi.org/10.26300/64d4-wa17).

Proposed primary endpoint: **signed normalized axial-field residuals and equal-downstream-slice mean absolute error**, using each slice's coordinate-based quadrature weights. Freeze coordinate orientation, finite/missing-value handling, lateral bounds, slice/band weighting and interpolation rules after coordinate/schema inspection but before decoding velocity values. Use one common far-field region satisfying both `Q>6.5` and `Q/k>=2.5`, within actual documented measurement coverage. Report residuals by downstream location and profiles as secondary diagnostics. Never mask a finite observation merely because M31 predicts zero there.

Compare the delivered frozen M31 airflow on that plane as the main model. Separately show the unfaded literature profile to expose the role of existing downstream/radial fades; label it a diagnostic variant. Preserve the frozen support rules and do not optimize coefficients, offsets, fades or masks against this field. Do not route either prediction through the receiver cubic.

For velocity scaling, explicitly reconcile the dataset's Ui convention (RSS Eq.1 uses total thrust) with the model's UH convention (hover thrust). Equality requires the same thrust/area/density convention; do not infer an absolute SI calibration or fit a multiplicative factor. If that equality cannot be established, state the comparison is under a shared induced-velocity convention.

The RSS fit was derived from this published field, so its agreement is descriptive reconstruction, not independent predictive validation. Grid cells are spatially correlated and the published means are stitched: do not treat cells as independent trials or attach calibrated rejection probabilities without appropriate uncertainty data. Agreement would leave receiver/actuation mapping unresolved; disagreement would locate a field-level problem without uniquely identifying its cause.

## Private evidence provenance

Official PDF URL: https://www.roboticsproceedings.org/rss21/p102.pdf

Retained PDF: `PRIVATE_ACQUISITION/rss2025.pdf`, 8384486 bytes; SHA256 `e821c65273015921437fafc7b35b4f669ec01f985d965c31d3feeecbffb94932`.

Visually inspected complete official PDF pages 4, 6, 7. Existing page 4 and page 6 renders were retained. Page7 was rendered from this same local PDF using bundled `pdftoppm -f 7 -l 7 -scale-to 1800 -png -singlefile`; no download/install was needed. Figure evidence is source reading, not digitization. All files remain in the private directory:

| File | Evidence | SHA256 |
|---|---|---|
| `rss-page-04.png` | Fig.4 front-rotor laser plane; l=32.5mm description | `5bd591cdf5e9552b83883e7915db2980f399fe9106d2dd25fb2b3b1ca2d5a87d` |
| `rss-page-06.png` | Fig.7 normalized components; Fig.8 z/l and r_half/l; Eq.2–3 | `1e9569f117e2b99ffc5dfc22037468d1aeefa0ad65dff69e57fbc61ce2df07ef` |
| `rss-page-07.png` | Fig.9 u/Ui and z/l; TableI; Fig.10 ξ=x/r_half; Eq.4–5 | `07c538a7e82e70413c02665e131ea082683dc340b7387d2d485517437f9d8c85` |
| `README_static.txt` | l and single-PIV variable definitions | `2695a000f2beac1c2f84d645bf6c0b24ca879f5b7ecb8d9873e2b6cfd8e4de6b` |

README dates: created 18 April 2025, updated 5 May 2026. Previously acquired official archive: SHA256 `b495b7a224b3c1db9f15efd5a15815c586e4e11ea29d4df6edcbc25bf50554fa`, 16150227 bytes, CC BY4.0. No archive code was executed for this review.

## Parent disposition before scoring
Adopt normalization/plane findings and the airflow-only endpoint. Retain prospectively chosen equal-cell stride weighting and3fixed axial bins, not the suggested new quadrature/slice weighting. Retain only the2declared fields; no extra unfaded variant. Ui=UH is explicitly conditional. Private absolute acquisition paths replaced by PRIVATE_ACQUISITION/ for publication; source hashes retained.
