# The model moves too little air sideways in these comparisons

The fixed model underestimates the magnitude of sideways transport through **all 12 radial surfaces on the full retained grid**: the inner and outer walls of each of the six preset regions. The signs agree with the measured reconstructions, but the strengths do not. This is an observed mismatch on the existing dataset under our stated projection assumptions; it does not yet identify a physical cause.

Think of checking a household budget. If income and spending are both underestimated, the final balance may still look close. Here, mistakes on different surfaces also cancel. The saved comparison finds positive between-surface cancellation in every region. A small net balance alone cannot certify that the model sends the right amount of air through each surface.

For example, at the outer wall of the right middle region, the measured signed transport is **0.25541** and the model gives **0.04298**, in the same normalized units. No coefficient was changed to make that comparison.

## The six results

The surface-error ratio adds the magnitudes of the four integrated transport errors and divides by the previously saved measured flow scale. The local-error ratio first adds absolute sampled errors along each surface, before those errors can cancel. Both ratios use the same denominator as the earlier balance diagnostic, but measure different quantities. They are not percentages of model accuracy and can exceed 100%.

| Region (preset z/l band) | Surface-error ratio, full grid | Local-error ratio, full grid | Coarse-minus-full surface ratio |
|---|---:|---:|---:|
| Left 12–16 | 15.508% | 17.705% | +0.1954 percentage points |
| Left 16–20 | 11.067% | 11.201% | +0.1296 percentage points |
| Left 20–24 | 10.598% | 10.598% | +0.0295 percentage points |
| Right 12–16 | 19.720% | 22.446% | +0.0450 percentage points |
| Right 16–20 | 22.735% | 22.735% | +0.0209 percentage points |
| Right 20–24 | 18.229% | 18.384% | −0.1163 percentage points |

Across the six regions, both full-grid ratio ranges are 10.598–22.735%. Their matching range endpoints do not mean the two measures are identical. The maximum absolute coarsening change is 0.1954 percentage points for surface error and 0.4051 percentage points for local error. These are fixed sampling-sensitivity observations, not experimental error bars or convergence evidence.

The underlying sideways terms remain important because the common denominator includes large axial through-flow:

| Region | Inner wall measured | Inner wall model | Outer wall measured | Outer wall model |
|---|---:|---:|---:|---:|
| Left 12–16 | −0.13133 | −0.04438 | 0.08777 | 0.03153 |
| Left 16–20 | −0.08789 | −0.03657 | 0.12097 | 0.04294 |
| Left 20–24 | −0.07541 | −0.03170 | 0.14364 | 0.04923 |
| Right 12–16 | −0.21826 | −0.04435 | 0.18269 | 0.03159 |
| Right 16–20 | −0.14482 | −0.03654 | 0.25541 | 0.04298 |
| Right 20–24 | −0.10969 | −0.03167 | 0.21326 | 0.04925 |

Positive means outward across that surface; negative means inward. Actual sampled coordinates, not nominal band edges, define the boundaries. Left and right supports remain distinct. These are correlated portions of one exposed experiment, not 12 independent experimental trials.

## What changed and what remains open

We have a more specific model-data discrepancy and evidence that aggregation hides part of it. The current model, inherited gain, measurements and earlier whole-field errors are unchanged. No new fit, field evaluation, square root, raw-data decode or measured quadrature was performed. Simply multiplying the sideways model would generally disrupt its existing continuity relationship with the downward component and would need separate justification.

The comparison assumes that the offset planar measurements can be interpreted as an axisymmetric field with no average swirl. Actual component preprocessing and calibration, stitching and departures from that interpretation remain unresolved. Neither this test nor the independent numerical audit proves which explanation is responsible. Physical validation, novelty and safe swarm flight remain unestablished.

All 1,220 saved model nodes passed the predetermined admission checks. The independent audit verified the whole inherited annular result, 117,896 preserved binary64 words, 12 comparisons, 48 signed faces and 568 face-local node occurrences (corners/resolutions can repeat a node). All 43 source pins remained unchanged. Evaluator, audit and display allocations are closed; no failures or historical outcomes were replaced.

The next priority is evidence admission: complete the exact measurement-definition chain if genuinely new source evidence is available, or find an independent compatible calibrated vector field. Existing exclusions stay in place. This is more useful now than adding another score to the same exposed field or choosing a lateral multiplier to reduce its error. See the next-question review for the proposed gates; no new experiment is authorized by that design note.

[Explore the Three.js evidence](viewer/) · [Saved comparison](results/comparison.json) · [Independent audit](results/audit.json) · [Protocol](PROTOCOL.md) · [Sources](LITERATURE.md) · [Next-question review](review/NEXT-QUESTION.md).
