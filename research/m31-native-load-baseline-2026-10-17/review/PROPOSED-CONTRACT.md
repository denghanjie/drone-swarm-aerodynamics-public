# Proposed native-load baseline contract

2026-10-17. Source-only decision draft for parent review. Repository: `[PUBLIC_REPOSITORY_ROOT]`.

This note proposes one bounded prerequisite: qualify and time an ordinary binary64, current-input, full-contribution load chain before choosing grouping or temporal reuse. It authorizes no implementation, scientific import, target generation, browser launch, execution allocation or large-state run. Fresh seeds, snapshot times and new numerical control literals remain unset. Existing frozen artifacts remain unchanged.

Parent decision after the initial draft: implement source for **retained-state qualification only**, then review all source before any allocation. The intended first numerical stage is exactly 12 F/L target calls on the six retained states in named Chrome, with actual delivered native rounded loads checked offline. No fresh generator or performance claim belongs to that first stage. The fresh/timing envelopes below are conditional later proposals, not part of the adopted first implementation stage. Separate parent instructions authorize wrapper/checker source drafting; this document grants no execution authority.

## 1. Decision and claim boundary

Use the existing browser-screen F builder and ordered O solver as the performance-oriented starting point, with its L all-pairs builder as the matched semantic comparator/fallback. A small separately named wrapper must define raw input/ID validation, actual native load outputs and numerical failure handling. Preserve their initial arithmetic and solver recipe; do not copy the direct-load diagnostic's oracle coefficients or 48-round proposal recipe into a supposedly cheap baseline.

The output is **ordinary native loads with finite offline qualification against M-current**. It is not Q-current: there are no required per-query outward load enclosures, full row certificate, certificate-tolerance decision or online proof of admission. Native success must not be labeled `certified` or `proved admissible`. M-current remains the explicitly named mathematical reference for the offline audit. Passing a finite audit is evidence on those inputs, not a uniform native/exact bridge, physical validation or closed-loop guarantee.

“Full contribution” describes the algorithm: enumerate the full source universe, retain every positive native term, and make no deliberate distance truncation beyond the declared formula's zero branches, source deletion, grouping, stale reuse or per-row truncation. Native/exact branch or positive-support discrepancies must be exposed by the offline audit; this descriptor does not assert exact membership for all real inputs. A material semantic discrepancy cannot be hidden by a small aggregate load error.

The prerequisite answers whether cheap current binary64 coefficient construction plus a full solve already meets strict load accuracy, and what it costs. Replacing rational proof work with doubles is not itself an algorithmic speedup or novelty result. If this baseline is accurate and satisfies the eventual application budget, there is no demonstrated need to approximate it. If it is inaccurate, resolve the model/interface discrepancy before grouping. If accurate but costly, use measured stage costs to choose the next single direction.

## 2. Input, native computation and output

Freeze one raw interface: N rows of exactly 17 binary64 words (position, velocity, xyzw quaternion, body rate, four nominal rotor forces), explicit unique stable IDs and a declared finite N limit. Preserve the raw words, ID mapping and constants as provenance. Sort raw rows by ascending stable ID before the historical index-based builders, and charge that validation/canonicalization; return results by the same explicit IDs. This is a new wrapper, not a claim of historical byte identity under arbitrary permutations. Reject malformed/duplicate IDs and wrong shape explicitly.

Use the same declared native preparation and constants in F and L. Record/check the prepared center, rounded rotor points, axes, offsets and constant words against the common offline adapter. All raw fields must be finite and every nominal force positive; finite/positive totals and normalizers require explicit checks. The current frozen mg/R words are `3fd0f3a14cec41dd` and `3fa4462fb7ff5035`; preserve supplied words rather than substituting ideal algebraic constants. Raw-to-prepared arithmetic is part of timed computation. An oracle may inspect it offline but may not provide it for free to the native query.

Retain F's existing eligible component screen and full L fallback, existing guard precedence, actual positive-term ceiling 2,000,000, descending-z/ascending-ID operational domain, native O one-pass solve and 56-bisection cubic closure. Preserve alpha-zero handling. F still visits all ordered nonself pairs; it is not an indexed spatial search. The initial chain retains its native residual check. Removing residual work or changing the root recipe requires a separately declared later source change.

The wrapper must return and consume actual rounded native values for every ID:

| Output | Required native formula and order |
|---|---|
| Rotor loads | `T[r] = nominal[r] * x[r]`, rotor order 0,1,2,3. The force law is linear in x, not x squared. |
| Collective | Left-fold sum of the four returned T values. |
| World force | Each actual prepared axis component times the returned collective. |
| World moment | Left-fold sum of `cross(actual offset[r], actual axis) * T[r]`, with cross-product grouping and rotor order frozen. |

The signed actual axis/levers matter. Do not substitute an assumed orthogonal frame, body wrench/yaw torque, cached ratio adapter or a positive absolute-value moment sum. Return x/y and native residual diagnostics if useful, but do not let them replace the four delivered load arrays. The old checksum of y and summed T does not satisfy output consumption. All required rotor, collective, force and moment words and their ID/status association must be read by the timed consumer.

Expose native success, input/domain refusal, numerical-range failure and resource failure separately. Native coefficient, alpha, ratio, source y and load arithmetic must have explicit finite/range checks. Unsupported subnormal/underflow behavior may refuse the query; a `NaN` comparison or lost positive source must not silently produce success. Record independent offline reference admission/rejection/unresolved/resource status separately from native status and accuracy verdict. No failed attempted case disappears from the denominator.

## 3. Exact offline qualification and semantic differences

The independent exact audit reconstructs M-current from saved raw words/IDs and the frozen common preparation policy. Use the existing exact branch/reference machinery with its bounded small-state domain (reference cap 180), exact four-force totals/weights and directed reference uncertainty. Compare the delivered native load words as exact dyadics to reference load enclosures. Reconstructing exact loads from a native x would audit different outputs and miss native load-assembly error.

Preserve all four primary criteria, each required for every admitted fresh state and admissible accuracy control:

| Error category | Normalized maximum over drones/rotors | Primary threshold |
|---|---|---:|
| Rotor | `max |T_native - T_reference| / (mg/4)` | <= 1e-8 |
| Collective | `max |C_native - C_reference| / mg` | <= 1e-8 |
| World force | `max ||F_native - F_reference||_2 / mg` | <= 1e-8 |
| World moment | `max ||M_native - M_reference||_2 / (mg*R)` | <= 1e-8 |

Reference uncertainty belongs in each error enclosure. Pass requires its upper endpoint <= 1e-8; lower endpoint > 1e-8 establishes failure; overlap is unresolved. Componentwise vector maxima cannot replace Euclidean norms. No relaxed tier, average, percentile, cancellation across drones or native residual can rescue a failed primary category. Expected rejected controls pass only their declared status/precedence assertions, never count as load-accuracy successes.

The source freeze must explicitly preserve and audit these differences:

| Surface | Native behavior that differs from exact M-current |
|---|---|
| Geometry admission and branches | Rounded subtraction/dots, Math.hypot norms and finite boundary decisions versus exact prepared-word comparisons. |
| Radial/profile arithmetic | Grouped radial/xi arithmetic versus the exact squared formula; algebraic equivalence does not imply identical rounded results. |
| Projection precedence | Native profile work precedes the late projection-zero classification; exact reference can exit earlier. Near-field rejection precedes projection in both. |
| Source normalization | Rounded left-fold S0 and `sqrt(sum(f*x)/S0)` versus exact total and exact weights. |
| Positive support/caps | Native positivity, underflow and native K/scaled-cap decisions versus exact positivity/caps. |
| Source order and solve | Stable-ID canonicalization plus ordered native reductions/56 bisections versus enclosed exact roots. |
| Loads | Returned native products/cross products/sums versus enclosed exact physical-unit loads. |

Record native/exact preparation, admission, positive-edge and load disagreements with witnesses. A boundary disagreement is not a license to change the reference, tune a tolerance or replace a fixture. A source-only decision must resolve whether a mismatch is an explicitly unsupported native domain or a bug before any successful compatibility claim. In particular, a native admitted state that the reference rejects or cannot resolve is not a qualified state.

## 4. Minimal proposed qualification envelope

First qualify delivered native rounded loads on **all six retained N=64 states**: `run-a-t0`, `run-a-t5`, `run-a-t10`, `run-b-t0`, `run-b-t5`, `run-b-t10`. These are exposed regression inputs, not fresh evidence. Use the pinned raw-state/reference association from `research/m31-normalizer-replication-2026-10-17/results/index.json` (SHA-256 `3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393`) and the checked full-reference load enclosures from the completed direct-load diagnostic. Reuse independently verified saved exact reference work when identity/semantics match; do not recompute it merely to create another campaign. The native runtime must still construct its own coefficients and delivered loads from raw input. Make exactly one qualification call per native method/state in named Chrome: **12 target calls total**, without performance repetitions or supplying oracle coefficients. Any recorded durations are diagnostic and cannot be promoted as a performance result. All six must remain in the report, including any native/target status disagreement.

Only after that retained-state/control gate passes and a separate source decision adopts the later stage, reserve **two fresh N=64 post-initial moving-state slots**, one from each of two independent fixed generation recipes/seeds. The seed/time literals, generator duration, initial-state recipe and exact snapshot rule must be frozen prospectively; none is selected here. Preserve both initial states and both scheduled snapshots before any target force evaluation. Require nonzero exact coupling in each fresh state so nominal zero-coupling answers cannot constitute the entire accuracy evidence. If a snapshot is unavailable, rejected, unresolved or lacks the declared coupling, retain that outcome; there is no substitute seed/time. Two slots are a minimal transfer check, not a representative population or long-trajectory study. The source is frozen before fresh-state generation, and named-browser performance timing begins only after both fresh states also pass all four strict categories.

Retain existing fixed controls without selecting them by result:

- The complete 48 named F/L screen controls and six separately paid cross-call ownership builds from browser-screen `source/controls.cjs`.
- The four moving-admission controls `positive`, `distant-zero`, `raw-force`, `order-incompatible`. The positive fixture has three drones; the other three have two. Preserve their fixed raw literals and expected exact status assertions.
- The existing browser Buffer-subset adapter assertions when reusing that delivery layer.

Deduplicate coverage before source freeze and add only missing semantic microcontrols. Use the auditor's eight coverage families: shape/ID ownership; geometry norm bands; down/near/radial precedence; projection/cap boundaries; normalizer extremes/nonfinite handling; graph order and ID permutation; linear tilted/canceling loads; delivered-load/ID corruption. Eight families do not mean eight fixtures. A proposed hard ceiling is **24 additional literal fixtures, each at most four drones**, plus at most four deliberate saved-output corruptions. Use below/equal/above checks where meaningful; do not promise reachability of a downstream guard that upstream valid geometry excludes. Declare unit-only controls separately. If this ceiling cannot cover a material gap, stop for a source-only contract revision rather than quietly expanding or searching fixtures.

Run each independent exact control/state reference once, with a frozen finite refinement cap; unresolved stays unresolved. F/L native parity and the independent reference have distinct jobs. Native F/L equality alone does not establish M-current accuracy. A corrupted rotor load, squared-force law, wrong frame or ID association must be caught by the audit. Retain load/control failures even when performance measurements are not pursued.

Proposed execution ceilings for later reviewed source freezes, **not an allocation now**: one retained-state/control qualification invocation; after its pass, at most one two-slot generation invocation and one fresh-state reference/qualification invocation; at most two fresh Chrome process/profile slots; one independent saved-result checker; 1,500 seconds total supervised wall time, 256 MiB combined scientific artifacts and 16 MiB metadata/logs. Per-stage time/RSS/output ceilings and a deterministic stop order must fit within that envelope and be frozen before launch. This permits a small concrete native wrapper/checker implementation and retained-state qualification to be the next stage; it does not require waiting for fresh-seed selection or a coupled-flight implementation. No automatic retry, replacement, extra precision pass, wider tolerance, extra seed or continuation beyond a cap. Failed/partial evidence remains append-only and counted. No N=5,000 execution is included.

## 5. Named-Chrome timing and fair comparators

The first timing is a native cost characterization. F and L must share raw words, ID policy, constants, outputs, status rules, residual obligation and timing boundary. Use the exact reference only outside that clock; its running time is not the native speedup denominator. Historical timings are context because their checksum/interface differs. `fullSymbols=false` was already used historically; do not claim a saving from removing dense diagnostic tensors.

The bounded proposed timing schedule is two fresh Chrome processes/profiles, two qualified fresh inputs and both F/L methods. Per process/input/method: record one first-use call, perform two fixed warmup calls, then record five warmed calls. This is at most 64 state-method calls across the two processes. Order and interleaving must be fixed before results; first-use order is counterbalanced, and first-use means first use of that method/input within the declared shared process, not a guarantee that all shared code is JIT-cold. Preserve every call's time, status and output identity; warmup is a separately reported cost. No adaptive warmup, GC filtering, repeated best-of search or median-only success test. Report raw calls, process medians and observed maxima; this finite schedule cannot prove tail latency.

Run fixed native controls once per process before successful timing claims, preserving their cost separately. Audit the first-use Chrome outputs against the saved exact reference before allowing warmed timing for that process/input/method; Node qualification is not a substitute for browser output accuracy. If a control/state fails the semantic or accuracy gate, retain first-use/diagnostic costs already available but do not proceed to warmed performance repetitions or make a qualified performance claim. Exact reference/audit must check every distinct returned output identity; equality hashes may avoid duplicate exact reference construction but cannot substitute for output ownership/identity checks.

Name the actual Chrome product/version, binary/framework hashes, OS/architecture and machine identity; preserve process/profile launch configuration, source/bundle hashes and timing API details. Reuse the already reviewed bundle-slice verification pattern. The historical identity is Chrome 155.0.8059.80, darwin arm64, Node v24.19.0 and Playwright 1.62.1; those pins are historical, not proof of the installed runtime today. Verify the runtime for a future run and stop on an unreviewed mismatch. Do not report a Node microbenchmark as Chrome feasibility. A headless named-Chrome result supports that exact runtime/configuration; visible interactive app behavior needs a later matched check.

For any later grouping/reuse performance claim, the denominator must be the strongest applicable qualified current native alternative under this same complete interface. At minimum report F and L; do not compare only with the rational reference or a deliberately weaker scalar path. The already present native aerodynamic grid and typed assembly are known alternatives: either qualify/include an applicable stronger path in that later comparison or state a source-based exclusion before looking at new target results. This prerequisite does not require implementing their combination or claim F is universally fastest. Speed ratios may be descriptive; no arbitrary fixed percent gain is the pass criterion.

## 6. Query, step and application timing boundaries

The native **query clock** starts when the current raw input and IDs are available to the query, before any required row decode/copy, shape/ID checks, canonicalization or preparation. If input is already in native arrays, identify that entry format and charge every conversion the application needs. The clock ends only after the consumer has read all required per-ID statuses and rotor/collective/world-force/world-moment outputs. Include:

1. Input validation/preparation, span/screen work, all current coefficient construction and any fallback.
2. Nominal scaling, caps/domain checks, graph order, the full solve and the retained residual.
3. Actual native loads, output allocation/copy and the full output consumer.

Current matrix/prepared-state construction, an exact admission oracle, previous x/y, final loads or prior-query geometry cannot be free prerequisites. Constant/source loading can be amortized only with its separately reported initialization cost. If later workers or devices are introduced, end-to-end query latency includes request queueing, transfer, synchronization and returned-output consumption. Count fallback and unsuccessful query costs too. Stage timers are diagnostics; their sum must reconcile with the enclosing wall timer without subtracting overhead or GC pauses.

Separately report startup/bundle verification, input acquisition/transport, browser/JIT warmup, evidence encoding/hashing/persistence, exact offline audit and rendering. The complete supervised duration remains available. These exclusions must be identical for F/L and later candidates. If real application input acquisition/rendering lies on its critical path, it belongs in application latency even if outside the numerical query clock.

The **complete current-step clock** starts with the current application state before its scheduled controller/coupling work and ends after integration/state update, required safety work and consumption of the new state. Charge the actual number of aerodynamic queries at their actual integration locations; state whether controls update on that step and distinguish controller-update steps from others. A frame deadline also includes its required rendering/queue work. If no coupled integration consumer exists, record complete coupled-step cost as **not yet measured**. Adding an aero-query time to an old airflow-off timing is only a cost estimate, not a measured coupled step or closed-loop result. This query prerequisite must not silently invent a new force/moment integration policy merely to manufacture a step timing.

## 7. Cadence evidence and conditional deadlines

The historical browser generator imports `outputs/milestone-31-source/sim.cjs` and requests `dt=0.0025`, while its returned configuration explicitly says `airflow:'off'`. The simulator declares `P.controlDt=.01` (line 4), updates controls at `step % Math.round(P.controlDt/dt) === 0` (line 43), and calls `F.integrate(s,u,dt)` once per integration step (line 44). It passes no aerodynamic force. The imported `outputs/step02c-source/physics.cjs` RK4 integrator evaluates four derivatives with the same supplied external vector, default zero. Therefore this source establishes 400 integration steps/s and 100 controller updates/s for that configuration, **not an aerodynamic query frequency**.

Before scoring application feasibility, freeze the actual coupling location, query multiplicity, reuse policy, controller/integration cadence and wall-clock target. For a real-time configuration with one fresh aero query per 2.5 ms integration step, 2.5 ms is only a provisional necessary upper budget for that query; the full step needs time for everything else. Four current-state queries within an RK4 step would have a different aggregate cost. One query per 10 ms controller update would change the current-load policy; it is not licensed by the airflow-off source. Temporal holding/multirate reuse needs its own accuracy experiment. A 60 Hz/16.67 ms display assumption, if later adopted, is distinct from both cadences.

Until those choices are explicit, report query cost and any actually measured complete step cost without an achieved-deadline label. With a future frozen budget, report every observed miss and the full cost, not an arbitrary percent improvement. Passing a finite observed maximum is finite evidence, not a hard real-time guarantee.

## 8. Stop gates and connection to 5,000 drones

Proceed in order: source/runtime identity and complete wrapper/control freeze; fixed controls and all six retained-state native-load qualifications; only after their pass, preservation of both prospective raw states and independent reference admission/four strict error verdicts; then first-use Chrome output qualification and matched warmed-browser cost characterization. Numerical qualification failures, unresolved references and resource limits close the attempted stage as such. A source correction requires a new explicit source decision, not a hidden rerun of the same allocation.

This prerequisite does not meet the 5,000-drone objective. N=64 exact qualification cannot establish N=5,000 accuracy, support/cap behavior, memory use, latency or coupled-flight stability. F remains quadratic pair enumeration and the two-million-positive-term guard remains binding. A later separately bounded N=5,000 current-input browser measurement must retain its own domain/resource failures and complete output costs; it cannot call a small-state audit a full-scale proof. End-to-end closed-loop and physical/model validity remain separate obligations.

The fixed 10% omission route is already closed by the completed direct-load diagnostic. At most two deferred directions remain relevant after this baseline: contribution-preserving spatial aggregation, or current-valid temporal reuse with explicit refresh. Choose neither here. A baseline that passes strict loads but misses the real application budget should identify whether preparation/coefficient enumeration, solve, output handling or the rest of the step dominates before new approximation work.

## Source provenance used for this desk result

The coordinated inventory is `/tmp/m31-native-baseline-source-audit.md`, 24,127 bytes, SHA-256 `148b36a52fcbcbc4daf188dbf71a1e4c04b7a932bd4fbfd3338836ed4e6740b5`; its 31-file pin list is `/tmp/m31-native-baseline-source-pins.json`, 5,692 bytes, SHA-256 `4550ea1ac94d229860d892f4ed68526c4c0b4e7a7fe11b02ac06691ee19687c7`. It documents guard precedence, solver arithmetic, model differences, browser delivery and exact native source pins.

Additional directly checked source hashes:

| File relative to repository root | SHA-256 |
|---|---|
| `outputs/milestone-31-source/sim.cjs` | `2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e` |
| `outputs/step02c-source/physics.cjs` | `0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1` |
| `research/m31-browser-screen-2026-10-16/source/generate.cjs` | `fec8b14b804c8fc0e930172c2e8f0fae620a33727ca5ed31b76932b569d440cc` |
| `research/m31-moving-admission-2026-10-17/source/config.json` | `0a6b876edb63f13ce17ac81f996dea741e93abe72bdb28b7c6649626ffab278e` |
| `research/m31-moving-admission-2026-10-17/source/run.cjs` | `e1849f95cbd2bef9fbea1b4e45bb7f2b837bd6184711f60b2374d4e418d55460` |
| `research/m31-current-bound-design-2026-10-16/ADOPTED-DESIGN.md` | `702d64e84c3fc12fdc9e85cb59abf4dd00e8df010647e1567a47eed49ee5387c` |
| `research/m31-browser-screen-2026-10-16/runtime.json` | `500a1522833696a7c4fff4bb3eeaf84514304ac101148ca11f56968bfced4460` |

Only source/provenance reads, byte hashing and this markdown draft were performed for this contract. No fresh target, native numerical query, exact scientific evaluation or browser execution occurred.
