# Preregistered coordinate-origin diagnostic

Prospective, unexecuted source preparation. The published wake-slice failure is closed. This campaign has exactly one externally supervised invocation; no retry, replacement geometry, seed search, added cell or skipped-stage rescue is allowed. All source, controls, constants, generator, layouts and work/output limits must pass independent static review, be published and be independently retrieved before seed release or numerical exposure.

## Question, construction and dependent conditions

Test A(world-point subtraction), B(local-first subtraction with A's exact represented inputs), and C(local-first subtraction with high/low positions only) on one fresh synthetic5,000source scene. Compare each at origins[0,0,0]and[64,-32,16]. These six conditions share one scene; origin copies and receivers are dependent. No independent-sample confidence interval, significance test or population claim is planned.

`generator.cjs` is authoritative. Shape20×25×10, ID=(z×25+y)×20+x; canonical numerator=(2index−(axisSize−1))×131072+jitter, denominator1048576. Each jitter is the next uint32 modulo16385 minus8192. Canonical integer magnitude<2^22; translated magnitude<2^27. All intermediate integer operations fit the exact53bit range, and power-of-two division preserves the intended binary64 coordinate. Canonical numerators fit binary32 significant precision; this is a deliberately easy control. Save both numerator arrays, both17state arrays, angle ticks/angles, exact translation residuals and generator audit. The translated one-word interface must actually lose position bits. Require exact high+low reconstruction; record every residual. No failed stimulus permits regeneration.

Derive exactly one seed from the first little-endian uint32 of SHA256 of UTF8`m31-coordinate-origin-v1\n`+the independently verified source-publication commit+`\n`. The generator defines Mulberry32 uint32 consumption in source order: three jitter words then three attitude words per node. Accept zero. Reject the historical seed608897 without another draw/commit. No new geometry is generated while preparing or reviewing source.

Roll/pitch magnitudes use fixed ticks giving2°through6°inclusive with independently selected signs; yaw magnitude1°through179°inclusive, nonzero, with sign. Quaternion formula is frozen. Validate the original quaternion and20°global tilt policy; never normalize. Prepare original axes and16receiver offsets once and copy identical bytes between origins. Source strength remains prescribed nominal hover, not a coupled flight result.

Fixed receiverIDs[749,500,2250,4750] correspond to lattice strata[9,12,1],[0,0,1],[10,12,4],[10,12,9]. Their ordering is fixed before outcomes. The first three receivers must have, on every rotor at each origin, at least4positive R terms individually>=16epsilon and exact stored-term sum>=256epsilon. The top receiver has no positive-exposure requirement and remains visible even if all terms are zero. These engineering usefulness thresholds exclude a trivially zero diagnostic; they are not physical thresholds. Failed exposure is terminal and uninformative for candidate selection.

## References and unchanged gates

R is the unchanged independent-I binary64 arithmetic on original prepared inputs at the matching origin. There is no previous saved-I output for this fresh scene: do not call its own result independent reproduction. R must have complete, finite, valid records and exact stored-term sum/ordinary/Neumaier agreement within the original1e-12m/s allowance. Numerical consistency of this reference does not validate the wake physics or make its individual terms exact real-valued solutions.

Q0 is the same arithmetic on decoded ordinaryf32 positions, axes, offsets and constants. A/B share Q0 and byte-identical input payloads. Q1 changes positions only to the semantic binary64 sum of C's high/low words; all other represented fields match Q0. Save C's full12word nodes, A/B's8word nodes, decoded Q0/Q1 nodes, constants, offsets, IDs and axis metrics. Runtime checks require shared fields identical and reconstruction residual zero.

For every required rotor use epsilon=0.000018270441835956964m/s and allowance=1e-12m/s as the exact values of their frozen binary64 encodings. They are an engineering allocation, not an empirically established physical tolerance. Gate decisions use integer dyadic arithmetic, never rounded display values:

1. Interface:sum|Q−R|+allowance<=epsilon, with complete matching policy classes.
2. Before reduction:sum|T−R|+allowance<=epsilon, with valid complete GPUterms and matching classes.
3. After reduction:sum|T−R|+|S−exactSum(T)|+allowance<=epsilon.

T is each cell's actual GPUterm. S is one ascending-source GPU serial sum of that same retained buffer; no term reupload/reconstruction occurs. Only passing term cells may spend their reserved reduction. A signed total or cancellation cannot replace a failed conservative gate. No roots, final forces, state integration or timing comparison is added.

Each origin permits exactly R,Q0,Q1: six80,000slot reference passes in total. R retains world-point arithmetic at both origins. Exact input translation need not make that arithmetic translation invariant; retain the R cross-origin saved-term/vector comparison. Compare Q1−Q0 within each origin, and A/B and B/C GPUvectors where both buffers exist. Missing/incomplete contrasts remain unavailable. Signed differences and L1 errors are attribution bookkeeping, not additive causal percentages.

## Kernel and control sequence

One nonfallback adapter/device, one module, seven pipelines:termsA/B/C,controlsA/B/C,reduceMain. No warmup, second adapter, fallback or compile retry.20literal controls per arm are dispatched once, before the six possible main cells. Their shared output buffer is explicitly zero-cleared before each control dispatch; clears are accounted separately from compute dispatches and uploads. Expected metadata, signs, placeholders and direct literal vector words are frozen; controls do not contain a newly evaluated profile magnitude oracle.

All arms emit the same104byte record: eight metadata words, twelve original scalar words, and six actual reached center/rotor displacement components. Validity bits12–14and15–17 distinguish the latter stages; unreached values remain rawzero. Preserve source-minus-receiver signs. A uses source−(receiver+offset), B uses(source−receiver)−offset, C forms(highSource−highReceiver)+(lowSource−lowReceiver), then subtracts offset. C also uses the reconstructed center vector for center admission. Written WGSL grouping does not guarantee backend ordering; returned values establish only observed behavior on the recorded backend.

Main order is origin0A/B/C then origin1A/B/C, skipping only cells whose predeclared interface dependency failed. Create one cell's buffers, upload positions/offsets/IDs, dispatch terms, save raw bytes before API/term assessment, optionally reduce the retained buffer, save raw sums before assessment, then release. Complete cells can be numerically negative. Diagnostic matrix storage and readbacks are not a proposed production full-flock architecture.

## Failure dependencies and decision

|Failure or outcome|Frozen action|
|---|---|
|Construction/admission, original R invalid/incomplete, bad source/runtime identity, exhausted caps, malformed records, API/device loss, process ownership or any failed control|Stop the campaign and retain all available evidence. No retry or replacement.|
|Wellformed Q0 numerical/class failure at an origin|Skip that origin's A/B GPUcells; independently planned Q1/C and other origin may continue.|
|Wellformed Q1 numerical/class failure|Skip that origin's C; independent Q0/A/B and other origin may continue.|
|Wellformed term numerical/class/domain/arithmetic failure|Retain term buffer/readback, skip its serial stage, continue independent frozen cells. Undefined/malformed records remain global integrity failures.|
|Wellformed serial combined-error failure|Retain the negative cell; continue independent frozen cells.|
|Insufficient R exposure or absent precision stimulus|End as uninformative without new GPUcell work or regeneration.|

Assessors return uncapped integrity and numerical error counts separately; the capped witness list never controls continuation. All required cells at both origins must complete and pass for an arm to qualify. Missing, skipped, invalid or failed cells cannot be excluded. Prefer B if it qualifies and A fails at least one required condition. Consider C only if B is inadequate, C qualifies, and A does not already qualify. If A passes both origins, no remedial candidate is selected. If none qualify, stop the position-only choice. Lower average error is insufficient.

A selected candidate earns exactly one separately frozen fresh broader confirmation with a new coordinate family/coverage and unchanged gates. It does not authorize tuning or switching to the next-best arm if confirmation fails. Any novel algorithm, speed, low-end suitability, coupled-Boids benefit, physical validity or publication readiness remains unresolved.

## Resources and evidence closure

Authoritative numeric caps are in config.json, callback/assessment reservations and BYTE-ACCOUNTING.json. Maximum15GPUdispatches:60control slots,480,000term slots,96sum outputs;480,576launched lanes including420padding;480,000storedterm reads reserved for sums. Up to seven pipelines,48buffers,1,124,896uploaded bytes,49,929,312readback bytes,6,240control-clear bytes,100,979,360cumulative allocated bytes and16,880,848peak tracked live GPUbuffer bytes. Driver checks observed costs against these ceilings. C's node buffer adds80,000bytes(50%) over A/B. These are resource counts, not a speed result or total process-memory bound.

Complete typed raw files total144,439,440bytes in116files; conditional absences remain absent. JSON, manifests, capability, API, counters and terminal evidence share a256MiBraw writer ceiling with8MiBreserved for terminal failure records. A separate32MiB results ceiling covers duplicated terminal result, stdout/stderr, lock and supervisor budget. The supervisor polls byte ceilings and also reconciles exact closure sizes; polling can detect an overshoot and reject it, not impose a filesystem quota. Private process/error provenance is separately retained and never published verbatim.

External total ceiling180s, subprocess deadline178.5s, cooperative guard170s; perGPUbatch10s, bounded browser/error/cleanup calls. Cooperative checks occur in charged generation/reference callbacks and before/after each synchronous saved-data assessment; they do not interrupt an assessment mid-pass. The external process deadline remains authoritative. The guard also stops on recorded browser errors before further dependent work. The process registry records detached browser ownership at spawn. The supervisor confirms registered groups absent or terminates only identified owned groups. Final qualification requires no timeout, cap overrun, cleanup failure or missing coverage. Resource wall times are bookkeeping only.

Exactly one independent saved-only review has a separate90s external ceiling and32MiBoutput ceiling. Its contract prohibits model reconstruction or GPUexecution. Source and result publication each require privacy review and independent remote commit/exact-manifest retrieval plus local pin verification. Do not claim all remote binaries independently downloaded. Every terminal outcome receives preserved raw evidence, a readable summary, claim/literature ledgers, restart instructions and a tested Three.js saved-evidence view.
