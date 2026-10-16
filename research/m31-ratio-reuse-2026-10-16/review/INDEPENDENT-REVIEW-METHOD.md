# Independent saved-evidence reviewer: 10 ms ratio reuse

`review.py` reviews `research/m31-ratio-reuse-2026-10-16`. Include it in the published source freeze before the sole candidate and reviewer invocations. Preparation used static source inspection, text editing and `ast.parse` only. No scientific module, candidate, control or reviewer was executed or imported during preparation.

The fixed allocation is three every-stage coupled repetitions, then conditional three reuse paths, at h = 0.005, 0.0025 and 0.00125 s. All use 16 vehicles, exposed seed 260201 and duration 2 s. Exact config and prior ablation pins are embedded. Full-reference sample times, states, commands, modeled rotor loads, modeled/applied corrections, derivatives, geometry witnesses and group summaries must match the prior records exactly as stored numbers/structure. Initial and complete final states are also checked; timing and new metadata are excluded. This is not floating bit-pattern proof.

## Reconstruction and event ordering

The reviewer verifies source/result/reference hashes, supervisor success, resource accounting, path order and conditional execution. Missing data, incomplete paths or globally interrupted analysis fail closed; retained candidate prefixes are not presented as a complete independent audit.

Geometry, symbols, CSR indices, coefficients, analytic positive roots, loads, source/receiver consistency and body derivatives are reconstructed independently at every full-reference saved endpoint and each reuse refresh. The 63 reuse sampled endpoints share those already checked refresh geometries and must preserve exact event source identities.

Caches must equal the saved solver `x` fields directly. Cached loads are current nominal motor thrust multiplied by held roots. World force uses the current quaternion; full roll/pitch correction, nominal yaw, gyroscopic terms, quaternion dynamics and motor lag are checked in the independent 17-state derivative.

At each positive refresh, LEFT uses the preceding cache, the instantaneous evaluation contains a fresh joint solution, and RIGHT uses its new roots on identical states and held commands. Event zero has null LEFT. Positive 100 ms samples exactly reproduce LEFT; t = 0 reproduces RIGHT. The 2 s refresh is audit-only. Every RK stage, including k4 at a boundary, keeps its interval's cache; samples add no solve. Current geometry/admission/residual fields must remain null on ordinary cached stages.

The first and last saved steps provide 24 full and 24 cached global stage captures. Stage/final assembly and quaternion projection are reconstructed algebraically from saved slopes, without reintegration. At the 24 cached captures, current geometry and, where admitted/descending-eligible, fresh loads are also reconstructed as descriptive audits. These checks cannot establish current closure or domain validity between captures.

Six inherited analytic controls are checked alongside identity roots, current-nominal scaling, cache-age rejection and nonfinite-cache rejection. Three successful synthetic cached evaluations are independently reconstructed; five rejection records are checked against frozen predicates/source. Candidate rejection code is not re-executed. These eight synthetic attempts are separate from trajectory counts.

## Separate decisions

Five maximum sampled metrics cover position (m), velocity (m/s), full sign-invariant quaternion orientation (rad), per-rotor load in nominal mg/4 units, and body rate (rad/s). Their tolerances are 0.001, 0.001, 0.0017453292519943296, 0.001 and 0.001. Adjacent-grid fine discrepancy must meet tolerance and be at most 0.75 of coarse discrepancy unless both are below 1% of tolerance. The floor rule does not establish observed order or rigorous trajectory error bounds.

The same five full/reuse approximation screens apply at ALL THREE timesteps. Positive pre-refresh errors independently compare maximum per-rotor difference divided by mg/4, collective world-force vector difference divided by mg, and roll/pitch moment vector difference divided by mgR. R = sqrt(2) * 0.028 m is the motor-arm radius. Every event threshold is 0.001 on all three paths; RIGHT/fresh errors must be at most 1e-12.

`allocationPass` covers complete paths, exact repetition, refinement and post-refresh identity. `approximationPass` additionally requires every paired trajectory and pre-refresh event-error gate. A passing independent audit can correctly report `approximationPass: false`. The reviewer reconstructs the declared decision without relaxing thresholds or treating engineering screens as physical validation.

## Counts and resources

For six complete paths, joint-query attempts are 11,263 full-reference plus 603 reuse, totaling 11,866. Reuse includes 600 propagation refreshes and three terminal audits. Trajectory cached applications total 12,403; eight synthetic attempts are separate. `evaluationAttempted` distinguishes projection failure from evaluator entry. Accepted-path checks require completed records. Attempt counts are not measured speedups or completed-root-solve counts for failed paths.

Coefficient tolerance is `2e-12 + 2e-12*abs(reference)`; load/wrench/derivative tolerance is `1e-9 + 1e-9*abs(reference)`. Saved RK assembly uses `1e-12` absolute and relative tolerance, identity checks `1e-12`, and inherited synthetic checks `1e-14`. Near-upright diagnostic tilt allows `2e-6` degrees absolute without relaxing orientation convergence. Full quaternion distance includes yaw and is not labeled tilt.

External candidate/reviewer caps are 300/120 s, cooperative guards 280/115 s and RSS 768 MiB. The 96 MiB scientific aggregate includes run records, logs and review output. Normal candidate writes have 88 MiB, reserving 8 MiB for failure evidence; logs have 4 MiB. Each trial's bulky events/stages are discarded after checking, retaining samples/summaries for comparisons. Output is exclusive, aggregate capacity is checked before writing, and failures emit no traceback/private path. External termination can prevent a final review record; supervisor evidence remains.

## Limits and execution

Initialization, controller commands, group summaries and swept-contact checks are not independently rerun. Unsaved states and ordinary cached-stage geometry remain unchecked. Source hashes establish provenance, not physical truth. The closure, receiver and moving-pose model are provisional; ratio reuse is a synthetic lagged model, not validated wake memory. One exposed seed cannot establish generalization, continuous safety, stability, physical accuracy, novelty, statistical confidence or 5,000-drone performance. Assertion counts are not independent experiments.

Run only through the frozen one-use supervisor after publication verification and candidate evidence creation. Positional arguments are the package directory and a new output JSON path. Syntax-check by parsing source with `ast.parse`, never by importing it.
