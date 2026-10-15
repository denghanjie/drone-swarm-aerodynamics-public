# Prospective complete body-load question

Status: proposed for independent static scrutiny, before implementation or numerical exposure. No old case, seed, component tolerance, source, result, skipped stage or terminal invocation is reused as a new launch identity.

## Question and estimand

Does one fixed ordinary-binary32 primitive-A GPU implementation deliver all receiving-rotor forces, total body thrust and body roll/pitch/nominal-yaw moments within the declared direct-output tolerances relative to original binary64 model inputs, for each of four newly generated, fully retained finite test families including two N=5,000 cases?

All cases are required. Failure, incomplete evidence or absent required work prevents qualification. This finite feasibility question has no timing, real-time, physical-validity, general-domain or novelty claim. Its interpretation cannot retroactively qualify an earlier strict component gate.

## Fixed architecture

Host derives axes and four world rotor offsets from original binary64 quaternions, saves them and packs ordinary f32 words. No normalization, recentering, high/low coordinates, source omission, adaptive precision, method search or fallback. GPU computes `sourcePosition-(receiverPosition+offset)`. One invocation per receiver inspects ascending source IDs, maintains four serial accumulators, performs four receiver solves and assembles body loads in the same invocation. No world rotation is computed. Source wake amplitude stays isolated hover regardless of source motors, a disclosed model limitation.

R is the independent original-state binary64 model. Q consumes the exact decoded prepared GPU interface, including packed constants, axes, offsets and prescribed lagged nominal motor values. Q does not reconstruct from rounded quaternions or truncate its subnormal nominal values. Actual GPU inflows are separately fed to a reserved independent scalar reference during the sole science invocation for receiver attribution. No duplicate hidden root solves. Saved-only review may recompose loads and residuals from saved values, but may not rerun field/root solvers or generate new cases.

Original, decoded and GPU terminal policy classes and complete validity coverage are mandatory. Positive and arithmetic-zero policy-7 statuses are retained separately but map to the same policy class; no boundary exceptions may be introduced after outcomes. No full term arrays are retained. R/Q ordinary and same-pass Neumaier sums are retained; their difference must be <=1e-10 m/s. This is a consistency check, not an exact summation proof. Combined field discrepancies are diagnostics; no term L1 or standalone reduction certificate is claimed.

## Direct output targets

For m=.027 kg, g=9.81 m/s², arm coordinate a=.028 m and D=2sqrt(2)a:

- epsilonT = .005mg, the pre-existing analyst-selected body-thrust scale.
- epsilonMoment = .0005mgD, the pre-existing roll/pitch engineering scale, prospectively reused for this two-sided output question.
- epsilonYaw = epsilonMoment, a NEW engineering choice of the same moment scale, not an inherited historical yaw target or a physical sensitivity result.
- epsilonRotor = .5 min(epsilonT/4, epsilonMoment/(4a)), a NEW direct rotor-output limit. It prevents large rotor errors from hiding in the thrust/roll/pitch assembly nullspace. The factor .5 leaves an analytical planning margin for body assembly; actual body outputs must independently pass their gates.

Compare actual delivered GPU outputs directly against R. Proposed numerical-reference allowances (added inside the target comparison, not widening it) are 1e-12 N for rotor/thrust and 1e-13 N m for moments; independent critique must resolve reference convergence and error evidence before adoption. Q-R and GPU-Q differences support attribution only. Meeting a direct rotor gate is not qualification of the old isolated receiver or wake gate.

## Receiver and domain

Prescribed lagged motor-state admission is [0,2.25mg/4] N. This is motivated by a command envelope, not a proven invariant of actual RK-stage motor states. Raw f32 negative/nonfinite words are invalid; zero signs are canonicalized. Original-positive values packing to zero remain flagged and included in original-R comparisons. Packed positive subnormal nominal values are explicitly truncated by raw-word inspection to +0 before candidate arithmetic, with a distinct status; Q retains their ideal decoded values. The ideal force is bounded by nominal, so the absolute force removed per subnormal is <2^-126 N. This is an analytical magnitude bound, not a physical assertion or implementation result.

For a normal positive nominal n, compute vi=sqrt(n/(2rhoA)); invalid/nonfinite/zero vi rejects. U=0 returns n. Otherwise, for U<=vi use alpha=U/vi, x0=1 and x³+alpha*x-1; for U>vi use r=vi/U, x0=r and r*x³+x-r. Exactly twelve Newton updates; no clamp or fallback. Record branch, coefficient, vi, final x/force, residual, final step, iteration count and status. Arithmetic ratio/product zero remains explicitly flagged and is acceptable only under the frozen validity and final-output gates; never call it an original exact zero or convergence. Nominal yaw uses the candidate's same explicitly canonicalized nominal operands, with loss visible against R/Q.

Retain the original field support, tilt and near-domain policies. Individual terms must be finite and in [0,128] m/s. Completed R/Q/GPU inflows must be finite in [0,2^20] m/s. At most 5,000 admitted terms gives a real-arithmetic bound of 640,000 m/s; the larger numerical admission provides headroom and is still checked on actual sums. This is not a physically plausible flow envelope or a proof of all rounded arithmetic. Position admission ±128 m is a separate geometric bound.

## Inputs, controls, stopping and resources

Four output-independent fresh families are proposed: N50 paired columns, N500 tilted layers, N5000 dense volume and N5000 sparse broad-coordinate pairs. The prior application memo supplies the sketch; exact generator/proof/control/schema decisions remain under independent review. General coordinates, unequal nominal motors and fixed zero/tiny/normal/max edge assignments must be fixed before generation. No redraw or parameter tuning after outcomes.

One science invocation: 300 s wall, 768 MiB raw evidence plus 32 MiB results, one case resident at a time, raw GPU buffers <=208 MiB, measured process RSS <=4 GiB. A separate sole saved-only review: 120 s wall and 32 MiB outputs. Exact loop/byte/lifetime/reference/control counts must be frozen before execution. Public raw files must fit repository per-file limits without changing scientific values. Any timeout, unsupported device, resource/validity failure or implementation fault closes the invocation without retry. Numerical output failures remain reported and may allow the already-reserved independent cases only if the final protocol explicitly says so. No benchmark is authorized by a correctness pass.

Independent static source review, privacy review, source publication and independent byte verification must all precede numerical exposure. Every completed milestone retains source/raw/reference/claim/literature/restart records and a tested Three.js view of saved evidence. No new launch after 2026-10-15T23:00:00Z.
