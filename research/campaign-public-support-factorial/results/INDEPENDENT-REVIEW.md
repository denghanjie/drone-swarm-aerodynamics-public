# Independent completed-run review

Public edition: complete 401-row wind/load tensors are retained privately. This checkpoint publishes their exact hashes and schemas, numerical summaries, and 25 selected frames. It is not a complete public rerun bundle.

2026-10-15 UTC. Verdict: execution and saved-output consistency VERIFIED for this one public fixed-state case. The primary axial-support question was not exercised by its geometry. Radial-tail sensitivity was measured within the stipulated model; physical accuracy remains unresolved.

This review decoded saved tensors with Python struct, recomputed statistics and rehashed files. No model import/rerun, dynamics, benchmark or old-evidence mutation occurred.

## Identity, coverage and terminal state

The reviewed runner remained 19,310 bytes, SHA-256 9b27c5fe2e3011ee994cd35179e8b2948bf62241ebd9a286f7eae235c6518e9b. The plan still matches 2879a16281c5ce16ef064165fbcd9254ccf77ca6fde7759844144838305add44. The supervisor source matches its release-record hash, 9178f2a5f575733998f4569c4df8579e0d50cf1444066c8ca3c2fae13e29dd85.

All four immutable kernel files match their pinned byte counts and SHA-256 identities. The public identity manifest still matches 8cd490bc9b83e5b8f0819be17206aad308d320ac436e1e1a9a1e79c17662f35d. The original trajectory still matches 055fa27e4b7baeb3e363a2f6a912a4fd50b44cb52ce948d23e061dffd8c4ed8d. No source/input mutation was found.

Supervisor exit is 0, timeout false, stderr empty. Progress, summary and receipt all report 401/401 rows and valid rows 0–400. Tensors have the exact planned layouts and lengths:

- winds.f64: [401,4,16,4], 821,248 bytes; SHA-256 7b672779275b0b1a4e2a4f871758d0845f7bcd17ebb91841f4277c43e42d94c3
- loads.f64: [401,4,16,3], 615,936 bytes; SHA-256 a6d68dc2e982edf1890e1b4fea5dbc9c771459397cae271ee92f5f8f4c4e8d75

Both hashes were independently recomputed. All saved inflows are finite/nonnegative and all saved loads finite. Research coverage is 384,960 ordered rotor/source visits: 199,640 upstream exclusions +47,187 unmodeled near-field exclusions +138,133 far-field pairs. Partition pair counts also sum to 138,133. No failure or pending-progress file appeared.

The runner reports 25,664/25,664 production rotor matches bit-exact, zero production inflow/load residual, 401 nonmutation checks, maximum interaction residual 2.776e-17 and receiver cubic residual 6.661e-16. These are retained checks from the reviewed program, not a second independent production-model execution.

## Independently recomputed findings

Every saved inflow and load for X (axial taper removed) is byte-identical to P (original tapers). Every saved inflow and load for U (both removed) is byte-identical to R (radial taper removed). This is a complete tensor comparison, not equality of selected maxima.

For R-P and U-P, tensor-only recomputation confirms:

- Peak rotor inflow increase 0.3055554034013147 m/s at row 251, t=0.6275 s, zero-based receiver 8, rotor 3; about 7.577% of the reference induced speed.
- Peak total-thrust reduction 0.005214235805224066 N, or 1.9686018821% of body weight, at row 261, t=0.6525 s, receiver 8.
- Mean sampled total-thrust reduction 0.3551163491% of body weight across 6,416 receiver-times. This is the equal-endpoint sample mean, not an independent-sample or continuous-time estimate.
- 887/6,416 receiver-times (13.8248%) exceed the descriptive 1%-of-weight reduction marker. This marker has no empirical safety interpretation.
- Peak maximum-axis roll/pitch angular-acceleration change 2.601755830616087 rad/s^2 at row 199, t=0.4975 s, receiver 4. It is an instantaneous modeled acceleration difference, not a realized attitude change.
- Positive thrust reductions occur for 11 of the 16 receiver IDs. The longest sampled exceedance runs match the saved results: 164 points above 0.05 reference induced speed, 243 above 1% weight, and 401 above 0.1 rad/s^2. These are consecutive samples, not proven continuous durations.

Independent recomputation matched all 210 reported signed/absolute summary statistics (count, min, nearest-rank median, p 95, max across seven metrics and three contrasts), all descriptive bins, and longest-run counts. World-vertical force was reconstructed from saved thrust differences and original quaternion components without calling the model. All comparisons used 1e-13 absolute plus 1e-12 relative tolerance for cross-language reduction/rotation arithmetic. Key extrema above matched exactly.

## Important scientific limitation: no axial exposure

All recorded eligible-pair bins at downstream distance>=2 m contain zero pairs. The fade starts at 2 m. Thus this case contains no eligible interaction in the region where the axial arm differs from baseline. The exact X=P result is expected from absent exposure; it does not show that the axial cutoff is adequate for other geometries. The recorded geometry partition is not independently regenerated here, but it agrees with complete-tensor equality and the frozen arm definitions.

Keep the distinction explicit: the numerical case completed, but its primary axial-support objective is uninformative. This is a research-design limitation worth retaining, not a reason to discard the null result or quietly select another case after seeing it. A later axial study needs a prospectively declared exposure criterion, such as sufficient valid far-field source/rotor encounters at d>=2 m with core radial coordinates, and its own approved case scope. Do not manufacture new flight states and call them closed-loop data.

## Radial result is entirely in uncertain tails

The recorded contribution partitions place every added term outside xi<=2. Their summed R-P inflow contribution is 1085.3968014155075 across all endpoint source/rotor terms; direct saved-tensor subtraction yields 1085.3968014155034, agreeing to rounding. These are pooled velocity sums, not physical momentum or independent measurements.

The added contribution splits as follows:
- 2<xi<3: 33.30595%
- 3<=xi<=5: 40.29638%
- xi>5: 26.39767%
- xi<=2: 0%

Therefore the load sensitivity is wholly driven by the analytic radial tail where the literature review reports overprediction beyond xi 2 and noise-dominated measurements beyond xi 5. This result quantifies dependence on that continuation; it does not justify widening support automatically. The largest added-term xi is about 34.98, emphasizing the extrapolation. The fixed-power receiver closure, 27 g scale extrapolation, hover-source amplitude, independent mean superposition and quasi-steady assumptions remain unvalidated.

The case also omits 47,187 near-field pair terms outside the small near-core exclusion under the original domain rule. They are unmodeled exclusions, not measured zero flow. Upstream exclusions and the lack of wake dynamics further limit physical interpretation. The 1-second trajectory and its 16 interacting vehicles are correlated; there is no basis for population confidence intervals, general flight-safety conclusions or a speedup claim. Historical held-air forcing was not replayed; 401 endpoints were instantaneously rescored.

## Resources and retained evidence

Supervisor-observed process wall time 0.775825 s, child CPU 1.508721 s, peak RSS 108,994,560 bytes. The narrower scientific receipt records 0.716278 s before receipt and 1.438627 s process CPU. Different windows explain why these need not match; CPU may exceed wall. All are resource observations from one run, not comparative performance evidence. RSS was observed, not hard-capped. Node version is v24.19.0; an executable-binary hash was not recorded, so runtime provenance is less complete than source provenance.

Complete tensors and original execution records remain privately retained. This public edition omits transient workspace retention accounting.
