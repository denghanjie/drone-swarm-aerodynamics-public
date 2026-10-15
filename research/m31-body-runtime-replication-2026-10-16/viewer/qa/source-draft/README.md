# Runtime replication viewer — unbound source draft

This directory is a viewer-only draft excluded from the scientific source freeze. It is not a scientific result, a published viewer, or a browser-verified artifact. No evidence is bound, and no adapter or browser has been run for this draft. The explicit unbound `viewer-artifact.json` contains no predecessor result, controls, poses, review or samples. No `evidence/` directory exists at this stage.

The implementation starts from the tested original interrupted-campaign viewer, but the new schema is `m31-runtime-body-viewer/1`. The loader rejects the predecessor schema and stops before any scene import when unbound. The binder requires this replication's directory, actual source commit, source-freeze pin, terminal result pin and exactly one designated final external observation. It rejects source/result mismatches. Binding and browser QA await separate authorization and actual terminal identities.

The intended actual-data view covers all saved receiver records for the four prescribed static fixture families, planned N = 50, 500, 5000 and 5000. Family 3 is preferred only when it has actual selectable evidence. Original17 positions and xyzw quaternions drive enlarged static glyphs; conventional RGB world-origin axes are labeled display guides. These are prescribed fixtures, not local Boids motion or reconstructed flight.

Per-rotor tables expose R and Q reference inflow/force, raw GPU inflow/force, H handoff force, display-only GPU−R/H differences and saved gate dispositions. Body tables show saved R/Q/GPU effective and nominal values. H contains no body payload, so the viewer explicitly says “Not stored in H”; it never assembles a replacement body result. Saved headers, validity masks and scalar hex bits remain inspectable.

Fixed pair inputs and scalar root controls are separate selectors. Pair controls display actual saved positions/axes/offset and diagnostics. Scalar controls show the original operands and saved R/Q/GPU/H fields without inventing geometry. Canonical files and recognized exact-layout partial R/Q/H files may be displayed; absent, truncated or unsupported partial files remain visibly absent or receipt-only.

Scientific qualification, byte consistency and the final external observation remain separate. A saved failure sample can identify a failure; absence from the capped failure list cannot prove an individual pass. A complete saved assessment with pass true is labeled as a global saved assessment, never recomputed by this viewer.

The browser will hash every fetched asset against its byte-length/SHA-256 descriptor. The offline binder will hash the complete terminal raw manifest, including policy arrays, but policies are not browser assets. Errors disable selectors, clear records and remove the scene. Family switching aborts stale loads and disposes old scenes.

No scientific host/generator/independent module is imported, and no shader compilation, profile/root evaluation, input generation, WebGPU compute or simulation belongs to this viewer. The existing vendored Three renderer uses WebGL only for displaying saved geometry. No package installation is required.

See [DATA-CONTRACT.md](DATA-CONTRACT.md), [QA-PLAN.md](QA-PLAN.md), [source checks](SOURCE-STATIC-CHECKS.json) and [source provenance](SOURCE-DRAFT-LEDGER.json). Those source checks are not actual-data or browser validation. The historical link points to the already-existing airflow-off saved-pose audit and is explicitly separate.

## Terminal-record adaptation, pending final review

The sole scientific attempt is now terminal. Source `f12d8c836e7b991ec33e6de662d00ed05dcce33e` reached runtime 155.0.8059.80, initialized three pipelines and saved the 15 pair inputs, 146 scalar inputs, CPU R/Q diagnostics and host controls. The first `controlPairs` dispatch was submitted with 15 active / 64 launched invocations. Its API report says `TypeError: Failed to fetch`; the output persistence reservation never started, and no GPU output binary was saved. No GPU root dispatch, H output or main-family input was reached. This does not establish the fetch failure's underlying cause.

The draft now selects the actual saved dispatch/runtime/API JSON records for future byte binding and will state “GPU dispatch submitted. Output unavailable.” GPU pair cells will say “Output unavailable”; CPU diagnostics stay separately labeled. It does not equate missing GPU output with no GPU work. All main families stay empty and no body result is inferred.

`ACTUAL-EVIDENCE-PREPARATION.json` is a read-only inventory and intended descriptor plan, not the viewer binding or final-review authority. `viewer-artifact.json` remains explicitly unbound. The scientific capture observation is retained as an execution report and does not replace the still-pending saved-review final authority. Adapter execution, final binding, browser QA and publication remain deferred.
