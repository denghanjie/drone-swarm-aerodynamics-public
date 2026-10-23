# Neighbor-list antecedents and the density question

23 October 2026. This checkpoint reuses the two primary sources verified on 20 October; it performs no new literature acquisition. The retained [antecedent ledger](../m31-buffered-candidates-2026-10-20/LITERATURE.md) records the actual access, imperfect PDF OCR and rolling documentation version. The [buffered-motion literature note](../m31-buffered-motion-2026-10-22/LITERATURE.md) and [literature/history review](../m31-buffered-motion-2026-10-22/review/LITERATURE-HISTORY-REVIEW.md) retain the same limits. This is a narrow antecedent check, not a comprehensive novelty, priority or correction/retraction review.

## Retained primary sources

**Loup Verlet (1967).** *Computer “Experiments” on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules*. *Physical Review* **159**, 98; published 5 July 1967. [DOI and publisher record](https://journals.aps.org/pr/abstract/10.1103/PhysRev.159.98) · [publisher PDF](https://journals.aps.org/pr/pdf/10.1103/PhysRev.159.98).

The retained reading of printed page 99, PDF page 2, section II describes constructing neighbor tables at intervals, with a table radius beyond the force cutoff, and using them between rebuilds. This establishes an antecedent for temporal candidate-list reuse. The access record identifies the relevant extracted lines as 104–126. Because OCR was imperfect, this account paraphrases the algorithmic passage; it neither quotes an uncertain formula nor imports an empirical molecular velocity estimate as a guarantee for drones. The paper does not establish this implementation's binary64 bound, buffer width, speed or aerodynamic validity.

**LAMMPS developers.** *4.4.3. Neighbor lists*, [official stable developer documentation](https://docs.lammps.org/stable/Developer_par_neigh.html), displaying git info **30Sep2026** when read on 20 October 2026.

The retained reading covers a Verlet-style cutoff-plus-skin list, periodic reuse and the typical half-skin movement trigger, together with full/half lists and binning/direct construction options. The access record identifies opening lines 12–15 and later lines 23–39. This is primary project documentation, not another research paper. Its qualitative discussion separates list maintenance from current interaction evaluation; it supplies no measured cost for this project. The stable URL is rolling and was not rechecked on 23 October. It does not certify this project's axis-box omission rule or exact-output contract.

The original bounded access used two search queries and three primary-page opens. That acquisition is closed. Neither source is redistributed here, and neither supports a new-method claim: neighbor-list reuse is established prior art.

## What the implementation's thresholds mean

The following is a local source interpretation, not a claim attributed to Verlet or LAMMPS. It is based on the retained [candidate cache](../m31-buffered-candidates-corrected-2026-10-20/source/candidate-cache.cjs), [candidate kernel](../m31-buffered-candidates-corrected-2026-10-20/source/candidate-kernel.cjs), and imported [anchor constants](../m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs).

| Test | Meaning in the present software | What a tighter buffer can establish |
|---|---|---|
| Threshold 4 component screen | A cheap current-pair check rejects when the maximum absolute rounded coordinate difference is at least 4, within the stated screen domain. | Stored boxes can certify that this same component rejection continues to hold while centers remain in their boxes. |
| Threshold 3 center-distance filter | After the center norm and its guard, `center >= c.neighbor`, with `c.neighbor = 3`, excludes the pair before rotor classification. `center` is `Math.hypot(dx,dy,dz)` between drone centers. | Shrinking boxes around the threshold-4 rule does not create a bound for this separate Euclidean test. |
| Rotor wake-axis classification | Later code uses the lateral distance named `radial`, relative to the source axis, with down-distance, near-field and other checks. | This is a different quantity from the radius-3 center-distance filter and cannot be inferred from center-list density alone. |

The existing candidate stores each center in an outward-rounded axis-aligned box built from center ±0.125. It omits a directed pair only when an interval endpoint subtraction certifies that at least one current rounded coordinate difference meets the threshold-4 rejection. Reuse requires current centers to remain inside their stored boxes; identity changes, box exits and fallback conditions have separate handling. This is a component-screen buffer, not a physical wake boundary. Smaller padding would alter the conservative envelope and rebuild behavior, but would retain the same underlying rejection predicate unless a new rule were explicitly designed and reviewed.

For an eligible saved F output, the [protocol](PROTOCOL.md) defines `P = n(n−1)` and `N` as actual center norm calls. After the prescribed counter checks, `N` is the number of current directed pairs surviving the component screen. Any conservative list based on that same screen must retain these survivors. Thus `N` is an optimistic lower bound on list size and `P−N` is an upper bound on the number of pairs that such a list could omit at that state. Stored-box extent and outward rounding can retain additional pairs. This implication concerns the specified component rule, not every possible exact-model candidate construction.

If the saved diagnosis finds `P−N = 0` at every selected stage, shrinking that component buffer cannot remove pairs on these clips. That is a conditional statement pending the saved-record analysis. The prior [summary](../m31-buffered-motion-2026-10-22/SUMMARY.md) and [result claims](../m31-buffered-motion-2026-10-22/RESULT-CLAIMS.md) report that every candidate list retained all 4,032 directed pairs. Dense padded lists alone do not identify whether padding or the underlying component screen caused this; no new counter totals are inferred here.

## What center-distance exclusions would and would not show

The protocol's `radialRejected = N−G−E` counts rejection by the existing **Euclidean center-distance** test after center-guard rejections `G`, with `E` denoting center-eligible pairs. The term “radial” in that diagnostic must not be confused with the later wake-axis lateral distance. Nonzero center-distance exclusions would identify work already filtered by F. They would not establish a valid reusable moving bound, net savings or measured acceleration.

A future center-distance candidate would require its own justified conservative bound and an explicitly reviewed equivalence contract. The current scientific/status/symbol evidence and protected diagnostic counters cannot silently be discarded. Positive coefficients alone are insufficient: unsupported near-field symbol 4 and invalid classifications can affect refusal even when they contribute no positive coefficient. Likewise, the saved positive-coupling edge count `U` does not make `E−U` a safe-to-omit count.

All threshold and support statements describe this model's software semantics. They establish no physical cutoff for real wakes, aerodynamic accuracy, flight safety, larger-swarm scaling or population performance. The new checkpoint is a descriptive diagnosis of the same saved N64 stages; it is neither a new numerical run nor an independent sample. Literature, pair counts and list density cannot substitute for an implementation-equivalence review or a cost measurement.
