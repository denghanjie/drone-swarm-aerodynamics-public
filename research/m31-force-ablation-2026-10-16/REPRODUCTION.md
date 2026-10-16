# Reproduction contract

Use the original public repository and the source commit recorded in the publication receipt. Existing official allocations are one-use and closed after invocation; reproduce only in a separate copy with a separately named and recorded allocation. Never delete the checkpoint's lock files or overwrite its raw evidence.

Runtimes used by the parent checkpoint: Node v24.19.0 on darwin/arm64 (actual version will be recorded by the run); Python with NumPy for the independently derived saved-only check. Verify source/result/reference manifests before interpreting output. No new dependencies are installed by this package.

Official commands use source/run.py, an explicit runtime executable, the independently verified source-manifest SHA256 and exact published source commit. Candidate invocation precedes reviewer invocation. The source HEAD must match the manifest's publication commit during both. Supervisor uses one continuous monotonic clock and sampled process RSS. Duration is execution accounting, not a benchmark.

Three.js displays saved numerical poses; browser performance says nothing about solver cost. Only the finest sampled paths appear in the viewer, with slower playback and no interpolation. All three timestep records remain available for audit.
