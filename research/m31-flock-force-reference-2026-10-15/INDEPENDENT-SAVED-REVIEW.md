# Completed independent saved-data review

**PASS: 3,067,306 checks, zero failures, one invocation.** Source freeze `89c3b14e6d59f2446d257bd106e3af4bbcb029c6`. The coordinator explicitly authorized the saved-only review after confirming the one scientific invocation was complete. No geometry, field, root solving, integration, fixture or scientific rerun occurred. No correction or retry was needed.

Checker SHA-256: `c71b25552e53e8a5f669675ee4d2b539c4b2111baad91e3845026e550fc7f10a`. Internal elapsed through result/log output: **5.250015791 s**. External launch elapsed: **5.317982083 s**, below the separate 60 s allowance (55 s internal alarm, 59 s external timeout).

Original execution artifacts: `/tmp/m31-force-verifier-runs/1792080672196313000`. External launch artifacts: `/tmp/m31-force-verifier-launches/1792080672171636000`. Full machine-readable result: `/tmp/m31-force-saved-review.json` (also retained as `/tmp/m31-force-verifier-runs/1792080672196313000/review.json`). Original prepared checker and memo, invocation arguments, stdout, stderr, runtime, and original scientific result/budget/start records are preserved. Canonical output did not previously exist.

All 12 snapshots, 28,000 poses, 112,000 rotor rows, 28,000 vehicle rows and metadata rows, 22,176,000 binary evidence bytes, all 50 raw files totaling 32,883,829 bytes, and all 432,000,000 prior classification bytes passed integrity and coverage checks. All 22 frozen source/input files match. Complete count reconciliation gives 107,972,000 independent center checks, 9,378,560 eligible ordered pairs, 37,514,240 eligible rotor visits per implementation, 491,535 support evaluations per implementation, 147,497,390 actual contributor-code inspections, and 4,822,003 independent root iterations. All 19,725 no-contributor rotor records have exact zero inflow on all three saved paths, and these are exactly the saved zero-inflow records for both ordinary paths. The 2,373,850 code-4 near-policy skips remain disclosed.

The scientific supervisor retained a single completed process: 7.878831208 s wall, 7.657548042 s driver elapsed, 8.327697 s aggregate child CPU and 344,031,232 maximum-RSS platform units. These are execution diagnostics only. Budget terminal was false at review time; closing the campaign budget is a separate coordinator action.

Every frozen pointwise comparison was rechecked. Every snapshot's 13 metric counts, maximum, first maximizing index, sequential sum-of-squares and RMS passed. Every full-population minimum, nearest-rank q50/q95 and maximum passed with all zero entries retained. Checker arithmetic tolerances remain separate from scientific gates, as described in the preserved preparation note below.

## Largest retained discrepancies across snapshots

Each maximum and each RMS below is copied from the verified saved-data report; the RMS column is the largest single-snapshot RMS, not a pooled campaign RMS. The full result preserves every snapshot's value and maximizing index.

| Metric | Largest maximum | Maximum snapshot and index | Largest snapshot RMS | RMS snapshot |
| --- | ---: | --- | ---: | --- |
| inflow | 7.5495165674510645e-14 | case-2-t-0, receiver=4606, rotor=2 | 1.3649050889718936e-15 | case-0-t-0 |
| compensated | 1.7763568394002505e-15 | case-0-t-20, receiver=221, rotor=1 | 2.3455204778826852e-16 | case-2-t-30 |
| rotorThrust | 3.6082248300317588e-16 | case-2-t-0, receiver=3140, rotor=0 | 7.5662584939262138e-18 | case-0-t-0 |
| bodyThrust | 4.9960036108132044e-16 | case-2-t-0, receiver=3140 | 1.639694545445761e-17 | case-2-t-0 |
| roll | 1.1384122811097797e-17 | case-2-t-0, receiver=931 | 5.4604887622774485e-19 | case-0-t-0 |
| pitch | 1.1140177322288558e-17 | case-2-t-0, receiver=931 | 5.1819509139939124e-19 | case-0-t-0 |
| worldForce | 4.9960036108132044e-16 | case-2-t-0, receiver=3140, component=2 | 1.3022144556263541e-17 | case-0-t-60 |
| worldForceChange | 4.9960036108132044e-16 | case-2-t-0, receiver=3140, component=2 | 1.4745914736364776e-17 | case-0-t-20 |
| worldMoment | 1.588356182691264e-17 | case-2-t-0, receiver=931, component=0 | 4.3493832652795523e-19 | case-0-t-0 |
| rootResidualPrimary | 6.6613381477509392e-16 | case-0-t-30, receiver=443, rotor=1 | 1.4602703977091185e-16 | case-1-t-60 |
| rootResidualIndependent | 4.4408920985006262e-16 | case-0-t-20, receiver=64, rotor=0 | 9.9592636715722192e-17 | case-2-t-60 |
| powerResidualPrimary | 1.1102230246251565e-16 | case-0-t-0, receiver=354, rotor=0 | 3.3186198628321333e-17 | case-2-t-20 |
| powerResidualIndependent | 1.6653345369377348e-16 | case-0-t-30, receiver=107, rotor=0 | 4.1577815215352323e-17 | case-0-t-60 |

## Verified all-vehicle prescribed-load distributions

Units are N for thrust loss and N m for absolute roll/pitch. These are prescribed-input static model outputs, not measured or reconstructed historical flight loads.

| Snapshot | Observable | N | Minimum | q50 | q95 | Maximum |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| case-0-t-0 | thrustLossN | 1000 | 0 | 0.05533218189737843 | 0.083656620007076188 | 0.094772260339583803 |
| case-0-t-0 | absoluteRollNm | 1000 | 0 | 0.0001361451060024469 | 0.00031720398852637431 | 0.0004124225806734817 |
| case-0-t-0 | absolutePitchNm | 1000 | 0 | 0.00013648844771820315 | 0.00031443936907379617 | 0.00044433583735681422 |
| case-0-t-20 | thrustLossN | 1000 | 0 | 0.017568517568781417 | 0.063564838481802777 | 0.1002779594706911 |
| case-0-t-20 | absoluteRollNm | 1000 | 0 | 4.1397968308235118e-05 | 0.00019833738784757571 | 0.00035463995830245531 |
| case-0-t-20 | absolutePitchNm | 1000 | 0 | 3.9286910179572041e-05 | 0.00022320980105960237 | 0.00052041388011314529 |
| case-0-t-30 | thrustLossN | 1000 | 0 | 0.014553174273309266 | 0.062750283544912605 | 0.10486264245062393 |
| case-0-t-30 | absoluteRollNm | 1000 | 0 | 3.3507283743855563e-05 | 0.00019098317840191351 | 0.00040993468677449191 |
| case-0-t-30 | absolutePitchNm | 1000 | 0 | 3.3710816493127179e-05 | 0.00019171810012809072 | 0.00040375509977876338 |
| case-0-t-60 | thrustLossN | 1000 | 0 | 0.012092428292166335 | 0.055157075544190165 | 0.091693100794192572 |
| case-0-t-60 | absoluteRollNm | 1000 | 0 | 3.147835503275638e-05 | 0.00019879524795318759 | 0.00041596929742649226 |
| case-0-t-60 | absolutePitchNm | 1000 | 0 | 3.1032389747598192e-05 | 0.00018693256052716234 | 0.00040428648550044303 |
| case-1-t-0 | thrustLossN | 1000 | 0 | 0.056802462516173824 | 0.083263592561185068 | 0.098150862393935834 |
| case-1-t-0 | absoluteRollNm | 1000 | 0 | 0.00013392390055758682 | 0.00031573837605414863 | 0.00041405989996917496 |
| case-1-t-0 | absolutePitchNm | 1000 | 0 | 0.000146073977906552 | 0.00031877849556922371 | 0.00040447234061733914 |
| case-1-t-20 | thrustLossN | 1000 | 0 | 0.023254050527360154 | 0.085869430559418425 | 0.12372631335986278 |
| case-1-t-20 | absoluteRollNm | 1000 | 0 | 3.9939746450190191e-05 | 0.00021179531056084687 | 0.00042624823578053784 |
| case-1-t-20 | absolutePitchNm | 1000 | 0 | 4.1048330052979864e-05 | 0.00022955145171325137 | 0.00045598331026226995 |
| case-1-t-30 | thrustLossN | 1000 | 0 | 0.02029724558589599 | 0.093219979941762787 | 0.13981808562072984 |
| case-1-t-30 | absoluteRollNm | 1000 | 0 | 3.3136926205556494e-05 | 0.00022044785724414798 | 0.00045192071178144061 |
| case-1-t-30 | absolutePitchNm | 1000 | 0 | 4.5636851436853254e-05 | 0.00027793213910753066 | 0.00053074189678816819 |
| case-1-t-60 | thrustLossN | 1000 | 0 | 0.0066731512355087674 | 0.059116999955641292 | 0.098042968317172491 |
| case-1-t-60 | absoluteRollNm | 1000 | 0 | 1.8201677428248504e-05 | 0.00017470764060430774 | 0.00036736719109899747 |
| case-1-t-60 | absolutePitchNm | 1000 | 0 | 1.9410583347137826e-05 | 0.00020829998694469254 | 0.00048984618297883125 |
| case-2-t-0 | thrustLossN | 5000 | 0 | 0.061160500031049281 | 0.084899145574734991 | 0.10021566975979257 |
| case-2-t-0 | absoluteRollNm | 5000 | 0 | 0.00014825663514156503 | 0.00032324461886281005 | 0.00043842521741908696 |
| case-2-t-0 | absolutePitchNm | 5000 | 0 | 0.00015023879563151013 | 0.00032230343971131827 | 0.00044360074456993733 |
| case-2-t-20 | thrustLossN | 5000 | 0 | 0.032355024280130068 | 0.082136589485057698 | 0.12157950833813713 |
| case-2-t-20 | absoluteRollNm | 5000 | 0 | 5.3762839960634851e-05 | 0.00023259043924456733 | 0.0005081746968324584 |
| case-2-t-20 | absolutePitchNm | 5000 | 0 | 5.4935558519188027e-05 | 0.00023898750756547616 | 0.00048516736639520335 |
| case-2-t-30 | thrustLossN | 5000 | 0 | 0.031545093168762084 | 0.085936979146193943 | 0.13990329821871711 |
| case-2-t-30 | absoluteRollNm | 5000 | 0 | 5.216870302750796e-05 | 0.00024005565751729395 | 0.0005376101804968037 |
| case-2-t-30 | absolutePitchNm | 5000 | 0 | 5.1872275471130614e-05 | 0.00023333627959615548 | 0.00048965978699493096 |
| case-2-t-60 | thrustLossN | 5000 | 0 | 0.030775405283558682 | 0.083408627481164094 | 0.12480297387548744 |
| case-2-t-60 | absoluteRollNm | 5000 | 0 | 4.9561564237782631e-05 | 0.00023223551033141852 | 0.00050954709223294064 |
| case-2-t-60 | absolutePitchNm | 5000 | 0 | 5.2977655476552218e-05 | 0.00023509466288675453 | 0.00056412678452102505 |

## Retained limitations

- The current force campaign retains code hashes, not a duplicate code vector. Every prior vector is fully decoded and matches both prior/current digests; the independent field classification itself is not regenerated.
- No world rotor positions are saved in the new binary records. Saved axis discrepancies can be recomputed, but the reported maximum geometry discrepancy also includes unsaved rotor coordinates and is checked only as retained runtime evidence within its frozen gate.
- World force and force change are cross-checked against saved axes. A single saved thrust axis does not determine roll about that axis, so world-moment rotation cannot be independently reconstructed; retained components, their cross-implementation gates and their orthogonality to the saved axis are checked.
- Quaternion norm defects and domain predicates are retained evidence tied to pinned prior rows; they are not recalculated from pose quaternions.
- Operation counters are recorded execution evidence reconciled against complete saved coverage; this review does not independently instrument the original execution.
- Binary64 root residuals and brackets are diagnostics, not formally rounded interval certificates. No roots are solved in this review.
- Passing is only finite static arithmetic qualification of prescribed inputs on selected historical poses. It is not physical validation, reconstructed historical motor loads, trajectory convergence, temporal/spatial approximation acceptance, or a speed claim.

## Original preparation note (preserved verbatim below)

The original standalone preparation memo is also preserved in the external launch archive.

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

