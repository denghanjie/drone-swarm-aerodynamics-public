# Static WGSL/host contract

Draft 2026-10-16; not compiled or executed. `controls.u32` was materialized by packing literal floats/u32 words only, using the retained `materialize-controls.py`. No geometry, wake, root or shader value was evaluated. The published receiver review is a prior component result, not qualification of this kernel. Independent static review is required before freeze.

## Bindings and entry points

One module, group0, all storage buffers. Inputs use `read`; outputs use `read_write`. All three entry points have `@workgroup_size(64)`; y=z=1.

| Binding | Name | Exact byte size / layout |
|---:|---|---|
| 0 | constants | 64; sixteen u32 words |
| 1 | nodes | 160,000; 5,000×32-byte records |
| 2 | offsets | 256; sixteen×16-byte records |
| 3 | selectedIDs | 16; four u32 IDs |
| 4 | terms | 6,400,000; 80,000×80-byte records |
| 5 | controls | 2,048; sixteen×128-byte records |
| 6 | controlOutputs | 1,280; sixteen×80-byte records |
| 7 | sums | 512; sixteen×32-byte records |

`termsMain` accesses bindings0–4; launch1250groups. `controlsMain` accesses0,5,6; launch1group. `reduceMain` accesses3,4,7; launch1group with16 active invocations. `layout:'auto'` can create the appropriate layout per entry; alternatively use one explicit eight-storage-binding layout after checking the actual device limit. Shader sources do not invoke an API or control launch ordering.

The driver must retain binding4's original GPU storage through term readback and host qualification, then bind that same buffer for reduction. Never replace it with a CPU reupload. Its usages need STORAGE|COPY_SRC; a readback buffer uses MAP_READ|COPY_DST. If the host chooses an explicit initialization sentinel, account for COPY_DST/upload separately. Raw zero status0 is already unwritten/invalid, never a valid term. The shader writes every in-range slot, including failures.

The source-major index is `ordinal=((selectionIndex*5000+sourceID)*4+rotor)`. selectedIDs are unique integers in[0,4999]; rotor order0..3 is the independent-I order. Offsets are `offsets[4*selectionIndex+rotor]`. Source node index is sourceID; receiving node index is selectedIDs[selectionIndex]. Shader bounds checks reject wrong buffer record counts or IDs without out-of-range reads.

## Inputs

Node eight words: px,py,pz,ax,ay,az,0,0. Offset four words: ox,oy,oz,0. Numeric words are raw binary32 encodings, not numeric u32-to-float conversions. All raw exponent masks and padding checks precede any float reinterpretation for the relevant record. Original and decoded host admission owns finite states, original quaternion norm and global tilt checks on every source/receiver; the shader does not claim a whole-fleet tilt check.

Finite prepared bounds: absolute position component<=128; absolute axis component<=1.01; absolute offset component<=0.1. No axis normalization or coordinate recentering. These approximate-axis inputs do not make radial an exact perpendicular distance and do not qualify the original quaternion API.

Constants words0–13 are raw f32 encodings in this exact order:

`D,decay,spread,origin,minDownstream,neighborRadius,nearFieldRadius,downstreamFade,downstreamCutoff,radialFade,radialCutoff,tiltCosine,sourceInduced,sqrt2Minus1`.

Words14–15 are zero. Host checks every frozen constant word exactly. Shader additionally checks finite bits and bounded ranges/exact policy constants before division. Source-induced speed is the independent-I source expression; it is not silently imported from the receiver experiment. The tilt constant is transported/provenance-checked but its admission is host-owned.

## Term/control output: twenty u32 words, 80 bytes

| Word | Field |
|---:|---|
| 0–3 | ordinal,receiverID,sourceID,rotor |
| 4–7 | status,policyCode,validityMask,routingFlags |
| 8–19 | centerNormBits,downBits,radialBits,halfWidthBits,axisDotBits,projectionBits,normalizedDownBits,xiBits,normalizedSpeedBits,fadeDownBits,fadeRadialBits,termBits |

The twelve numeric fields are raw f32 words. Validity bit0 maps word8, through bit11 mapping word19. All unavailable numeric words are0 with their bit clear. A zero payload with term bit11 clear is **not a summand**. Typed identity/status must remain integer data.

Statuses:0unwritten;1malformed input/shape/padding/contract;2model-domain invalid;3valid early zero;4profile evaluated with numerical zero;5profile evaluated with positive term;6arithmetic invalid. policyCode is the independent-I code0..7. Before classification it is0xffffffff; an arithmetic failure can preserve the last established code and valid diagnostics. Status6 never retains term validity. A reducer may accept only statuses3,4,5 with valid term bits, valid identities and finite nonnegative term words.

Policy codes:0self/outside-center;1down<=0;2down>=cutoff;3near-domain invalid;4near-policy skip;5radial cutoff;6retained zero projection;7retained positive projection. Code7 can have status4: a profile/fade calculation may produce numerical zero despite positive projection. No invalid near-domain tuple is converted to code4 or a valid zero.

Routing flags:bit0self,bit1outside-center,bit2down-fade-region,bit3radial-fade-region,bit4control,bit5full-prepared-control. Fade flags are descriptive evaluated-region labels, not independent-I code equality gates. They are only set when the profile stage reaches the corresponding argument. Control expected flags are exact because their inputs are frozen.

Common validity masks: self2048; outside2049; downstream exit2051; near-domain invalid7; near skip2055; radial cutoff2127; full profile4095. These are reached-stage masks, not assertions that uncomputed fields are zero in the model.

## Reduction output: eight u32 words, 32 bytes

`selectionIndex,receiverID,rotor,status,validityMask,termCount,sumBits,firstBadSlot`.

status0unwritten,1invalid,2complete-valid. Only bit0 is defined, meaning sumBits is valid. Success has termCount5000, firstBadSlot0xffffffff and finite nonnegative raw f32 sumBits. Failure retains the number of preceding accepted terms and first bad slot if known; sum validity is clear and sumBits0. One invocation reads source IDs0..4999 in ascending order from the materialized term records. No root solve, profile recomputation, parallel tree or extra term dispatch occurs.

## Shared controls

`controls.json` contains exact32 input words and expected outputs per record. All expected checks are exact identity/status/code/validity/routing and zero-placeholder/valid-zero/positive-sign assertions; there is no host control wake evaluation or positive-term magnitude tolerance. Quantitative term accuracy is assessed on the main slice.

Input32words: id,kind,selfFlag,0; eight scalar words centerNorm,down,radial,halfWidth,axisDot,normalizedDown,xi,radialRatio; sourcePos.xyz,0; receiverPos.xyz,0; sourceAxis.xyz,0; receiverAxis.xyz,0; offset.xyz,0. kind0 uses the synthetic scalar policy/profile interface and requires all unused prepared-geometry words zero. kind1 uses the complete prepared geometry and requires all eight unused scalar words zero. All padding is zero, IDs equal their buffer ordinal, selfFlag is0or1. The frozen malformed controls deliberately violate a raw exponent/padding rule.

Scalar controls share the exact staged composite decision helper and final factored-profile helper with normal terms. Their supplied quantities need not be jointly realizable geometry. In particular record11 supplies a radial-fade endpoint3 while its policy scalars admit support: it tests profile-evaluated valid zero without zero source strength. It does not claim to be a physical pose. Projection0/negative records are synthetic and outside the valid unit-axis tilt geometry.

Records12and15 use the full prepared-geometry path for near-domain rejection and outside-center zero. Record13 is a raw-NaN input guard and must return before any float reinterpretation. Record14 is a padding guard. None of these controls normalizes an axis or repairs an input.

Sixteen controls reserve13 synthetic scalar-helper records, two complete finite prepared-geometry records and one raw-invalid prepared record. Four scalar controls reach the profile helper (8–11). The invalid raw record performs zero geometry. These counts are reservations/expected paths, not observations from a run.

## Source correspondence and bounds

The port uses the independent-I grouping: left-associated explicit component dot; down<minDownstream*D as the near predicate; normalizedDown=down/D; halfWidth=spread*(normalizedDown-origin)*D; xi=(radial/D)/(spread*(normalizedDown-origin)); denominator=1+sqrt2Minus1*xi*xi; speed=(decay/(normalizedDown-origin))/(denominator*denominator); and factored fade(1-t)*(1-t)*(1+2*t). It does not call a normalizedWake helper with an additional normalizedDown>=minDownstream rejection. Norms use WGSL length, an explicit numerical difference from host Math.hypot. WGSL can legally fuse/reassociate; this is written-expression correspondence, not a strict IEEE execution claim.

Raw constant/pair checks establish bounded operands before arithmetic. Positions/offsets bound subtraction and squared norms far below f32 overflow. The early center and downstream exits precede radial/profile work. Positive D/spread and negative origin keep normalized-distance and profile denominators away from zero; fade denominator gaps are fixed0.5and1. Numeric stage checks reject unexpected results, never clamp them. `max(0,dot)` is the model's stated projection policy, not an error repair. No physics or performance claim follows.

The final source note must report exact hashes and any static corrections. Do not compile, preview or execute this draft before independent review and the coordinator's completed freeze/publication process.
