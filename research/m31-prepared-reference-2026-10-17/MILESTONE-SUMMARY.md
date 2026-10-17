# Milestone: prepare each drone once, preserve every reference result

**The single preregistered test passed all 24 fixed scenes.** The reference can reuse each drone's prepared geometry in its remaining pair calculations without changing any saved scientific result in this corpus. This is a useful implementation qualification, not yet a research breakthrough or physical validation.

Think of preparation as calculating where a drone's four rotors are and which direction they point. Previously each remaining pair check rebuilt both drones' geometry. The new reference prepares and validates those operands at scene setup, then looks them up. It checks that the saved geometry, raw drone state and model settings still belong together before using them.

## What was actually observed

| Test / counter | Result |
|---|---:|
| Fixed cases matching complete saved tree records | 24 / 24 |
| Cases with admitted loads / matching expected refusals | 16 / 8 |
| Actual scene geometry preparations and validations | 447 each |
| New geometry preparations inside pair checks | 0 |
| Scalar pair checks / bound operand lookups | 26,570 / 53,140 |
| Deliberately wrong cache/context tests detected | 6 / 6 |
| Arithmetic fixtures | 14 / 14 |
| Unchanged saved native checker reports / load corruption reports | 4 / 4 each |
| New flights / browser scientific executions / full-oracle reruns | 0 / 0 / 0 |

The complete equality comparison includes original and prepared input words, tree and coverage, scalar ordering and decisions, positive coefficients, root intervals and signed forces/moments. Expected refusals remain refusals. Two raw-invalid rows bypass preparation; this explains why447 actual preparations differ from449 logical scene rows. The previous tree method's residual calls imply53,140 additional pair preparations by source inspection; that older prefix count was not newly measured here.

The six controlled errors change a receiver, source, prepared center, model constant, rotor-corner ordering, or context lifetime. Each failed with its intended reason before a scientific pair calculation. They test specific failure paths, not every possible misuse. The earlier six coverage-corruption tests remain prior evidence and were not rerun.

Raw evidence: [terminal index](results/index.json), [event journal](results/events.jsonl), [prospective protocol](PROTOCOL.md), [reviewed design](source/DESIGN.md), and [independent source review](review/STATIC-REVIEW.md). The [independent saved-data audit](review/SAVED-RESULT-REVIEW.md) also passed: all 24 files are byte-identical to their baselines. The [new Three.js view](viewer/) passed its first UI check (62 checks, 32 fixed selections).

## What this means for the research

This removes redundant preparation from the independent numerical reference, a prerequisite for affordable larger accuracy checks. The underlying aerodynamic model and exact arithmetic are unchanged. The run took3.747833208 seconds in its one prescribed ordering, but that observation includes its own administrative work and is not a controlled performance comparison. We do not infer a speedup, extrapolate to5,000 drones, or claim interactive browser simulation.

The 24 scenes were already exposed. Agreement supports regression correctness on these scenes; it does not establish universal implementation correctness, real airflow accuracy or safe flight. Tree traversal, binding checks, positive interactions and exact root/load work still cost time, and worst-case pair work can remain quadratic.

## Physical evidence remains a separate question

The [bounded literature decision](../m31-next-evidence-decision-2026-10-17/literature/EVIDENCE-TABLE.md) checked five candidate families. Kiran, Ayanian and Breuer's [direct force/moment dataset](https://doi.org/10.26300/64d4-wa17) is a promising independent interaction target. Current access returns a verification page; file identities, conventions and calibration are not yet inspectable. No new physical numerical target was admitted or scored. Component-only propeller or rotor data cannot substitute for a multi-drone interaction test.

The overall goal remains active: a defensible accuracy–computation trade-off for5,000 locally interacting 3D drones in a browser. The next decision should test a meaningful remaining obstacle to that goal rather than start an indefinite chain of small optimizations.
