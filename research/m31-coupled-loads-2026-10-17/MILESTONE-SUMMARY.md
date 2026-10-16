# Milestone: complete groups have independently checked load bounds

**The numerical bridge from individual interactions to complete small groups passed this fixed experiment.** All11 admitted scenes received sound load certificates and met the predeclared normalized error tolerance of1e-8. Six scenes were correctly rejected and two extreme-force scenes remain unqualified. This is progress toward the original5,000-drone Boids/dynamics/mutual-aerodynamics accuracy–computation goal; it is not completion or a claim of a publishable breakthrough.

## What we asked

If every drone affects the other drones' effective loads, can we account for every interaction, solve that coupled problem and give trustworthy bounds on the resulting forces and moments? Checking only one pair cannot answer this group question.

## What we did

Before execution, we froze19 synthetic static scenes with1..16 drones, exact model semantics, a fixed solver recipe, an independently authored checker, nine deliberate fault probes and resource limits. We published source commit `0e184452f0ccc5fbe02c8c5491ee849259b74a26` and independently fetched its exact public manifest before running. No parameter was tuned after observing results. Both sole scientific allocations are now closed.

The candidate considered every ordered nonself rotor–source pair, then solved complete coupled rows and certified rotor thrust, collective thrust, world force and all three world-moment components. The separate checker reconstructed geometry, interaction membership and coefficients, solved a high-precision bounded reference and checked every returned load box and error claim. It never trusted the candidate's native proposal as an accuracy proof.

## Observed results

| Outcome | Recorded evidence |
|---|---|
| Admitted and independently checked load certificates |11/19 scenes |
| Admitted scenes meeting all four declared error targets |11/11 |
| Correctly rejected scenes |6 |
| Explicitly unqualified extreme scenes |2 |
| Deliberate faults detected |9/9 |
| Baseline checker errors |0 |
| Planned pair records |2,632 |
| Observed pair records |2,624 |
| Explicitly skipped after global invalidity |8 |

Observed pairs comprise1,001 positive,1,602 exact zero,16 rejected and5 unresolved. Positive statuses in refused scenes do not make those scenes admitted. The isolated invalid scene has no planned pairs but is still globally validated. The invalid two-drone scene explicitly stops before its8 pairs; none is silently treated as zero.

The accepted groups include vertical stacks, two columns, tilted unequal-force groups, a stable-ID permutation and a staggered16-drone group. Maximum returned normalized upper bounds across admitted scenes, rounded for reading, were: rotor1.862e-15, collective8.124e-16, world force1.897e-14, world moment5.867e-13. Exact integer endpoints are in the saved output. These are conservative uncertainty bounds relative to mg/4, mg and mgR, not measured physical errors or estimates relative to each potentially small output component. Some bounds include visible arithmetic enclosure floors even when symmetry makes a true component zero.

The tilted group exercised a nonzero saved world-z moment under the actual supplied geometry and unequal forces. This confirms that the tested calculation did not silently drop the third moment component; it does not establish a new physical yaw effect.

The two unresolved stress cases remain distinct. In tiny-force, the candidate cannot certify a positive normalizer lower bound and the fixed independent pair reference is also undecidable for that pair. In huge-force, the candidate refuses its arithmetic range while the reference can prove cap rejection. Both remain unqualified; verification does not turn refusal into a load certificate.

## What we can conclude

For these finite, static, ordered M-current scenes, complete-pair assembly, coupled-root certification and signed load/error propagation worked together and passed independent scrutiny. The error probes show that this checker detected the nine specified corruptions. They are not exhaustive software correctness proof.

We cannot yet conclude physical accuracy, flight safety, closed-loop benefit, browser scientific equivalence, scalability, a speed advantage or novelty. The11 certificates are not evidence for every swarm geometry. The positive-edge ordering restriction is part of this operational prototype, although the inherited contraction reasoning is more general.

## Why it matters and what follows

We now have a checked complete-load reference for small groups, which is necessary before judging a faster calculation. The next useful research step is a prospectively bounded comparison of complete current-state work against exact spatial screening/hierarchy and certified omission, using a common load-error contract. Charge preparation, interaction discovery, admission, solve, certification and any fallback. Existing timed baselines already omitted dense diagnostic tensors; removing those cannot be credited as a new speedup. Do not infer a5,000-drone runtime from these supervision times.

The [new Three.js view](viewer/index.html) shows saved group geometry and forces. It is static and reads saved evidence only. The linked historical5,000-drone Boids replay remains airflow-off and unchanged. Future milestones still need actual coupled dynamics and browser computation.

See PROTOCOL.md, MODEL.md, source-publication.json, results/, review/SAVED-RESULT-AUDIT.md and RESTART.md for the exact evidence and continuation boundaries.
