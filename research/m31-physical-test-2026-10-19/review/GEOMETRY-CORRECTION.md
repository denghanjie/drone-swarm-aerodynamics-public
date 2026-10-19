# Pre-execution correction of the apparatus length mapping

19 October 2026. Reviewer: `/root/m31_protocol_challenge`.

**Withdraw the earlier unconditional identification R = l. The primary apparatus figures and accompanying alignment statement support l as the horizontal Cartesian half-spacing, with rotor-center radius R = sqrt(2)l for the depicted square layout.** Accordingly, the applicable model diameter is D = 2sqrt(2)l. The earlier protocol acceptance must not be used to launch the radial-l version.

This correction was made before source freeze and before experimental force decoding or model evaluation. The parent is retaining the unexecuted radial-l protocol, source and reviews under `design-history/radial-l-unexecuted`. Their preservation records the design change; it does not make that discarded version an empirical test. The current figure-supported variant is named `Kiran-stacked-projected-arm-fixedPWM-v1`.

## Primary-source reasoning

I visually inspected the official PDF page 3 apparatus render and page 4 render supplied for this review. These are source-page readings, not force-data extraction or pixel-based dimension measurements. The official PDF identity is recorded below.

1. **Page 3, Fig. 3:** the l dimension arrow runs horizontally in the front-view apparatus schematic from the vehicle centerline to the right motor column. It is a projected horizontal lever arm; the drawing does not dimension the diagonal line from the center to a motor in the rotor plane.
2. **Page 4, Fig. 4:** the top view depicts a square/X motor layout, with motors at two horizontal and two transverse coordinates around the body center. The front-view center-to-column distance therefore differs from the full in-plane center-to-motor radius. This is a geometric interpretation of the labeled layout, not a measurement of its schematic pixel scale.
3. **Page 4, force/moment discussion:** the paper says that horizontal separation Δx/l = 2 aligns the upper vehicle's left rotors with the lower vehicle's right rotors. That relation supports a left-to-right motor-column separation of 2l, hence coordinate components ±l. It agrees with the projected dimension in Fig. 3 and the square layout in Fig. 4.

The prose phrase “horizontal distance from the … body center to a motor (32.5 mm)” was previously interpreted as the in-plane radial distance. The figures and the explicit 2l alignment relationship resolve that ambiguity in favor of the coordinate-component interpretation for this test. No external Crazyflie dimensions or later-paper measurements are required for this correction, and none were independently verified here.

In the existing corner convention, the corrected mapping is `arm = l`, with motor centers `(±l, ±l)`, radius `R = sqrt(2)l`, and `D = 2R`. For the stacked specialization, each receiver rotor has radial distance R from the upper source axis. Both the profile's radial argument and its diameter must change together. Keeping radial=l while changing D, or changing the coordinate data's normalization to R, would be inconsistent.

## Consequences for the prospective test

The experimental normalization remains the paper's l = 0.0325 m. Decode physical separation as `z = z_l × 0.0325 m` for every case. Do not reinterpret `z_l` as z/R.

The model's near-height cutoff becomes `2.5D = 5sqrt(2)l`. Consequently the stacked row at 0.21 m is outside the corrected near-domain. Restrict the prospective selected slice to rows 3–13, corresponding to 0.25–1.10 m: 11 nominal predictions and 11 × 81 = 891 finite sensitivity predictions. For the declared sensitivity set, the smallest selected z is 0.249 m, while the largest near cutoff is below 0.231 m. The selected finite set therefore clears the corrected cutoff. These are elementary geometry bounds, not executed model outputs or experimentally established pose-error bounds.

The primary near/far upper contrast becomes row 3 minus row 13. Its predicted value remains zero: the lower vehicle is upstream-excluded from the upper receiver in the declared upright arrangement. This structural result is independent of the numerical isolated-force baseline and does not depend on the discarded radial mapping. The lower predictions do depend on the corrected R and D and must be generated only from the amended source.

The source/receiver induced-scale cancellation remains valid under the existing common-hardware and equal-rotor-force assumptions. No propeller-diameter estimate is introduced by the geometry correction. The fixed-PWM versus ideal-power limitation and the descriptive, uncalibrated uncertainty treatment also remain unchanged.

Controls must use admitted 0.25 m and 1.10 m positions and verify refusal of the now-inadmissible 0.21 m example. The amended protocol/source require a new pinned static review before freeze. There is no reason to execute the discarded radial interpretation as an additional alternative or choose a geometry by force-data agreement.

Source: Kiran, Ayanian and Breuer, *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, RSS 2025, [DOI 10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102), official PDF pp. 3–4, Figs. 3–4 and §III-A. Official PDF identity previously recorded by the parent: SHA256 `e821c65273015921437fafc7b35b4f669ec01f985d965c31d3feeecbffb94932`.

No experimental force values were decoded and no scientific code was executed by this reviewer. This note explicitly supersedes the radial-l geometry assertion in my earlier test-design and protocol reviews.
