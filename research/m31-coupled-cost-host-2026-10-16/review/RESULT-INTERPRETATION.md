# Coupled-cost host result: independent interpretation

Saved-record and arithmetic review, 2026-10-16. No scientific source or checker was imported or executed, no state was reevaluated, and no repository file was changed. All 140 raw call records were read; their hashes and common fields match their validated records, and every saved validation flag is true. Medians, block-paired ratios/differences and phase sums were recomputed from those raw values and agree with `analysis.json`. Details are in `ARITHMETIC.json`. This is an independent descriptive cross-check, not a second execution of the scientific audit or reconstruction of transient timed arrays.

**The predeclared same-grid ordered/Picard comparison passes. Geometry construction remains the dominant cost, and all-pairs+ordered is the fastest of the measured complete-query arms.**

Both frozen invocations completed once, with successful supervisors, exit zero, no monitor errors or exit races, and no recorded termination: candidate 67.276 s; saved-record reviewer 3.625 s. They identify source `a459802be0b46beac72f35568a60533215f8f784` and manifest `f88099916c1a26fe999fb9a0d998d4e048c486e3d27916541762fa0b93b2284f`. The frozen reviewer reports all 10,010 checks passed, complete qualification and coverage of 12 full warmups, 72 full measured calls, eight cached warmups and 48 cached measured calls. These allocations are now closed.

All durations below are milliseconds. A=all-pairs+ordered; B=grid+ordered; C=grid+Picard. O/P are separate cached-matrix ordered/Picard workloads. Method columns are marginal medians; B/C is the median of six block-paired ratios, not a ratio of marginal medians.

| Exposed state | A median | B median | C median | Paired B/C | Cached O median | Cached P median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| N1000/t20 | 46.946 | 81.991 | 91.205 | 0.902652 | 3.350 | 12.901 |
| N5000/t20 | 586.637 | 1022.532 | 1098.364 | 0.930374 | 18.289 | 97.058 |
| N5000/t60 | 568.158 | 976.438 | 1048.869 | 0.929131 | 18.090 | 95.130 |
| N5000/t180 | 516.926 | 621.077 | 679.358 | 0.913258 | 17.769 | 76.215 |

For the three required N5000 states, ordered solving reduces same-grid complete-query time by median paired fractions of 6.963%, 7.087% and 8.674%, with six strict B wins out of six in each case. The predefined ratio <=0.95 and >=5/6 wins condition is therefore met on every required state. Median paired absolute savings are 76.505, 74.331 and 58.969 ms. N1000 is contextual, as preregistered. These are six repeated measurements per state in one process on Apple M4/Node 24.19.0; they are not a population effect, independent-scenario replication or significance test.

The diagnostic A/B ratios are 0.575637, 0.573841, 0.581590 and 0.833642 in table order, with A faster in all six blocks of every state. Thus the grid is not the winning coefficient-construction implementation here. A is the fastest *measured* complete arm, not an established best available CPU implementation. An all-pairs+Picard arm was not measured, so the same-grid B/C ratio must not be transferred numerically to that missing contrast.

## What the saved phases support

Using sums across the six measured blocks, the geometry phase accounts for 97.62%, 97.58% and 96.33% of N5000 B time, and 95.99%, 95.98% and 95.71% of A time. These shares are derived from the full-query phase clocks, not by subtracting an independently timed cached workload. The source's geometry phase includes candidate gathering/sorting, classification and coefficient assembly; its total does not isolate which suboperation is responsible for the grid's excess.

The grid avoids 45.69%, 49.50% and 68.61% of directed center tests at N5000, while retaining the same rotor-pair calls and positive terms as all-pairs. Fewer center tests consequently do not imply lower elapsed time. Candidate gathering, sorting and representation work are plausible contributors, but their individual costs were not measured. Do not attribute the whole loss to sorting or claim that a different cell size would fix it.

The paired phase differences support the solver interpretation: the sum of C-minus-B solve-phase time across six blocks is 467.510, 460.819 and 344.367 ms; the corresponding ordered setup penalties are only 6.596, 6.236 and 6.470 ms. Geometry differences are small relative to those solver savings. This is a real benefit in the measured instrumented implementation, including iteration-dependent resource checks; it does not isolate bisection arithmetic alone.

Cached O/P paired ratios are 0.188857, 0.188256 and 0.230579 at N5000. The ~18 ms O result includes solving, residual evaluation and checksum on an already qualified resident matrix/schedule. It excludes coefficient refresh and does not show that coefficients can be reused after poses or nominal motor loads change. It cannot be labeled complete refresh latency, browser frame time or flight-update time. Even deleting all B setup, solve and residual work would remove only about 1.85%, 1.93% and 2.88% of the measured B totals, holding everything else fixed. That arithmetic ceiling is not a proposed valid implementation.

## One next question

**Can one structurally different, order-preserving batched coefficient builder materially reduce complete-query latency below the measured all-pairs+ordered A baseline while preserving the exact coupled-model guards and outputs on new, independently frozen states?**

Recommend source/design work on that question before any new allocation. Select one justified construction design, retain canonical source accumulation and all support/admission semantics, and prospectively freeze its correctness checks, complete-query clock, practical threshold and stopping rule. A is the measured baseline to beat; outperforming the slower B alone would be insufficient. A new finite allocation would require its own explicit protocol and source checkpoint; this note creates none.

This recommendation targets the measured dominant stage rather than further solver tuning or an open-ended grid-parameter sweep. The closed positive-omission ablation and E/Z, L/E screening variants already failed their incremental usefulness gates despite reduced operation counts. Those failures remain evidence against another sequence of small screening/bookkeeping adjustments on exposed cases. Their fixed-strength timings cannot be pooled with this coupled-law result, and their omission bounds cannot be reused as coupled error guarantees. If source/design review cannot identify a credible structural gain over A, stop this CPU optimization line rather than manufacture another minor variant.

The useful completed finding is a workload-specific same-grid scheduling benefit alongside a larger geometry-construction bottleneck and a negative grid diagnostic. It supplies no physical validation, flight accuracy, fresh-scenario generalization, browser-real-time or algorithmic novelty claim. Preserve the earlier failed execution and its unresolved transient-execution history with the new successful checkpoint.
