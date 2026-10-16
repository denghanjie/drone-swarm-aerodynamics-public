# Independent saved motion-feedback reviewer

Prepared source-only on 2026-10-16 for `research/m31-motion-feedback-2026-10-16`. No target calculations, fixture evaluations, numerical-reference imports, simulations or candidate helpers were executed during construction. Only file reads and `ast.parse` syntax checks were used. These isolated files are ready for integration and source freeze; their existence grants no run permission.

After the separately authorized candidate has finished and its supervisor record is saved, the frozen invocation is:

```
python3 source/review.py PACKAGE_PATH PACKAGE_PATH/results/independent-review.json
```

The script uses Python standard library and NumPy. It imports only the preexisting independent `../m31-typed-assembly-2026-10-16/source/numeric-reference.py`, pinned to SHA-256 `4b21e84674d0007e23641622aec52724bced4791fcca3c1b97d48189c21f6aeb`. It never imports JavaScript, calls candidate helpers, reruns initialization/Boids/control, or advances trajectories.

## Checks

- Every saved endpoint from the 18 fixed primary paths, plus all six conditional Boids16 paths if independently recomputed primary gates permit them. Literal primary states and common initial states across modes/refinements are checked. No endpoint is subsampled.
- Independent complete pair symbols, sparse support/order, K and scaled a from the saved pose; independent descending coupled forces from analytic hyperbolic cubic roots; all amplitudes, rotor alpha/x/T, symbol census, graph counts, admission, residual and source-total consistency. The saved reference geometry is not taken from the candidate's witness.
- Independent total axial force and body roll/pitch torque, retained nominal yaw torque, quaternion rate, gyroscopic angular acceleration, gravity, translational acceleration and motor-lag derivatives. All 17 derivative components and each correction field are compared. The body equations are implemented here, not imported from the JavaScript physics or adapter.
- The fixed first and planned last integration steps' **saved stage states** receive independent geometry/load/derivative recomputation too. Saved stage inputs, raw quaternion normalization diagnostics and final accepted states are checked algebraically from saved slopes and `stepWitnesses`. This uses only frozen saved inputs; it does not generate an unsaved RK stage or rerun a trajectory. A failed final projection is handled separately from a rejected numeric RK stage.
- All stage attempt times/statuses, terminal rejection recording, endpoint attempt counts, held-command/sample cadence, integration and coupled-query counts, all control update times and saturation counts. Failed model-admission stage/endpoint states are independently checked where retained. Correctly recorded incomplete paths remain negative diagnostic evidence and cannot pass the primary gate.
- Six saved synthetic adapter controls, zero-effect four-metric comparisons, complete17-state zero identity and empty-CSR/unit-load identities, centered symmetry, and initial centered/offset wrench signs. Both refinements' discrepancies and every convergence/roundoff/ratio gate are recomputed. Conditional execution requires all primary gates; an independent review pass is separate from a primary scientific pass.
- Source manifest/run identity and all source/artifact pins; candidate supervisor completion, monitoring, wall/RSS/log and scientific-byte accounting; exact path schedule with no extra trial files. Descriptive fine on/off discrepancies and sampled relative rotor changes are reported without changing acceptance criteria.

Coefficient comparisons use `2e-12 + 2e-12*abs(reference)`; force, root, wrench and full derivative comparisons use `1e-9 + 1e-9*abs(reference)`. Identity and saved-slope assembly use `1e-12` absolute, with `1e-12` relative additionally for assembled state arithmetic. Symbols/support are exact. Synthetic sign/angle controls preserve their `1e-14` criterion. The reported tilt diagnostic alone allows `2e-6` degrees absolute because acos is ill-conditioned near an upright axis; this does not relax attitude convergence, state identity, forces or derivatives.

## Bounds and failure reporting

The approved external wrapper supplies the 120-second wall and 768MiB RSS bounds. This reviewer has a 115-second cooperative guard and the same RSS ceiling. It enforces a 32MiB aggregate over results/inputs/generation, including its projected output, and the candidate's 24MiB normal evidence ceiling. Output is exclusively created. If necessary, a failure report is compacted to fit; if even that cannot fit, the output failure is reported without writing an over-cap JSON. The wrapper must still account for its own final log/run record.

Output contains compact per-path summaries, discrepancy/decision results, total checks and failure names rather than every passing stage check. Exceptions print only a generic label and exception class; no traceback/private path is emitted. Invalid-domain library warnings are suppressed while finite/domain assertions remain enforced. A failed/aborted review exits nonzero and reports covered endpoint/path counts, without retry or tolerance alteration.

## Limits

Intermediate stages outside the first/last captures have saved diagnostics only: their numerical values and trajectory continuity are not independently reconstructed. Boids initialization, steering/controller commands and obstacle/contact logic remain source-provenance dependencies. The reviewer checks their saved command schedule/range and uses those commands in the independent derivative, but does not regenerate them. `minimumSweptSeparation` is explicitly labeled candidate-reported; the full set of accepted step chords is not saved, so its exact global minimum cannot be recomputed. Common0.1-second discrepancy samples do not bound between-sample error or establish integration order.

Even a passing numerical audit does not validate the provisional steady field, command-to-power interpretation, nominal yaw torque, transient wake omissions, physical flight, or browser scale/performance. Primary failure correctly closes the conditional extension. No rerun, replacement encounter, new seed or threshold adjustment follows from this reviewer.

## Source-review findings communicated before freeze

The parent has made per-path stopping explicit, replaced off-mode zero tilt with actual tilt, retained rejected stage and endpoint attempts, strengthened full-state/initial-wrench controls, captured first/last stage and accepted-step witnesses, and added finite input/derivative and final-projection records. The force correction has the correct replacement form and roll/pitch signs; nominal yaw and motor-state dynamics remain explicit assumptions. No remaining blocking adapter-formula finding was identified. This is static assurance only: target and review execution have not occurred.
