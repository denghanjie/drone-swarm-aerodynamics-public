Public edition. Intended destination: research/campaign-velocity-2026-screen/demo/.

# Viewing and verification

Serve the repository over local HTTP and open this folder's index.html. The diagram fetches the exact EPOCH2-RESULT.json; it does not import or run the aerodynamic model. No extra point or trajectory is generated.

The default orthographic cut view shows the true-axis y=0 plane. Source centers are (±.046,0),(0,±.046) m, rotor radius .0225 m; depth is -zeta*.046 m. Bars encode observed/model magnitudes on opposing sides for comparison, not velocity vectors. Unit switching preserves bar proportions because both displays share the printed 4.36 m/s conversion. Exact numbers and intervals remain in the DOM table.

Three.js is reused from the existing public-support vendor, with its existing MIT license; no vendor copy is included. There is one WebGL scene, capped DPR 2, no animation loop, and event-driven rendering. Native buttons/selects supply keyboard alternatives to orbiting; the table and linked report remain available when WebGL fails. No permissions are requested.

Static syntax, numerical-field mapping and relative-path checks are documented in the public review. Browser rendering, visual layout and interaction have NOT been verified. This limitation remains visible in the viewer.

The 3D geometry communicates the true-axis plane change from the earlier offset experiment; numerical comparison is also presented as a simpler 2D table. The original scientific figure is not included.
