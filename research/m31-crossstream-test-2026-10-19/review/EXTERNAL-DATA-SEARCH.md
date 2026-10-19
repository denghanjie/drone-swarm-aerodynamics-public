# Independent calibrated axial-airflow candidate ledger

Checked 2026-10-19. Scope: independent experimental multirotor axial velocity, usable dimensional scale, geometry/operating point, and public files/licensing. No installs, author contact, paid access, large downloads, digitization, or numerical evaluations were performed.

**Result:** no candidate was verified to satisfy all gates with downloadable measurement arrays. This is a bounded search result, not proof that no such release exists. The strongest accessible independent evidence is Wolf et al.'s published velocity fields. A paper, thesis, presentation, or repository record alone is not a raw-data release.

## Ranked candidates

### 1. Wolf et al. (2024): strongest published-field fallback; raw release unverified

- [Primary article](https://link.springer.com/article/10.1007/s00348-024-03880-3), [DLR publication record](https://elib.dlr.de/223206/), [Fig. 12](https://link.springer.com/article/10.1007/s00348-024-03880-3/figures/12), [Table 1](https://link.springer.com/article/10.1007/s00348-024-03880-3/tables/1).
- Independent DJI Mavic 2 Pro hover experiment. Rotor diameter 0.22 m; front/rear spacing 1.35D/1.17D; front height offset 0.18D; inward cant. Masses 915/1135/1355 g. Hover reference speed uses weight and total rotor area, with reported 4.9–6.1 m/s. Standard front/back rotation rates differ (94/81 Hz).
- STB particle tracking, plate calibration, volume self-calibration, and FlowFit assimilation. Published mean axial component is `w/Vh`; Fig. 12 contains **color fields**, not tabulated line profiles. Fig. 10 supplies the colormap. Fig. 15 is mass flux and Fig. 16 thrust, not pointwise axial velocity.
- Public PDF is listed by DLR; no raw velocity file link found in inspected primary pages. Table URL fetch failed; its full entries remain to inspect. Publisher explicitly licenses article/images CC BY 4.0 unless a credit line says otherwise.
- Gates: exact slice, figure credit, colormap, coverage in motor-distance units, cant/asymmetry, and enclosure effects. Parent is inspecting figures. Do not assume far-field coverage from rotor-radius axes.

### 2. Flem et al. (2024): dimensional sonic measurements; release not verified

- [Journal article](https://www.mdpi.com/2073-4433/15/3/242), [DOI](https://doi.org/10.3390/atmos15030242), [preprint](https://www.preprints.org/manuscript/202401.0756), [preprint PDF](https://www.preprints.org/manuscript/202401.0756/v1/download).
- Five sonic anemometers measure three velocity components at 10 Hz, spanning approximately 2–10 rotor diameters downstream and 0–3D laterally; throttle settings 35% and 45%.
- Important domain mismatch from methods inspection: coaxial X8 platform, 8° tilt, and wall/door contamination. It cannot directly stand in for an untilted isolated quadrotor.
- Data statement says data were being prepared for an open repository. No actual measurement-file release verified.
- [Zenodo 10678904](https://zenodo.org/records/10678904) contains **only the 25.0 MB thesis** `Master_Flem_2023.pdf` (MD5 `1de8c49f88626aa818f79d340c71f598`). [Zenodo 10681156](https://zenodo.org/records/10681156) contains **only the 3.2 MB presentation** `ISARRA2023_Session3_Flem.pdf` (MD5 `75543deaee14c170abc799b0f0ec3adf`, CC BY 4.0). Neither establishes downloadable flow arrays. Repository download-volume statistics are not file sizes.
- Gate: actual data release, sensor calibration/error model, thrust/RPM mapping, and a usable uncontaminated domain.

### 3. Jin et al. (2024): calibrated 3D lidar; request-only

- [Primary article](https://amt.copernicus.org/articles/17/2721/2024/), [PDF](https://amt.copernicus.org/articles/17/2721/2024/amt-17-2721-2024.pdf), DOI `10.5194/amt-17-2721-2024`.
- Three WindScanner lidars reconstruct 3D velocity around a Foxtech D130 X8; rotor diameter 0.71 m. Outdoor low-wind measurements include a near plane about 1D below the aircraft.
- Primary availability statement makes underlying data available from the authors upon reasonable request. No public measured-field download verified. Excluded under the no-contact constraint.
- Paper is CC BY 4.0; that does not turn request-only data into public files. A related DTU **CFD** dataset is simulation, not independent experimental validation.

### 4. Cene et al. (2026): relevant observable; publication-only lead

- [Liverpool repository](https://livrepository.liverpool.ac.uk/3197346/), [measurement-system publication notice](https://www.procap.tech/publication-on-procap-measurements-on-aerodynamics-of-hovering-drones/).
- *Wake Characteristics of a Free-Flying Quadrotor Hovering in Uniform and Shear Inflows*: DJI NEO in still air/uniform/shear inflow; ProCap multihole probe and optical tracking yield mean three-component velocity and pressure on multiple planes.
- Repository search metadata lists accepted manuscript `AERO2026_043_CENE.pdf`, about 3 MB, CC Attribution. Full repository fetch returned 406; direct PDF and measurement arrays were not verified. Do not infer calibration or dataset licensing from the title.
- Gate: primary methods, operating point, independent reference scale, actual file inventory, license, and still-air spatial coverage.

### 5. Thielicke et al. (2021): real data DOI, but wrong main wake target

- [Primary paper](https://amt.copernicus.org/articles/14/1303/2021/), [data DOI](https://doi.org/10.6084/m9.figshare.12581678.v4).
- The article says measurements other than PTB lidar data are released. The Figshare inventory/API could not be retrieved in this session, so filenames and dataset license remain unverified.
- Fig. 19 concerns a **wind-turbine wake sampled by a drone**, not the drone's wake. Fig. 9 concerns aircraft interference at a sensor above the aircraft; potentially local sensor calibration, not the required far-downstream axial field.
- Gate: verify contents before further work; do not admit it based solely on a public DOI.

## Actual public files that fail the required observable/domain

| Source | Verified repository offering | Why it is not the target |
|---|---|---|
| [Aerodynamic forces in air ducts](https://zenodo.org/records/13837470) | `aero_forces_in_air_ducts.tgz`, 5.1 GB, MD5 `2c7c8a0ddf262bd7c513c4b5c04e71f0` | Force/torque maps; not axial velocity. |
| [Quadcopter forward-flight LES](https://zenodo.org/records/7059240) | `LESofQuadInFwdFlight_v1.1.tar.gz`, 1.6 GB, MD5 `3fa7d85fb1760ed15a5a454328d90897` | CFD, not experimental validation. |
| [NASA HVAB](https://rotorcraft.arc.nasa.gov/HVAB/pivData.html) | `VectorFielddata.zip` (733 MB), `CoreSize_SwirlVelocity.xlsx`, `TipVortexTrajectory.xlsx` | Single large helicopter rotor; component-level fallback only. |
| [MODERA UAV model/tests](https://zenodo.org/records/17457069) | `experimental_data.zip`, 2.5 GB, MD5 `7db17fe4e723571fcffd2e7da6fed637`; CAD and simulation also offered | Experiments contain force/moment and acoustic measurements at throttle combinations, not velocity fields. |

These inventories were read; archives were not downloaded. Their existence does not establish a usable airflow validation set or permission to reuse every file.

## Remaining publication leads closed for this pass

- [Chen et al., ERF 2019](https://dspace-erf.nlr.nl/items/b63962aa-df32-4055-a821-43f076c459d4): repository lists only `ERF2019 0038.pdf` (1.83 MB). Side-by-side, coaxial, and tandem configurations; inflow/outflow planes immediately near rotor disks. No raw-field link verified, and near-disk domain does not match a developed far wake. [Repository PDF](https://dspace-erf.nlr.nl/server/api/core/bitstreams/f8c87a81-4f7b-4aba-9143-a8478822c2df/content).
- [Longobardo et al., blade-tip vortex interactions](https://www.iris.unina.it/handle/11588/1068703), DOI `10.1016/j.ast.2026.113809`: repository explicitly has no associated files. Early vortex evolution near the disk; publisher fetch 403. Record assigns a 2027 volume despite 2026 DOI/online indexing. No raw-data claim.
- [Wolf follow-up](https://arxiv.org/html/2609.19507v1): related STB wake analysis; no new public raw-file release found in inspected page.
- Bauersfeld's measurements generated the current kernel coefficients and report speed magnitude, so they are not blind independent axial validation. The already exposed RSS single-PIV benchmark and later same-author work must not be relabeled independent validation.

## Concrete next action within current constraints

Use **Wolf only as a conditional published-field diagnostic** if inspection confirms a physically appropriate domain. Before any extraction, freeze the aircraft case, coordinate convention, admissible region, sampling positions, scale calculation, and uncertainty rule. Preserve the image/source hash and citation; attribute CC BY 4.0 and mark the extraction as a modification. Mask arrows, text, boundaries, and other overlays; account for finite pixel/color resolution and any color saturation. The original experiment's uncertainty is separate from digitization uncertainty.

Do not fit gain or select favorable points after observing model discrepancies. A source already inspected while choosing a protocol is not an untouched blind holdout. If far-field coverage or geometry mapping fails, record **not admitted** and stop; do not turn flux/thrust figures into axial velocity or claim normalization calibration from fitted agreement.

The existing RSS normalization question remains unresolved by these candidates. No current scores, kernel parameters, or prior allocations were changed or rerun.

## Adopted disposition

The subsequent [domain challenge](EXTERNAL-DIAGNOSTIC-CHALLENGE.md) rejects the proposed two-flux score as outside the current model's admitted domain. No Wolf digitization or numerical comparison was performed. The separately specified same-experiment cross-component test in [the protocol](../PROTOCOL.md) is the adopted next numerical action; it does not replace independent validation.
