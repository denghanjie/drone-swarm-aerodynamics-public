# Static host API and implementation notes

Draft source only; `reference.cjs` has not been imported or scientifically executed during preparation. The one saved-only selection run is separately logged in selection.json. Text-editing scripts did not import this module, decode states, evaluate geometry or wake values, or compile shaders. No prior campaign is reopened.

## Driver interface

- `makeOriginalConstants()` returns the original independent-I constants plus f0, area, epsilonWake and referenceSumAllowance. Call only inside the charged future invocation. There is no constant evaluation on module load.
- `prepareOriginal(states,ids,C,charge)` returns `{nodes,offsets,ids,constants,axisMetrics}`. Nodes are5000×8f64, offsets16×4f64, IDs4u32, constants16f64 and axisMetrics5000×3f64. Axis metrics are norm, norm−1, axisZ−tiltCosine. All5000 states are admitted before rotation. All5000 axes and16 offsets are prepared exactly once. Malformed input may throw before a prepared return; retain bounded driver failure context.
- `packPrepared(P,C,charge)` returns `{prepared,constants,packed}`. `prepared` has the same five raw arrays as P, with independently decoded f32 geometry/constants stored in f64. `constants` is the decoded kernel-constant object plus the original allowance/force-scale metadata; those metadata are not recalculated from packed inputs. `packed` contains nodes40000u32, offsets64u32, ids4u32 and constants16u32. Pack includes all padding words; global decoded-axis metrics and tilt checks are charged.
- `evaluateSelected(P,C,label,charge)` returns `{label,metadata,scalars,codes,terms,ordinarySums,compensatedSums,sumValidity,complete,failure,counts}`. label must be R or Q. Every non-self source center is checked once per selected receiver; eligible pairs are evaluated in the original receiver/rotor/ascending-source order, stored by source-major ordinal. All arrays are allocated first. An unexpected domain/arithmetic/charge failure returns `complete:false`, preserved arrays, sumValidity and bounded failure context. Unvisited records retain status0/code0xffffffff and code byte255; zero placeholders without validity never count as terms. Failed preparation has no comparable complete P snapshot and may throw.
- Save all R/Q arrays, including `sumValidity` and failure metadata, before gates. An incomplete reference always fails assessment. `sumValidity=1` marks a completely traversed rotor; partial running totals can be present with validity0. The driver must stop after failed R/Q gates.
- `assessR(R,savedCodes,savedSums,C)` consumes saved80k codes and16f64 sums. Exact policy codes, original-I inflow tolerance and ordinary/Neumaier diagnostics are required.
- `assessQ(R,Q,C)` checks exact codes and exact dyadic L1 Q−R plus allowance per rotor. Ordinary/Neumaier diagnostics for both references are included.
- `assessControls(bytes,controlsJSON)` checks all16 exact expected identities/statuses/codes/masks/flags, every reached finite numeric field and raw-zero unreached payload, plus the frozen valid-zero/strict-positive/invalid-placeholder term assertion. No host control geometry or wake magnitude is evaluated.
- `assessGpuTerms(R,Q,termBytes,C,ids)` validates80k raw80-byte records; includes exact L1 and signed Q−R,T−Q,T−R certificates, exact stored-term sums, per-stage T−Q maximum absolute differences, sign/classification counts, and conservative T−R pre-reduction gate. No new geometry or wake evaluation.
- `assessSerial(termAssessment,sumBytes,C,ids)` checks16 raw32-byte reduction records and combines exact saved-term sum error with the conservative T−R L1. It does not traverse term bytes again.
- `encodeU32`, `encodeF64`, `decodeU32`, `decodeF64` use explicit little endian. No native-endian Buffer view assumption. Assessment reports contain ordinary JSON values and decimal BigInt strings, no BigInt objects or large typed arrays. Witnesses are capped at32 per report; each report retains uncapped errorCount.

## Exact gates

The declared binary64 epsilon is the evaluation of `3 * sourceInduced * 1e-7 / f0`; allowance is binary64 `1e-12`. Both are converted to exact dyadics. For each rotor:

1. Packing: `sum_j |Q_j − R_j| + allowance <= epsilon`.
2. Term pre-gate: `sum_j |T_j − R_j| + allowance <= epsilon`.
3. Final: `sum_j |T_j − R_j| + |S − exactSum(T)| + allowance <= epsilon`.

Binary64 coefficients use2^−1074 units; binary32 terms use2^−149 units and are shifted925bits for common-unit comparison. Normal words use hidden mantissa bit and exponent−1 left shift; subnormal words use their fraction. Signed zeros yield coefficient0. Certificates retain the coefficient string and exponent. Approximate display converts the leading53bits only to avoid overflowing an intermediate Number; display values never drive gates. Saved Q−R and T−Q are attribution diagnostics; the conservative final gate is direct T−R plus reduction error and allowance. There is no cancellation-benefiting total-only acceptance and no force-error composition with the prior receiver experiment.

## Charge callback names and ceilings

The callback is `charge(name,amount)`; omitted amount is1. Each counter is reserved/incremented before its operation. The following are exact maximum names/ceilings for the future host invocation, independent of earlier selection work:

| Name | Ceiling |
|---|---:|
| originalStateAdmissions | 5000 |
| originalQuaternionNorms | 5000 |
| originalAxisRotations | 5000 |
| originalOffsetRotations | 16 |
| RAxisMetrics | 5000 |
| QAxisMetrics | 5000 |
| packedFloatWords | 40080 |
| decodedNodeAdmissions | 5000 |
| decodedOffsetAdmissions | 16 |
| RPairSlots / QPairSlots | 80000 each |
| RCenterChecks / QCenterChecks | 19996 each |
| RWorldPoints / QWorldPoints | 16 each |
| RRotorVisits / QRotorVisits | 79984 each |
| RProfileEvaluations / QProfileEvaluations | 79984 each |
| RSumTermVisits / QSumTermVisits | 79984 each |

`PairSlots` is a reservation of all output slots. RotorVisits are actual eligible rotor-path visits; profile and sum counters are actual retained profile paths (including code6 or zero-valued code7). The prior saved data suggest far fewer profile paths but do not reduce ceilings or authorize branch changes. No timing/root/dynamics counter is consumed here.

The following saved-output assessment counters are returned in each report's `counts`; the driver must aggregate them into the attempt ledger. They are saved-data arithmetic, distinct from fresh model evaluation:

| Name | Aggregate ceiling per complete attempt |
|---|---:|
| savedCodeComparisons | 80000 |
| savedInflowComparisons | 16 |
| referenceSumComparisons | 48 |
| packedCodeComparisons | 80000 |
| packingDyadicTermRows | 80000 |
| controlRecordsChecked | 16 |
| numericFieldsChecked | 960192 |
| gpuTermRecordsChecked | 80000 |
| gpuDyadicTermRows | 80000 |
| gpuExactStoredTermAdds | 80000 |
| serialRecordsChecked | 16 |
| serialDyadicGates | 16 |

Each packingDyadicTermRows operation converts2 binary64 terms and updates L1/signed Q−R. Each gpuDyadicTermRows operation converts1 binary32 and2 binary64 terms, updates3 L1 and3 signed error sums, and shares the already converted term with exactStoredTermAdds. Counts identify semantic row work, not individual BigInt machine instructions. Saved-output assessments presently have no charge callback; driver should reserve each assessment's ceilings before calling if cooperative wall/operation guards must precede rather than follow it. Do not run assessment functions during static preparation.

## Static review points

R uses original matrix rotation, Math.hypot, left-associated component dot, down-before-radial branches, original near predicate, inline normalized profile, factored fade and ordinary/Neumaier source accumulation. Offsets and axes are prepared before evaluation but never normalized. The original I expression computes sqrt2−1 per profile; the same expression is evaluated once in original C and transported to Q, preserving the binary64 value for R. Q uses decoded prepared axes and offsets; it is a deliberately approximate prepared interface, with norms/tilt margins saved, not qualification of an original-quaternion GPU API. WGSL may fuse/reassociate and uses length instead of Math.hypot.

GPU masks are checked exactly by policy. Every reached field must be finite and within the shader's numeric admission envelope; unavailable payloads must be raw +0. For fades, the arithmetic envelope is the exact f32 value of1.001 (1.0010000467300415), matching the shader and avoiding a spurious binary64 1.001 threshold. Successful code7 may have numerical zero and status4; positivity is counted directly. Main fade flags are descriptive only, not compared to R/Q. Control flags are exact. For main flags, only defined bits0..3 are allowed, self/outside routing must agree with identity/class, and early returns cannot claim profile fade flags.

## Additional exact reference-sum qualification

`assessR` reuses the80k saved-code loop to accumulate exactSum(R). For each of16 rotors it requires all three gaps within the exact binary64 allowance: exactSum(R)−prior saved I ordinary sum; R ordinary−exactSum(R); R compensated−exactSum(R). The old relative reproduction tolerance remains a diagnostic gate but cannot substitute for these stricter exact gates. This qualifies the link to the stored numerical oracle, not the exact mathematical/physical wake model.

`assessQ` accumulates exactSum(R) and exactSum(Q) in its existing80k pair-comparison loop, with no new geometry. It records both exact sums and requires Q ordinary/compensated gaps from exactSum(Q) within allowance. `assessSerial` records `signedSerialTotalVsR = signedTR + signedReductionError`, whose target is exactSum(R), never uses it as a total-only gate.

Additional returned saved-arithmetic ceilings are RExactStoredTermAdds80000, RExactStoredSumGates48, packingExactStoredTermAdds160000, QExactStoredSumGates32. Machine-readable authoritative ceilings are callback-limits.json and assessment-reservations.json. Per-stage reservations precede assessment; return counts may be lower on incomplete input. Aggregate shared names across assessment stages (referenceSumComparisons48 and numericFieldsChecked960192).

## Authorized fixed-constant materialization

The coordinator explicitly authorized a separate data-independent constant encoding step. `materialize-constants.cjs` evaluates the original literal expressions without importing reference.cjs and writes the16 original f64 constant words,16 packed f32 words, exact encodings for f0/area/epsilon/allowance, generator hash and runtime version. It reads no states and performs no geometry, wake profile, root, browser, shader or GPU operation. No empirical output was seen. The first bare `node` command failed shell lookup before the script ran (exit127); its stderr/stdout remain. The generator ran successfully once using the pinned bundled Node executable; successful logs are separate. Constant binary hashes are c4277ba18f4f653b0387f9c08e9b10a8336d01b1f40920f7057b02bd728e42eb (original128B) and99a526adfee88f045932bff552acbf0f57956f4bf5e7e5c2492feb8ef1fd72ef (packed64B). The original module is still not imported or evaluated. Driver must compare actual future original/packed arrays against these frozen byte files before GPU work, and original epsilon/allowance against their exact f64 words.

Final static peer reconciliation found no blocking schema mismatch. Main term assessment now excludes every record with any validation error from all exact diagnostic sums; raw invalid records still remain in saved evidence. `completeTermCoverage` and each rotor's `qualifiedTermCount` explicitly distinguish full5000-term certificates from partial diagnostic certificates. All80000 rows must qualify for a passing report. This static tightening was made before empirical execution, without changing work ceilings, valid-path expressions, gate tolerances or source selection.

The parent adopted64MiB overall raw evidence and4MiB failure reserve. The parent's repository PROTOCOL.md is authoritative for the final cap/sequence; the smaller allocation proposal in this temporary package's BUDGET.md is superseded. Planned raw typed arrays remain exactly29366048bytes across33files.
