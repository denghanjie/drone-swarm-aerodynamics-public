# Coupled-cost kernel and tiny controls: source-only review

2026-10-16. Reviewed kernel source against the unchanged prior experiment and
reference pairTerm. No target state values were read, no JavaScript was imported
or executed, no controls or model calculations were run, and no timings were
measured. All review writes are confined to this private review directory.

Initial kernel SHA256:
`a3399f7a08752832ef876c727295a40a7c735e86cc15902961ab86bbb3b78bbb`.
Revised kernel inspected after the coordinator's fixes:
`c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a`.
Reference excerpt in both old and new packages has identical SHA256
`ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e`.
Initial inspected experiment/control harness SHA256:
`90fd676e365aad337cd58e38adee220ee65edf675ed18cc1bfe864eab9b92cdd`.
Final inspected experiment/control harness SHA256:
`ff9d35d168e2a8c1e843245724e4c4d8f762df21f986fffce834c66506a0c287`.

## Definite issues raised and source dispositions

1. Initial A/all-pairs build unnecessarily scanned the bounding box and allocated
   an empty Map. That overhead is not required for an all-pairs baseline and can
   favor the grid's relative timing. **Resolved:** revised indexScene returns an
   explicit all-pairs-selected record before the scan/Map allocation.
2. Initial all/fallback candidates allocated an N-ID array for every receiver,
   adding N-squared ID writes absent from the original simple numeric loop.
   **Resolved:** revised all/fallback traverses numeric j directly; only a
   certified grid gathers/sorts candidate IDs.
3. Initial solve threw on Picard nonconvergence before returning its final
   amplitudes, rotor records, work and available iterate trace. **Resolved in
   kernel:** revised solve returns the full nonconverged final record. The
   qualification harness persists full solutions before rejecting comparison.
   **Initial harness scope caveat:** initial timed failure records retain timing,
   counters, hashes and mismatch statistics, not the full available final
   solution arrays. Requested either failure-only persistence of result.s,
   without another solve, or explicit documentation of that limited retention.
   **Resolved in final inspected harness:** a failed repeat saves the complete
   available result.s and mismatch record before throwing, without another solve;
   numeric comparisons additionally retain the first mismatch index/values.
   As with other artifact writes, this is subject to the output allocation. Raw
   timing records are persisted before validation; budget exhaustion remains a
   recorded failure, not permission to rerun.

## Positive mathematical/source findings

- Constants, quaternion xyzw cross-product rotation, rotor ordering, nominal
  sums, input checks, scaled-cap calculations and a construction match the prior
  experiment. No normalization, force clipping or rotor-world arithmetic change
  was introduced.
- A finite per-axis rounded span <=256 suffices for the planned center-guard
  certificate. Only certified grid paths form local bins. Failed certificates
  use the complete canonical center traversal. Original positions remain the
  source of center and rotor arithmetic.
- Cell width4, floor-based local bins, inclusive floor((u±3)/4) with one-cell
  padding, complete bucket insertion and numeric source-ID sorting implement the
  proposed conservative enumeration. Local indices are bounded by the certificate;
  nonfinite/overflowing positions never enter bin loops. No occupancy truncation
  appears in source.
- Every visited nonself center applies nonfinite/norm>512/component>257 guards
  before the >=3 exit. The strict <3 neighborhood, four pairTerm calls and
  canonical positive-K source order are preserved.
- Initializing all4N² symbols/counts to1 and decrementing count1 once for every
  non-1 classified rotor is sound here: each receiver/source is visited at most
  once, each rotor is classified once, and skipped/self entries remain1.
  Source-order/uniqueness assertions reject repeated candidate IDs.
- Unique source sets recover graph edges. For finite z, testing
  `z_j > z_i || (z_j === z_i && j < i)` is equivalent to rank_j<rank_i under the
  stated descending-z/ascending-ID order. Height violations remain separate.
  This equivalence is qualified to finite positions, as guaranteed for extracted
  inputs; no claim is made about JavaScript comparator behavior on NaN states.
- Root closure uses the same56 loop iterations for positive alpha and exact1 at
  alpha0. Direct and synchronous maps preserve per-row source order and four-root
  retention. Picard starts at ones, caps at64 and tests the same1e-11 log change.
  Final residual and source/receiver mismatch arithmetic is unchanged.
- Cold query paths include their selected setup/build, schedule where used,
  solve, residual and checksum. Full tensor persistence is outside timed query
  calls and must be named as such in the eventual estimand. Cached paths are a
  distinct reuse measurement, not complete-query measurements.

## Tiny-control source assessment

The coordinator clarified that the eventual21 controls deliberately run both
production scalar builders and pairTerm/K inside the allocated post-freeze
candidate; they do not run load solvers. This review did not run them.

The initial source defines exactly21 fixtures: six radius fixtures at receivers0
and-6, three cell fixtures, signed zeros, two coarse translation fixtures, dense16,
two span fixtures, far258, NaN, Infinity, overflow span, near field, and duplicate
positions. nextUp/nextDown is used only on finite nonzero values in these fixtures;
its limited helper domain is sufficient for those calls.

Good boundary choices: cell fixtures contain the separate0 origin anchor;
nextUp256 uses min0; translation2^40 uses coarse representable offsets instead of
pretending near-origin ulp perturbations survive translation. Coincident sources
retain separate IDs. Far258 explicitly exercises invalid-before-outside, and the
span just over256 exercises fallback without forcing physical invalidity.

Two control improvements were requested before freeze:

1. The initial21 fixtures all have y/z extents below4, so incorrect y/z bin/stencil
   behavior can evade the small controls. Rotate the three existing cell fixtures
   across x/y/z, or include equivalent triple-axis pairs within those same fixtures;
   no additional target or allocation is required. **Resolved:** the three cell
   controls now rotate their4m boundary across x,y,z while retaining the0 anchor
   and nearby paired point. The case count remains21.
2. Independently recount each saved symbol buffer and compare it with the
   incremental symbolCounts. Cross-arm tensor equality alone does not validate
   a count bug shared by both builders. Existing target qualification later
   compares counts to prior records, but tiny controls should retain their own
   direct count invariant as well. **Resolved:** the final control pass condition
   independently recounts each arm's symbol buffer against its declared counts.

## Final disposition and limits

Kernel reread found no remaining numerical/geometry blocker at the revised hash
above. All raised source findings and control improvements are resolved in the
exact final hashes recorded here. This is a static readiness conclusion limited
to the reviewed kernel and control/failure-handling portions of the harness; it
does not replace complete runner/protocol/publication review.

No runtime qualification, boundary evidence, benchmark permission, performance
evidence or physical validation follows. The separate CHECKLIST.md records the
prospective boundary expectations and the coordinator's control-scope
clarification. No JavaScript, target calculation, control or timing was executed.
