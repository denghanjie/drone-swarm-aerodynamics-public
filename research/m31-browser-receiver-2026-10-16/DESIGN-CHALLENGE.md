# Receiver-only browser f32: static design challenge

2026-10-16. Static inspection only; no implementation execution, root evaluation, field generation, browser launch or benchmark. This note reviews the parent's selected design, not an executed result.

**Disposition:** this is a distinct and appropriately bounded successor question: whether one actual browser f32 translation of the fixed M28 receiver law meets newly stated engineering limits on 24,000 exposed saved inflows plus 32 frozen scalar probes. It does not port or qualify the wake field. Proceed to final protocol after resolving the operand definitions, constant/power semantics and finite-domain items below.

## 1. Pin the reused data and constants

The current exact-zero manifest lists `fresh1000-I.f64` as 136,000 bytes, SHA-256 `85bed7f928b00b9da379f853b80097f6ba8dd30c57e65f21bcbbdca9cabcfa59`, and `fresh5000-I.f64` as 680,000 bytes, SHA-256 `cc17e5d23a3761f5b175c987c1ca1d8a1631f34f0502ac533365b8c8526043aa`. Those are 17-column binary64 output rows, not contiguous four-column inflow arrays. Extract columns 0–3 in receiver-major, rotor-major order; preserve original row/rotor IDs, original binary64 bits and packed binary32 bits. Verify source hashes and exact lengths before interpretation. This note read the manifest and writer, not the binary values or their range.

Call these exposed reused inputs. The names `fresh1000`/`fresh5000` describe the closed parent campaign; they are not new holdouts. The 32 scalar probes must have a frozen exact list and original bit patterns, include zero and 128, cover small positive normal values, the `min(1,1/alpha)` transition, and the intermediate/high range. No selective deduplication: repeated values still count as separate input items. Duplicate packed values should be identified descriptively.

Pin original `f0` and `vi0` as binary64 values with their derivation/provenance, then separately pin their uploaded f32 bits. The original code computes `f0=m*g/4` and `vi0=sqrt(f0/(2*rho*area))`; a decimal label alone does not specify its exact binary64 value. Keep the shader constants uploaded, as selected. Recomputing `vi0` in the shader would introduce a different question.

## 2. Use an alpha-parameterized independent reference

Let R denote the reference on original U, f0 and vi0; Q the reference on exact decoded packed values Uq, f0q and viq; and A the reference on the shader's returned alphaG. For each item:

| Control | Cubic coefficient | Reference force |
|---|---|---|
| R64 | alphaR = original U / original vi0, evaluated in binary64 | original f0 × xR |
| Q64 | alphaQ = decoded Uq / decoded viq, evaluated in binary64 | decoded f0q × xQ |
| A64 | exact decoded returned alphaG, passed directly to the solver | decoded f0q × xA |
| G32 | uploaded Uq / uploaded viq in WGSL f32 | returned shader fG |

**Implementation trap:** the existing independent `receiverSolution(nominal,inflow)` recomputes vi0 from nominal, rho and area. Calling it with f0q and Uq does not implement Q. Likewise, constructing a synthetic inflow `alphaG*viq` and passing it through that API adds an unnecessary multiply/divide rounding. Freeze an independent bisection that accepts alpha directly, with the intended force multiplication outside it. Do not import the whole field module just to obtain roots.

Save each reference's x, alpha, force, residual, bracket, iteration count and status. Retain strict independent binary64 reference checks, e.g. the existing residual/bracket ceilings where applicable; do not loosen reference accuracy to the GPU engineering gates. Ordinary binary64 bisection is an independent numerical reference, not a directed-rounding interval proof. R can also be compared with saved I rotor-force columns 4–7 using the same scheduled R result, without an extra solve.

The signed force-error decomposition is then explicit:

- Packing/parameter quantization: `fQ - fR`.
- Shader alpha-division effect: `fA - fQ`.
- Newton root arithmetic effect: `f0q * (xG - xA)`, reconstructed in binary64.
- Final force-product effect: `fG - f0q * xG`, reconstructed in binary64.

Their sum is `fG - fR`, up to host reconstruction rounding. Also report `alphaG-alphaQ`. This isolates the final multiplication, which an x-only comparison would miss. The packing term combines U, f0 and vi0 quantization; do not claim to separate those three effects without additional prospectively budgeted controls.

## 3. Preserve the chosen Newton experiment exactly

M28 uses **at most twelve** Newton steps, initialized with `min(1,1/alpha)`, with `next = x - (x*x*x + alpha*x - 1)/(3*x*x + alpha)`, then tests `abs(next-x) < 1e-15`, assigns `x=next`, and breaks if that test succeeds. Freeze parentheses, f32 types, threshold representation, update-before-break behavior and iteration-count semantics. Do not add clamping, a safeguarded step, a different initial guess, more steps or a tuned f32 stopping threshold.

The zero-U fast path must return x=1, alpha=0, f=the packed f0, iterations=0 and a distinct status before any reciprocal. For positive U, return the final updated x and whether termination was the threshold branch or the twelve-step cap. In this f32 range the 1e-15 expression can effectively detect a rounded fixed point; it is not a residual certificate. A two-cycle or a cap-reached result may still satisfy the new accuracy gates. **Cap reached is not automatically a numerical failure under the selected finite-step M28 experiment**; distinguish algorithm termination from qualification. This receiver-only choice supersedes the more conservative generic root-stagnation stopping suggestion in the earlier full-wake proposal.

WGSL compiler contraction/reassociation allowed by the implementation may affect results. Source expression parity is not bitwise parity with JS or a `Math.fround` emulation. Record the actual browser/adapter/backend and pin shader source. Do not use a CPU f32 replay as the decisive GPU reference.

## 4. Define exactly what the three new limits compare

The proposed limits are prospective engineering choices, not consequences of the old omission allowance or evidence of flight/physical adequacy.

- Make `abs(fG-fR) <= 1e-7 N` the primary end-to-end rotor gate so quantization remains charged. Report G/Q and G/A force errors separately.
- For the root-isolation gate, define `abs(xG-xA) <= 1e-6` and `abs(xG^3 + alphaG*xG - 1) <= 2e-6`, both computed on decoded outputs in host binary64. The latter is the absolute dimensionless cubic residual; do not silently divide it by an additional normalization factor.
- Also report x error and cubic residual against Q and R. If the claim is that *all three limits* hold relative to the original model, explicitly enforce the x/residual gates against original-reference operands too. Do not leave that interpretation to the report writer. A residual reconstructed from `fG/original f0` is distinct from one at the separately returned xG and should be labeled accordingly.
- Require finite alphaG/xG/fG and `0 < xG <= 1`, `0 <= fG <= f0q` for positive accepted inflows; exact zero behavior as above. Declare whether any harmless signed zero is accepted and retain raw bits regardless. No tolerance-based clipping of bad outputs.

Report the old `1e-12 N` original-reference rotor gate separately, including maximum error and failure count. Even at zero U this compares packed f0 with original f0, so a difference there is constant quantization rather than Newton failure. Failure of that legacy gate does not invalidate a pass under a separately labeled new gate. It does mean the experiment has not met the old binary64 compatibility standard. Do not replace it with a larger omission tolerance. Report all-item maxima, their IDs and exact operands, as well as batch coverage; averages cannot excuse a failing item.

## 5. Power needs two parameter conventions

The selected cubic is coherent with an ideal-power law whose coefficient is `vi0^2/f0`. Independently rounding f0 and vi0 generally breaks exact equality between `viq^2/f0q` and the original `1/(2*rho*area)`. Therefore a power check using original rho/area on GPU fG and Uq contains parameter-quantization effects as well as solver error.

Save and label both:

1. **Represented receiver identity:** use `kq=viq^2/f0q`, `Pq(f,U)=f*(U/2+sqrt(U^2/4+kq*f))`, and nominal `Pq0=f0q*viq`. Evaluate at actual fG and Uq. This includes alpha-division, root and final-product effects relative to the represented model. For a pure root identity, the dimensionless expression `xG*(alphaG/2+sqrt(alphaG^2/4+xG))` uses the returned alpha directly; label it separately.
2. **Original model deviation:** use original rho/area, original U and actual fG against original nominal power. This includes all representation/arithmetic effects, matching the original-reference rotor comparison. Preserve R's original power residual as reference-quality evidence.

Do not label either as electrical or shaft power, measured efficiency, or independent physical validation; it is ideal actuator-disk power including thrust times upstream flow. Power reconstruction is algebraically related to the cubic and is not an independent physical test. The proposed design supplies no new power tolerance. Either declare power a diagnostic (with finiteness required), or freeze a new explicit gate before execution. The old binary64 power tolerance cannot silently become the GPU acceptance gate.

## 6. Finite-domain and actual-browser safeguards

Define the input domain for **all** saved and scalar U values, not only the probes. If it is [0,128] m/s, validate original and decoded U against that bound before any shader dispatch; a saved out-of-range value is admission failure, not permission to clip, omit or enlarge the interval. Positive finite f0q and viq are required.

Finite positive U alone does not guarantee safe initial reciprocal arithmetic. A very small positive U can round to zero, produce a subnormal/zero alpha, or overflow `1/alpha`; WGSL exceptional and subnormal behavior must not be assumed identical to JS. For this first finite-step test, prospectively admit exact zero or positive values whose decoded Uq and viq are bounded so that alpha and its reciprocal stay safely normal/finite, including permitted division rounding. State that host admission rule without requiring an undisclosed GPU probe or alternative root solver. If the reused data violate it, close admission as failed; changing the algorithm or adding a tiny-alpha rescue would be a different experiment. No blanket validity claim for every real U in [0,128] follows from 32 probes and two saved matrices.

Use an actual secure browser context with WebGPU. Record browser version/build, OS, adapter metadata exposed by the API, requested features/limits and fallback-adapter indication where available. Do not invent an unavailable hardware/backend identity; state the limitation. An unavailable adapter, unsupported required capability, compile/validation error, device loss or readback failure ends this attempt; no silent CPU/software/browser substitution. Compile/setup can occur before the scientific dispatches, but no test dispatch, warmup, automatic rerun or page auto-run may consume unrecorded science. No timing comparison is needed; lifecycle duration is resource accounting only.

## 7. Count dispatches, items and reference solves separately

“One GPU invocation per batch” is ambiguous in WGSL terminology. Freeze **three dispatches on success**, with one active shader invocation per item: 32 probes, 4,000 saved fresh1000 inflows and 20,000 saved fresh5000 inflows, in a fixed order (probes first is the useful fail-fast order). Padded invocations must return before reading/writing. Record IDs/status sentinels so default zeroed buffers cannot masquerade as completed results.

Total active items are 24,032. R, Q and A require 72,096 scheduled bisection calls, charged even for zero fast paths; the GPU has at most 288,384 Newton updates. With a frozen 96-iteration reference ceiling, reserve at most 6,921,216 bisection iterations. If workgroup size is 64, three ceil-rounded dispatches launch 24,128 invocations including padding; do not call all of those receiver solves. These are prospective accounting identities, not measured work. Budget host residual/power reconstruction and all output/bit records too.

Each successful batch needs GPU outputs persisted before reference-at-returned-alpha or gate checks. Bound buffers and evidence size up front; retain a reserved failure record. Define attempt lock, watchdog, browser-close/device-loss path, phase deadlines, overall wall cap and no-retry terminal status before launch. A capability/admission/numerical failure prevents later batches; preserve the completed prefix and do not call it full coverage. Successful completion requires all 24,032 items and all three dispatch/reference batches. Any saved-only review may reconstruct arithmetic from saved results but must not solve additional roots or dispatch the shader again.

R8 and every prior budget remain closed. The question answered by a successful result is only finite receiver arithmetic feasibility on the recorded environment and frozen exposed/probe inputs. A future wake/geometry/reduction port needs its own domain, quantization, arithmetic and cost qualification.

## Sources inspected

- [M28 receiver/power implementation](<REPOSITORY_ROOT>/outputs/milestone-28-source/aero.cjs).
- [Independent receiver solution](<REPOSITORY_ROOT>/research/m31-source-omission-2026-10-16/source/independent.cjs:261) and [original constants](<REPOSITORY_ROOT>/research/m31-source-omission-2026-10-16/source/candidate.cjs:4).
- [Exact-zero writer/qualification code](<REPOSITORY_ROOT>/research/m31-zero-screen-2026-10-16/source/experiment.cjs) and [saved-artifact manifest](<REPOSITORY_ROOT>/research/m31-zero-screen-2026-10-16/manifest.json).
