# Measurement-method verification for design

2026-10-20. Documentary review only. No measurements, numerical work, downloads to disk, author contact, installation, repository writes, or new agents.

**Design conclusion:** stereo PIV can supply three signed velocity components on a measurement plane (2D3C); it does not by itself measure a volume. Tomographic PIV reconstructs three-component velocities throughout an illuminated volume (3D3C). Either requires an experiment-specific uncertainty assessment. A camera count, grid spacing, self-calibration result, or published benchmark accuracy does not establish precision for the proposed experiment.

## Verified primary references

### 1. Stereo calibration and light-sheet registration

B. Wieneke (2005), **“Stereo-PIV using self-calibration on particle images.”** *Experiments in Fluids* 39, 267–280. DOI [10.1007/s00348-005-0962-z](https://doi.org/10.1007/s00348-005-0962-z). [Publisher](https://link.springer.com/article/10.1007/s00348-005-0962-z).

Publisher abstract verified. The original method fits camera mapping using a calibration plate, estimates inter-camera disparity from particle images, locates the actual light sheet, and corrects the mappings. It also considers refraction and light-sheet overlap/thickness. Supports retaining calibration images, mappings, disparity and sheet-location diagnostics. It does **not** warrant treating self-calibration as zero registration error or a complete uncertainty budget. Full paid text was not accessed.

### 2. Stereo-component uncertainty

S. Bhattacharya, J. J. Charonko, P. P. Vlachos (2017; online 2016), **“Stereo-particle image velocimetry uncertainty quantification.”** *Measurement Science and Technology* 28, 015301. DOI/publisher [10.1088/1361-6501/28/1/015301](https://doi.org/10.1088/1361-6501/28/1/015301).

Primary publisher search text verified title, authors, DOI and abstract; direct opening failed. The framework combines stereo-registration uncertainty with the underlying planar-velocity uncertainties. Tests vary sheet thickness and registration error. Supports treating out-of-plane reconstruction and registration as explicit parts of the measurement chain, not assigning every component one generic precision. No numerical accuracy was imported. The authors' [research-group listing](https://vlachosresearch.org/author/aerognome/) also identifies stereo PIV as 2D3C; this classification was visible in the primary-site search result, not a separately opened full article.

### 3. Volumetric alternative

G. E. Elsinga, F. Scarano, B. Wieneke, B. W. van Oudheusden (2006), **“Tomographic particle image velocimetry.”** *Experiments in Fluids* 41, 933–947. DOI [10.1007/s00348-006-0212-z](https://doi.org/10.1007/s00348-006-0212-z). [Publisher](https://link.springer.com/article/10.1007/s00348-006-0212-z).

Publisher abstract verified. Multiple simultaneous camera views reconstruct particle intensity in a three-dimensional voxel volume; three-dimensional correlation then yields the velocity-vector field over that volume. This supports the planar-versus-volumetric distinction. Reconstruction and calibration remain part of the measurement process. The paper's existence does not guarantee suitable resolution, uncertainty, optical access, or sampling for this aircraft. Full paid text was not accessed.

### 4. Spatial covariance and finite repetitions

A. Sciacchitano, B. Wieneke (2016), **“PIV uncertainty propagation.”** *Measurement Science and Technology* 27(8), 084006. DOI [10.1088/0957-0233/27/8/084006](https://doi.org/10.1088/0957-0233/27/8/084006). [Author-institution record](https://research.tudelft.nl/en/publications/piv-uncertainty-propagation/).

Primary institutional abstract and DOI verified. It treats uncertainty of mean velocity, Reynolds stresses, vorticity and divergence. Derivative uncertainty depends on spatial correlation of displacement errors and measurement resolution. Statistical uncertainty depends on the **effective number of independent samples**, not simply the number of images. Supports recording spatial/temporal dependence and distinguishing uncertainty of instantaneous vectors from uncertainty of estimated means. Published validation percentages are not transferable precision promises. The record offers a CC BY published PDF; it was not downloaded.

### 5. General metrology framework

JCGM (2008), **“Evaluation of measurement data — Guide to the expression of uncertainty in measurement,” JCGM 100:2008 (GUM 1995 with minor corrections).** [Official BIPM document](https://www.bipm.org/documents/20126/20763265/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6). Document identifier verified; no DOI is asserted.

Relevant passages read in the public document:

- §4.2.1–4.2.6: repeated-observation uncertainty uses independence assumptions and requires degrees-of-freedom information.
- §4.2.7: temporally correlated observations can make the ordinary mean and mean-uncertainty estimators inappropriate.
- §5.2.1–5.2.5: significant covariance must enter propagation; shared instruments, standards and reference data can create correlation. Covariance should be estimated experimentally where feasible or from available information.
- Annex E.4.3: repetition-based uncertainty estimates are not automatically superior to other evaluations.

Thus common calibration uncertainty must not be assumed to disappear through more repeats, and repeated frames must not be treated as independent flight trials. No universal sample count, uncertainty threshold, or coverage factor is prescribed here.

## Reused reconstruction caveat — no candidate reopened

Wolf et al. (2024), **“Volumetric wake investigation of a free-flying quadcopter using Shake-The-Box Lagrangian particle tracking.”** DOI [10.1007/s00348-024-03880-3](https://doi.org/10.1007/s00348-024-03880-3).

From the earlier verified reading: its FlowFit assimilation uses an incompressibility/continuity constraint. **Design inference:** a divergence or closed-surface mass-balance result from a field reconstructed using that same condition is not independent validation of that condition. Preserve the measurement/reconstruction distinction and document imposed constraints. This is a caveat about that processing chain, not a claim that all STB or tomographic measurements enforce continuity.

## Practical implications — proposed design judgments, not new measured facts

1. Define the measurand: signed components and their coordinate basis, instantaneous or time-averaged state, and the spatial/temporal support of each reported value. Keep speed magnitude separate.
2. For plane/face transport, stereo PIV is a candidate measurement method. A single plane does not provide normal-direction gradients or a complete instantaneous closed surface. Sequential plane surveys require a justified stationarity assumption for mean comparisons; they do not directly measure simultaneous cross-plane covariance.
3. Retain component and cross-location covariance where relevant to transport or derivative calculations, along with registration, timing, scale, reconstruction, masking and sampling contributions. Distinguish flow variability from measurement error; observed velocity covariance is not automatically error covariance.
4. Separate repeated image pairs within a run from independent reruns. Determine temporal dependence and between-run variation before selecting an effective sample count. Repetition under one unchanged calibration cannot reveal every shared bias.
5. Set acceptance precision only after apparatus-specific calibration and uncertainty evidence. These sources justify the structure of that assessment, not a numerical accuracy guarantee.

## Access and scope audit

Four search queries. Five `open` requests: Elsinga publisher; Wieneke publisher twice (the second positioned the same page); Bhattacharya DOI (failed); TU Delft record. One first-document `find` opened the official GUM. Five further **in-document finds** read already opened Wieneke/TU Delft/GUM material; no additional primary documents were opened. Thus six opening requests across five unique primary documents, plus five in-document reads.

Queries: (1) stereo-PIV uncertainty title/authors; (2) tomographic-PIV and stereo-self-calibration titles; (3) official BIPM JCGM 100 correlated/independent inputs; (4) PIV uncertainty propagation and effective sample size. Secondary results were not used as authorities. Two Springer texts were abstract-only; Bhattacharya was verified through publisher-indexed text after its direct-open failure. No excluded data candidate was revisited.
