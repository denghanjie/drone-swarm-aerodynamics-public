# 2026 primary-source readiness ledger

Public edition, checked 2026-10-15. This records the historical readiness checks; the completed 18-call experiment is documented in literature/LITERATURE-EXPERIMENT-LEDGER.md.

## Bibliography and status

Anoop Kiran, Nora Ayanian and Kenneth Breuer, “The Structure of Merging Turbulent Jets Beneath a Small Quadrotor,” arXiv:2608.30900v1, submitted 31 August 2026. DOI: 10.48550/arXiv.2608.30900.
Primary record: https://arxiv.org/abs/2608.30900
Technical version: https://arxiv.org/html/2608.30900v1
The inspected arXiv record lists v1 and no journal reference; peer review is unverified. The HTML identifies CC BY 4.0. License: https://creativecommons.org/licenses/by/4.0/ . No figure redistribution is authorized in this campaign.

## Located evidence

- Section 2, Eq. (1), Fig. 1: 32 g Crazyflie 2.1; arm l=46 mm runs center-to-hub; rotor diameter 45 mm; density 1.29 kg/m^3; hover induced velocity approximately 4.36 m/s. Diagonal plane A contains the true axis and opposing hubs.
- Section 2: stitched planar PIV, five sections, domain approximately z/l=-1.5 to17.5; tethered hover. No plotted-mean experimental uncertainty budget located.
- Section 3.2, Fig. 5(a): measured centerline filled circles; open circles are in-plane maxima; dashed curve is fitted. Section 3.3 calls profiles at7/11 developing and approximately13 onward self-similar.
- Table 1's comparison footnote uses an ambiguous unit on Bauersfeld's10.11; use original model definitions. Sections3.1.1 and3.1.3 disagree on which cut merges earlier; do not base the test on that ordering.

## Access and limitations

HTML fetched in memory:331,225 bytes; SHA256 ddbfee970c3b331965e853d43b82d690bac050c4e8b4f9074b44fb6d68ed6d16. No PDF downloaded. HTML advertises Fig.5(a) as a476x373 SVG:
https://arxiv.org/html/2608.30900v1/centerline_decay_width_growth_a.svg
Exact SVG fetched 2026-10-15T04:02:14.684379+00:00: 128,212 bytes, SHA256 7c3860c3ff421aee0abc8e3ad830b81dba92ef271d721d00f66f937754075425. Native viewBox is 0 0 675 527.695 (the HTML display size differs). Existing Inkscape rendered a 675-pixel-wide readiness PNG: 72,814 bytes, SHA256 269156d9fa82eb8f70652e606275a6f396fb839add2c327820d71998c16fab8b. Full axes and legend are readable. Structural inspection confirms 37 gold marker paths have exactly the legend filled-circle local shape, distinct from red open maxima and the dashed fit. No measured marker positions or predictions had been extracted at that readiness snapshot; the subsequent separately adopted experiment is now complete. No source-figure redistribution is authorized.

No dataset DOI/link, data-availability statement or supplement was found in the inspected HTML. Raw-data access, license and size therefore remain unknown; do not assume the2025 Brown dataset contains these measurements. No raw-data repository was accessed.

Treat this as a distinct documented32 g configuration. Do not pool it with the2025 approximately27 g source, repair that source's normalizer retroactively, or assume raw-measurement independence/reuse without evidence.

## Original-model authority

Bauersfeld et al., arXiv:2403.13321v3, Fig.2 and SectionsIII-B/III-D/VI-B, Eqs.(1),(7)–(9):
https://arxiv.org/html/2403.13321v3
Its length scale is opposite-motor distance; induced-velocity and dimensionless coefficient definitions are the authority, not the2026 paper's comparison footnote.

## Frozen nominal scale and quantity caveat

Using printed m=.032 kg, rho=1.29, R=.0225 m and explicit g=9.81 gives U_H=4.373329400265024 m/s, whereas the text reports approximately4.36. The prospective prediction on that printed plot scale is kappa*q, kappa=1.0030572018956476, with no fitted multiplier. This0.306% nominal inconsistency is not an experimental uncertainty estimate. Bauersfeld SectionIV-A averages omnidirectional speed magnitude; Kiran PIV measures axial velocity. Mean lateral symmetry on-axis does not remove the difference under fluctuations.
