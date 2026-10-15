# Independent epoch-2 extraction review

2026-10-15 UTC. **READY for separate root release of 18 scalar model calls**, subject to evaluator review and storage admission. This review verifies frozen extraction only. I did not run the collector, evaluator or aerodynamic kernel, and did not calculate model predictions or residuals.

## Frozen evidence and preserved stop

Verified EPOCH2-FREEZE.json SHA256 `1f7d28e85096abf4f3e4c62633370437dd60bf8bb9bc74e635e4b7aa9614844e`, every input hash, collector hash, and all three output byte counts/hashes. The measurements hash is `00be77aea11b447fa7c69dc097ada01a55e61a84984dd18c8fe5f4b754e42c7f`; calibration is `1cc81f04c9645ca5b73648446d2998e2ea2bec623a37f0875314803fe0ee6963`; selection is `d0c637e97722538be39ab3ee63c7cd95de5db4348dd31cda7c743fda864be20d`.

The original plan, original adoption and GATE-STOP.json hashes remain unchanged. The stopped first epoch is still gate-unverified before marker extraction. Epoch 2 has a distinct adopted exact-decimal method and remains stopped for review in its immutable receipt. Do not edit that historical status when releasing evaluation; use a separate release record.

## Independent source and arithmetic checks

A separate SAX reader verifies 37 gold data paths in clip_16, one matching gold legend path in clip_19, identical local path geometry, expected matrix form, and absence of transformed ancestors. The marker center is exactly (-4.5,0) in local coordinates. All 37 x positions were independently checked; y coordinates were evaluated only for the six selected paths. Selected original XML occurs verbatim in the immutable SVG and its path hashes match.

The eight tick paths, fixed labels, transforms and exact positions match the frozen calibration and the earlier visual axis check. These are the preselected outer and inner pairs, not calibrations selected using data values.

Exact decimals parsed through Decimal/Fraction provide a reference independent of floating agreement. Recomputed maximum floating arithmetic error is 5.2023096941411496e-14 SVG unit, below the inherited 1e-6 gate. The collector's independently parsed matrices agree at floating precision (reported maximum difference zero); that agreement is not used to prove accuracy. Source inspection confirms both gates are enforced separately.

## Independent shared-calibration extrema

The collector enumerates exact intersections for inverse maps p=A*v+B. My verifier instead clips a bounded polygon for the forward map v=a*p+b with rational half-plane arithmetic. Its initial finite rectangle follows from the two separated outer tick envelopes; all four tick constraints per axis are then applied. Positive x and negative y slopes stay bounded away from zero.

Both resulting four-vertex polygons exactly equal the transformed saved feasible sets. For each marker-envelope endpoint, v=a*p+b is linear over this polygon, so its extrema occur at vertices. Taking the two endpoint extrema preserves the full marker envelope. This independently reproduces all 86 lower/upper rational endpoints and all 43 centers: 37 x intervals and six y intervals. Floating outputs also match the specified outward 1e-12 padding exactly. This is a different extrema formulation, not a rerun of the collector.

## Inclusion, normalization and release

The complete selection is:

| Window center | Gold path IDs | Actual z/l centers |
|---|---|---|
| 7 | 12, 13 | 6.615031, 7.141514 |
| 11 | 20, 21 | 10.826885, 11.353368 |
| 15 | 27, 28 | 14.512259, 15.038739 |

All six full x intervals lie inside their assigned windows; none has partial eligibility or duplicate membership. The other 31 intervals do not intersect any window. Each neighborhood has two points, below the total cap of 12. All lower x bounds exceed 5, so later evaluation endpoints satisfy the stipulated model domain. No point was substituted from an open ring or dashed fit.

The frozen geometry is l=0.046 m, opposite-motor D=0.092 m and r=0. Rechecking only the requested nominal normalization gives U_H=sqrt(0.032*9.81/(8*1.29*pi*0.0225^2)) and kappa=U_H/4.36=1.0030572018956476, matching the frozen definition. No wake expression was evaluated. The later amplitude comparison remains v against kappa*q, not v against q.

Six selected observations imply exactly 18 later kernel calls at centers and endpoints. Keep the source law and nominal inputs unchanged. No recollection or selection changes are justified by subsequent predictions.

The +/-0.01 SVG-unit envelopes are chosen graphical sensitivity conventions. They do not establish historical exporter precision, symbol-placement accuracy, PIV confidence, nominal-parameter uncertainty or physical agreement. Retain the mean-speed versus mean-axial observable caveat and separate developing 7/11 from approximately self-similar 15. A passed extraction review establishes numerical fidelity to published symbols only.

Verifier: `check-epoch2.py`; its hash and check summary are in `EPOCH2-CHECK-RECEIPT.json`. No frozen source or collection output was modified.
