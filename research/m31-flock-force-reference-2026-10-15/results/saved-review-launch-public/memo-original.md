# Prepared saved-data review — not yet executed

This verifier is prepared for source freeze `89c3b14e6d59f2446d257bd106e3af4bbcb029c6`, campaign `research/m31-flock-force-reference-2026-10-15` in `<REPOSITORY_ROOT>`. Preparation writes only this memo and `/tmp/m31-force-saved-review.py`; it does not run any campaign source or the verifier. The final config, schema, driver, independent scalar helpers, supervisor, freeze and static-review note were read as text. The frozen 22-file manifest SHA-256 is `c6c6c91dbde3e342da355474d60f5bd2b81316c8c31cefe4a87777fa21c5456a`.

Execution requires the coordinator's explicit confirmation that the sole scientific invocation completed and separate authorization for one saved-data-only run of at most 60 seconds. No geometry, field, fixture, new root solving, integration or scientific rerun is permitted. This script imports only Python standard-library modules and never imports or executes the campaign's JavaScript.

## Verification coverage

- Verify frozen files, pinned input metadata/binary and all selected byte slices; retain all 12 case-major primary snapshots, 28,000 poses, 112,000 rotor records, 28,000 vehicle records and metadata rows.
- Verify the exact 16/35 Float64LE column schema and 22,176,000 scientific binary bytes; hash all 50 raw files and reconcile raw bytes with the one-shot supervisor.
- Verify every prior receiver file against the pinned domain manifest. Strictly inflate every 4N-byte classification vector, verify both old and new digests, all eight counts, self entries, eligibility groups, per-receiver counts and complete prior domain constraints. No classification geometry is recreated. Recover the precise early-breaking contributor-inspection count from retained code bytes, including code 6 and code 7, and enforce exact zero inflows where no contributor exists.
- Recheck every frozen scientific finite/range, exact zero-input, inflow/compensation, thrust, body moment, world force, world-force-change, world moment, residual, independent bracket/iteration and ideal-power gate. No mean-based rescue and no adjustment to scientific tolerances.
- Independently recompute saved rotor normalization, alpha, cubic residuals, ideal power, total thrust, signed roll/pitch wrench and deltaT. Model yaw remains zero. Check world force and force change using the saved axes, without rebuilding a rotation.
- Rebuild all 13 discrepancy metrics, including worldForceChange, with sequential sum-of-squares, maximum/RMS and the first maximizing index. Rebuild full-population nearest-rank q50/q95/min/max thrust-loss and absolute roll/pitch distributions including zeros.
- Reconcile all field/receiver/center/eligible-visit/support counters and caps. Record CPU/RSS as diagnostics only, with no memory acceptance threshold or timing comparison.

## Checker arithmetic and retained power baseline

The checker uses absolute `2e-16` plus relative `8e-15` only for independently recomputed scalar arithmetic and saved-axis relations. Cubic-residual reconstruction and rounded bracket endpoint consistency allow absolute `4e-15` for checker arithmetic. Summary arithmetic uses relative `5e-13`, with absolute floors `1e-30` for maxima/RMS and `1e-55` for sum-of-squares. These are checker tolerances, separately declared in the output; none is added to a scientific gate.

Each implementation's exact original nominal-power value is recovered from the first retained rotor with exact zero inflow and exact nominal thrust. All other zero-inflow powers must match that retained baseline. The baseline is also checked against the scalar ideal-power formula. Power-discrepancy statistics then use the retained baseline, so maximizing-index ties are not changed by a different Python square-root rounding. Every power identity is separately checked against both the retained baseline and the independently computed nominal formula using the unchanged scientific tolerance. No root is recomputed.

## Evidence limits

The new campaign retains code hashes; complete vectors remain in the pinned prior checkpoint. This verifies their byte identity and accounting, not the absent new vector through fresh calculation. Runtime geometry maxima include unsaved rotor coordinates; only the saved-axis contribution to that maximum can be recomputed. World-moment rotation cannot be reconstructed from the thrust axis alone; the checker verifies saved components, cross-implementation gates and orthogonality to the saved axis. Quaternion norm defects are compared to pinned retained records, without recomputing quaternion geometry. Counters remain reconciled saved execution evidence, not a second instrumentation run. Root brackets are binary64 diagnostics, not formal interval certificates. A pass establishes only this finite static prescribed-input arithmetic comparison, not physical validity, historical motor loads, trajectory refinement, approximation acceptance, or speed.

## Once authorized: preservation and bounded launch

The coordinator must create a fresh `/tmp/m31-force-verifier-launches/<time_ns>/` directory, preserve the current checker and this memo there, and write exact launch arguments before invoking the checker once. Use `subprocess.run` with `timeout=59`, writing stdout and stderr directly to exclusive files in that directory. Preserve exit code or timeout exception and elapsed time in a launcher result JSON even if the checker cannot start or has a syntax/runtime error. Suggested argument vector:

```
[python_executable, '/tmp/m31-force-saved-review.py',
 '<REPOSITORY_ROOT>',
 '--authorized-after-science']
```

The checker independently creates `/tmp/m31-force-verifier-runs/<time_ns>/`, snapshots itself and the original scientific result/budget/start files, and uses a 55-second internal alarm. It retains checker source, stdout, stderr, review result, runtime and traceback/exception information. The canonical `/tmp/m31-force-saved-review.json` uses exclusive creation and never overwrites an older result. No scientific source, input or raw file is written.

If any checker issue occurs, preserve the entire original launch/run directories and original canonical result. Do not silently patch and rerun. Report the concrete issue and obtain separate recorded correction justification and execution authorization; scientific gates and evidence remain immutable.
