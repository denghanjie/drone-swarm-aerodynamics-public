# Retrospective methods literature audit

Date: 2026-10-13. Four verified primary works. No simulation, benchmark, code change, or publication was performed for this audit.

The exact-equation campaign was already complete when this review began. The bibliography therefore records sources actually read for this audit; it does **not** assert that they were read before implementation or that the frozen campaign was literature-preregistered. The historical source of the controller coefficients, support-envelope derivation and timing estimator remains unverified where no contemporaneous citation exists.

## Deliverables

- `bibliography.json` and `bibliography.bib`: verified titles, authors, year, venue, DOI or institutional URL, consulted versions and metadata discrepancies.
- `literature-experiment-ledger.json`: exact sections/PDF locations, relationship classifications, local implementation and experiment paths with SHA256, findings, failures and untested applicability.
- `verification-log.json`: reading coverage, primary records, correction/new-version checks and access limitations.
- `saved-pipeline-attribution.json`: new arithmetic on an existing record, explicitly distinct from a new experiment.
- `HYPOTHESES.md`: two untested proposals, including one recommended bounded diagnostic experiment.
- `audit-integrity.json`: local-link and hash verification only.

Third-party reading copies and the cache-dependent full-audit builder are not distributed. No redistribution license was established for those copies. Use the primary URLs, consulted-document hashes and location pointers instead. The substantive JSON/BibTeX/Markdown audit is included.

## What changes in interpretation

1. **Boids terminology has a concrete implementation basis.** The controller computes three-dimensional local separation, alignment and cohesion, with a shared broad route and additional wall/pair constraints. Reynolds is the retrospective behavioral comparator, not evidence that current coefficients or safety filters reproduce his implementation. The short existing records do not demonstrate a completed obstacle mission. [Reynolds (1987), author paper](https://www.red3d.com/cwr/papers/1987/boids.html); ledger M01.

2. **Exact spatial filtering is an implementation claim with a bounded domain.** Current full-key Map buckets and sorted strict-radius neighbors differ from Teschner's compressed hash table. The support branch needs its own conservative numerical argument; a spatial-hashing citation cannot supply that proof. Dense occupancy, sorting, allocation and support-test cost remain possible bottlenecks. [Teschner et al. (2003), institutional full text](https://cg.informatik.uni-freiburg.de/publications/2003_VMV_collisionDetectionHashing.pdf); ledger M02.

3. **The reported intervals have a narrower scope than a full benchmarking-method reproduction.** The campaign resamples a small set of paired time ratios and takes a median. This differs from the source paper's mean-ratio method. Process restarts and independence were not dimensioned in the saved protocol. Keep the present descriptive intervals and mixed results unchanged; a later study must use a new plan and results. [Kalibera and Jones (2013), accepted manuscript](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf); ledger M03.

4. **Numerical branch safety remains distinct from algebraic correctness.** The retained huge-translation false cull is directly relevant to the support test. The repaired accepted-domain checks and regressions are valuable evidence; they are not a formal proof of every floating-point branch. Shewchuk's determinant predicates are an analogy, not an implementation dependency or a proof of the wake margin. [Shewchuk (1996), author full text](https://people.eecs.berkeley.edu/~jrs/papers/robust-predicates.pdf); ledger M04.

## Evidence preserved without reinterpretation

- Five variants: legacy, previous-zero, lean, support, reuse. Lean is not a positive-interaction or physics approximation.
- Primary suite: 151 cases passed. Independent suite: 85 fixtures, comprising 78 valid fixtures with bitwise equality and seven matching model-domain failures. Do not describe all 85 as valid aerodynamic cases.
- Short genuine 3D Boids: 14 records; eight matched implementation comparisons. Do not turn their equivalence into long-horizon convergence.
- CPU field and pipeline measurements only. Rendering/replay is separate; no GPU or browser throughput claim.
- Incremental field and whole-pipeline gains versus previous-zero are mixed. Scaling stopped before N=500; no later source citation changes that gate outcome.
- Primary and independent timing scopes differ, including checksum placement, and are not pooled.
- The v0 positive-contribution loss and A2 numerical-domain guard remain visible. No paper retroactively validates physical aerodynamics, superposition, receiver response or the finite wake cutoff.

## Strongest next methods question

Existing primary lean runs devote a median 50.6% of instrumented total time to physics and 17.6% to field evaluation. Controller and safety shares are 20.1% and 10.4%. These are medians of per-run fractions, so they need not sum to 100%; uninstrumented overhead also remains. They apply only to seed 4301, N=16, one simulated second. The underlying record is [the saved primary pipeline record](../../campaign-exact-efficiency/results/pipeline.json), linked and hashed in the JSON analysis.

Before another optimization, test whether the incremental **whole-pipeline** effect is reproducible across process restarts and method order. H1 names the competing explanations and falsification criteria. If fresh results confirm that non-field work limits useful total savings, stop field-only optimization for this goal and prioritize the unresolved physical-model question or a separately justified dominant-stage study. H2 is a lower-priority exact-indexing idea, not a recommendation to launch another tuning campaign immediately.

## Verification limits

The targeted correction searches found no formal erratum in the inspected records; that is not a guarantee that none exists. The 1997 expanded Shewchuk work and fuller Kalibera/Jones report were checked as version metadata, not fully audited as additional citations. Author-hosted reflowed manuscripts have different page numbering from final proceedings; the ledger explicitly uses 1-based PDF leaves. DOI-access errors were handled using legitimate author/institutional copies. This four-paper subset cannot support an exhaustive related-work or novelty claim.
