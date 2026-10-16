# Receiver transfer checkpoint

We tested whether a simple thrust-response equation, connected to a published rotor-speed setting by an explicit assumption, matches a measured small-propeller run. It differs from the reported values. This helps identify a missing physical connection in our simulation; it does not establish a new swarm algorithm.

## What we did

The equation predicts how incoming air changes thrust. It keeps a model-defined ideal power quantity constant. The experiment instead prescribed rotor speed. We explicitly assumed that the model's nominal thrust could be taken from the zero-inflow thrust at that speed, then tested the equation and that assumption together.

We used all 14 conditions from one previously exposed UIUC GWS 2.5×0.8 run. Before scoring, we fixed three ways of choosing the static baseline, the metrics, and a secondary summary for the nine reported positive-thrust conditions. We fitted no parameter and selected no best baseline. [Protocol](PROTOCOL.md); [source commit](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/ffec6dccee9def5acc473cd907417d09533bc636).

## What we measured

CT is thrust scaled by air density, rotor speed and propeller diameter. RMS is a typical discrepancy computed by squaring the gaps, averaging them, and taking a square root. The percentages below divide that discrepancy by the static baseline CT; they are not average percentage errors at individual conditions.

| Baseline | All 14: RMS CT gap | All 14: RMS / baseline | Positive 9: RMS CT gap | Positive 9: RMS / baseline |
|---|---:|---:|---:|---:|
| Fixed interpolation | 0.0319503 | 51.8834% | 0.0126928 | 20.6115% |
| Lower-RPM anchor | 0.0319366 | 51.8880% | 0.0126759 | 20.5949% |
| Higher-RPM anchor | 0.0325081 | 51.7192% | 0.0133888 | 21.3010% |

All three comparisons retain the full run. Five reported thrust coefficients are nonpositive, whereas this model branch remains positive. Those rows contribute to the primary result. The positive-thrust secondary result shows that discrepancy is not confined to those five rows; it is a descriptive subset, not a separate validation experiment. Changing the baseline changes both the predictions and the denominator, so normalized values alone should not rank baseline quality.

[Exact aggregate evidence](results/aggregate.json) includes maximum discrepancies, signed means, baseline anchors and membership. Full original and derived rows remain private because redistribution permission has not been established; official input URLs and hashes are public in [config.json](config.json). [Reproduction](REPRODUCE.md).

## What the evidence supports

The combined equation-and-baseline transfer differs from this published run, and the discrepancy persists for these three specified baseline choices. Independent calculation by a different root formula reproduced all 42 predictions and passed 71 checks. Numerical root agreement is about 9e-16; this confirms arithmetic consistency, not physical accuracy. [Independent review](review/numerical/REVIEW-CONCLUSION.md); [interpretation review](review/INTERPRETATION.md).

The experiment cannot isolate whether the equation, the control mapping, specimen/baseline mismatch or measurement effects explain the gap. Total measurement uncertainty is unavailable. The baseline scenarios are not confidence bounds. There is no statistical rejection or physical adequacy verdict, no direct validation of the original 46 mm vehicle, and no evidence here about flight trajectories or 5,000-drone performance.

## What improved and what comes next

We now have a reproducible empirical check of one explicitly declared transfer and a clearer reason not to treat rotor speed as ideal power. We have not improved the flight model or made the simulation faster. The next priority is to identify one real rotor/drive and documented command, establish its independent zero-inflow thrust, and test the same command at two predetermined nonzero inflows. The [next decision](NEXT-DECISION.md) defines the evidence needed before that test can be admitted. Further tuning on the exposed GWS run is closed.

The [Three.js view](viewer/) shows the saved aggregate discrepancies and links the historical local 3D Boids replay. It is an interactive scientific graph, not a new flight or fluid simulation. All 16 display checks passed; [QA record](QA-REPORT.md).

The published measurements and methods are from Deters, Ananda and Selig (2014), *Reynolds Number Effects on the Performance of Small-Scale Propellers*, [AIAA 2014-2151](https://doi.org/10.2514/6.2014-2151), §§II-A–E, pp. 2–5, and the [UIUC Propeller Database Volume 2](https://m-selig.ae.illinois.edu/props/volume-2/propDB-volume-2.html). The [literature ledger](RESULT-LITERATURE-LEDGER.md) states exactly what was used.
