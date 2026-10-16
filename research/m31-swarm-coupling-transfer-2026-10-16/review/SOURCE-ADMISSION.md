# Historical M31 full-state admission: static feasibility note

This note inspects source, schema, frozen metadata, public manifests and filesystem presence only. It does not parse state arrays to calculate geometry, motor statistics, tilt counts, coefficients or loads; launch source code; extract a binary; or rerun any scientific campaign. Applicability of the new coupled solver to the selected snapshots remains an unanswered admission question.

**Finding:** the six requested full-state checkpoints are available, including the complete-horizon 5,000-vehicle primary checkpoint at 180 seconds. Their recorded schema supplies the four motor-lag thrust states missing from the old public pose-only export. A public binary extraction is feasible after exact source-hash and structural validation. These are exposed, synthetic, airflow-off historical states; a new coupled steady solve would be a frozen-state counterfactual under the newly assumed source/receiver law.

## State meaning and rotor identity

The authoritative schema is the comment and `derivative`, `integrate`, `rotate`, and `wrench` functions in `outputs/step02c-source/physics.cjs`, imported by the historical M31 `sim.cjs`.

| Zero-based state indices | Meaning | Units/frame |
|---|---|---|
| 0–2 | Position `p` | Metres, world coordinates, +z up |
| 3–5 | Translational velocity `v` | m/s, world coordinates |
| 6–9 | Quaternion `[qx,qy,qz,qw]` | Dimensionless, xyzw order; body-to-world rotation |
| 10–12 | Angular velocity | rad/s, body coordinates |
| 13–16 | Four motor-lag thrust states | Newtons, in the original rotor order |

The orientation interpretation follows `rotate(q,[0,0,T/m])` for world acceleration and `qdot = 0.5*qmul(q,[omega_body,0])`. Quaternions are normalized after each RK4 integration step. This identifies the intended convention; it does not replace a prospective per-record finite/norm check. Do not renormalize or repair historical inputs silently.

With `a=0.028 m`, the original rotor order is:

| Rotor index | State thrust | Body-frame rotor-center offset | Reaction sign in original wrench |
|---|---|---|---|
| 0 | state[13] | `(+a,+a,0)` | +1 |
| 1 | state[14] | `(-a,+a,0)` | -1 |
| 2 | state[15] | `(-a,-a,0)` | +1 |
| 3 | state[16] | `(+a,-a,0)` | -1 |

This differs from the corner ordering used in the recent designed solver fixtures. Historical thrusts must remain paired with these historical offsets. Use `rotate(q,offset_r)` for world rotor offsets and `rotate(q,[0,0,1])` for the source/receiver axis. Reconstructing an arbitrary square frame from the axis alone loses yaw and can permute unequal rotor loads; it is unsuitable here.

The motor equation is `df_r/dt=(u_r-f_r)/0.04 s`. The controller's `u_r` is a clipped thrust target in newtons, while state[13:17] contains the lagged values actually used by this airflow-off dynamics model. These are not PWM, measured RPM, shaft power, or measured effective aerodynamic thrust. The four checkpoint fields do not preserve held actuator commands or mission/controller history. The 17-state vector alone should not be advertised as a complete general restart state.

## Generator, model and checkpoint identity

The requested IDs are `heldout-2001-{1000,5000}-wide-wall-priority-0.0025`, at exact saved times 20, 60 and 180 seconds. The historical protocol names seed 2001, the wide `factory-v1` geometry, the frozen wall-priority controller, local 3D Boids, ideal observations, airflow off, 100 Hz control and primary RK4 step 0.0025 s. Vehicle mass is 0.027 kg; gravity is 9.81 m/s². The factory is synthetic. The 5,000-vehicle refinement covered only 60 seconds; its existence does not provide a refined 180-second reference.

`study.cjs` writes checkpoint objects `{t,states,passed,stopReason}` at 20/60/120/180 seconds when reached. `states` is the current full state array in original vehicle order. It does not delete completed vehicles; the simulator explicitly continues flying completed vehicles. `passed` is an aggregate crossing count, not a per-vehicle active mask.

The separate one-second `.f64` replay stream contains time plus position/quaternion only. Likewise, `research/m31-restart-2026-10-15/viewer/snapshots.bin` contains seven-value poses, not motor or velocity states. The older pose-only force reference explicitly used prescribed nominal rotor forces; it did not recover historical motors. Neither older product can substitute for these 17-component checkpoints.

Selected frozen source hashes, transcribed from `outputs/milestone-31-protocol.json` and corroborating historical manifests:

| Source | SHA-256 |
|---|---|
| `outputs/step02c-source/physics.cjs` | `0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1` |
| `outputs/milestone-31-source/sim.cjs` | `2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e` |
| `outputs/milestone-31-source/study.cjs` | `b78d712bc66ba12c9faa6823520967cba8742edb5853e5d6b58e6a709cb9f5e6` |
| `outputs/milestone-31-source/wall-filter.cjs` | `8273cc40a9530748fe43e9ef0a4d9a995ee152f9968ce2368e61e2f205502512` |
| `outputs/milestone-31-source/factory.cjs` | `fe46384aac6150c45a2ba38e4494da16969aeab4a8875a8596f6ad8e53bb2c40` |
| `outputs/milestone-31-source/factory-wide.cjs` | `8ea0d8784accfc039fee9ca2a2c0a86dc8e502b6d1003e4de54a8df8a999cc22` |

The frozen protocol also pins the grid and contact geometry dependencies. Pin the complete required source set in the new package; this short table is not a substitute for its dependency manifest.

## Availability and public extraction lineage

Historical public base: `c591ce2b195fa01b895d4ba881a44a4b92fdd703` in `denghanjie/drone-swarm-aerodynamics-public`. The 1,000-vehicle checkpoint files are Git-tracked at that base. The 5,000-vehicle files are indexed public release assets in `data/research-data-manifest.json`, release `v0.1.0-public`, asset `research-data-v0.1.0-public.tar.gz`. The public output manifest pins all six files.

Each filename below is prefixed by `outputs/milestone-31-source/checkpoint-heldout-2001-` and suffixed by `.json`.

| Filename middle | Expected JSON bytes | Published SHA-256 |
|---|---:|---|
| `1000-wide-wall-priority-0.0025-20` | 470998 | `8adc8213f6b036f498639bf070af53d3777fe1771c34f41bb54498e48be0f304` |
| `1000-wide-wall-priority-0.0025-60` | 470298 | `43fbf672322f063eac07c55131ea050099a38478c73763656760ae4382cb2b48` |
| `1000-wide-wall-priority-0.0025-180` | 470947 | `bd8ac3a4695f796b60fdf82eff0e5dc102500611c61ba37eac906d63180e7e6c` |
| `5000-wide-wall-priority-0.0025-20` | 2357471 | `64696f6aca0d74a00f8540f53abcb46b4bd8dd6ed387f5192506c84967ab267e` |
| `5000-wide-wall-priority-0.0025-60` | 2351516 | `9538f037be4a62abb9a550c7ac2a7aa182556c448136c86d66d1e09492fd050b` |
| `5000-wide-wall-priority-0.0025-180` | 2349503 | `1a4ba3d4cf3ffee87f783a2ba7e40865a438b342ff71e3ace16e5341ef208af4` |

Filesystem listings show all six files with these byte sizes. The 5,000/180 file has `t:180` at its beginning and closes with `passed:5000, stopReason:null`; the older run metadata records the full primary horizon. This is evidence that the retained endpoint is available, not a fresh state-array audit. The extractor must still verify each complete-file hash, parse the JSON, and require exactly the declared number of rows with exactly 17 finite numeric values. No current full-file hash calculation or row-count scan was performed for this note.

The public release audit describes a sanitized synthetic-research export, retaining research values while removing private paths and host metadata. The typed numeric checkpoint payload is suitable for a new public derivative provided its bytes match the public pins. Do not copy the private working directory or unrelated runtime records into that derivative.

A prospective exporter should write Float64 little-endian, snapshot-major then original vehicle-major then state-index order, with a new explicit 17-value schema. Preserve values decoded from the saved JSON without filtering, centering, rescaling, quaternion correction, reordering, or interpolation. A sidecar should contain relative public source identifiers, source JSON size/hash, exact time and count, units and quaternion convention, original motor/rotor order, binary offsets with explicitly named units, binary lengths/hashes and the extraction-source commit. Validate decoded binary equality to the parsed JSON. Keep timestamps in the sidecar or declare any embedded timestamp layout explicitly; do not silently reuse the old seven-value schema. No absolute workstation paths or host identifiers belong in the public sidecar.

## Scope of a later predeclared admission and sparse solve comparison

1. **Freeze these six inputs and all-vehicle scope.** They are exposed historical development snapshots, despite `heldout` in their original filenames. Do not select times or vehicle subsets after viewing new admission or load outcomes. Preserve completed vehicles as both possible sources and receivers; neither crossing count nor position permits an active-mask reconstruction.

2. **Admit the new nominal-force interpretation explicitly.** Taking state[13:17] as the new frozen `f0_ir` uses the old airflow-off motor-lag state as a nominal input to a different aerodynamic law. It does not recover an old ideal-power or fixed-command condition. Require every one of the four nominal values to be finite and strictly positive and every total finite; do not add epsilon, clamp, average, or replace a nonpositive value with hover thrust. A failure must remain a failure of that full snapshot under the four-active-root contract. An inactive-rotor extension would be a separate model change.

3. **Declare orientation and geometry admission before evaluation.** Check finite/unit quaternions and axes, exact historical rotor placement, and the complete near/downstream/radial branch policy. The old M28 wrapper's 20-degree policy, the 45-degree sufficient DAG theorem, and the broader assumed domain of the recent hexagon example are different concepts; choose and state the intended policy instead of silently mixing them. The old saved `maxTiltDegrees` is a maximum of Euler roll/pitch, not the required axis-z or full-snapshot admission test. A source-dependent load solve is permitted only for an entirely admitted snapshot; unsupported near pairs cannot be discarded to manufacture a solvable subset.

4. **Verify sparse coverage, not just final forces.** The center-radius broad phase must reproduce the exact strict three-metre candidate gate, including negative coordinates and cell boundaries, with stable ascending source IDs. Evaluate all four receiver rotors at their rotated offsets. Preserve rejection accounting before omitting zero contributions. Independently check complete candidate/edge sets or deterministic complete-set digests and boundary witnesses; a force comparison on the same accidentally truncated matrix would not validate the enumeration. Freeze memory, pair/rotor visit, wall-time and output caps, including partial/failure records.

5. **Freeze the admitted coefficients and compare defined solvers.** Confirm finite nonnegative coefficients and the whole-cube scaled speed cap. Cache those fixed coefficients for the solve only because the new hypothesis keeps shape/support independent of effective thrust. Direct descending-height evaluation is eligible only if every retained positive dependency respects its order; otherwise use the declared cyclic solver, without relabeling an ineligible case as a direct result. Retain all four receiver roots, report source/receiver total mismatch, and independently check residuals and rotor forces with evaluation-error limitations. Count coefficient construction, sparse contributions, update roots and residual roots separately. An operation-count comparison is not a runtime benchmark.

6. **Keep the interpretation static.** Positions, attitude and motor states come from moving, airflow-off simulated trajectories. The new calculation freezes them, ignores unsteady wake history and does not feed forces back into integration or control. Translational/angular velocities remain preserved evidence, not an implicit validation of a steady inflow approximation. Ground, obstacle, vehicle-motion and unequal-source-rotor effects are not repaired by this calculation. Passing it would establish executable domain and numerical agreement at six fixed historical snapshots, not an airflow-coupled mission, path refinement, safety, physical calibration, or a 5,000-drone real-time demonstration.

These recommendations define limitations for a future separately frozen question. This note allocates no experiment and makes no prediction about how many snapshots will be admitted or what their coupled loads will be.
