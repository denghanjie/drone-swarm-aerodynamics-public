# Prescribed support-crossing comparison
15 October 2026. Saved-output audit passed.
**NO_FIXED_VARIANT_DOMINANCE** (Q/C words 0/0); no resolved grid reversals.
This does not establish L dominance.

Cases 0..3: (refresh H, phase phi) in ms:
(1.25,0), (1.25,0.625), (5,0), (5,2.5). Each spans 0.5 s.
Z=hold, L=linear, Q=quadratic, C=restricted cliff. All use the same causal
sample history; C retains raw Q shadows during holds. Fine/coarse steps:
0.078125/0.15625 ms. Original guarded aerodynamic operator is the reference.

Fine summaries: peak U and leakage in m/s, integral U in m:
|Case|L peak U|Q peak U|Q integral U|Q leak peak|C leak peak|
|---|---:|---:|---:|---:|---:|
|0|.00102767|.000860767|.00000690940|.000422913|.000422913|
|1|.000970923|.00103393|.00000703483|.000315297|.000259607|
|2|.0118305|.0135240|.000341879|.00723378|.00350853|
|3|.0118096|.0113121|.000342822|.00665224|.00665224|

Q lowers all 12 discrete U, force/weight and moment/(weight*arm) accuracy
integrals versus L; C also lowers all 12. L's U integrals are
.0000644139, .0000646800, .000911845, .000921087 m.
Q worsens peak U in cases 1/2 and peak normalized force in case 1.
C has additional 5 ms peak penalties. L has zero sampled delivered leakage
but 148/184/640/648 negative raw scalars; Q/C have none yet leak in every
case. C reduces leakage integrals versus Q, without eliminating leakage.
Leakage is beyond compact model support, not physical zero.
The fixed-variant, both-grid criteria fail despite integral wins.

26,000-byte [evidence](EVIDENCE.bin), [audit](POSTRUN-REVIEW.md),
[protocol](../research-operator-successor-plan/PROTOCOL.md), [viewer](demo.html).
Viewer reads saved values; serve the pinned public checkout over HTTP.
Browser/WebGL rendering remains unverified; fallback decoder checks passed.

Literature/experiment ledger: [CHOPtrey](https://arxiv.org/html/1610.09261v2)
inspired the restricted comparison, not a full-method reproduction.
[Model/prior claims](../../research-decision-20261015/LITERATURE-CLAIMS-LEDGER.md);
[bibliography](../../research-decision-20261015/references.bib).
Sampled operator evidence only: no physical validation, flight or speedup claim.
