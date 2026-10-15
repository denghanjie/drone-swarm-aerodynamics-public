> Public edition of the 7,892-byte frozen plan. Initial status is historical; see PROTOCOL-HISTORY.json.

# Prospective 2026 scale-retaining velocity screen

2026-10-15. NOT ADOPTED. No measured marker coordinates or model predictions have been extracted. Independent review and root adoption precede collection. Completed 2025 studies remain unchanged.

## Question and frozen observations
Does the unchanged Bauersfeld law transfer in amplitude to this documented 32 g configuration, conditional on nominal geometry, normalization and measurement quantity? Preselected before viewing measured values: neighborhoods zeta=z/l of 7, 11 and 15, each +/-0.5. Include ALL identifiable measured filled-centerline markers whose coordinate intervals intersect a window, including its boundary. Keep actual coordinates and full bounds; flag partial eligibility. No nearest selection, clipping, fitted-curve substitution, anchor normalization or model-based exclusion.

At most 12 distinct points total; excess, duplicate neighborhood membership or an empty neighborhood stops rather than subsamples. If no interval is wholly inside its window, flag that marginal bounds do not guarantee eligibility, without claiming jointly feasible emptiness. Preserve membership evidence and source-coverage limits; never invent unplotted points.

Interpret 7/11 as developing-profile diagnostics and 15 as the approximately self-similar stratum under Kiran Section 3.3. All exceed the original model floor, which alone does not prove self-similarity. Report every point and stratum regardless of outcome.

## Source and prospective method change
Use only Kiran, Ayanian and Breuer, arXiv:2608.30900v1 (31 August 2026 PREPRINT), Fig. 5(a), diagonal cut. SOURCE-LEDGER.md records provenance, CC BY 4.0 and unknown raw-data availability. Peer review and raw-measurement independence are unverified.

Asset: https://arxiv.org/html/2608.30900v1/centerline_decay_width_growth_a.svg
128212 bytes; SHA256 7c3860c3ff421aee0abc8e3ad830b81dba92ef271d721d00f66f937754075425.
SVG viewBox 0 0 675 527.695; HTML display 476x373. A 675-pixel-wide readiness rendering verifies complete axes/legend; pixels are not the analysis coordinate system.

This prospectively replaces the UNADOPTED raster/shared-scale draft with vector extraction and fixed kappa scaling. Source identity, legend and marker-local shape were inspected, but no data-marker positions were extracted. No raw-data repository was accessed; this exact SVG was obtained directly from the public article.

## Series identity and bounded vector collection
The data group is g[clip-path="url(#clip_16)"]. Its 37 gold fill="#fabf2e" paths exactly match the filled-centerline legend path in g[clip-path="url(#clip_19)"]. Each is the same cubic circle, local center (-4.5,0). Its brown outline is #af8620; red #990d26 rings are maxima. The black dashed path is a fit. Assign stable IDs using document-order gold-path index plus original XML hash; retain each selected path/transform verbatim.

Verify the exact local path and full ancestor transform chain. The marker transform has form matrix(1,0,0,-1,e,f), giving viewBox center (e-4.5,f). Unexpected geometry, noncircular paths, ambiguous series identity or missing transforms stops collection. Never infer values from red rings or the fit. Overlap does not invalidate an independently identifiable encoded gold path; record it and that vector coordinates recover the published symbol, not raw measurements.

Freeze two linear tick-pair calibrations per axis: x labels (0,20) and (5,15); y labels (0,2) and (0.5,1.5). Identify tick/axis coordinates from vector paths and verify label alignment visually. Preserve path IDs, transforms, values and four coordinates per axis. No marker values or fitted curve determine calibration.

Use predeclared +/-0.01 SVG-unit descriptive bounds on each transformed tick position and marker center, plus 1e-12 arithmetic padding in normalized outputs. These bound representation/rounding only, not experimental or symbol-placement accuracy. Confirm coordinate decimal quantization <=0.001 SVG unit and transformation arithmetic error <=1e-6 SVG unit; otherwise stop rather than enlarge bounds after data. Two independent parses of selected transforms must agree within 1e-6 SVG unit.

Require a common feasible affine map for all four tick constraints per axis, positive x and negative y slope. Retain the shared-map feasible set; propagate bounds via extrema over it, not independent exact fits. Empty/unbounded calibration, inconsistent labels or unsupported nonlinearity stops. Report centers from the outer tick pair and bounds from all feasible maps. A second independent implementation checks calibration extrema before release.

Read all 37 x coordinates only for inclusion/exclusion bookkeeping; extract y values only for selected gold markers. Freeze source, calibration, selected XML, coordinates, bounds, membership and hashes after ONE collection pass. Independent extraction review precedes evaluation. No recollection after predictions.

## Nominal physical mapping and normalization
Kiran's l=46 mm is center-to-motor distance; rotor diameter is 45 mm. Bauersfeld's opposite-motor length D_B=2l=92 mm, distinct from rotor diameter and the old 2025 projected-arm convention 2sqrt(2)l. On the diagonal TRUE centerline r=0, so s/D_B=zeta/2. Require every lower zeta bound >=5 exactly, equivalent to the unchanged kernel floor s/D_B>=2.5.

Keep original dimensionless C=10.11, S=0.07668 and virtual origin=-5.817:
q(zeta)=normalizedWake(zeta/2,0)=10.11/(zeta/2+5.817).
Do not insert Kiran's fitted B=6.02, effective diameter 2.29l or fitted origin.

Freeze m=.032 kg, rho=1.29 kg/m^3, R=.0225 m, g=9.81 m/s^2. Original hover scaling U_H=sqrt(mg/(8*rho*pi*R^2))=4.373329400265024 m/s; the source reports U_i approximately 4.36 m/s. Thus kappa=U_H/4.36=1.0030572018956476. PRIMARY comparison is measured v=u_c/U_i against kappa*q. The 0.306% mismatch is a disclosed nominal normalization inconsistency, not measured uncertainty or a fitting allowance. Never select a normalizer by residual.

Dimensional displays use observed 4.36*v and predicted U_H*q. A different or point-dependent source normalization stops. No geometry/metrology bounds are invented: results are conditional on printed nominal inputs.

## Released evaluation and interpretation
After adoption, frozen extraction and independent review, require separate root release. Use public wake.cjs at commit 1336f5c416875a9651f92b58b2ed06649f25b04e, SHA256 fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc. Verify immutable inputs before importing.

Exactly 3N<=36 scalar calls: center and both coordinate endpoints per point. Since dq/dzeta=-10.11/[2*(zeta/2+5.817)^2]<0, endpoints enclose fixed-nominal predictions. Report each paired residual v-kappa*q and interval [v_low-kappa*q_high,v_high-kappa*q_low], padded by 1e-12. Multiply residuals by 4.36 for m/s. Report neighborhood unions/hulls OF THESE PAIRED DIFFERENCE INTERVALS. Shared calibration dependence remains; hull overlap does not establish joint agreement.

Bauersfeld's omnidirectional sensor averages speed magnitude, while Kiran measures mean axial PIV velocity. Even zero mean lateral flow on axis does not equate these under fluctuations. Experimental uncertainty, nominal parameter uncertainty and stitching errors remain unquantified. Vector precision cannot resolve them. No statistical pass/fail, safety threshold or arbitrary practical tolerance: this is a conditional preprint-based amplitude-transfer screen.

## Budget and stops
Total retained campaign cap 500000 bytes; PLAN <=8000 bytes. Measure before writes. One collection and one evaluation pass, separately released; preserve failed gates. No PDF, paid compute, installs, dataset-repository access, new experiment, fitting or public source-figure redistribution. No raster fallback without new prospective method adoption. Stop after one bounded report.
