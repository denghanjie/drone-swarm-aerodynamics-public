# Independent saved-data audit contract: two paired arrangements

21 October 2026, Asia/Shanghai. This contract and `source/audit.py` are prospective source. Independent review, a frozen public source commit and exact-public verification must precede the producer allocation. Source inspection and syntax parsing do not execute or qualify the audit. All earlier numerical, audit, storage and display allocations remain closed.

## Fixed design and allocation

The new evidence consists of four independently evolving paths, in exactly this order:

| Path case ID | Pair ID | Controller |
| --- | --- | --- |
| seed2026102101-original-h005 | seed2026102101-h005 | original |
| seed2026102101-memory-h005 | seed2026102101-h005 | memory |
| seed2026102102-original-h005 | seed2026102102-h005 | original |
| seed2026102102-memory-h005 | seed2026102102-h005 | memory |

Every path uses N=64, dt=.005 seconds, two steps per .01-second controller interval and horizon five seconds. Segment 0 has origin 0 and duration 1; segment 1 has origin 1 and duration 4. The exact configuration includes the fixed pair ID, controller arm, seed, dt and cadence for each path. There is no second integration resolution or replacement seed. `SEED-EXPOSURE.md` must be source-pinned; its historical search scope and limitations remain part of the evidence. The auditor verifies its byte identity, not exhaustive prior nonuse, randomness or the search's empirical completeness. These two date-based choices do not constitute a random sample.

One producer allocation has caps of 16,000 attempted native F calls/stages, 4,000 completed steps, 2,400 successful wall seconds including supervision cleanup, an external termination boundary at 2,420 seconds and 4 GiB total result output. Raw records are at most 4 MiB. One audit allocation has the same 2,400/2,420-second wall limits and a 128 MiB output cap. An exclusive audit launch lock and newly created `audit/` directory prohibit another attempt. Unexpected failure, timeout, malformed evidence or persistence failure closes the allocation; no tuning, changed tolerance, repaired rerun or storage trial is authorized here. These resource bounds are not speed measurements.

## Independence and source provenance

The auditor uses Python's standard library only. It does not import or execute the producer, scientific JavaScript, controller, initializer, Boids steering, contact geometry, native airflow solver, browser or earlier audit modules. Binary64, rotation, native-evidence, projection, derivative and RK helpers descend from the independent continuation Python auditor. Journal and memory checks descend from the independent vertical-memory and transfer auditors. Reuse preserves independence from JavaScript production; it is not another independently derived implementation of those Python helpers. This adaptation adds four-path pairing, original-controller target checks and common-sample error aggregation.

There is no reused numerical baseline. Both original and memory arms are read completely from their new saved journals. No earlier trajectory index/export is parsed and no earlier raw initial prefix is needed. Earlier result manifests, summaries, source bytes and storage-qualification metadata are provenance. A byte check of a source-manifest dependency is distinct from regenerating or semantically reauditing its historical numerical results.

The source gate requires a full commit ID and a publication receipt with exact source-manifest SHA-256, exact verified pin count, and true remote/local and committed/local byte-equality flags. This offline auditor checks the existing receipt; it does not refetch the public source. Source paths must be unique, safe repository-relative regular files without symlink traversal, with bounded lengths and exact SHA-256/length matches. All listed sources are verified before and after the audit. Mandatory coverage includes config, runtime identity, protocol, seed-exposure record, this contract, auditor, producer, supervisor and the immutable inherited sources.

The two controllers remain direct imports of their previously published bytes:

- Original: `research/m31-boids-continuation-2026-10-20/source/motion.cjs`, SHA-256 `c8cf434a23b6c7450eabbadb5bb371398d7a8d8c8810615667822529e8d12373`.
- Memory: `research/m31-vertical-memory-2026-10-21/source/motion.cjs`, SHA-256 `f7966691b52f2e14c2fbba82ed136fc99cf7a87b8d53725e08be9923128cea16`.

The adapter, native-load, physics, simulation, grid, geometry and continuation Journal also have fixed known SHA-256 identities in the auditor. Literal relative CommonJS dependencies are followed as text and must be pinned; both controller modules and native-load must appear in that closure. No JavaScript is imported by this inspection. The frozen producer separately checks its executable against the runtime pin.

The motivating transfer result is pinned to commit `341cfa5e9bec84c0615825b82665385469d84a2b`, manifest length 40,238, SHA-256 `530b5b76624dfea7e21127832e552af9deeab7358816ed164cfa00a0130b872a` and 198 pins. Its exact publication receipt and published `SUMMARY.md` are checked, and both inherited controller pins must match its public manifest. It supplies already exposed context, not another new comparator or a statistical trial to pool with this study.

The unchanged lossless Journal's prior qualification is reused from continuation result commit `a0f595f34a4f9ef8cef516caa0cde60053e0eade`, manifest length 33,149, SHA-256 `90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81` and 157 pins. The publication receipt, qualification report, storage supervisor and allocation closure are source-pinned and bound to that manifest. The qualification must be passed/closed; the supervisor must have zero return code, no timeout and passing wall/output flags; the storage closure must be closed-passed with exactly one attempt. No qualification executes again.

## Producer closure and byte handling

The producer index must be complete schema `m31-unseen-pairs-v1`, contain no failure, match the exact `m31-unseen-pairs-config-v1` config and public source commit, and contain all four prescribed paths in order. Launch and index must name the same source commit. The internal producer exit must be closed with code zero and wall at most 2,400 seconds; the external producer supervisor must report zero return, no timeout, passing wall/output caps and wall at most 2,400 seconds. A structured stop can close a path successfully; an unexpected producer failure cannot be relabeled as a completed study with missing paths.

The results directory contains only launch/index/exit files and every ordered journal part listed by the audited index. Four to eight journals exist according to reached segments. A first-segment stop has no second journal. All physical bytes must agree with supervisor accounting and the 4 GiB cap. `outputBytesBeforeIndex` equals launch bytes plus all compressed journal bytes. Native calls equal attempted stages, and all independent stage/endpoint/controller/safety totals reconcile with the index.

The Journal retains 16 MiB raw blocks and compressed parts at most 32 MiB. Part names, ordering, contiguous offsets, lengths, aggregate compressed/raw hashes and exact record totals are checked. Every nonfinal compressed part is exactly 32 MiB. No part bytes reach gzip or JSON parsing before its whole-part length/hash check succeeds. The auditor streams concatenated gzip members forward and checks complete compressed and uncompressed JSONL totals.

Every raw line is at most 4 MiB and ends in a newline. Duplicate JSON keys, nonfinite/overflowing numeric literals, missing or extra records, unexpected kinds/order and noncontiguous sequences fail. Endpoint frames retain endpoint- and safety-record uncompressed sequence/offset/length/SHA-256 provenance. Initial frames, controller observations and refused trials retain their respective source-line provenance. Hashes include the newline.

Each verified-read operation allows at most three byte-read attempts on an OS error or identity mismatch, before any bytes from that operation are consumed. The anomaly log records path, operation number, attempt and error or observed identity. Before-gate, consumption and after-gate reads are separate operations. Parsing, arithmetic and whole phases are never retried. A new small result without a prior expected hash gets one capture read; its captured identity is rechecked before success.

## Paired initial state and independent continuation

Every initial physical record contains exactly 64 canonical IDs and 17 finite binary64 words per ID. For each pair, the first original path's saved initial words establish the comparison reference. The corresponding memory path must match all 64×17 words exactly. The two seed references must differ. These checks establish exact pairing and distinct saved arrangements; they do not reproduce the initializer or prove that it correctly maps every seed to a geometry.

Every reached second segment must start with that same path's own previous terminal physical words. No additional normalization, other-arm state substitution or reinitialization is accepted. Original `controllerMemory` is null at initial, boundary, case-end and whole-path index. Memory paths instead carry all integral/error words and update counts exactly by the serialized evidence. Physical state alone is not a full memory-path restart state.

Each segment contains initial, then a controller whenever due, k1/k2/k3/k4, completed step, safety, and the next step or case-end. Structured refusal truncates that order as specified below. All physical adapter/controller arms remain `coupled`; the experiment's `original`/`memory` labels are separate fixed case metadata. Commands are held through all four stages and until the next due update.

## Controller and error arithmetic

The original controller retains schema `m31-coupled-controller-v1`, has no saved `globalControlIndex` and no per-row `verticalMemory`, and uses exactly:

```text
targetZ = z + (2.5 * desiredVz + 1.5 * currentVz) / 6
```

The memory controller retains schema `m31-vertical-memory-controller-v1`. Separate memory records have exactly `id`, `integralWord`, `previousErrorWord` and integer `updates`. Each memory path initializes integral/error to positive zero and updates to zero. The recurrence preserves the existing operation grouping and order:

```text
increment = updates == 0 ? +0 : (2.5 * .01) * previousError
unclamped = integral + increment
integral = max(-5, min(5, unclamped))
currentError = desiredVz - currentVz
previousError = currentError
updates = updates + 1
targetZ = z + ((2.5 * desiredVz + 1.5 * currentVz) + integral) / 6
```

Every saved before/increment/unclamped/after word and target-z word must match its independent computation. Required intermediates are finite. Integral bounds are [-5,+5]; update counts are 0..500. This clamp applies to memory only. The inherited F.control net-command clamp remains [-4,+5], with unchanged motor limits. Bounded integral memory is not conditional or back-calculation anti-windup.

The independent global controller index is `timeOrigin/.01 + stepIndex/stepsPerControl`. The audit derives it for original records without inserting a field into raw evidence; it checks the saved index for memory records. Local indices reset at the segment boundary; global indices continue at 100. Memory counts equal the global index before an update and global index plus one afterward. The error sampled at t=.99 is therefore integrated once at t=1. There is no new controller/memory update at a terminal endpoint unless a due controller record exists.

For both controllers, checks bind the saved physical state to the current completed endpoint, verify local/global schedules and relative/original time words, validate sorted unique neighbor-ID shape, finite desired velocities/targets/quaternions/commands, x/y target bindings and saturation boolean shape. Neighbor membership, Boids steering, yaw trigonometry, inherited F.control actuator law and saturation decisions are not regenerated.

At each reached controller, compute `abs(savedDesiredVz - savedCurrentVz)` for each ID and sum left to right in ID order, starting from positive zero; divide by 64. Save this mean absolute vertical error, actual time/time word, local/global indices and controller line provenance. Memory observations also contain integral minima/maxima; original extrema are null because it has no integral memory.

For each pair, intersect the two sets of integer global controller indices and order them increasingly. The saved controller schedules are contiguous, so any common set must be an initial prefix; the corresponding saved time words must agree. For each arm separately, sum its per-update means chronologically and divide by the number of common controls. Export both means, memory-minus-original, `commonControlCount`, `vehicleSamplesPerArm`, first/last global indices and each arm's actual first/last saved times. If no common controls are available, `available` is false and means/difference/window/indices are null, never zero-filled. An accepted complete four-path study ordinarily has the first controller for every path, but this unavailable representation is defined explicitly.

Include a due controller emitted before a native refusal: its errors describe its saved current completed state, not the refused trial. The common controller window can consequently end at the time of the last shared completed state even though no subsequent step was accepted. Both arms use their own state-dependent Boids requests. This is descriptive own-request error over the shared observed window, not tracking of a common reference, a tracking guarantee, a full-horizon metric after an earlier stop or a reason to pool unlike windows across pairs. No significance, normality, population reliability or general-stability inference is made.

Conditional full-horizon counts are 500 controller records per path, 2,000 total; 128,000 controller rows, including 64,000 memory rows and 64,000 original rows; and 63,872 nonfirst memory integrations. Each of the two memory paths has 64 first-update rows with zero increment. Actual counts depend on reached records, including controllers preceding refusals; those maxima are not assumed outcomes.

## Native evidence, integration and stopping

Required scalar/state words are 16 lowercase hexadecimal digits interpreted as finite IEEE binary64, with signed zero retained. Arithmetic follows the frozen producer's grouping and compares exact words. This is binary64 consistency on the audit runtime, not exact-rational arithmetic, cross-runtime accuracy or physical validation.

Saved positive roots must be within one ULP of Python `math.sqrt` of the independently computed operand; the saved root is used downstream. Comparisons and one-ULP differences are counted. The unchanged adapter omits per-row norm evidence on refusal. For those quaternions the auditor tests Python's root and immediate lower/upper neighbors, requiring an exact projected-word match from a finite positive candidate. Such reconstruction is counted and disclosed; it is not a recovered saved norm. Native root-two constants use the same three-candidate policy.

Both original and memory paths receive the same full saved-data arithmetic checks:

- Raw k1 equals the current base. k2/k3 equal base+h/2 times the preceding checked derivative; k4 equals base+h times k3. Relative/original times, dt, native input, projected/raw row words and held commands bind exactly. Quaternion norm-square/projection and all non-quaternion word preservation are checked.
- Native method F, model/schema, stage identity and canonical input hashes bind to current projected input. Saved constants, prepared centers, axes, rotor offsets/points, projected motor forces/totals and induced/beta/nu roots are checked.
- Saved coefficient dimensions, contiguous offsets, ordered source IDs and success ranges are checked. Scaling `a = K * sourceBeta / receiverNu` must match. Geometry-derived K coefficients are not recomputed.
- Successful native evidence requires admitted diagnostics, empty admission reasons, descending eligibility, recorded schedule order and finite recorded residual diagnostics within the inherited limits. The root algorithm and residual model are not rerun. Saved alpha sums, rotor force products, collective force, world force/moment, saved-y/load-ratio consistency and exact consumption checksum are checked.
- Derivatives consume same-ID native loads. Body-frame arm moment, unchanged nominal reaction yaw from projected motor states, total body moment and gyroscopic term are checked. Every one of the 17 derivative components is checked: position, coupled acceleration/gravity, quaternion rate, angular acceleration and motor lag. This verifies the implemented convention without validating it physically.
- RK accumulation is exactly `base + h * (((k1 + 2*k2) + 2*k3) + k4) / 6`, followed by endpoint projection. The complete result becomes the next controller/step input or terminal state. No new aerodynamic force is assigned to an unqueried final endpoint.

Every attempted stage records exactly one native call. Structured `domain-refused`, `input-refused` and `numerical-failure` statuses are allowed scientific stops with nonempty reason and a declared refusal stage. The adapter must report failed/`native-non-success`, no derivative rows and no consumable solution/load/checksum; available refusal preparation/coefficient evidence is still checked. A thrown/malformed native output, unknown status or unexpected producer failure fails the allocation.

The refused attempted step has no endpoint or safety record. Physical state stays at the last completed endpoint, including the initial state when zero steps complete. Memory stays at its most recently emitted value, including a due update immediately before refusal, without rollback; original memory stays null. A separate refused frame records the projected trial positions, actual time, local step/stage, attempted global step, status/reason and line provenance. It is excluded from completed-frame lists and endpoint comparisons. No later segment follows. Attempted stages equal four times completed steps plus the refused stage index if present. Successful plus refused stages equal all attempts.

Each completed endpoint has exactly one safety record. Checks cover issue kinds, ID shape/order, recorded finite distance/clearance fields and equivalence of pass with an empty issue list. Contact/obstacle geometry and vehicle-limit decisions are not regenerated. The first nonempty issue list ends that path, retaining its completed endpoint and exact termination identities. Final physical state, latest/null memory, status/reason, refusal, issues, counts and nominal last time must match case-end and index. Horizon completion requires all prescribed steps with empty terminal issues. After a structured path stop only the remaining prescribed paths may continue. Unexpected/resource/persistence failure fails the full allocation.

## Paired outcomes and export

Primary output is the five-second completion category for each seed: `both-completed`, `original-only-completed`, `memory-only-completed` or `neither-completed`. Each path's actual status, reason, final completed time, safety issues and any native-refusal metadata remain separately available. A native refusal is not a contact outcome. Counts across the two fixed pairs are descriptive counts, not a population rate or independent-trial probability. Earlier exposed outcomes are not pooled with them.

Secondary positional comparisons use the largest integer global step present in both paired completed-frame lists, including zero if needed. Export both actual saved times, safety flags, each arm's mean vertical displacement from its matching start, mean-height difference, ID17 heights, maximum/RMS per-drone center separation and ID17 velocities from the new saved endpoints. Differences are memory minus original. Terminal summaries are kept separately when endpoints differ. There is no floating-time equality join, interpolation, extrapolation, padded suffix or refused-trial comparison. Higher height alone does not establish better tracking.

`audit/viewer-data.json`, schema `m31-unseen-pairs-view-v1`, contains exactly two entries under `cases`, one per pair. Each retains `caseId` equal to its `pairId`, seed, dt, cadence, completion category, `memory`, `coupled` and `comparison`. For compatibility, `coupled` denotes this study's newly audited original-controller path; both paths physically use full coupling. Each arm includes its exact `pathCaseId` and `controllerKind`, every initial/completed endpoint, physical/safety provenance, controller observations, terminal memory/null, outcomes and any separate refused frame. Exactly one duplicate boundary frame is omitted per reached second segment. The export pins source/index identity, sets physical validity false and retains the fixed visual marker ID17 and floor z=0.

`comparison.pairedOwnRequestError` contains the defined common-control MAE fields. `sameSeedComparisons` is an empty array and `resolutionStudy` is false: this design has one step size and makes no new resolution-sensitivity claim. No missing trajectory suffix is invented.

`audit/audit.json`, schema `m31-unseen-pairs-audit-v1`, records evidence pass status, publication/source/context/storage/seed-exposure pins, producer closure pins, new journal descriptors, static dependency closure, counts, primary paired completion counts, and two pair entries under `caseOutcomes`. It preserves original/memory individual outcomes and paired comparisons, read anomalies, arithmetic scope and omissions. `viewerPin` identifies exact export bytes. `passed`, `allPathsCompleted`, `allMemoryPathsCompleted`, `allOriginalPathsCompleted` and `allAttemptedNativeStagesAdmitted` are distinct facts. A faithfully recorded structured stop may pass the evidence audit. The report declares zero native queries, zero numerical producer calls and zero old numerical trajectories parsed by the auditor.

## Failure and success meaning

`audit/launch.json` and `audit/exit.json` record the local allocation. Failure retains a false report, or a separate failure file after a late error, and returns nonzero. A partial viewer is unusable after failure. Finalization/display require passing evidence, no failure file, exact export pins, a closed zero-exit internal audit and a closed zero-return external supervisor with passing wall/output caps. The supervisor receipt exists only after auditor exit; the auditor cannot self-certify that closure.

Evidence consistency and paired completion do not establish native-solver correctness, correct initialization/steering/contact decisions, real aerodynamic accuracy, physical flight safety, an optimal/new integral method, large-swarm scalability or overall research completion. Two fixed arrangements at one resolution support only the explicitly recorded finite-path comparisons and their stated omissions.
