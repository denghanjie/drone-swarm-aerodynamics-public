# Static review of the exposed-profile protocol and scripts

Reviewed 2026-10-16, before physical-contrast calculation. Files read from
`research/m31-source-reference-admission-2026-10-16`:
`PROFILE-PROTOCOL.md`, `extract_profiles.py`, and `analyze_profiles.py`.
This review covers the versions initially read in this task; subsequent edits
require acknowledgement or a targeted reread. No PDF, extracted physical input,
scientific script, synthetic test or contrast calculation was run here. No public
worktree file was edited.

## Verdict

The fixed descriptive experiment is sound within its stated limitations. The
weighted-square polynomial is algebraically the integral of `x` times the square
of the linear segment: its local-coordinate coefficients are correct. Forming the
union of knots makes the profile difference piecewise linear, so the maximum
absolute difference occurs at a union knot. The radial L2 numerator, Offboard 2
reference denominator and square root implement the declared discrepancy.
The optional dimensional conversion retains the target hover-normalizer and does
not fit a gain. No broader evidence acquisition is needed for this audit.

## Findings and minimum remedies

1. **Distinguish a unique intersection from a downward crossing.**
   `analyze_profiles.py:21–32` returns `unique: true` for a sole tangential contact,
   for example the synthetic shape `(0,2), (1,1), (3,2)`. It reaches half its
   centerline value and returns above it; it does not cross downward. This does
   not invalidate an *all-intersections* statistic, which the protocol explicitly
   requests. Either retain that precise name and avoid inferring a width, or add
   direction/contact classification before calling it a half-speed crossing or
   width. The saved synthetic checks cover missing, multiple and plateau cases,
   but not this tangency. Endpoint intersections similarly need to remain
   endpoint intersections unless the visible curve establishes a crossing.

2. **The standalone analyzer does not enforce its named input contract.**
   `analyze_profiles.py:76–79` takes the first two profile arrays in arbitrary JSON
   order, while `:48` labels the denominator Offboard 2. It does not check the
   source PDF hash, schema, names/order, exact axis/domain metadata or strictly
   increasing finite knots. The prescribed fresh extractor supplies several of
   these properties, so this is not evidence that the intended input is wrong.
   Add small explicit admission checks, or preserve an external frozen gate that
   verifies them before invoking this standalone analyzer. A reversed pair must
   not produce a result still labeled as Offboard-2-referenced. Preserve the
   requirement that independent extraction agreement occurs before contrasts.

3. **Tighten the hardware wording in the saved result.**
   `analyze_profiles.py:88` says “same-frame hover pair.” The admitted fact is
   matching tabulated frame dimensions and propeller diameter. Prefer “pair with
   matching tabulated frame dimensions” unless actual frame/hardware identity is
   separately established. The protocol already disclaims causal loading and
   independent validation; the machine-readable scope should be equally precise.

## Bounded verification notes

- `extract_profiles.py:26–38` is adequate for straight, monotone-x segments whose
  retained vertices are within the stated y range: linear segments between them
  cannot escape that rectangle. The independent content-stream inspection should
  also establish that the selected paths are one straight-line subpath each;
  flattened point arrays alone do not prove the absence of Bézier commands or
  move-to discontinuities. This is a check on the already acquired source, not a
  request for another dataset.
- `maximizing_radii` uses a `1e-14` near-tie tolerance, and crossing deduplication
  uses `1e-12`. These are numerical reconstruction tolerances, not physical
  uncertainty. Describe near ties accordingly if the distinction is material.
- Plateaus are exposed as intervals and make `unique` false. Shared-vertex hits
  are deduplicated. A missing intersection remains visible as an empty list.
- Independent quadrature is promised by the protocol but is not implemented in
  this analysis script. It can remain a separate saved-result review, provided
  that check actually occurs before final scientific reporting.
- Graphical half-stroke widths are reported as display context only. The absence
  of physical confidence intervals and physical pass thresholds is appropriate.
  No bootstrap, SEM, source-law validation, motor-response conclusion or swarm
  feasibility claim is supported by these polylines.

These findings do not recommend changing the domain, metrics, source pair or
experimental plan. They concern faithful admission and interpretation of the
frozen bounded comparison.
