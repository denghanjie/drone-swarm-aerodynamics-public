# Deleting the weakest tenth causes real load errors

We tested whether our previous rejection came only from an overly cautious rule. We removed the weakest tenth of nonzero aerodynamic interactions, recalculated the loads, and compared them with the full model.

**The fixed shortcut fails.** Both starting snapshots exceed even our loosest numerical threshold. Later snapshots have smaller errors, but that cannot rescue a method required to pass every state. The independent checker accepted the calculations; it did not accept the approximation.

The complete-model controls passed the strict threshold in all six snapshots. That supports attributing the observed difference to this deletion proposal within the declared numerical model, rather than a failed control calculation.

| Snapshot | Interactions deleted | Direct rotor error | Conservative rotor bound | Direct comparison at stress tier | Bound at stress tier |
|---|---:|---:|---:|---|---|
| run-a-t0 | 39 / 389 | 6.1741% | 25.5181% | definite-fail | not-certified |
| run-a-t5 | 26 / 252 | 0.2283% | 1.2533% | pass | not-certified |
| run-a-t10 | 20 / 192 | 0.0764% | 0.4304% | pass | pass |
| run-b-t0 | 40 / 394 | 6.5895% | 26.4298% | definite-fail | not-certified |
| run-b-t5 | 26 / 256 | 0.1876% | 1.1163% | pass | not-certified |
| run-b-t10 | 17 / 163 | 0.0645% | 0.3861% | pass | pass |

Percentages in the two rotor columns are relative to **mg/4**, the nominal hover force scale per rotor. They are rounded displays of exact saved error intervals, not percentages measured on real aircraft. The stress tier is 1e-2 of the applicable force/torque normalization; it has not been justified as a physical tolerance. All four load categories and all three tiers remain in [the complete readout](analysis/summary.json).

There are two findings to keep separate:

- **Real approximation error:** the first two flight-start states have about 6.17% and 6.59% normalized rotor error. The strict 1e-8 test fails in all six states. We stop this fixed weakest-tenth deletion route; we do not quietly reduce its fraction or choose easier states.
- **Conservative-bound slack:** four later snapshots pass the direct stress-tier comparison, but only the two 10-second snapshots pass the bound. The 5-second states demonstrate that this particular certificate can be too cautious. That does not explain away the starting-state errors.

We also checked whether throwing away the omitted contributions' lower bounds makes the certificate worse. It does not on this panel: the full-contraction and upper-only certificates have identical local factors, global factors, root boxes and error intervals in all six states. The prospective [mathematical note](review/PROSPECTIVE-BC-EQUALITY.md) explains one sufficient condition for that equality. In 146 rows, the upper-only contraction interval is strictly wider despite the identical certificate. Some rows do not satisfy the sufficient condition yet still agree, so it is not a necessary test. Equality here does not mean the two contraction intervals contain the same information or that all future bounds will agree.

The [Three.js snapshot view](viewer/) uses the actual reused 64-drone poses and the actual deleted-interaction mask. The original two Boids flights had aerodynamic feedback off; these are post-hoc load comparisons, not newly simulated trajectories. Links are bookkeeping, not wake streamlines.

Both single-use stages completed normally. The producer passed 15 analytic fixtures; the independent checker passed 29 fixtures and rejected 13 intended corruptions. It checked 12 proposals, 3,072 rotor candidates, 96,768 reference pairs and 4,608 certificate rows. No extra state, retry, precision extension or post-result mask tuning occurred. The runtime/resource observations in [the execution record](EXECUTION-ATTESTATION.md) measure the offline diagnostic, not a browser speedup.

This advances the approximation/evaluation portion of the original eight-step framework. It does not establish a useful 5,000-drone browser approximation, physical validation, novelty or a publishable contribution. The next direction must be separately justified; preserving an approximate contribution instead of replacing it with zero is one possibility, not a demonstrated solution.

[Protocol](PROTOCOL.md) · [Claim ledger](CLAIM-LEDGER.md) · [Independent check](results/check.json) · [Reproduction](REPRODUCTION.md) · [Restart](RESTART-RESULT.md) · [Frozen source](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf)
