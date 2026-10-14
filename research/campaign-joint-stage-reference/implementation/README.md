# Joint-state temporal-reference implementation

Status: authored and statically inspected; **no fixtures, preflight, compatibility, simulations, or viewer extraction have been executed by the implementation worker**. The coordinator owns adoption, independent review, source freeze, and the single numerical budget.

## Numerical target

`src/joint-step.cjs` constructs each full-swarm RK stage before evaluating one frozen `lean` field. Only a separate geometry copy normalizes stage quaternions. The original `A.derivative` receives the raw state and unchanged held controller commands; accepted endpoints retain original normalization. `src/run.cjs` calls frozen `M.integrate` unchanged for H/P. Both families compute genuine local 3D Boids at each nonterminal 100 Hz control event from their own evolving states.

## Modules

- `joint-step.cjs`: pure synchronized stages, explicit geometry extension, stage/endpoint failure payloads.
- `branch-audit.cjs`: every ordered rotor/source geometry pair, signed extrema and conservative sampled-range jump risk; no smoothing or event localization.
- `controller.cjs`, `controller-record.cjs`: original controller plus read-only branch diagnostics and compact binary commands/IDs/scalars.
- `preflight.cjs`: compressed transport/raw identity checks and old-path controller hashes; no interpolation.
- `run.cjs`: exact event clocks, original held integrator, authoritative swept-contact checks, raw endpoints, selected raw stage evidence and audit signatures.
- `compare.cjs`: original geodesic primary comparator, separate stable atan2 diagnostic, frozen absolute/reduction gates and skipped rows.
- `campaign.cjs`, `supervise.cjs`: serial matrix, first-stop behavior, single global 300 s wall/CPU and 45 s job caps, 200 MB amended storage cap, 2 MB failure reserve, no budget restart.
- `io.cjs`, `freeze.cjs`: explicit LE Float64, SHA256, atomic fsynced writes, preservation of interrupted `.partial` artifacts, transitive source/input/runtime freeze.
- `build-viewer.cjs`, `demo/`: actual-record Three.js display plumbing. No synthetic animation trajectories or physical reference claim.

## Controlled entry points

After source review and coordinator adoption, coordinator may invoke `node src/freeze.cjs --coordinator-adopted`, then once `node src/supervise.cjs`. Any fixture failure stops the cycle. The supervisor refuses a second attempt. Model tests must not be run separately or before freeze. `node --check` is static syntax validation only.

Reviewer fixtures in `../robustness-review/` are separately hashed by the freeze. The source/input manifest must be re-reviewed before freeze if any source changes. `snapshot/` and `src/exact-aero.cjs` are unchanged copies of recovered frozen source; originals outside this directory have not been edited.

## Retention and limits

All new numerical binary artifacts are uncompressed and charged at their full byte lengths. Preserved transport fragments and materialized input arrays are both charged. Every required geometry sample audits every ordered receiver-rotor/source pair, including pairs outside field-neighbor support. Actual domain checks use production eligibility. Every observation retains one 32-byte SHA256 signature. The sidecar gives exact observation schedule and count; the signature encodes predicate signs, not raw margins.

Per-run signed minima, maxima and nearest margins retain identity and time. First/worst brackets per category retain whole-swarm geometry and raw J-stage values in indexed LE Float64. Exact failing J stages also retain commands, available field/derivatives and guard. Other raw J stages are not reconstructible from hashes. Historical dense and new J3 dense states are retained; other new runs retain full17 common endpoints. H/P refresh roles reference the already-audited identical endpoint signature rather than duplicating bytes or renormalizing the state.

An unexpected exception inside the unchanged held integrator cannot expose its private intermediate stage. Such a failure is explicitly marked `internalFailingStageUnavailable`, with exact integrator input, held commands and inflow; it is not mislabeled an exact failing internal state. No post-failure numerical replay is attempted. This makes the reference fail closed.

First/worst category brackets are sampled brackets, not exact events. The worst bracket is selected by largest absolute signed-margin change among transitions in that category. A risk range among equal-time RK trial states is distinguished from an accepted-endpoint bracket; neither proves an actual crossing. Both block acceptance as prescribed.

A kill can leave a signature prefix or `.partial` artifact. The supervisor inventories actual byte lengths and complete fixed-width records, keeps a separately labeled last durable checkpoint, and withholds qualification. The scientific result is gated by execution validity and every seed-specific screen, never by the replay appearance.
