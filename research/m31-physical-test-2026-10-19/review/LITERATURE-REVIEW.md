# Focused primary-source review — 19 October 2026

**The newly verified 2026 paper is useful wake evidence, but it does not currently supply an accessible, independent raw two-drone load test. Keep RSS 2025 / Brown DOI 10.26300/64d4-wa17 as the direct-measurement target.** No numerical experiment, fitting, digitization, installation, author contact or access-challenge bypass was performed. Only this original review is retained publicly; no third-party paper/data body was copied into the package.

## Newly verified primary source

Kiran, Ayanian and Breuer, *The Structure of Merging Turbulent Jets Beneath a Small Quadrotor*, [arXiv:2608.30900v1](https://arxiv.org/abs/2608.30900v1), submitted 31 August 2026. This is a verified preprint identity, not an asserted journal publication.

The [primary full text, §2](https://arxiv.org/html/2608.30900v1#S2) describes tethered single-Crazyflie planar PIV, diagonal and front-rotor cuts, five stitched sections, and 1000 image pairs. Parameters: mass 32 g, center-to-hub arm length 46 mm, rotor diameter 45 mm, density 1.29 kg/m³; velocity scale is actuator-disk hover induced velocity. The domain extends approximately −1.5≤z/l≤17.5. Profiles outside |r/l|≤3 are extrapolated for visualization. [§3.2](https://arxiv.org/html/2608.30900v1#S3.SS2) reports diagonal-cut merging at z/l=5, effective diameter 2.29l, and fitted B=6.02, S=0.088, z₀/D_eff=−3.42.

No data-availability statement, dataset DOI, raw PIV link or analysis repository was found in the inspected primary HTML. A targeted search verified no author/institutional release. This does not prove data do not exist.

Raw-record independence from the cited 2025 front-cut study is unestablished.

## Direct-load source, reverified rather than newly acquired

The [RSS XXI proceedings page](https://www.roboticsproceedings.org/rss21/p102.html) verifies *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, the same authors, and DOI [10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102). Its associated [primary manuscript, arXiv:2507.09463v1, §I-A](https://arxiv.org/html/2507.09463v1#S1.SS1), explicitly links [Brown dataset DOI 10.26300/64d4-wa17](https://doi.org/10.26300/64d4-wa17).

[§II-A](https://arxiv.org/html/2507.09463v1#S2.SS1) describes ATI Nano-17 force/torque transducers on both vehicles, a translation-stage separation matrix, 20 kHz sampling for 30 seconds per position, and three trials. Motors use 4 V and hover PWM; rotational frequency is not held constant. PIV and load measurements are separate experimental sets. [§III-A](https://arxiv.org/html/2507.09463v1#S3.SS1) normalizes thrust by W≈0.265 N and moment by Wl, with l=32.5 mm. These are direct bench-load measurements, unlike estimator-derived interaction residuals.

Accessibility differs by interface. This reviewer's normal DOI, DataCite and Brown-landing opens returned web-tool errors. However, the parent reviewer reports successful ordinary IAB navigation to the [official Brown landing page](https://repository.library.brown.edu/studio/item/bdr:rnnfmt6u/) on 19 October, without a manual CAPTCHA action or bypass. The page identifies the 2025 *Aerodynamic Interaction Dataset Measuring Quadrotor Downwash Forces, Moments, and Velocity Profiles*, the authors, RSS association and CC BY 4.0 license, and exposes an [official ZIP](https://repository.library.brown.edu/storage/bdr:rnnfmt6u/ZIP/). These browser observations are attributed to the parent, not independently reproduced by this reviewer. The old blanket access blocker is superseded for that interface; archive contents, measurement associations and calibration have not yet been verified in this review.

## Consequences for the requested physical test

The source-level kernel constants in `research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs:3–4` are mass 27 g, rotor-coordinate half-spacing 28 mm, rotor radius 23 mm and density 1.225 kg/m³. Its `arm` is a Cartesian rotor coordinate: rotor centers are `(±arm,±arm)`, while `R=sqrt(2)*arm`. These are facts from retained local source, not fresh measurements.

Therefore, dimensional geometry and normalization must be bound explicitly before comparing either paper with the kernel. In particular, the two papers' reported `l` values cannot be silently treated as the kernel's `arm`. A change in fitted jet constants would also constitute calibration, not independent validation. This is our methodological inference from the inspected definitions.

Admission disposition: the 2026 source can motivate a bounded single-wake comparison if independently identified measurements become available. It presently adds no verified raw load dataset or independent two-drone holdout. The officially exposed 2025 archive is the actionable candidate; actual physical validation still requires inspecting its measurements and binding separation, frame/sign, baseline, calibration and uncertainty associations. Previously reviewed Neural-Swarm residual-label records are inherited material and are not newly upgraded to direct force observations by this literature finding.
