# Independent static challenge: three arms at two coordinate origins

This is a prospective plan review, not an execution result or final integrated-source approval. I read the accepted coordinate-origin decision and challenge, the previous frozen host/kernel contracts and relevant reference source, and the kernel author's proposed interface. I did not decode scientific arrays, generate input positions, evaluate geometry or wake values, import scientific modules, compile a shader, start a browser, execute a checker, or rerun an old experiment. No new agent was created.

The published preceding wake checkpoint is identified by commit `3f8ce4b433c469c4a9a21b972206c287d48c6618` and manifest SHA-256 `3d59aa4bcb02e1e226808d960b1ade8708d4b65a52277c88c36daed76a664f1d`, with 194 pins, as supplied by the coordinator. That historical negative result remains closed. Its cause is not established by either this design or its motivation.

## Disposition

The three-arm, two-origin design is a defensible bounded diagnostic of coordinate-origin sensitivity, provided the conditions below are fixed before exposure and implemented in the frozen source. It can distinguish an observed local-arithmetic intervention from a position-representation intervention on one controlled scene. It cannot establish independent replication across origins, explain the old failure by itself, qualify arbitrary binary64 geometries, or demonstrate a runtime advantage.

There is no plan-level reason to add a fourth arm or more origins. There are launch-blocking details still to close: the complete construction and seed rule; receiver strata and useful-exposure thresholds; reference qualification on genuinely new inputs; the exact high/low operation graph and validity schema; a typed failure/dependency matrix; and a complete immutable resource ledger. Final integrated-source inspection is required after those details exist.

## Construction, seed, and useful exposure

Freeze the source-index-to-lattice-index mapping, centered integer numerator formula, jitter distribution and range, PRNG/hash algorithm, byte order, consumption order, attitude generator, and receiver-selection rule. No seed, geometry, receiver, or origin replacement may follow an unfavorable admission or usefulness outcome. In particular, do not reuse the exposed prior scene or choose new receivers from saved wake/error rankings.

For the proposed common denominator `2^20`, a centered quarter-unit lattice can be expressed with integer numerator `(2*i - (dimension-1))*2^17 + jitter`. A static proof must bound this integer for every axis and index, then bound addition of the frozen translated-origin integer. Show that every intermediate integer is within exact JavaScript integer range and that scaling by the power of two produces the intended binary64 value. An exact final value alone does not justify an unbounded or rounded intermediate construction. Preserve the recipe and numerator arrays, original coordinate bytes, translated coordinate bytes, and exact per-coordinate translation residuals; require the declared zero residuals.

The proof should establish both frames' original component bounds and the packed high/low bounds needed before shader arithmetic. With the stated short-significand canonical family, exact canonical f32 representation is an intentional easy control. It should be verified as saved-word evidence, not generalized to arbitrary coordinates. The translated frame should also record whether the stimulus actually discards position information in the one-word encoding. If the translated data have no such loss, report the representation contrast as uninformative rather than selecting another translation or seed.

Prepare attitude-derived axes and receiver offsets once and copy their exact saved bytes between origins. Generic nonzero roll, pitch and yaw must follow a frozen rule and pass the original quaternion and tilt admission. Do not reorient, normalize, or repack those shared quantities differently between arms or origins. Position translation is the only origin intervention.

A source-commit-derived seed is acceptable under the accepted decision if its exact derivation is frozen, the input is the independently verified source-publication commit, and there is no commit, seed, or scene search. Save the seed provenance. This is a fresh deterministic instance, not independent external randomness or physical evidence. Freeze handling of any forbidden seed or malformed digest without a replacement draw.

The four strata need exact index domains, selection/modulo rules, ordering, and collision handling. Predetermine which strata are intended to be active and which may legitimately be sparse or zero. Declare substantive positive-contributor thresholds for every intended active rotor using R, plus full finite/classification/domain coverage. Merely completing 80,000 mostly zero records does not establish useful wake exposure. The thresholds must not be selected from the new output. Failed usefulness is an uninformative terminal diagnostic, not permission to regenerate or omit that receiver. Keep sparse/zero strata visible.

Do not turn observed A/B vector differences into an outcome-conditioned admission rule. Whether the compiler/backend produces a changed consumed vector is itself a diagnostic observation. Identical vectors can make the intended arithmetic contrast unobservable on this backend; they do not disprove local-coordinate arithmetic as a general method.

## Reference meanings and error attribution

R is the unchanged original binary64 numerical oracle, separately evaluated at each origin. There are no earlier saved independent-I outputs for this new geometry, so do not relabel R's own fresh results as reproduction against prior saved I data. Preserve the oracle's expression source identity and grouping, complete-record policy/finite checks, ordinary and compensated totals, exact sums of stored terms, and the original exact reference-sum allowance checks. Those checks qualify a stored numerical reference; they do not prove exact real-arithmetic or physical truth.

Q0 uses A/B's decoded f32 inputs and the same original reference calculation. A and B must share Q0 and byte-identical prepared inputs. Changing the GPU source expression is not a reason to generate a second equivalent Q0. Q1 uses C's semantic high-plus-low positions with the same decoded axes, offsets, constants, selection and policies as Q0. Save both words, binary64 reconstruction and any exact residual from the original coordinate. Require zero reconstruction residual if exact recovery is a declared property of this construction. Do not reconstruct the absolute coordinate to a single f32 before GPU subtraction.

Keep matching-origin R as each cell's target. Exact translation of input does not ensure translation invariance of R's world-point addition or subsequent arithmetic. Save cross-origin R term, policy and exact-sum differences as diagnostics; do not add observed R drift to epsilon, subtract it from errors, or claim that the numerical oracle is invariant without evidence.

For each origin, retain exact per-rotor L1 and signed Q0−R, Q1−R, Q1−Q0, T_A−Q0, T_B−Q0, T_C−Q1, and each T−R as applicable. A/B's contrast holds represented inputs fixed. Q1/Q0 isolates the position-representation intervention passed through a nonlinear model while other represented inputs stay fixed. C/B's total GPU difference includes that representation effect and C's reconstruction arithmetic. Signed telescoping is bookkeeping; L1 values are neither additive causal percentages nor an order-independent error decomposition.

Two origins and three arms are paired conditions of one fresh source scene with four selected receivers, not six independent samples. All receivers also share sources. Preserve this dependence in the report and viewer; do not calculate an independent-sample significance claim or describe six successful cells as six replications. A successful new contrast alone does not identify the cause of the historical exposed failure.

## Kernel and evidence interface

The kernel author proposes one shared module with `termsA/B/C`, `controlsA/B/C`, and a common reducer. A uses `source - (receiver + offset)`. B uses `(source - receiver) - offset`. C forms high-position difference, low-position difference, their sum as the center displacement, then subtracts the packed offset. This preserves the required source-minus-receiver sign. C's center-neighbor test must consume that same reconstructed center displacement; otherwise the representation intervention would differ between center admission and rotor geometry without being declared.

The proposed C node layout has twelve u32 words: the first eight match the A/B high-position, axis and padding words; the extra four contain three low-position words and zero padding. Driver/host checks should require exact byte identity of A/B inputs and C's shared fields, not rely only on source intent. Every original and packed coordinate/axis/offset/constant must receive the relevant finite, padding and bound checks before potentially unsafe arithmetic. Add explicit residual exponent, padding and magnitude controls.

The proposed output has 26 u32 words: the previous eight metadata and twelve scalar words, then center displacement xyz and consumed rotor displacement xyz. Validity bits 12–14 and 15–17 respectively distinguish reached components. Every arm must have identical instrumentation. Non-self outside-center records can expose center vectors but not uncomputed rotor vectors; self/invalid/unreached vectors must retain exact zero payloads with validity clear. The host must check these masks, finite bounds, identities and routing consistently. The reducer must consume only fully qualified term records under the revised mask schema.

Source grouping and `let` statements do not establish a strict IEEE backend execution order. Returned consumed vectors make a practical intervention observable; they do not prove instruction identity, universal absence of reassociation, or per-operation causation. Save entry-point/module/compiler/backend identities and all three controls' results. The proposed twenty controls per arm and three control dispatches must be included explicitly in the final ledger and source correspondence checks.

Every qualifying serial reduction must read the same retained GPU term buffer that produced its saved raw term records. Host assessment must not reupload a repaired/reordered term array. Record the buffer/cell ownership and lifecycle. No old omitted serial stage is reopened by this new campaign.

## Gates, independent cells, and terminal states

Preserve the declared epsilon and original reference allowance as exact dyadics. For each rotor, the represented-interface gate is `L1(Q−R) + allowance <= epsilon`; the term pre-gate is `L1(T−R) + allowance <= epsilon`; the final gate is `L1(T−R) + abs(S−exactSum(T)) + allowance <= epsilon`. Exact policy equality, all required identities, finite values and full term coverage remain mandatory. Signed total cancellation and a lower average error cannot replace these gates.

Freeze a dependency matrix before launch, distinguishing these outcomes:

| Event | Required disposition |
| --- | --- |
| Invalid original construction, original R domain/admission, shared frozen-input identity, or a campaign-wide premise | Stop the dependent campaign; preserve partial evidence; no replacement scene. |
| Validly recorded Q0 numerical/class gate failure at one origin | Mark A/B at that origin blocked by Q0; no GPU term/serial spending for those cells. Q1/C and other independent predeclared cells may continue under the frozen rule. |
| Validly recorded Q1 numerical/class gate failure at one origin | Mark C at that origin blocked by Q1; independent Q0/A/B cells may continue. |
| Complete cell's numerical term failure | Preserve its terms and assessment; skip only its serial stage; continue the independent frozen cells. |
| Complete cell's numerical serial/final failure | Preserve the negative result and continue independent frozen cells if no shared failure occurred. |
| Malformed/unwritten evidence, API error, device loss, failed common controls, output/work/deadline cap, or compromised process ownership | Stop the affected dependencies according to a predeclared conservative rule; never retry or silently classify it as an ordinary numerical negative. |

The source must make this distinction using explicit reason types, not one generic `pass=false` that either aborts everything or continues through corrupted state. Variant-specific control failures also need a frozen dependency choice; a failed shared helper or API premise cannot be hidden as a single accuracy-cell failure. Runtime exception paths must preserve raw records already read before reporting the error.

A candidate must complete and pass every required cell at both origins, including the appropriate Q and final serial gates, and satisfy the predeclared exposure criteria. The phrase “every valid cell” must not allow excluding a missing, invalid, blocked or failed required origin. Prefer B only if it meets that complete requirement and corrects at least one comparable baseline failure. C is considered only if B is inadequate and C meets it with the accepted additional representation/preparation cost. All-arms-pass, no observable A/B intervention, insufficient exposure, missing required cells, or all-arms-fail are reportable outcomes, not invitations to expand the experiment.

## Resource, privacy, and publication closure

The coordinator currently proposes one 180-second invocation, a cooperative deadline of 170 seconds or shorter, a 256 MiB raw cap, six reference passes of 80,000 slots, six term cells of 80,000 slots, and at most sixteen serial sums with 5,000 stored-term reads per qualifying cell. These are proposals, not adopted limits or runtime predictions. The remaining deadline reserve must cover readback/error handling, result writing, process cleanup and durable closure; time must be charged from invocation start rather than after construction or browser setup.

Before launch, publish one machine-readable ledger for the exact six references, optional dependent GPU cells, controls, construction/admissions/rotations, packing and decoding, exact saved-data arithmetic, cross-origin and cross-arm contrasts, per-cell serial reads, uploads, resident GPU memory, raw files, JSON reports, stdout/stderr, archives, locks and failure reserve. Count cumulative upload/readback bytes separately from peak resident bytes. Retaining six buffers is different from processing and releasing one cell at a time. Preserve the exact visit definitions; counters reserved before an operation are not automatically observed work counts.

Use an external total deadline, a shorter subprocess limit, a cooperative limit inside long loops/assessments, and a bounded cleanup plan. Register the driver and detached browser process group with ownership evidence before use. Ensure partial readbacks and failures are retained within the output reserve. A process found absent is distinct from an actively verified/terminated process. Public runtime reports should use sanitized identities; keep absolute local paths, process IDs, profiles and private registry contents out of publication while retaining hashed private provenance for review.

Freeze the complete source/protocol/constants/layout/control/work ledger and seed-release rule; obtain final independent integrated static review; publish and independently verify the source pins before new numerical exposure. Do not materialize the fresh generator or evaluate scientific functions as a source-preparation check. A later saved-evidence checker requires its own frozen scope and budget; this plan does not authorize one. A successful diagnostic only earns a separately frozen broader confirmation, with no failed-confirmation candidate switching or reopening of this campaign.

## Final static review still required

The final review should inspect the actual generator/host, WGSL/schema, browser adapter, launcher/driver, protocol, caps and source-pin manifests together. In particular it must verify exact byte/stride/mask agreement, typed failure propagation, the retained-buffer reduction path, pre-operation reservations and deadline checkpoints, raw-before-assessment/error-scope retention, deterministic source/seed identity, and privacy sanitization. This memo approves the question conditionally; it is not an assertion that those uninspected implementations are correct.
