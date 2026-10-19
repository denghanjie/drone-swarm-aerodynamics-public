# A test that can tell competing explanations apart

This document specifies a candidate research design, not an experiment that has happened. No apparatus, compatible release, facility access, precision or physical amplitude mapping is confirmed. Its immediate outcome is an explicit decision about what must be known before testing the model.

## 1. What question are we trying to answer?
The existing conditional comparison shows smaller predicted radial-transport magnitudes than reconstructed measurements on twelve radial walls. We do not know whether this reflects component calibration/processing, unmeasured swirl, nonaxisymmetric flow, incorrect axial evolution, or a wrong closure. These possibilities can coexist. We cannot identify a unique cause by adjusting a parameter until one exposed plot looks better.

The proposed experiment has two separate outputs:
- **Observation checks:** independently calibrated component velocities and sampled tests of swirl/azimuthal variation. These do not require a fitted wake prediction.
- **Prediction check:** the unchanged model against direct signed Cartesian observations in a physically defined scale. This is blocked until the model-to-SI mapping is independently justified. The previously fitted gain is not a universal unit conversion.

## 2. The missing information, shown by algebra
Let z increase downwards, x/y span the rotor plane, R=sqrt(x²+y²)>0 and phi=atan2(y,x). All velocity components must use the same right-handed physical convention; the instrument-to-frame transform is recorded separately. For a chosen right-handed (x,y,z-down) frame, phi is measured about its positive z direction. Radial outward and tangential positive basis vectors are eR=(cosphi,sinphi,0) and eT=(-sinphi,cosphi,0).

    Vx = cosphi VR - sinphi VT
    Vy = sinphi VR + cosphi VT
    Vz = U

A sole Vx measurement leaves the combination (deltaVR,deltaVT)=t(sinphi,cosphi) invisible. At special azimuths one component can be directly observed, but the other remains unknown. Additional points with only Vx do not remove this local ambiguity unless an untested relationship between their velocities is imposed. Two measured horizontal components at the same location invert the rotation:

    VR = cosphi Vx + sinphi Vy
    VT = -sinphi Vx + cosphi Vy

Its determinant is one. This is an analytic information requirement, not a measured discovery. It does not assume zero swirl or axisymmetry. The axis R=0 is excluded from cylindrical decomposition; Cartesian components remain valid there.

Measuring Vz as well permits a direct three-component prediction test. Measuring all three at one point or one plane does not establish global symmetry. A horizontal three-component section samples multiple azimuths at matched R,Z, so it can test variation at those locations. Finite angular coverage can miss higher-order angular structure. For example, sin(8phi) vanishes at all eight equally spaced proposed angles while varying between them. This analytic counterexample is not a claim that the actual wake has that structure. Mean-zero VT does not exclude instantaneous counter-rotating motion; report mean and time-resolved behavior as separate quantities if measured.

## 3. Candidate coverage, chosen before new observations
Prefer signed three-component measurements over a volume covering the admitted domain, without imposing the very symmetry or continuity relation being tested. A lower-dimensional fallback is stereoscopic PIV in horizontal sections, recording all three velocity components in each plane, provided its out-of-plane displacement, optical access and uncertainty can support this task. Ordinary two-component planar PIV is not equivalent. Verified methods: [Wieneke2005](https://doi.org/10.1007/s00348-005-0962-z), [Elsinga et al.2006](https://doi.org/10.1007/s00348-006-0212-z). These references establish principles, not the precision or availability of our apparatus; access limits are in LITERATURE.md.

Draft spatial sentinels: Z=z/l in {12,18,24}; R=r/l in {1.5,2.5}; phi in {0,45,90,135,180,225,270,315}degrees. This gives 48 sites. They are prespecified engineering choices inside previously examined heights, not the result of a power calculation, an optimum or independent repeats. Images may cover more space, but the primary support and any secondary coverage must be frozen before outcome inspection.

For the historical fixed closure b(Z)=.07668*(Z+2sqrt(2)*5.817), the domain condition is R/b<=2 and Z>=12. At these proposed heights, analytically b>.075*(12+2*5)=1.65, so2b>3.3>2.5: the candidate rings lie inside its unfaded radial interior. This simple bound is design algebra, not a new model evaluation or evidence of physical validity. Physical rotor geometry still needs separate admission; domain membership alone does not make a different ducted/tilted/coaxial aircraft compatible.

Measure three components at the SAME physical sites. Sequential planes are not simultaneous volumes. Randomize/predeclare plane order across independent runs and bracket acquisitions with repeat reference conditions; record thrust, pose, ambient flow and drift. If stationarity fails at the required precision, do not combine sequential planes into a common mean-volume claim. More heights would be needed for resolved derivatives or a general continuity test; the three sentinels alone do not justify such derivatives. Do not infer a unique defective term from a remaining residual.

## 4. Separate instrument calibration from model calibration
Before wake data are used for comparison, retain a traceable geometric target/calibration, timing calibration, camera/probe transforms, axis/sign checks and independently known reference motion or velocity appropriate to the instrument. A stationary target/zero-flow check alone does not certify velocity gain. For stereo imaging, quantify reconstruction cross-talk and out-of-plane uncertainty in the proposed geometry. No wake-model prediction serves as the reference standard.

Export direct Cartesian mean components in m/s, positions in m, uncertainty/covariance and validity reasons, as well as original images/signals and processing settings where legally releasable. Retain reference and drift checks before/after runs. Register the wake reference axis and aircraft pose independently; do not fit the center to minimize model error. Propagate axis/pose uncertainty because misregistration can resemble swirl. Define transformation of moving-frame instantaneous samples before averaging; a fitted average pose is not automatically equivalent. Record rotor centers/radii/cant/heights, coordinate origin, density, total/per-rotor thrust conventions, RPM/control state, attitude and boundary distances. Actual settings and calibration acceptance tolerances must be instrument-specific and set before target residuals.

## 5. Prospective analysis and interpretation
Primary prediction quantity: the direct mean Cartesian residual vector at each prespecified site, measured minus model. Define its physical units, coordinate transforms and model scaling first. Derived VR,VT and azimuth contrasts are diagnostic secondary quantities; do not reconstruct missing components by imposing symmetry or continuity.

All 48 planned sites require usable data for the complete primary design claim. If a required site fails its prospective acquisition/geometry/uncertainty rule, report an incomplete primary test; do not interpolate from the model, drop it because of its residual or award an all-site pass. Any limited-support secondary report must be declared before data inspection.

Treat repeated experimental runs as replication units; grid points, frames and shared calibration errors are correlated. Keep within-run temporal correlation, calibration covariance, coordinate uncertainty and model-input uncertainty distinct. Instrument calibration shared across runs is not reduced merely by collecting more runs. Choose averaging duration and independent repetition count from separately justified precision/pilot evidence, before confirmatory data. No count, effect size or confidence width is invented here. [Sciacchitano & Wieneke2016](https://doi.org/10.1088/0957-0233/27/8/084006) and the [official GUM](https://www.bipm.org/documents/20126/20763265/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6) support accounting for effective sample size and covariance; neither supplies an apparatus-specific precision guarantee.

Before a launch protocol, define component-specific practical tolerances Delta_j from the intended aerodynamic use and measurement capability, not from these old residuals. A downstream receiving-force or flight tolerance cannot yet be derived from this field-only evidence. Define uncertainty coverage and multiplicity over the planned sites/contrasts prospectively. A covariance matrix alone does not supply valid confidence intervals without a justified distribution/sampling method.

For a two-sided uncertainty interval for a mean discrepancy d and an independently fixed practical tolerance +/-Delta: an interval entirely inside the tolerance band supports agreement at that precision; an interval wholly outside on one side supports a material mismatch; overlap with both acceptable and unacceptable values is inconclusive. Merely containing zero is not a pass. These logical rules apply only when the interval procedure and systematic-error treatment are justified. No empirical pass/fail threshold or statistical interval has been computed.

Use the same logic for prespecified VT and matched-azimuth contrasts with their own physically justified tolerances and uncertainty. Nonzero calibrated mean VT at sampled locations contradicts a no-mean-swirl assumption there; resolved azimuth contrasts contradict symmetry there. Nondetection is not global absence. If calibration gates fail, classify the comparison as uninterpretable, not as model failure. If calibration passes and direct prediction fails, report model discrepancy without claiming a unique physical cause. Multiple explanations may remain.

## 6. What would let us execute?
The readiness checklist in READINESS.md must be completed first. No laboratory access, instrument, experiment budget or precision has been established. This checkpoint defines the evidence we need and how to interpret it; it does not promise that collecting it is currently possible. Any future hardware acquisition, external contact or actual flight needs its own authorization. A new numerical analysis also needs admitted inputs, a prospective bounded protocol, independent review and a publicly verified exact source freeze.
