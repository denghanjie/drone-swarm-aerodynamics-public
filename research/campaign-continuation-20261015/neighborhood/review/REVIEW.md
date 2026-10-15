# Independent review: neighborhood observation protocol

2026-10-15 UTC. READY for root adoption and one collection pass, subject to the two reporting conditions below. Evaluation still requires a frozen extraction record and independent extraction review. This review performs no new digitization, ratios, predictions or kernel calls.

Reviewed PLAN.md: 2,975 bytes, SHA256
58ad86b32d4e47cae09a4fb3b02e98513846246e50e239b36bcd16ed767dd451.

## Failed pilot remains a valid stopping result

Verified all 12 file sizes and hashes in the pilot evidence-freeze.json, SHA256 fd0c462a38aa82589492472dc881ede6fe43bc1ff9f0eb34566af577922f70bd. The terminal record confirms target-11 selection failure, zero model calls and no observed ratios. Pilot evidence totals 70,149 bytes and is unchanged.

Checked the shared-affine calibration: five x vertices and six y vertices enclose the tick bounds. Slopes retain their signs; fractional-affine extrema occur at vertices and pixel endpoints. Recalculated saved witness bounds without importing the model.

Anchor 8 passes narrowly: selected distance upper bound 0.36801242236024834 is below the next marker's lower bound 0.3773291925465845, margin 0.009316770186336143. At target 11 the selected x=310 +/-3.5 pixels gives z/l in [10.613354037267081,11.11888111888112]. Its distance upper bound 0.38664596273291885 exceeds the competing x=326 +/-3.5 marker's lower distance 0.3586956521739122. The required strict inequality fails by 0.027950310559006653. This is a failed conservative extraction certificate, not evidence of wake-law error or proof that the competitor is truly nearer.

## New observable is scientifically defensible

The new protocol changes the observable from four uniquely nearest responses to four sets of plotted centerline observations, all sharing the already frozen anchor. This separate study follows extraction failure but precedes any residuals. It has no nearestness filter, residual-based selection, anchor optimization, or retrospective pilot success claim.

Including every measured orange marker whose full horizontal interval intersects a fixed window is a conservative, reproducible observation rule. Keep actual coordinates, full intervals, partial-eligibility flags and all qualifying markers. Do not clip coordinates to the window or silently omit its uncertain boundary markers. New markers require two reads under the unchanged bound rule; provisional reads are incomplete. Stop if orange identity is hidden, rather than substituting purple maxima or a fitted curve.

Adoption conditions:
1. The source plot ends at z/l=20. The nominal target-20 window extends to 20.75 and therefore has truncated source coverage. Record the observed plotting domain and coverage limitation explicitly; do not invent unplotted candidates or claim completeness over the whole requested window. An obscured or clipped marker remains a measurement failure.
2. If no marker interval lies wholly within a window, the possible-empty-set flag means that membership is not guaranteed by these marginal bounds. Shared calibration may forbid simultaneous exclusion of every marker. Do not claim a jointly feasible empty set unless established independently; the conservative flag alone is sufficient here.

## Bounds, interpretation and resource limits

Use each response at its own coordinate, with the nominal plane mapping lambda=2sqrt(2), eta=1 and the exact downstream floor 2.5lambda. With all response lower bounds nonnegative and anchor lower bound positive, observed ratio bounds are [response_low/anchor_high, response_high/anchor_low]. The previously checked decreasing-profile proof supplies endpoint model bounds. Coordinate-matched residual bounds are [observed_low-model_high, observed_high-model_low].

Only these paired residual intervals may be unioned or hulled within a neighborhood. Pooling observed and predicted ratios separately could manufacture apparent overlap across different coordinates. A hull is a conservative summary of several plotted observations and extraction bounds, not one measured value at the neighborhood center. Zero inside a hull does not establish a matching candidate, simultaneous agreement, a confidence level, or physical validation.

The common anchor and affine calibration induce dependence across every ratio; extra markers and repeated raster reads are not independent experimental replicates. Ratios cancel a common multiplicative amplitude only. Additive offsets, spatially varying/stitching calibration, unknown measurement uncertainty, nominal plane geometry, axial-mean versus modeled-magnitude mismatch and scale extrapolation remain unresolved.

The 15-marker cap, 45-call ceiling, unchanged bounds, extraction-review gate and 1,000,000-byte budget suit this bounded screen. Count referenced evidence once logically and preserve every terminal failure. Readiness authorizes no evaluation before the separate extraction review.
