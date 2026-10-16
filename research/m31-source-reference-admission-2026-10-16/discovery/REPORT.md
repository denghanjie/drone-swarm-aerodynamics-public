# Variable-source flow evidence: bounded discovery

2026-10-16. Four discovery queries and four primary documents. Metadata and methods inspection only; no dataset payload, archive, model calculation, fitting, author contact or scientific execution. Existing frozen packages remain unchanged.

**Strongest new reference: NASA/U.S. Army Hover Validation and Acoustic Baseline (HVAB) PIV and performance release.** It provides positive partial evidence: an official release documents measured spatial velocity fields at multiple collective/load settings and separate balance-based performance channels under matching run identifiers. This is stronger evidence for a possible component comparison than a plotted-only normalized wake or a single front/back contrast.

**Admission remains unresolved.** The inspected documentation does not establish vector-field spatial bounds or a compatible time average. Do not allocate the large archive or claim a test of the existing far-field law on this basis. The current evidence supports a prospective phase-conditioned near-wake component reference. It does not establish a directly executable comparison to the frozen source model.

## Four inspected primary documents

| ID | Exact source | Identity and scope |
|---|---|---|
| S1 | [HVAB PIV Data](https://rotorcraft.arc.nasa.gov/HVAB/pivData.html) | Official NASA Ames release listing; processed flow fields and vortex-property files |
| S2 | [HVAB PIV Data, ReadMe](https://rotorcraft.arc.nasa.gov/HVAB/HVABReleasedData_v2/PIV_Data/HVAB_PIV_ReadMe.pdf) | Manikandan Ramasamy, U.S. Army DEVCOM/NASA Ames; initial release 18 September 2024; 8 pages |
| S3 | [HVAB Performance Data](https://rotorcraft.arc.nasa.gov/HVAB/performanceData.html) | Official NASA Ames release listing; performance means, uncertainty, atmospheric conditions and blade motions |
| S4 | [HVAB Performance Data, ReadMe](https://rotorcraft.arc.nasa.gov/HVAB/HVABReleasedData_v2/Performance_Data/Performance_ReadMe_v2.1.pdf) | Lauren Wagner; filename v2.1; visible history gives initial release 28 September 2023 and v2 dated 30 September 2024; 6 pages |

No dataset DOI was verified. Do not invent a publication date for the filename's v2.1 revision.

## Verified content and its limits

**S1, release listing.** It links `VectorFielddata.zip`, labelled 733 MB, plus `CoreSize_SwirlVelocity.xlsx` and `TipVortexTrajectory.xlsx`. These are distinct released products, not interchangeable observations. The resolved archive URL and exact byte size were not recovered. No file request was made. The XLSX sizes are unverified; they must not be called small merely because they are spreadsheets.

**S2, pp. 1–5, Table 1 and data-format sections.** PIV uses tip Mach 0.65 and collectives 8°, 10°, 12°, 14°: run 92 contains 8°; run 95 contains the others. It is phase-locked stereo three-component PIV, initially 200 realizations per case. Filtering changes retained counts; provided means and standard deviations reflect filtered observations. Coordinates are `r/R` from the shaft and `y/R` from the tip-path plane. Channels are radial, axial/downwash and chordwise velocity in m/s. Files contain means and standard deviations. The filename encodes run, Mach, collective, blade and wake age. Vortex products involve fitted extraction and additional screening. Explicit rectangular field bounds are absent from inspected text; calibration-target width is not field extent.

**S3, release listing.** The matching performance file is `Run92_95_v2.1.xlsx`. Its resolved URL and byte size were not recovered. It was not opened.

**S4, pp. 1–5, processing section, Table 2 and appendix.** Rotor-balance drift is corrected in thrust and torque channels before condition averaging. Table 2 pairs runs 92/95 with tip Mach 0.650 and collectives 8°, 10°, 12°, 14°. The workbook has mean and confidence-interval tabs; rows identify run/Mach/collective and include dimensional and nondimensional parameters. Performance intervals use between-point variability, assuming relevant calibration uncertainty is small. Atmospheric uncertainty is treated separately. The appendix gives rotor radius 5.54167 ft. These are force measurements independent of PIV reconstruction, although the original balance-calibration report and individual workbook columns were not inspected. Run-level matching is documented; exact row joins, timing and environmental consistency have not been checked.

**Reuse terms:** neither landing page nor either README exposed a data-specific license. Official public release is verified; a license or unrestricted redistribution entitlement is not. The linked site disclaimer and full methods papers were not followed after the four-document cap. Do not import another dataset's license or infer license coverage solely from the NASA host.

## Bibliographic trail

The official PIV README cites Ramasamy, M.; Heineck, J. T.; Yamauchi, G.; Schairer, E.; and Norman, T., *Comprehensive Aerodynamic Analysis of PIV Measurements in the NFAC 80- by 120-ft Test Section Towards Understanding HVAB Hovering Rotor Characteristics*, Vertical Flight Society 80th Annual Forum, Montreal, 7–9 May 2024. This identity is verified from S2's reference list; the paper itself and a DOI were not inspected. S4 separately supplies the Norman et al. 2023 comprehensive-test reference. No full-paper reading is claimed for either reference.

## What a later component test could ask

If field extent, coordinate signs, masks, force pairing and reuse conditions are established under a separately bounded allocation, choose a fixed spatial/phase observable and test the explicit hypothesis

`u_test(x, phase) = u_base(x, phase) × sqrt[(T_test/rho_test)/(T_base/rho_base)]`.

This would be a proposed rule for this rotor and its measured operating domain. It would not be adopted as a universal physical law. Load comes from the independent balance channel, not from integrating the same velocity field. Do not fit the scaling amplitude from the test flow and then score that flow as validation.

A pair of collective settings could be fixed before payload inspection for a narrow comparison. Match the same phase and actual shared coordinates, preserve missing regions and compare a prespecified profile; do not choose a phase or mask after seeing favorable residuals. The released standard deviation describes dispersion and must not be converted to standard error using 200 as the retained count. A complete uncertainty interval cannot be manufactured from unspecified retained counts or independence assumptions.

The first admission question precedes acquisition: **does any documented field region and averaging convention answer the intended model question?** Existing planning restricts the Bauersfeld far-field use to `s/D ≥ 2.5`. Near-rotor phase-conditioned PIV does not automatically occupy that domain or represent a time-mean field. Vortex-trajectory coordinates do not establish the complete vector-field bounds. Unequally spaced phase samples cannot silently become a uniformly averaged wake. Until those points are resolved, do not call this a falsification test of the existing far-field law.

Even an admitted near-wake comparison would concern collective-pitch loading on one large rotor. It would supply no general fixed-pitch RPM/PWM law, no unequal-motor multirotor field, no shutdown dynamics, no receiver law, and no 27 g validation. It can identify a boundary of a deliberately broader amplitude-scaling hypothesis only if that broader hypothesis is explicitly stated. Its possible value is a constrained component question; it is not evidence to spend a large acquisition budget automatically.

## Acquisition posture

No archive HEAD, range request, ZIP index read, member request or workbook GET was performed. The 733 MB label alone does not prove byte-range access or selective-member feasibility. The exact archive href, compressed member sizes/formats, server range behavior and workbook sizes remain unverified. No exact direct download URL should be synthesized from the README path and presented as observed.

Three attempts to extract links from the already inspected HTML pages failed before body data: sandbox DNS, then approved Python TLS, then approved curl TLS. These were metadata-only requests, not attempts to acquire scientific data. No approval review rejection occurred. The PIV schematic screenshot request returned a marker without usable pixels; it supplied no additional extent measurement.

Recommendation: retain HVAB as the strongest documented partial flow reference. Resolve spatial extent/averaging and reuse from small documentation before deciding whether any separately capped payload inspection is worthwhile. The four-document budget is now closed; no further discovery or acquisition is authorized by this memo.

## Prior work and search scope

Acquisition logs were inspected first. Brown, MODERA and Neural-Swarm routes were not retried. Bauersfeld and Wolf were not reread in this discovery; their completed bounded check remains separate at `[private prior-discovery staging]/`.

Search also surfaced NASA's 2010 rotor-hover measurements, an INSEAN marine-propeller report, TU Delft propeller/wing work and wind-turbine releases. Those were discovery leads only; no technical claim or license was accepted from their snippets, and none was opened as a primary document. The budget was concentrated on a released powered-hover flow source with documented load variation and matching performance records. This is neither an exhaustive literature survey nor evidence that a more compatible reference is absent.

Exact query strings, source locators, access failures and accounting are retained in `SOURCE-ACCESS.json`. No existing package or source file was modified.
