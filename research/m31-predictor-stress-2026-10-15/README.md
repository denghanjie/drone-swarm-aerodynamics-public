# M31 predictor stress: startup still matters

The 5 ms causal predictor reduced sampled peak and RMS errors relative to a 5 ms hold in all 18 case/observable comparisons across six prescribed encounters. **It nevertheless missed the chosen thrust target in the source-pitch case.** Prediction had no advantage in the first interval, when only one actual sample existed.

This result supports continued numerical investigation of prediction, while ruling out acceptance of this 5 ms scheme as a blanket replacement. It establishes neither physical validity nor a novel algorithm. The simple predictor is explicit prior art; the new evidence concerns its behavior in these particular declared model inputs.

[Open the Three.js milestone](viewer/index.html). It replays exact saved positions, orientations and rotor inflows for all six cases, with five methods, update-boundary values and a receiver close-up. [Reproduction](REPRODUCE.md) explains local serving. This is a prescribed-input/model-load recording, not integrated flight or emergent Boids.

## What changed and why

The previous envelope challenge had one fixed-orientation pair. This prospective suite adds wake entry/exit, startup inside a wake, repeated reversal, source pitch, receiver roll under two wakes, and three-source exposure with two moving sources. All vehicle fields are still calculated and independently checked, including source-source interactions. Receiver0 is the vehicle whose load discrepancies are compared.

Protocol/source were reviewed and pushed before execution as `661bb14c99521ef2b1d3350600e202b4fb44d5b9`. Preflight reviewers caught timing-order and failure-recording defects; those fixes occurred before any case evaluation. The six formulas and all-pair model-domain argument were separately reviewed. See [driver review](DRIVER-REVIEW.md), [case review](CASES-CLEARANCE.md), [design](DESIGN-REVIEW.md) and [frozen protocol](PROTOCOL.md).

## Results in plain language

The predictor and 5 ms hold both refresh 201 times per timed one-second encounter. The predictor extends the trend between the two latest actual samples, clips negative inflow to zero, and uses the same hold until the second sample. Prediction adds small measured computation at the same field-call schedule; timing ranges for these two methods overlap in every case. It should not be described as faster than that matched-schedule hold.

The predictor's recorded timing range was below the 2.5 ms hold's range in every case, but it did **not** beat that faster-refresh hold on every peak error. Against the 2.5 ms hold, prediction had 12 better and six worse peaks, while all 18 RMS values were lower. These are descriptive comparisons of the saved suite. A lower cost therefore does not establish interchangeability. All results are retained below and in JSON.

| Case | Hold5 peak thrust, mN | Predict5 peak thrust, mN | Hold2.5 peak thrust, mN | Predict5 meets all sampled targets? | Median predict5 / hold5 loop, ms |
|---|---:|---:|---:|---|---:|
| support-transit | 0.998918 | 0.073223 | 0.499503 | yes | 3.865 / 3.787 |
| cold-start-inflow | 0.693725 | 0.485979 | 0.346900 | yes | 3.711 / 3.752 |
| smooth-fast-reversal | 1.426228 | 0.097031 | 0.713288 | yes | 3.732 / 3.646 |
| fixed-position-source-pitch | 3.567856 | 2.898438 | 1.787649 | **no** | 3.814 / 3.659 |
| two-source-receiver-roll | 0.342673 | 0.025077 | 0.171360 | yes | 5.624 / 5.567 |
| stacked-moving-sources | 0.896544 | 0.481393 | 0.448439 | yes | 7.953 / 7.595 |

The target is 1.32435 mN body thrust and 104.883169 µN·m each body roll/pitch torque. These are chosen numerical tolerances, not flight-safety requirements or measured tolerances. Under receiver roll, total body thrust is not world-vertical lift. This is a finite selected suite; five qualifying cases out of six is not a population success estimate.

The source-pitch predictor's peak thrust discrepancy, **2.898438 mN**, occurs immediately before the first 5 ms refresh. At that boundary it still uses its initial hold. A 2.5 ms hold also misses the target on this case (1.787649 mN). Startup limits several other predictor peaks as well. The protocol preserved 0–5 ms and 5–10 ms startup windows and ±10 ms around all three interior reversals. Signed load/inflow extrema are in each case's `reportingWindows`; these windows were selected before results.

## Evidence and boundaries

Every peak/RMS comparison passed the frozen primary 0.5ms versus refined 0.25ms sampling screen, using augmented peaks and event-split RMS. This does not repair four uniform-RMS failures from the earlier cadence pilot. All reference inflows for all vehicles were checked against an independent direct-pair implementation; only receiver0 load outputs were independently checked. Largest discrepancies were at binary64 rounding scale. The independent saved-record review passed **922,282 checks** on its first invocation, including 312,078 saved production/oracle scalar comparisons; no checker correction was needed. It confirmed all 12 source-pitch predictor target exceedances occurred during the initial hold. Full evidence contains both sets of saved values.

One invocation completed in 3.2304365  supervised seconds, with 158,016 field calls including 24,006 independent oracle calls, and 41,337,905 raw bytes. There were no model-domain/arithmetic exceptions, retries or post-outcome source patches. Five technical timing repetitions plus a warmup were run per method/case in prospectively rotated order. Timing includes current-pose creation, complete all-vehicle grid/field evaluation when due, history/prediction, receiver0 roots/wrench, refresh-left bookkeeping and loop/checksum overhead. Cache initialization, oracle verification and saved-data persistence are outside the timer. Flight dynamics, Boids, obstacles, GPU and rendering are absent. A slow prior-evidence download was active during execution. Technical ranges are not population confidence intervals.

The mean-wake model retains isolated-hover source amplitude despite source tilt or incoming airflow; it lacks transport/history and measured unsteady response. Its current receiver-projected scalar inflow is cached/predicted; no new current-attitude projection is applied between refreshes. Thus a successful equation comparison is not evidence that a real source can tilt this way with this wake. The historical 27g use remains outside the verified source-model vehicle scale. No acceptable full-flight reference or 5,000-drone performance result follows.

See [complete result](results/result.json), [independent saved-record review](results/independent-review.json), [budget](results/budget.json), [claim ledger](claims.md) and [postrun restart](POSTRUN-RESTART.md). Frozen scientific source and all raw records are unchanged. The earlier audit, order diagnosis and rejected trajectories remain evidence.

## Complete comparison table

Errors are augmented refined-grid sampled peaks. Loop medians/ranges use five recorded technical repetitions. Calls count complete all-vehicle field invocations, whose cost differs with the number of vehicles.

| Case | Method | Thrust mN | Roll µN·m | Pitch µN·m | Median ms | Range ms | Field calls |
|---|---|---:|---:|---:|---:|---:|---:|
| support-transit | instant | 0.000000 | 0.000000 | 0.000000 | 28.151917 | 27.852292–30.638667 | 2001 |
| support-transit | hold-10ms | 1.995679 | 10.350926 | 39.169031 | 2.362542 | 2.249667–2.431459 | 101 |
| support-transit | hold-5ms | 0.998918 | 5.187785 | 19.664832 | 3.787000 | 3.550000–4.928500 | 201 |
| support-transit | hold-2.5ms | 0.499503 | 2.595437 | 9.842487 | 6.433084 | 6.354958–6.596958 | 401 |
| support-transit | predict-5ms | 0.073223 | 0.466747 | 1.313983 | 3.864708 | 3.684667–4.222000 | 201 |
| cold-start-inflow | instant | 0.000000 | 0.000000 | 0.000000 | 28.855084 | 28.367375–29.307417 | 2001 |
| cold-start-inflow | hold-10ms | 1.386550 | 7.207758 | 27.277662 | 2.273166 | 2.244292–3.595750 | 101 |
| cold-start-inflow | hold-5ms | 0.693725 | 3.604635 | 13.665788 | 3.751500 | 3.695125–4.079666 | 201 |
| cold-start-inflow | hold-2.5ms | 0.346900 | 1.802670 | 6.836268 | 6.598291 | 6.249417–6.801250 | 401 |
| cold-start-inflow | predict-5ms | 0.485979 | 1.923467 | 4.269624 | 3.710834 | 3.699291–5.004791 | 201 |
| smooth-fast-reversal | instant | 0.000000 | 0.000000 | 0.000000 | 28.120041 | 27.979792–30.168750 | 2001 |
| smooth-fast-reversal | hold-10ms | 2.843218 | 15.935195 | 18.929284 | 2.301542 | 2.220041–2.398375 | 101 |
| smooth-fast-reversal | hold-5ms | 1.426228 | 7.973188 | 9.549301 | 3.645709 | 3.571250–4.324375 | 201 |
| smooth-fast-reversal | hold-2.5ms | 0.713288 | 3.992050 | 4.785874 | 6.556667 | 6.289000–7.453833 | 401 |
| smooth-fast-reversal | predict-5ms | 0.097031 | 0.965878 | 1.678596 | 3.732416 | 3.681083–3.882958 | 201 |
| fixed-position-source-pitch | instant | 0.000000 | 0.000000 | 0.000000 | 28.307375 | 27.717375–29.105167 | 2001 |
| fixed-position-source-pitch | hold-10ms | 7.072523 | 35.796149 | 114.971233 | 2.276875 | 2.209041–2.408709 | 101 |
| fixed-position-source-pitch | hold-5ms | 3.567856 | 18.095870 | 57.639128 | 3.659500 | 3.545292–3.893333 | 201 |
| fixed-position-source-pitch | hold-2.5ms | 1.787649 | 9.069753 | 29.090803 | 6.595375 | 6.323709–7.334875 | 401 |
| fixed-position-source-pitch | predict-5ms | 2.898438 | 12.136383 | 22.867924 | 3.814083 | 3.612000–3.935709 | 201 |
| two-source-receiver-roll | instant | 0.000000 | 0.000000 | 0.000000 | 44.494417 | 43.440583–45.709459 | 2001 |
| two-source-receiver-roll | hold-10ms | 0.684321 | 2.678918 | 11.170151 | 3.458416 | 3.208958–3.572041 | 101 |
| two-source-receiver-roll | hold-5ms | 0.342673 | 1.339826 | 5.595186 | 5.566792 | 5.410750–6.416125 | 201 |
| two-source-receiver-roll | hold-2.5ms | 0.171360 | 0.670303 | 2.811137 | 9.911292 | 9.686625–9.979125 | 401 |
| two-source-receiver-roll | predict-5ms | 0.025077 | 0.365200 | 3.556886 | 5.624125 | 5.548917–6.763917 | 201 |
| stacked-moving-sources | instant | 0.000000 | 0.000000 | 0.000000 | 63.009208 | 62.138791–64.822916 | 2001 |
| stacked-moving-sources | hold-10ms | 1.789805 | 21.341883 | 37.605174 | 4.622208 | 4.373250–4.831750 | 101 |
| stacked-moving-sources | hold-5ms | 0.896544 | 10.671094 | 18.827653 | 7.595375 | 7.574583–8.470000 | 201 |
| stacked-moving-sources | hold-2.5ms | 0.448439 | 5.335954 | 9.414438 | 13.906833 | 13.456750–14.877792 | 401 |
| stacked-moving-sources | predict-5ms | 0.481393 | 4.033942 | 5.462627 | 7.952709 | 7.656583–8.148333 | 201 |

## Research decision and literature

Keep the predictor as a numerical lead. Do not choose an operational 5ms cadence or silently erase the startup failure by adding prior history. A future startup policy requires a new frozen challenge; any tuning on these six cases is development, not independent confirmation. Coupled-state convergence, physically compatible force/moment data, full-cost scaling and a defined novelty contribution remain open.

The [five verified prior-art sources](literature-and-prior-work.md) include Grubmüller and Tavan (1998), _Multiple Time Step Algorithms for Molecular Dynamics Simulations of Proteins: How Good Are They?_, whose DC-1b formula uses the two latest exact force samples. Tuckerman et al.(1992) and Constantinescu–Sandu (2013) provide multirate integration precedents; Panerati et al.(2021) and Folk et al.(2023) give relevant drone-simulation comparisons and limitations. Their models/results are not assumed to transfer directly. Each citation has verified identity, primary-source links and inspected evidence anchors. The earlier [aerodynamic ledger](../m31-restart-2026-10-15/literature/annotated-ledger.md) remains the source of the wake/receiver assumptions.

The [physical-target follow-up](physical-target-followup.md) verifies a real Brown experimental dataset, but its files are behind a human-verification page for this client. File conventions, reuse terms and force/moment calibration remain unresolved. The published setup also has different geometry and actuation from M28. A quantitative physical validation target is not yet secured; this does not mean no public data exist.
