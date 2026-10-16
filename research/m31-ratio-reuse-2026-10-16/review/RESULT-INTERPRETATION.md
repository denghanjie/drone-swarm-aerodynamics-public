# Closed ratio-reuse experiment: interpretation scrutiny

Date: 2026-10-16. Reviewer: `/root/m31_protocol_challenge`.
Package: `research/m31-ratio-reuse-2026-10-16` in `repository root`.
Frozen source commit: `b8ff0c4dca71187db7efd8d72cde2d83fcdb3288`.
Source-manifest SHA-256: `cdec3a218b10658f2196e56a47aac71c8811ee460bfcaa368a808297cdd77560`.

## Disposition

**Accept the saved numerical diagnostic; reject the fixed 10 ms ratio-reuse candidate for its declared accuracy screen. Close this allocation without retuning or retry.** The evidence supports that narrow negative result. It does not invalidate the provisional physical closure, rule out every temporal-reuse method, or establish performance at 5,000 drones.

This review read existing result JSON, protocols and the already-written next-direction note. It verified saved-file hashes and derived unit conversions/counts from saved numbers only. It did not rerun or import the candidate/checker, solve the model, integrate a trajectory, acquire a source, change cadence, add a seed or benchmark anything.

## What completed and what failed

All six paths completed. The three full-reference paths exactly reproduce the prescribed fields at all 21 saved samples of their prior recordings. Both arms pass all five refinement checks: 10/10 cells, with eight passing the below-floor exemption and the two body-rate cells passing the ordinary reduction rule. All post-refresh normalized rotor/force/moment errors are zero in the saved candidate calculations.

The independent checker completed with `pass:true`, 559,589 assertions, no failures, 666 instantaneous endpoints/events, 1,293 cached reconstructions and 24 captured reuse-stage current-geometry audits. All 24 captured-domain checks report admitted and descending-eligible. Candidate and reviewer supervisors both exited zero under the fixed caps.

Those findings make `allocationPass:true` an appropriate description of the numerical comparison. They do not make `approximationPass` true. All 15 paired-grid trajectory/load cells and all nine pre-refresh event cells fail their declared thresholds. Therefore `approximationPass:false` and `decision:"missed-declared-targets"` are the appropriate decisions. The 24 failed cells are dependent metric/grid comparisons from one exposed seed, not 24 independent experiments.

## Size and meaning of the discrepancy

At the finest integration step, h = 0.00125 s:

| Maximum sampled full/reuse difference | Observed | Declared tolerance | Multiple of tolerance |
|---|---:|---:|---:|
| Position norm | 0.036860741576 m | 0.001 m | 36.86 |
| Velocity norm | 0.168290362453 m/s | 0.001 m/s | 168.29 |
| Full quaternion orientation distance | 0.162834823516 rad = 9.329748° | 0.1° | 93.30 |
| Per-rotor load difference / (mg/4) | 0.238347468523 | 0.001 | 238.35 |
| Body-rate norm difference | 1.941097049071 rad/s | 0.001 rad/s | 1,941.10 |

These are maxima over the 21 saved times and 16 vehicles, with rotor maximum also taken over the four rotors. They are not at one shared time or on one shared vehicle. The postrun saved-array extraction locates the finest-grid position maximum at 1.7 s on zero-based drone 11, velocity/body-rate maxima at 1.4 s on drone 11, orientation maximum at 1.5 s on drone 11, and rotor maximum at 1.8 s on drone 8, rotor 2. They are sampled maxima, not continuous maxima or final-time errors. The orientation metric includes yaw and must not be labeled tilt. The hover-normalized rotor discrepancy is an absolute difference between modeled loads on two evolving paths; it is not a 23.8% physical thrust loss or a percentage of each rotor's instantaneous command.

Pre-refresh event comparisons answer a different question: old-cache versus fresh loads on the reuse arm's SAME accepted state and incoming commands. Finest-grid positive-event maxima are:

| Same-state pre-refresh quantity | Normalized maximum | Approximate raw maximum | Multiple of 0.001 preference |
|---|---:|---:|---:|
| Individual rotor error / (mg/4) | 0.034641310307 | 0.002293860965 N | 34.64 |
| Collective force-vector error / mg | 0.022282031285 | 0.005901841626 N | 22.28 |
| Roll/pitch moment-vector error / (mgR) | 0.010175726666 | 0.000106726246 N m | 10.18 |

Here mg = 0.26487 N and R = sqrt(2)*0.028 m. The saved extraction locates the finest-grid rotor maximum at 1.81 s on drone 8, rotor 2; force maximum at 0.42 s on drone 15; and moment maximum at 0.45 s on drone 15. These use the 200 positive refreshes/path, including the terminal audit, and are event-sampled quantities; an interval's largest error need not occur just before refresh.

The 0.23835 cross-path rotor contrast and 0.03464 same-state stale-root contrast are not interchangeable. The first includes the states, current motor loads and controller histories that diverged under closed-loop feedback. The second isolates stale-root arithmetic against a current solve at a fixed saved state. Their difference does not identify an additive causal contribution. Both are simulated-model quantities.

Post-refresh zero error is expected because the newly cached direct roots are the fresh solver's roots and the same state is used on both sides. It verifies construction and prevents a root-transfer implementation error; it cannot show that the preceding 10 ms interval was accurate.

## Numerical-resolution interpretation

All three grids give essentially the same failed approximation contrast. For example, maximum sampled position discrepancy is 0.036860744343, 0.036860745356 and 0.036860741576 m from coarse to fine. Refining RK4 while keeping the cache interval fixed therefore does not remove the discrepancy at the tested resolutions.

For descriptive context, the sum of the two arms' observed medium/fine position discrepancies is approximately 8.32e-8 m, far below the 0.03686 m cross-arm contrast. The analogous separation holds for all five metrics. This supports treating the outcome as a well-resolved difference between the tested numerical models on the retained sample grid. The sum is not a rigorous error bound, and the eight below-floor passes do not establish an observed RK order. No extrapolation to an untested cache cadence follows: a smaller integration step is not a smaller reuse interval.

The strongest safe numerical claim is: “On this exposed 16-drone, two-second case, fixed 10 ms direct-root reuse with current nominal motor states and full modeled wrench fails the predeclared sampled motion/load and same-state event-error preferences, despite passing the sampled integration-refinement and saved-evidence checks.”

## Computation and coverage claims

The reference arm made 11,263 joint-query attempts across its three grids; the reuse arm made 603, including three terminal audits. The campaign total is 11,866. Reuse also made 12,403 path cached applications; eight synthetic cached-control attempts and all independent reconstruction work are separate. This confirms the planned count reduction.

If a percentage is shown, 603 versus 11,263 is 94.646% fewer joint calls across the three-grid bundles, or an arithmetic count ratio of 18.678. At the finest grid alone it is 201 versus 6,421. These denominators include different endpoint/refresh schedules. Neither ratio is a measured runtime speedup, CPU saving, complexity proof or real-time result. The sole instrumented candidate run includes both arms, three grids, controls and evidence writing; the reviewer is additional work. Its wall/RSS totals must remain resource accounting.

The 666 checked instantaneous endpoints/events are 63 full-arm endpoints plus 603 reuse refreshes. Forty-eight first/last global stages are retained overall; 24 belong to reuse. Passing geometry at the events and these 24 captured reuse stages does not establish current coupled admission at every ordinary cached stage. The candidate deliberately did not rebuild full current geometry there. No continuous model-domain, collision-free or stability certificate follows from complete paths, scalar diagnostics or candidate swept-contact checks.

The earlier 5,000-drone cost and provisional physical assumptions remain unresolved. A successful call-count reduction at 16 drones cannot override the declared accuracy miss or qualify a browser-scale implementation.

## Recommended next decision

1. Publish the completed allocation as a negative approximation result, with its separate audit and approximation statuses, exact source/result pins, all failed cells, and a recorded replay that uses common bounds and clearly identifies the 10 ms approximation miss. Preserve both invocation locks and all raw evidence.
2. Close this fixed 10 ms candidate. Do not promote it to a larger/fresh test under the protocol's eligibility rule. Do not lower the refresh interval, add predictors, alter thresholds, choose another seed, repeat the run, or benchmark in this allocation. The present evidence also does not justify a cadence that would pass by dividing the error by a desired factor.
3. Accept `NEXT-QUESTION.md` as a planning-only question about whether a cheap indicator of changes in relative pose and nominal motor states can predict when saved roots become inaccurate. The observed miss motivates that question but does not support a predictor, derivative correction or event-triggering method yet. Before any new candidate, separately bound the relevant original-source/assumption review and define a falsifiable numerical scope. Relative-geometry monitoring, certification and data-structure overhead must be counted; a supposed cheap indicator must not hide the full geometry work it intends to avoid. Fresh confirmation conditions, full-wrench error targets and explicit domain limits would be needed in a separately frozen experiment. No access or computation is allocated by this note.

Physical evidence remains a parallel unresolved priority. The already-written `unadopted private source-admission planning note (not evidence)` offers a separately considered bounded admission checkpoint for the specified Simmons–Hatke fixed-command direct-load triplet, ending at an admission/extraction specification. That remains a useful alternative to another numerical variant; this interpretation does not select or execute it, reopen closed PDF/transfer attempts, permit acquisition now, or authorize transcription/scoring. Its scope would require its own recorded adoption before action.

A later physical comparison would still have a different and limited target: a hardware/control/load transfer under stated assumptions, not coupled 16-drone dynamics, transient wakes, full moments or 5,000-drone feasibility. The result here supplies no new physical measurement and no novelty finding.

## Review of the drafted result documents

`MILESTONE-SUMMARY.md` and `RESULT-CLAIM-LITERATURE-LEDGER.md` correctly distinguish the adequate numerical comparison from the rejected approximation, disclose eight floor exemptions, separate same-state event error from cross-path error, describe post-refresh zero as a construction identity and restrict computation claims to counts. Their principal reported numbers agree with the saved analysis. The coordinator adopted the precision correction: both documents now refer to prescribed saved fields matching, rather than entire recording files. This matches the audited repetition scope.

`NEXT-QUESTION.md` is acceptable as a question and source-review plan, not an allocated or supported new method. The stale-root error is a numerical diagnosis within this provisional model. It does not isolate a physical wake mechanism or establish that the listed predictors/indicators can satisfy accuracy and cost together. The note correctly retains physical validation as a separate priority and disclaims new execution and novelty.

`analysis/saved-extrema.py` is a postrun saved-array locator using only Python standard-library JSON, arithmetic and hashing. Static inspection shows no model import, solve, integration, fitting or new gate; it records raw input pins and checks extracted maxima against the preexisting analysis. Its AST and its saved JSON parse successfully. I did not execute it. The small last-digit differences from the original maxima are consistent with its alternative summation/norm arithmetic and do not alter decisions. Located indices are zero-based and should remain labeled that way. This new descriptive file is not a change to frozen scientific source.

The coordinator reports that viewer QA completed with 53 passing checks and desktop/mobile/gate/altered-evidence screenshots were inspected. I did not rerun or independently repeat viewer QA. This interpretation does not claim completion of the later result-publication receipt.

Document bytes inspected for this supplement:

| File relative to package | SHA-256 at inspection |
|---|---|
| MILESTONE-SUMMARY.md | fb17b4828db6c631a9d66d34b8a4bc0e3a8c6d9b7d946c82e659e4ff1355a142 |
| RESULT-CLAIM-LITERATURE-LEDGER.md | a6c5ec4304945edca120922febc7ce449c2d46d9182c9677482ead06d63d3749 |
| NEXT-QUESTION.md | 368814e12380453ad22636645d6452ed243bd497a58c1980313b264bae0686e8 |
| analysis/saved-extrema.py | 3834e3ff77c6180e860401dffc81c1cbc8a517bf1d311cea1efa2772dea8a97a |
| analysis/saved-extrema.json | 9ea1484ceedcf85b9c7089315fe970c998d593ae53ad9718514277c1f909813c |

## Wording to avoid

- “The experiment failed.” The execution and consistency audit succeeded; the chosen approximation failed its declared numerical screen.
- “The model has a 3.7 cm physical error.” The 3.7 cm value compares two simulated models at sampled times.
- “The drones tilt by 9.33 degrees because of reuse.” The reported value is a full orientation distance including yaw, not an absolute or differential tilt measure.
- “Loads are wrong by 23.8% throughout each interval.” That is a maximum sampled cross-path rotor difference in hover units, not an interval-wide same-state percentage.
- “The post-refresh residual is zero, so the reuse is accurate.” Construction identity at a boundary does not establish stale-root accuracy.
- “The shortcut is 18.7/31.9 times faster.” These are query-count ratios; no valid speed comparison was allocated.
- “All stages stayed within the coupled model's domain.” Ordinary cached stages had no current geometry/admission evaluation.
- “Temporal reuse is impossible” or “the physical closure is falsified.” Only this fixed cadence and accuracy screen were tested against an every-stage numerical reference.

## Evidence checked

All six raw trial byte lengths and SHA-256 values match their saved analysis pins. Both supervisor records identify the frozen source commit and manifest above. Principal saved evidence:

| File relative to package | SHA-256 |
|---|---|
| results/analysis.json | 926d0d98b89082bad212c046b237c2554245af5117182dba10851688230d898a |
| results/independent-review.json | e88cc48df67113deb75c5fdc670991eb145031e8a15d24530f4d52c4f5b13816 |
| results/candidate-run.json | 9045fb77de3879d2d1e7e6139e1f4d40a9088145445ac399a29a2a4cbe498bc4 |
| results/review-run.json | 038344ce3a678b3d473e59e52c387d73837a699da807b663d87b5ce99b64093a |
| results/boids16-coupled-0.00125.json | ba5da0617aaf01118f5900163432940c83018ae27c895950f25d3c393e0df4ef |
| results/boids16-reuse10ms-0.00125.json | ca0a19b3fe2c9f17ec9f89dcd0fda19a649912033fd4809882da9d7a4cfc7e07 |

The assertions, event samples and saved times are an implementation-evidence audit and deterministic trajectory observations. They are not independent physical observations or statistical replicates.
