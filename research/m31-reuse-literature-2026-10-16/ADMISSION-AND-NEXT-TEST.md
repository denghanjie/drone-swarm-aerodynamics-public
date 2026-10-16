# Two multirate originals admitted; drone applicability remains a hypothesis

2026-10-16. Read-only literature and source review. Eight delegated source
operations consumed, including one timeout; no additional retrieval is allowed
under this scope. No paper PDF/full text was downloaded or redistributed, no
third paper was opened/used, and no model, predictor, fit or target score ran.

**Admit both originals as method evidence. Do not adopt either as a validated
drone integrator or refresh criterion. Recommend one separately frozen, causal
shadow-prediction diagnostic before any new feedback-motion experiment.** The
proposal below is our hypothesis, inspired by prior methods; it is not a
reproduction of Ahmad–Cohen or reversible RESPA and has no novelty presumption.

The source/result/receipt b8ff0c4/7cdf101/611010f remain closed. The previous
fixed-10-ms held-ratio approximation failed its declared screens despite adequate
refinement. Its public milestone and protocol were read; its numerical results
were not rescored here. The latest raw-bound Three.js viewer remains unchanged.

## Verified original evidence

**Ahmad–Cohen (1973).** The institutional-hosted original is *Journal of
Computational Physics* 12, 389-402. Section 2, pp.391-395, separates regular and
irregular force updates, extrapolates from divided differences (Eqs.9-12), and
corrects force/derivative bookkeeping when neighbors change. It includes fast
approachers in the neighbor treatment. Section 3C, pp.398-400, cautions that
energy behavior need not reliably track close-encounter or trajectory errors.
These are gravitational-method findings, not certified drone error bounds.
The DOI is only discovery-corroborated in this scope; the original identity is
verified. [Original scan](https://courses.physics.ucsd.edu/2019/Winter/physics141/Labs/Lab4/AhmadCohen.pdf).

**Tuckerman–Berne–Martyna (1992).** The original verifies *Journal of Chemical
Physics* 97(3), 1990-2001, DOI10.1063/1.463137. Sections II-III, pp.1990-1993,
derive symmetric propagator splitting; Eqs.3.1-3.8 combine slow-force endpoint
kicks with repeated short-force evolution. Section VI, pp.1997-1998, connects
this to predictor-corrector formulations. Section VII, pp.1998-1999, explicitly
treats Nosé–Hoover extended dynamics with a specified reversible factorization;
its conserved quantity is not the physical-coordinate Hamiltonian. It therefore
does not justify a blanket claim that nonconservative-looking terms make
splitting impossible. It also does not provide this drone model's decomposition
or error guarantee. [Original scan](https://aiichironakano.github.io/phys516/Tuckerman-RESPA-JCP92.pdf).

These source summaries are deliberately limited. No numerical speedups or
figure values were extracted. OCR is imperfect, so the cited equation locations
are not an executable transcription. The paper copies are original published
scans, not verified corrected editions. The bounded status searches admitted no
correction/retraction notice; absence of such a result is not clearance. Direct
DOI access failed in the independent parent scope. See SOURCE-ACCESS.json and
bibliography.json for exact provenance and unresolved metadata.

## Assumption mapping: our analysis of the current model

| Question for transfer | Current drone-model issue | Consequence |
| --- | --- | --- |
| What is slow? | Finite directed wakes depend on orientation, relative position, support branches and changing nominal commands. Euclidean distance alone does not establish a slowly varying load contribution. | Do not label distant neighbors slow without checking the proposed criterion. |
| Is the force additive? | Pair coefficients are geometric, but the source-total closure and four receiver roots couple final loads nonlinearly. | A sum of pair coefficients is not an additive split of the final force/moment dynamics. |
| What happens at membership changes? | Positive support and the dependency graph can change, and near-field/current-domain rejection can be entered during a cached interval. | Prior accepted classifications and valid cached roots do not certify current geometry. |
| Which state is integrated? | Controller updates, motor lag, quaternion normalization, directed aerodynamic effects and contact/guard events are parts of the implemented dynamics. | Reversibility or symplecticity cannot be asserted by replacing only the airflow update. An applicable full split has not been derived. |
| Can a smooth predictor be trusted? | History can become invalid across command, support or domain events. An event visible only at the right endpoint can invalidate the entire predicted interval. | A trend estimate is a heuristic unless event handling and remainder bounds are established. |
| What error matters? | Rotor imbalance creates moments; feedback can amplify local discrepancies. Mechanical energy is not the mission observable of this powered controlled system. | Keep rotor, collective force, moment, attitude and motion errors distinct. Energy behavior is not a substitute. |
| What would save time? | Current geometry/coefficient construction dominates the joint query; a monitor that rebuilds it may cost nearly the reference. | Count every monitor/refresh operation and later measure complete cost. Fewer nonlinear solves alone do not establish practical acceleration. |

The cached stages in the closed ratio-reuse protocol intentionally leave current
geometry/admission/order/residual metadata null. This is an unresolved domain
check, not proof that the state is admitted; valid roots and cache age do not
fill it. A future approximation must not silently treat this fail-open behavior
as inherited scientific permission. Unsupported geometry must remain a reported
failure, or a separately justified conservative check must force an exact refresh.
Neither original supplies that check for this kernel.

No complete published method has been reproduced or adapted in code here.
Multirate grouping, extrapolation and symmetric corrections are antecedents.
Choosing a drone load-ratio predictor or a domain monitor would be our adaptation
decision. The next test is only inspired by prediction, not RESPA, not an
Ahmad–Cohen implementation, and not a physically justified wake-memory model.

The coordinator's bounded HISTORY-INVENTORY was also read. Causal two-sample
linear inflow prediction, nonnegative clipping and analytical refresh envelopes
have already been implemented in the older prescribed-motion studies. The
predictor-stress record retains a startup/source-pitch failure, and M28 already
tested held airflow in actual feedback flight. Its historical bibliography
already names Tuckerman; this task newly verifies the original reading, not the
existence of that attribution. No third cited paper is newly admitted here.

The only distinct proposed quantity below is the later joint-source solved root
vector applied with evolving nominal motors and full current force/moment
assembly. This is different from extrapolating old fixed-hover-source scalar
inflow, but not a new extrapolation algorithm. Historical failures rule out
presenting a warm-history-only score or a retuned startup as complete evidence.
The old moment scale mgD also differs from this model's mgR; use the current
normalization consistently.

## One bounded next experiment, proposed only

**Question:** on the already exposed finest-grid reuse path's saved refresh
states, does one fixed causal first-order prediction of load ratios pass the
existing same-state load screen where a held ratio failed? This tests a minimal
temporal-trend premise before spending on a new trajectory or spatial grouping.
It does not qualify a refresh policy or prove performance.

Use only the published finest-grid event record from the closed result, identified
and byte-pinned in a new protocol. Treat these states as an exposed diagnostic
sequence. Do not regenerate, integrate, choose a new seed, alter their commands
or select a favorable event subset. The proposed new diagnostic allocation does
not reopen the old invocation. Nothing below has been computed in this review.

Freeze one candidate, no tuning: let x[k] be the exact saved fresh four-rotor
root vector at time t[k]. At k=1 use xhat[1]=x[0], the mandatory cold-start hold.
For every k=2 through 200, predict using only the two previous events:

`xhat[k] = x[k-1] + ((t[k]-t[k-1])/(t[k-1]-t[k-2])) * (x[k-1]-x[k-2])`.

The held comparator uses x[k-1]; the oracle uses saved x[k]. Only t=0 initializes
history without a positive-age target. The source sequence must have exactly
the expected 201 ordered events or the test fails input admission. All 200
positive events, including cold start, remain in the primary report. Report the
199 extrapolated events separately only as secondary diagnostics. This is a
deliberately simple secant predictor of roots, not the published force-derivative
algorithm. It may fail around rapid changes or even on smooth events.

At each target state, apply candidate/comparator roots to the same current nominal
motor states, current orientation and fixed body lever arms, exactly as the
frozen load assembly specifies. Compare with the saved fresh load/root output.
No candidate supplies states or commands; no future root enters the prediction.
Do not clip, refit, smooth, adapt slopes, reset after seeing a large residual or
substitute an exact answer. Nonfinite or out-of-domain predicted roots are
candidate failures retained at their event IDs. A root failure must not prevent
reporting other finite event diagnostics.

Before arithmetic, require every source event's saved current geometry/admission,
order, commands, roots and correspondence metadata to pass the retained input
contract. Missing or failed current-state admission invalidates the planned
comparison; old cached-stage null metadata cannot substitute for it. This gate
uses already saved fresh witnesses and does not manufacture current-domain
coverage at unrecorded times. An independent saved-only reviewer should verify
indices, units, causal inputs and current-state load assembly.

Retain the existing normalized local screens: maximum rotor error in mg/4,
collective-vector error in mg and roll/pitch-moment error in mgR, each <=0.001.
Predeclare candidate passage only if all three maxima pass, no candidate root is
invalid, and each maximum is no worse than the paired held comparator on this
same complete 200-event set. Cold-start error cannot be excluded from passage.
The threshold is the inherited numerical engineering
screen, not a physical accuracy requirement. Record signed component errors,
all event-level errors and argmax IDs, not just a pooled average. No confidence
interval over these correlated events is warranted.

Suggested finite resource envelope for that later new protocol: one saved-data
candidate invocation, 60 seconds/512 MiB RSS/16 MiB total new artifacts, plus
one separate saved-only reviewer with the same limits; no retry, new model
solve, timing benchmark, integration or parameter search. Exact source paths,
record hash, parsing/serialization contract and monitor implementation must be
frozen and remotely verified before any scoring. If inputs fail, preserve the
gap. If the candidate misses, reject this secant candidate and do not tune its
slope or choose another cadence in the same cycle.

A pass would justify only considering a separately designed intermediate-time
and current-domain diagnostic. It would not show the predictor is safe between
events, estimate a certified local-error bound, recover the closed trajectory,
save a query, or generalize to new motion. An eventual feedback test would still
need fresh prospective inputs, resolution evidence, explicit event handling and
the full force/moment/motion observables. No automatic next allocation follows.

## Decision boundary

Method evidence is admitted; direct algorithmic applicability and correction
history remain incompletely admitted. The proposed diagnostic is a new question
on exposed saved evidence, with explicit failure handling. If the coordinator
requires a theorem-backed refresh mechanism rather than a heuristic premise
screen, the honest decision is **unresolved**: these two originals do not furnish
the missing coefficient/geometry-to-load error certificate or an applicable
reversible flow split. Do not present a fresh implementation as a published
method merely because it uses two rates.

Physical validity, novelty, application tolerances and 5000-drone browser cost
remain unresolved. The next substantial numerical milestone still requires its
own raw-bound 3D result; this literature checkpoint preserves the existing viewer.
