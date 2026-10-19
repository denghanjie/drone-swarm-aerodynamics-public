# M31 closure: source-premise and missing-core review

19 October 2026. Source-text review only. The current public archive README and three MATLAB plotting sources were inspected as text; no MAT arrays were opened, no scientific code was executed, and no scores or controls were run. Existing frozen packages were not changed. Geometry/page findings below are attributed to the retained primary-source reviews; no source image was reopened in this pass.

## Normalization: documented convention, unverified implementation

The archive `static/README_static.txt` explicitly describes `u_piv` as average axial velocity divided by induced velocity `U_i` and `v_piv` as average lateral velocity divided by the same named `U_i`. It describes `x_piv,z_piv` as coordinates divided by `l`, with `l=32.5 mm`. Therefore a **common nominal u/v Ui convention is documented**. It would be inaccurate to call that convention undocumented.

`static/plot_FM_data.m` loads prepared MAT variables and calls `contourf(x_piv,z_piv,u_piv,...)` and `contourf(x_piv,z_piv,v_piv,...)` directly, labeling both components with `/Ui`. It reverses the displayed vertical axis only. It contains no construction of Ui, dimensional conversion, camera calibration, stitching chain, or preprocessing sign history for those single-vehicle variables. Thus **the actual common denominator and preprocessing are not independently verified**. The README was updated 5 May 2026; identity with the original 2025 release is not established.

The separate multi-vehicle magnitude scripts `piv_maxF_plot.m` and `piv_maxM_plot.m` contain `vi=sqrt((0.032*9.81)/(2*1.293*pi*(22.5/1000)^2))`. The retained paper review identifies Eq. 1 as `Ui=sqrt(Fz/(2 rho A n))`, with A one rotor's swept area and n the rotor count. The script expression has no explicit n. This is a source-level ambiguity involving different multi-vehicle fields; it neither reveals the denominator actually used for single-PIV u/v nor licenses a factor correction or physical interpretation of the inherited empirical gain.

## Original geometry and later material stay separate

The corrected original geometry is supported by the retained RSS primary-page review: Figs. 3–4 and the statement that horizontal separation `Δx/l=2` aligns opposite rotor columns identify Cartesian motor coordinates `(±l,±l)`, with the original coordinate normalization `l=32.5 mm`. The earlier unconditional interpretation of l as center-to-hub radius was withdrawn before the physical test and must not be revived from historical files.

The existing `review/LITERATURE-REVIEW.md` records the later preprint *The Structure of Merging Turbulent Jets Beneath a Small Quadrotor*, arXiv:2608.30900v1, as using a center-to-hub arm of 46 mm. That primary text was not independently reopened in this pass. The possible geometric relationship between a square layout's Cartesian half-spacing and radial arm does **not** establish identical specimens, records, release versions, processing or normalization. Do not swap the later l into the original archive, transfer dimensionless height thresholds, or call the later records independent validation without a provenance chain. The existing review explicitly says raw-record independence is unestablished.

## Exactly what the off-axis sheet misses

With `X=x/l, Y=y/l, Z=z/l`, the original front-rotor PIV plane is `Y=1`, and cylindrical radius on that plane is `R=sqrt(X²+1)`. Therefore it can sample only `R≥1`. Its line `X=0` lies at R=1, not at the cylindrical axis. The entire inner interval `0≤R<1` is geometrically unobserved by this plane, before any masks or finite X/Z coverage are considered. This geometric bound does not assert that the saved grid contains X=0, every outer radius, or any particular valid sample; those values were not inspected here.

Under steady incompressible axisymmetry, sufficient smoothness and a regular axis,

    R Vr(R,Z) = −∂Z ∫₀ᴿ s U(s,Z) ds.

For R≥1, write `C(Z)=∫₀¹ s U(s,Z) ds`. Then

    R Vr(R,Z) = −C′(Z) −∫₁ᴿ s ∂Z U(s,Z) ds.

The sheet does not supply C′(Z) from its measured axial field. Regularity removes a singular integration term only after the axial field is specified through the missing core; it does not reconstruct that field from off-axis axial observations. Under extra assumptions and adequate lateral measurements, one could constrain a net core term from the lateral relation, but that would use lateral evidence to close it, not independently predict lateral velocity from the axial sheet.

Further limits matter: without axisymmetry, a plane cannot define the complete radial disk. At Y=1 the projection is `Vx=Vr X/R−Vtheta/R`; interpreting measured v as solely the radial projection requires zero mean swirl, and division by X/R cannot recover Vr at X=0. The in-plane divergence `∂X Vx+∂Z U` omits `∂Y Vy` and cannot establish three-dimensional continuity. The previous continuity candidate supplied the unseen core and three-dimensional extension through its model. The restriction ξ≤2 avoided a model taper inside the integration disk; it did not make that disk measured.

## Safe Three.js saved-evidence and geometry view

Display the rotor geometry, source axis, and translucent plane Y=1 in the original dimensionless coordinates. Mark the cylinder R<1 distinctly as **“not sampled by this measurement plane”**, including a top view that makes the tangency at X=0 legible. Keep that geometry annotation visually separate from saved measurements and model evidence.

Show only already saved evidence records/plots with their existing provenance and labels. Preserve the archive's component directions and units. Keep any previously saved candidate evidence explicitly labeled as a model completion. Do not create a colored core, new vectors, a revolved measured volume, interpolation presented as observation, new field evaluation, integration, fitting, residuals, scoring or scientific controls. Camera movement and geometric primitives are presentation operations, not new scientific results. A small evidence panel should state: common nominal Ui is documented; preprocessing is unverified; R<1 is unsampled by this plane; later 46 mm material has no established record identity with this archive.

## Inspected source identities

- `static/README_static.txt`: 4,960 B; SHA-256 `2695a000f2beac1c2f84d645bf6c0b24ca879f5b7ecb8d9873e2b6cfd8e4de6b`.
- `static/plot_FM_data.m`: 2,489 B; `f7d19ac69ca303ee1c39a5bfd5e36ec85a7d996b0e61adae46c204607150a8ab`.
- `static/piv_maxF_plot.m`: 3,534 B; `e879b41afdaf44053323c06e81c3eaf6bc1b07c7870428bbd59de49ace4a066d`.
- `static/piv_maxM_plot.m`: 3,593 B; `05da70dae934e6018a4d5c523c7398ec29177216448bf50d281c87d6549296d3`.

All four hashes were rechecked from source-text archive members in this pass. Retained reviews: `research/m31-physical-test-2026-10-19/review/GEOMETRY-CORRECTION.md`, `research/m31-physical-test-2026-10-19/review/LITERATURE-REVIEW.md`, `research/m31-crossstream-test-2026-10-19/review/GEOMETRY-AND-CONTINUITY.md`, and `research/m31-airflow-scale-transfer-2026-10-19/review/NORMALIZATION-SOURCE.md`.

References: RSS paper [DOI 10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102); released archive [DOI 10.26300/64d4-wa17](https://doi.org/10.26300/64d4-wa17); later preprint [arXiv:2608.30900v1](https://arxiv.org/html/2608.30900v1).
