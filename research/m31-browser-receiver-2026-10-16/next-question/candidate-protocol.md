# Candidate protocol: stored geometry to wake terms to inflow

2026-10-16. **STATIC, UNSELECTED, UNEXECUTED.** This document is not a launch authorization or a new active budget. It must not change or reopen R8, the full-flock reference, source-omission, zero-screen, receiver or saved-review ledgers. No timing campaign is proposed. The current receiver result is preliminary and independent review is pending; do not assume it qualifies, and do not run its roots again here.

## 1. Single question and decision unit

Can an actual browser f32 component preserve the declared finite-support M28 `sum-rotor` wake terms and summed inflows for four selected receivers in the exposed `fresh5000` input, with the contribution of packing, geometry/branches, term arithmetic and addition separated?

The tested unit is a static four-receiver slice with all 5,000 sources, plus 32 comparator controls. There are sixteen receiver-rotor sums. It is not a 5,000-receiver field call, a benchmark, a new neighbor algorithm, a physical validation or a coupled Boids run. No source omission, grid, root solve, body/world wrench, controller or integration is included.

Condition selection on the receiver's saved review resolving its actual API/numerical evidence. A failed/unsupported receiver result does not logically forbid every wake diagnostic, but any change of next-step priority must be a new explicit decision; this note does not silently proceed around that result.

## 2. Reuse and new work

Use the already saved `research/m31-zero-screen-2026-10-16/raw/fresh5000-states.f64`, `fresh5000-I.f64`, `fresh5000-source-audit.ndjson`, their manifest, schema, freeze and independent saved review. Pin the original source commit and complete byte hashes. Do not regenerate its lattice, alter a state, run the old driver or repeat an old force/root call.

The source audit retains complete source/rotor classifications and root records, but not every successful term. New R64/Q64 pair calculations are required below and must be charged to this distinct future component experiment. Reusing old summed inflows does not make those calculations free.

Select exactly four receiver IDs from the exposed saved I records, in this order:

1. Largest saved maximum rotor inflow.
2. Largest saved contribution count among IDs not yet selected.
3. Smallest saved maximum rotor inflow among IDs not yet selected.
4. Largest saved difference between maximum and minimum rotor inflow among IDs not yet selected.

Tie-break by ascending receiver ID. Freeze the resolved IDs, ranking values and selection script before any new geometry calculation or GPU exposure. This selection deliberately stresses existing evidence; it is not random sampling, a new holdout or a representativeness claim. Do not replace a row because its later result is inconvenient. If the saved evidence is incomplete, stop preparation instead of substituting another dataset. The IDs have **not** been resolved in this static note.

Include all source IDs 0–4999 for every selected receiver/rotor, retain self slots explicitly, and preserve ascending source order. This fixes 4×4×5000=80,000 output slots, of which 16 are self slots and at most 79,984 require pair/rotor evaluation. There are 19,996 distinct nonself receiver/source pairs; a simple rotor-invocation shader may recompute their center predicate four times. Report the actual implementation's count rather than claiming center reuse it does not implement.

## 3. Deliberately restricted geometry interface

The original states retain binary64 positions and quaternions. Check their original finite, shape, quaternion and tilt conditions without repairing them. Prepare source axes and the selected receivers' four local-to-world rotor offsets once with the pinned independent binary64 rotation. This is new geometry preparation, counted separately. All 5,000 source axes and sixteen rotor offsets are needed; receiver axes reuse the source-axis entries.

For this component the uploaded inputs are original absolute source/receiver positions, source/receiver axes, and receiver rotor offsets, each rounded once to binary32. Keep both original numbers and exact uploaded u32 words. The shader constructs the rotor world point and relative vector; no quaternion rotation occurs on the GPU. Do not recenter coordinates, normalize axes, construct a new local-coordinate representation, or precompute pair distances unless a different protocol is explicitly selected before exposure.

This is an explicit approximate-axis interface. It does **not** assert that decoded axes remain exactly unit length, or that packed quaternions satisfy the original 1e-10 admission. Record source/receiver axis norms, their deviations and tilt margins in original and decoded geometry. The original production pose API is not being qualified. A later full-pose port needs its own representation/admission decision; this study cannot silently supply it.

Freeze each transferred constant and construction expression: D=2*sqrt(2)*0.028, wake decay/spread/origin/minDownstream, center radius, near radius, downstream/radial fade and cutoff values, tilt cosine and isolated-hover induced speed. Q64 uses decoded f32 constants; R64 uses originals. Do not mix a rounded coefficient with an unrounded derived threshold without documenting that exact interface. Match the M28 written equations, branch order and rotor order. Retain any difference between the production and independent formula grouping as source provenance, not as a bitwise-equivalence claim.

Raw input u32 exponent validation must precede float reinterpretation. Freeze finite operand magnitude and positive denominator admission based on these particular inputs before compiling. Reject unsupported/nonfinite intermediates; do not depend on post-hoc `isFinite`-style checks to make arbitrary exceptional WGSL arithmetic safe. No f16, relaxed-precision feature, explicit approximate reciprocal, alternate profile or post-hoc clipping is selected.

## 4. Two kinds of classification evidence

### Fixed comparator panel

Reserve thirty controls as three exact binary32 scalar values at each of ten decisions: center radius; tilt axis-Z; downstream zero; far-field start; downstream cutoff; near radius; far radial cutoff; projection zero; downstream fade start; radial fade start. At positive thresholds use predecessor, threshold and successor. At the two zero thresholds use the normal-valued triple -2^-20,0,+2^-20; adjacent-to-zero subnormals would introduce flush-to-zero semantics rather than isolate the comparison. Add two routing controls for self exclusion and an all-zero source contribution, giving 32 records.

These are scalar comparator controls with explicit threshold words and frozen expected inequalities. They test translation of the decision policy; they do not claim to be 32 realizable physical pose pairs or test threshold construction from geometry. In particular the projection-zero controls are outside the valid two-axis tilt geometry. Where a threshold is derived, its frozen scalar control uses the declared rounded threshold, while the main geometry path separately tests the arithmetic that constructs it.

Materialize and freeze every input/expected output word before launch. The old ±1e-12 m fixtures may be cited as known representation stress, but must not be assumed to straddle a threshold after packing. Any collapsed distinctions must be reported. This note has not generated probe values.

### Actual geometry classification

For the receiver/source slots, retain the exact original policy: self/outside-center; down<=0; down>=2.5; invalid near wake when 0<down<2.5D and radial<0.15; near-policy skip otherwise in that interval; radial>=3H cutoff; retained zero projection; retained positive projection. Preserve fade flags separately. An invalid near wake has no contribution value; it is not a zero term. The global tilt check precedes pair qualification.

Record R/Q/G code transitions, original and represented signed boundary margins, lost/gained support counts and every witness in the bounded selected slice. A small numerical contribution never excuses a changed domain verdict. Apply the same strict inequalities; do not create an epsilon band that changes acceptance. A reporting band can be frozen only as a descriptive label.

For valid unit axes each within20degrees of vertical, dot>=cos40degrees>0 is a real-arithmetic geometric consequence. Projection<=0 in the actual admitted slice therefore needs investigation, not an automatic physical interpretation. Rounded approximate axes must be checked explicitly; the scalar panel alone is not evidence for their geometry.

## 5. Reference ladder and saved outputs

| Name | Inputs and computation | What its comparison establishes |
|---|---|---|
| R64 | Independent binary64 component on original prepared geometry/constants. | Compare codes and summed inflows with the saved I evidence using its unchanged tolerances; any disagreement stops the new experiment. |
| Q64 | Same independent formulas on exactly decoded uploaded geometry/constants, evaluated in binary64. | Q−R exposes packing and the declared approximate-geometry interface. It is not a replacement original reference. |
| H64 | Independent host evaluation using the GPU's returned center distance/downstream/radial/axis-dot scalars and decoded constants; recompute decisions and profile. | H−Q locates changes due to returned geometry; H/G code differences expose subsequent threshold/profile arithmetic or implementation changes. |
| T32 | Actual WGSL per-source contribution, saved before any sum. | T−H exposes remaining decision/profile/fade/projection/product differences at returned geometry. Retain both branch and numeric effects; do not label all of this “summation error.” |
| S32, P32 | Ascending-source serial sum and fixed parallel addition graph of the exact same T32 array. | Comparison with host addition of saved T32 isolates addition from term generation. |

H64 is a diagnostic reconstruction, not a new physical reference. Exact arithmetic-stage attribution is conditional on the saved scalars and branch definitions; fused/reassociated operations can span written source expressions. For domain-invalid rows the ladder stops rather than inventing a numeric residual. Any S−R telescoping statement must retain signed operands; component maximum absolute errors cannot be added as if they were an observed signed decomposition.

Proposed pair output stride: 64 bytes, scalar members only. Four u32 fields are ordinal, status, validity/branch flags and reserved0. Twelve f32 fields are centerNorm, down, radial, axisDot, halfWidth, normalizedDown, radialRatio, downstreamFade, radialFade, normalizedSpeed, unprojectedTerm and term. Unreached numeric fields are zero with corresponding validity bits clear; they are not measured zeros. Status/code definitions, raw-word padding and output count must be frozen in the final schema. An unwritten sentinel and ordinal coverage check must prevent a default-zero buffer from looking successful. Invalid controls/early returns still write a complete typed record.

Save all original/packed input bytes, R/Q terms and decisions, GPU records, H diagnostics, sixteen sums and every reduction intermediate specified below. Preserve available readback bytes before API-dependent qualification. Typed IDs/statuses must not be transported through lossy float conversions. A final source layout review must reconcile exact offsets and storage capacities; this document does not provide compiled source.

## 6. Isolate addition order without recomputing a wake

The first reduction uses one invocation per rotor, an explicit ascending source-ID loop over its 5,000 saved T32 values, including zero/self slots. This source ordering matches the intended ordinary independent sum, subject to legal WGSL compiler behavior.

The second uses exactly one64-lane workgroup per rotor. Lane l adds terms l,l+64,l+128,... in that order (at most79 real terms). All lanes then participate in barriers around pair combines at strides32,16,8,4,2,1. Save the64 lane totals and63 combine nodes for each rotor. No subgroup operation, atomic float sum, random ordering or hardware-dependent wave width is selected.

This is a **strided partial-sum plus balanced-combine graph**, not a fully balanced pairwise sum of5,000 leaves. Do not apply Higham's pure logarithmic-depth pairwise bound to it. Its exact source mapping and intermediate records are required to interpret a result. No assertion is made that WGSL uses a particular IEEE rounding mode or preserves every written operation boundary.

Host binary64 ordinary and Neumaier sums of the saved T32 values provide numerical diagnostics. They are not called an exact real sum or a formal interval certificate. All terms must be nonnegative; for a positive exact sum the usual summation condition number is1, but term-generation and branch error are separate. No positive terms permits an exact zero identity. A zero-term sum and known ordinal/term coverage must both pass.

Report separately S−host(T), P−host(T), P−S, S−R and P−R. A tree/serial difference alone does not identify which is more accurate; compare both against the same retained reference. Both graphs are frozen before observing either output. Do not select a winner from a timing measurement—none is allowed.

## 7. Proposed numerical decision, needing explicit adoption

Use an additional wake-component thrust allocation e_w, distinct from the current receiver-only allowance and all earlier omission gates. A prospective engineering choice is e_w=1e-7N, but that value must be explicitly adopted before execution; it is not granted by this memo or by a receiver pass.

For the ideal receiver equation x³+(U/vi0)x−1=0, f=f0*x and U>=0, differentiation gives

`|df/dU|=(f0/vi0)*x²/(1+2*x³)<=f0/(3*vi0)` for0<x<=1.

Therefore an inflow allowance `epsilon_U=3*vi0*e_w/f0` bounds the *ideal-model* force change due solely to replacing one nonnegative inflow with another, using original f0/vi0. This is a desk derivation of the declared equation, not a WGSL error certificate or physical tolerance. No root solve is needed in this wake experiment.

Candidate gates: all selected original/represented input-domain and exact expected classifications pass; every retained term/output is finite and nonnegative; serial total inflow error versus R is<=epsilon_U for each of sixteen rotors. The parallel graph is assessed separately against the same total allowance; if it fails while serial passes, reject that graph and preserve the narrower serial finding. Report the original binary64 inflow tolerances unchanged as diagnostics, as well as all maxima/indices and absolute and relative term errors with near-zero denominators handled explicitly.

Also report the sum of absolute per-term errors for each rotor, the packing/geometry/profile/addition contributions and support transitions. A small total error may hide cancellation between positive and negative **errors**, even though physical terms are nonnegative. The L1 term-error total is a useful conservative diagnostic; it is not silently substituted for the frozen total-error gate.

If Q64 alone fails the selected domain/classification gate or exceeds the total inflow allowance, reject this interface before GPU field work. Do not change coordinates or increase tolerances within the attempt. If exact original classification is mandatory throughout all real inputs, f32 collapse of distinct boundary inputs already rules out that universal claim; the candidate can only qualify the particular frozen admitted slice and scalar controls.

Do not add e_w to the receiver's measured error and claim a composed end-to-end bound. The receiver experiment exercised its original saved U values, not every newly perturbed GPU inflow. Composition needs a separately justified receiver guarantee or later qualification on those actual inputs, plus any load-assembly error. No such root work is selected here.

## 8. Candidate ceilings and stops

Final adoption should use one externally supervised attempt, a60s total wall ceiling, bounded initialization/readback stages, at most64MiB new evidence with4MiB reserved for failure, and no warmup, retry, extra browser, diagnostic rerun or cap increase. These are proposed resource ceilings, not runtime predictions or an active authorization. They need static reconciliation with the eventual source and process cleanup before freezing. The future launch deadline must be explicit; do not inherit an expired deadline or reuse an old job ID.

On a complete selected implementation: at most4 dispatch attempts—32 comparator controls,80,000 pair slots,16 serial sums,16 parallel workgroups. With workgroup64 the corresponding groups are1,1250,1,16. Record reserved attempts, actual submissions and completion separately. No root or integration operations occur.

R64 and Q64 each reserve at most79,984 pair/rotor evaluations; G32 reserves the same nonself count plus16 self slots. H64 independently reserves up to79,984 scalar reconstructions, with no new pose or neighbor traversal. Geometry preparation, scalar controls and reductions have their own counts; do not hide H work inside “saved-only review.” The three pose-based paths total at most239,952 nonself pair/rotor reservations, plus H. Each reduction reads80,000 values; parallel-loop padding is not a real input read. Pair output payload is5,120,000bytes, with another5,120,000bytes for its readback; input/reference/host/process memory is separate. Do not extrapolate this to the cost of a complete field.

Stop before dependent stages on missing/corrupt inputs, reference disagreement, represented-domain failure, unreviewed source change, unsupported nonfallback adapter/API, shader/API/device-loss/readback failure, unexpected invalid/nonfinite/negative values, comparator/code disagreement, incomplete coverage, cap or cleanup failure. Save all already computed raw output, error phase and attempted work. Expected synthetic comparator outcomes are not domain-valid wake observations.

For a completed numerical stage, finish its already reserved saved-output attribution, retain every failure count/witness and then stop; no later geometry dispatch is permitted to rescue it. A failed parallel reduction does not erase a completed serial observation, and a completed component does not trigger full-flock or timing work automatically. Any future alternative—local coordinate packing, a new axis representation, a different reduction or f64 emulation—requires a different prospective question, not a continuation of this attempt.

A future independent review may read the immutable saved scalars/bytes and reconstruct declared summaries without repeating geometry, roots or GPU work. Its separate ceiling and permitted arithmetic must be frozen before launch. The current assignment performs none of this review.

## 9. Claims that remain unavailable

Even a complete pass would leave quaternion rotation, original pose-API compatibility, all-receiver coverage, exact spatial enumeration, dense-cell overflow, body/world loads, original receiver behavior at changed inflows, control/actuators, temporal wake updates, integrated trajectories and cross-adapter behavior untested. The fresh5000 name is historical; these are exposed inputs. Four receivers see5,000 source IDs, but this is not5,000 coupled drones.

The mean far-field source model, finite-radius truncation, near-policy skips, linear aggregation, constant ideal-power receiver, nominal yaw, point-sampled rotors, isolated-hover source strength, tilt restriction and absent walls/ground/unsteady flow remain modeling assumptions or omissions. Agreement with original code cannot validate them. Compatible independent physical receiver data and adequate aggregation evidence remain separate missing evidence.

The verified source ledger in the companion rationale supplies the literature basis. Relevant prior CUDA work motivates direct evaluation and data reuse, not a WebGPU performance estimate. Higham/Neumaier motivate addition diagnostics under explicit assumptions, not a portable certificate for the proposed shader. No algorithmic novelty or publication-readiness conclusion is made.

## 10. Freeze checklist still outstanding

This static proposal is intentionally not executable: receiver independent review; explicit selection and wake allowance; resolved four IDs; exact32 control records/expected words; original and packed geometry byte schema; constant encodings/admission bounds; independent reference and WGSL sources; precise status/validity rules; exact reduction storage; attempt/storage/process/watchdog accounting; source/input publication and independent integrity review. Complete those items before any launch, without an exploratory shader compile or preparatory field run.
