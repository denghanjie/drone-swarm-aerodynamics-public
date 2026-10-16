# Literature and experimental ancestry

No new external source acquisition or exhaustive novelty search occurred in this cycle. Reuse the previously verified readings and their access/version limitations. bibliography.bib contains machine-readable records; source texts are not redistributed.

| Source | Specific use and boundary | Provenance |
|---|---|---|
| Nyland, Harris & Prins2007, *Fast N-Body Simulation with CUDA*, GPU Gems3ch31,§§31.2–31.4,31.6; technical book chapter | Established data-reuse/batching background. CUDA gravity performance does not establish JS sparse wake performance or originality. | [Prior reading](../m31-restart-2026-10-15/literature/annotated-ledger.md), [primary chapter](https://developer.nvidia.com/gpugems/gpugems3/part-v-physics-simulation/chapter-31-fast-n-body-simulation-cuda). |
| Bauersfeld et al., arXiv2403.13321v3,§§III-D/IV,Eq8; accepted RA-L manuscript with year/version caveat | Inherited fitted single-source wake shape.27g scaling, finite support, projection, source-total coupling and ideal-power receiver are unvalidated local assumptions. | [Verified source receipt](../m31-source-accounting-2026-10-16/literature/SOURCE-RECEIPT.json), [primary record](https://arxiv.org/abs/2403.13321v3). |
| Feyzmahdavian, Johansson & Charalambous2012, arXiv1201.3740v2,§§II-A/IV/V | Inherited contraction/log-map antecedent. No changed solver or aerodynamic validation from wireless experiments. | [Verified readings](../m31-coupled-solve-2026-10-16/literature/LEDGER.md), [read version](https://arxiv.org/html/1201.3740v2). |
| Kahn1962, *Topological Sorting of Large Networks*, DOI10.1145/368996.369025; metadata/abstract only | Known ordering antecedent only. No attribution to unread full text. Current solver uses explicit descending-height/ascending-ID order. | [Prior access record](../m31-coupled-solve-2026-10-16/literature/SOURCE-ACCESS.json), [DOI](https://doi.org/10.1145/368996.369025). |

The closest implementation antecedent is the repository's already published DOT exact-efficiency scalar-lean kernel and its mixed reuse/support results at1336f5c416875a9651f92b58b2ed06649f25b04e; see [builder design](../m31-post-cost-decision-2026-10-16/BUILDER-DESIGN.md) and review/KERNEL-STATIC.md. This is prior internal work, not a novel literature result. L and T both receive its relevant known lean concepts, while preserving the newer coupled model's original arithmetic.

Implementation: source/kernel.cjs with byte-pinned anchor and reference. Planned experiment:m31-typed-assembly-2026-10-16, fresh fixed cases/config. Outcome: pending; no gain or agreement inferred from prior work. Physical data access remains a separate inactive question in the decision package, with no new acquisition, transcription or scoring here.
