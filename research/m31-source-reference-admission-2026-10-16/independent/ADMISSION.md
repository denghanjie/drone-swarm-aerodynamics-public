# Independent Figure 7 extraction admission

2026-10-16. Read-only extraction from Bauersfeld et al., arXiv:2403.13321v3, page 5, Figure 7. Private PDF SHA-256: `81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c`. The full page was visually inspected; numerical geometry was recovered independently with pypdf 6.10.0 ContentStream operators and graphics-state/CTM traversal, without pdfplumber or dependency installation.

**Admission:** the two measured median polylines can be identified and calibrated independently. This admits extraction of the displayed figure coordinates only. No physical contrast, model fit, significance test or SEM transformation was performed or admitted here.

## Axes and normalization

Figure 7 is page Form `/Im7`. Page operator 252 invokes it after a translation of (317.280, 441.611) pt; form operator 2 adds (33.106, 23.798) pt. Its plot-local rectangle is x=0..198.42685 and y=0..99.21342 pt. The page top-origin plot box is x=350.386..548.81285, y=227.37758..326.591 pt.

The visible axis labels and grid establish x=0..3, with ticks every 0.5, and y=0..1.5, with ticks every 0.25. Thus x_normalized=3*x_local/198.42685 and y_normalized=1.5*y_local/99.21342. Boundary stroke S144, grid strokes S29/S53, and label operator locations are recorded in the evidence file. All operator indices are zero-based within `/Im7`, unless labeled as page operations.

Independent reading of section III-D on PDF page 3, equations (7)/(8), confirms speed normalization by U_H and spatial normalization r/l. The displayed profiles are at normalized downstream station s/l=3.0. These are not normalized by a fitted profile center, width or peak. The motor-distance geometric convention is not resolved further by this extraction.

## Selected and excluded objects

| Object | Exact encoded stroke or fill | Operator identification |
|---|---|---|
| Offboard 1 median | DeviceRGB (0.85, 0.325, 0.098), stroke width 0.79701 pt, alpha 1 | m856 through S897; legend S1115 with label TJ1135 |
| Offboard 2 median | DeviceRGB (0.929, 0.694, 0.125), stroke width 0.79701 pt, alpha 1 | m910 through S941; legend S1153 with label TJ1173 |
| Offboard 1 shaded band | Same RGB, fill alpha 0.2 | f316; excluded |
| Offboard 2 shaded band | Same RGB, fill alpha 0.2 | f397; excluded |
| Fitted curve | Effective DeviceGray 0, black | m1290 through S1390; excluded |

The fit is black because G1289 overrides the preceding purple RGB instruction. Selecting by the earlier RGB setting alone would misidentify it. Legend strokes are separate short horizontal paths, not data profiles.

## Visible coordinates and clipping

The complete encoded Offboard 1 and Offboard 2 paths have 41 and 31 vertices respectively, and extend beyond the displayed x=3 clip boundary. Each has sixteen original vertices inside the displayed axes, from x=0 through approximately 2.85714282. The public handoff includes exactly those sixteen original vertices per series and one explicitly labeled x=3 display-interpolation endpoint per series. An endpoint created by clipping is not an additional measurement vertex. Off-axis vertices and the full path records remain in a separate private file; only their hashes and operator identity are in the public handoff.

## Extraction uncertainty and limits

The coordinate source is the encoded vector centerline, rather than raster pixels. Plot coordinates are encoded to 0.00001 pt. A conditional half-last-digit estimate is about 7.56e-8 in either normalized coordinate, if nearest rounding was used by the PDF exporter; it is not a guaranteed bound on the original measurement data. The proposed 1e-6 cross-extractor tolerance is only a numerical reconciliation tolerance. The approximately 0.006025 normalized half-stroke width describes the rendering footprint and is not statistical uncertainty.

The caption identifies colored lines as medians and shading as a one-sigma uncertainty region around the mean. Raw samples, effective sample sizes, correlation structure and a median uncertainty model are absent from this extraction. No conversion of the shaded region to SEM or a confidence interval is justified. Figure coordinates may be used as a labeled descriptive extraction; recovering raw measurement values or establishing a physical difference would require additional evidence and an explicit later analysis scope.

No paper or figure image is included in the public handoff. `PRIVATE-FULL-PATHS.json` must not be copied into a public package. The public-only inventory identifies the script, visible coordinates, operator/calibration evidence and this memo.
