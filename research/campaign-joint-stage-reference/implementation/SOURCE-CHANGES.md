# Source changes from the recovered held-input campaign

Unchanged copies: the complete original `snapshot/` tree, `src/source.cjs`, and `src/exact-aero.cjs`. They preserve source summation order, wake support/guards, fixed hover-induced amplitude, receiver torque convention and local Boids parameters. Original recovery artifacts are untouched.

New modules replace the campaign harness without changing frozen physical equations:
1. Synchronized whole-swarm RK4 with normalized geometry copies and raw aerodynamic derivatives.
2. Branch/regularity diagnostics on old saved paths and every prescribed new sample, plus conservative unresolved-jump stop.
3. Integer1/51200s timing and 100Hz left-command semantics.
4. Compact branch/controller/field records, raw full17 state arrays, SHA256 identity and selected exact stage evidence.
5. Single-window supervised serial scheduler, prospective gates, resource stops and retained skipped rows.
6. Independent adversarial fixture integration and an actual-record-only Three.js viewer.

The held arm calls the original exported integrator without modifying its function bytes. Diagnostic evaluation neither changes commands nor feeds back into dynamics. The new algorithm has its own freeze identity and does not overwrite historical failures or the old source aggregate.
