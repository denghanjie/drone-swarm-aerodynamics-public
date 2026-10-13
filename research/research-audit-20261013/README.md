# Evidence and literature audit — 13 October 2026

This audit is retrospective: the exact-equation efficiency experiments were completed before this expanded literature review. It does not rewrite their preregistration or claim a literature-inspired method was tested when it was not.

## What the audit changes

1. **Correct a reporting count.** Three of twelve independent nonzero cases, not four, passed both the ≥10% median speed-improvement criterion and the upper-confidence-bound criterion versus previous-zero. Four passed the median criterion alone. The primary eight-of-twelve result is unchanged. Raw measurements and code are unchanged. [Correction](../campaign-exact-efficiency/CORRECTIONS.md), [claim ledger](claims/claims.json), [recalculated evidence](claims/audit-results.json).
2. **Separate model provenance from model validation.** The inherited far-wake kernel cites Bauersfeld et al.; that citation does not validate this project's fixed-power receiver response, finite support, overlapping-wake sum or tilted-wake extension. Its tested vehicle range also differs from this project. [Physics ledger](physics/literature-experiment-ledger.json), [Bauersfeld et al., equations 1 and 3–9, Table I](https://arxiv.org/html/2403.13321v3).
3. **Reject an inappropriate proposed comparison before running it.** Kiran et al.'s projected-length geometry and motor-distance conversion make the proposed near-merge figure window ineligible under the conservative interpretation of our model's far-field limit. The original proposal is retained and marked superseded. This is a protocol correction, not an experimental rejection of either paper or model. [Normalization audit](physics/NORMALIZATION-CORRECTION-2026-10-13.md), [Kiran et al., Figures 3–4 and section III-B1](https://arxiv.org/html/2507.09463v1).
4. **Keep performance inference narrow.** Repeated inner timings do not by themselves establish process-independent performance. The current paired median-ratio bootstrap is not a reproduction of Kalibera and Jones's published mean-ratio inference. [Methods ledger](methods/literature-experiment-ledger.json), [Kalibera and Jones, sections 3, 6, 7 and 9](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf).

## Records

- [Research charter](RESEARCH-CHARTER.md) and [verified-literature policy](RESEARCH-REQUIREMENT-11.md).
- [Claim–evidence audit](claims/AUDIT.md): 17 scoped audited claims; five historical claims explicitly not re-audited.
- [Physics bibliography](physics/bibliography.json), [methods bibliography](methods/bibliography.json), and [methods BibTeX](methods/bibliography.bib).
- Combined machine-readable [bibliography](bibliography.json) and [literature–experiment ledger](literature-experiment-ledger.json).
- [Physics literature–experiment ledger](physics/literature-experiment-ledger.json) and [methods ledger](methods/literature-experiment-ledger.json).
- [Access and verification records](physics/verification-and-access.json), [dataset access limitation](physics/DATA-ACCESS.json), [methods verification log](methods/verification-log.json).
- [Completed campaign report](../campaign-exact-efficiency/REPORT.md), [actual-record Three.js replay](../campaign-exact-efficiency/demo/index.html), [reproduction instructions](../campaign-exact-efficiency/README.md).

The repository replay must be served locally; the separate offline HTML attachment bundles its dependencies and records. It is recorded playback, not live simulation or a GPU benchmark. Rendered browser verification remains unavailable; static source/data integrity checks are separate.

## Search and interpretation limits

This is a targeted seven-paper audit spanning mean wakes, multirotor interaction experiments, local flocking, spatial filtering, numerical predicates and CPU measurement. Primary full-text locations and bounded correction/version checks are recorded per source. It is not an exhaustive novelty search or a publication-readiness determination. Reading caches are excluded from distribution; the linked source versions remain authoritative.

The related experimental dataset is identified, but raw observations and reuse terms were not acquired. No physical-validation result follows. Numerical reference convergence and compatible independent measurements remain priority gaps. Proposed future tests are unexecuted unless a later experiment record explicitly says otherwise.
