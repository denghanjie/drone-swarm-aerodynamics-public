# SUPERSEDED BEFORE EXECUTION

The following proposal is retained for provenance only. Its figure-screen window was rejected by the normalization audit before any experiment or digitization. See [the correction](NORMALIZATION-CORRECTION-2026-10-13.md). Do not execute this version.

Original content follows.

# Proposed next physical-model falsification screen

Status: proposal saved 2026-10-13, after the retrospective audit. No simulation, digitization or model calibration has run under this proposal. A new execution protocol must select one branch below and freeze its inputs before any outcomes are inspected. No completed experiment ID is assigned.

## Decision

Prefer a tiny static force/moment comparison if legitimate raw measurements and required metadata become available. Until then, use a separately labeled qualitative/interval-valued published-figure screen to test a necessary shape property. A flock run cannot answer the present physics question more directly.

The most relevant accessible paper is [Kiran, Ayanian and Breuer, RSS 2025](https://arxiv.org/html/2507.09463v1). The associated [Brown dataset record](https://repository.library.brown.edu/studio/item/bdr:rnnfmt6u/) is identified by DataCite metadata but returned HTTP 403. No alternate endpoint was probed after that denial. See DATA-ACCESS.json. No author contact is authorized by this proposal.

## A. Preferred raw-data static receiver test

Question: can the present wake-plus-receiver surrogate predict operational force and pitch moment for a stationary pair under documented physical conditions, within a predeclared useful-error screen?

1. Inputs gate. Obtain raw repeats or numerical means plus defensible uncertainty; coordinates, frames, calibration/tare, vehicle geometry, propeller radius, mass, actuation, units and data license. Verify raw-file hashes. Stop this branch if essential metadata is absent. The paper alone does not provide a complete machine-readable calibration record.
2. Match geometry explicitly. Existing code: mass 0.027 kg, rotor-center coordinates (±0.028, ±0.028) m, rotor radius 0.023 m, opposite-motor distance 0.07919595949 m. The physical comparison uses the independently documented geometry. Do not silently reinterpret the paper's center-to-motor length as an opposite-motor distance.
3. Preserve the candidate with SHA-256 6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189. Primary branch is an unmodified transfer screen. If needed, create a separately hashed geometry-matched fork as a diagnostic, with no fitted response or wake coefficients. Differences in voltage/RPM versus assumed ideal induced power are an applicability question, not hidden calibration freedom.
4. Bounded matrix, selected before reading load values: target Δz/l = {8, 12.5, 19} and Δx/l = {0, 2, 4}, where l is the measurement's center-to-motor length. Use directly measured conditions only; nearest available coordinate may differ by at most 0.5 mm. Missing conditions remain missing. If fewer than six conditions remain, stop rather than interpolate into an apparently full test.
5. Controls: isolated hover; no-source/zero-inflow code branch; stacked zero pitch by symmetry; lateral far control. Compare total lower-vehicle Fz/W and My/(Wl), with sign/frame independently checked. Preserve upper-vehicle data as a useful diagnostic, not an extra fit target.
6. Primary engineering rejection screen: absolute force error greater than max(0.05 W, conservative 95% measurement-plus-metadata error bound), or moment error greater than max(0.02 Wl, corresponding bound), in at least two distinct conditions. These are prospective engineering thresholds, not values claimed from the literature. Report every condition, bias, RMSE and worst residual. With three repeats, calculate repeat-level uncertainty, do not treat autocorrelated samples as independent repeats. Never equate fluctuation standard deviation with confidence of the mean without checking its definition.
7. Passing means only that this bounded static screen did not reject the surrogate. It cannot validate dynamic flight, all geometries, three-or-more wakes, yaw torque, walls, turbulence or large swarms. If uncertainty cannot be bounded, report inconclusive even if residuals appear small.
8. Stop after one fixed matrix, no parameter retuning, no trajectory simulations and no timing claim. CPU prediction budget: 60 seconds; generated diagnostic output below 10 MB; raw acquisition budget must be set after a file inventory is visible. Any fit is a later separately frozen experiment with independent held-out configurations.

## B. Feasible published-figure structural screen while raw access is blocked

Question: does the existing isolated mean-wake profile have a qualitative shape conflict in a declared cross-paper normalized region?

The analytic repository profile is strictly decreasing with radial distance for positive downstream centerline speed; its maximum is on the source axis. This is directly inferable from its formula and is not a computational benchmark. The current downstream-domain start is 2.5 opposite-motor distances, equal to five center-to-motor lengths for a square layout.

1. Freeze the consulted arXiv PDF digest and the selected panel: Kiran Fig. 7(b), with domain/normalization checked against III-A and III-B1–2. Work from the licensed arXiv version, not an unverified web image. Record CC BY 4.0 attribution if any derived image is distributed; do not include the full article in the package.
2. Select all distinguishable plotted axial slices with 5 < z/l < 6.5 before reading their radial curves. If no labeled slice can be unambiguously located, stop with an extraction/access limitation.
3. Digitize each selected curve twice independently from a saved rendering. Record pixel coordinates, axis calibration, image resolution, line width, curve-overlap ambiguity and coordinate-convention uncertainty. Verify the PIV-plane offset from Fig. 4; an off-center planar slice of an axisymmetric radially decreasing profile remains center-peaked along the slice, but coordinates must be mapped explicitly. These are figure-derived values, never raw measurements. Do not extrapolate to invisible points or attach the paper's PIV instrument precision as the digitization uncertainty.
4. Falsification target: an off-axis local mean maximum exceeding the on-axis value by more than the complete conservative extraction interval at two resolved adjacent radial samples, in at least one selected profile. Verify both sides where visible. This tests unimodality only. If interval overlap or axis-location ambiguity prevents the comparison, report inconclusive.
5. If rejected, state precisely: the mean-profile family cannot represent this published near-merge shape under this explicit geometry mapping. This does not establish the magnitude of force errors for the repository's different geometry or validate another model. Retain the cross-vehicle mismatch prominently.
6. If not rejected, draw no physical-validation conclusion. Stop after the selected panel; do not tune a new near-field continuation from the same plot. This is a screening result supporting which raw measurements to prioritize.

## Deferred follow-on

Only after a static screen and reliable data access, use approach/retreat matched-position force records to test the memoryless response separately. First ensure both states lie inside the declared model domain; excluding unsupported near-wake cases must not be called a successful dynamic prediction. A successful implementation-equivalence benchmark is never the physical reference for any of these tests.
