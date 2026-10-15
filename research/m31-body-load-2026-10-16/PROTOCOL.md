# Preregistered protocol — source preparation, not yet frozen

The parent adopted [the complete body-load contract](design/ADOPTION.md) after [independent static critique](design/INDEPENDENT-CONTRACT-REVIEW.md). The [input construction](design/INDEPENDENT-INPUT-DESIGN.md) fixes the fresh test families and numerical edge schedule. No scientific result exists at this stage. The integrated source, schema, configuration and final independent review must be frozen and published, then independently retrieved and verified, before invocation.

## Purpose and scope

Test one complete ordinary-f32 browser field-to-body-load query against the specified original-state numerical model at N=50,500,5,000,5,000. The two largest families have different density, coordinate extent and support structure. All required cases must pass. They are four structured finite tests, not independent samples from a population of flights; no statistical generalization or confidence interval over flight conditions is claimed.

The candidate computes all receiver inflows, four effective rotor forces, thrust and roll/pitch/nominal-yaw moments. It includes host quaternion preparation, packing, allocation/upload, GPU field/roots/body assembly and readback, but this campaign does **not** compare speed. Excluded: Boids steering, control, dynamics/integration, world force rotation, rendering and physical validation. Static fixtures are not emergent flock behavior. Source wake strength remains isolated hover irrespective of source motors.

## Immutable sequence

1. Verify frozen files, runtime entry pins, independently verified remote source/freeze identity, empty raw directory and overnight cutoff. The external supervisor creates a permanent exclusive launch lock before starting the worker.
2. Construct one fixed set of constants and finite controls. Save original and exact packed controls. Execute explicitly reserved R/Q control references and host admission/decoder checks. Failed shared controls or reference quality stop without retry.
3. Launch the registered browser once, capture its actual adapter/default-device limits and nonfallback status, compile the three fixed entry points once, and require clean API status. No alternative backend or precision implementation is selected.
4. Execute the 15 pair controls and 146 root controls once. Save raw GPU bytes through a bounded binary loopback sink before assessment. Execute the separately reserved actual-input handoff reference for the 146 root controls. Require all shared control gates before generating a main family.
5. For each fixed family ID 1–4, generate once, save original states and permutation/input audits, then prepare/save original candidate, independent R and decoded Q interfaces. No seed search, regeneration or input substitution.
6. Evaluate one R and one Q full field/root/body pass. Save policies, outputs, counters and completed prefixes before any dependent decision. R/Q must be numerically admitted and complete. Check the prospectively fixed coordinate/motor stimulus and every designated R inflow >=.25 m/s.
7. Dispatch one complete GPU query for that family, persist both raw policy and output buffers, then execute one H scalar-root pass at actual GPU Uraw/raw nominal/decoded constants. Save H before assessment.
8. Assess every policy symbol, root record and delivered body output. Valid numerical differences that fail a gate remain failures while the other already-reserved families continue. Malformed, invalid, inconsistent or incomplete evidence, reference/control/stimulus failures, resource/API failures or timeout terminate the invocation. No fallback or rerun.
9. Close browser/device/transport resources. The external supervisor verifies Node/browser group absence, records caps and terminal state, and preserves private process ownership evidence. The result is incomplete until this closure exists.

The launch source is never modified after freeze. No process may run an omitted stage after a terminal result. A favorable result supplies finite numerical feasibility evidence only, subject to the independent saved review; it does not authorize benchmarking or erase prior failures.

## Numerical acceptance

Let m=.027 kg, g=9.81 m/s², a=.028 m and D=2sqrt(2)a. Adopt epsilonT=.005mg; epsilonM=.0005mgD for each body moment (yaw is a newly selected common engineering scale); epsilonRotor=.5 min(epsilonT/4,epsilonM/(4a)). These targets preserve agreement with the stored numerical model and are not measured physical tolerances.

For every rotor, require |GPU−R|+1e-12 N<=epsilonRotor and |GPU−H|+1e-12 N<=epsilonRotor/4. For each body thrust require |GPU−R|+1e-12 N<=epsilonT; for each body moment require |GPU−R|+1e-13 N m<=epsilonM. Evaluate these inequalities with exact dyadic representations of the saved finite floating values. The added quantities are inward comparison margins, not certified propagated reference-error bounds. Q comparisons and body recomposition are attribution diagnostics.

R/Q ordinary and same-pass compensated totals must agree within1e-10 m/s. R/Q/H roots require the independent review's finite domain, bracket, residual, identity and endpoint-consistency checks; 96 bisection iterations maximum, width<=2e-15 and absolute original-polynomial residual<=1e-12. These checks do not provide outward-rounded exact-real enclosures.

Candidate positive solves use exactly12 scaled Newton updates; identities use zero. The independently recomputed normalized residual must be <=2e-6: x³+alpha*x−1 in the low branch; x³+x/r−1 in the high branch. Positive solves require x>0, positive normal vi, and positive normal high-branch r. Low alpha zero/subnormal and final force-product zero are explicit flags, never silent identities. Raw positive-subnormal nominal/Uraw words are explicitly canonicalized only for candidate receiver arithmetic; raw values remain in Q/H and primary R comparisons. See the exact schema and source for applicability masks.

Complete terminal policy classes must agree across R/Q/GPU. Positive versus numerically-zero policy7 outcomes are separately retained but share a class. Invalid, reserved and unwritten symbols never become valid zero support. No full GPU term arrays are retained, so there is no term-L1, exact GPU-sum or isolated reduction certificate.

## Work, memory, failure and independent review

The [configuration](config.json) freezes finite operation ceilings and one300 s science envelope, 768 MiB raw evidence, 32 MiB scientific result files, 208 MiB tracked live raw GPU buffers and a sampled4 GiB sum-of-owned-process-RSS stop cap. The supervisor polls process RSS; shared pages may be counted repeatedly, and transient peaks/driver memory are not a proved global-memory bound. A failed RSS probe terminates. The worker uses a285 s cooperative deadline and30 s GPU batch deadlines including readback persistence and validation; bounded cleanup remains inside the external envelope.

Only one family is logically active at a time. Host raw arrays and transient copies are enumerated separately from browser/JavaScript overhead. Garbage collection can retain unreachable allocation pages; measured process RSS, not logical array sizes, decides the RSS stop rule. No implicit claim of immediate host-memory release is made. Every GPU batch allocates fresh zero-initialized WebGPU buffers and explicitly destroys them before its returned API snapshot. No reused output can masquerade as newly written evidence.

A separately prepared independent reviewer may read saved evidence, validate manifests/layout/coverage, recompute saved-value gates, root residuals and body assembly, and reconcile counters/resources. It may not regenerate geometry, reevaluate wake profiles, rerun root solvers or launch GPU science. Its sole invocation is bounded by120 s and32 MiB outputs. Prepare and freeze that reviewer after all scientific records and external closure are terminal; never run a final-state checker against active/incomplete closure and then retry it. A failed review remains failed, with any static diagnosis separately documented.

All attempts, incomplete stages and failures are preserved. Stop new overnight launches at2026-10-15T23:00:00Z. Publication requires privacy review; result publication requires remote commit/manifest verification. Every completed milestone includes a tested Three.js view tied to saved data, with independent-review status explicit.
