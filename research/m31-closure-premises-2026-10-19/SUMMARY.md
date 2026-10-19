# We found a source discrepancy and a better-targeted next test

19 October 2026. This milestone checked assumptions; it did not rerun or improve the model.

Think of the downward airflow as a column of water. To work out how much moves sideways, we need to know how that column changes shape as it travels downward. Matching its downward speed at a few places is not enough to establish the sideways motion.

We checked the original formulas. The older and later papers print different sideways-flow expressions. Their shapes differ as well as their scales, so multiplying one by a single number cannot make them identical. Our implementation agrees with the later expression and the mathematical conservation derivation. **We found no justified coefficient correction to apply.** The discrepancy is documented; it is not a proved typo or evidence that the measurements are wrong.

There is also a concrete measurement gap: the laser measured a slice beside the drone's center. It never measured the central core that the full airflow calculation needs. The updated [3D view](viewer/) shows that missing core in amber alongside the unchanged measurements and errors. The amber cylinder marks absent coverage, not a predicted wake shape.

A useful next test is to consider a hollow sleeve outside that missing core. We can ask whether the air crossing its top, bottom, inner wall and outer wall balances. That can avoid guessing the central flow. It still needs a fixed plan for geometry, symmetry, swirl and measurement error before any calculation. This is a proposed use of a standard conservation law, not a tested or novel result.

The earlier finding remains unchanged:84.03% of the farther paired squared error is opposite-direction error. No new prediction, fit or measurement score was produced. Actual speed calibration, independent experimental validation and swarm behavior remain unresolved.

[Source reconciliation](SOURCE-RECONCILIATION.md) · [Proposed next test](NEXT-TEST.md) · [Verified sources](LITERATURE.md) · [Restart record](RESTART.md).
