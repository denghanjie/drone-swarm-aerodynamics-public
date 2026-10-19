# Independent paired-component derivation and matching scope

Preparation only, 19 October 2026. No pair enumeration, payload scoring, synthetic control, previous scientific rerun or numerical audit has been executed.

## Matching and coverage

Use only the frozen saved crossstream comparison. A matching vertex is a previously included record; all carried observations and predictions are immutable. Candidate edges connect a negative-X left record to a positive-X right record with the exact same saved Z and abs(X_right + X_left) <= .01 in normalized l units. Neither measured velocity nor residual determines an edge.

Mutual uniqueness means the left endpoint has exactly one admissible right neighbor and that right endpoint has exactly one admissible left neighbor. It is not nearest-neighbor matching, greedy assignment, best residual matching or an arbitrary resolution of duplicates. Each admitted edge yields one ordered (left,right) pair. Preserve the original record indices and declared deterministic pair order. Report unmatched vertices and their reason; preserve zero-X vertices in the coverage denominator even if they cannot be paired by the opposite-sign rule.

For primary Z>=12, define cell coverage as twice the number of primary pairs divided by all prior-included primary cells. The admission conditions require at least twenty primary pairs, at least three distinct primary Z values, and coverage >=90%. An exact integer check 10*(2*pair_count) >= 9*eligible_primary_count avoids a percentage-rounding decision. Do not remove difficult-to-pair cells from the denominator or widen the tolerance after an admission failure. Near/middle/far memberships remain coordinate-only and fixed.

## Independent sum/difference derivation

For one ordered pair with observed v_L,v_R and saved model p_L,p_R:

    E_v=(v_R+v_L)/2,   O_v=(v_R-v_L)/2
    E_p=(p_R+p_L)/2,   O_p=(p_R-p_L)/2.

The inverse transform is v_R=E_v+O_v, v_L=E_v-O_v, with the same relation for p. Define residuals e_R=p_R-v_R, e_L=p_L-v_L and e_E=E_p-E_v, e_O=O_p-O_v. Then

    e_E=(e_R+e_L)/2,   e_O=(e_R-e_L)/2
    e_R^2+e_L^2 = 2*(e_E^2+e_O^2).

Consequently, across N pairs, mean squared residual over the 2N original cells is the sum of mean squared even residual and mean squared odd residual. The corresponding RMSE is sqrt(mean(e_E^2)+mean(e_O^2)). The unscaled component sum of squares is half the original per-cell sum of squares; retain that factor explicitly when reporting energies or normalized fractions.

The same identity holds for observed signal energy and saved model energy. A zero total denominator requires null/undefined fractions; it does not justify excluding cells. No equality of the two component MAEs or additive RMSE identity follows from this quadratic identity.

The paired zero baseline has E_p=O_p=0. The continuity candidate is theoretically odd only at exactly mirrored coordinates. Under the allowed .01 coordinate mismatch, E_p may be nonzero. Therefore compute E_p from both saved predictions and compare it with E_v; never force E_p to zero or attribute all observed E_v to model residual. The audit should independently preserve and recompute these values with Decimal60 from original saved words.

## Scientific scope

Even/odd here names a two-point sum/difference decomposition, not an inferred field symmetry away from the sampled locations. A measured even component can reflect crossflow, coordinate offsets, nonaxisymmetry, swirl or measurement/normalization effects. It does not uniquely identify drift, a correctable bias or any physical cause. Do not subtract it as a newly fitted correction, infer a rotation/translation, adjust the inherited gain, or replace measured values with a symmetry-constrained field.

Use exactly the same admitted pairs for the baseline and candidate and retain signed quantities. Primary evaluation remains Z>=12; the near band is descriptive. Coverage is part of the fixed admission rule, and any conclusions remain conditional on the retained matching pool and prior core restriction. This is a decomposition of already-exposed same-experiment saved data, not new independent validation or uncertainty calibration.

## Frozen audit scope

Independently hash/bind the crossstream input to its prior successful evaluator/auditor and exact-public receipts. Do not import or run old scientific code or recompute the wake/gain. Check every copied original binary64 word and index; independently enumerate the coordinate graph and require mutual degree-one edges, deterministic pair order, no reuse, exact matched/unmatched partition, coverage and fixed group memberships. Recompute all saved E/O quantities and energy identities from saved values with Decimal60 and the declared absolute tolerance. Check the saved matching table and selection.json trace, all pair quantities, four region summaries, and twenty-four side metric groups (left/right/joint × baseline/candidate × four regions). Empty groups have null summaries; zero residual energy has null pooled shares. The primary endpoint is pooled even residual energy divided by pooled even-plus-odd energy, never a mean of per-pair fractions. Preserve source/input/result receipts and enforce the new permanent audit lock, external sixty-second limit and output cap. The evaluator implements its matching test in binary64. The independent audit constructs the coordinate graph with 60-digit Decimal and the exact .01 bound. Any classification disagreement at a numerical boundary fails the audit; neither source may widen the matching interval or choose a more favorable pairing after execution.

The unchanged predecessor full-field subsets remain alongside the paired-only summaries. A favorable paired-support quantity cannot replace the previously reported full-field result. The audit preserves the entire originalCases and fullFieldSubsets JSON trees, including float sign bits, exact integer/boolean/null types, keys and list order. The inherited gain is copied and checked exactly; no wake function, continuity field or gain fit is called.
