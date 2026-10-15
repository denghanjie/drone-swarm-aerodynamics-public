# Physics source ledger

Checked 2026-10-15 UTC. Three primary papers were read beyond their abstracts. No dataset was downloaded and no flight/model experiment was run for this literature review. Publication metadata and the version actually read are distinguished below. Bibliographic records are in `references.bib`.

## B: Bauersfeld et al., mean hovering-quadrotor jet

Read: [arXiv v3 HTML](https://arxiv.org/html/2403.13321v3), [v3 history](https://arxiv.org/abs/2403.13321), and Fig. 2 visually via the [original SVG](https://arxiv.org/html/2403.13321v3/main-figure1.svg).

Evidence: III-A assumes a hovering source; Fig. 2 defines opposite-motor length. Eqs. (1), (3)-(9), VI-C specify induced-velocity normalization, radial profile, inverse axial decay, width growth, and fitted constants. IV-B/Table I uses uncanted fitted vehicles spanning 230 g-6.3 kg. IV-C stabilizes for 5 s and excludes source speeds above 0.1 m/s; autonomous measurement heights reach 3 m, with a larger Matrice measurement volume. V/VI locate the merged far field after approximately 2.5 motor distances. VI-B, Fig. 9/Table II find tail overprediction for xi>2 and noise domination beyond xi>5. VII-A Eq. (11) concerns extra ideal power at maintained hover thrust; its throttle mapping is vehicle-specific. VIII leaves boundaries/crossflow as extensions.

Version/status: v3, 12 December 2024, is the read preprint. [Publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1109/LRA.2024.3518835), read successfully as JSON, verifies the final RA-L issue: 10(2), 1241-1248, February 2025, DOI 10.1109/LRA.2024.3518835. The arXiv journal field says 2024; do not conflate this with final issue year. IEEE's web page required human verification; no challenge was attempted.

## G: Gielis et al., aggregate forces

Read: [arXiv v1 full text](https://arxiv.org/html/2312.03488v1), especially Sections 2-6, Eqs. (1)-(2), Figs. 4-7 and Table 1.

Evidence: Eq. (1) sums pairwise forces; Eq. (2) permits nonlinear aggregation. Sections 3.0.1-3.0.2 describe a powered receiver on a load stand and 0.5 m/s formation passes. Section 4.3/Figs. 5-6 show formation-dependent merging and failure of linear force addition; Section 4.1 reports measurement/mount limitations. Section 6 limits velocity coverage and extrapolation beyond observed neighbor counts. This directly motivates an independent aggregation test; it does not by itself reject velocity addition followed by a nonlinear receiver law.

Version/status: [arXiv history](https://arxiv.org/abs/2312.03488) has v1 dated 6 December 2023. [Springer's primary record](https://link.springer.com/chapter/10.1007/978-3-031-63596-0_35) verifies ISER 2023 proceedings publication on 6 August 2024, SPAR 30, pp. 393-404, DOI 10.1007/978-3-031-63596-0_35. Final chapter full text was not accessed; byte identity with v1 is not asserted.

## K: Kiran et al., independent Crazyflie measurements

Read: [arXiv v1 full text](https://arxiv.org/html/2507.09463v1), II-A, III-A/B/C, Eqs. (1), (3)-(9), Figs. 3-16 and Tables I-II. Figs. 3, 4 and 9 were visually inspected.

Evidence: II-A uses tethered 4 V/PWM operation, not regulated rotor speed. III-A defines l=32.5 mm and weight approximately 0.265 N; this l differs from B's motor diagonal. Fig. 4 samples through front-rotor centers, away from the vehicle's central axis. Fig. 9 provides measured velocity markers; Fig. 7(b) provides lateral profiles. Table I contains fitted coefficients, not independent validation targets. III-C/Figs. 15-16 demonstrate history-dependent force loops, largely in very close proximity. Those loops cannot validate an instantaneous far-field-only model.

Version/status: v1 dated 13 July 2025; [official RSS proceedings](https://roboticsproceedings.org/rss21/p102.html) verify authors, title, 2025 publication and DOI 10.15607/RSS.2025.XXI.102. No byte-equivalence claim between proceedings and arXiv.

## Dataset access and small-data alternative

K links [dataset DOI 10.26300/64d4-wa17](https://doi.org/10.26300/64d4-wa17). Public [DataCite metadata](https://api.datacite.org/dois/10.26300/64d4-wa17), successfully read, identifies *Force, Moment, and Velocity Dataset for Quadrotor Downwash*, creators Kiran/Ayanian/Breuer, Brown University, 2025, at [Brown's record](https://repository.library.brown.edu/studio/item/bdr:rnnfmt6u/). Its rightsList, sizes, formats and version fields are empty. The DOI landing returned HTTP 403; the direct Brown page was also inaccessible through the web tool. No CAPTCHA or alternate data route was attempted. Exact license, file list and sizes remain unknown. This is the same DOI cited by K; whether it matches any earlier repository-roadmap candidate cannot be confirmed without that candidate's identifier.

Fig. 9 is readable enough for a future five-marker screen. Exploratory inspection included marker pixel locations before the formal screening plan was frozen; no extracted coordinate dataset is retained and no model predictions or residuals were calculated. Formal collection remains prospective outside this checkpoint; it must not be described as blind to all prior visual inspection. The PNG is not redistributed. No rights for the blocked raw dataset are inferred from article availability.

