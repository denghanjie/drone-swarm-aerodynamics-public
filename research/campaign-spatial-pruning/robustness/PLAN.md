# Independent robustness and cost plan

Frozen before independent measurements on 2026-10-12 UTC. Source: `denghanjie/drone-swarm-aerodynamics-public` at `c591ce2b195fa01b895d4ba881a44a4b92fdd703`. Read the original eight-step roadmap at `outputs/research-roadmap.md`. This work contributes provisional software evidence for Steps 3, 4, 6 and 8; it does not complete vehicle validation, actual-flock scaling, or WebGPU work.

## Scope and controls

- Test omission of spatial wake interactions first on identical prescribed states. Each evaluated drone retains four rotor samples, the same receiver-force law, roll/pitch moments, nominal yaw convention and force summation mode. A prescribed fixture is not a flock controller.
- Reference A is a deterministic all-pairs evaluation of the currently declared finite-support equations. The repository's 3 m center-neighbor grid is a separate implementation baseline, not an untruncated physical reference.
- Reference B is a separately labeled, exploratory support-extension sensitivity check. Extending the empirical far-field formula does not establish accurate physics. Do not mix those changes into the exact-model comparison.
- Freeze state arrays, orientation, nominal rotor thrust, source model, float representation, source order, query refresh and method settings per comparison. Force-law or cadence changes are not approximation gains.
- Shared checkout and implementation are read-only for this independent review. Only `robustness/` is written. No paid compute, installation, provisioning, external mutation, publishing or heavy overlapping jobs.

## Correctness and adversarial cases

1. Empty and isolated states; airflow off; equal-height symmetric layout; symmetric receiver directly below emitter. Expect finite zero outputs where geometry demands zero; normalize errors with an absolute floor instead of dividing by zero.
2. Vertical stack: 0.2–2.5 m separations and axial cutoff crossings; assess all four rotor inflows, force loss and roll/pitch moment. Do not hide near-field domain exits.
3. Asymmetric wake edge: one-sided rotor inclusion at radial fade/cutoff. Include cutoff epsilon on both sides and exact equality; a center-only test cannot certify all-rotor coverage.
4. Tilted emitters and receivers: zero, 10, 19.999 and 20 degrees, both tilt signs and multiple yaw angles; test 20.001 degrees as an expected explicit domain failure. Compare rotations of fixtures and translation across grid-cell boundaries.
5. Many individually weak sources: ring/shell placements near smooth-fade regions; test aggregate omitted inflow and nonlinear load change, rather than using the largest omitted pair as the error bound. Keep valid geometric cases separate from deliberately overlapping-source software stress fixtures.
6. Near-domain hazards outside the candidate cutoff: a receiver rotor close to the near-wake cylinder while an aggressive distance candidate excludes the emitter center; candidate must fail in the same circumstances as the reference. Invalidity checks must not disappear with omission.
7. Independent N and density: at each small/medium N, use dense and sparse volumes; at fixed density grow extent with N; at fixed volume grow N. Record active and candidate pairs. Do not infer favorable scaling from growing N and reducing density together.
8. Explicit invalid input: NaN/Infinity state components, missing state fields, malformed/nonunit quaternion, negative nominal thrust where used, unknown modes/settings, zero/negative cutoffs. Expected handling is rejection, not finite-looking success or silent NaN propagation.
9. Metamorphic checks: source permutation (allow stated floating-summation tolerance), common translation, yaw rotation when valid, exact four-rotor shape, and no mutation of input states.

## Predeclared numerical checks

- Exact candidate/reference: maximum absolute rotor inflow difference <= 1e-10 m/s, derived total thrust difference <= 1e-12 N and roll/pitch moment difference <= 1e-12 N m, unless the candidate explicitly advertises omission. Report exact observed values rather than only pass/fail.
- Approximate candidates: report per-state and worst-case rotor inflow absolute/relative error, vector load error, normalized loss of weight support, moment magnitude and error. The campaign owner's frozen acceptance thresholds decide success; this independent review does not tune thresholds to observations.
- Stable relative normalization: inflow denominator max(reference magnitude, 1e-6 m/s); force denominator vehicle weight; moment denominator weight times arm distance. Report symmetric/near-zero references separately.
- Expected domain failures must be consistent across methods, including aggressive-pruning cases. Preserve complete failing inputs and method settings in JSON.
- Retain source/config/seed checksums and negative results. A candidate that passes the finite sample is not a global bound.

## Modest timing experiment, only after exclusive serial timing slot

- Functional checks may run now; timing experiments await a dedicated serial measurement window. The fixture matrix and repetition counts are written before execution.
- Use identical fixed state arrays and fixed evaluation counts, not time-until-crash or completed-mission wall times. Consume returned checksums to prevent dead work. Validate workload identity and repeatable checksums.
- Measure whole field evaluation including spatial-index construction, candidate search, guards and four rotor queries. Separately report preparation/setup and load conversion only if method boundaries support valid instrumentation.
- Warm each method before samples. Use seeded shuffled/interleaved method order across at least 7 measured repetitions. Record each duration, median, interquartile range and range. Avoid presenting a small timing difference below run-to-run variation as a gain.
- Keep output serialization and fixture generation outside core timing; use a separate end-to-end result including serialization. Record memory/RSS with caveats (process high-water memory and GC do not attribute exact per-method allocation). If allocations are measured, record heap before/after separately from timing and invoke identical GC policy.
- Keep the process single-threaded Node CPU; record Node version, OS/CPU/available affinity, source checksums, method options, process clock and host load where available. Record unavailable host details honestly. Never label this a GPU or low-end-device benchmark.
- Include an N so small indexing overhead can dominate, and both a dense and a sparse case at the same larger N. Report candidate acceptance fraction as well as time. No extrapolation to 5,000 coupled real-time drones from a small CPU sample.
- Record recording-off physics cost versus recording/serialization if a dynamic study is authorized. Demo FPS is rendering throughput and is excluded from physics speed claims.

## Dynamic gate and stopping conditions

Only after the fixed-state exact-model/error gate and physical auditor review may the campaign permit a small genuine local-Boids run. It must retain the same initial state, seed, Boids implementation, update cadence, force/moment model, controller and safety/domain exits for both methods. Report matched horizon cost as well as failure/early-stop status. Do not substitute scripted formations. No larger or longer runs on failed correctness, domain preservation, failed prescribed error criteria, unstable timing, or clear lack of benefit. A failed candidate and its raw counterexample are a useful terminal result.

## Deliverables

`PLAN.md`, machine-readable fixture/config manifest, independent test harness, raw correctness/domain failures, raw ordered timing samples if authorized, environment and source hashes, and a concise findings report with integration recommendations. Methods proposed but never run remain explicitly untested.
