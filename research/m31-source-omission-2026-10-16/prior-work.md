# Focused prior work: bounded omission of weak wake sources

Verified 16 October 2026 Asia/Shanghai (15 October UTC). Literature inspection only: no scientific computation, model run, service launch, contact, paid access, or publication claim. Candidate remains unselected and unrun.

**Assessment:** the generic idea of reducing pair interactions using spatial contribution bounds and an accumulated error budget is established. The closest verified mathematical precedent below explicitly bounds omitted Gaussian sources and adds their error allowances. Published wake-graph edge pruning also exists, although its inspected threshold is not a cumulative force/moment guarantee. These sources justify a numerical-method analogy; none validates the M28 wake or receiver physics. No absence-of-hits novelty inference is warranted.

## 1. Closest mathematical precedent: per-source budget and bounded Gaussian omission

Vikas Chandrakant Raykar and Ramani Duraiswami, **“The Improved Fast Gauss Transform with Applications to Machine Learning,”** in *Large-Scale Kernel Machines*, MIT Press, 2007, pp. 175–202. DOI **[10.7551/mitpress/7496.003.0010](https://doi.org/10.7551/mitpress/7496.003.0010)**.

Verified against [Crossref's publisher-deposited metadata](https://api.crossref.org/works/10.7551/mitpress/7496.003.0010), the [book editor's contents](https://leon.bottou.org/papers/lskm-2007), and the [author-hosted chapter draft](https://www.umiacs.umd.edu/labs/cvl/pirl/vikas/publications/raykar_LKSM_2006.pdf). The draft filename/year and chapter numbering differ from the final book; locators below refer to that inspected draft.

In §1.8.6, printed pp. 15–17 (PDF pages 19–21), equation (1.27) sets

\[
|\widehat G(y_j)-G(y_j)|\le\sum_i|\Delta_{ij}|\le Q\epsilon,
\qquad Q=\sum_i|q_i|,
\]

and explicitly allocates \(|\Delta_{ij}|\le|q_i|\epsilon\). Equation (1.28) identifies the error of omitting a source's cluster as \(q_i e^{-\|y_j-x_i\|^2/h^2}\). Algorithms 1–2 choose \(r=\min(\sqrt d,h\sqrt{\log(1/\epsilon)})\) on the normalized unit-cube domain, and evaluate only clusters satisfying \(\|y_j-c_k\|\le r+r_x^k\). Retained clusters also have a separate Taylor-truncation condition.

**Transfer limit:** this already supplies the general per-source-to-total error accounting. Its isotropic Gaussian and common bandwidth do not match a tilted, downstream-dependent, faded wake. The actual M28 contribution requires its own proved upper bound; copying the Gaussian distance cutoff is invalid. The normalization is by total absolute source weight, not by each target's true sum.

## 2. Bounding groups of sources and several targets: dual-tree KDE

Alexander G. Gray and Andrew W. Moore, **“Rapid Evaluation of Multiple Density Models,”** *Proceedings of the Ninth International Workshop on Artificial Intelligence and Statistics*, 2003, pp. 117–123. [Official PMLR record](https://proceedings.mlr.press/r4/gray03a.html); [paper](https://proceedings.mlr.press/r4/gray03a/gray03a.pdf). PMLR reissued it in 2021 as volume R4; the research year is 2003. The official record supplies no DOI; none is invented.

Visually inspected PDF pages 3–4, §3 and its dual-tree pseudocode. For query node Q and source node T, the algorithm bounds contribution mass using

\[
d_l'=N_T K_h(\operatorname{maxdist}(Q,T)),\qquad
 d_u'=N_T K_h(\operatorname{mindist}(Q,T)).
\]

It maintains per-query lower/upper density bounds and aggregate log-likelihood bounds \(L_v,U_v\), stopping when \(|U_v-L_v|/|L_v|<\epsilon\). Exclusion, inclusion and centroid approximation are distinguished; pruning need not mean replacing a node by zero. Priority traversal can refine earlier approximations until the requested tolerance is met.

**Transfer limit:** a region containing four rotor targets can similarly support common bounds, but source-axis orientation and the wake's nonuniform downstream/radial dependence require new bounding expressions. The KDE log-likelihood stopping rule is not a force/moment tolerance. This paper is direct prior art for spatial bounds and error-controlled traversal, not rotor aerodynamics.

## 3. Pair-interaction accuracy criteria: strict bounds versus practical estimates

Walter Dehnen, **“A fast multipole method for stellar dynamics,”** *Computational Astrophysics and Cosmology* **1**, article 1 (2014). DOI **[10.1186/s40668-014-0001-7](https://doi.org/10.1186/s40668-014-0001-7)**. [Publisher full text](https://link.springer.com/article/10.1186/s40668-014-0001-7) verifies metadata and equations.

Section 4.1.1, equation (10), gives the single cell-interaction strict bound (in the paper's gravitational units)

\[
\delta a\le {M_A\over r^2}{(p+1)\theta^p\over(1-\theta)^2},\quad\theta<1.
\]

Section 5.3, equation (16a), instead accepts a cell interaction when
\(\theta<1\) and \(\widetilde E_{A\to B}M_A/r^2<\epsilon\min_{b\in B}a_b\).
The paper distinguishes its sharper practical estimator from the strict bound; §4.1.2 documents underestimated errors, and §5.3 reports maxima around ten times the requested parameter in those tests. It also explains why accumulated **absolute** interaction errors matter.

**Transfer limit:** this approximates retained gravity interactions using multipoles rather than simply discarding weak sources. It supports the accuracy-versus-work framing and the need to distinguish proved bounds from estimated errors. Its gravitational kernel, multipole order and acceptance rule cannot be reused as wake guarantees.

## 4. Direct wake-domain precedent: thresholding weak graph edges

Yanfang Chen, Young-Hoon Joo and Dongran Song, **“Modified Beetle Annealing Search (BAS) Optimization Strategy for Maxing Wind Farm Power through an Adaptive Wake Digraph Clustering Approach,”** *Energies* **14**(21), 7326 (2021). DOI **[10.3390/en14217326](https://doi.org/10.3390/en14217326)**. [Primary publisher article](https://www.mdpi.com/1996-1073/14/21/7326).

The publisher's indexed full text supplied metadata, §3.2 equations (8)–(9), and Algorithm 1; direct live requests returned 429/403. Thus this criterion was read from the publisher text exposed by search, not an independently downloaded PDF.

Equation (8) keeps \(w_{ij}\) when \(w_{ij}\ge\epsilon_k\), otherwise replacing it by zero; \(\epsilon_k=k\epsilon\). Equation (9) defines the base threshold via the geometric median of wake weights. Algorithm 1 and the following discussion choose suitable k by comparing power output and computation time, then build lookup tables.

**Transfer limit:** this is explicit prior wake-edge pruning for wind-farm communication/clustering and optimization. The inspected rule is a per-edge threshold selected by performance comparison; it does not supply the proposed sum-of-omitted-bounds certificate or four-rotor load bound. It cannot establish that those narrower features are novel, either.

## What an M28 adaptation would actually need to prove

The following is a conditional mathematical specification for the candidate, not an experimentally established result or a claim attributed to these papers. For fixed states and the selected nonnegative linear-superposition mode, let \(u_{jr}\ge0\) be source j's inflow contribution at receiving rotor r. If an omitted set O has valid bounds \(u_{jr}\le B_{jr}\), define \(b_r=\sum_{j\in O}B_{jr}\). Then \(0\le U_r-\widehat U_r\le b_r\). A bound \(B_j\ge\max_{r=1,\ldots,4}u_{jr}\) is sufficient but potentially looser.

Given a separately justified receiver-law Lipschitz constant \(L_r\) over the entire admissible inflow interval at the fixed nominal motor state,

\[
|\Delta f_r|\le L_rb_r,\quad
|\Delta F_z|\le\sum_rL_rb_r,\quad
|\Delta\tau_x|\le\sum_r|y_r|L_rb_r,\quad
|\Delta\tau_y|\le\sum_r|x_r|L_rb_r.
\]

These are triangle-inequality and Lipschitz propagation; moment signs must not be treated as nonnegative merely because inflow sources are. Freeze separate force and moment budgets, units and reference axes. The root-sum-square overlap mode needs its own derivation. Bounds must cover all four actual rotor positions, source/receiver orientations, wake support and fading, and must preserve model-domain checks even for sources later omitted. Arithmetic rounding of a computed upper bound also needs treatment before calling an implementation certified.

**Existing model and implementation stay distinct from the candidate.** Read-only inspection of `outputs/milestone-28-source/aero.cjs:4,12–16` confirms an existing grid/neighbor search, downstream fade/cutoff at 2/2.5 m, radial fade/cutoff at 2/3 half-widths, 3 m neighbor radius, and near-wake/tilt domain gates. Spatial pruning already exists in the project's main lineage; do not call that new. The finite-support/fade choices are already model assumptions. Any additional omission budget should first be measured against the same full sum of that frozen finite-support model; it does not bound the physical wake beyond those cutoffs.

A fixed-state force/moment bound does not certify trajectory error, stability, controller success, domain coverage between samples, or physical accuracy. Nor does a cheap-looking bound establish speedup: the cost of constructing, checking and accumulating bounds must be included. The defensible framing is an implementation and evaluation of established error-controlled summation ideas for this specific model, with novelty and physical transfer still unresolved.

## Access record

- Gray–Moore official PDF: HTTP 200; 241,944 bytes; SHA-256 `4d1e01a9b3e5cc1c3e7f4d170df4087927c1a1399147b5634ca436a453f38037`; local `/tmp/m31-gray-moore-2003.pdf`. Garbled text extraction was replaced by visual reading.
- Raykar–Duraiswami author draft: HTTP 200; 728,541 bytes; SHA-256 `fc9afe0e7d279b3a4774c151d75899593f29a38791c39bc6c4c19ce5b840c9da`; local `/tmp/m31-raykar-duraiswami-chapter.pdf`. Relevant equations and algorithms were checked visually. Final-book metadata came from Crossref/editor; the final publisher page was inaccessible.
- Dehnen: accessible publisher HTML, §§4.1–5.4 read; no PDF download needed.
- Chen et al.: primary publisher content available through search; live page access blocked as stated above. No site challenge bypass or access payment.
- An additional Applied Energy wake-sparsification lead, DOI `10.1016/j.apenergy.2021.117986`, has verified metadata but inaccessible full text; it is not used for an algorithm claim here.
