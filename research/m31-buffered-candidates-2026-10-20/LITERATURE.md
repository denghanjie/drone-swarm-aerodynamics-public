# Neighbor-list antecedents

Verified on 20 October 2026. This is a narrow check of two primary sources supporting the established neighbor-list idea. It is not an exhaustive novelty search or a systematic review. No paper or documentation file is redistributed here.

## 1. Original research paper

Loup Verlet, **Computer “Experiments” on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules**, *Physical Review* **159**, 98 (1967), published 5 July 1967. [DOI and publisher record](https://journals.aps.org/pr/abstract/10.1103/PhysRev.159.98) · [publisher PDF](https://journals.aps.org/pr/pdf/10.1103/PhysRev.159.98).

The original paper's technical discussion on printed page 99 (PDF page 2, section II) describes constructing tables of nearby particles at intervals and using them between rebuilds. The table radius exceeds the force cutoff; the intervening skin must prevent an omitted particle from entering interaction range before rebuilding. This directly establishes an antecedent for temporal candidate-list reuse. It does not establish a numerical bound, useful skin width, performance gain or physical validity for the present drone-load implementation. Its molecular-dynamics measurements are not transferred to M31.

Verification: the publisher search result supplied author, title, volume, first page, DOI and publication date. The opened six-page publisher PDF supplied the actual neighbor-table discussion (extracted lines 104–126 on PDF page 2). OCR is imperfect, so the attribution above paraphrases the legible algorithmic passage rather than quoting its formula or relying on its empirical velocity estimate as a guarantee.

## 2. Primary implementation documentation

LAMMPS developers, **4.4.3. Neighbor lists**, official developer documentation, stable version showing git info **30Sep2026** when accessed. [Official page](https://docs.lammps.org/stable/Developer_par_neigh.html).

The opening paragraphs describe a Verlet-style neighbor list rebuilt periodically and reused for current force calculations, with neighbor radius equal to force cutoff plus a skin. The documented typical rebuild trigger is an atom moving half the skin distance. The page also describes full versus half lists, binning, and a direct all-pairs list-construction option. These support separating list maintenance from current interaction evaluation; they do not prescribe this project's axis-box rule, ordered directed rows or exact-output contract. Memory use and rebuild frequency remain engineering costs to measure here.

Verification: the official page was opened and its opening list/rebuild description and later construction options were read (extracted lines 12–15, 23–39). It is primary project documentation, not an additional peer-reviewed paper. The stable URL may change later; the displayed version above records the consulted state.

## Use in this checkpoint

The [protocol](PROTOCOL.md) therefore calls this ordinary neighbor-list reuse. The candidate retains possible source IDs while evaluating the current scientific calculation on every query. Its binary64 box-containment and endpoint-subtraction argument must be checked against F's actual component screen; neither cited source certifies it. F/C equality is an implementation-equivalence question, and the eight-stage timing screen measures this particular implementation and recorded workload. No novelty, general speedup or physical-accuracy claim follows from these references.

The earlier saved reuse review considered Ahmad–Cohen and reversible multiple-time-step methods for field/force scheduling. Those are useful historical context but are not substituted for the more directly relevant neighbor-list passages above; see [history](HISTORY.md).

## Bounded access record

The new verification used exactly two search queries in one search call: one restricted to APS for the 1967 paper, and one restricted to official LAMMPS documentation for neighbor-list rebuilding. It then used three primary-page opens: the APS PDF; the official LAMMPS page; and a second viewport of that same page to read its complete short body. No additional searches, secondary-source opens, citation-count assessment, comprehensive correction/retraction search or further browsing was performed. This access allocation is closed.
