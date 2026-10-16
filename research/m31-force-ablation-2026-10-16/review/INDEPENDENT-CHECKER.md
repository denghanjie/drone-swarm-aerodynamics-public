# Independent saved-evidence reviewer: force/moment ablation

`review.py` is a prospective Python/NumPy reviewer for `research/m31-force-ablation-2026-10-16`. It must be included in the published source freeze before the campaign's sole candidate invocation and sole reviewer invocation. Preparation used source inspection and syntax parsing only; no candidate model, numeric reference, control or trajectory was executed or imported.

The fixed schedule is three 0.5 s offset-pair force-only controls, then six 2 s Boids repetition paths (off/full at three timesteps). Only if the first nine pass their prescribed completeness, pair identities, pair all-stage/endpoint mask, refinement and exact-reference gates may the three Boids force-only paths run. The reviewer reconstructs that decision using the initial three mask controls, then reconstructs all six mask controls if the conditional paths ran, all trial identities and the final allocation decision. Failure records do not authorize retries.

## Independent reconstruction

- Verify the source manifest, supervisor record, result pins and six immutable prior Boids pins. Check exact numerical/structural equality of the prescribed prior sample fields, excluding elapsed timing and new modeled-correction metadata. Initial states and complete final states are also compared exactly. This is stored-number equality, not floating bit-pattern identity.
- At every saved endpoint, independently rebuild geometry and classify all symbols, CSR indices and coefficients using the pinned earlier Python reference. Independently solve the descending load equations using analytic positive cubic roots, then verify loads, source/receiver consistency, residuals, admission and graph diagnostics.
- Separately reconstruct `modeledCorrections` and applied `corrections`. `forces` always means modeled rotor loads. Force-only retains their collective force but applies exactly zero added torque; nominal roll/pitch/yaw torque, gyroscopic terms, quaternion dynamics and motor lag remain in the full 17-state derivative.
- Recompute saved first/planned-last step stage states' geometry, loads, applied wrench and derivatives. Check saved-slope RK4 stage/final assembly and quaternion projection algebra. This evaluates fixed saved states; it does not integrate trajectories or create unsaved stages. Other stage records receive schedule, domain, census, residual and torque-diagnostic checks only.
- Reconstruct the six adapter controls, force-only offset-pair identities, shared-initial-state equality, and `forceOnlyMask`. Every force-only stage must report completed status and exactly zero applied added moment; endpoint applied force must equal its modeled force and applied moment must be exactly zero. Mask controls are retained even when the conditional paths are skipped.
- Recompute all five sampled discrepancy/refinement metrics: position (m), velocity (m/s), full sign-invariant orientation (rad), modeled rotor loads (nominal-hover units), and body rate (rad/s). Check all three raw Boids pairwise contrasts at every timestep. Incomplete pairs report null measurements.

Full quaternion distance includes yaw. The separate body-axis angle excludes rotation about that axis. Absolute tilt from vertical is independently recomputed at saved endpoints; the all-stage maximum remains explicitly labeled candidate-reported. These quantities are not interchangeable.

## Saved-state coverage

The output groups `savedStateCoverage` by mode and endpoint versus captured-stage record. It counts vehicle-state occurrences with body-rate norm above `1e-12` rad/s, nominal rotor-state range above `1e-12` N, both together, nominal roll/pitch torque norm above `1e-12` N m, and body rate plus nominal roll/pitch torque together. The rotor states are indices 13 through 16 of each saved 17-state vector. Counts include repeated occurrences at common endpoint/stage times; they are not counts of independent experiments. These descriptive counters establish whether nontrivial rotational/nominal-torque states were exercised without adding a new campaign gate or evaluating extra geometry.

## Tolerances and resources

Coefficient checks use `2e-12 + 2e-12*abs(reference)`; load/wrench/full-derivative checks use `1e-9 + 1e-9*abs(reference)`. Saved RK assembly uses `1e-12` absolute and relative tolerance; identity checks use `1e-12`, synthetic sign/angle controls `1e-14`. Applied force-only torque must be exactly zero. Diagnostic `acos` tilt allows `2e-6` degrees absolute near upright; this does not relax orientation convergence or identity gates.

The five frozen convergence tolerances are 0.001 m, 0.001 m/s, 0.0017453292519943296 rad, 0.001 hover units and 0.001 rad/s. Fine discrepancy must meet its tolerance and be at most 0.75 of coarse discrepancy unless both are below 1% of tolerance. These are sampled refinement checks, not rigorous error bounds or an observed-order claim when the floor rule applies.

The official wrapper permits candidate/reviewer wall times of 300/120 s and 768 MiB RSS; cooperative guards are 280/115 s. Scientific evidence, both run records/logs and review output share a 40 MiB aggregate cap. Candidate normal writes have a 32 MiB allowance with 8 MiB reserved for failure retention; supervisor logs have a 4 MiB cap. The reviewer creates its output exclusively, emits no traceback/private path, and enforces the aggregate cap again before writing. Timing is resource accounting, not a benchmark.

## Interpretation limits

The reviewer does not independently regenerate Boids initialization/commands or replay all collision checks. Unsaved integration stages are not independently recomputed. Source hashes establish provenance, not physical truth. The source-total closure, moving-pose geometry and receiver model remain provisional. The exposed seed and controller support only this deterministic within-model sensitivity comparison. Force-only is a synthetic wrench intervention, and each arm evolves its own states, commands and geometry; raw contrasts cannot be added or converted into causal percentages. No physical, stability, novelty, statistical or performance validation follows from a passing audit.

Run the reviewer only through the campaign's frozen one-use supervisor after source publication and candidate evidence creation. Its positional arguments are the campaign package directory and a new output JSON path. A direct syntax check may use `ast.parse` on the source text; do not import the reviewer to syntax-check it.
