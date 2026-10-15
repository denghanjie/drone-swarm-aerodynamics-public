# Independent extraction review

2026-10-15 UTC. READY for root release of the single bounded evaluation pass: 12 markers, at most 36 scalar kernel calls (center and two coordinate endpoints each). No new observation values, observed ratios, model predictions or residuals were produced in this review. Frozen reads were not changed.

Reviewed extraction manifest: evidence-freeze.json, 1,796 bytes, SHA256 b3c14e51a256f161df96f5f1df96c1b42d3c3cb2abed7869272a58b4fe1a01de. Verified all 10 listed new-file sizes/hashes and all 12 files in the referenced pilot freeze. The unchanged adopted plan is SHA256 58ad86b32d4e47cae09a4fb3b02e98513846246e50e239b36bcd16ed767dd451. The records consistently state zero kernel calls and no observed ratios before review. Combined retained evidence before this report is 115,347 bytes, well below the 1,000,000-byte cap.

## Independent verification

Read the original figure, legend, adopted protocol, both new read records, pilot read records, calibration, measurements, selection and freeze script. Recomputed saved extraction arithmetic independently in memory; did not execute the supplied freeze script or import the model.

Applied the already frozen orange threshold to the original raster only to verify the saved records. Within the declared scan band it reproduces all 15 occupied-column groups, the ten new/repeated marker bounding boxes and their orange-pixel counts exactly. The grouping joins occupied columns separated by at most one empty column; all between-marker gaps are larger. It therefore combines the final marker's disconnected orange fragments without merging adjacent markers. This is a recorded collection detail chosen before predictions, not a preregistered subpixel recovery method.

The figure legend identifies orange as measured centerline velocity. The saved second reads use these orange fragments; they do not use purple ring centroids or the black fit. Their bounding-box midpoint rule and inclusive extent convention agree with the records. Every included marker has visible orange pixels. Entirely hidden/unplotted identities cannot be reconstructed or certified absent from raster colors alone; completeness is limited to identifiable plotted markers under the declared scan and inspection scope.

Recomputed average read centers and half bounds as max(2 pixels, inclusive visible extent/2 + 1, absolute repeated-read difference). Recomputed every coordinate and velocity endpoint over the frozen feasible affine-calibration vertices and pixel endpoints, with agreement within 1e-12. CSV and JSON values agree. The anchor and completed target-11 numerical records match their pilot records exactly. The provisional target-14/17/20 first reads were reused and completed, rather than silently replaced. No calibration or bound was reduced.

## Membership and guards

Independently tested each saved interval against all four closed windows, retaining touching endpoints. Eleven responses are included: target 11 has m294/m310/m326; target 14 has m358/m374/m390; target 17 has m422/m438/m454; target 20 has m486/m501. Four x-only groups are outside every window and were excluded. No response belongs to multiple neighborhoods. The unchanged anchor makes 12 distinct markers, below the 15-marker cap.

Seven response intervals cross window boundaries and remain fully retained: m294, m326, m358, m390, m422, m454 and m486. Every neighborhood also has a wholly contained response interval, so none needs the conservative unguaranteed-eligibility flag. In particular, m326 retains its upper bound 11.864801864801866 beyond the first window, and m486 remains included although its central coordinate is below 19.25. The final marker retains its full upper bound 20.04705882352941; it is not clipped at the source boundary.

All lower coordinate bounds exceed the exact model floor 2.5*(2*sqrt(2)). All lower velocity bounds are nonnegative; the minimum is 0.3549407114624506. The fixed anchor lower velocity bound is 0.5027667984189723, strictly positive. These are domain/ratio arithmetic guards, not physical-validity findings.

Target 20 has only plotted-source coverage through z/l=20, short of its nominal upper window boundary 20.75. selection.json and EXTRACTION-REPORT.md explicitly retain this limitation. There are no invented points beyond the plot and no claim of full-window completeness.

## Conditions on interpretation and evaluation

Partial occlusion is material: the last two orange fragments contain only 9 and 13 threshold-matching pixels. Purple rings and the black fit can shift a visible-portion midpoint. The declared bounds describe raster extraction and do not guarantee coverage of the underlying plotted center, experimental uncertainty, geometry uncertainty or calibration errors outside the adopted bounds. The evidence reports this honestly; readiness is for a conditional descriptive screen only.

Evaluate every frozen response at its own actual coordinate; retain all partial-eligibility observations. Use the same fixed anchor and nominal geometry throughout. Only coordinate-paired residual intervals may be unioned/hulled within a neighborhood. Do not pair an observed ratio at one coordinate with a model ratio at another or select candidates by residual. A hull containing zero does not establish a matching candidate or simultaneous agreement. Shared anchor/calibration dependence and repeated readings of one raster preclude treating these as independent replications.

Ratios remove only a common multiplicative amplitude. Additive offsets, stitched-field or spatially varying calibration, nominal plane position, measured axial mean versus modeled magnitude and scale extrapolation remain unresolved. Preserve the failed nearest-marker pilot and disclose the changed neighborhood observable. Freeze all evaluation outputs, preserve any failure, and stop after the one authorized pass; no retuning or recollection follows from this readiness decision.
