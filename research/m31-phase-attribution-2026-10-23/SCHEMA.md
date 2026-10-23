# Output contract

Source `analyze.py` defines exact field names/order-independent JSON contract; rows order must match query order. Times are canonical finite decimal strings. Shared canonical JSON sorts keys and appends one newline; output identity is exact bytes. No numeric-time rounding. Ratios are numerator/denominator strings.

results/rows.jsonl:34,560 records. call/window/index/rep/method/status/reason; outerMs/innerMs; original phasesMs; kernelPhasesMs dict or null; disjoint leavesMs; encodePersistMs/comparisonMs. Success leaves have input,kernelInput,kernelIndex,geometry,kernelAdmission,buildUnassigned,schedule,solve,residual,loads,consumption,finalization,outerBoundary,timerResidual. Refused leaves have input,unfinishedPhaseAndFinalization,outerBoundary,timerResidual.

results/summary.json: complete/nativeCalls/calls/stages/arithmetic; pooled (bucket/method/status), perRep (rep/method/status), byWindowRep (rep/window/method/status) arrays sorted lexicographically by those keys. Each aggregate has count, outerMs, innerMs, encodePersistMs, comparisonMs, leavesMs. No empty aggregate record is emitted. groupReconciliation has216records in original group order with F then C, rep/window/method/resetMs/loggedTotalMs/signedDeltasMs. Decision: largestComponent,numeratorMs,denominatorMs,sameWinnerReps,perRepWinners,atLeastHalf,stableMajority,classification,interpretation. oldResult is the prior summary copied unchanged as parsed JSON; sourceCommit,scope,readEvents accompany it.

results/viewer-rows.json:1,920records sorted window/index, each with window,index,status,methods:F/C objects containing outerMs,innerMs,leavesMs from measured repetition0. These are illustrative recorded samples; headline uses all measured successful baseline calls. Refused rows have no geometry field.

results/input-binding.json pins all config.inputs and current sourceCommit, nativeCalls0. Producer launch/exit/failure and supervisor retain administrative evidence.

Audit output `audit/audit.json` must contain passed=true only after all checks, calls34560,stages1920,nativeCalls0, filePins for rows/summary/viewer/input-binding, viewerRowsPin, sourceCommit, readEvents, independentArithmetic, limitations. Auditor may add evidence fields. Each filePin uses file relative to this checkpoint, bytes,sha256. `audit/viewer-rows.json` must independently reconstruct and byte-match results/viewer-rows.json, with its own pin. Finalizer consumes these explicit fields. Any mismatch fails; no source edits/rerun after freeze.
