# Current-geometry bounds: bounded prior-art review

2026-10-16. **Disposition: the design has clear published antecedents in hierarchical kernel summation, error-controlled approximation, and verified numerical computation. Do not claim those ingredients as new.** The project-specific question is their sound and useful composition with the guarded, candidate-dependent coupled-root problem. This desk review does not establish the priority, correctness, tightness, or computational advantage of that composition.

Exactly eight external connector operations were used, for three selected primary works. Access is now closed under this scope. No PDF or image was opened, downloaded, extracted, rendered, or published; one author-uploaded paper was partially readable as indexed HTML text. No physical-source access was attempted. There was no scientific computation, target-array access, implementation, experiment, contact, new agent, or repository edit. The companion authored access ledger is `m31-current-bound-prior-art-access.json`.

## Verified works and precise reading depth

### W1. Gray and Moore, 2003

**Alexander G. Gray and Andrew W. Moore, “Nonparametric Density Estimation: Toward Computational Tractability,” Proceedings of the 2003 SIAM International Conference on Data Mining, pp. 203–211. DOI: [10.1137/1.9781611972733.19](https://epubs.siam.org/doi/10.1137/1.9781611972733.19).** The publisher verifies this identity; its later online-publication date, 18 December 2013, must not replace the 2003 proceedings year.

Actually visible: publisher heading/metadata and Abstract; [Gray's author HTML](https://www.cs.cmu.edu/~agray/nbody.html), “Multi-tree Methods” and “Kernel Density Estimation.” These describe hierarchical divide-and-conquer for kernel sums and accuracy-controlled non-exact evaluation. The author page specifically identifies a dual-tree method, finite-difference scheme, and hard error bounds. This establishes a close methodological antecedent to avoiding individual kernel evaluations while bounding aggregate error.

**Not read:** the paper's detailed pruning formulas, error allocation, proof, or experiments. The publisher exposes an access boundary after the abstract. Claims of speed on this page remain the authors' claims for their setting, not evidence for the draft or its browser cost. The broad kernel-coverage statement does not verify the project's directed, orientation-dependent guarded wake law.

### W2. Rump, 2010

**Siegfried M. Rump, “Verification methods: Rigorous results using floating-point arithmetic,” Acta Numerica 19, pp. 287–449, 2010. DOI: [10.1017/S096249291000005X](https://www.cambridge.org/core/journals/acta-numerica/article/abs/verification-methods-rigorous-results-using-floatingpoint-arithmetic/770FE58E5293985CCAB770AF09C4F3FF).** Cambridge verifies title, author, venue, pages, DOI, and online date 10 May 2010.

Actually visible: publisher metadata and introductory “Extract,” describing rigorous verification using floating-point arithmetic. This verifies the work's identity and general methodological purpose.

**Not read:** the article body or any interval inclusion, directed-rounding, norm, square-root, nonlinear-system, or contraction theorem. Consequently this task has **not verified a specific published interval-enclosure theorem** for the draft. Rump is an accurately identified verification-method reference, not a citation that discharges the draft's arithmetic obligations. Search results also surfaced a separate short ISSAC item with a similar title; its different DOI and pages were not merged into this citation or admitted as a fourth work.

### W3. Curtin et al., 2013

**Ryan R. Curtin, William B. March, Parikshit Ram, David V. Anderson, Alexander G. Gray, and Charles L. Isbell, Jr., “Tree-Independent Dual-Tree Algorithms,” ICML 2013, PMLR 28(3), pp. 1435–1443.** [PMLR publication record](https://proceedings.mlr.press/v28/curtin13.html). PMLR supplies shortened author names; the [author-uploaded HTML text](https://www.researchgate.net/publication/236203408_Tree-Independent_Dual-Tree_Algorithms) supplies the expanded names and identifies itself as arXiv:1304.4327v1, 16 April 2013. No DOI was displayed in the inspected PMLR record; none is invented.

Actually visible: PMLR abstract/metadata and partial author text through part of §5. Section 2 separates tree, traversal, point-pair base case, and pruning rule. Section 3 defines node geometry and minimum/maximum distance quantities, including conservative bounds. Section 4 distinguishes traversals from pruning decisions. These are concrete antecedents for separating the hierarchy from a problem-specific admissibility/bounding rule.

**Not read:** later paper sections, any KDE-specific error-budget rule, or the remainder of §5. The returned HTML stopped midsection despite listing a longer document. No equation was transcribed from its damaged mathematical formatting. This partial preprint view was not established byte-identical to the published paper.

## Mapping to the project draft

The following is **our comparison with the local draft**, not a claim that any external paper contains the project's equations.

| Draft ingredient | Prior-art implication and remaining project obligation |
|---|---|
| Source hierarchy, node summaries, refine-or-prune traversal | Hierarchical kernel evaluation and pruning are established approaches [W1, W3]. The draft currently clusters sources for individual receiver rows; it is not automatically a dual-tree implementation, which would also organize receiver queries. Do not call it a reproduced dual-tree algorithm without specifying that structure. |
| Boxes for current centers/axes; bounds for `h`, `r`, projection and fades | The use of enclosing node geometry has antecedents [W3]. The draft's anisotropic formula and guards need their own inclusion argument. A Euclidean-distance bound alone does not capture source orientation, near-field rejection, non-unit prepared axes, or original branch precedence. |
| `U_irC * B_C / nu_ir`, with `B_C = sum(beta_j*yhat_j)` | This is a nonnegative weighted-sum upper estimate once its premises hold; counting or aggregating a bounded node contribution is not itself a new algorithm. The particular shape bound and candidate-dependent aggregate are the project's specialization. Their dependencies and disjoint membership must be checked, not asserted by analogy to KDE. |
| Controlled omission | Omission must retain the omitted contribution's enclosure. Setting a small term to zero without accounting for it is a different contract. A published error-controlled kernel method does not automatically choose this model's local load budget or preserve its admission failures. |
| Outward-rounded implementation | A conditional real-arithmetic bound and a floating implementation are distinct. W2 confirms an appropriate established discipline, but the required theorem/implementation details remain unread in this review. The draft must independently justify its endpoint arithmetic and exceptional-value policy. |
| Coupled-root and force/moment certificate | The local corollary propagates a complete current row-contraction enclosure through the candidate root defect and global factor. This is additional to direct kernel-sum estimation. The external passages read do not supply that bridge, but their silence cannot establish its novelty. |

Node upper bounds need not attain their extrema simultaneously; that affects tightness rather than basic inclusion if each nonnegative factor is bounded correctly. This is reasoning about the draft's premises, not a theorem newly verified in the external texts. Conversely, positive weights do not remove interval dependency, arithmetic error, or a loose global maximum.

The candidate source amplitudes are functions of the proposed root vector, not independently fixed physical weights. The aggregate must therefore correspond to the same current candidate and current motor normalization used by the residual certificate. A geometry-only tree cache cannot silently supply a candidate-dependent sum. The draft correctly says that rebuilding/reaggregation and refinement belong in complete query cost.

## What would make the coupled-root bridge defensible

The meaningful prospective contribution is not “trees make a kernel sum faster.” It is an inspectable composition with these explicit obligations:

1. **Target:** choose exact-real geometric coefficients on declared prepared inputs, or rigorously enclose the actual legacy rounded computation. An interval for an exact formula does not certify native `Math.hypot` results or branch behavior. Maintain a separate legacy-discrepancy account if the target changes.
2. **Admission:** certify guard precedence, self exclusion, nonoverlapping membership, all potentially positive ordering edges, whole-source-domain caps, and positive-term resource rules before accepting omission. Unresolved is not zero. Existing field rejection must not be converted into numerical success.
3. **Complete contraction:** include retained singleton work and every omitted node in a bound for the same current complete row sum. Account for current candidate-derived amplitudes and exact weight normalization through sound enclosures.
4. **Nonlinear transfer:** invoke the inherited root-defect corollary only under its actual assumptions, including positive lower residual enclosure and the source-domain bridge. A small approximate-matrix residual alone is insufficient. One loose row can make the global factor unhelpful.
5. **Practical value:** count tree construction, all node checks, candidate-dependent passes, outward arithmetic, refinement, fallback, solution, and load/certificate consumption. Soundness does not imply useful tightness or subquadratic work; difficult geometry can require full refinement.

These are proposed conditions for later review, not completion of the mathematical or implementation review in this task. No measured result follows.

## Comparator and claim consequences

Retain F as the strongest admitted implementation baseline and add an equally lean exact hierarchy H sharing the chosen representation/traversal. Compare bounded omission B against **both** under a common returned-output and admission contract. This separates benefit from ordinary exact spatial enumeration from benefit attributable to certified approximation. A comparison only against the historically slower grid would not establish the latter.

The new local query clarification corrects an ambiguity in my preceding planning note: **timed L/F calls already disabled dense symbols**. Dense tensors belonged to separate qualification builds. Their removal is not a prospective saving. The real common-interface issue is whether omitted sparse coefficients, graph details, exact residuals, and rejection/count metadata must still be produced. Changing those tasks requires explicitly matched, requalified baselines; it cannot be hidden under a familiar method name.

Suggested cautious claim wording:

> We study a current-state hierarchical enclosure for this specified guarded coupled-load model, combining source-cluster bounds with an inherited root-defect certificate. Hierarchical kernel approximation and verified numerical methods are antecedents. This checkpoint proposes a conditional composition; it establishes neither a new general hierarchy method nor validated implementation, physical accuracy, or speed.

A later originality claim would need fuller access to the closest error-controlled kernel algorithms and interval/residual methods, a comparison of exact assumptions and certificates, and matched implementation evidence. This eight-operation review is not exhaustive and does not identify the globally closest work or prove absence of the same composition. No correction/retraction-status search was performed; none of the three works receives a claim of current-status clearance from silence.

## Exact access inventory and closure

External operations, each counted once:

1. Search: `Gray Moore "Nonparametric Density Estimation" "Computational Tractability"`.
2. Open Gray's author HTML: `https://www.cs.cmu.edu/~agray/nbody.html`.
3. Open SIAM W1 publication page: `https://epubs.siam.org/doi/10.1137/1.9781611972733.19`.
4. Search: `Rump "Verification methods" "Rigorous results using floating-point arithmetic" 2010 interval`.
5. Open Cambridge W2 publication page (URL in W2).
6. Search: `"Tree-Independent Dual-Tree Algorithms" Curtin 2013`.
7. Open PMLR W3 publication page: `https://proceedings.mlr.press/v28/curtin13.html`.
8. Open W3 author-uploaded HTML view (URL in W3).

Search results incidentally exposed PDF snippets, bibliographic records and other titles. No PDF link, image, cited work, or download was followed, and these incidental items were not admitted as additional evidence. Reinspection/filtering of already-returned text used no external operation. Publisher access limits and the partial HTML endpoint remain unresolved, with zero operations remaining. No acquisition is requested or implied here.

Local content read: three current-checkpoint drafts/notes plus one existing file, within the fourteen-existing-file cap. Paths are exact and relative to the public repository root; local machine paths are deliberately omitted. File-name listings exposed names only.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-current-bound-design-2026-10-16/PROSPECTIVE-SCOPE.md` | 2741 | `fc13783c7331466becb0649db86b57455d9401ee2556a3698da1e58ae2f13461` |
| `research/m31-current-bound-design-2026-10-16/DERIVATION-DRAFT.md` | 9835 | `e1bd9faf15a76f5b8b2acccb4bdce34b6f5fdc0bf292cbabb079127b606fb014` |
| `research/m31-current-bound-design-2026-10-16/QUERY-CONTRACT-CLARIFICATION.md` | 2037 | `f34915372d63570c4ebb419b5130ac015e887f8a696ea7f7e38fea2575dd2585` |
| `research/m31-root-defect-planning-2026-10-16/ADOPTED-DERIVATION.md` | 4242 | `dd1afefb4cefb4f10176cb2ba2fae25024e28116ce7c78d73fa152e3ea29104c` |

The last file's corollary is inherited local conditional theory. Its linked draft/reviews were not opened for this prior-art task, and this report does not replace the independent mathematical challenge. No full-paper assets, raw connector-return dumps, personal contact details, or private filesystem paths are included in the public-safe deliverables.
