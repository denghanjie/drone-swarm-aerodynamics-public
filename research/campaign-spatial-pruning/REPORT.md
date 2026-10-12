# Spatial wake omission: bounded campaign result

## Conclusion

The conservative candidate met all declared numerical error bounds, but weak-wake pruning did **not** meet the preregistered speed-benefit gate. Do not advance this implementation as a practical acceleration method on the basis of these results. Same-equation implementation changes improved performance against the legacy code; that is separate evidence and must not be attributed to pruning.

This is a numerical study of the pinned finite-support mean-wake model, not physical validation. It does not demonstrate turbulent flow, flight safety, a validated receiver response, browser-coupled real-time operation, WebGPU execution or 5,000-drone coupled feasibility.

## Frozen method and retained failure

- Source snapshot: `c591ce2b195fa01b895d4ba881a44a4b92fdd703`.
- Candidate SHA-256: `1d9e1afcf9983b900034b7b586c4ffd02ec4b3242c467f8e684fbdda1850d562`.
- Primary experiment: summed wake law, all four receiver rotors, unchanged force/moment response and support/fades, identical prescribed states, accumulated omitted-inflow budgets 0.002 / 0.01 / 0.04 m/s.
- Exact matched control executes the same geometric bound and exact-zero support culling, with zero positive-influence omission. Original code provides an independent reference and legacy timing comparison.
- Version 0 ignored fades in its conservative envelope and could omit no positive-bound interaction within any frozen budget. That failure, source and hash are retained. Version 1 adds mathematically valid upper bounds on the existing fades before held-out evaluation. No budgets were relaxed.

The original eight-step framework is preserved. This campaign supplies bounded software evidence for Steps 3–6 and a small Step 7 scale test; it does not complete their physical-validation requirements or resolve Step 8 novelty.

## Accuracy: prescribed identical states

The complete matrix pools development seeds 3301/3302 and untouched evaluation seeds 3391/3392. It contains 4,848 snapshots: four seeds, counts 16/50/100/200, sparse/dense/tilted 3D clouds, and 101 times over one second. Three budgets yield 1,330,776 receiver comparisons. All per-rotor fields, force/moment loads and error bounds are retained in the raw evidence. Pooled results:

- Zero-budget matched/reference maximum inflow difference: **0** in this matrix.
- Bound violations, domain failures or nonfinite results: **0**.
- Positive-bound source–receiver omissions: **259,032**, summed across budgets/cases/times.
- Maximum inflow error: **0.0308559073 m/s**, below the recorded accumulated bound and the maximum budget.
- Maximum force-vector error: **0.000343458918 N**, or **0.1297% of weight** (screen: 0.5%).
- Maximum roll/pitch moment-vector error: **0.000006408602 N m**, or **0.0864% of weight × arm** (screen: 0.75%).

These screens were engineering budgets chosen consistently with epsilon and nominal rotor thrust limits. They are not independently established physical or mission-usefulness tolerances. Force and moment both had to pass; errors near zero were evaluated absolutely. Independent adversarial checks also examine near-domain exits, support boundaries, many weak sources, invalid inputs and source-order permutations.

Greedy source-order omission is not invariant under drone relabeling. In a symmetric configuration it can create a small nonzero moment where the exact reference moment is zero, while satisfying the absolute bound. The bound therefore does not imply symmetry preservation or that the effect is harmless under feedback.

## Separate support-assumption diagnostic

Independent all-pairs diagnostic fixtures changed only the named finite-support/fade constants, while retaining the same four receiver rotors, source strength and receiver law. A source 3 m above a receiver has zero inflow in the nominal compact model; extending the downstream fade/cutoff from 2–2.5 m to 4–5 m produces 0.9160 m/s and a computed thrust difference of 7.5562% of weight. A deliberately selected 16-source ring at the same height changes thrust by 20.0016% of weight when both axial and radial support expand. The near-wake fixture still fails explicitly in all regimes.

These selected sensitivity examples are not a physical error estimate. The extended formula is also unvalidated and is not established truth. They show that tiny omission errors inside the existing support do not settle the larger support/aggregation assumptions. [Full independent support configurations, states and results](results/independent-support-sensitivity.json).

## Computation cost: no pruning win

Twelve untouched seed/count/family cases at 100 and 200 drones were timed serially. Every case retained seven paired repetitions and input-state hashes. The timed scope is the complete `fields()` call, including validation, rotor/axis preparation, broad phase, bounds, retained kernels and result allocation; receiver loads, integration, serialization and rendering are excluded.

**0 of 36** budget/case comparisons passed the predeclared gate of at least 10% median time saving and a paired bootstrap 95% interval wholly below a ratio of 1. Across-case median candidate/zero-budget time ratios were:

|Inflow budget|Median time ratio across cases|
|---|---:|
|0.002 m/s|0.9992|
|0.010 m/s|0.9946|
|0.040 m/s|0.9924|

The primary timing work took 46.73 seconds. No larger timing campaign was run after the failed speed gate. Independent timing checks likewise found no qualifying pruning speed benefit.

The zero-budget implementation was approximately 1.53–1.95× faster than legacy across these cases. This combines allocation reduction, scalar equations and exact-zero spatial culling. Because the matched control pays for conservative bounds, it is not a claim to the fastest possible exact implementation; a lean exact implementation could be faster still. No practical pruning advantage is claimed against either that unmeasured alternative or other hardware.

## Genuine local Boids: separate short diagnostic

Eight 16-drone records reached their planned one-second end: exact/pruned/off on seeds 3391 and 3392, plus separate exact physics-step and airflow-refresh refinements on seed 3391. These reuse the original local 3D separation/alignment/cohesion rules, shared broad route, wall-priority controller, rigid-body integration and contact checks. There are no assigned per-drone tracks and no controller retuning.

- Primary cadence: physics 2.5 ms, controller 10 ms, held aerodynamic field 10 ms.
- Pruned records actually omitted 24 and 59 source–receiver pairs over their respective runs.
- Seed 3391 maximum common-frame position difference, exact versus pruned: **0.05583 mm**.
- Seed 3392 maximum common-frame position difference, exact versus pruned: **0.5102 mm**.
- Same-seed 1.25 ms physics-step refinement difference: **4.93 nanometres**.
- Same-seed 5 ms airflow-refresh refinement difference: **6.855 mm**.

The refresh sensitivity is materially larger than the pruning perturbation in this short window, despite passing its 1 cm screen. This result does not override the earlier M28 cadence failure or M31 long-trajectory failures. Airflow-off is a different model control, not an approximation expected to satisfy the coupled-trajectory tolerance. No dynamic scaling is justified here.

The Three.js viewer replays exact saved states and the actual held fields used by the integrator. It does not interpolate a prettier path. Wake surfaces are illustrative mean-wake envelopes with prescribed source strength; they are not measured airflow, resolved turbulence or transported particles. Drone bodies are enlarged 2× for legibility, while spatial coordinates and wake widths retain metre scale.

## Evidence and reproduction

- [Frozen plan](PLAN.md), [amendments](AMENDMENTS.md), [source provenance](provenance.json).
- [All accuracy summary](results/accuracy-summary.json), [144 case summaries and exact worst-case rows](results/accuracy-cases.json).
- [Separate untouched evaluation-seed summary](results/accuracy-heldout-summary.json): 2,424 unique snapshots and 665,388 receiver comparisons; no threshold tuning used these seeds.
- [All primary raw timing repetitions](results/timing.json).
- [All short Boids outcomes and comparisons](results/boids/index.json); each links its full state and held-field record.
- [Local viewer](demo/index.html); run `python3 -m http.server 8876 --bind 127.0.0.1` from this directory, then open `http://127.0.0.1:8876/demo/index.html`.
- `wake-pruning-evidence.html` is the self-contained offline viewer, with bundled Three.js and every small replay record. Its evidence links download embedded records. No hosting is implied.

The viewer passed source/data identity and JavaScript syntax checks. Actual rendering, interactions and mobile layout remain unverified because the browser launch was blocked by the environment's socket permission restriction. No browser security settings were changed and no rendered screenshot is claimed.

Numerical reproduction, from this directory in the source repository:

```
node src/verify-source.cjs
node src/checks.cjs
timeout 180s node src/experiment.cjs accuracy
python src/summarize-accuracy.py
timeout 285s node src/experiment.cjs timing
timeout 90s node src/boids-diagnostic.cjs
```

Run timing serially without other CPU-heavy tasks. Full accuracy evidence is approximately 194 MiB compressed and is verified as separately persisted in an owner-private attachment. It is excluded from Git because the file exceeds the host's single-file size limit. Its exact byte count/SHA-256 and reproduction command are recorded in `results/accuracy-cases.json`; all 144 case summaries and worst-case rows are included in the checkpoint. No private attachment identifiers or download addresses are published. The large historical evidence archive was not downloaded.

The source and outcome are reproducible numerical evidence. Independent receiver calibration, source operating-condition validation, overlapping-wake measurements, support/refresh convergence and matched application-level accuracy criteria remain open. The appropriate next implementation experiment would reduce candidate-selection/bound overhead or investigate exact broad-phase efficiency, with a new plan; this campaign does not silently begin it.
