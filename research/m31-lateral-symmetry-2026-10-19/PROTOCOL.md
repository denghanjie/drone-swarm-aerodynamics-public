# Prospective paired-support lateral-error decomposition

19 October2026. User “Go on” authorizes a new bounded cycle. All previous scientific/display allocations remain closed. Question: how much of the saved lateral candidate's residual energy appears in same-direction versus opposite-direction paired components? Keep the candidate and all its parameters fixed.

## Evidence and exposure
Only input: research/m31-crossstream-test-2026-10-19/results/comparison.json,2,291,932bytes,SHA2561721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a. All3,240cases, coordinates, measurements, candidate values and residuals were previously exposed and reviewed. No original MAT decode, field evaluation, candidate refit or new measurements. This is a prospective diagnostic of an exposed same-experiment mean field, not blind or independent validation.

## Geometry-only matching
Keep original declared center X=0, plane Y=1 and units X=x/l,Z=z/l,l=.0325m. Use only cases already marked included by the predecessor. Group by exactly equal saved Z (binary64, no tolerance/rounding). Opposite X signs required, excluding X=0. A pair is geometrically eligible if abs(Xright+Xleft)<=0.01 in dimensionless X, equivalent physical mismatch<=0.01l. This is a prospective engineering matching tolerance, not measurement uncertainty. No further tolerance, nearest-response or center search.

Construct all eligible opposite-sign edges within each equal-Z group. Admit only mutual-unique pairs: each endpoint has exactly one eligible neighbor. Thus every input cell appears at most once. Store full eligible-neighbor lists in ascending original-index order. Order pairs by increasing original index of the positive-X endpoint; pairId is zero-based in that order. No interpolation, resampling, center shift or response-based rejection. Preserve all original cases, including old geometric exclusions and all new unmatched cases.

Matching reasons in precedence order: prior-excluded; axis(X=0); no-eligible-counterpart; ambiguous-counterparts(if own neighbor count>1); counterpart-ambiguous(if own count1 but neighbor count>1); paired. Every case gets reason, pairId or null and eligible-neighbor list. Original predecessor exclusions remain unchanged within copied cases.

Primary region Z>=12; near8<=Z<12 descriptive; middle12<=Z<20; far20<=Z<=30. Coverage denominator is all predecessor-included cells in the region, including axis/unmatched/ambiguous cells; numerator2*admitted pairs. Require at least20primarypairs,3distinct primaryZ,and primarycoverage>=.90; otherwise save failure and stop without changing matching. Secondary empty groups valid with null metrics. Preserve the entire predecessor subsets object unchanged for full-field context; paired-only improvements cannot replace full-field performance.

## Components and endpoints
For each admitted pair, left means X<0,right X>0. Measurements vL,vR and saved predictions pL,pR are used directly:

    observedE=(vR+vL)/2; observedO=(vR-vL)/2
    predictedE=(pR+pL)/2; predictedO=(pR-pL)/2
    errorE=predictedE-observedE; errorO=predictedO-observedO
    directSSE=(pR-vR)^2+(pL-vL)^2
    evenSSE=2*errorE^2; oddSSE=2*errorO^2.

E describes the same-direction pair component; O the opposite-direction component. PredictedE is not forced to zero on imperfectly mirrored coordinates. Store signed components, original indices,Xleft,Xright,Z,and absXSum on every pair. These are paired sum/difference components, not exact field parity or experimentally separated causes.

For each fixed region report pair/cell/eligible/unmatched counts, coverage,maxAbsXSum; observed/predicted/error RMS of E and O; pooled directSSE,evenSSE,oddSSE,energyShareE=evenSSE/(evenSSE+oddSSE),energyShareO likewise; pairedCandidateRMSE=sqrt(directSSE/(2*n)); baseline and candidate MAE,RMSE,bias on each side separately and jointly on identical paired support. Primary endpoint: pooled energyShareE. If residual energy is zero, both shares null and agreement retained, not a failure. Empty groups have null summaries, coverage null if eligible count zero. Do not average per-pair fractions. Verify directSSE=evenSSE+oddSSE numerically with2e-12 absolute tolerance per pair and group. This identity follows algebra even for mismatched geometry; it is not evidence of incompressible flow or symmetry.

No p-values, CI, fitted lateral gain/background/center, physical acceptance threshold or causation. A same-direction residual could reflect swirl, asymmetry, center error, drift, calibration or stitching; this experiment does not isolate which. An opposite-direction residual need not identify a particular wake coefficient. No SI calibration, global vector/force/swarm validity or novelty follows.

## Fixed bounded execution
Before controls or real-data matching: independent protocol/source review, immutable source freeze, public push, independently retrieved exact-public source manifest. One evaluator<=60s,<=16MiB saved scientific output; at most3,240inputcases,1,620pairs,10,497,600pair-eligibility comparisons. Fixed synthetic controls only: pure same-direction pair; pure opposite pair; mixed residual algebra; zero residual with null fractions; exact matched geometry; just-outside tolerance; same-sign and unequal-Z rejection; ambiguous mutual matching; axis/prior-excluded precedence; response-perturbation invariance of matching; empty secondary summary. No exploratory threshold/partition sweep.

One independently authored saved-result audit<=60s,<=16MiB cumulative scientific output; no producer imports, new physics or old evaluator rerun. Independently reconstruct pairing and all declared metrics using60-digit Decimal arithmetic, verify binary64 copies and original component identities, check provenance and exact input/source/result pins. Tolerance2e-12 absolute numerical only. External supervisor, fixed output caps, permanent single-use locks, failures preserved. No retry or completion of omitted stages; no overlapping jobs.

## Three.js and publication
One new viewer uses only saved points/pairs/components. Modes: measured,candidate,totalerror,same-directionerror,opposite-directionerror,coverage. Decomposed arrows at the original paired coordinates are diagnostic glyphs, not measured component separation, trajectories or a new flight simulation. Same-direction E assigned equally to both ends; opposite O assigned positive on right and negative on left. No component removal is presented as a corrected model. Explicit enlarged arrow scale4m per reference-speed unit, fixed sparse original row/column%24 glyph rule; all original points remain with unpaired/excluded gray.

One UI allocation<=60s,<=32MiB total saved evidence; desktop1280x1000/mobile390x844, sixmodes, metrics/counts matching saved results, sparse arrows, orbit/reset, corrupt-evidence refusal, console/page/HTTP. Parent screenshot inspection. Any further display attempt needs a separate prospective display-only allocation. No installations, spending, contact or submissions; keep8876. Save source/result/claim/literature/review records, plain summary and restart; privacy-check,commit,push and exact-public verify.
