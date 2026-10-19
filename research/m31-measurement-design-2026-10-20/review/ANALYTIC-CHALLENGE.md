# Independent analytic measurement-design challenge

20 October 2026. Analytic/documentary work only, using the existing geometry/continuity derivation, source reconciliation and measurement requirements. No numerical field evaluation, data calculation, control, metric, browsing, browser work or acquisition. No repository file changed.

**Disposition:** the proposed three-component observations resolve the local radial/azimuthal ambiguity that defeats a single transverse component. The nominal ring/height draft lies inside the inherited unfaded core by an exact analytic bound. It is a useful design draft, not a feasible, powered or calibrated experiment protocol. Physical scaling, instrument capability, registration, uncertainty and acceptance rules remain gates.

## 1. What becomes identifiable

At a known point with R>0 and known azimuth phi,

    [Ux] = [cos(phi)  -sin(phi)] [Vr    ]
    [Uy]   [sin(phi)   cos(phi)] [Vtheta].

The determinant is cos²(phi)+sin²(phi)=1. Hence

    Vr     = cos(phi)*Ux + sin(phi)*Uy,
    Vtheta = -sin(phi)*Ux + cos(phi)*Uy.

This is a local coordinate rotation, not a continuity reconstruction. It requires no axisymmetry, no zero-swirl assumption and no division by X. It remains regular at the cardinal azimuths. The cylindrical direction is undefined at R=0, which the draft does not sample.

With Ux alone, adding (a*sin(phi), a*cos(phi)) to (Vr,Vtheta) leaves Ux unchanged. At special azimuths Ux isolates one component, but still cannot identify both. Moving a two-component instrument to another location does not automatically supply the missing component at the first location.

The two horizontal components must describe the same physical location, registered frame and averaging condition. Uz must also be measured for the axial comparison. Primary comparisons should stay in directly observed Cartesian components; the radial/azimuthal rotation can be a separately declared descriptive result. Neither calculation should fill an unmeasured component by symmetry.

## 2. Analytic core admission of the nominal draft

Use the inherited dimensionless definitions only:

    b(Z) = S*(Z + 2*sqrt(2)*a), S=.07668, a=5.817.

For the proposed Z in {12,18,24} and R in {3/2,5/2}, use the exact inequalities S>3/40, a>5 and sqrt(2)>1. Then

    2*b(Z) > 2*(3/40)*(12 + 2*5) > 5/2 >= R.

Thus b is positive and xi=R/b<2 at every nominal point, independently of azimuth. This proof uses a deliberately coarse rational lower bound; it does not evaluate b or xi numerically or generate a field. The selected heights retain the previously used primary downstream support. This is internal consistency with the inherited dimensionless model, not proof that a different aircraft or a dimensional instrument grid has compatible geometry. Actual registered support and its uncertainty must pass a separately fixed physical-domain rule.

Two radii and three heights are transparent design choices, not a power calculation, radial reconstruction or validation of the full axial-derivative law. They do not observe the central region, all intervening radii or the continuous downstream field. No whole-plane flux, axis regularity, complete continuity or global momentum claim follows.

## 3. Sampled azimuth variation is not global axisymmetry

Matched radii/heights with all three components allow comparison across sampled azimuths without imposing equality. If the eight angles are equally spaced, phi_k=2*pi*k/8, an azimuthal variation proportional to sin(8*phi) vanishes at every sampled angle. This analytic counterexample shows why agreement at the chosen locations cannot establish global axisymmetry. Other finite arrangements also leave unsampled variation unconstrained.

Zero or small mean Vtheta at these samples does not establish absence of instantaneous swirling motion. Nonzero measured mean Vtheta is local azimuthal velocity relative to the registered axis; center/attitude error or flow displacement can contaminate its interpretation. The reference axis and pose must come from independent geometry/tracking, with uncertainty, rather than fitting a center that minimizes the observed disagreement.

Sequential sections or azimuths additionally need a predeclared acquisition order, repeat/reference measurements and evidence about stationarity and vehicle drift. Otherwise time variation can masquerade as spatial variation. For a moving reference frame, define whether and how instantaneous samples are transformed before averaging; transforming averaged values using a fitted mean pose is not automatically equivalent.

## 4. Statistical acceptance and feasibility are unfinished

The next design must specify instrument capability for co-located three-component measurements. A horizontal two-component plane measures its in-plane components but does not supply the normal axial component. A proposed three-component plane/volume or vector probe must have a verified calibration, usable coverage, uncertainty and assessment of relevant disturbance or reconstruction constraints. No instrument or facility capability has been demonstrated here.

Specify independent calibration checks, signed axes, dimensional scale, operating point, masks, temporal averaging, spatial correlation, run-to-run variation and uncertainty propagated through registration/rotation. Grid nodes, azimuths and successive frames must not be treated as independent replicates by default. Choose replication and duration from declared precision or separate pilot evidence; the present point layout supplies neither statistical power nor a justified sample count.

Failure to reject zero swirl or equal azimuthal means is not evidence of equivalence. Any practical equivalence margin, joint/multiple-comparison treatment, uncertainty rule and minimum usable coverage must be fixed before target outcomes. An instrument/domain/calibration failure should remain an admission or quality-control failure, not become a favorable model score. Missing samples need a declared failure/limited-claim rule rather than outcome-driven interpolation or dropped regions.

Finally, the physical model amplitude remains a distinct unresolved gate. The inherited fitted gain is not an SI conversion. Direct component observations can support local kinematic description with sound measurement calibration, but an absolute model-accuracy acceptance decision additionally needs an independently justified mapping of the model to those units. A target-fitted lateral/common gain would change the question. This draft authorizes no fit, new evaluation, acquisition or experiment launch.
