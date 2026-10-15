# Coordinate-origin static kernel contract

Status: STATIC SOURCE ONLY, uncompiled and unexecuted. The accepted three-arm/two-origin decision supplies the scope. The published wake source is preserved unchanged. This module adds identical vector instrumentation to all arms and changes only the declared position interface/displacement expression. No origin, position, attitude, wake or reference value was generated or evaluated while preparing it. New control bytes were packed from explicit u32 literals only, with no float conversion; see the retained encoder and source note.

## Cells and written arithmetic

The driver owns six immutable cells: origins0=`[0,0,0]`,1=`[64,-32,16]`, crossed with armsA/B/C. The original/decoded references, seed, receiver selection and gates belong to the host protocol. A/B share every input byte, including node positions, axes, offsets, constants and IDs. C adds position residuals only: every node's first eight words must match A/B exactly, and all other input buffers must match. The driver must retain/check those identities; the kernel cannot certify equality with another dispatch.

All signs are source minus receiver:

- A center: `highDifference=sourcePosition-receiverPosition`; center=`length(highDifference)`. Rotor displacement: `point=receiverPosition+offset`, then `sourcePosition-point`.
- B same input bytes and center calculation; rotor displacement=`centerDelta-offset`.
- C center: `highDifference=sourceHigh-receiverHigh`; `lowDifference=sourceLow-receiverLow`; `centerDelta=highDifference+lowDifference`; center=`length(centerDelta)`. Rotor displacement=`centerDelta-offset`.

C never reconstructs either absolute coordinate as one f32 high+low before subtraction. Its referenceQ1 may reconstruct semantic high+low in binary64 under the host's exact saved-encoding checks. A/B shareQ0; R/Q0/Q1 keep original oracle arithmetic. Policies, projection, source strength, profile/fade expressions, axes, offsets, constants and absolute allowances are unchanged. A's identical added instrumentation is part of this prospective baseline; it is not the previous uninstrumented binary.

These are WGSL written expressions, not a guaranteed backend operation graph. The returned center and rotor vectors are the actual values supplied to `length`, downstream dot and radial expressions. Their observation can reveal a geometric difference, but cannot prove a universal ordering/fusion guarantee. No extra materialization dispatch or host-generated pair geometry is used.

## Shared module and bindings

One shader module, seven compute pipelines: `controlsA`, `controlsB`, `controlsC`, `termsA`, `termsB`, `termsC`, `reduceMain`. All use group0 and workgroup64, with y=z=1. Each controls pipeline accesses bindings0,5,6 and launches1group. Each terms pipeline accesses0..4 and launches1250groups. Common reduction accesses3,4,7 and launches1group with16active invocations.

| Binding | Storage | Exact byte length |
|---:|---|---:|
| 0 | read constants,16u32 | 64 |
| 1 | read flat node words | A/B160,000; C240,000 |
| 2 | read offsets,16×4u32 | 256 |
| 3 | read selected IDs,4u32 | 16 |
| 4 | read_write terms,80,000×26u32 | 8,320,000 |
| 5 | read controls,20×40u32 | 3,200 |
| 6 | read_write control outputs,20×26u32 | 2,080 |
| 7 | read_write sums,16×8u32 | 512 |

The declarations contain eight storage bindings, but per-entry automatic layouts need only3/5/3. No pipeline requires all eight bindings. Use `layout:'auto'` or explicit stage-specific layouts after actual device-limit checks. A single explicit eight-binding layout would need its own supported limit and is not required. Storage buffer lengths are checked before indexed loads. Out-of-range dispatch lanes return; malformed in-range records get an explicit invalid output.

A/B node stride8words: `[px,py,pz,ax,ay,az,0,0]`.
C stride12words: `[pxHi,pyHi,pzHi,ax,ay,az,0,0,pxLo,pyLo,pzLo,0]`.
Nodes are flat u32 storage so all three term entrypoints use the same binding type. The internal Node struct has12members; A/B loaders supply literal zero residuals. Offset is`[ox,oy,oz,0]`. Numeric words are raw f32 bit patterns, never integer conversions.

All raw high/axis/low exponent and padding checks precede numeric reinterpretation. Low components must be finite and have magnitude≤2^-17 (`0.00000762939453125f`) before any geometric operation. A/B controls additionally require residual words rawzero. High position component≤128, axis component≤1.01, offset component≤0.1 retain the prior guards. Host owns original/decoded global tilt and exact semantic high+low admission. No normalization is performed. Conservative diagnostic bounds are centerDelta component≤257 and rotorDelta component≤258; all original scalar bounds remain unchanged.

Constants order remains `D,decay,spread,origin,minDownstream,neighborRadius,nearFieldRadius,downstreamFade,downstreamCutoff,radialFade,radialCutoff,tiltCosine,sourceInduced,sqrt2Minus1,0,0`. Host checks exact frozen words.

## Term record:26u32,104bytes

Words0..7 remain `ordinal,receiverID,sourceID,rotor,status,policyCode,validityMask,routingFlags`.
Words8..19 retain the prior12numeric fields: `centerNorm,down,radial,halfWidth,axisDot,projection,normalizedDown,xi,normalizedSpeed,fadeDown,fadeRadial,term`.
Words20..22 append `centerDeltaX,centerDeltaY,centerDeltaZ`.
Words23..25 append `rotorDeltaX,rotorDeltaY,rotorDeltaZ`.
All18numeric fields are raw f32 words. Bitk of validity corresponds exactly to word8+k. Thus bit11 is term, bits12..14 centerDelta (`0x7000`), bits15..17 rotorDelta (`0x38000`). No padding or vec3 members occur in the storage record.

Ordinal remains `((selectionIndex*5000+sourceID)*4+rotor)`. Origin and arm are deliberately not packed into these eight identity words: the immutable cell descriptor, exact pipeline entrypoint, input-buffer hashes and unique output file identity must bind them externally. The driver must never compare or reduce a buffer under another cell's identity.

Self returns before vectors; both vector masks remain clear and all six placeholders are raw+0. Every non-self eligible raw record that reaches center evaluation records the centerDelta triad, even if the center is outside support. Only center-admitted records reach rotorDelta. Each triad is stored/marked only after all three components pass finite/range checks. A later invalid operation preserves earlier reached diagnostics but clears term validity. Invalid/unreached numeric payloads are raw+0, never apparent model zeros or summands. Reached zeros may carry either numerical signed-zero encoding.

| Main path | Policy | Status | Exact mask |
|---|---:|---:|---:|
| self | 0 | 3 | 2048 |
| outside center | 0 | 3 | 30721 |
| downstream≤0 / cutoff | 1 / 2 | 3 | 260099 |
| near-domain invalid | 3 | 2 | 258055 |
| near policy skip | 4 | 3 | 260103 |
| radial cutoff | 5 | 3 | 260175 |
| complete profile | 6 / 7 | 4 / 5 | 262143 |

Statuses retain0unwritten,1malformed,2domain-invalid,3validearlyzero,4evaluatedzero,5positiveprofile,6arithmetic-invalid. Policy unset=`0xffffffff`. Flags retain self1,outside2,downfade4,radialfade8,control16,preparedcontrol32. Main fade flags describe reached regions and are not independent R/Q classification gates. Policy code7 with numerical zero is status4, not an error. An invalid near-domain tuple never becomes a valid zero.

## Controls: original16 plus4residual cases

One shared20record input buffer is dispatched once through each compiled arm, before the six cells. The reused control output buffer needs STORAGE|COPY_SRC|COPY_DST; the driver clears its2,080bytes before each arm dispatch so a missing write cannot inherit a previous arm's valid status. These three clears total6,240bytes and are GPU clear operations, not uploads or compute dispatches. No per-origin repeat is needed. The first32words of original controls0..15 remain byte-for-byte identical. All controls now append8words: sourceLow.xyz,0,receiverLow.xyz,0, yielding160bytes each. The scalar synthetic interface, high positions, axes and offset fields are unchanged. Scalar controls intentionally have no vector validity; they do not reconstruct geometry.

Controls0..11 retain scalar policy/profile cases;14 retains scalar padding rejection. Prepared12 retains near-domain rejection,13 raw high-NaN rejection,15 outside-center zero. Prepared12now records both vector triads;15 records center only.

New16: raw source-low quietNaN; all arms malformed before reinterpretation.
New17: nonzero source-low padding; all arms malformed before reinterpretation.
New18: finite residual literalword`0x3c23d70a`, magnitude above2^-17; A/B reject reserved nonzero low words raw, C rejects numeric residual bounds before geometry. All malformed, mask0.
New19: source high`[4,0,0]`, source low`[2^-20,0,0]`, receiver high/low zero, axes+z, offset0. A/B explicitly malformed because low words are reserved. C returns outside-center valid zero, center vector reached. The nonzero center x component has exact literalword`0x40800002`; no center-norm magnitude or wake-profile magnitude is prescribed.

`controls.json` uses `expectedByArm.A/B/C`. `expectedNumericWords` keys are absolute record-word indices8..25. Only nonzero exact dyadic vector components are compared as rawwords: control12words22/25=`0x3d800000`;15word20=`0x40800000`;C19word20=`0x40800002`. Reached zero components are not constrained to a sign bit. All unreached components remain required rawzero. Other assertions retain exact metadata and validzero/invalidplaceholder/strict-positive term sign only. No host positive-control profile evaluation is authorized by these controls.

Static control reservations per arm:13synthetic records (one malformed padding record),7prepared-kind records;4scalar profile calls maximum. Across three arms:60output slots,39synthetic-record reservations,21prepared-kind reservations,12scalar profile calls maximum. Statically expected finite prepared geometry paths are2forA,2forB,3forC; control18C rejects before geometry. These are source-derived expectations, not observed counts.

## Retained-term reduction and stop ownership

Reduction record remains32bytes: `selectionIndex,receiverID,rotor,status,validityMask,termCount,sumBits,firstBadSlot`. Success status2/mask1/count5000/sentinel`0xffffffff`; invalid status1/mask0/rawzero sum with accepted-prefix count and firstbad slot when known. Each active invocation visits sourceIDs0..4999 once in ascending order. It validates identity/status, finite/nonnegative term, exact augmented path masks and finite/ranged or rawzero vector payloads before addition. Invalid zero payloads never become summands. It never recomputes a center, profile or source term.

The host must save/qualify one cell's complete materialized term buffer before deciding reduction. Only a cell passing its exact unchanged term gate and all prerequisites may dispatch reduction, on that exact retained GPU binding4 buffer; no CPU reupload or new term dispatch is allowed. A numeric failure may end that cell while predeclared independent cells continue. A shared-premise/API/device/budget failure obeys the parent's stop rules. No retry, fallback or origin/receiver replacement is implied. After an explicit `finishCell` decision, dependent GPU buffers may be released; later cells need their own provenance and output identities.

## Bounded work and bytes

At most3control+6term+6reduction=15dispatches,7pipeline creations,7,509workgroups,480,576launched lanes. Active outputs are60controls+480,000terms+96sums; padding lanes132controls+288sums=420. Maximum serial stored-term visits480,000. Failed/skipped cells lower actual work; they do not authorize replacement work. Resource counts do not establish elapsed-time speed.

Complete retained GPU outputs:49,920,000term bytes+6,240control bytes+3,072sum bytes=49,929,312bytes. Inputs, hostreferences, exact-encoding audits, JSON/provenance and review outputs are additional and require the parent's campaign ledger.

The actual sequential driver plan uploads a node buffer, offsets and IDs for each cell:4×160,000+2×240,000=1,120,000node bytes;6×256=1,536offset bytes;6×16=96ID bytes. Once-shared64constant+3,200control bytes bring total input uploads to1,124,896bytes. A/B same-origin inputs must still compare byte-for-byte equal even though uploaded separately. New term/sum buffers begin zero/unwritten; reused control output is explicitly cleared as above. No output initialization upload is added. If the driver changes physical reuse or adds a sentinel upload, update the authoritative parent ledger before freeze.

With controls released before cells and only one cell resident, main persistent buffers including the512byte sum output are8,480,848bytesA/B and8,560,848bytesC. One8,320,000byte term readback makes16,800,848/16,880,848bytes. Controls with one reusable2,080byte output plus one2,080byte readback need7,424bytes including constants/input. These are explicit buffer payloads; allocator overhead, host copies, array decodes, API/runtime memory and queue-internal staging are not bounded by these numbers. Parent owns final physical ownership/peak ledger and any additional simultaneous buffers.
