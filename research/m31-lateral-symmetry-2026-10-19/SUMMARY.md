# Most remaining sideways error is an opposite-direction pattern

19 October 2026. Completed, independently checked diagnostic; the model has not changed.

Imagine looking at the air below a drone from the front. Compare one measurement on the left with another at almost the same position on the right. Some prediction errors point the same way on both sides, like a shared sideways breeze. Other errors point opposite ways, like getting the inward or outward motion wrong. We separated those two patterns without changing any measurement or prediction.

The result: **84.03% of the remaining squared error is in the opposite-direction part; 15.97% is in the same-direction part.** These percentages describe squared prediction error, not fractions of airflow, physical energy, drones, or experimental certainty.

We matched all **2,440 farther measurement locations into 1,220 pairs**, using a fixed coordinate rule published before calculation. None of those farther locations was dropped. The maximum coordinate mismatch was 0.001342 in the saved normalized units, below the prospective 0.01 limit. All original coordinates were retained.

| Selection | Pairs | Coverage of previously included cells | Same-direction error share | Opposite-direction error share |
|---|---:|---:|---:|---:|
| Primary: 39–97.5 cm below drone | 1,220 | 100% | 15.97% | 84.03% |
| Near: 26–39 cm, descriptive | 391 | 99.87% | 14.17% | 85.83% |
| Middle: 39–65 cm | 820 | 100% | 18.09% | 81.91% |
| Far: 65–97.5 cm | 400 | 100% | 8.51% | 91.49% |

The centimeter ranges above are selection limits, not a claim that measurements reach every endpoint. The near region retained its earlier 17 excluded cells and has one additional unmatched included cell. Both exclusions and the unmatched point remain in the saved evidence. Overall there are 1,611 pairs and 3,240 original records.

## What this tells us

Adding one constant sideways velocity cannot remove the dominant error pattern. This does not rule out ambient crossflow that physically changes the wake. Adding the same sideways velocity to both ends of a pair changes the same-direction part; it cancels out of the opposite-direction part. That follows directly from subtraction. We did not fit or subtract such a breeze.

The fixed model's opposite-direction component has RMS 0.003936 reference-speed units, compared with the measured component's 0.014640; its residual component RMS is 0.010769. This points toward investigating the model's representation of inward/outward flow and its assumptions. The size difference is not proof of a missing multiplier or a physical cause.

The overall primary candidate RMS error remains **0.0117476 reference-speed units**, exactly the previous full-field result. The earlier 23.59% reduction versus a zero-sideways-flow baseline remains the same. This checkpoint diagnoses that remaining error; it does not improve the model.

## What we should investigate next

Check whether the published assumptions connecting downward flow to sideways flow actually apply to this measurement and our model: speed magnitude versus downward velocity, wake width/spreading definitions, coordinate scales, how downward speed and width change with distance, and whether both measured components use the same normalization. Compare the relevant published formulas and their premises before any further fit.

Even a good match to downward speed values need not imply accurate spatial changes in those values, which are needed to infer sideways flow. The measured plane also misses the central core needed by the full sideways-flow calculation, so this plane alone cannot supply that calculation without further assumptions. Any new numerical comparison needs its own fixed protocol and public source checkpoint. Do not choose a missing factor simply because it improves these already-seen measurements.

## Evidence and limits

The sole evaluator, independent Decimal audit and sole desktop/mobile display check all passed within their frozen bounds. The audit checked 1,611 pairs, all four regional summaries, 24 side metric groups and preservation of 48,615 copied floating-point values, including predictions and metrics. All scientific and display allocations are closed. A prelaunch documentation-pin correction is retained in the history; no calculation ran under the superseded freeze.

The [Three.js evidence view](viewer/) lets you switch between measured flow, the fixed model, total error, the two error patterns and coverage. It displays saved measurements in their original plane, with enlarged arrows; it is not a new flight simulation.

This is one previously examined experiment. The pairing is approximately mirrored, the arithmetic split does not identify swirl or another cause, and each pair's same-direction part can differ. Physical units/calibration, an independent experiment, full 3D airflow, drone forces, swarm safety and novelty remain unresolved. This is a useful diagnostic checkpoint, not a publication-level breakthrough.

[Fixed protocol](PROTOCOL.md) · [Saved results](results/comparison.json) · [Independent audit](results/audit.json) · [Result review](review/RESULT-REVIEW.md) · [Verified source ledger](LITERATURE.md) · [Restart instructions](RESTART.md).
