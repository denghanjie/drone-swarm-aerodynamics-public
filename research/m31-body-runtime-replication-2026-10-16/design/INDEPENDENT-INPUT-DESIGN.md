Replication note: the inherited input proof/scaffold below is unchanged; only the adopted namespace is replaced by `m31.body-load.runtime-replication.v1/2026-10-16` plus NUL. This note is a coordinator override, not a new independent proof or observed input.

# Static body-load input and control design

**Proposal only. No inputs, hashes or seeds were generated; no model/kernel was imported, evaluated, compiled or run.** This document concretizes the parent's narrowed candidate: ordinary-f32 primitive A, original-f64 host-derived axes/offsets, all receivers, body-only observables. It does not authorize the proposed 300-second science or 120-second saved-review invocations, nor reuse any previous invocation, seed or budget.

The four families below are fixed in advance. Their parameters and controls must be part of a new immutable protocol/source manifest before any data generation. Failure of admission, exposure, coverage, policy agreement, time or resource limits ends the affected case; no resampling, seed replacement, parameter search or fallback is allowed.

## 1. Exact deterministic recipe, without evaluating it

Use ASCII namespace bytes `m31.body-load.input.v1/2026-10-16` followed by one NUL byte. A hash message is exactly:

`namespace || uint32_BE(familyID) || uint32_BE(latticeIndex) || uint8(streamID) || uint8(component)`.

SHA-256 is the hash algorithm. Family IDs are 1, 2, 3 and 4. Lattice indices begin at zero. Stream IDs are 0 permutation, 1 jitter, 2 local tilt, 3 local yaw, 4 motor scale, 5 velocity and 6 angular velocity. Unused component bytes are zero. For scalar streams, interpret digest bytes 0–7 as an unsigned big-endian integer, discard its low 11 bits and call the resulting 53-bit integer k. Set `u=k/2^53` and `s=2u-1`. Thus `0<=u<1`, `-1<=s<1`, with no half-integer conversion ambiguity. This is a written namespace/algorithm, not a generated seed or populated manifest.

For each family, enumerate `(ix,iy,iz)` in increasing x, then y, then z, with `ell=((ix*ny)+iy)*nz+iz`. Compute stream-0 digests and sort the lattice indices by all 32 digest bytes lexicographically, breaking ties by ell. The position in that sorted list is the actual receiver/source ID. All scientific summation visits these IDs in ascending order. This fixed permutation prevents geometry-order accumulation from being an implicit design choice. Save both permutation and inverse permutation. The designated exposed source for lattice row `(ix,iy,iz)` with `iz<nz-1` is the inverse-permuted ID of `ell+1`.

All elementary arithmetic producing the authoritative original states uses binary64 with operation order frozen as written in the generator source. JavaScript Math.sqrt is implementation-approximated; ECMAScript does not guarantee correct rounding. Pin the exact runtime and retain actual quaternion, frame, axis and domain admissions. No trigonometric routine is required. `nextUp64`, `nextDown64`, `nextUp32` and `nextDown32` denote adjacent finite IEEE representable values, specified by raw bit stepping, not a numerical search. The actual runtime/version and arithmetic implementation must be pinned before generation. The bounds below are an analytical construction argument with conservative rounding assumptions and mandatory actual admissions, not a full formal floating-point proof.

Define `Y(t)=(0,t,0,1)/sqrt(1+t*t)` and `Z(h)=(0,0,h,1)/sqrt(1+h*h)` in quaternion xyzw order. Use the standard Hamilton product, left operand applied last, and the original independent-reference matrix rotation formula. The family frame quaternion is `qB=Z(h) ⊗ Y(t)` and its matrix is B. The columns of the exact mathematical B form an orthonormal basis; its third column c is the common column axis. The actual generated binary64 matrix is admitted separately and is not silently repaired.

| ID | Dimensions / N | Spacing `(sx,sy,sz)` m | Frame `(t,h)` | Local tilt parameter b |
|---:|---|---|---|---|
| 1 | 5×5×2 / 50 | `(.731,.763,.611)` | `(0,0)` | `1/64` |
| 2 | 10×10×5 / 500 | `(.731,.763,.611)` | `(21/200,1/3)` | `1/96` |
| 3 | 20×25×10 / 5,000 | `(.731,.763,.611)` | `(7/100,1/5)` | `1/64` |
| 4 | 50×50×2 / 5,000 | `(3.211,3.211,.611)` | `(0,3/20)` | `1/64` |

These algebraic parameters replace approximate angle descriptions: family 2's common tilt is exactly `2 atan(21/200)` in real arithmetic, close to 12°; family 3's is `2 atan(7/100)`, close to 8°; family 4's horizontal rotation is `2 atan(3/20)`, close to 17°. Only the rational parameters above are generation inputs.

For each ell, define centered local coordinates `v=((ix-(nx-1)/2)*sx, (iy-(ny-1)/2)*sy, (iz-(nz-1)/2)*sz)`. Set original position to `origin+B*v+jitter`, with fixed origin `(.123456789,-.234567891,1.345678912)` m. Each world-coordinate jitter component is `(7/10000)*s` from stream 1 components 0–2. These are fresh deterministic binary64 coordinates; no previous geometry, translated scene or saved input is used.

Let `tx=b*s(stream2,0)`, `ty=b*s(stream2,1)`, and `w=(7/5)*s(stream3,0)`. Construct `qL=(tx,ty,0,1)/sqrt(1+tx*tx+ty*ty)`, `qZ=Z(w)`, and original attitude `q=qB ⊗ qL ⊗ qZ`, with the two products parenthesized `(qB ⊗ qL) ⊗ qZ`. The rightmost local yaw leaves the thrust axis unchanged while giving general rotor orientations. Constructing a normalized original input quaternion is part of this recipe; neither host preparation nor GPU packing may subsequently renormalize an admitted quaternion or axis.

Velocity components are `(1/10)*s(stream5,k)` and angular velocity components `(1/5)*s(stream6,k)`, k=0,1,2. They are finite provenance fields and are unused by this quasi-static load query. Original axes and all four world offsets are derived in binary64 from q; those prepared values are packed once to f32. There is no world-load matrix in the candidate interface.

A fixed input audit requires at least 99% of the 3N original position components to differ numerically from their f32 representations. This is an input admission, not output selection. Its failure is terminal without changing the recipe. No statement that this hash realization passes that audit is made here.

## 2. Motor schedule and packed-zero policy

Let `fmax` be the binary64 value of the production-ordered expression `((2.25*.027)*9.81)/4`. Original nominal motors must lie in `[0,fmax]`. The packed upper admission is `RN32(fmax)`, allowing the representational rounding of the valid original endpoint. Do not compare that packed endpoint against the unrounded original maximum and accidentally reject it.

For ell, set `scale=3/4+u(stream4,0)/4`, and the core tuple to `fmax*scale*(13/100,37/100,61/100,89/100)`, with source multiplication grouping frozen. For residue `r=ell mod 64` at least 16, use this tuple cyclically rotated by `ell mod 4`. It is unequal, positive, below fmax and has nonzero nominal roll, pitch and yaw; no flow observation influences it. For r below 16 use the following fixed tuple before the same cyclic rotation. `C1,C2,C3` are the last three entries of the current core tuple, `n=2^-126`, `d=2^-149`, and `m=n-d/2`.

| r | Unrotated tuple |
|---:|---|
| 0 | `(0,0,0,0)` |
| 1 | `(fmax,fmax,fmax,fmax)` |
| 2 | `(0,C1,C2,C3)` |
| 3 | `(2^-1074,C1,C2,C3)` |
| 4 | `(2^-151,C1,C2,C3)` |
| 5 | `(2^-150,C1,C2,C3)` |
| 6 | `(nextUp64(2^-150),C1,C2,C3)` |
| 7 | `(d,C1,C2,C3)` |
| 8 | `(n-d,C1,C2,C3)` |
| 9 | `(m,C1,C2,C3)` |
| 10 | `(nextDown64(m),C1,C2,C3)` |
| 11 | `(n,C1,C2,C3)` |
| 12 | `(n+d,C1,C2,C3)` |
| 13 | `(nextDown64(fmax),C1,C2,C3)` |
| 14 | `(fmax,0,fmax,0)` |
| 15 | `(0,fmax,0,fmax)` |

The adopted candidate has a deliberate approximation: **packed nominal raw words with exponent zero and nonzero fraction are truncated to applied nominal +0, with an explicit flag**. Q's ideal reference retains the decoded subnormal nominal. Canonicalize signed zero and positive-subnormal raw receiver U to +0 as well, with distinct flags; save Uraw and bind the handoff reference to it, not the canonical value. Original positives that already round to packed zero are a separate status. Original exact zero, packed exact zero, packed subnormal truncation, positive-input coefficient rounded/flushed to zero, and positive-product rounded/flushed to zero must be distinguishable. Save both nominalQ and nominalApplied. For nominalApplied zero, force and x are zero; inapplicable root residuals are masked, not advertised as successful residual certificates.

For normal positive nominal, compute vi from that nominal and frozen rho/area. A zero or nonfinite vi is invalid. After nominal canonicalization, canonical zero U takes the explicit identity branch. Use the parent's bounded-coefficient root branches: low-U `x^3+(U/vi)*x-1`, start one; high-U `r*x^3+x-r`, `r=vi/U`, start r; exactly 12 Newton updates on these positive-input branches. A low-branch alpha that becomes zero/subnormal is flagged and still receives all 12 iterations. A high-branch r of zero is INVALID. Product zero/subnormal is flagged; direct gates decide its observable error. Do not repair/clamp a failed iterate. Normal-input vi zero and nonfinite/negative outputs fail, regardless of final gate size.

The actual-GPU-U handoff reference uses **raw U and ideal decoded nominalQ**, including subnormals and signed-zero provenance, and decoded physical constants; it does not adopt nominalApplied merely to conceal truncation error. Across the intentional truncation branch, x and residual agreement with the ideal equation are diagnostics, not asserted identities. The direct rotor/body gates below still decide its observable error.

Source wake strength remains the prescribed isolated-hover constant even for a source with zero nominal motors. This is existing model semantics, not a physically motor-responsive wake model.

## 3. Static finite envelope and domain proof

The following proves envelopes for the recipe, not observed generated values. Its rounding allowance is deliberately much larger than the fixed number of elementary operations requires. For implementation review, verify the operation count and absence of transcendental calls, integer overflow or implicit f32 preparation. Admit original quaternion norm error ≤`1e-10`, axis components ≤1.01, offset components ≤.1, finite states and both original/decoded global tilt. The mathematical-to-binary64 construction allowance is `1e-9` in positions/rotated vectors and quaternion-induced direction differences; RN32 position components contribute at most `8e-6 m` each within the box below. A conservative `2e-4 m` total displacement allowance covers packing plus primitive-A point addition/subtraction. No coordinate-generating code has yet been checked against this allowance. Frame quaternion norm and Gram-matrix deviation must pass fixed actual admissions (norm error <=1e-10; every Gram deviation <=1e-10); actual designated geometry is checked against the conservative downstream/radial/projection bounds during input admission. Those 29,700 designated rotor geometry audits across all four families are included in the one science envelope and are not additional all-pair field passes.

**Absolute position bounds.** For families 1–3, any rotated component is bounded by the sum of the three local half-spans. Including origin, jitter and the construction allowance gives component magnitudes less than 5 m, 10 m and 22 m respectively. For family 4 the horizontal half-span is `49*3.211/2=78.6695 m`; a planar orthonormal rotation bounds each horizontal component by `sqrt(2)*78.6695<112 m`. Adding the actual origin and jitter still leaves each horizontal component below 112 m, while its z magnitude is below 2 m. Thus every family has a substantial margin inside ±128 m, before and after packing. Broad coordinates do not require recentering.

**Tilt.** The local tilt angle is `delta=2 atan(sqrt(tx^2+ty^2))`, so `delta<=2 sqrt(2)b`: less than .045 rad for b=1/64 and .030 rad for b=1/96. The common frame tilt is at most 2t. Family 2 therefore has total tilt below .240 rad; family 3 below .185 rad; families 1/4 below .045 rad. All are strictly below 20°. In particular `axis.z>=cos(.240)>=1-.240^2/2=.9712` before the tiny construction/packing allowance, giving a wide margin above cos(20°). The local yaw does not alter this bound. Packed axis perturbation may be bounded by `2e-7` in Euclidean norm; it is not normalized away.

**Minimum center and rotor-point separation.** Orthogonality of the common frame preserves lattice separation. The smallest spacing is .611 m. Two jitter vectors differ by norm at most `2 sqrt(3)*.0007<.0025 m`. Thus distinct original centers are separated by more than .6084 m after the stated construction allowance. A rotor offset has norm `sqrt(2)*.028<.0396 m`, so every source-center to every other receiver rotor point has norm greater than .5688 m; the conservative packed primitive-A displacement allowance keeps it greater than .568 m.

An invalid near cylinder would require `0<down<2.5D` and radial `<.15`, with `D=2 sqrt(2)*.028<.08`, so down is below .2 m. Using the actual formula `perpendicular=d-down*axis`, the triangle inequality would force `norm(d)<.15+.2*norm(axis)` before small arithmetic allowances. With axis norm within `2e-7` of one, even a generous `.001 m` allowance makes that upper bound below .352 m. It contradicts the lower bound .568 m. This argument does not incorrectly assume the packed axis is exactly unit or that its computed perpendicular is exactly orthogonal. All distinct-pair near-domain visits are excluded by a gap above .21 m. Self is separately classified before geometry.

**Designated positive source at all four rotors.** For each non-top row, the next member of the same column has displacement from the receiver center `.611*c+eta`, where `norm(eta)<.0025`. Crucially, **c is the same tilted frame axis used to place the column and to define its attitudes**. Comparing a tilted source axis against a vertical-world scaffold would not justify these bounds.

For rotor offset o, `d=.611*c+eta-o`. Every source axis differs from c by at most delta<.045, independent of source/receiver yaw. Thus

`down >= .611*cos(.045)-.0025-.0396 > .56`,

`down <= .611+.0025+.0396 < .66`,

and the radial distance to the source axis obeys

`radial <= .611*sin(.045)+.0025+.0396 < .070`.

These bounds use the full offset norm and therefore apply to **all four rotors**, even when receiver/source local tilts differ. With the conservative packed/arithmetic margins, retain `down in [.56,.66] m`, `radial<.075 m`. Center distance is below .614 m, hence strictly below 3 m. Pairwise axis projection exceeds `cos(2*.045)>.99` with the rounding margin.

Since `2.5D<.2`, downstream is beyond the near region and below the 2 m fade start. The minimum half-width on this interval is `hmin=.07668*(.56+5.817D)`, which exceeds .075 m. Hence radial is below two half-widths with a wide margin; both fades equal one and the support projection is positive. The designated term is strictly positive for each rotor. This is not a claim that every upper row receives zero from every other column.

The adopted material exposure gate is **R ordinary inflow >=.25 m/s on all four rotors of every designated row**. Its analytical rationale is deliberately conservative: `D>.079`, so `down/D+5.817<15`; radial is below hmin, so xi<1 and the profile denominator squared is below 2. The fixed isolated-hover induced speed exceeds 1 m/s: `m*g>.25`, while `8*rho*pi*radius^2 < 8*2*4*.024^2 <.25`. Both fades are one and projection exceeds .99. Therefore the designated term exceeds `.99*(10/15)/2=.33 m/s` in the real-arithmetic bound, leaving .08 m/s of margin above the gate for the stated elementary-rounding assumptions and actual input admissions. Nonnegative ordinary summation cannot lower a retained positive contribution. No model output was evaluated to choose .25.

There are exactly 25, 400, 4,500 and 2,500 designated rows. Of these, the general unequal four-normal-motor core schedule covers 17, 298, 3,370 and 1,872 respectively: at least 68% in every family. At least three motors are normal positive on 23, 382, 4,281 and 2,343 designated rows respectively. These are static integer counts of the fixed lattice/residue schedule, not generated states or scientific evaluations. Edge/zero rows do not dilute the material exposure requirement, and a gate failure cannot trigger regeneration.

**Numerical inflow cap.** The candidate's cap is `2^20 m/s`, explicitly a numerical guard, not a physically credible inflow claim. Every accepted term is finite, nonnegative and at most 128. With at most 5,000 terms per rotor, the exact sum is at most 640,000. For f32 round-to-nearest additions, `5000*u32<1/3000`, so the standard positive-sum rounding bound stays below `640000*3000/2999<641000<2^20`; flushing can only reduce such nonnegative contributions. This also leaves margin under alternative addition grouping with at most N rounded additions on a path. Preserve the actual sum and fail if it is nonfinite, negative or above `2^20`; never clip. This mathematical bound does not validate arbitrary compiler behavior or the field model.

## 4. Finite controls, fixed before observation

Controls are a small, separate fixed table; they are not extra full-flock searches. Each designated policy control executes once per R/Q/GPU path. For pair controls, receiver center is zero, its inspected rotor offset is `(.028,.028,0)`, source position is `offset+d`, and both axes are +z unless explicitly stated. Distinct IDs are used except for self. Primitive A still computes source minus receiver-plus-offset, so inputs are packed/prepared normally. Exact policy expectations refer to frozen constants and the margins below.

| ID | Pair/control definition | Expected policy/outcome |
|---|---|---|
| P00 | Self ID and identical node | 0, valid self |
| P01 | Source center `(3,0,0)` | 0, strict center cutoff |
| P02 | Source center `(nextDown32(3),0,0)` | 1, center inside then zero downstream |
| P03 | `d=(.4,0,0)` | 1, downstream zero |
| P04 | `d=(.4,0,-.25)` | 1, downstream negative |
| P05 | `d=(0,0,2.5)` | 2, exact downstream cutoff |
| P06 | `d=(0,0,2.75)` | 2, beyond cutoff |
| P07 | `d=(0,0,D)` | 3, invalid near cylinder |
| P08 | `d=(.25,0,D)` | 4, valid near skip |
| P09 | `d=(.75,0,.6)` | 5, radial cutoff |
| P10 | `d=(0,0,.6)` | 7, positive interior |
| P11 | `d=(.02,0,2.25)` | 7, downstream fade |
| P12 | `d=(.2,0,.6)` | 7, radial fade |
| P13 | `d=(.5,0,2.25)` | 7, both fades |
| P14 | `d=(0,0,.6)`, receiver axis +x | Direct prepared-pair policy 6; globally inadmissible |
| P15 | Same axis +x in complete-input admission | Reject global tilt before query |

Policy 6 cannot be presented as a valid globally tilted application case: two near-unit axes both within 20° of +z have positive dot product. P14 is explicitly a low-level prepared-pair function control; P15 verifies the full-query rejection. Do not bypass global admission in a science case. Full-query zero/error/coverage records and the policy-7-numerically-zero symbol should also have synthetic raw-record decoder controls; they are not manufactured evidence of a physically valid profile evaluation.

Root controls comprise 16 original nominals crossed with nine U values (144 rows), plus two signed-zero rows (146 total). Nominals are `0`, `2^-1074`, `2^-151`, `2^-150`, `nextUp64(2^-150)`, `d`, `n-d`, `m`, `nextDown64(m)`, `n`, `n+d`, `2^-32`, `2^-16`, `fmax/64`, `fmax/2`, `fmax`. For each nominal, let `vstar` be the pinned host simulation of the candidate f32 vi construction if the packed nominal is normal positive; otherwise use exactly 1 solely to define the U control list. U values are `0`, `2^-149`, `2^-126`, `1/4`, `4`, `2^20`, `nextDown32(vstar)`, `vstar`, `nextUp32(vstar)`. This fixes zero, tiny, both scaled-root branches and the branch boundary without searching observed iterations or residuals. The nine rows remain separately identified even if any values coincide. Add `(nominal=-0,U=1/4)` and `(nominal=fmax/2,U=-0)`. A device square-root approximation can move a vstar-adjacent row between branches: check the branch against saved actual U/vi, not an assumed exact host/device equality. Wide low/high-U rows still cover both branches. Reference construction and admission work is explicitly part of the finite control budget.

Twelve admission/record controls are fixed: negative original nominal `-2^-149`; original nominal `nextUp64(fmax)`; nonfinite quaternion word; infinite position word; zero quaternion; position 129; nonzero packed pad; wrong state length; out-of-range source ID; synthetic term `nextUp32(128)`; synthetic sum `nextUp32(2^20)`; and one unwritten required policy/output slot. They must reject at the designated stage. Synthetic malformed bits remain raw until finite-word admission; no accidental NaN propagation is a valid rejection mechanism.

The explicit control ledger is 16 policy/global rows, 146 root rows and 12 admission/record rows, plus a fixed raw-schema table containing each of the 12 defined terminal symbols and four reserved symbols. This last 16-row table is decoding-only. No adaptive control expansion, rerun or alternate root solver is allowed after outcomes are observed.

## 5. Observables, gates and saved evidence

Primary body outputs are four U values, four effective forces, thrust T, effective roll, effective pitch and **nominal** yaw. The parent's engineering gates compare each receiver directly against original R:

`epsilonT=.005*m*g`, `epsilonM=.0005*m*g*D`,

`epsilonRotor=.5*min(epsilonT/4, epsilonM/(4*a))`.

Require each effective rotor's absolute error ≤epsilonRotor, thrust error ≤epsilonT, and each of roll/pitch/nominal-yaw error ≤epsilonM. The yaw gate is explicitly a new engineering choice, not inherited qualification. R uses ordinary ascending-source sums and independent binary64 root bisection; same-pass compensated sums are retained diagnostics. Q consumes exact decoded axes/offsets/nominals/constants directly. All values must be finite/admitted, outputs complete, and R/Q/GPU policy classes equal. Distinguish positive versus numerically-zero policy-7 statuses while comparing their common class as 7. Do not invent a separate passed L1, exact-GPU-term-sum or reduction-error certificate without retained terms.

Save actual same-pass GPU U, nominalQ, nominalApplied, vi, x, force, branch/coefficient, residual/validity, iterations, last step and zero flags. Save one independent ideal-nominalQ reference solve at each actual GPU U. A normal positive nominal yielding vi zero fails. Root finite/range/identity invariants remain hard checks; intentional truncation diagnostics must use their declared validity semantics. No additional numerical residual/x acceptance threshold is silently inherited from the old hover-only receiver.

## 6. Body-only resource and work ledger

Use one family resident at a time, scalar-u32 storage members and the evidence agent's authoritative 256 B / 64-word GPU record. Header words 0–7 are receiverID, N, recordStatus, failureStage, writtenFullPolicyWords, writtenRotorSymbols, firstFailureOrdinal, payloadValidity. Each rotor block begins at `8+12*r` and contains Uraw, nominalRawBits, vi, coefficient, x, force, shaderResidual, signedFinalUpdate, packedMeta, validityMask, positiveTermCount, zeroPad. packedMeta has branch bits 0–2, iterations bits 3–6, status bits 7–9, flags bits 10–25 and zero reserved bits 26–31. Words 56–59 contain effective `[T,Mx,My,nominalMz]`; words 60–63 contain nominal `[T,Mx,My,Mz]`. NominalApplied is reproducible from saved raw nominal and explicit canonicalization flags; no extra array is hidden. Source/schema indices are authoritative. Masked fields cannot masquerade as valid numeric zeros.

| GPU buffer | Formula | N=5,000 bytes |
|---|---:|---:|
| Packed nodes | 32N | 160,000 |
| All four packed offsets | 64N | 320,000 |
| Packed nominal motors | 16N | 80,000 |
| Constants/dimensions | 128 | 128 |
| Policy u32 per ordered pair | 4N² | 100,000,000 |
| Body/root outputs | 256N | 1,280,000 |
| Policy readback copy | 4N² | 100,000,000 |
| Output readback copy | 256N | 1,280,000 |

Listed raw GPU buffers total **203,120,128 B**. A 1 MiB reserve for all other control/uniform/readback buffers gives **204,168,704 B**, below 208 MiB (218,103,808 B). No world rotations or uploaded vi array are present. If a later implementation adds them or duplicates buffers, revise the ledger before adoption. Each 100 MB policy binding still requires fresh actual-device admission; old limits do not guarantee a new run. Dispatch at 64 lanes/group needs 79 groups at N=5,000. Watchdog/latency feasibility remains unknown.

R/Q policy words are uint16 per pair; GPU raw u32 words are retained. Each R/Q output uses the evidence agent's 480 B layout: 32-byte header; four 96-byte rotor blocks, each containing ten f64 values `(Uordinary,Ucompensated,nominal,vi,alpha,x,force,lo,hi,residual)` and four u32 values `(status,iterations,flagsValidity,positiveTerms)`; eight f64 body values, effective and nominal T/M. The handoff witness is 288 B/receiver: 32-byte header plus four 64-byte blocks, each seven f64 `(vi,alpha,x,force,lo,hi,residual)` and two u32 status/iteration and validity words, bound to actual Uraw/nominalRawBits in the GPU packet.

Original states are 136N B; original production-prepared interface is 224N B; independently R-derived prepared axes/offsets/nominals are retained separately at 224N B; packed interface is 112N B; decoded interface is 224N B. This explicitly preserves both original preparation paths rather than silently omitting one. The original production/reference rotation operation groupings must be frozen separately; their numerical difference is part of original-R error, while Q consumes the exact packed interface.

Total retained binary evidence is `8N^2+2424N` B plus fixed constants/headers/controls: **212,120,000 B** for one N=5,000 case. The four families total **427,593,200 B**. Reserving one failed maximum case and at most 64 MiB of controls/logs/metadata gives **706,822,064 B**, below the 768 MiB corpus ceiling (805,306,368 B). Duplicate staging files count toward the ceiling. A separate host raw-array cap of 384 MiB can contain one case plus one additional 100 MB policy-copy overlap and bounded scratch/control arrays; browser/driver/JS object overhead is not covered by that raw-byte claim. Stream R/Q per-receiver scratch terms; never retain full 4N² terms or unbounded pair objects.

The fixed science schedule is one R, one Q and one GPU full field pass per family, one root/load pass per path, and one actual-GPU-U handoff reference-root pass, plus the finite controls. The four families contain 50,252,500 ordered pair slots per path and 201,010,000 rotor-policy slots per path; three field paths therefore have at most 603,030,000 rotor-policy slots, before controls. There are 10,550 receivers total, hence 42,200 roots per path and 42,200 actual-U handoff roots. Record actual visited/early-exited work separately. Failure does not earn another pass.

All authorized generation, admission, controls, preparation, R/Q/GPU science, roots, copies and persistence must fit one newly authorized **300-second hard science envelope** if this protocol is adopted. The **120-second saved-review envelope** reads saved evidence and checks schema, coverage, gates, root/load identities and completion; it cannot rerun fields, regenerate geometry or silently spend another science pass. Time caps need an external closure mechanism that also handles a stalled dispatch. Static byte/work accounting establishes neither completion within these caps nor a speedup. This document launches neither envelope.
