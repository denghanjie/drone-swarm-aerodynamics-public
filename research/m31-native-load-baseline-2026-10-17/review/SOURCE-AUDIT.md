# Source-only audit: ordinary binary64 full-contribution native-load baseline

Date: 2026-10-17. Repository: `[PUBLIC_REPOSITORY_ROOT]`.

Scope: source/schema reads, byte comparisons and SHA-256 hashing only. No scientific module was imported, no numerical fixture or target was executed, no result file was read, and no new seed, target, tuning choice or execution allocation was selected. Existing frozen sources/results were not edited. Reading historical fixed fixture definitions is not a new control run. This memo is a prospective inventory and recommendation, not qualification evidence.

## Recommendation

Use the existing **browser-screen F native coefficient builder plus its unchanged ordered O solver** as the performance-oriented full-contribution candidate, and its **L all-pairs builder** as the semantic comparator and fallback. Add only a small, separately named wrapper for a complete raw-state input contract, explicit ID order, native finite-result checks, and four native load outputs. Preserve the arithmetic grouping, threshold order, all positive terms and solver from those sources for the first prerequisite. Do not start by porting the exact-rational coefficient/certificate machinery into the browser.

The source already supports browser execution; a new browser numerical kernel is unnecessary. This recommendation does not assert that F equals M-current, that F is faster than L on a new interface, or that native results meet 1e-8. Those are finite offline qualification questions. The adopted ordinary-native output contract should explicitly supersede Q-current's online certificate output obligation for this prerequisite while preserving M-current as the named offline exact-reference target.

The decisive sources are:

| Role | Existing source | Reuse decision |
|---|---|---|
| Native screened preparation/coefficient assembly | `research/m31-browser-screen-2026-10-16/source/kernel.cjs` | Use F through `build(states,'screen',false)` or its query wrapper; adapt the latter to materialize/consume complete loads. |
| Native all-pairs comparator/fallback | same package `source/lean-anchor.cjs` | Use L; it is byte-identical to `m31-typed-assembly-2026-10-16/source/kernel.cjs`. |
| Ordered solver and residual | same package `source/anchor-kernel.cjs` | Reuse `schedule`, `solve(q,'O',...)`, `residual`; byte-identical to the coupled-cost kernel and typed-assembly anchor. |
| Native fade/pair semantics | same package `source/reference-excerpt.cjs` | Preserve as the semantic anchor, including guard precedence. |
| Browser delivery | same package `source/browser.js`, `browser-bundle.js`, `source-bundle.json`, `browser.html` | Reuse the loader/byte-verification design, not the old campaign allocation or schedule. |
| Prospective browser identity and containment | same package `runtime.json`, `source/controller.cjs`, `source/run.py` | Reuse structure and provenance; runtime must be reidentified for any future run. No browser was opened here. |
| Exact reference semantics | `m31-normalizer-replication-2026-10-17/source/baseline/{adapter.cjs,pair-prepared.cjs,spec.json}` and `m31-moving-admission-2026-10-17/source/semantic-reference.py` | Offline mathematical reference only; preserve raw/prepared identity and exact force weights. |

Source-byte verification completed: the current browser bundle matches the byte length/hash in `source-bundle.json`; all five embedded slices match their declared pins and standalone source files. This is a byte check, not execution or proof of correctness. All exact file pins are in the final section and `/tmp/m31-native-baseline-source-pins.json`.

## What the native candidate actually does

### Preparation and coefficients

The native packed preparation uses 28 doubles per drone: center, rotated thrust axis and four rotated rotor offsets. The raw layout is 17 values: center 0–2, velocity 3–5, quaternion xyzw 6–9, body rate 10–12, nominal rotor forces 13–16. The numerical builder assumes this layout; it does not itself implement a complete shape/ID contract.

Rotation is `t=2*cross(q,v); u=cross(q,t); result=v+(q.w*t+u)` with the displayed grouping. This matches the current M-current adapter's operation grouping. Receiver rotor points use the rounded binary64 center-plus-offset sums. The four-force total S0 is a native left-to-right reduction from zero.

Preparation records native `Math.hypot` quaternion and axis norm errors (limits 1e-10 and 1e-9), offset norm error against R and offset/axis dot error (both 1e-9), input finiteness and strictly positive nominal forces. Invalid geometry is not waived by a far-center shortcut. All values in the supplied state row are checked for finiteness, including unused velocity/body-rate fields.

F first checks finite center coordinates and finite per-axis spans in [0,256]. If this preflight is ineligible, it delegates to unchanged L and pays its preliminary preparation/predicate plus the full fallback. If eligible, it still visits every ordered nonself pair in ascending source index. A maximum component difference >=4 skips the center norm; otherwise the native center norm/guard path is unchanged. **F is not a spatial-index enumeration method.** Its `finiteRuntimeOnly` metadata expressly disclaims a portable `Math.hypot` equivalence theorem.

Guard/branch precedence is preserved:

1. Nonfinite center norm, norm >512 or center component >257 is invalid before center >=3 gives zero.
2. Rotor displacement components must be finite and <=258; down must be finite and have magnitude <=1024. Then down<=0 is zero and down>=2.5 is zero.
3. Native residual-vector radial norm must be finite and <=2048. If down<2.5*D, radial<0.15 is unsupported near field; the remainder of that slab is zero.
4. The native width must be positive and finite; radial>=3*width is zero.
5. Projection is `max(0,receiverAxis dot sourceAxis)`. Native profile and fades are evaluated before the projection-zero classification. Speed must be finite, nonnegative and <=128.
6. Every strictly positive native speed becomes an entry. Its native scaled value `K*sqrt(S0_source/mg)` must be finite and <=128. The 2,000,001st actual positive term throws immediately; there is no row truncation or positive-term budget pruning.

Normalized coefficient arithmetic is exactly the native grouping `K * sqrt(S0_source/mg) / sqrt(nominal_receiver_rotor/(2*rho*A))`. Native positive underflow and source-total/normalizer arithmetic therefore matter.

### Solve and output

The inherited O solve refuses any nonadmitted model or any positive dependency violating descending z then ascending input index. It is a one-pass ordered solve over the resulting directed graph, initialized with source y=1. Each rotor contraction is an ascending-source-index left fold of `aa*y`. Its cubic closure is 56 native bisections on [0,1] using `x*x*x+alpha*x-1>0`, with an exact alpha===0 shortcut returning 1. Then:

- rotor ratio x is the native cubic result;
- rotor force T is `nominal*x`, **not nominal*x*x**;
- source y is `sqrt(left_fold_sum(T)/S0)`.

The iterative P alternative is capped at 64 rounds with a log-distance <=1e-11 stopping rule and still rejects order-incompatible graphs. It is not needed for this baseline. The current native O source already supplies the straightforward full-contribution solver; forcing the diagnostic's 48 simultaneous updates would add a new algorithm and cost.

The query also evaluates a full native residual map and consumes a small checksum. The residual is useful finite diagnostics, not an exact error certificate. The checksum covers y and summed T, with first/last K, and does not materialize all required loads.

For the new wrapper, use the already prepared axis/offsets and the native T values to return:

- `rotor[4] = nominal[r]*x[r]`;
- `collective = left_fold_sum(rotor)` in rotor order 0,1,2,3;
- `worldForce[k] = axis[k]*collective`;
- `worldMoment[k] = left_fold_sum(cross(offset[r],axis)[k]*rotor[r])`, with an explicitly frozen native cross-product and reduction order.

Return and consume the actual native rounded values. The offline checker must decode those returned words exactly and compare them to independent reference enclosures. Recomputing exact loads from x would audit a different output and omit load arithmetic rounding.

## Compatibility with M-current and the completed diagnostic

| Area | Ordinary native source | M-current/offline exact model | Required handling |
|---|---|---|---|
| Constants | Native expressions for mg, A, R, D, induced and kappa | Frozen supplied binary64 words interpreted as exact dyadics | Record actual constants/prepared words; verify identity before comparison. Do not silently use ideal pi or recomputed algebraic constants. |
| Preparation | Same rotation grouping and rounded rotor points; native norm/dot checks | Exact rational checks on supplied prepared words, including squared norm bands | Audit preparation identity and admission separately; a native admission is not proof of exact admission. |
| Geometry | Rounded subtraction/dot, `Math.hypot`, rounded radial/profile arithmetic | Exact dyadic differences/dots/residual squared norm, exact branch comparisons | Boundary disagreement is a recorded model/admission discrepancy; never convert it to an admitted zero or silently drop it. |
| Projection | Profile arithmetic happens before projection-zero classification | Exact projection<=0 exits before profile arithmetic | Preserve native source and explicitly test/report this distinction offline. Near-field rejection precedes projection in both. |
| Radial profile | Native `xi=(radial/D)/(spread*(down/D-origin))`; denominator `1+kappa*xi*xi` | Exact xi²=r²/width², then outward reference square roots/fades | No identity claim from algebraic equivalence over reals. |
| Forces/weights | Rounded S0; y=`sqrt(sum(f*x)/S0)` | Exact S0=sum supplied forces; exact weights f/S0; y=sqrt(sum(w*x)) | Compare against exact target offline. Keep native grouping declared; do not normalize weights or clip to force agreement. |
| Positive terms/caps | Native term>0, native K and scaled cap tests | Exact branch/cap decisions with reference unresolved states | Preserve native full terms and distinguish reference rejection/unresolved from native success; no selected-case denominator. |
| ID/order | Index-ordered rows and equal-z index tie | Stable-ID provenance and ascending stable-ID tie | Either define native IDs as input indices or validate unique stable IDs and canonicalize rows by ID before build, charging that wrapper. Never silently relabel indices. |
| Solve | Ordered one pass,56 bisections, native finite arithmetic | Exact-reference ordered roots with128 rational bisections and192-bit source bounds | This is a numerical approximation to the target; residual alone does not certify it. |
| Loads | Required native four-output computation is missing | Exact force ratio is linear; world force and moment use prepared near-unit axis/levers | Add native materialization, and compare the returned rounded words. |

The completed direct-load diagnostic is also not a native implementation template: it uses Python binary64 proposals from midpoints of already available exact coefficient enclosures, 48 simultaneous updates,54 bisections, and precomputed normalized weights. Its cubic comparison is `mid^3+alpha*mid>1`, different from the anchor's subtract-one expression. Its saved candidate loads are exact rational reconstructions from the proposal ratios. Those are appropriate diagnostic semantics but do not demonstrate the proposed browser coefficient-to-native-load chain.

All four primary offline criteria remain strict normalized error bounds <=1e-8: maximum rotor component divided by mg/4, collective divided by mg, world-force Euclidean error divided by mg, and world-moment Euclidean error divided by mg*R. Reference uncertainty must be included in the comparison. An unresolved enclosure remains unresolved; widening the tolerance or treating native residual as a substitute does not establish a primary pass. Any secondary relaxed tiers are separate descriptions.

## Spatial and storage options

The byte-identical anchor contains a purpose-built aerodynamic grid: span<=256 preflight, origin-relative coordinates, cell width4, a halo around center +/-3, sorted unique ascending candidates, and all-pairs fallback when preflight fails. It preserves world-coordinate arithmetic. It is a viable later enumeration comparison, but selecting it now would introduce another builder path to qualify. First establish the F/L native-load chain, then qualify any grid variant against L under the same output and timing obligations.

The typed-assembly T path offers capacity-N row scratch and4096-entry chunks with final owned arrays, no truncation, and accounting metadata. Its source is already present through lean-anchor, but F's public screen path does not select the internal typed flag. Combining F and typed assembly is a new implementation and should not be assumed qualified or faster. Source accounting does not establish heap peak or garbage-collection cost.

The generic `outputs/milestone-31-source/grid.cjs` is a Boids neighbor grid with native distance filtering; it does not provide the aerodynamic guard/fallback contract. `wall-filter.cjs` is a Dykstra obstacle/speed constraint projection, and `geometry.cjs` supplies obstacle distances, so neither is a wake-zero filter. `outputs/step03b-source/wake.js` explicitly excludes force law, rotor response and superposition; its ideal power ratio is not a force ratio. The rigid-body physics `wrench` includes body torque and yaw reaction torque. The force-ablation/ratio-reuse adapters normalize quaternions and apply body torque corrections, and ratio reuse uses cached x. These are not the requested instantaneous world-load output semantics.

## Minimal failure and boundary controls to freeze before any run

These are control families to specify prospectively, not chosen numerical cases or authorization to execute them.

1. **Input and ownership:** exact N×17 shape, fixed N/resource limit, unique permitted stable IDs and deterministic mapping; reject invalid/empty input if not explicitly supported; finite raw values; positive forces and finite positive totals; input and output ownership across repeat/fallback calls. The native builder's `.every`/slice operations alone are not a complete shape gate.
2. **Existing screen invariants:** retain the48 named controls in `source/controls.cjs`, covering neighbor3, cell/component4, span256 and adjacent representable values, center257/258 fallback, nonfinite/overflow/coarse-translated coordinates, signed zero, near-field/far mixtures, duplicate positions, dense plane sizes, bad quaternion/nominal/overflow/cap mixtures and unequal forces. Retain the six cross-call ownership builds as definitions. Do not infer pass results from this inventory.
3. **Exact/native branch boundaries:** define below/equal/above controls for quaternion/axis/offset admission limits; down0, minDown*D and downCut; near radius; width/radial cutoff; projection0; K and scaled cap128. Preserve precedence cases (invalid or near-field paired with an otherwise-zero condition). Some scalar guard surfaces may be unreachable under valid upstream geometry; exercise those through declared unit controls or record the upstream rejection rather than claiming an end-to-end reached branch.
4. **Normalizer and arithmetic range:** unequal nominal forces, very small positive forces and highly unequal scales, rounded total overflow, normalizer/aa/source y/root/output nonfinite or nonpositive behavior. Add explicit runtime refusal for any nonfinite coefficient/alpha/ratio/load or invalid denominator instead of letting a `NaN` compare pass. Do not promise all positive subnormals are supported. Native speed underflow-to-zero and exact positivity disagreement belong in the offline report.
5. **Graph and full contribution:** admitted descending graph; equal-z ID tie; a positive edge violating the order; cycle/order incompatibility; changed input permutation with preserved IDs; actual positive count budget failure. Refuse unsupported graph domain and resource excess explicitly. No ignored edge, missing source, per-row truncation or candidate-only cap test may turn failure into success.
6. **Loads and audit integrity:** alpha0 should return the nominal-force state; nontrivial root/force must use f*x; tilted near-unit axes, unequal forces and signed moment cancellation; a deliberate incorrect squared-ratio or body/world-frame output must fail the checker. Corrupt one returned load word and a prepared/ID association to establish that the audit checks delivered output identity rather than recreating an answer from x. Compare Euclidean force/moment errors, not only their separate largest components.

Expose at least native-success, input/domain refusal, numerical-range failure and resource failure, plus independent offline reference admissible/rejected/unresolved and accuracy pass/fail status. All attempted cases remain counted. Native success is not labeled proved admissible, and no online interval/certificate is required by this recommendation.

## Browser viability and cost boundary

The existing loader verifies exact bundle bytes and each scientific source slice before factory execution, uses a five-module allowlist and a local Uint8Array/DataView Buffer subset, and avoids global Buffer/native prototype changes. Nine adapter control groups define56 assertions for that subset. Normal timed builds already use `fullSymbols=false`; removing a dense symbol tensor cannot be credited as a new speedup.

Historical source pins name **Chrome155.0.8059.80 on darwin arm64**, Nodev24.19.0 and Playwright1.62.1. The controller launches headless `channel:'chrome'`, captures `Browser.getVersion` and `browser.version`, uses a fresh profile and same-origin pinned-source routing; the supervisor verifies listed Chrome components. `runtime.json` explicitly says this is not a complete transitive runtime-resource inventory. These are historical prospective metadata, not a verification of the currently installed browser or a new timing result.

A matched native-load query must start with the same raw current words for every method and include ID validation/canonicalization, native preparation, preflight/index/fallback, coefficients/admission/ordering, solve, required native residual checks, actual four-load materialization and output consumption. A prebuilt CSR, exact reference coefficients, cached y/x, prevalidated admission or loaded final answer cannot be free work. If residual calculation is removed, that is a separately declared change, not inherited query equivalence. The inherited total/phase timers do not yet include four-load materialization and cannot be used as the complete new denominator.

Offline exact-reference generation/audit, artifact encoding/hashing/persistence, browser launch and rendering may be accounted separately from the per-query timer, consistently and explicitly. Keep end-to-end supervision accounting as well. No real-time cadence/deadline guarantee follows from this source audit; cadence and deadline must be stated in the prospective contract rather than inferred from old medians or physics controlDt.

## Exact source/schema inventory

The following pins identify bytes inspected or compared for this memo. A hash is provenance only, not a source-correctness or execution claim. The historical spec includes frozen fixture definitions; no fixture was evaluated or newly selected. Paths are relative to the repository stated above.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-browser-screen-2026-10-16/source/kernel.cjs` | 16676 | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| `research/m31-browser-screen-2026-10-16/source/lean-anchor.cjs` | 14840 | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| `research/m31-browser-screen-2026-10-16/source/anchor-kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `research/m31-browser-screen-2026-10-16/source/reference-excerpt.cjs` | 2731 | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| `research/m31-browser-screen-2026-10-16/source/browser.js` | 43362 | `ba90d2951c678cdbf85cd7d56217d9fd7f4664a58245ba768cd5066f95e9d46e` |
| `research/m31-browser-screen-2026-10-16/source/browser-bundle.js` | 51804 | `61591ede127e562cdbf03c5ac7fd499ad282d6ae10453676b363723fdbc33660` |
| `research/m31-browser-screen-2026-10-16/source/source-bundle.json` | 1024 | `a626b1019128734e0f59ddd06d7574dfbb1e59a3de077d036f7c0c16045baa35` |
| `research/m31-browser-screen-2026-10-16/source/browser.html` | 429 | `e9a6dbae8bf7caaa942bc1e1713d4ab8fda005ae48442f3b9ff2219eb732225c` |
| `research/m31-browser-screen-2026-10-16/source/controller.cjs` | 11291 | `a3c3797012ff820ed62aee4149e1c4e99caacacf13d1aefa56986d35cb5434cd` |
| `research/m31-browser-screen-2026-10-16/source/run.py` | 14328 | `31e54e76a6b3c2b560ab3c698d9dd4942fdfd453aa3c8a5e2639c62ea1878f45` |
| `research/m31-browser-screen-2026-10-16/source/controls.cjs` | 5355 | `bf54381ee7f4dab8fbb19e48ada7e11c0f6d129cec1bcd21e5ce5075fc91f1ba` |
| `research/m31-browser-screen-2026-10-16/source/adapter-controls-spec.json` | 3298 | `da4de67642ef92283cfd7087aac6f57700a64860b16068cfbcd00d4591a833b0` |
| `research/m31-browser-screen-2026-10-16/source/numeric-reference.py` | 39666 | `4b21e84674d0007e23641622aec52724bced4791fcca3c1b97d48189c21f6aeb` |
| `research/m31-browser-screen-2026-10-16/runtime.json` | 6678 | `500a1522833696a7c4fff4bb3eeaf84514304ac101148ca11f56968bfced4460` |
| `research/m31-typed-assembly-2026-10-16/source/kernel.cjs` | 14840 | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| `research/m31-typed-assembly-2026-10-16/source/anchor-kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `research/m31-coupled-cost-2026-10-16/source/kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `research/m31-normalizer-replication-2026-10-17/source/baseline/adapter.cjs` | 2400 | `5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145` |
| `research/m31-normalizer-replication-2026-10-17/source/baseline/pair-prepared.cjs` | 3357 | `e963362c4b095196b5cc0bcc67c1b613f28c4d6a5e5d5e15101a4f847a61ff56` |
| `research/m31-normalizer-replication-2026-10-17/source/baseline/spec.json` | 296772 | `a47b9b920ddbbd14e1838e9c031a0b34dd1820f14959ef1295cef039e7f48d2f` |
| `research/m31-moving-admission-2026-10-17/source/semantic-reference.py` | 39634 | `ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c` |
| `research/m31-current-bound-design-2026-10-16/ADOPTED-DESIGN.md` | 10420 | `702d64e84c3fc12fdc9e85cb59abf4dd00e8df010647e1567a47eed49ee5387c` |
| `research/m31-direct-load-diagnostic-2026-10-17/source/analyze.py` | 24587 | `98f1802b3cf880009998bdb1235f57dadd91cc49c4dbd921731501fb8281cf37` |
| `research/m31-direct-load-diagnostic-2026-10-17/source/config.json` | 1095 | `06faace0212dc10a01510ce8aa591b47a72cfb0833790c0ad1923d1a18ee9e6c` |
| `research/m31-force-ablation-2026-10-16/source/adapter.cjs` | 5814 | `3389613bb855361b5ec41768eafee60bc7c9bb85868697cf391d5689eea60469` |
| `research/m31-ratio-reuse-2026-10-16/source/adapter.cjs` | 4389 | `c6759b7ccc90e0adbc4feb8eb552d1959a988ca33e54ff158d42373be8ecd74e` |
| `outputs/step02c-source/physics.cjs` | 6115 | `0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1` |
| `outputs/step03b-source/wake.js` | 2102 | `19c890c8fa5914ca0ceb55cd3332eaa67c5632883e7f1ebbcf70b258d592c2d1` |
| `outputs/milestone-31-source/grid.cjs` | 898 | `f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302` |
| `outputs/milestone-31-source/wall-filter.cjs` | 1182 | `8273cc40a9530748fe43e9ef0a4d9a995ee152f9968ce2368e61e2f205502512` |
| `outputs/milestone-31-source/geometry.cjs` | 1462 | `e209e492fc523ab3c0c7df62745fb0d3dd7204f35e53309938a19d7895ed3d4f` |
