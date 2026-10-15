# Coordinate-origin host contract — static proposal

This directory contains source and reservations only. Nothing here has generated the fresh scene, evaluated a wake/reference, imported the model, compiled WGSL, launched a browser/GPU, or run a checker. The parent owns integration, source publication, prospective budget, launch, and the final decision. The prior receiver budget is not reopened.

## Source release and immutable construction

Call `generateFresh(sourceCommit, charge)` exactly once after the parent confirms that the new campaign source commit is published and frozen. `sourceCommit` is exactly 40 lowercase hexadecimal digits. Seed digest is SHA256 of the UTF-8 bytes `m31-coordinate-origin-v1\n` + commit + `\n`; the seed is digest bytes 0–3 interpreted as an unsigned little-endian uint32. No seed is evaluated during source preparation. Historical seed 608897 is forbidden: if obtained, stop this frozen campaign before random draws and geometry. Do not redraw, choose another seed, or alter/search commits to obtain another digest. Seed zero is accepted.

The specified Mulberry32 transition consumes exactly six uint32 words per node, 30,000 total, without rejection or outcome-dependent draws. For each node the first three words generate x/y/z jitter: `(word % 16385) - 8192`. The next three words generate roll/pitch/yaw. The high bit supplies sign; the lower 31 bits supply magnitude by the explicit modulo mapping in the generator. Roll and pitch magnitudes are 131072–393216 ticks (2–6 degrees); yaw is 65536–11730944 ticks (1–179 degrees). One tick is 1/65536 degree. Conversion is `(ticks / 65536) * Math.PI / 180`. Quaternion multiplication/trigonometric grouping is copied from the prior cases source; no normalization is introduced.

The lattice is `[20,25,10]`, nested z, y, x; ID = `(z*25+y)*20+x`. For axis coordinate index i and dimension d:

`numerator = 131072 * (2*i - (d-1)) + jitter`

`canonical = numerator / 1048576`

`translatedNumerator = numerator + shift * 1048576`

`translated = translatedNumerator / 1048576`

The two origins are `[0,0,0]` and `[64,-32,16]`. Canonical absolute numerators are at most 3,153,920, below 2^22. Translated absolute numerators are at most 69,607,424, below 2^27. All integer operations are exact in binary64; scaling by 2^-20 is exact. Canonical positions need fewer than 24 significand bits and are deliberately exact binary32. Translated values need at most 27 and therefore remain exact binary64; their binary32 encoding can discard low bits. These facts are design limitations as well as useful controls: the campaign does not establish performance on arbitrary input encodings.

For every coordinate, the generator checks the exact dyadic certificate `units64(translated) - units64(canonical) - units64(shift) == 0`, saves the numeric zero residual, and checks canonical binary32 equality. It saves both integer numerator arrays, angle ticks, radian angles, source digest/seed, and exact-certificate counts. It clones the same quaternion, velocity, angular velocity, and force fields into translated states.

Receiver IDs are fixed `[749,500,2250,4750]`: lattice indices `[9,12,1]` lower interior, `[0,0,1]` lower corner, `[10,12,4]` middle interior, `[10,12,9]` top interior. These four disjoint strata are literal choices. There is no collision resolution, receiver replacement, scene rejection sampling, seed search, or follow-up microtest sweep.

## API

`generateFresh(sourceCommit,charge)` returns:

- `statesByOrigin`: two arrays, each 5000 arrays of 17 binary64 values.
- `receiverIds`: u32[4].
- `canonicalNumerators`, `translatedNumerators`, `angleTicks`: i32[15000] each.
- `angles`, `translationResiduals`: f64[15000] each.
- `audit`: bounded JSON metadata and proof counts; no BigInt values.

`prepareOriginal(statesCanonical,ids,C,charge)` runs once. It admits all 17-state fields, original quaternion norms within 1e-10, position bounds, prepared axis bounds and the unchanged 20-degree tilt gate. It rotates all 5000 source axes once and all 16 receiving rotor offsets once. No quaternion normalization is permitted.

`translatePrepared(P,translatedStates,C,charge)` runs once. It copies the original prepared arrays and metrics, admits translated finite states/position bounds, and replaces exactly 15,000 position fields. It performs no quaternion norm, rotation, or tilt recomputation. `C` is retained in the signature for stable integration and is not reevaluated.

Prepared snapshots P, Q0 and Q1 all have `nodes:f64[40000]` (8/node: position.xyz, axis.xyz, two +0 pads), `offsets:f64[64]`, `constants:f64[16]`, `ids:u32[4]`, `axisMetrics:f64[15000]` (axis norm, norm-minus-one, tilt margin). Each snapshot encodes to 440,656 bytes.

`packPrepared(P,C,charge)` runs once per origin and returns `Q0`, `Q1`, `constants` (QC object), `packedAB`, `packedC`, `reconstructionResiduals:f64[15000]`, `positionPackingResiduals:f64[15000]`, and `audit`.

`packedAB` and `packedC` each expose `nodes`, `offsets`, `ids`, `constants` as u32 arrays. A/B share one exact packed input. A/B node stride is eight words `[px,py,pz,ax,ay,az,0,0]`. C is twelve `[pxHi,pyHi,pzHi,ax,ay,az,0,0,pxLo,pyLo,pzLo,0]`. C's first eight words per node are copied from and explicitly checked equal to A/B. Offset/constant/ID arrays are shared in memory, but can be saved as separate logical artifacts if desired.

For each axis, high = ordinary binary32(original), low = binary32(original - decoded high). Each low must be finite and have absolute value at most 2^-17. The frozen integer construction actually limits the largest rounding residual to 2^-18; the common shader/host admission bound remains 2^-17. Exact dyadic `units64(high)+units64(low)-units64(original)==0` is required for all 15,000 coordinates; actual binary64 `(high+low)` must also equal the original exactly. The reconstruction residual array contains one saved zero for every certificate. Ordinary position residuals save decoded high minus original, signed.

Q0 uses decoded ordinary binary32 positions. Q1 uses the binary64 semantic sum of high+low as its position, not an attempted f32 reconstruction. Every nonposition field in Q1, including axis metrics and pads, is explicitly compared with Q0 via `Object.is` (therefore preserving signed zero). There are 40,084 such comparisons per origin. Axis metrics are computed once for Q0 and copied to Q1. All other decoded fields and constants are identical. Q1 is not an orphan accuracy oracle: it is assessed against R under the unchanged epsilon before C can run.

`evaluateSelected(P,C,label,charge)` accepts labels `R`, `Q0`, `Q1`, with one invocation of each per origin, six total. Each invocation reserves 80,000 slots and preserves the original independent-I reference formulas: source minus `(receiver + offset)` in binary64; left-associated dot products; Math.hypot; strict center `<3`; down-before-radial policy; the original near predicate, profile, cutoffs and factored fades; ordinary and Neumaier accumulation over ascending eligible source IDs. Adding saved displacement vectors does not change term expressions. Output ordinal is `((selectedIndex*5000+sourceID)*4+rotor)`.

The result has `metadata:u32[640000]`, `scalars:f64[1440000]`, `codes:u8[80000]`, `terms:f64[80000]`, `ordinarySums:f64[16]`, `compensatedSums:f64[16]`, `sumValidity:u8[16]`, `complete`, `failure`, and counts. Metadata is eight words: ordinal, receiver, source, rotor, status, policy, validity mask, flags. Scalar indices 0–11 retain the old order (centerNorm, down, radial, halfWidth, axisDot, projection, normalizedDown, xi, normalizedSpeed, fadeDown, fadeRadial, term); 12–14 are centerDelta.xyz, 15–17 are rotorDisplacement.xyz. A snapshot is 14,800,272 raw bytes.

Valid status values remain 3 early zero, 4 profile zero, 5 positive. Reference domain failure is status 2; a failed current arithmetic slot is status 6. Unvisited slots retain status 0, policy sentinel 0xffffffff and code byte 255. Completed-rotor sum validity is separate. A domain/numerical stop produces `complete:false` plus partial evidence, never fake complete zero terms. Known reference finite/domain failures set `failure.errorClass='numerical'`; unexpected exceptions and charge failures are integrity failures. These partial arrays must be saved, not treated as completed scientific summands.

Binary helpers are `encodeU32`, `encodeI32`, `encodeF64`, `decodeU32`, `decodeF64`, all explicit little-endian. u8 arrays are already byte-addressed.

## Assessment and failure routing

All assessment reports have `pass`, `integrityPass`, `numericalPass`, uncapped `errorCount` and `errorClassCounts:{integrity,numerical}`, bounded first 32 witnesses, and named `counts`. Never infer routing from the witness subset. `pass = integrityPass && numericalPass`.

`assessR(R,C)` validates all 80,000 saved R records: fixed identities, policy/code agreement, full reached masks, routing, status/sign semantics, all eighteen finite bounded reached scalars and +0 placeholders, and exact identity of scalar term with term array. `assessQ` applies the same row validator to Q within its existing pass. These comparisons have explicit row/field counters and perform no geometry recomputation. `assessR` then validates exact stored-term sums, ordinary/Neumaier gaps and the unchanged 1e-12 allowance. There is no comparison to historical receivers or historical inflows. Any R noncompletion or qualification failure invalidates the shared original-scene premise and stops all arms, regardless of whether classified as numerical or integrity.

`assessQ(R,Q,C)` requires complete R and the represented-interface Q. A valid Q domain/arithmetic failure may have incomplete records and is a numerical failure; dependent arms are skipped. Q0 failure skips A/B only; Q1 failure skips C only. An unexpected Q exception, charge failure, shape mismatch or malformed completed record is an integrity failure and stops the campaign. Both Q0/Q1 references retain their prospectively reserved opportunity even if one fails numerically. Exact per-rotor `L1(Q-R)+1e-12 <= epsilonWake`, classification equality, and Q ordinary/compensated exact-sum gaps must all pass. No epsilon rescaling or cancellation-based gate is introduced.

`assessUsefulness(R,C)` scans only complete saved R terms. All first twelve rotors (three intended-active receivers) individually require at least four terms at least `16*epsilonWake` and exact stored-term sum at least `256*epsilonWake`. These threshold products are BigInt products of the original epsilon dyadic, not a rounded floating multiplier. The last four top-control rotors have no activity threshold. Each rotor still reports positive and substantive counts and exact sum. Failure makes the scene uninformative; no replacements. The driver also requires canonical packing nonzero count = 0, translated packing nonzero count > 0, exact translation count = 15000 and exact split reconstruction count = 15000 per origin. Save all residual arrays so the extent of input-bit loss is reviewable.

`assessControls(bytes,spec,arm)` requires 20 records, 2080 bytes, and the arm's `expectedByArm`. Metadata and listed exact nonzero vector literals (`expectedNumericWords`, absolute output word indices 8–25) are checked. AB use three exact literal comparisons, C four. Reached zeros allow either sign; unreached numeric words require raw +0. Controls have no independent profile/norm magnitude oracle. Any failed control is a shared-integrity stop.

`assessGpuTerms(R,Q,bytes,C,ids)` consumes exactly 80,000 records ×26 u32 = 8,320,000 bytes. Identity, shapes, routing, known masks, finite reached fields, raw-zero unreached fields and valid status semantics are structural checks. Numeric vectors may be signed; their bounds are 257 for center components and 258 for rotor components. A malformed/unwritten main record, raw NaN/Inf in a claimed reached field, or undefined mask is an integrity failure. A correctly formed reported domain failure (status2/code3/mask258055) or a correctly formed arithmetic-failure prefix (status6, no valid term) is a local numerical failure. The allowed arithmetic masks are the actual main-path prefixes 0,28672,28673,258049,258051,258055,258127,258303,260095, with constrained policy/flag combinations. Such invalid terms never enter any exact sum or vector comparison.

A structurally valid classification mismatch is a numerical failure. Its term remains an eligible diagnostic summand; this is not qualification for reduction. Every rotor requires all 5000 terms qualified and exact `L1(T-R)+1e-12<=epsilonWake`. L1 and signed T-R/T-Q/Q-R diagnostics are kept separately. The 18 fields also report maximum absolute T-Q differences with slot witnesses. Only the overall passing term cell may consume its single reserved serial reduction on the exact existing GPU buffer.

`assessSerial(termAssessment,bytes,C,ids)` retains sixteen 32-byte records (512 bytes) and the exact gate `L1(T-R)+abs(S-exactSum(T))+1e-12 <= epsilonWake`. Identity/status/finite failures are integrity failures; a finite conservative error excess is numerical. Each passing candidate requires both origins and all required gates; no missing cell is excluded from the decision.

`compareReferences(A,B,C,label)` is diagnostic-only and uses saved arrays: R0/R1 once, Q0/Q1 within each origin twice. It reports exact per-rotor L1/signed differences, classification and mask mismatch counts, and reached-field maxima. Its `withinUnchangedEpsilon` fields are diagnostic and do not create a new acceptance rule. Incomplete reference input yields `available:false` and no term traversal. The driver may instead save a skipped-diagnostic reason without consuming this call.

`compareGpuVectors(bytesA,bytesB,label)` is diagnostic-only and uses saved, already structurally assessed buffers. It is reserved for A/B and B/C within each origin, four possible comparisons. It counts raw and numeric differences separately (signed-zero differences are not numeric differences), masks, and component maxima/witnesses. It skips domain/arithmetic failed rows. Identity/shape/nonfinite corruption still triggers integrity failure. No geometry, norms, profiles, or shader arithmetic are recomputed by either comparison.

## Work and storage

`callback-limits.json` gives per-function maximum callback amounts. Labels expand to R/Q0/Q1. Names have no implicit origin prefix: parent aggregation multiplies each invocation's limits by its call multiplicity, while individual saved results retain their own counts. Charge all complete assessor reservations before entry, including skipped short-circuit cases if called. `assessment-reservations.json` bounds returned counters; `call-reservations.json` bounds invocations. Copies are precharged before slice operations.

There are six reference traversals, 480,000 total reserved slots; each can inspect at most 19,996 centers and 79,984 nonself rotor slots, with no rerun. At most six GPU main cells and their dependent reductions are reserved. Host diagnostic traversals are separately counted and do not authorize fresh scientific recomputation.

`byte-proposal.json` inventories the full completed logical raw artifacts, including duplicate saved shared packed side fields, all states, and all reference evidence. JSON reports, source, logs and manifest are separate. Its 256 MiB aggregate saved-artifact cap is a proposal for parent acceptance, not permission to consume unbounded memory or add passes. The full completion payload may be smaller after dependent-cell skips, but skipped work is never reassigned. No test/checker/browser/science execution has validated these drafts; that limitation must remain explicit at the source freeze.
