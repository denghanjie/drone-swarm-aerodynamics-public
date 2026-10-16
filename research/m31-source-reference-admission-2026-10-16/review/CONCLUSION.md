# Independent saved-profile result review

Accepted for the stated descriptive arithmetic scope. All 38 checks passed in one bounded review, using the previously extracted pypdf visible coordinates. The review plan was saved before this independent calculation; the author's result values had already been seen. No original analysis function was imported or rerun.

Source commit `37750e0ea4d929ac7bb414a7636cfebaea3f3c2a`, the published source-manifest hash, all 29 committed manifest entries, current required analysis/protocol/input files, and result provenance fields agree. The independent pypdf input retains SHA-256 `fc9a0bc90dd50912dc95d7a96f5c39ee1089e2ea294164db86656c3b6e0ad09d`. The reviewed saved result has SHA-256 `deae09799d9cc28701b934f17c648fe3f5ed46af11c0e7b94d3914bee14ea9fe`.

| Quantity | Independent result |
|---|---:|
| Maximum absolute normalized discrepancy | 0.25814683134600147 |
| Sole maximizing normalized radius | 0.38095222496350667 |
| Radially weighted relative L2, Offboard 2 reference | 0.24069936659545974 |
| Weighted squared-difference integral | 0.01105874827645825 |
| Weighted squared Offboard 2 reference integral | 0.19087808873318002 |
| Offboard 1 half-centerline radius | 0.44870459064565726 |
| Offboard 2 half-centerline radius | 0.5591573742129753 |

Two-point and three-point Gauss-Legendre rules were applied separately to each of the sixteen union intervals, for 80 quadrature abscissae total. Both integrands are cubic on each interval, so this is independent of the author's polynomial-antiderivative implementation. The two rules agree within the fixed numerical tolerance, and both agree with the saved integrals and asymmetric L2 value.

All seventeen saved union knots and all associated g1, g2 and signed-difference values were independently checked. The largest absolute saved-versus-independent knot-field discrepancy is 2.3314683517128287e-15. The maximum is attained at only the reported union knot. Both profiles have exactly one half-centerline intersection; each is downward, bracketed by original graphical vertices 2 and 3, with no threshold plateau. No global monotonicity assumption was used.

This review uses only the sixteen visible original graphical vertices plus the labeled clipping endpoint for each curve. It does not read hidden path extensions, acquire new physical data or reinterpret graphical vertices as independent raw observations. The recorded maximum and L2 quantify the two exposed reconstructed median polylines; the L2 denominator is Offboard 2 and the result is asymmetric. They are not thrust error, a momentum balance, a confidence interval or a physical rejection threshold. The reviewed result correctly retains null experimental confidence intervals and null physical pass threshold. No significance, causal isolation, independent physical validation or novelty follows.

The review remained within 30 s CPU and 2 MiB output limits. Files contain no local private paths, source paper, figure image or hidden path coordinates. The accompanying script and raw checks preserve the calculations and exact input hashes.
