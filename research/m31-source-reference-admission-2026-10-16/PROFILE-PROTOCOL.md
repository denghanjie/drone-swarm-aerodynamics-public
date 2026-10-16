# Exposed published-profile transfer audit

Protocol saved before calculating contrasts. This is exploratory descriptive reanalysis of an already inspected figure, not preregistered independent physical validation. Preceding result: source-accounting commit edd2b69773b0544be3270e951ecb56ce768662e8.

## Question

At s/l = 3, how different are the displayed Offboard 1 and Offboard 2 median speed profiles after the paper's independent geometry and hover-speed normalization? Hypothesis to examine: one displayed normalized profile transfers approximately to the other. No numerical accuracy threshold is justified by the available evidence, so this audit reports discrepancies without a physical pass/fail verdict.

Source: Bauersfeld et al., *Robotics meets Fluid Dynamics: A Characterization of the Induced Airflow below a Quadrotor as a Turbulent Jet*, arXiv:2403.13321v3, 12 December 2024, accepted RA-L preprint. Inspect §III-B/D eqs. 1, 7, 8; §IV-A–C; Table I; Fig. 7 and §VI-A. The horizontal axis is r/l, not fitted half-width; vertical is speed/UH, not a fitted peak. UH is calculated using hover weight, propeller area and air density, not independently measured flow. Both frames have tabulated l=0.266 m and propeller diameter=0.1295 m; masses 0.572 and 1.207 kg. Rounded UH values 6.66 and 9.66 m/s support only approximate dimensional illustration.

## Input gate

Use the exact versioned PDF SHA256 81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c. Keep the paper and renders private. Publish factual visible plotted coordinates and our extraction programs, with citation; do not relicense the original publication. Extract the orange Offboard 1 and yellow Offboard 2 median paths only. Exclude fitted black curve, dispersion bands, legends, all invisible path extensions. Coordinates cover 0≤r/l≤3. Each curve has 16 visible original graphical vertices plus one explicitly interpolated clipping endpoint. Original graphical vertices are not claimed to be raw samples or bin centers.

Require independent pdfplumber and pypdf ContentStream extractions to agree within 1e-6 normalized units on all visible knots and attribution. The threshold concerns parser reconstruction only. Stop on failed attribution, missing shared support, nonpositive centerline or nonpositive L2 denominator; do not shrink the domain or repair data silently. Preserve discrepancies/failures.

## Fixed analysis

Let g1(x), g2(x) be piecewise-linear reconstructions on their union of knots, x=r/l. Transfer g1 unchanged; no amplitude, radius, area, offset or peak fitting to g2.

1. Maximum absolute normalized discrepancy max |g2−g1| and every maximizing union knot, including x=0. This is exact for the polylines.
2. Radially weighted relative L2 discrepancy, using Offboard 2 as reference: sqrt[∫_0^3 x(g2−g1)^2 dx / ∫_0^3 x g2^2 dx]. Integrate segment polynomials exactly and independently verify by quadrature. This is asymmetric and weights outer radii more. It is not thrust error, energy loss, or a momentum balance.
3. Each supported centerline value g_j(0), all intersections with g_j(0)/2, and whether the intersection is unique. Use the actual plotted centerline, not a fitted peak or first nonzero bin. Report missing or ambiguous crossings. Comparison of unique half-speed radii is descriptive; do not silently assume monotonicity.
4. Optional dimensional table uses x×0.266 and g×rounded tabulated UH. Transferring to Offboard 2 uses g1×9.66, not a fitted target amplitude. This is an illustration of the published normalization, not independent validation of a square-root thrust law.

Unit checks before analysis: identical curves yield zero discrepancies; linear functions integrate correctly; crossing logic exposes multiple crossings. One finite analysis run, then independent review of saved results with different arithmetic. No search, tuning, stochastic replicates or benchmark claims allocated. Reruns only for demonstrated implementation faults, retaining failed records and deviations.

## Uncertainty and interpretation

The instrument is omnidirectional and measures speed magnitude; processing includes slow-hover filtering, ambient subtraction and grid-cell medians. Fig. 7 shows median lines and 1-sigma bands around means. Those bands are neither SEM nor independent repetitions. Raw samples, per-bin counts, covariance, atmosphere and processing uncertainty are unavailable here. Do not bootstrap vertices or turn line thickness into experimental uncertainty. Record the graphical line thickness in normalized units as display resolution context only; no statistical CI or significance claim.

No equivalence, causal load isolation, motor-command response, shutdown response, 27 g qualification, multi-source superposition, 5,000-drone feasibility or novelty claim follows. This article contributed the existing model's fit: the evidence is exposed and not held out. The audit can constrain the scale of mismatch visible in a compatible published pair and guide a future independent experiment.

## Deliverables and stopping

Publish source/protocol checkpoint before computing contrasts; then preserve values, independent scrutiny, claim/literature ledgers, reproduction commands and a Three.js view of the actual extracted profiles. The view is a static scientific plot, not live fluid simulation; link the existing Boids replay separately. Stop this campaign after the bounded analysis and review. The overarching 5,000-drone accuracy–computation goal remains active.
