# Literature and prospective-claim review

23 October 2026. **Accepted within the documentation scope below.** The literature note and prospective claim ledger retain the verified antecedents, distinguish the three distance-related tests, and leave the new component/radius results conditional. No mandatory citation or claim correction remains in the inspected versions.

This was a local source-and-document review. No new web acquisition, raw-record extraction, aggregate calculation, model import/query, geometric evaluation or timing run occurred. Only `LITERATURE.md`, `CLAIMS.md` and this review were written by this reviewer. This is not independent executable qualification: it does not establish archive identity, numerical counter totals, candidate completeness, audit correctness or result validity. Those remain for the checkpoint's separately allocated checks.

## Reviewed document identities

SHA-256 identifies the exact inspected text. Later edits require reconciliation with this review.

| Document | SHA-256 |
|---|---|
| [Current protocol](../PROTOCOL.md) | `81dc6e99c73f2db0e2caa302fee74a99f2503dbcd8a96d390a9af271865ba610` |
| [Current literature note](../LITERATURE.md) | `4f810c7f26682b74211b2b2deeddeaa7a3c8eef8d67a5afb1834953c11123881` |
| [Current prospective claims](../CLAIMS.md) | `236b1c49e09dbf52d9fadacb36dd9020dfa237a709ce484cdb5619185e4b02eb` |
| [20 October antecedent ledger](../../m31-buffered-candidates-2026-10-20/LITERATURE.md) | `9a514f8e340a5d4146c08d21603c4ef1a29c512e5b44dae78496309a9db52076` |
| [22 October literature note](../../m31-buffered-motion-2026-10-22/LITERATURE.md) | `7fcebb92dd138d2e11b790e487c14f84892e4a9e8e468f34981633683d28b592` |
| [22 October literature/history review](../../m31-buffered-motion-2026-10-22/review/LITERATURE-HISTORY-REVIEW.md) | `ee11b658e8a16301c7b0714f47e61a62350cf03c04c850b47d8a7b65481e7dcc` |
| [22 October summary](../../m31-buffered-motion-2026-10-22/SUMMARY.md) | `6e82e87a311941de770cca169dc0d5b3b5589c06c36eb768d13afd240f34fa93` |
| [22 October result claims](../../m31-buffered-motion-2026-10-22/RESULT-CLAIMS.md) | `d56b7c7c2ad4080c6655f0721a4b4e219f3b456fc1b55221aa1b60e50d512382` |

The protocol was updated during this review; the final hash above identifies the version with the explicit center-distance terminology and saved-CSR structural checks. The earlier version was not treated as the final reviewed version.

## Citation and access check

The current note accurately retains Loup Verlet's 1967 title, *Physical Review* volume 159, first page 98, DOI [10.1103/PhysRev.159.98](https://journals.aps.org/pr/abstract/10.1103/PhysRev.159.98), and 5 July publication date. The substantive attribution is limited to the previously read neighbor-table discussion on printed page 99/PDF page 2/section II. It preserves the OCR caveat and does not turn an empirical molecular estimate into an implementation guarantee.

The LAMMPS citation is correctly labelled official project documentation, with [the stable URL](https://docs.lammps.org/stable/Developer_par_neigh.html) and the previously observed 30Sep2026 git information. The note preserves the 20 October access date and makes clear that the rolling page was not revisited. Cutoff-plus-skin, reuse/rebuild and construction choices are qualitative antecedents, not measured results for M31.

The retained two-query/three-open access record is accurately summarized. Neither a new search nor a comprehensive novelty or correction/retraction audit is implied. The rejection of a novel-neighbor-list claim is appropriate; neither cited source proves this binary64 box rule, exact-output contract or drone physics.

## Implementation terminology and conditional inference

Targeted source-text inspection confirmed the threshold and branch interpretation, without executing it:

| Inspected source | SHA-256 |
|---|---|
| [Candidate cache](../../m31-buffered-candidates-corrected-2026-10-20/source/candidate-cache.cjs) | `9b38064690c2ae5b505cae936d574e3355bcc613b3f69fda8b89ed50732f96ad` |
| [Candidate kernel](../../m31-buffered-candidates-corrected-2026-10-20/source/candidate-kernel.cjs) | `4fea99f4e61bff3c5eb54a0090e50b48e41d4cdf7cff5cdc770a37366f321b19` |
| [Imported anchor kernel/constants](../../m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs) | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| [Imported reference excerpt, targeted center-branch check](../../m31-native-fresh-transfer-2026-10-17/source/vendor/reference-excerpt.cjs) | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |

The cheap threshold-4 check acts on the largest absolute rounded component difference. The candidate cache pads center coordinates by 0.125 with outward rounding and certifies that component rejection through interval endpoint differences; it does not use radius 3 for omission. The imported constant is `neighbor:3`, and the subsequent kernel branch tests `Math.hypot(dx,dy,dz)` after center guards. Later rotor code computes a different lateral `radial` relative to the source axis and includes near-field symbol 4. Calling both quantities simply “radial” would obscure the reasoning; the current documentation and the final protocol explicitly distinguish them.

The lower-bound argument is correctly restricted to eligible saved F outputs and conservative lists using the same component rule. Such lists must include current component survivors `N`, so `P−N` is an optimistic omission ceiling once the prescribed counter identities pass. The documents do not assert that this ceiling is zero before analysis. The previous fully dense list finding is clearly attributed to published history, not presented as a fresh audit or proof of zero component opportunity.

The center-distance diagnostic `N−G−E` is appropriately described as an existing F exclusion. It is not a proved moving-list bound or a saving; a different candidate requires a separate bound and an explicit full-evidence contract. Positive coefficient sparsity and `E−U` are correctly denied safe-omission status, since refusal/status/symbol contributions remain material. Symbol 4 is not reclassified as supported zero.

## Scope of acceptance

The documents preserve the saved-only N64 scope, inherited refusal, conditional branch decision and absence of speed, population, physical or novelty claims. They do not reopen prior allocations or reclassify the earlier failed attempts. Their account of all 4,032 retained pairs relies on the preceding published summary and claims only; no raw results or original journals were recomputed for this review.

Result claims remain pending the new producer and independent audit. Before making unconditional claims, bind them to the checked saved records, preserve status strata and exact counts, and retain all failed attempts and limitations specified in the protocol. This review accepts the literature use and prospective wording only.
