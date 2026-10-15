Static independent review of the proposed M31 field-to-body-load contract

2026-10-16. No implementation or scientific execution. This memo incorporates the coordinator's latest adopted design decisions: narrowed body-only scope; new per-rotor and handoff gates; explicit nominal and receiver-inflow subnormal truncation; normalized residual gates; R/Q/H reference checks; comparison margins; and the designated-exposure target. These are design decisions before source implementation, not a scientific freeze or launch. It read the existing source text and `PRIOR-APPLICATION-SKETCH.md`; that memo's broader world-output sections are superseded by the body-only scope. No model import, input generation, numerical script, geometry/profile/reference/root evaluation, binary scientific decoding, browser, shader, checker or benchmark ran. No repository file was changed.

**Judgment.** The resulting numerical question is legitimate and useful, and its contract can be made prospectively finite without reopening any older gate. I find no analytical reason to reject the fixed primitive-A/body-load design or the scaled receiver before implementation. Static contract clearance is conditional on the exact definitions below; it is not source clearance, a source freeze, launch permission, physical validation or evidence that the future attempt will finish or pass. A separate implementation audit must check that every gate and lifecycle transition actually matches the adopted protocol.

The remaining implementation prerequisites are the final generator/control literals and their envelope proof, schema/layout and complete work/byte reservations, plus supervisor/reviewer lifecycle. The numerical gates below are settled design choices for source development. Resource ceilings are stopping limits, not evidence of feasibility.

**1. Scope and comparator semantics**

One fixed ordinary-f32 primitive-A query prepares original binary64 axes/offsets on the host, packs them once, visits all receivers, computes the assumed wake and receiver forces, and returns body thrust and all three body moments. Nominal yaw remains `k*(n0-n1+n2-n3)`, with k=km/kf. Source strength stays prescribed isolated hover regardless of source motor values. No positive omission, B/C/rebase option, fallback solver, clamp, regeneration, tuning, world rotation, control, RK4, held-flow dynamics or benchmark belongs to this campaign.

This is not a drop-in replacement for the application's held-wind loop: that loop recomputes the receiver response at changing RK-stage motor states. The generated motor slots are prescribed lagged-motor-state inputs within an explicitly admitted envelope, not evidence that the full family is dynamically reachable.

R evaluates original inputs under the frozen independent-I arithmetic convention. Q evaluates exact decoded packed geometry/constants and **untruncated decoded nominal words** in binary64. The GPU's explicit subnormal-nominal truncation is therefore visible in Q-to-GPU error rather than silently deleted from the represented reference. Retain original states and exact upload bytes. Pin the prepared rotation convention; do not recompute Q axes/offsets from a packed quaternion. Shared prepared data do not constitute an independent numerical reproduction of preparation itself; state that limit and inspect preparation against the independent source and controls.

Use the original numerical R as the comparison target, including its declared ordinary inflows. Ordinary and same-pass Neumaier agreement is a numerical consistency check, not an exact-real or physical reference proof. No full term matrices means no independently reproducible L1, exact GPU-term sum, isolated profile error or isolated reduction certificate. Code-7 positive/numerically-zero distinctions remain disclosed diagnostics.

**2. Concrete final-output gates and inward margins**

Let `epsT=.005mg`, `epsM=.0005mgD`, `D=2*sqrt(2)*a`, and

`epsRotor = .5*min(epsT/4, epsM/(4*a))`.

For every completed receiver and every required rotor, use prospective gates:

- `abs(fGPU_k-fR_k) + 1e-12 N <= epsRotor`.
- `abs(TGPU-TR) + 1e-12 N <= epsT`.
- `abs(rollGPU-rollR) + 1e-13 N m <= epsM`.
- `abs(pitchGPU-pitchR) + 1e-13 N m <= epsM`.
- `abs(yawGPU-yawR) + 1e-13 N m <= epsM`.

All operands must be finite and complete. Freeze the original binary64 threshold expressions/encodings before data. Prefer exact dyadic evaluation of saved-value absolute differences and these inequalities so displayed rounding cannot decide a boundary. The one-half per-rotor allocation rules out the previously identified body-load nullspace and leaves room between its generic assembly bound and the final body targets; direct body gates remain required for assembly and yaw. There is no cancellation-based exemption.

The yaw target is a **new** common engineering moment scale chosen before outcomes. It is not inherited from a historical yaw campaign and does not assert equal yaw/roll/pitch control sensitivity. These are all analyst-selected fidelity targets against the stored validated numerical R, not measured tolerances.

The coordinator explicitly chose to interpret `1e-12 N` and `1e-13 N m` as **inward comparison margins**. This is a coherent finite engineering rule. Do not describe them as propagated independent-reference uncertainty certificates or as bounds against exact real equations. A genuine per-rotor reference bound of 1e-12 N would alone propagate to 4e-12 N thrust and 1.12e-13 N m roll/pitch before assembly; the proposed margins are not that certificate. Ordinary/Neumaier agreement at 1e-10 m/s cannot supply such a certificate either.

**3. Required R/Q numerical qualification**

For each R and Q rotor total require finite `0<=U<=2^20`, all completed policy records valid, and `abs(Uordinary-UNeumaier)<=1e-10 m/s`. Apply the new consistency threshold as this campaign's explicitly declared numerical gate; do not relabel any older 1e-12 failure as passed. Record both totals rather than replacing the ordinary input silently.

For every positive-nominal numerical bisection used by R, Q or the handoff reference, the accepted finite check set is:

- Input nominal and inflow pass their declared finite nonnegative domains; the fixed density/area expressions are positive finite.
- For positive U, alpha is finite and nonnegative, and the returned root is finite with `0<x<=1`.
- `0<=lower<=x<=upper<=min(1,1/alpha)` for positive alpha; use upper limit 1 when numerical alpha is zero.
- Numerical bracket width `upper-lower<=2e-15`, and at most 96 bisection iterations. Save iteration and termination reason, including floating equality or midpoint stagnation.
- Independently recomputed binary64 residual `abs(x*x*x+alpha*x-1)<=1e-12`.
- Numerical endpoint consistency: `g(lower)<=1e-12` and `g(upper)>=-1e-12`, where `g(x)=x*x*x+alpha*x-1`. These allowances acknowledge numerical arithmetic; they do not create an outward-rounded enclosure.
- Returned force is finite, nonnegative, no larger than nominal, and consistent with the frozen binary64 `nominal*x` expression. Save force-scaled bracket width as a diagnostic.
- Original nominal zero returns force +0 with a distinct identity status; root/alpha/residual are not applicable under explicit validity masks. Positive nominal with U=0 returns that path's nominal exactly and x=1; no bisection is charged as performed, though the attempted record is charged.

These are finite reference-quality gates, not a theorem that the stored reference is within the inward margins of exact physics. The reference must stop terminally if they fail. No increasing iteration limits or changing residual tests after exposure.

The original unscaled independent oracle can cover the admitted tiny positive nominal range without a huge-alpha overflow in real arithmetic. With original positive binary64 nominal at least `2^-1074`, positive fixed c=`2*rho*area<1`, and U<=2^20, vi is at least `2^-537` and alpha is at most `2^557`, well below binary64 overflow. Actual coefficient/alpha finite guards remain mandatory. Tiny intermediate cubic/product underflow does not justify a zero root: a returned positive-input root must remain positive, with its residual checked. A zero **force product** may be valid under the recorded numerical semantics.

**4. Explicit truncation and zero conventions**

For each packed nominal word, inspect bits before float arithmetic. Canonicalize signed zero to +0. If the packed raw value is a positive subnormal, explicitly replace it with +0 for both effective-force computation and nominal-yaw assembly. Save original binary64 nominal, raw packed word, effective arithmetic nominal word and separate flags for original zero, packing-to-zero and deliberate subnormal truncation. This is a declared arithmetic approximation, not uncontrolled device behavior or an original physical zero.

The omitted exact-model effective force from a truncated decoded nominal is at most that decoded nominal, which is strictly below `2^-126 N`. This is an analytical magnitude bound using `0<=F(n,U)<=n`. Final gates still charge all original-to-GPU loss, including packing; do not claim the subnormal bound alone covers original-to-packed rounding. For nominal yaw the corresponding loss is bounded through `abs(k)*sum(truncated decoded nominals)` plus coefficient/assembly terms. Q retaining the true decoded subnormal is the correct attribution choice.

For tiny inflow, the adopted choice preserves the actual field sum **Uraw** and its words unchanged, then explicitly maps signed zero to +0 and a positive subnormal Uraw to **receiver Ueff=+0** before receiver float arithmetic. Store both words and separate exact-raw-zero and receiver-inflow-truncation flags. This avoids allowing device flushing to choose whether a raw positive sum is called an exact-zero identity. Q retains its own untruncated total, and the actual-handoff reference uses the saved GPU Uraw, not Ueff, so truncation loss remains included. At fixed effective nominal the ideal force change is at most `L(n_eff)*Uraw < Lmax*2^-126 N`; final acceptance still charges it rather than granting an exemption.

Freeze identity precedence: effective nominal zero first; otherwise receiver Ueff zero; otherwise a positive solve. A Ueff-zero identity after truncation is an identity relative to the explicitly transformed receiver input, never a claim that Uraw or original R inflow was zero. Use integer word tests for this transformation. All inapplicable candidate-root payloads must carry false validity bits rather than fake valid zero residuals. If Ueff is positive, a low-branch Ueff/vi may still become zero or subnormal; flag that coefficient outcome, retain the low solve status and twelve updates, and do not relabel it an inflow-zero identity. Handoff comparisons against Uraw include this coefficient loss.

For a positive normal effective nominal that reaches a solve, computed vi must have finite normal positive encoding. This is consistent with the admitted bounds and provides a useful corruption check. A nonfinite, zero or subnormal vi fails. Nonfinite iterates, negative or out-of-range x, invalid denominator, invalid term or incomplete output fails without clamping or fallback. The identity paths need not compute vi; their payload applicability must say so.

**5. Scaled Newton and tiny-root residual acceptance**

Freeze exactly twelve updates, not “up to twelve until convenient.” The two real-arithmetic equations and initial points are sound:

- Low branch Ueff<=vi: alpha=Ueff/vi in [0,1], solve `x^3+alpha*x-1=0` from x=1. The positive root exceeds 2/3; exact convex Newton decreases toward it from above.
- High branch Ueff>vi: r=vi/Ueff in (0,1), solve `r*x^3+x-r=0` from x=r. Here g(r)=r^4>=0 and g'=1+3*r*x^2>=1, so exact convex Newton again decreases toward the root from above.

Neither fact proves twelve f32 updates accurate. The following are new numerical engineering gates, not inherited receiver qualification:

- Every solve returns finite `0<x<=1`, an exactly recorded branch, coefficient, twelve-update count and final step. A zero force product can be allowed only with an explicit product-zero flag and the final force gates.
- Low branch coefficient is finite in [0,1]; recompute in binary64 from the **saved actual coefficient and x** and require `abs(x^3+alpha*x-1)<=2e-6`.
- High branch r must have normal positive f32 encoding and be <=1. Require `abs(x^3+x/r-1)<=2e-6`, recomputed in binary64 from saved r and x. Do not use an unnormalized absolute `abs(r*x^3+x-r)<=2e-6` as the sole acceptance gate: when r is tiny it can accept x=0.
- The shader-reported residual is diagnostic. Save its equation/scale and do not label r as alpha. Arithmetic grouping and any compiler-permitted behavior must be described honestly.

Unexpected high-branch r=0 is invalid under the adopted decision. Once raw subnormal nominals are explicitly truncated, every positive effective nominal is at least `2^-126`. With c fixed in (0,1), vi is at least `2^-63`; U<=2^20 gives the loose real lower bound `r>=2^-83`. There is enormous distance to f32 underflow, so accepting a zero r is unnecessary and could conceal a defect. Actual coefficient guards, rather than the real bound alone, decide execution validity. Final n*x underflow remains possible and is explicitly permitted; it is distinct from losing the root.

For a positive-input solve, the normalized high residual catches a zero root even when the final force would round to zero and trivially pass an absolute force gate. This is the important tiny-root safeguard. Low-branch alpha zero from a tiny positive U is a different case and must retain its own flag and branch semantics.

**6. Actual-handoff reference and acceptance must be explicit**

The adopted handoff design should independently solve at the **actual saved GPU Uraw**, the **raw decoded packed nominal before deliberate truncation**, and the intended exact decoded packed density/area. Its binary64 vi construction must be independent of the returned GPU vi/r so coefficient construction errors remain visible. It intentionally retains both raw positive subnormal nominal and raw positive subnormal inflow when the candidate replaces either with zero. Thus both declared truncation losses, coefficient construction and receiver arithmetic stay inside this one handoff comparison. It is not a solver-only isolation. A reference solved only at the returned r, or at n_eff, would answer a narrower question and is not an additional required H path.

If raw decoded nominal is zero or Uraw=0, no handoff bisection is needed: save the applicable raw-input identity. A positive raw nominal with Uraw=0 returns that raw nominal, even if the candidate explicitly truncated it. If raw decoded nominal>0 and Uraw>0, reserve and retain one independent bisection witness even when candidate n_eff=0 or Ueff=0, and apply the R/Q reference checks above. Candidate and handoff identity statuses need not match in those declared truncation cases. Do not call a helper that re-solves roots during body assembly. The handoff path is an additional bounded scientific path, not a free saved-review operation.

The adopted handoff gate is `abs(fGPU-fHandoff)+1e-12 N<=epsRotor/4`. It reserves a stated fraction of the new rotor allowance for the declared input truncations plus receiver/coefficient arithmetic and guards against cancellation between field and receiver error. This is a new pre-exposure engineering gate, not an old 1e-7 gate or a proved stage composition. It supplies an actual acceptance check on the retained handoff comparison. Direct original-R rotor/body gates remain mandatory.

Body assembly is recomposed from saved GPU rotor outputs and effective nominal motors in binary64 during the bounded review **diagnostically only**. Do not demand exact equality to an independently ordered binary64 sum or claim separate assembly qualification. The direct original-R body comparisons are the actual accuracy gates. Nominal yaw recomposition uses the same declared effective nominal values as the GPU, while original-R yaw retains the original values so all truncation/packing loss stays charged.

**7. Policy agreement, inflow headroom and evidence limits**

Require every N-by-N pair and all four rotor terminal symbols complete and schema-valid. Compare policy classes exactly across R/Q/GPU. Symbols 8 and 9 both map to policy 7 by the predeclared rule; retain their distinct values and report all mismatches/counts. This consciously permits positive-to-numerical-zero profile outcomes if final rotor/body gates pass. It does not qualify relative accuracy of tiny terms. Invalid-domain, arithmetic, unwritten, malformed or reserved symbols never become a zero contribution.

The individual runtime term guard is `finite 0<=term<=128 m/s`; the actual completed sum guard is `finite 0<=U<=2^20 m/s`. At most 5,000 nonnegative terms gives a real upper bound of 640,000 m/s, motivating headroom below 2^20. That argument is not a universal rounded-arithmetic proof, and the actual sum guard remains mandatory. Without retained terms, saved-only review can verify returned sums/policy/status but cannot independently verify every term's magnitude guard; distinguish frozen runtime checks from reproducible saved-value checks.

The new full-flow bound supersedes only the proposed new campaign's admission. It does not alter the historical receiver's [0,128] domain or qualify it over this larger range.

**8. Four families: acceptable design direction, proofs and literals still required**

The application memo proposes 50 paired-column, 500 tilted-layer, 5,000 dense-volume and 5,000 sparse broad-coordinate cases. The varied density, general positions, bounded tilts, designated exposure and unequal motors make them useful finite challenges. They are four structured families, not a representative probability distribution or exhaustive domain coverage.

Before generation, freeze scaffold frames, origin, jitter arithmetic, hash/seed consumption, attitude construction, motor permutation/edge schedule and every literal control. Prove the stated envelope admissions, including near-domain exclusion and designated source geometry, using the actual frame/offset/norm/jitter bounds. The input author's selected same-frame designated-source envelope is downstream `[.56,.66] m`, radial `<.075 m` and positive projection `>.99`, together with strict center eligibility. The adopted runtime exposure gate is **R U>=.25 m/s on all four rotors of every designated non-top receiver**. Missing exposure terminates without redraw.

A coarse independent desk check supports that target. The frozen constants satisfy `.079<D<.08`, sourceInduced>4 and spread=.07668. Over the proposed envelope, the half-width exceeds `.075`, so normalized radius is <1, the squared profile denominator is <2, and both fades are one. Also downstream/D<9, hence downstream/D+5.817<15; the normalized centerline exceeds `10.11/15>2/3`. With projection>.99 the corresponding real-model contribution has ample headroom above .25. This does not verify the final generator's envelope or establish a universal outward-rounded field certificate. The source proof and actual R geometry/exposure checks remain required; no fresh profile was evaluated for this desk argument.

The non-f32-exact-coordinate gate and most-positive-motor requirement are legitimate predeclared stimulus checks. A failed stimulus terminates without redraw. Include finite controls for exact zero, packing-to-zero, largest subnormal/smallest normal and their neighbors, maximum nominal and adjacent values, Uraw=0, subnormal Uraw explicitly transformed to Ueff=0, normal Ueff producing a zero/subnormal low coefficient, both sides of Ueff=vi, tiny high-branch roots with zero final product, and invalid raw inputs. The exact control count, expected statuses and comparison gates must be fixed. No search or extra scalar controls after exposure.

**9. Budgets and lifecycle must match the final body-only implementation**

The proposed ceilings are one 300-second scientific attempt, 768 MiB raw evidence plus 32 MiB results, 208 MiB tracked live raw GPU buffers, 4 GiB declared process-RSS stop cap, one case resident, no concurrent science, and one 120-second/32 MiB saved-only review. These are plausible prospective ceilings, not verified run-time/resource predictions. Recalculate the final layout after removing world matrices/outputs; do not carry stale 512/640-byte field maps into the decoder. Decide whether raw and result caps are disjoint, count temporary/staging copies, and reserve explicit failure space.

Define which processes the RSS cap covers and how it is sampled. A driver-only RSS limit excludes browser descendants. Summed process RSS can double-count shared pages and is not unique physical memory; either interpretation must be named. GPU buffer accounting excludes driver/browser/compiler overhead. Sampled RSS and timeout supervision are best-effort stopping observations, not instantaneous hard OS containment.

One case resident means retaining completed cases on disk and releasing host/GPU buffers before the next. The independent reviewer must likewise stream or load only bounded portions, rather than materialize all policy files as JS object arrays. All R/Q passes, all GPU slots, handoff bisections, controls, reference checks, decoding scans and review arithmetic need explicit maximum reservations. All four predeclared cases must complete for the full claim; no easier-case substitution after a cap failure.

To avoid lifecycle/checker ordering defects, freeze this conceptual order and reconcile it with actual source:

1. Publish and independently verify the source/config/schema/constant freeze; create a unique attempt reservation before any scientific work.
2. Persist original inputs and exact uploaded bytes; reserve each charged stage before it can execute.
3. Persist returned raw buffers before dependent numerical assessment or later work. Preserve all completed prefixes on failure.
4. Finish scientific assessments and record their provisional result; close the scientific ledger once, with actual attempt/completion counts and no future science permitted.
5. Complete supervisor/API/device/process cleanup and record the authoritative terminal process outcome. Numerical pass alone cannot override failed cleanup, timeout, incomplete bytes or exceeded caps.
6. Seal the completed/failed evidence manifest only after all authoritative terminal files it references are finalized. Do not run a verifier that requires a closed ledger against a still-running ledger, then misclassify the resulting lifecycle mismatch as a scientific failure.
7. Reserve the separate saved-only review exactly once. It reads the final sealed lifecycle state, validates bytes/coverage/counters and performs only its explicitly budgeted saved-operand arithmetic. It never generates geometry, reevaluates fields, solves a missing root or dispatches the GPU.

If the actual design has different filenames or statuses, the same dependency ordering must be explicit. Do not allow a mutable success flag, uninitialized all-zero output, missing final log or absent process-cleanup record to stand in for completed evidence. An early terminal failure remains a valid negative/incomplete result; no reviewer repair may cause new science.

**Final static disposition.** The numerical design is conditionally cleared for implementation: direct R rotor/body gates, exact policy agreement, deliberate nominal/receiver-inflow subnormal truncation, normal-positive high coefficient, normalized residuals, gated raw-input handoff references, and explicitly noncertifying inward margins are analytically coherent. The new yaw, per-rotor, residual, handoff and exposure rules are engineering choices made before outcomes. Implement only this fixed design, finish the finite controls/generator proof/schema/work ledger, and submit the actual source and lifecycle for independent audit before any freeze or launch. This memo grants no scientific execution or benchmark. Preserve every older failure, skipped reduction, no-candidate decision, unearned confirmation, R8 closure and unresolved physical/temporal limitation.
