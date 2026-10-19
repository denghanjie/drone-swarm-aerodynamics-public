# New independent velocity-data admission — documentary checkpoint

Date: 2026-10-19. Scope: new, independently acquired, compatible quadrotor **signed velocity components**, with usable units, geometry, domain, calibration and public measurement-file access. Reused the prior exclusions; no closed scientific or display evaluation was rerun.

**Decision: NO ADMISSION.** The main new evidence is direct access to Cene's primary conference paper. It resolves an earlier access gap but exposes geometry/domain/observable limitations rather than a qualifying new measurement release. No compliant alternative was verified in this bounded search. This does not prove that no release exists elsewhere.

## Cene 2026 — primary methods now verified; not admitted

Sources: [Liverpool record](https://livrepository.liverpool.ac.uk/3197346/), [ProCap announcement](https://www.procap.tech/publication-on-procap-measurements-on-aerodynamics-of-hovering-drones/), [ProCap download record](https://www.procap.tech/download/february-2026-3af-international-conference-simon-barbe-andrin-landolt-ivan-lunati-and-claudio-mucignat/), [resolved primary PDF](https://www.procap.tech/download/february-2026-3af-international-conference-simon-barbe-andrin-landolt-ivan-lunati-and-claudio-mucignat/?filename=AERO2026_43_A.-CENE_P.pdf&ind=1772455905398&refresh=5bec2157&wpdmdl=5392).

- **Acquisition/geometry:** DJI NEO, four **ducted** rotors, rectangular planform; rotor spacings 60/90 mm; mass 135 g. Independent of the previous RSS acquisition.
- **Units/calibration:** three mean components measured at 50 Hz by a 14-hole pressure probe; optical tracking, motion correction and moving-least-squares reconstruction on a 5 mm grid. Paper reports `UH ≈ 8.3 m/s` from momentum theory and `L = 60 mm`. This is not a complete pointwise uncertainty certificate.
- **Observable/domain:** still-air Fig. 4a shows vertical `w/UH` only at `z/L = −2`; Figs. 4b/c show **magnitude** `U/UH` with vectors. The paper distinguishes `u,v,w` from magnitude. No compatible far-field signed-component array was verified.
- **Files/license:** ProCap lists one attachment, `AERO2026_43_A. CENE_P.pdf` (3.27 MB), while its aggregate header says 4.19 MB. The accessible file is a ten-page paper, not measurements. Liverpool search metadata lists accepted manuscript `AERO2026_043_CENE.pdf`, about 3 MB, Creative Commons Attribution; license version and measurement-data license remain unverified.
- **Failure:** no raw-field inventory; ducted rectangular geometry; near-wake component plane. Vehicle drift is acknowledged. No admission or digitization proposed.

The PDF's prose and Fig. 4 caption disagree on the sign of the plane-c lateral coordinate (`+0.75` versus `−0.75`); resolving it would not cure these failures. Its thrust-balance agreement is not evidence that speed images supply signed components. The requested visual screenshot timed out, so no unseen image details are claimed.

## New repository hit checked and rejected

[Hundur et al., Mendeley Data v1](https://data.mendeley.com/datasets/84mp2p3php/1), DOI `10.17632/84mp2p3php.1`, published 2026-07-08: *Reducing the rotor–airframe aerodynamic penalty of a quadcopter through pressure-informed topology synthesis*.

- Primary record says the release contains onboard flight-controller `.mat` logs, processing scripts, and processed CFD tables; raw CFD solutions are request-only.
- CC BY 4.0 is explicit. The rendered Files section exposes no individual filename inventory; none is invented here.
- **Rejected:** aircraft kinematics and CFD are not independently measured wake-velocity components. A hover experiment in the title or metadata does not satisfy the observable gate. Velocity units/domain/calibration for a measured airflow field are consequently not established.

## Budget and failure audit

Six search queries, eight conservatively counted primary accesses, including failed clicks and the screenshot attempt. No raw archives, numerical extraction, model evaluation, file download to disk, author contact, installation, paid resource, or repository edit.

Searches:

1. `"Wake Characteristics of a Free-Flying Quadrotor" data repository velocity`
2. `"Cene" "quadrotor" dataset still air ProCap`
3. `quadrotor signed velocity field experimental dataset download zenodo 2026 -CFD -simulation -forces -faults`
4. `"AERO2026_043_CENE.pdf"`
5. `"quadcopter" "velocity" "experimental" "dataset" -site:researchgate.net -site:globalresearchspace.com -simulation -fault -CFD -control -acoustic`
6. `("quadrotor" OR "quadcopter") ("wake" OR "downwash") ("data availability" OR "dataset" OR "repository") ("PIV" OR "ProCap" OR "anemometer") -site:researchgate.net -site:globalresearchspace.com -CFD -simulation -Bauersfeld`

Primary accesses: Liverpool record (406); ProCap announcement (success); absolute-reference download click (failed); Mendeley record (success); ProCap publication-record click (success); announcement download click (returned announcement); record's actual PDF click (success); PDF page-5 screenshot (timeout). Query 6 returned no results. Other returned hits were already excluded sources or aircraft flight logs; no new compatible candidate arose. Search snippets alone were not treated as raw releases.

## Evidence route

No best **admissible** new data route was established. The useful documentary result is the now-accessible Cene primary PDF and its explicit rejection grounds. Keep the previous exclusions and scientific results closed; do not relabel this paper-only near-field material as fresh independent far-field validation. A future admission requires actual compatible signed-component files with a coordinate convention, dimensional calibration, spatial coverage, uncertainty information and reusable license.
