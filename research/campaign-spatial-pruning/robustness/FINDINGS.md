# Independent robustness review

## Current decision

The fade-aware candidate v1 passes the independent sampled finite-model numerical and physical-domain-preservation checks for its declared nonempty input scope, but **fails the useful pruning-speed gate**. Stop scaling this candidate. The separately measured exact implementation optimization is promising only relative to the inherited baseline. Physical validity remains unestablished. Replay data identity and syntax pass; rendering and interaction QA remain blocked.

Frozen candidate SHA-256: `1d9e1afcf9983b900034b7b586c4ffd02ec4b3242c467f8e684fbdda1850d562`. Pinned original repository commit: `c591ce2b195fa01b895d4ba881a44a4b92fdd703`.

## Numerical coverage and findings

The independent scalar oracle evaluates all ordered pairs with the exact declared support and the same rotor positions, wake geometry, source strength, cosine factor, fades and receiver law. It uses no spatial grid. Tests preserve all four rotor samples and derive total force plus roll/pitch moment separately.

- 44 fixtures: 40 valid nonempty states, three expected physical-domain exits, and one empty-array interface test.
- Zero-budget grid and brute implementations agree with the independent all-pairs oracle to at most **1.7764e-15 m/s** per rotor. The legacy implementation also agrees on these fixtures.
- At epsilon **0.04 m/s**, maximum per-rotor inflow error is **0.02414251 m/s**, force error is **0.027827% of vehicle weight**, and roll/pitch moment-vector error is **0.039353% of weight × arm distance**. These are below the frozen 0.5% and 0.75% engineering tolerances.
- No recorded accumulated-bound violation, hidden near-wake/tilt exit, or input-state mutation.
- Exact permutation and translation tests pass. Positive-budget reversed-order results remain within their own exact-reference budgets; approximate permutation invariance is not assumed for greedy source-order omission.
- Pruning is limited in this matrix: epsilon 0.002 omits no pairs; epsilon 0.01 omits three positive-bound pairs but does not measurably change fields; epsilon 0.04 omits eleven pairs. A count of skipped exact-zero-support pairs must not be credited as approximate omission.

Fixtures include axial and radial cutoff equality/epsilon crossings, asymmetric rotor-edge inclusion, vertical pairs, 20-degree tilt boundaries, a near-wake failure, many weak sources, fixed-density growth, fixed-volume density growth, and matched dense/sparse N. The 24/64-source rings deliberately overlap emitters and are labeled software stress tests rather than plausible flights. Their purpose is accumulation and domain logic.

Primary records: `raw/candidate_smoke_checks.json`, `raw/candidate_checks.json`, `fixture_manifest.json`; reproduction: `node checks.cjs` or, after the functional-matrix gate, `node checks.cjs --full`.

### Explicitly post-baseline accumulation extension

After observing that the initial many-source fixtures activated little omission, six additional 24-source ring fixtures were constructed near axial/radial fades. This is an adversarial coverage extension, not untouched evaluation or tuning: candidate source and all thresholds remained frozen, and every tried configuration is retained in `raw/accumulation_probe.json`.

For the 2.1 m downstream / 2.85 half-width ring, each individual source-to-rotor contribution is at most **0.021043 m/s**, while the aggregate is **0.16643 m/s**. A naive independent 0.04 m/s per-pair cutoff could remove all of it. The accumulated-budget candidate removes only one pair and remains within its 0.04 m/s receiver budget.

All six extension cases pass accumulated inflow and force/moment gates. Worst force and moment errors in this extension are **0.057686% of weight** and **0.057665% of weight × arm**, respectively. Those are the larger independent worst cases when combining this extension with the original matrix. Greedy source-order omission can create a small roll/pitch moment in a perfectly symmetric reference; force error alone would miss that effect. It is measured and remains inside the declared moment gate. Other cases exercise partial omission of 3, 9 and 21 sources and full omission of 24 sufficiently weak sources.

## Preserved development failure

The initial bound omitted fade factors, making every positive bound exceed **0.048789 m/s**. No proposed epsilon could prune a positive-bound pair. This was identified before timing, reported, and corrected by a documented conservative fade-aware bound amendment without changing the planned epsilon/error thresholds. The original candidate and diagnosis remain preserved in the implementation's version archive .

A preliminary run loaded a changing source file and was excluded from frozen evidence. Subsequent checks verify identical before/after source hashes. Only frozen records are included here.

## API limitations, separate from aerodynamic approximation

- Legacy fields silently return zeros for a NaN position and can hang for an Infinity position; the latter was stopped by a one-second isolated-process timeout. Legacy also accepts a zero/nonunit quaternion and truncated state in this field-only interface.
- Candidate rejects those malformed geometry inputs. This is input validation, not an aerodynamic accuracy benefit.
- Candidate rejects an empty state list while the legacy function returns empty winds. This is an explicit nonempty API restriction and does not compromise valid nonempty field comparisons.
- The field function does not depend on nominal motor thrust and accepts negative stored thrust in both implementations. Candidate load helpers separately reject negative motor thrust. Do not advertise universal state validation from the field function alone.

Complete malformed fixtures are saved in `raw/invalid_inputs.json` with explicitly tagged nonfinite values rather than misleading JSON nulls.

## Cost and visualization status

The independent timing plan and runner are frozen in `timing_config.json` and `timing.cjs`. They separate same-equation optimization from positive-budget pruning and compare fixed work, never early-stop run totals.

The exclusive run started **14:22:30 UTC** and ended **14:22:54 UTC** on 2026-10-12, taking 24.002 seconds. Candidate source hashes match. It covered seven prescribed static scenarios at N=8/100/200, with dense, moderate and zero-neighbor sparse layouts; 9 seeded, interleaved repetitions per method; 252 individual timing samples. Fixture generation and serialization were excluded. The core includes field preparation, guards, spatial index, all four receiver-rotor queries and a lightweight returned-field checksum. No graphics were running as part of the benchmark.

- **0/14 positive-budget comparisons pass the frozen useful-speed criterion.**
- Epsilon 0.04 paired median time ratios versus the bound-paying zero-budget method range from **0.9766 to 1.0263**. Every corresponding paired 95% bootstrap interval crosses 1.0. No reliable pruning gain is demonstrated.
- At dense N=100, median field times are legacy **5.171 ms**, exact **2.986 ms**, epsilon 0.04 **2.903 ms**. At dense N=200 they are **17.784 ms**, **10.169 ms**, and **10.134 ms** respectively.
- The approximately **42–43% same-equation improvement relative to legacy** in those dense cases includes scalar/allocation work and exact-zero-support culling. It is not evidence for omission. The bound-paying exact comparator is not claimed to be the fastest possible exact implementation.
- Zero-neighbor sparse cases remain dominated by index/query/validation overhead and show no pruning benefit. Small N also shows no useful pruning win. Density and N are independently varied, so this is not a claim derived solely from expanding the volume.
- Process memory snapshots and resource usage are recorded, but they do not precisely attribute allocations or peak memory to a method. No GPU, low-end-hardware, 5,000-agent, real-time closed-loop or FPS claim follows.

Raw ordered samples: `raw/independent_timing.json`; exact state arrays: `raw/timing_fixtures.json`. Reproduction requires an exclusive exclusive serial slot and `timeout 120s node timing.cjs --serial-slot`.

The offline viewer was statically checked against its actual source records. All 12 embedded JSON documents match current retained raw data. Each of the eight Boids runs has 51 saved frames, 16 full 17-component drone states and four held rotor inflows per drone per frame; all span exactly 0–1 s and use the frozen candidate hash. Every run's index configuration matches its embedded raw record. Both inline JavaScript scripts pass Node syntax checks, no external script src remains, and labels state saved states, the one-second limitation, unvalidated physics and no demonstrated useful pruning-speed win.

**Rendering, visual appearance, controls, mobile layout and network-disabled file opening were not verified.** Cloud-browser localhost navigation returned `ERR_CONNECTION_REFUSED`. The same-process installed Chromium attempt then aborted with `socket() failed: Operation not permitted`. Browser sandboxing remained enabled; no permission escalation or security relaxation was attempted. No screenshots or interaction claims are available. Static verification is not a substitute for this missing QA.

Static data/syntax evidence is in `raw/viewer_qa/offline_static.json`. The exact tested HTML hash is recorded there; if the viewer is rebuilt, repeat the static check. These are eight one-second diagnostics, not completed missions or a cure for prior long-horizon refinement failures. CPU field timing and rendered frame rate are different quantities.

## Separate support/fade sensitivity

`support_sensitivity.cjs` holds the original near-field/tilt rules, four rotor queries, source strength and receiver response fixed, and changes only explicitly named support/fade constants. It uses all-pairs search so the larger domain is actually covered. The six small scenarios and all four support regimes are saved in `raw/support_sensitivity.json`.

- A source 3 m overhead gives zero nominal compact-model inflow. Moving the axial fade/cutoff from 2–2.5 m to 4–5 m produces **0.9160 m/s** and changes computed receiver thrust by **7.5562% of weight**.
- A 16-source ring 3 m overhead gives zero nominal inflow and **2.4602 m/s** with both extended supports, a **20.0016% of weight** thrust difference.
- A radial-tail pair produces zero nominal inflow and **0.06680 m/s** when the radial fade/cutoff expands from 2–3 half-widths to 4–5, a **0.46062% of weight** thrust difference.
- The deliberately unsupported near-wake fixture still throws in all four regimes.

These are deliberately selected sensitivity examples, not a population estimate or a physical error bound. The expanded formula has not been calibrated or validated; larger support is not established as truth. They demonstrate why tiny pruning error against the compact model does not resolve the much larger uncertainty in assumed support and source accumulation.

## Scientific limits

Passing against the present finite-support empirical model does not validate wake overlap, receiver response, free-flight accuracy or physical safety. The source is already truncated at 2.5 m downstream and three local half-widths radially. Cutoff extension is a separately labeled model sensitivity, not a better-established truth. These CPU checks cannot support GPU, 5,000-drone coupled real-time, or low-end-device feasibility claims.
