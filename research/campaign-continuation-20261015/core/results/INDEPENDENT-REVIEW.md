# Independent saved-result review

2026-10-15 UTC. VERIFIED: six complete fixtures satisfy the conditional finite all-rotor omission certificate. This review made no wake calls and did not rerun the benchmark. It reconstructed deterministic input geometry in memory for hash/count verification and recomputed finite bounds from saved layer counts and rotor sums.

## Integrity, coverage and resources

All six fixture JSON byte counts and SHA256 hashes match summary.json. The plan, runner and four public source files still match their reviewed hashes. The release binds the same plan and runner. The supervisor records exit 0, no timeout and empty stderr; summary, progress and receipt consistently report six completed fixtures, 8,436 source/rotor pairs and 16,872 arm slots. This is complete coverage, well below the declared evaluation ceiling.

Independently reconstructed the ordered Float64-LE xyz triples from the frozen lattice definition, without retaining new coordinate files. All six coordinate hashes, exact layer/source counts, uniqueness and coordinate prefixes match. Source counts are 19/131/911 for phase 0 and 20/128/900 for phase 0.125, at extents 2/4/8 m. Both phases have 7/15/31 enumerated layers, including empty layers where appropriate.

Recomputed the physical constants from frozen source values, layer radii, axial fade weights, cell-area count bounds, B, lower/upper omission bounds, rotor differences, fractions, slacks, normalized inflows and cross-extent ratios. Rechecked witness coordinates and geometry and the maximum xi over all source/rotor pairs. There were 770 numeric comparisons within the planned 1e-12 relative-or-absolute tolerance, plus exact count, byte, hash and binary64 prefix/equality checks.

The supervisor wall time is 0.11923798 s, child CPU 0.162209 s and observed maximum RSS 54,439,936 bytes. These are resource receipts, not comparative performance measurements. Before this review, outputs were 45,113 bytes and the campaign 72,127 bytes; both remain comfortably below the 100,000/200,000-byte caps with this file.

## Verified finite results

The following uses rotor 0 for compactness; all four rotors were verified independently. P and X have units m/s within the stipulated scalar model. Omitted fraction is (X-P)/X.

| Horizontal phase | L (m) | Sources | P | X | Omitted fraction |
|---|---:|---:|---:|---:|---:|
| 0 | 2 | 19 | 17.810680 | 17.810680 | 0 |
| 0 | 4 | 131 | 19.819440 | 57.251548 | 65.3818% |
| 0 | 8 | 911 | 19.819440 | 203.764215 | 90.2733% |
| 0.125 | 2 | 20 | 12.939923 | 12.939923 | 0 |
| 0.125 | 4 | 128 | 14.340311 | 51.488582 | 72.1486% |
| 0.125 | 8 | 900 | 14.340311 | 197.310364 | 92.7321% |

At 2 m, the omitted sum and both bounds are exactly zero. For phase 0 the finite omission bounds are [13.08432684,92.36062109] m/s at 4 m and [65.55580930,462.75023080] m/s at 8 m. For phase 0.125 they are [13.01363222,91.86159666] and [64.86126069,457.84749932] m/s. Every saved rotor difference lies within its corresponding bounds; all 4/8 m lower bounds are positive. The bounds are intentionally broad and are not tight physical uncertainty estimates.

P(4) and P(8) are binary64-identical per rotor in both phases. X(8)>X(4)>X(2) for all eight phase/rotor combinations. The X(8)/X(4) ratios are approximately 3.559104 and 3.832119 for the two phases. This is finite extent growth, not an estimated asymptotic exponent.

The largest geometric xi is 1.989922183693113, strictly below 2. All 8,436 recorded radial weights are exactly one. The support-envelope bound is 2.630711448903349 m, below the 3 m neighbor radius. Thus the effect is not caused by radial taper removal or center-neighbor culling in these fixtures. The positive near-field margin and coordinate reconstruction independently establish the admitted geometry.

The maximum recorded aggregate-versus-direct omission cancellation residual is 1.4210854715202004e-13 m/s; independently recomputed differences agree with the saved direct sums. Closed-form/profile checks are recorded by the released runner; this review does not claim to have repeated the kernel evaluations or independently established the maximum individual term from all source velocities.

## What this establishes

The test supplies a finite, rotor-aware example and certificate: original fixed axial support can hide growing accumulated inflow in the unchanged independent-source formula even when every contribution lies inside its code-defined radial core. Existing finite-support pruning guarantees remain guarantees relative to P. The analytic growth-order argument is separate from these six finite checks.

The populations are static mathematical stress fixtures, not Boids flight, measured multi-source flow or physical truth. Core membership does not validate the axial continuation to 8 m. X/vi reaches about 48.93–50.53 at 8 m, emphasizing the extreme aggregate extrapolation rather than establishing actual aerodynamic velocities. Source interaction, entrainment, boundaries, wake age, compressibility and receiver response are absent. The result alone proves neither momentum violation nor a required physical cutoff.

The existing genuine local3D fixed-state replay remains useful context but had no axial-cutoff exposure and was not rerun. The separate single-source normalized-shape screen cannot validate this aggregate behavior. Report this as a conditional mathematical certificate with finite bounds, without novelty, flight-performance or empirical-validation claims. No retuning or further model run was needed for verification.
