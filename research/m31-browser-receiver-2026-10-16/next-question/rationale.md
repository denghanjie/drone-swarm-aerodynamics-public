# Next browser question: can the GPU preserve the wake calculation?

2026-10-16. Static recommendation only. No scientific computation, source-module import, shader compilation, browser launch, GPU call, benchmark or new agent was used to prepare this note. No source repository was edited. All earlier campaign and review budgets remain closed; R8 still has `benchmarkPermission:false`.

## Recommendation

After the receiver result receives its independent saved-data review, consider **one wake-only diagnostic on four receiving drones, with every source in the exposed 5,000-drone input**. Save each source's contribution before adding anything. Test geometry and branch decisions first; then compare two specified addition orders on exactly those saved contributions. Do not yet add a grid, pruning, a controller, motion or timing comparisons.

The four receivers would be deliberately selected from existing saved results to cover strong inflow, many contributions, weak inflow and unequal rotor inflows. Their IDs must be resolved and frozen before the new scientific attempt. This is a small stress test using exposed data, not an independent sample and not a full 5,000-receiver test. The companion candidate protocol explains the input interface, comparisons and stop rules.

## Why this is the next useful question

The simulation has three different arithmetic jobs. First it finds the position of each receiving rotor relative to each source. Then it decides whether that source counts and calculates its contribution. Finally it adds the contributions and converts the resulting inflow into thrust. A failure in any one of those jobs can change the answer.

The current receiver experiment addresses only the last conversion. The coordinator reports a preliminary sole-run result at source checkpoint `4f2ead3`: all 24,032 valid roots met the new driver gates and all five invalid controls returned the expected result; maximum thrust difference was about 8.56e-9 N. The older 1e-12 N comparison failed for 24,022 valid records. Independent saved review is pending at the time of this note. These are reported results, not observations reproduced here. Most positive records reached the twelve-update cap. The retained endpoint metadata does not reveal intermediate iterates, oscillation, exact stagnation or speed.

Even a reviewed receiver pass would not answer the next question. Rounding a position can move a source across a cutoff. Rounding an axis can change a projection. A norm computed in WGSL need not behave exactly like JavaScript `Math.hypot`. Adding many approximate terms introduces a further error. The receiver-only inputs were already saved CPU inflows, so none of these effects was exercised.

There is already useful adverse evidence against more small CPU changes. The completed zero-screen study found exact output preservation on its valid recorded inputs, but both E/Z and L/E missed their predeclared usefulness criteria at both 1,000 and 5,000 drones. Avoiding about half of one kind of radial norm was not a comparable runtime gain. Earlier DOT support/reuse changes also had mixed gains over its lean implementation. Repeating those campaigns or comparing a GPU against an intentionally weak CPU baseline would not answer the accuracy question.

The full-flock reference study established finite numerical agreement on twelve exposed static poses: 112,000 rotor evaluations and 28,000 vehicle evaluations. It did not establish physical accuracy, coupled-flight accuracy or execution speed. The later zero-screen evidence retains complete classifications and summed inflows, but not every successful source contribution. A new pair-to-term diagnostic therefore requires a small, honestly counted new reference calculation. It must not be described as merely rereading old answers.

## Make the component boundary explicit

For this first wake test, compute source axes and receiver rotor offsets from the original saved quaternions on the host, using the frozen independent binary64 geometry. Upload the resulting positions, axes and offsets as explicitly recorded f32 values. The GPU then calculates rotor world points, relative vectors, downstream distances, radial distances, projection, support decisions and wake terms.

This does leave quaternion rotation and a fully GPU-resident pose pipeline untested. That is a useful, honest boundary. Simply rounding quaternion components and retaining the original 1e-10 unit-norm admission rule is not generally compatible. Silently loosening that rule or renormalizing would change the experiment. The proposed component instead has a declared approximate-axis interface; it records axis-length defects and compares its results against the original geometry. It must never be advertised as passing the original quaternion API.

The reference comparisons answer separate questions:

1. Original versus packed inputs: what changed when the same data were stored as f32?
2. Packed-input binary64 versus returned GPU geometry: what changed during geometric arithmetic and branch decisions?
3. Independent evaluation at returned geometry versus saved GPU terms: what changed in the profile, fades, projection and multiplication?
4. Host addition of the saved GPU terms versus GPU addition: what changed when adding exactly the same values?

The last comparison needs no second wake calculation. An ascending-source sum and a fixed 64-lane addition graph both read the same term buffer. Neither gets different neighbors or recomputed terms. A numerically acceptable tree would still be only a candidate for later performance work; this diagnostic cannot establish that it is faster.

## Cutoffs need a separate answer

The existing fixtures put some positions only 1e-12 m apart around a threshold. Different original values can become the same f32 value. No shader can recover a distinction that was lost before upload. Preserve this as a representation limit; do not move a cutoff until the outputs look right.

A small control panel should therefore test the strict and non-strict comparisons on exact packed decision scalars. The actual receiver/source test separately reveals whether computing those scalars changes the decision. A branch mismatch near a boundary is not excused by a small force difference. In particular, a represented near-wake violation must not be turned into a zero contribution.

Projection deserves another distinction. If both unit axes stay within 20 degrees of vertical, their separation is at most 40 degrees, so their dot product is positive. The zero/negative projection branch is a useful standalone arithmetic control, but it is not a reachable valid pair in that declared tilt domain. It cannot be presented as extra physical coverage.

## What success and failure would mean

Success would support a narrow statement: this specified browser/backend calculated this component on these exposed inputs within a predeclared numerical allowance. The allowance should be expressed in inflow units and linked analytically to an additional rotor-thrust error allocation. The older binary64 tolerances remain visible, and a new f32 allowance is an engineering choice, not a measured flight tolerance.

If packing alone causes a domain failure or spends the whole allowance, stop before blaming the shader. If geometric branches disagree, retain the witness and stop dependent wake qualification. If terms are acceptable but the parallel addition fails, reject that addition graph. If both arithmetic paths pass, stop there with the diagnostic result; do not turn the same run into a speed campaign. No failure justifies a retry, a larger cap, new easier receivers or tuning exposed results.

This component cannot validate the aerodynamic model. Bauersfeld et al. provide a mean far-field, near-hover flow model; they do not supply this 27 g vehicle's complete receiver law or validate arbitrary overlapping wakes. Kiran et al. show why actuation and offset receiver measurements matter. Gielis et al. show that aggregation itself needs evidence. Numerical precision cannot repair near-field omissions, unsteady wakes, walls/ground, isolated-hover source strengths, rotor point sampling or the constant ideal-power receiver assumption.

The useful research outcome is a clear boundary between acceptable and unacceptable computation for the declared equations. Reaching 5,000 coupled local-3D Boids still requires a later full receiver-set test, a complete geometry pipeline, local-neighbor behavior, load assembly, integration/control checks and measured end-to-end computation. None is granted or implied by this recommendation.

## Verified source basis

No new literature search was needed. The project already verified the following primary material; versions and reading limits remain in its existing ledgers:

- [WGSL, 21 September 2026](https://www.w3.org/TR/2026/CRD-WGSL-20260921/), §§15.7.2–15.7.6 and 17.5.32: permitted f32 behavior, reassociation, subnormal handling and norm/division accuracy. It does not make `Math.fround` an exact shader emulator.
- [WebGPU, 15 September 2026](https://www.w3.org/TR/2026/CRD-webgpu-20260915/): compilation, error scopes, device loss and readback contracts. API success is not numerical qualification.
- [Higham 1993](https://doi.org/10.1137/0914050), pp. 784–788, and [Neumaier 1974](https://doi.org/10.1002/zamm.19740540106), p. 40: summation methods under stated arithmetic assumptions. Their error analyses are not automatic WGSL guarantees.
- [Bauersfeld et al., arXiv v3](https://arxiv.org/html/2403.13321v3), III–VIII; [Kiran et al., RSS 2025](https://www.roboticsproceedings.org/rss21/p102.html), relevant arXiv v1 sections II–V; [Gielis et al., arXiv v1](https://arxiv.org/html/2312.03488v1), §§2–4: flow, receiver and aggregation scope respectively.
- [Nyland, Harris and Prins, GPU Gems 3, chapter 31](https://developer.nvidia.com/gpugems/gpugems3/part-v-physics-simulation/chapter-31-fast-n-body-simulation-cuda), §§31.2–31.4: directed work and data reuse need an implementation baseline. CUDA gravity timings predict neither WebGPU wake cost nor swarm performance.

These sources motivate the questions and limitations. The proposed protocol and its numerical allocation are our design choices, not reported findings of those sources.
