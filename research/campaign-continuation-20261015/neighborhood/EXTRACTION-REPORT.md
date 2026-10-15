# Frozen neighborhood observations, awaiting review

2026-10-15 UTC. One collection pass completed; no observed ratios, model calls, predictions, residuals or fits.

The new observation definition retains 11 measured centerline response markers plus the unchanged, certified pilot anchor: 12 distinct markers. Neighborhoods 11/14/17 contain three responses each; neighborhood 20 contains two. Seven response intervals cross a neighborhood boundary and remain included with full, unclipped coordinate bounds. Each neighborhood has at least one whole-window-eligible observed marker. No marker is assigned to multiple neighborhoods.

The original strict-nearest pilot remains failed. This collection does not retroactively pass its gate or preserve its original five-point estimand.

## Source and extraction

The existing 560x420 original figure and frozen affine calibration were reused without recalibration. Pilot anchor and target-11 completed reads were reused unchanged. Three provisional pilot first reads were completed; seven additional response markers received two reads. The first new read was visual; the second used the unchanged orange-color threshold and visible-orange bounding-box midpoint. Both read the same raster and are not independent experimental observations.

Orange centerline pixels remain visible for every included marker. Purple maximum rings overlap them, and the black fitted line occludes parts of several markers. Neither purple centroids nor the fit were substituted. The last marker's disconnected orange pieces were grouped across one empty pixel column, preserving their full bounding box. This grouping did not join neighboring markers, whose gaps are much larger.

Visible-orange pixels are sparse near the downstream end: m486 has 9 threshold-matching pixels and m501 has 13. Partial occlusion can bias a visible-portion center; the prescribed pixel bounds are descriptive extraction bounds, not a metrological guarantee or experimental error model. The frozen evidence records this limitation instead of assigning invented additional uncertainty.

## Coverage and checks

Target 20's nominal window is [19.25,20.75], but the source plot ends at z/l=20. Its two observed candidates do not establish full-window coverage; no unplotted marker was inferred. Partial-eligibility flags describe interval/window intersections, not known physical membership.

All included coordinate lower bounds satisfy the exact far-field floor 2.5*lambda. All velocity lower bounds are nonnegative and the anchor's is strictly positive. The fixed nominal geometry is lambda=2sqrt(2), eta=1; plane-position and experimental mean-velocity uncertainty remain unknown. These checks permit an extraction review, not physical validation.

## Evidence and next gate

measurements.json and measurements.csv preserve actual coordinates and bounds. selection.json lists every included and excluded x-only candidate, neighborhood membership and source truncation. read-1-new.json and read-2-new.json preserve raw pixel readings, visible extents and overlap descriptions. freeze-extraction.py reproduces calibration and membership arithmetic without importing or evaluating the wake model.

evidence-freeze.json records all current hashes and references the unchanged pilot evidence. The combined retained size is below the 1,000,000-byte cap. The original figure is not authorized for public redistribution.

Stop here for independent extraction review and root release before the single bounded evaluation pass.
