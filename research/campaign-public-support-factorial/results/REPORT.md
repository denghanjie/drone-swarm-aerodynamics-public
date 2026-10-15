# Fixed-state support sensitivity: radial-tail effects, no axial-cutoff coverage

Public edition: complete 401-row wind/load tensors are retained privately. This checkpoint publishes their exact hashes and schemas, numerical summaries, and 25 selected frames. It is not a complete public rerun bundle.

Experiment: **PUBLIC-SUPPORT-FACTORIAL-20261015**. One released attempt completed on 2026-10-15 UTC. This report analyzes its saved outputs only; it does not rerun the model or add experiments.

## Result in plain language

The artificial downstream cutoff made no difference in this particular saved trajectory because no evaluated far-field pair reached the distance where that cutoff begins. Removing the radial taper changed the model's predicted thrust by up to **1.969% of vehicle weight** and rotor inflow by **0.3056 m/s**. Those changes come entirely from the uncertain outer wake, where the source paper already warns that the analytic profile overpredicts measurements. This is a quantified modeling sensitivity, not evidence that the larger wake is more accurate.

## What actually ran

The 401 unchanged historical endpoints contain 16 vehicles over one second, with a 0.0025 s sample interval. The historical run identifies genuine local 3D Boids on its own evolving state; this diagnostic merely rescores those saved states. It does not create a new flight or predict how changed aerodynamic loads would alter subsequent motion. The historical simulation held its aerodynamic field between 100 updates; this diagnostic evaluates all 401 endpoints instantaneously.

Four arms use identical geometry, source strength, superposition, receiver-axis projection, and receiver thrust law:
- P: original axial and radial tapers
- X: axial taper/cutoff removed, radial taper retained
- R: radial taper/cutoff removed, axial taper retained
- U: both removed, a formal continuation over the finite 16-source population

All research arms enumerate every other source. The untouched original grid-based kernel is the baseline comparator. This is separate from historical R8 and is not a correctness qualification or speed benchmark.

## Numerical result and coverage

- Completed all 401 rows, 6,416 receiver-times, 25,664 rotor samples per arm, and 384,960 ordered rotor/source visits.
- P matched the original finite-support field **bit-for-bit in all 25,664 rotor samples**. Maximum inflow and load residuals were both zero.
- All 401 input rows passed explicit nonmutation checks. No domain error, nonfinite output, or numerical gate failure occurred.
- Maximum factorial-identity residual was 2.776e-17 m/s. The directly accumulated interaction was zero throughout this geometry; subtraction of arm totals incurs floating roundoff.
- Maximum receiver cubic-equation residual was 6.661e-16. This checks the implemented ideal-power closure numerically, not its physical correctness.
- Observed support-envelope bound was 2.630712 m, inside the original 3 m center-neighbor radius; the near-core envelope was 0.287994 m.
- Of all candidate visits, 199,640 were excluded as upstream, 47,187 were outside the far-field formula in the non-core near region, and 138,133 used the far-field formula. The near-region exclusions are unmodeled terms, not validated zero real flow.

Saved tensor hashes were rechecked during this postrun analysis. Direct byte comparisons confirm P=X and R=U for every saved row. These equalities are actual output identities, not just matching summary maxima.

## Axial result: exact zero effect with an important coverage gap

X-P is exactly zero for all retained inflows and loads. Every one of the 138,133 evaluated far-field terms is in the downstream bin d<2 m. There are **zero terms** in 2<=d<2.5 m or d>=2.5 m. Thus the data never exercise the axial fade or cutoff; zero sensitivity here provides no evidence that the 2-2.5 m choice is generally adequate.

The 25 prescribed scalar profile checks independently exercise the formula weights at selected distances and radial positions, including the fade/cutoff. They are scalar identities, not extra flight observations or empirical data.

## Radial result: conditional predicted-load changes

R-P and U-P are identical in this trajectory. Values below are absolute differences, except signed thrust witnesses. Percentages use fixed hover weight mg=0.26487 N, fixed hover-induced speed vi=4.032743274 m/s, and moment scale mg*a=0.00741636 N m.

| Quantity | Median across receiver-times | 95th percentile | Maximum |
|---|---:|---:|---:|
| Largest rotor inflow change per receiver | 0.01202 m/s | 0.18134 m/s | 0.30556 m/s |
| Same inflow change / vi | 0.298% | 4.497% | 7.577% |
| Total-thrust change magnitude | 0.0002366 N | 0.0034140 N | 0.0052142 N |
| Total-thrust change / mg | 0.0893% | 1.2889% | 1.9686% |
| Roll/pitch moment-vector change / (mg*a) | 0.00749% | 0.33971% | 0.52334% |
| Largest absolute roll/pitch angular-acceleration change | 0.03539 rad/s^2 | 1.65108 rad/s^2 | 2.60176 rad/s^2 |

These changes are conditional on the same unvalidated fixed-ideal-power receiver law. They are neither electrical-power measurements nor actual flight-acceleration measurements. The largest world-vertical force change is 0.00516364 N, or 1.94950% of weight. Nominal yaw torque is unchanged by model convention.

Exact zero-based witnesses:
- Largest inflow change: row 251, t=0.6275 s, receiver 8, rotor 3. P=0.0832677742 m/s; R=0.3888231776 m/s; difference=0.3055554034 m/s.
- Largest total-thrust change: row 261, t=0.6525 s, receiver 8. P=0.2820805085 N; R=0.2768662727 N; difference=-0.0052142358 N.
- Largest angular-acceleration change: row 199, t=0.4975 s, receiver 4, roll channel. Moment change=3.64245816e-5 N m, giving 2.60175583 rad/s^2 with the frozen inertia.

Of 6,416 correlated receiver-times, 236 (3.678%) exceeded the descriptive 0.05vi inflow marker; 887 (13.825%) exceeded the 0.01mg thrust marker; and 2,466 (38.435%) exceeded the 0.1 rad/s^2 angular marker. These are predeclared descriptive bins, not safety/physical-accuracy acceptance limits. The longest consecutive sampled runs above those markers were 164, 243 and 401 samples respectively; these are sampled run lengths, not continuously established duty cycles. No statistical independence or significance claim is made.

Removing the radial taper made 1,314 previously zero rotor-time predictions positive, out of 10,416 baseline zero rotor-time samples. The underlying rotor count remains 64; these are repeated temporal observations.

## Where the effect comes from

The core xi<=2 is unchanged. The sum of additional inflow contributions over all endpoint/source/rotor terms is partitioned as follows:

| Radial region | Share of aggregate added inflow |
|---|---:|
| Transition 2<xi<3 | 33.306% |
| Outer 3<=xi<=5 | 40.296% |
| Extreme xi>5 | 26.398% |

The aggregate added sum is 1,085.3968 in summed m/s terms, equivalent to a mean added inflow of 0.0422926 m/s across all 25,664 rotor samples. This is an unweighted discrete sum, not a physical flux or time integral. It is not legitimate to assign the same percentages to load changes because the receiver law is nonlinear.

There are 122,094 positive added pair contributions for R/U; their maximum recorded downstream distance is 1.869505 m and maximum xi is 34.9775. More than a quarter of aggregate added inflow comes from xi>5, where the literature review reports measurements dominated by noise. This sharply limits physical interpretation of U.

The largest retained **single-source** added contribution is 0.12978146 m/s: row 218, t=0.545 s, receiver 9, rotor 0, source 3; downstream=0.7648011 m, radial=0.2625579 m, xi=2.794058. This is in the 2<xi<3 transition. It is a different event from the largest aggregate rotor difference, so it must not be described as that event's dominant source without additional evidence. No extra source-term replay was performed to infer that attribution.

## Increment over prior research

The prior weak-wake-pruning study already retained 4,848 prescribed snapshots and 1,330,776 receiver comparisons. It bounded omissions inside the finite-support reference and did not pass its preregistered speed-benefit gate. That outcome is unchanged.

Its existing report also already contained selected support-expansion examples: a 3 m source stack changed predicted thrust by 7.5562% of weight, and a selected 16-source ring by 20.0016%, under specified support expansions. Therefore this experiment does not newly discover that support assumptions can matter.

The incremental evidence is complete factorial support attribution on every endpoint of one genuine local3D trajectory, with full rotor tensors and reproducible predicted-load effects. It identifies an axial-coverage gap and shows that this trajectory's sensitivity is entirely radial-tail sensitivity. This is useful progress toward a more credible model assessment, not demonstrated novelty or independent physical validation.

## Most useful next step

Prioritize an independent measured-velocity comparison at compatible vehicle scale, geometry, normalization and probe location before changing cutoffs. A candidate Crazyflie source is documented in the [literature ledger](../physics/SOURCE-LEDGER.md); quantitative comparison requires matching geometry, normalization and uncertainty first. No such validation is claimed in this checkpoint.

For the axial question, use a separately approved genuinely local3D state sequence that actually contains valid source/receiver separations across and beyond 2 m. Do not manufacture that coverage by repositioning individual drones and present it as a Boids flight. Repeating the same one-second replay or another isolated 3 m support fixture would add little beyond existing evidence. Fresh closed-loop work still needs the genuine pinned local3D controller/source closure and an explicit new plan.

## Resource record and reproducibility

The execution supervisor recorded exit0, no timeout, 0.775825 s wall, 1.508721 s child CPU and 108,994,560 B peak RSS. Child self-report ended before its final receipt write and reports a slightly smaller interval. These observations are resource accounting for one run, not speedup evidence. No paid compute, new dependency or dataset download was used.

Complete wind tensor: 821,248 B, shape[401,4,16,4], time/arm/receiver/rotor order; SHA-256 7b672779275b0b1a4e2a4f871758d0845f7bcd17ebb91841f4277c43e42d94c3.

Complete load tensor: 615,936 B, shape[401,4,16,3], columns total thrust/roll moment/pitch moment; SHA-256 a6d68dc2e982edf1890e1b4fea5dbc9c771459397cae271ee92f5f8f4c4e8d75.

Public supporting files: [metadata](metadata.json), [scalar probes](probes.json), [numerical summary](summary.json), [independent review](INDEPENDENT-REVIEW.md), and the [public plan edition](../feasibility/PUBLIC-PLAN.md). Original progress, execution and release records remain privately retained. Frozen plan SHA-256: 2879a16281c5ce16ef064165fbcd9254ccf77ca6fde7759844144838305add44. Executed runner SHA-256: 9b27c5fe2e3011ee994cd35179e8b2948bf62241ebd9a286f7eae235c6518e9b. Source public commit: 1336f5c416875a9651f92b58b2ed06649f25b04e.

This report is postrun analysis, written after results were known. It does not alter the frozen plan, arm definitions, bins, source code, failed historical evidence, or publication claims. The main result is model-relative and limited to the retained state sequence.
