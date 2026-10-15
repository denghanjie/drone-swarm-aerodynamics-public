# Prospective source-omission ablation: separate zero screening from approximation

Date: 2026-10-16. **Design only; no new scientific execution.** The only campaign file read for this task was `research/m31-source-omission-2026-10-16/raw/result.json`, under `<REPOSITORY_ROOT>`. Its SHA256 is `5f45a5f7f44480267613fad62c20971de6aa4b673d43f396a4c0af73a8358dc7`; it identifies source commit `88dc542604d902909b7cc96c0bd0ca93b88cab0c`. JSON selection, arithmetic summaries of saved counters/times, and a file hash were used. No scientific module was imported, no code implementation or fixture was created, and no geometry, field, root, case generation or benchmark was evaluated.

Close and publish the current checkpoint first. This proposal must become a separate, prospectively reviewed and frozen campaign with its own launch authorization and budget. It does not amend the completed experiment, extend its deadline, or license a rerun.

## What the saved result establishes

The saved result reports completion and passing gates for all152attempted queries. It reports no integration steps. The following are observations or simple arithmetic on saved counters, not measurements of a Z implementation:

| Saved observation | fresh1000 | fresh5000 |
|---|---:|---:|
| Eligible directed source pairs | 707,024 | 6,614,638 |
| C bounded-zero culls | 684,020 | 6,488,768 |
| C positive-bound omissions | 4,965 | 26,742 |
| C retained pairs | 18,039 | 99,128 |
| B/M rotor visits | 2,828,096 | 26,458,552 |
| C rotor visits | 72,156 | 396,512 |
| B/M profile evaluations | 66,754 | 361,424 |
| C profile evaluations | 62,086 | 338,404 |
| Zero culls / all skipped source pairs | 99.279% | 99.590% |
| Positive-bound omissions / all candidates | 0.702% | 0.404% |
| Profile-evaluation reduction | 6.993% | 6.369% |
| Near-domain fallbacks on these cases | 0 | 0 |

Positive-bound omission means the envelope is positive; it does not prove the actual four source terms are positive. For example, the saved `radial-3` and `downEnd-0` fixture records show positive-bound omission while the full profile count is zero. Do not rename all such selections “positive wake contributions removed” without consulting the retained term evidence. That evidence was not opened for this design task.

The five measured complete-query medians, with the saved warmups excluded, are B/M/C =0.170814209/0.108610083/0.084825875s for fresh1000 and1.888841125/1.333426792/1.121855125s for fresh5000. These are measured technical repetitions of the two fixed inputs. Correctness-call times include different surrounding activity and are not substituted for the prescribed timing series.

The saved error maxima show real approximation effects on the fresh cases: maximum body-thrust error0.000125631758N and0.000141524353N; maximum roll/pitch component errors range from approximately3.00e-6 to3.52e-6Nm. The maximum used-capacity fractions are0.999918879 and0.999999424. These maxima do not establish how many receivers saturate the budget. Both `multipleWeak` and `signedMoment` have zero positive-bound omissions and zero used capacity in the saved result; their descriptive names are not evidence of an exercised positive-omission moment pattern.

**Inference permitted now:** exact-zero culls dominate the reduction in counted rotor visits. **Hypothesis requiring Z:** exact-zero screening also accounts for most of the net time reduction versus M. Counts cannot establish wall-time attribution: a cheap early-zero rotor visit and a supported profile evaluation cost different amounts, and C pays bound construction, selection, allocation and root/load overhead. C/M compares a package containing both zero screening and approximation.

## The intervention: Z

Freeze the existing B, M and C implementations and all physics, numerical margins, source ordering and error targets at the reviewed source bytes. Add exactly one experimental treatment, Z:

1. Z performs the same geometry, grid, neighbor discovery, source envelope, zero classification and near-domain fallback as frozen C.
2. Z culls exactly the source pairs for which C's source-bound function returns the zero category. It retains every fallback pair and every pair receiving a positive envelope, including pairs that C would omit within its capacity.
3. Z runs the existing greedy positive-bound capacity rule in **shadow form**. It computes the same nextUp additions, shadow B, selection mask, positive-bound list and per-receiver records as C, but an accepted positive-bound decision proceeds to all four exact terms instead of skipping them. This controls the selection and bookkeeping overhead in C/Z. It must not remove numerical bound computation merely because Z does not need an approximation budget.
4. Actual Z omission budget is zero, actual positive omissions are zero, and its physical retention set is C's retained set union C's positive-bound-omitted set. Its shadow choices are labeled as such everywhere. A saved actual Z classification can be derived from the shadow record by mapping positive-selected code3 to retained code2; do this outside the timer as persistence work, with the mapping explicitly specified. Do not silently present shadow decisions as actual omissions.

This shadow control makes the primary intervention narrow: evaluate the positive-bound-selected sources versus skip them. The different final fields and resulting solver cost are genuine consequences of that intervention and remain inside complete-query time. It does not measure the best possible zero-only production implementation. A lean zero-only implementation that drops bound-value/selection bookkeeping is a separate future engineering candidate.

For a valid input, Z must preserve full-model loads to the existing full-reference precision gates. Exact-real zero terms do not consume an error budget. Floating-point zero classification remains subject to the unchanged engineering allowance and independent zero-term checks; the old pass is not a universal numerical proof.

The saved counts imply hypothetical Z rotor visits92,016 and503,480 **if** the same decisions were used on the old fresh inputs. The extra visits versus C would be19,860 and106,968. These are algebraic consequences of the proposed control, not executed Z counts or a time prediction. Do not run Z on the closed cases merely to fill this table.

## Falsifiable questions and decision rules

Separate correctness from performance. Any false zero cull, wrong domain decision, changed shadow selection, incomplete required case, or failed full-load/approximation gate fails the new campaign's implementation claim. A correct Z or C that runs slower remains a useful negative cost result.

Primary performance hypothesis H1: positive-bound omission supplies a practically useful incremental benefit over this matched Z. Before any new generation, choose and freeze a threshold. A concrete proposed rule is median paired C/Z query-time ratio<=0.95 on **each** fresh case, with C faster in at least7of8measured blocks on each. The5% threshold is an analyst-selected engineering criterion, not statistical significance or a discovered constant. Report every time, ratio and sign even when the rule fails; do not promote one favorable count into a general result.

Secondary mechanism hypothesis H2: the zero-screen package accounts for at least half the observed net M-to-C savings on both new inputs. Within each paired block, the identity is

`time(M)−time(C) = [time(M)−time(Z)] + [time(Z)−time(C)]`.

Report those two absolute differences before ratios. For a descriptive aggregate attribution, let T_X be the sum of all8measured durations of X on one input. When T_M−T_C>0, report `(T_M−T_Z)/(T_M−T_C)`. H2 holds descriptively if this is>=0.5 for both inputs. Leave the ratio unbounded: a negative number indicates the zero-screen package cost time, and a value above1 indicates positive omission lost time after the zero-screen package. If the denominator is nonpositive, report H2 as unsupported for that input, not as a favorable fraction. Do not add independently chosen medians and pretend they satisfy the identity. This attribution is implementation- and input-specific, including the shadow overhead in Z.

Interpretation is fixed prospectively:

- Z/M improves while C/Z fails H1: report that zero screening supplies the useful measured gain and the additional approximation has not justified its error for this criterion.
- C/Z passes H1 and Z/M also improves: both mechanisms contribute under the stated controls.
- C/Z improves but Z/M worsens: approximation recovers the cost of the bound/screen package; counts alone would have misled.
- Z/C and/or C/M are mixed across inputs: report the mixed outcome without changing seeds, budgets or timing exclusions.

## New confirmation and fixed controls

Use the unchanged24small fixture inputs as **exposed regression diagnostics**, not new confirmation. No new fixture is constructed here. Their existing domain expectations remain fixed. In the future campaign, run B/M/Z/C/I on them so zero and fallback behavior receive a direct ablation check.

For confirmation, propose exactly two new static inputs with the same generator family and shapes10×10×10 and20×25×10, spacings(0.30,0.30,0.50)m, jitter±0.02m and the existing tilt/yaw mapping. Suggested new seeds, chosen here without generation or inspection, are421337 and914629. The coordinator must ensure these have not already been exposed and freeze them before any generation. If already exposed, replace them before the new scientific invocation and document why; never replace after seeing results. A new seed in the same lattice family tests repeatability within that family, not density robustness or a new physical distribution. Increasing count still increases extent at fixed spacing.

Generate each input once in the sole new invocation, save all exact17-column states, and run B/M/Z/C/I on identical input bytes. Do not tune layout, source IDs, threshold, margins or seeds for favorable Z/C separation. Rejecting an input stops the prescribed progression; no “find another valid seed” loop. Do not regenerate or re-time old fresh cases as if they were held out.

Check: all full outputs finite and in the receiver-law range; unchanged residual/bracket/power checks; full Z/M/B agreement with I at the established full-reference tolerances; C's original source and aggregate budget inequalities; every Z/C zero-class source's four independent terms exactly zero; equal C/Z zero and fallback identities; equal shadow positive selection identities, source bounds, accumulated B and capacity decisions; ascending source order and matching retained-term algebra. Compare Z and M bitwise as a useful additional diagnostic, but do not substitute it for the independent reference gates or silently loosen the existing tolerances.

Save complete correctness outputs for B/M/Z/C/I, all input bytes, both actual and shadow semantics, zero identities, source bounds and C per-source term checks, actual rotor/profile counters and root/load diagnostics. The oracle can expose terms in its one existing direct pass; no extra field is required. Same-pass evidence must distinguish a positive envelope with all-zero actual terms from one with positive terms.

Only after correctness passes, perform one warmup query per B/M/Z/C and8measured paired blocks per fresh input. A four-method balanced within-block schedule is:

| Block in cycle | Method order |
|---|---|
| 1 | B, M, C, Z |
| 2 | M, Z, B, C |
| 3 | Z, C, M, B |
| 4 | C, B, Z, M |

Repeat this fixed cycle twice. It balances each method's position and all ordered within-block predecessor pairs; it does not eliminate all between-block, thermal or runtime-state effects. Freeze the warmup order and case order too. Use the same process/runtime, complete-query timer boundary, wall guards and exclusion of persistence for every method; no special cleanup or forced collection applied selectively. Keep the frozen controls' instrumentation and record Z's shadow instrumentation explicitly. Do not reuse geometry, masks, lists, fields or roots between queries. Every timed output must reproduce that method's correctness output under the fixed comparator, and every raw timing/checksum/counter is retained. Eight repetitions are technical blocks, not8independent swarms or a confidence interval.

This proposed matrix has202attempted queries:26inputs×5correctness methods plus2fresh inputs×4timed methods×9passes. A next preflight must independently derive exact shape charges and storage sizes from the final implementation. Plausible conservative ceilings for this stated matrix are26million direct-independent center checks,520million combined C/Z source-bound attempts,4.3billion rotor-visit reservations and1million receiver solves. Retain separate actual counters. These are budgets, not forecasts. A300s executable cap,128MiB raw cap with4MiB failure reserve and separately bounded saved-only review can be considered; they need their own prospective protocol/source freeze and may fail without extension. No hidden microbenchmarks or optional postfailure timing.

## Later idea: cheaper early branching in the bound

This must follow the attribution checkpoint as a different candidate. Do not optimize Z or C during the ablation.

The inspected frozen source from the earlier review computes both downstream center projection and radial norm before testing whether the entire rotor interval is nonpositive-downstream or beyond the downstream cutoff. A prospective E variant could first compute the identical downstream interval and perform these two domain-safe zero exits; compute radial residuals and Math.hypot only for surviving pairs. The existing proof already licenses those downstream exits, so deferring unused radial work need not change source classes or the positive-bound formula. Likewise, the receiver/source projection dot product is currently supplied before source-bound classification; it might be deferred until after domain safety and radial-support screening. Preserve the global tilt check and all finite-input assumptions.

Hypothesis H3: many current zero culls are decided by cheap downstream intervals, and avoiding their radial norm/projection work improves full query time. The result currently aggregates zero reasons, so H3's frequency and time benefit are **unknown**. Neither99%zero share nor a source-level operation count proves avoided hypot cost is the bottleneck; grid enumeration, memory traffic and branch overhead may dominate.

A later E evaluation should freeze one lazy-evaluation change, require source-decision/bound/mask equality with its unchanged parent on all required valid inputs, domain-reject agreement, identical omission capacity and unchanged output gates, and then compare complete-query costs under fresh balanced controls. Reason counters can be collected in the same prescribed correctness pass; hot-loop instrumentation must be equal between compared implementations or disclosed as part of them. The current result cannot retrospectively supply reason counts.

Do not move radial/projection pruning ahead of the near-domain obligation. If the downstream interval can enter the near slab, radial information may be essential to decide whether exact four-rotor evaluation is required, even when the wake is estimated weak. Nor may an early coarse **upper** bound exceeding remaining capacity prove the final tighter bound cannot fit: that inference is invalid. Conservatively retaining such a source would define a different omission policy with different masks and must be evaluated separately. Skipping all bounds once capacity seems full similarly changes zero-screen work and cannot serve as the matched Z control.

## Claims and stopping point

Use “source-level screening of exact zeros” and “incremental effect of positive-bound omission.” Finite-support pruning, broad-phase rejection and error-controlled screening are established techniques. A successful Z is evidence about this implementation/model, not zero-screen novelty. A successful C/Z comparison quantifies the cost/fidelity tradeoff of the frozen positive-bound policy on the new cases; it does not create aerodynamic novelty, prove a universal binary64 certificate, establish physical accuracy, or validate a trajectory/controller/browser-real-time claim.

The immediate next action is closure of the completed checkpoint. This document supplies a falsifiable next question and a controlled intervention. It supplies no implemented Z/E, generated confirmation data, runtime measurement or authorization to begin the next scientific invocation.
