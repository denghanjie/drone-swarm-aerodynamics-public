# Physical checkpoint: our model disagrees with published drone measurements

**We have now compared the model with real experimental evidence. It does not reproduce the published mean forces in this test.** This is a useful finding about our model's limitations, not a new discovery about drones and not a statistically calibrated rejection.

Imagine one small drone sitting above another. The upper drone blows air downwards. Our model assumes that this changes the lower drone's lifting force but leaves the upper drone unaffected. We tested that assumption against measurements published by Kiran, Ayanian and Breuer.

We selected 11 stacked placements, from 25 cm to 110 cm apart, before reading the force values. We used the experiment's stated geometry and kept the model's airflow coefficients unchanged. The test method was reviewed, published to GitHub and independently retrieved before execution. No fitting to these measurements was performed.

| What we checked | Published measurements | Our model |
|---|---:|---:|
| Change in upper lift: 25 cm minus 110 cm | −8.34 percentage points of drone weight | Zero change |
| Lower lift at 25 cm | 69.42% of weight | 75.08% of weight* |
| Lower lift at 110 cm | 99.11% of weight | 83.19% of weight* |

Across all 11 placements, the lower prediction's mean absolute difference is **10.20 percentage points of weight**, with a maximum of **17.72 points**. Approximately these are 0.0270 N and 0.0470 N, using the paper's W≈0.265 N. These are errors for this selected static slice, not a universal accuracy rating.

*The lower calculation assumes an isolated nominal lifting force equal to weight. The upper difference test does not need that numerical baseline. Holding motor voltage and command fixed is not the same as holding mechanical power fixed; this comparison tests the combined motor/airflow approximation.

The numerical result was independently checked using a separately written data reader and higher-precision calculation: all 44 selected measurement values, the complete coordinate grid, 11 nominal predictions and 891 prespecified sensitivity calculations matched the saved evidence. This checks arithmetic and data association; it does not remove experimental uncertainty.

There is an important limit. The release contains mean grids, not the individual trials needed here, and its standard-deviation description is ambiguous. Calibration, drift and complete mounting uncertainty are not quantified. We therefore do not claim a p-value, confidence level or definite physical cause. Erasing the upper near/far discrepancy would require an unaccounted differential correction of 8.34 percentage points of weight (about 0.0221 N), or opposing corrections of 4.17 points at each endpoint. Those are required amounts, not estimates of actual measurement error. The 891 input variations are an illustrative sensitivity grid, not an uncertainty interval.

Before the run, checking the original apparatus drawings corrected our interpretation of the 32.5 mm dimension: it is the horizontal motor half-spacing, giving a radial distance of √2 times that value. This moved the minimum admissible placement above 21 cm. The discarded, unexecuted interpretation and the correction are retained in the record. Neither version was selected by matching measured forces.

**Research decision:** keep the existing computation as a numerical reference, but do not treat this aerodynamic approximation as physically validated or use it to support real-swarm safety claims. The next scientific task is to compare a physically motivated alternative that allows upstream influence and models the motor/load response, against this fixed reference. Select any fitting and evaluation data separately before tuning; these 11 cases are now exposed evidence. Consult the existing literature first, rather than claiming the already reported upper interaction as our novelty.

The [interactive Three.js evidence view](http://127.0.0.1:8876/research/m31-physical-test-2026-10-19/viewer-v2/) lets you select each measured spacing and compare lift. It reconstructs static bench placements; it is not a flight experiment or a new Boids trajectory.

[Method](PROTOCOL.md) · [All saved values and sensitivity calculations](results/comparison.json) · [Independent audit](results/audit.json) · [Geometry correction](review/GEOMETRY-CORRECTION.md) · [Precise restart](RESTART.md).

Sources: Kiran, Ayanian & Breuer, *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, [RSS 2025](https://doi.org/10.15607/RSS.2025.XXI.102); their [Brown dataset](https://doi.org/10.26300/64d4-wa17), retrieved 19 October 2026, CC BY 4.0. The authors already reported upper interaction effects. Our public repository checkpoint is not a peer-reviewed publication, hardware test by us, general physical validation or novelty claim.
