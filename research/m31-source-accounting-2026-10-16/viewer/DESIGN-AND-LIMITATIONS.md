# Design and limitations

This is a compact extension of the existing checkpoint viewer design system:
light slate background, white working surface, restrained teal accents, system
typography, native controls, and numeric tables. No generated imagery or external
assets are introduced. The task's explicit static-only/no-QA instruction controls
this handoff; generic frontend-skill browser and visual-fidelity gates were not run.

Design tokens: background `#f1f4f7`; surface white; ink `#192d3e`; secondary text
`#526977`; border `#dbe3e9`; primary teal `#126f79`; comparison orange `#b36c21`;
comparison purple `#7767aa`. Main content is limited to 1340 px with 28 px desktop
gutters and 16 px mobile gutters. The scene/inspector layout collapses to one
column below 790 px. Native selects, visible focus rings, semantic table captions,
status announcements, and original-evidence links accompany the canvas.

The intended hierarchy is: fixed-position source-response finding and evidence links; three recorded summary
values; profile controls and slice view; accessible profile tables; separate
source-state witness; evidence bindings and technical normalization detail. The
opening cards lead with the source-state finding, percentage retention of the
squared-speed proxy, and recorded numerical check. The twenty-row witness table
is an optional disclosure. No decorative metrics,
physical drone model, fluid particles, automatic orbit, or source-motor slider is
included. Profile mode colors are repeated consistently in the SVG comparison.

Scientific boundaries:

- J is a squared scalar-profile proxy with force units. It is not measured thrust
  or a complete axial-momentum balance. The viewer labels this explicitly.
- Surface colors use only saved scalar speeds. Geometry, color scaling, display
  rounding, and connecting adjacent samples are visualization operations, not new
  field evaluations or scientific quadrature. Only recorded r/b <= 4 is drawn in
  the untruncated mode; the finite visible extent is not the infinite integration
  domain.
- The field-plane data excludes receiver-center neighborhood eligibility and
  receiver projection. “Both fades” refers to the saved field-plane profile, not
  a complete pair-query or fluid simulation.
- The witness supplies a structural statement about the exact saved five cases.
  Off-state values do not model physical motor shutdown or wake persistence.
- No independence assertion is inferred or silently repaired in the viewer. The
  saved assertion is displayed, alongside all twenty outputs that support review.
- An empty faded field is represented as no colored slice. A dashed ring can still
  mark where samples were recorded; it is expressly not nonzero support.
- No measured raw flow/thrust validation, physical 27 g qualification, safe flight,
  performance benchmark, or aggregate-swarm conclusion is added.

Engineering boundaries:

- The renderer relies on existing local Three.js/OrbitControls versions and a
  WebGL-capable browser. If 3D setup fails, verified SVG and tables remain usable.
- SHA-256 requires a secure context. Missing or mismatched evidence stops the
  display; no embedded sample values exist.
- The binding itself is not cryptographically authenticated by a separate trust
  root. Byte integrity is distinct from scientific or publication authenticity.
- Result-file schemas and counts are deliberately narrow: ten planes, forty-one
  profile records per plane, five witness cases, and four outputs per case.
- Browser behavior, visual polish at target sizes, accessibility interactions,
  integrity-failure behavior, and actual GPU/display cost remain untested until
  the root's separately bounded QA. No browser or runtime test was performed here.
