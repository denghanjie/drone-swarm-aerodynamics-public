# Literature and experiment map

The unchanged aerodynamic assumptions and verified source limitations are inherited from [the restart bibliography](../m31-restart-2026-10-15/) and the [cadence physical-data review](../m31-airflow-cadence-2026-10-15/). DESIGN-REVIEW.md preserves the relevant model audit and data compatibility concerns. Agreement of two implementations cannot validate those assumptions.

Arnold Neumaier (1974), *Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen*, ZAMM54(1),39–51, DOI10.1002/zamm.19740540106, supplies the compensated accumulation diagnostic. Publisher metadata and the author's scan were checked; p40, §2IV, Eq.(IV,1) specifies the update and p45 discusses conditional analysis. [Exact verified source note](compensated-summation-source.md), [BibTeX](sources.bib). The current diagnostic does not establish a formally certified floating-point bound or algorithmic novelty.

The frozen question is independent implementation agreement, not a replication of an aerodynamic measurement paper. No physical-validation conclusion is made from the reported loads. Future source-omission methods need a separate verified prior-work map and prospective experiment.
