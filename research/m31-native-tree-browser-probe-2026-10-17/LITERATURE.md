# Literature boundary

This preparation uses the already verified [tree qualification literature record](../m31-native-tree-design-2026-10-17/LITERATURE.md), the [machine-readable filter bibliography](../m31-filter-design-2026-10-17/review/literature/bibliography.json), and the [M31 restart bibliography](../m31-restart-2026-10-15/literature/sources.bib). No new priority search or new physical-validation claim is made.

- Green (2010), *Particle Simulation using CUDA*, revision 1.3, pp. 4–7: established spatial neighbor-search practice. This motivates avoiding distant candidate visits; it does not establish a benefit for this tree or browser workload.
- Brönnimann, Burnikel and Pion (2001), DOI [10.1016/S0166-218X(00)00231-6](https://doi.org/10.1016/S0166-218X(00)00231-6), §§1–3.2: conservative filtering with fallback. This informs the refusal/omission discipline, not an aerodynamic result or proof of our implementation.
- ECMA Number-operation passages cited in the verified record: declared binary64 rounded arithmetic. Their applicability must still be checked in the actual saved execution.

The experiment adapts established ideas. Numerical equivalence, compression fidelity and runtime behavior require the prospective experiment in PROTOCOL.md. The tree is not claimed novel. A publication gate requires a new, appropriately scoped closest-prior-work audit and additional evidence.
