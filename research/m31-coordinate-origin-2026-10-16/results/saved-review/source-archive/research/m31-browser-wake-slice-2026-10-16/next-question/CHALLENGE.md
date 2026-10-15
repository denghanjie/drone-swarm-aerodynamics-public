# Next question: position representation and local wake arithmetic

Static challenge, 2026-10-16. No implementation or experiment is selected or authorized by this note. Finish the independent saved review and publication of the terminal wake-slice result first. This preparation read existing JSON reports and source text, and verified the primary literature below. It did not decode any raw scientific array, generate a position, calculate a new wake/reference value, import a scientific module, compile a shader, launch a browser, or run a GPU. All prior attempts remain closed.

## Recommendation

Consider one new, prospective **three-arm, two-origin coordinate diagnostic on genuinely new geometry**. Its question is: can a small change in local-coordinate arithmetic, or the additional cost of high/low position storage, restore the unchanged conservative inflow allowance while preserving every policy class? Test the complete selected-receiver term-to-sum component, with raw term attribution, rather than starting a sequence of isolated scalar fixes.

Use one fresh 5,000-source construction and four receivers selected by a frozen index/stratum rule, with all four rotors and all source IDs. Freeze the input generator, seed-release rule, receiver rule, two origins, three implementations, original R oracle, controls, gates, work/output ceilings and stop rules before exposing new values. Do not rerun receivers27/445/4500/988 from the terminal input. A repeated calculation on a translated old input would be an exposed development probe; a new seed and a construction never evaluated before freeze make the proposed diagnostic prospective. It remains a controlled synthetic geometry test, not a Boids-flight test or an independent aerodynamic validation.

The three arms are sufficient for the practical choice; avoid a larger factorial sweep:

| Arm | Position interface and displacement expression | Main contrast |
|---|---|---|
| A | Current absolute f32 positions; `source − (receiver + offset)` | Frozen baseline implementation on the new geometry |
| B | Identical input words to A; `(source − receiver) − offset` | Local-first arithmetic on exactly the same represented inputs |
| C | High/low f32 **positions only**, with the same packed axes, offsets and constants as A/B; form high/low center difference before subtracting offset | Additional coordinate representation plus its reconstruction cost, relative to B |

The signs above match the actual frozen kernel. Changing to `(receiver−source)+offset` without also changing every downstream convention would reverse the model's displacement. No normalization, policy threshold, source strength, profile, fade, receiver law or absolute allowance changes belong in these arms.

## What the terminal result does and does not show

The recorded source identity is4767787487fc7f8c3a8e8189523b1299c9c7f190. The driver result is terminal/failed. R, Q and all16controls passed; all80,000GPU term records qualified and matched policy classes. The reports record388positive terms, no arithmetic-invalid record and complete term coverage. There were two dispatches and zero GPU sum slots. The serial reduction was not run; there is no reduction result to rescue, diagnose or complete under its old budget. Independent saved review was pending when this note was prepared.

At receiver988, rotor3, existing report values are:

| Saved report quantity | Value in m/s |
|---|---:|
| Conservative T−R L1 plus reference allowance | 2.6080175808988906e−5 |
| Frozen epsilonWake | 1.8270441835956964e−5 |
| Q−R L1 | 1.2397087254744332e−5 |
| T−Q L1 | 1.5259289651755273e−5 |
| Signed T−R sum difference | 2.5468264261715474e−5 |

These are copied display values, not newly computed measurements. Exact dyadic coefficients remain authoritative in raw/terms-assessment.json. The signed error also warns against assuming that cancellation alone will make this an acceptable output; the predeclared L1 gate is the reason for failure and must not be replaced by a total-only gate.

R versus Q already separates original numerical inputs from the collectively rounded prepared interface. It does **not** separate positions from axes, offsets or constants. T versus Q collects GPU geometry, norms, dot products, profile/fade arithmetic and compiler effects. Large intermediate discrepancies in the report can identify stages worth examining, but the per-stage maxima need not be from the same term, and they do not prove a causal path to the failed rotor sum. This note has not inspected coordinate magnitudes, lost offset bits or individual binary displacements. The present term record does not contain the full displacement vector or rotor world point. Inferring their exact arithmetic history from down/radial scalars would not be justified.

The source makes the proposed mechanism plausible: `point = rp + arm` followed by `displacement = sp − point` can round the small arm in the absolute world frame before subtraction. Reordering can avoid that particular intermediate. It cannot recover information lost when original positions were already packed to f32. High/low storage addresses that separate loss. Neither mechanism is established by the current reports.

Evidence used: research/m31-browser-wake-slice-2026-10-16/{results/result.json,raw/terms-assessment.json,raw/Q-assessment.json,raw/R-assessment.json,raw/R-counts.json,raw/Q-counts.json,raw/controls-assessment.json,raw/capability.json}; source/wake.wgsl lines256–257 and source/host.cjs lines142–148. The reported backend is Apple/metal-3 under Chrome155.0.8059.40; no cross-device conclusion follows.

## A controlled fresh input that removes translation-construction ambiguity

The coordinator's dyadic construction is preferable to assuming that arbitrary host `p + translation` is exact. Define new positions from a centered integer lattice plus bounded signed-integer jitter, with one common denominator2^20. A concrete proposed family is shape[20,25,10], spacing1/4, jitter numerator bounded by2^13, and centered coordinates. For example each coordinate numerator can be specified by an integer expression using the lattice index and an integer jitter, then scaled by2^−20. This is a specification only; no integers or positions were generated here.

Use canonical origin[0,0,0] and one frozen translation[64,−32,16], with no origin sweep. Prove from the generator's integer bounds that both coordinate numerators after translation fit the53-bit binary64 significand, and that both frames obey the original128m component bound. At execution, save the integer recipe, exact coordinate bytes and exact dyadic translation residual for every coordinate; require residual zero. An implementation that performs an unproved floating addition instead is not entitled to that zero-error claim. A failed construction/admission ends this design without trying another origin.

This choice intentionally creates an informative asymmetry. With canonical coordinates bounded in magnitude below8m and denominator2^20, their integer significands can fit f32 exactly; adding the fixed origin requires more significand bits. Thus the canonical frame is a **deliberately easy position-representation control**, while the translated frame challenges f32 position storage. Axes, generic rotated offsets and constants are still rounded in both. The construction is not evidence that the method handles arbitrary53-bit coordinate values; high/low can be particularly favorable on these short-significand inputs. That limitation must be tested by the separate confirmation design below.

Retain generic nonzero roll/pitch and yaw through a separately frozen attitude generator, with original quaternion and tilt admission unchanged. Four receiver IDs should come from declared lower/interior/upper/edge index strata by a seed-hash rule, not saved inflow rankings or observed term errors. Predeclare substantive nonzero-exposure requirements for the intended active strata; failure to obtain them is an uninformative diagnostic, not permission to replace receivers or regenerate a seed. Expected sparse/zero strata remain visible.

Freeze the seed derivation before revealing the new seed, preferably with an independent post-freeze entropy value. Do not use the historical seed608897. Two origin copies of one fresh geometry are paired transformations, not two independent samples. They share one scientific scene and one source-configuration sample.

Exact input translation does not make the binary64 **calculation** translation invariant: R's own world-point addition may round differently at the two origins. Compute the same unmodified R oracle once per origin; save its cross-origin term/sum differences as diagnostics. Judge each arm against R at the matching origin. Record any R drift explicitly rather than silently adding it to epsilon or declaring translation invariance of the numerical oracle. The coordinate construction removes input-translation error, not all subsequent floating-point error.

## Separate what can be separated, without full-flock reruns

For each origin use these references:

- R: original prepared binary64 geometry/constants and the unchanged independent-I arithmetic.
- Q0: the same original reference on A/B's decoded f32 positions, axes, offsets and constants. A and B share Q0 because their represented inputs are identical. Do not evaluate a redundant new Q merely because the shader's written grouping changes.
- Q1: the same reference on the semantic high+low coordinates of C, with every other decoded field identical to Q0. Preserve exact high/low words and any binary64 reconstruction rounding. Do not reconstruct each absolute coordinate into a single f32 value before subtraction, which would discard the point of the representation.

Q0−R remains total prepared-input error. Q1−Q0 is the effect of **only changing position representation while holding the other represented inputs fixed**, passed through the nonlinear model; it is not a universal, order-independent percentage attribution. T_B−Q0 measures B's actual GPU arithmetic discrepancy, and T_C−Q1 includes C's reconstruction and GPU arithmetic. Compare T_B with T_A on the same bytes; compare Q1 with Q0 and both GPU residuals before attributing a T_C−T_B improvement. Signed telescoping identities are useful bookkeeping; L1 terms do not add as causal percentages.

For the dyadic scene, if the saved high/low encoding reconstructs the original coordinates exactly, Q1−R leaves axes/offsets/constants packing and reference arithmetic effects visible. Do not assume that identity from the design alone: check the saved encodings in the future run. This controlled contrast is sufficient to distinguish the principal representation intervention from the local-first intervention without adding all combinations of rounded/original constants, axes and offsets.

No full5,000-receiver reference is needed: each R/Q pass visits just the four selected receivers with all source IDs. Prepare original axes/offsets once; reuse unchanged attitude data between origins. A/B share packed inputs and Q0, and all three arms share the same per-origin R. The new proposed six cells reserve6×80,000GPU term slots and at most6×80,000selected host reference slots (R,Q0,Q1 at each origin). These are prospective work counts, not computed scientific outputs or runtime predictions. Raw bytes, controls, exact-sum work, process deadlines and partial-failure retention still require a new frozen ledger before any implementation/run authorization.

Existing saved outputs already suffice for the coarse Q−R/T−Q attribution and exact stored-term/reduction arithmetic. They cannot reveal a counterfactual local-first term or new position encoding without new geometry/profile evaluation. Hybrid-reference or host-profile-at-GPU-geometry calculations would be additional scientific work, not a saved-only review. Do not append such passes if the six-cell design fails. Likewise a host `Math.fround` emulator is not an exact emulator of all legal WGSL execution.

## Make the backend intervention observable

WGSL permits reassociation. Merely replacing parentheses or inserting a `let` does not guarantee that the backend evaluates a different operation graph. Add the actual displacement components consumed by the downstream calculation to each future term record, with reached-stage validity, and return the center displacement when its stage is reached. Save the same diagnostics for all arms; do not compare an uninstrumented baseline against an instrumented candidate without acknowledging that difference.

The observations can show whether the candidate implementation produced different local vectors and whether those changes accompany better terms. They cannot prove a universal source-order guarantee. If A/B produce identical vectors, report that the intended intervention had no observable geometric effect on that backend; do not conclude that the mathematical local-first idea was disproved or secretly add another forcing technique.

A separate dispatch that stores center differences and then reads them could impose an observable f32 materialization boundary, but it adds a pass, storage and loads, and changes the computation under study. Host-generated receiver-relative pair data also changes the interface and can scale with receiver×source count. Neither should be a hidden fallback. Defer them unless this first practical architecture decision specifically motivates that cost.

## Accuracy, computation cost and stopping rules

Preserve epsilonWake=1.8270441835956964e−5m/s, the original1e−12 reference allowance, exact policy equality, full validity/finite coverage and the same R oracle. Retain the represented-interface gate for Q0/Q1 against the matching R. If Q0 fails, A/B are already inadequate under that contract and their dependent GPU work may be skipped by the frozen plan; Q1/C remain an independent predeclared arm. That outcome identifies a representation barrier but supplies no observed A/B arithmetic contrast for the skipped cell. Never manufacture that missing contrast or quietly waive the Q gate to complete a table. For each arm/origin retain exact per-rotor L1 term error against R. Only a qualifying cell may spend its newly reserved serial reduction on the same materialized GPU terms. The final gate remains `L1(T−R) + |S−exactSum(T)| + allowance <= epsilonWake`. This is a new complete component test on fresh inputs, not execution of the old omitted reduction. Do not add roots or a force-error composition claim.

A numerically failed cell is an outcome in this predeclared comparison, so it need not suppress independent cells already frozen in the same campaign. API/device loss, malformed input, exceeded caps or an invalid shared premise stop the affected dependent work; no retry/replacement cell is permitted. Freeze these distinctions before launch, including which independent cells may finish after a numeric failure. Retain all raw failures.

B adds no position words and can reuse the center difference already needed for the neighbor check, but actual instruction counts are compiler dependent. C adds three position-residual floats per source before layout padding, plus residual loads and difference/combine arithmetic. Record preparation operations, uploaded/resident bytes, dispatches, pair visits, stored-term reads and compiler/backend metadata for all arms. These establish a concrete resource tradeoff; they do not establish elapsed-time speedup. The existing diagnostic readback and pair matrix are not a production throughput architecture.

Predeclare the practical decision: prefer B if it passes every valid cell's complete term-plus-sum gate and corrects a baseline failure without extra input storage. Consider C only if B is inadequate and C passes with the explicitly accepted bandwidth/preparation cost. If all arms pass or A/B are indistinguishable, do not claim that the mechanism explains the historical failure. If C also fails, stop the position-only design and report that it did not deliver the required component; do not launch a new microtest for each remaining constant, axis or fade. A smaller average error with some failed rotors is not acceptance.

A candidate that survives this diagnostic earns one frozen confirmatory comparison, not performance or flight claims. For a genuine accuracy–runtime tradeoff, a later authorized measurement must compare the chosen complete implementation against the current serious CPU/GPU baseline on the same required work, including preparation/transfers as appropriate and excluding diagnostic-only readbacks symmetrically. No favorable runtime is predicted from source operation counts or another paper's GPU results.

## Separate fresh confirmation

After the diagnostic decision, freeze exactly one candidate, its representation, gates, scope and seed-release rule before exposing a second independently generated scene. Use a modest predeclared cohort, for example eight receivers with all5,000sources, and the same two fixed origins; compare only the chosen candidate and A, without retuning. General binary64 coordinate values or a different frozen denominator must be included so the confirmation does not merely repeat the f32-friendly canonical lattice. Include a predeclared change in geometric coverage, such as density/tilt strata, with an honest boundary/domain policy and no outcome-conditioned rejection or receiver replacement.

Prove or exactly account for translation construction for this broader family too. A power-of-two translation is not automatically exact for arbitrary53-bit inputs. The smallest rigorous options are to generate bounded dyadic numerator families whose exact translated values still fit53bits, or to retain an exact-rational position representation and certify conversion separately. Choose one before freezing; do not add an unbudgeted model-derived allowance afterward.

Origins within a scene remain dependent copies; two seeds remain a small synthetic confirmation, not a population guarantee. A changed seed on the same lattice tests fresh arithmetic instances but is weaker than confirmation spanning new geometry. A failed confirmation rejects the selected candidate without reopening the diagnostic or selecting the next best arm. Successful confirmation should lead to one integrated full-workload qualification/resource comparison, rather than a string of further favorable pair probes.

## Alternatives rejected or deferred

| Alternative | Why it is not the next recommendation |
|---|---|
| Rerun the exposed four receivers, or just receiver988/rotor3 | Useful development replay only; cannot be called fresh confirmation and risks tuning to one failure. The terminal budget remains closed. |
| Run the skipped old serial reduction | Cannot repair the already failed conservative term gate; it was not authorized after that failure. |
| Loosen epsilon/classes or accept signed cancellation | Changes the question after exposure and hides term error. |
| A full2×2 ordering/encoding factorial or many origins/seeds | Adds a high/low world-point variant with little practical value at this stage; the nested A/B/C contrasts plus Q0/Q1 answer the immediate architecture choice. |
| Blanket high/low arithmetic, f64 emulation, normalization or profile/FMA changes | Changes several sources of error and cost together; neither the reports nor the literature identifies all as necessary. WGSL fma is not a strict IEEE fused-operation guarantee. |
| Per-receiver host-relative uploads or a forced storage prepass | May be accurate, but can add receiver×source preparation/traffic or a new dispatch; a different architecture requiring its own resource case. |
| Cross-device sweep, grid/pruning, coupled trajectories, timing sweep now | Enlarges scope before the component's accuracy–representation choice is settled. |

## Verified primary-source basis and attribution limits

1. **David Goldberg (1991), “What Every Computer Scientist Should Know About Floating-Point Arithmetic,” ACM Computing Surveys23(1),3–48, DOI10.1145/103162.103163.** Read the “Cancellation” section in the [Oracle edited reprint](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html). It distinguishes newly rounded arithmetic from error already present in operands: even exact subtraction can expose earlier error. That supports distinguishing world-point rounding from coordinate quantization; it does not prove the observed wake failure has this cause. No quotation or numeric example from the paper is used as our evidence.

2. **Evghenii Gaburov, Stefan Harfst and Simon Portegies Zwart (2009), “SAPPORO: A way to turn your graphics cards into a GRAPE-6,” accepted New Astronomy manuscript, [arXiv0902.4463v2](https://arxiv.org/abs/0902.4463v2), [full PDF](https://arxiv.org/pdf/0902.4463v2), related DOI10.1016/j.newast.2009.03.002.** Verified authors/version and read §§2.2–2.3, especially printed pp.3–6 and Eq.(3), plus the accuracy discussion§3.2. Their CUDA gravitational solver stores positions as high/low single-precision pairs and forms separation from high and low differences, then retains single precision for the remaining force work. This is direct precedent for selective coordinate precision. Their GPU generation, gravitational model, integration metrics and performance do not predict this Apple/WebGPU wake kernel. The DOI page failed to open, so the version actually read is identified; no broad novelty claim follows.

3. **W3C WGSL Candidate Recommendation Draft,21September2026**, [fixed edition](https://www.w3.org/TR/2026/CRD-WGSL-20260921/), §§15.7.4–15.7.6 and17.5.32. Read the reassociation/fusion rules and fma definition directly. Written grouping is not a mandatory operation graph; fma may be implemented as separate multiply/add. CUDA or error-free-transformation assumptions therefore cannot simply be imported into WGSL. Qualification remains about observed bounded outputs on the recorded backend.

4. **Nathan Whitehead and Alex Fit-Florea, NVIDIA, “Floating Point and IEEE754 Compliance for NVIDIA GPUs.”** Read the [archived CUDA11.4.0 edition,29June2021](https://docs.nvidia.com/cuda/archive/11.4.0/floating-point/index.html), §§2.2–2.3,3.1–3.2 and the author attribution. Its dot-product comparison illustrates that implementation choices can change results even under IEEE754 operations. It supports recording the chosen algorithm; its CUDA controls/accuracy guarantees are not claims about WGSL or Apple Metal.

The existing project ledgers already establish the wake-model and receiver assumptions. This arithmetic proposal adds no physical validation and makes no claim of a new high/low technique. No benchmark, source-code reproduction of the cited GPU work or exhaustive literature/novelty search was performed.
