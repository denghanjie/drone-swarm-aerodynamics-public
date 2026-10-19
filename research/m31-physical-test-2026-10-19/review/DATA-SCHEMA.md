# Brown static dataset: text-only schema review

**Disposition:** the documentation supports a direct static force/moment comparison, subject to explicit coordinate, baseline, sign, and uncertainty checks. It does not resolve the meaning of the supplied standard-deviation fields sufficiently to construct confidence intervals. No force or moment MAT values have been inspected by this reviewer.

## Sources and inspection boundary

The ordinarily acquired archive is 16,150,227 bytes, SHA-256 `b495b7a224b3c1db9f15efd5a15815c586e4e11ea29d4df6edcbc25bf50554fa`; this reviewer independently verified that identity. CC BY 4.0 and official acquisition provenance are attributed to the parent's inspected Brown landing page. The two text members independently read are:

| Archive member | Bytes | SHA-256 |
|---|---:|---|
| `static/README_static.txt` | 4,960 | `2695a000f2beac1c2f84d645bf6c0b24ca879f5b7ecb8d9873e2b6cfd8e4de6b` |
| `static/plot_FM_data.m` | 2,489 | `f7d19ac69ca303ee1c39a5bfd5e36ec85a7d996b0e61adae46c204607150a8ab` |

Only these text members and archive central-directory names/sizes were inspected. The plotting script was read as text, never executed. No MAT member was opened, no numerical producer/reader/checker ran, and no force/moment array, fitted value, or residual was inspected. The parent’s physical-test design and literature reviews were read for context. The minimal reader and its checks remain forthcoming and are not approved by this schema note.

The README identifies the RSS paper *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, creation on 18 April 2025, and an update on 5 May 2026. Preserve that archive-version identity rather than assuming this text is byte-identical to the original 2025 release.

## Documented variables

| Variables | Documented meaning |
|---|---|
| `x_l`, `z_l` | Coordinates normalized by characteristic arm length `l`; shared ranges for upper and lower vehicles |
| `lower_F_W`, `upper_F_W` | Mean z-direction force/thrust, divided by weight `W` |
| `lower_Fstd_W`, `upper_Fstd_W` | Force standard deviation divided by `W`; statistical interpretation unresolved below |
| `lower_M_Wl`, `upper_M_Wl` | Mean y-direction pitch moment, divided by `W*l` |
| `lower_Mstd_Wl`, `upper_Mstd_Wl` | Moment standard deviation divided by `W*l`; statistical interpretation unresolved below |
| `x_piv`, `z_piv`, `u_piv`, `v_piv` | Separate single-vehicle PIV coordinates and mean axial/lateral velocity normalized by induced velocity `U_i` |

The stated characteristic length is **32.5 mm**. Force/moment values are described as averaged over three trials. This documentation describes aggregate maps; it does not establish that the archive contains trial-level means or raw time series. Do not invent three replicates from a mean and SD.

The sample uses `contourf(x_l, z_l, lower_F_W, ...)` and similarly plots `lower_Fstd_W`. MATLAB's coordinate/grid conventions must be validated against the actual shapes before flattening or transposing. Vector coordinates normally associate x with columns and z with rows; matrix coordinates require elementwise grid association. MAT storage order is column-major. No actual dimensions, grid spacing, ordering, finiteness, or missingness have yet been established here.

The script labels separation axes as `Δx/l` and `Δz/l`, reverses the displayed vertical axis, and sets display limits x=0–8 and z=4–30. Those limits are visualization choices, not verified coordinate extrema or a case list. Its force color range 0.65–1 and SD color range 0.009–0.021 likewise do not establish measured extrema, clipping absence, or test outcomes. No measurement magnitude was inferred from these settings. A reversed plot axis is not a physical sign transformation.

The documented multi-vehicle PIV files and plotting helpers concern separate velocity fields. They should not be silently treated as simultaneous force measurements or extra force replicates.

## Standard-deviation ambiguity: preserve it

The README explicitly calls each `*std*` field a **“Standard deviation over three trials.”** The retained primary-paper review describes the corresponding panels as force/moment fluctuations or unsteadiness, while its methods also refer to repeated trials. These descriptions do not uniquely distinguish between-trial variability of means, within-trial temporal fluctuations, a pooled time-series SD, or an average of trial SDs. Reading the labels does not resolve the ambiguity, and neither label should be silently substituted for the other.

Until trial definitions or data-processing provenance identify the statistic, report it as the **published SD/spread field with unresolved aggregation semantics**. Do not divide by `sqrt(3)` or by the square root of the 20 kHz × 30 s sample count; do not assign a 95% confidence level, a standard error, independent-sample count, or coverage probability. Serial samples are not independent experimental trials. The fields do not by themselves bound calibration, tare, drift, cross-talk, alignment, or baseline uncertainty.

A numerical comparison can report means, residuals, and the published spread descriptively. Any uncertainty interval or resolved-rejection claim must separately state its justified assumptions and missing systematic terms. An SD bar alone is not a calibrated confidence interval or a total physical-error envelope.

## Mapping requirements before force evaluation

1. Validate exact MAT variable names, matrix classes, dimensions, coordinate association, storage order, finite/missing-value policy, and shared upper/lower grid identity. Do not infer these solely from filenames or the plotted axes. Select cases from geometry under a declared coordinate-only step before inspecting force outcomes.
2. Map `l` to the model’s geometry explicitly. The existing square-corner kernel uses Cartesian rotor coordinates `(±arm, ±arm)`, so its center-to-motor radius is `sqrt(2)*arm`. Identifying the paper's `l` with that radius implies `arm=l/sqrt(2)`; identifying `l` directly with `arm` would change the geometry. Physical yaw/layout and propeller dimensions still require independent documentation.
3. Establish the measured axial-force sign/frame, upper/lower association, whether gravity/tare/baseline corrections are already applied, and the meaning of `W`. The paper's approximately 0.265 N normalization is not automatically an exact isolated transducer measurement. A far-separation point is not automatically an isolated baseline.
4. For moments, additionally establish the reference point, y-axis sign, and any load-cell-to-body transform. The README's “pitch, y direction” is insufficient to infer a moment origin. Do not convert an unexplained moment into rotor-force asymmetry.
5. Keep fixed voltage/PWM distinct from constant ideal power. A hardware-matched static prediction tests the combined operational approximation unless independent actuator information separates its components. Freeze any geometry or nominal-force choices before force inspection; do not fit them to the interaction maps.

The eventual minimal MATLAB v5 reader should fail closed on unsupported classes/types, complex or sparse data, inconsistent dimensions, duplicate/unexpected variables, truncated tags, trailing unexplained content, and decompression/size limits. Its ordinary and small-element tags, endian handling, column-major reconstruction, and compressed-element boundaries need independent source inspection and prespecified synthetic checks. Synthetic and coordinate-only checks must not open force/moment values or quietly become a pre-freeze physical test.

Primary dataset: [DOI 10.26300/64d4-wa17](https://doi.org/10.26300/64d4-wa17). Associated paper: [DOI 10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102). This review establishes schema expectations and limitations, not an executed physical-validation result.
