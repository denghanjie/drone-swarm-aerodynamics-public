# Static proposal: one complete ordinary-f32 load query

**Unadopted specification; no implementation or execution authorization.** This note identifies a possible application contract and its remaining blockers. It is separate from the completed coordinate-origin campaign and does not reopen its failed gates, skipped cells or confirmation. Only source/report text was inspected. No model import, scientific binary decoding, geometry generation, field/root evaluation, shader compilation, browser, checker or benchmark ran.

Repository inspected: `repository root`. Paths below are relative to that repository. Source changes, a new immutable manifest and fresh launch identities would require a separate adoption decision. No old seed, lock, job, terminal or budget is carried forward.

## 1. Production meaning and proposed admissions

The query accepts N original binary64 17-state records, with N between 2 and 5,000. The layout is position 0–2, velocity 3–5, quaternion xyzw 6–9, body angular velocity 10–12, and **actual lagged nominal motor thrusts in newtons at 13–16**. Commands are not these states. Velocity and angular velocity remain part of original-state provenance but are unused by this quasi-static wake/load query.

`outputs/step02c-source/physics.cjs:16` clamps actuator commands to `[0, ratio*m*g/4]`; M28 calls control with ratio 2.25. The motor derivative is `(command-actual)/.04`. Neither the generic derivative/integrator nor M28's finite-state safety check imposes a universal admission/max check on supplied actual motor states. Thus `[0, f_max]`, where `f_max=2.25*.027*9.81/4 N`, is a **proposed explicit query admission motivated by the command envelope**, not an already enforced production invariant. Imported/RK-stage states must independently pass it. No negative-value clipping, replacement by hover thrust, or clipping to the old GPU receiver's `[.01,.1] N` range is permitted.

M28's loop (`outputs/milestone-28-source/sim.cjs:29–44`) computes a flow field on its flow cadence, then passes that field into aerodynamic integration. The receiver law consumes the changing actual motor states within RK stages. A static full-query result does not qualify the held-flow schedule, RK trajectories, stability, contact avoidance or real-time closed-loop operation. M31's historical airflow-off replay is not evidence for that consumer.

Proposed geometric admission preserves the previously explicit host envelope:

- Exactly 17 finite components per state; position components within ±128 m.
- Original quaternion norm differs from one by at most `1e-10`, with no normalization or repair. Produce axes, all four offsets and the world rotation matrix once under a frozen original binary64 rotation convention.
- Original and decoded packed axes are finite with component magnitude at most 1.01; every rotated rotor offset is finite with component magnitude at most .1 m. Record axis norm drift and global tilt margin separately for R and Q. Original axis.z must be at least the original `cos(20°)`; decoded axis.z must be at least its decoded packed threshold. Passing one does not waive the other. Packed axes/matrices are not renormalized or orthogonalized.
- Validate finite raw float words, pads, length, index bounds and frozen constant identities before interpretation/use. Proposed packed world-matrix entries are bounded by 1.01 and saved as three padded rows. Axes, offsets and world matrix must derive from the same original quaternion; their independent packing can introduce rounding inconsistency, which remains part of the interface error.
- Source-center eligibility remains strict distance `<3 m`; primitive A remains `sourcePosition - (receiverPosition + rotatedOffset)`. No recentering, residual coordinates, B/C fallback, nearest-source truncation or changed source ordering.
- Preserve domain order: self/outside; downstream `<=0`; downstream `>=2.5 m`; near region `downstream<2.5D`, which is invalid if radial distance `<.15 m` and otherwise a valid skip; then radial cutoff at three half-widths; then nonnegative axis projection. Near-domain invalidity cannot be hidden by radial/projection pruning. Here `D=2*sqrt(2)*.028 m` and half-width is `.07668*(downstream/D+5.817)*D`.

The prepared-term source additionally guards center components ≤257 m, center norm ≤512 m, rotor displacement components ≤258 m, absolute downstream ≤1024 m, radial distance ≤2048 m, and individual finite nonnegative term ≤128 m/s. These are numerical guard limits, not a guarantee that a sum fits a receiver limit. Propose a separately explicit finite rotor-inflow admission `[0,128] m/s` for each R, Q and actual GPU completed sum. A sum outside it is a terminal case failure, never truncation. This upper bound still needs an application rationale; the old reducer's `1e6` allowance is not that rationale.

The source wake amplitude stays the model's prescribed isolated-hover amplitude `sqrt(m*g/(8*rho*area))`, independent of source motors. Making wake amplitude motor-dependent is a different physical model. Constants retained include mass .027 kg, gravity 9.81, arm .028 m, kf `3.16e-10`, km `7.94e-12`, density 1.225, rotor radius .023 m, wake parameters `(10.11,.07668,-5.817)`, downstream fade/cutoff 2/2.5 m, radial fade/cutoff 2/3 half-widths and tilt limit 20°.

## 2. Complete observable and actual consumer

Use `sum-rotor`. Rotor signs/order are `(x,y,spin)=(a,a,+1),(-a,a,-1),(-a,-a,+1),(a,-a,-1)`. If effective forces are e0…e3 and nominal forces f0…f3, return:

- All four inflows and all four effective rotor forces; body thrust `T=e0+e1+e2+e3`.
- Body moment `[a*(e0+e1-e2-e3), a*(-e0+e1+e2-e3), (km/kf)*(f0-f1+f2-f3)]`.
- Body force `[0,0,T]`, world force `rotation*[0,0,T]`, and world moment `rotation*momentBody`.
- Nominal T/body moments/world force and effective-minus-nominal T/body moments/world force.

`outputs/milestone-28-source/aero.cjs:18` substitutes effective thrusts into the rigid-body derivative, then restores nominal yaw torque for `sum-rotor`; the production consumer therefore uses world force and body moments. World moment is an additional diagnostic/output, not the angular-acceleration operand. Gravity, gyroscopic torque, actuator lag and integration remain outside the query. The returned body-force x/y are exact semantic zeros, not omitted records.

Freeze grouping for load assembly. The algebra above defines meaning but does not promise identical rounding between the production sequential wrench, independent-reference explicit algebra and a GPU compiler. Save actual assembled outputs. All N outputs must be covered; a few selected receivers or aggregate maxima cannot substitute for them.

## 3. Receiver zero and tiny-positive semantics

Independent reference `research/m31-source-omission-2026-10-16/source/independent.cjs:261` rejects nonfinite/negative nominal or inflow. Nominal zero returns force zero and x=0, with alpha/residual not applicable. Positive nominal with zero inflow returns nominal force and x=1 exactly, with zero residual. For positive inputs it independently bisects `x^3+alpha*x-1=0`, where `alpha=U/sqrt(f/(2*rho*area))`, on `[0,min(1,1/alpha)]`, up to 96 iterations. Its saved numerical brackets are not a directed-rounding interval proof.

The existing GPU receiver is insufficient: `research/m31-browser-receiver-2026-10-16/source/receiver.wgsl:65` admits U `[0,128]`, nominal `[.01,.1]` and supplied vi `[1,10]`, lacks a nominal-zero branch and was qualified for fixed hover words. It cannot be relabeled as a general-motor pass.

A possible new GPU root formulation, pending critique and qualification, computes `vi=sqrt(f/(2*rho*area))` from actual packed nominal rather than accepting a stale uploaded vi. Handle zero nominal before division; handle zero U next. If `U<=vi`, Newton uses `x^3+(U/vi)*x-1` starting at one. Otherwise use `r=vi/U` and `r*x^3+x-r`, starting at r. The bounded coefficient avoids constructing a very large U/vi. Twelve iterations would be a new fixed iteration cap, not inherited accuracy evidence. Do not silently clamp an out-of-range iterate or accept exhaustion as a certificate.

Full `[0,f_max]` means the proposal must explicitly confront original positive values rounding to packed zero, packed subnormals, permitted device flushing, and effective-force/product underflow. Preserve separate flags for original exact zero, packed exact zero, packed subnormal input, arithmetic result rounded/flushed to zero, and numerical failure. A packed-zero identity does not establish an original-zero identity. Save original and packed nominal words, actual vi, branch/coefficient, x, force, residual, final step, iterations and validity. Decide before implementation whether the target contract permits particular flush behavior under final absolute error gates, requires a raw-word fallback with specified semantics, or narrows the positive admission. Narrowing must be explicit; source inspection establishes none of these choices.

Minimum controls include exact zero nominal/zero inflow separately and together; positive normal nominal with zero inflow; asymmetric motors; the maximum and adjacent representable values; both sides of `U=vi`; smallest positive normal/subnormal packed nominal; original positives below the f32 rounding threshold; and output-underflow cases. Malformed, negative, nonfinite and sum-limit inputs require rejection evidence. These are fixed controls to be specified before observation, not invitations to search for friendly inputs.

For every completed GPU root, independently recompute a binary64 reference solution using the saved actual GPU U and represented intended nominal/rho/area. This requires only 4N additional scalar reference solves, not another field pass. It tests receiver error at its real handoff, including vi construction. Check finite/range `0<=x<=1`, `0<=effective<=nominal`, branch identities, independently computed polynomial residual, root/reference force difference and numerical-bracket consistency. Save this handoff witness. Root residual should use the scaled equation for the high-U branch as well as a well-defined original-equation diagnostic where finite. It must not be read as a universal force certificate without the stated conversion/gates. At zero nominal, inapplicable fields carry validity bits, not fabricated valid zero residuals.

## 4. R/Q/GPU comparison and compact policy retention

R uses original binary64 prepared geometry, constants and actual motor states. Q uses the exact decoded packed input interface, with binary64 evaluation of the same policy/profile/root/load meaning. Q must consume saved decoded axes, offsets and world matrices directly; reconstructing them from a quaternion would silently change its interface. GPU uses ordinary f32 primitive A, one invocation per receiver, ascending source IDs and four rotor accumulators. Visiting four rotors per source preserves each rotor's ascending-source accumulation order. Complete root/load assembly follows the actual four accumulated inflows. No cross-receiver atomics or unspecified parallel reduction tree are needed in this proposed architecture.

Retain R/Q ordinary and same-pass compensated inflows, actual GPU inflows, complete loads and root diagnostics. A future wrapper must expose same-pass root solutions rather than call `receiverSolution` for diagnostics and then `loads` to solve again unnoticed. The current independent helper's successful receiver callback can provide sums/terms; its failure callback path needs additional reviewed instrumentation because a near-domain throw occurs before a completed receiver callback. Uncomputed array zeros are not evidence.

One proposed per-rotor terminal symbol uses four bits:

| Symbol | Meaning |
|---:|---|
| 0 | Unwritten/unreached |
| 1 | Valid policy 0: self or outside center radius; identity distinguishes self |
| 2, 3 | Valid policy 1 or 2: nonpositive downstream or downstream cutoff |
| 4 | Policy 3: invalid near-domain |
| 5, 6, 7 | Valid policies 4, 5, 6: near skip, radial cutoff, zero projection |
| 8 | Policy 7, finite positive profile term |
| 9 | Policy 7, finite numerically zero profile term |
| 10 | Malformed input/layout |
| 11 | Arithmetic invalid |
| 12–15 | Reserved; any occurrence fails schema admission |

R and Q store four nibbles in one uint16 word per ordered receiver/source pair. GPU stores one symbol in each byte of a u32 word, with every byte's high nibble zero. Index is `receiver*N+source`; rotor position is fixed. Initialize policy buffers to unwritten. A successful query must replace all N² words and all 4N² rotor symbols, including self/outside zeros. Preserve raw GPU words, not only their host-compacted form. This is full **terminal policy/validity** retention; it intentionally does not preserve the old per-intermediate numerical validity masks or geometric values. First-failure records carry stage/indices and partial completion. A failed invocation remains incomplete; unvisited slots cannot count as zero support. Reference/GPU traversal differences must not be disguised as identical failure prefixes.

Require complete R/Q/GPU policy-class agreement as a separately frozen interface/domain gate. Report positive versus numerically-zero status differences explicitly; decide their acceptance before data. Global valid-query tilt makes zero projection unlikely/unreachable under ideal unit geometry, but that does not justify removing the state from the schema or controls.

**No full-term raw arrays are retained, so there is no L1 certificate.** In particular, no conservative `sum |GPUterm-Rterm|`, no exact sum of actual GPU terms, no standalone GPU reduction-error certificate, and no term/profile-versus-reduction attribution can be claimed. Compensated R/Q sums do not restore missing GPU terms. Output agreement can hide cancelling signed term errors. The admissible evidence is combined complete field-output error, complete receiver/load error and policy/validity coverage. A saved-only reviewer can check these differences and root/load identities but cannot independently replay every discarded profile value.

Application gates remain unresolved: rotor-force, T, body/world force and moment bounds need a declared use-case rationale, plus an absolute-zero convention and root gates. Neither old `1e-7 N` fixed-hover gates, binary64 equivalence tolerances nor source-omission budgets automatically become this contract. Do not choose thresholds after looking at the fresh results.

## 5. Fixed fresh input families: specifications only

Propose four cases, chosen before any outputs, with no search, retries, substitution or generation in this task:

| Family | N and scaffold | Purpose |
|---|---|---|
| Paired columns | 50: 5×5×2 | General coordinates, axes within 3° of vertical, two-height direct exposure and upper zero strata |
| Tilted layers | 500: 10×10×5 | Common column axis tilted 12°, individual axes within 2° of it; general yaw |
| Dense volume | 5,000: 20×25×10 | All-receiver scale, many eligible sources, common axis tilted 8° with individual perturbations ≤3° |
| Sparse pairs at broad coordinates | 5,000: 50×50×2 | Widely separated column pairs, axes within 3° of vertical, large absolute coordinates, many policy-zero pairs and known exposed partners |

For the first three, scaffold spacings are `.731,.763,.611 m` in an orthonormal frame; fourth-family horizontal spacings are `3.211 m`, vertical spacing `.611 m`, with a fixed 17° horizontal frame rotation. Center each scaffold and add a fixed non-f32-friendly origin such as `[.123456789,-.234567891,1.345678912] m`; add bounded general binary64 per-component jitter ≤.0007 m. These are new geometries, not old scenes translated or reconstructed by subtracting a previous translation. The broad-coordinate family fits the ±128 m box by a static envelope, subject to the same actual input admission.

Freeze a new namespace, deterministic hash-to-53-bit-fraction recipe, per-family key, state-index permutation, attitude construction and exact arithmetic convention before generating anything. No old case seed is reused. A predeclared input audit can require a high fraction (e.g. 99%) of original coordinate components differ from their f32 representations; failure ends the case without redraw. This is an input property, not output screening. General quaternions and motor values must similarly not be deliberately snapped to binary32-friendly values.

The positive-exposure construction is geometric: each non-top row has the next member of its own column above it, at approximately .611 m. Conservative design inequalities for that designated source at all four receiver rotors are center distance below 2 m, downstream within [.5,.8] m, radial distance below .12 m, and axis dot above .9. These place it strictly inside positive support and away from downstream/radial fades. Prove the inequalities from the frozen frame/jitter/attitude envelopes before generation, then independently check them as input/domain audits; they are not selections based on computed loads. The ≥.61 m inter-vehicle spacing also leaves a conservative gap from the invalid near cylinder after rotor-offset allowance. Do not claim these static sketches are already a numerical proof for the final generator.

Designated non-top rows number 25, 400, 4,500 and 2,500 respectively. An adopted exposure gate can require all four R inflows on every designated row to be strictly positive, plus a separately justified predeclared lower bound if material exposure is required. Missing exposure fails terminally; do not redraw. Top rows and isolated/outside pairs supply valid zero strata; finite clouds need not make every receiver positive. Assign normal positive motors to most designated rows so wake exposure changes a nonzero load.

Motor assignments are output-independent and unequal. A core pattern proportional to `(.13,.37,.61,.89)*f_max`, with fixed permutations and bounded general scales, produces nonzero nominal roll/pitch/yaw; include near-upper values and explicit zero rotors. A separate fixed edge schedule includes binary64 positive values that pack to zero, the smallest f32 subnormal/normal, values straddling the subnormal transition and the upper boundary. Record which cases are intended application observations versus numerical controls. These inputs test nominal yaw preservation; they must never be converted into equal hover motors. Edge cases remain in the evidence if they fail. The full continuous motor range is not empirically proven by a finite corpus.

## 6. Static resource ledger at N=5,000

Use one case resident at a time. The following is an explicit **proposed** layout, not an implemented allocation:

| Object | Bytes per N / formula | Bytes at 5,000 |
|---|---:|---:|
| Packed nodes: position xyz, axis xyz, two pads | 32N | 160,000 |
| Four packed world offsets, four padded vec3 | 64N | 320,000 |
| Four packed nominal motors | 16N | 80,000 |
| Packed world matrix, three padded rows | 48N | 240,000 |
| Frozen field/root/load constants and dimensions | 128 | 128 |
| GPU policy | 4N² | 100,000,000 |
| GPU all-receiver output | 512N | 2,560,000 |
| GPU policy readback copy | 4N² | 100,000,000 |
| GPU output readback copy | 512N | 2,560,000 |
| R policy retained on host | 2N² | 50,000,000 |
| Q policy retained on host | 2N² | 50,000,000 |
| Original 17-state binary64 input | 136N | 680,000 |
| Original prepared interface, binary64 | 320N | 1,600,000 |
| Decoded packed interface, binary64 | 320N | 1,600,000 |
| R and Q complete reference output | 2×640N | 6,400,000 |
| GPU-input scalar-root reference witness | 224N | 1,120,000 |

The 512-byte GPU output has 128 u32 words: 8 header/status/completion words; four each of U, nominal, vi, x and effective force (20 float words); eight diagnostic words per root (32); 24 load float words; four positive-term counters; and 40 reserved-zero words. The 24 load values are T, body moment3, world force3, world moment3, nominal T, nominal body moment3, nominal world force3, delta T, delta body moment3 and delta world force3. Body force is completely defined by `[0,0,T]`. Header and root field masks govern every payload; invalid missing values cannot masquerade as valid numeric zeros.

Each 640-byte R/Q record comprises 16 u32 header words (64 B), 64 binary64 values (512 B), eight u32 root iteration/status words (32 B), and 32 reserved bytes. Its 64 doubles are ordinary U4, compensated U4, nominal4, vi4, x4, effective4, alpha4, residual4, brackets8 and the same loads24. The 224-byte handoff witness has a 32-byte header and four 48-byte root records: x/thrust/lower/upper/residual as binary64 plus iteration/status u32. Retain actual GPU input U/nominal alongside it via the GPU output record. Root-zero null diagnostics are represented by validity bits. No uploaded vi array is needed because the proposed kernel computes vi; if this choice changes, amend the byte ledger.

Raw GPU buffer residency for the listed inputs, policy, output and both readbacks is **205,920,128 B**; reserving 1 MiB for all additional control/uniform/readback buffers gives **206,968,704 B**. A proposed 208 MiB raw-buffer cap leaves a small explicit reserve; browser/driver/compiler/object overhead is separate and unknown. Do not infer a global GPU-memory guarantee from this arithmetic. Each allocation/binding must satisfy the actual new device's limits.

The saved old capability report (`research/m31-coordinate-origin-2026-10-16/raw/capability.json`) records an actual default device binding cap 134,217,728 B and buffer cap 268,435,456 B, while adapter maxima are much larger. The 100,000,000-byte policy binding fits that observed default, but this does not admit a future device. Require fresh capability/feature/fallback admission and check every binding/storage count, per-stage resource limit, workgroup size, dispatch count, total buffer cap and u32 index multiplication before launch. R/Q uint16 files are host encodings and do not imply GPU native uint16 storage support. At workgroup size 64, 5,000 receivers need 79 workgroups; each live invocation still executes up to 5,000 source iterations and 20,000 rotor visits. Buffer fit does not establish browser watchdog or latency feasibility.

For the proposed retained binary layouts, one case occupies `8N²+2952N` B plus constants/headers/controls: **214,760,000 B** at 5,000. The four proposed cases total **433,163,600 B** before those extras. One additional failed maximum-size case adds 214,760,000 B. A proposed 768 MiB retained-corpus ceiling can contain these plus at most 64 MiB of controls/logs/metadata, but is not an execution budget or permission. Duplicate staging copies must count too. Store typed numeric buffers and stream per-receiver temporary reference terms; do not keep 4N² float64 term arrays or unbounded JS object records. The independent callback's temporary 4N terms is only 160,000 B at 5,000 if released each receiver. Account possible mapped-readback plus retained-copy overlap explicitly; an additional 100 MB host copy is easy to overlook. Host/browser memory overhead remains unmeasured and needs its own stop cap.

## 7. Feasibility, timing and physics remain distinct

Static arithmetic establishes that this compact design is plausible under the **saved** per-buffer limits, not that it runs. Each maximum case still entails 25 million ordered pair slots and up to 100 million rotor visits per R, Q and GPU field pass, plus 20,000 roots per path and 20,000 handoff reference roots. Any reference re-evaluation, failure instrumentation or control repetition must have a new explicit work reservation; none is borrowed from a previous terminal budget.

A feasibility run, if later adopted, must account for original admission/rotation, all offsets, packing/motors, allocations, upload, field accumulation, roots, body/world assembly, synchronization/readback and caller-owned outputs. Separate cold compile/setup, reused allocation lifetimes, evidence persistence and per-query work. Accuracy R is not automatically the appropriate optimized CPU timing comparator. No timing or physical accuracy benefit follows from a valid load-output comparison. The physical wake model, its fixed source strength and near-domain exclusions remain assumptions.

Remaining adoption blockers are justified complete-observable gates and inflow bound; an explicit subnormal/flush policy or honestly narrowed motor scope; frozen input/generator/exposure/control specifications; a reviewed same-pass R/Q wrapper and compact schema; device/resource/host-memory/closure caps; and a newly authorized immutable invocation. Until then this is a static contract sketch only.

## Source pins and evidence scope

- Independent reference: `research/m31-source-omission-2026-10-16/source/independent.cjs`, SHA-256 `da857f37129c6d3fc87fe223efd2b37b140fbf11417c1f1bb92331d5cfa53cec`.
- Production aerodynamic consumer: `outputs/milestone-28-source/aero.cjs`, SHA-256 `710b0a8f0df62208e3385ac9b8288240b379fe9248a1a645251a77c533f24a62`.
- Existing primitive-A coordinate source: `research/m31-coordinate-origin-2026-10-16/source/coordinate.wgsl`, SHA-256 `c6916c379806aea76d224ba223a16a4ba85729b130301dc0672b31f0e11a94ad`.
- Existing limited receiver: `research/m31-browser-receiver-2026-10-16/source/receiver.wgsl`, SHA-256 `dc64e23b3905d635f0d1de4d56233c2380455e89c2f50ee5a59c67baca6f1555`.
- Original/packed preparation: `research/m31-browser-wake-slice-2026-10-16/source/host.cjs:50–116`.
- Mechanics/state semantics: `outputs/step02c-source/physics.cjs:15–19`; aero-enabled scheduling/consumer: `outputs/milestone-28-source/sim.cjs:29–44`.

No source or public-worktree file was changed while preparing this note.
