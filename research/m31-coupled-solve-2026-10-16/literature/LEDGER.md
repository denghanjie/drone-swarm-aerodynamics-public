# Coupled-map mathematical antecedents

2026-10-16. Bounded desk review: three discovery queries, two reference identities, no numerical execution. This is not a priority or novelty search. The source-strength law remains a hypothesis; the results concern a frozen mathematical dependency structure, not physical validation.

## Verified log-coordinate antecedent

**Feyzmahdavian, Johansson and Charalambous, _Contractive Interference Functions and Rates of Convergence of Distributed Power Control Laws_.** The read text is [arXiv:1201.3740v2](https://arxiv.org/html/1201.3740v2), dated 30 May 2012; its [record](https://arxiv.org/abs/1201.3740) identifies the journal publication as _IEEE Transactions on Wireless Communications_ 11(12), 4494–4502, December 2012. The journal version itself was not compared.

Exact read locations:

- §II-A, Proposition 1: contraction of a closed invariant subset gives a unique fixed point and a geometric error bound.
- §IV, Theorem 6 and Corollary 1: the conjugacy `log(I(exp(z)))` and metric `max_i |log(p_i/p'_i)|` connect positive-map scaling to contraction analysis.
- §V, Definition 3 and Corollary 2: two-sided scalability removes the increasing-map requirement and gives strict distance reduction in that metric.
- §V, Definition 4/Theorem 8: a separate uniform additive contractivity condition gives existence and a convergence rate. Mere strict distance reduction does not supply these conclusions.

These are close published antecedents for the mathematical method. They do not analyze the rotor closure or establish its one-half constant.

**Application boundary, from our contract analysis.** The proposed map is order-reversing, so the increasing-map assumptions in the paper's standard-interference results must not be imported. The applicable final step is the general contraction principle, applied to `G(z)=log(F(exp(z)))` on the closed invariant set `(-infinity,0]^N`, after independently establishing the stated Jacobian row-sum bound. The two-sided framework explains why a logarithmic metric need not require an increasing original map; it does not replace that bound or the domain proof. Do not describe the negative-valued log map itself as a positive interference function.

The factor one half, force-error translation, handling of a zero-coordinate start, and inner-root numerical-error accounting remain parts of the local contract argument. The literature does not identify hardware control with ideal power, justify fixed wake shape, or validate unchanged support under thrust scaling. No claim of novelty is made for the transformation, contraction argument, or residual-based reasoning.

## Topological-evaluation antecedent: verification incomplete

**A. B. Kahn, _Topological sorting of large networks_, _Communications of the ACM_ 5(11), 558–562, 1 November 1962.** [DOI 10.1145/368996.369025](https://doi.org/10.1145/368996.369025).

The indexed publisher record supplies this identity and describes a general topological-ordering procedure. Both the publisher PDF and DOI-page requests returned HTTP 403. Consequently the algorithm body and exact method passage were **not read**. This is a historical/bibliographic antecedent only in this ledger; do not claim its precise algorithm was verified, quote its steps, or attribute a modern complexity statement to the unread paper.

The local mathematical implication remains an elementary dependency argument: if every admitted edge decreases a fixed rank, the dependency graph has no directed cycle. With a unique local output once predecessors are known, evaluating vertices in that order resolves each dependency once. This statement is our explanation, not a passage verified in Kahn. It presupposes correctly admitted edges and fixed dependencies; rejected near-field interactions cannot become zero edges, and state-dependent support requires renewed analysis. The geometric rank proof and rotor-specific closure are not supplied by the sorting citation.

## Disposition

One relevant mathematical framework was verified in full at its stated theorem locations. The topological-sort reference was verified only at indexed bibliographic/abstract level. The bounded search is closed rather than expanded to a third reference. No author contact, source archive, dataset, computation, repository edit or scientific run occurred. This ledger reports antecedents and limits, not an exhaustive literature result.
