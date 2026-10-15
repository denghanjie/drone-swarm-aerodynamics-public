# Prospective M31 retained-flock aerodynamic-domain audit

Static design only. No saved geometry, field, receiver model, controller, trajectory, or integration was evaluated to prepare this memo. The review read source code, saved metadata, manifests and historical reports. No repository file was edited and no evidence download was started.

## Frozen input choice and question

Audit exactly the **primary wall-priority poses at 0, 20, 30 and 60 seconds** for wide1000, narrow1000 and wide5000: 12 snapshots and 28,000 vehicle-pose records. This selection is fixed before geometry evaluation. The requested 40-second poses exist in the original public one-second streams, but those streams are not restored in this worktree. The parent chose the already committed compact viewer payload instead: use its exact 30-second poses, with no download, interpolation, regeneration, silent substitution or later time selection.

Question: would the unchanged M28 field's declared geometry/orientation gates admit each retained full-flock pose set, and which ordered rotor/source interactions are inside formula support, explicitly skipped by policy, or invalid? This is a geometry-coverage question, not a force, performance, integration, cadence or physical-validation experiment.

These are retained **simulated, airflow-off M31 poses** with ideal observations. They are exposed development evidence. Their original individual-path refinement checks failed; this audit neither requalifies those paths nor predicts how adding aerodynamic feedback would change them. Passing selected snapshots says nothing about unsaved times, physically measured flights or an airflow-coupled mission.

## Exact public provenance

Original public source/data-manifest commit:

`c591ce2b195fa01b895d4ba881a44a4b92fdd703`

Repository: `https://github.com/denghanjie/drone-swarm-aerodynamics-public`

The three original run IDs are:

| Audit label | N | Seed | Primary run ID |
|---|---:|---:|---|
| wide1000 | 1000 | 2001 | `heldout-2001-1000-wide-wall-priority-0.0025` |
| narrow1000 | 1000 | 2002 | `heldout-2002-1000-narrow-wall-priority-0.0025` |
| wide5000 | 5000 | 2001 | `heldout-2001-5000-wide-wall-priority-0.0025` |

Original paths are `outputs/milestone-31-source/<run-ID>.json` and `<run-ID>.f64`. Their public release identity is recorded in `data/research-data-manifest.json` at the original commit: release `v0.1.0-public`, asset `research-data-v0.1.0-public.tar.gz`, archive bytes `883875762`, archive SHA-256 `03f8b96378c7208f292596bf6152e48ac67bb9cfa155a76c994894c196f57ae7`. No restoration is part of this audit.

| Run | Original `.f64` bytes | Original `.f64` SHA-256 | Original `.json` SHA-256 |
|---|---:|---|---|
| wide1000 | 10137448 | `e9e9f3cd2fb5734040d93143d8c2f2be985a77f68f324a7a0928936006b80772` | `220d88a10fa22f51496381d9681a7282b7068131e38281855957ff660c619d18` |
| narrow1000 | 10137448 | `6bcd0a01c28bb557fd1a7ed305b684e4574077365e067140697a36d1ec5f6c80` | `8dc46948c7316771c535f712459ba1e54e2c01abf55afca55fc9b38d73577dcf` |
| wide5000 | 50681448 | `8f3f9f43fc7cc05aed98d7e1dba23ae547d55d6b7214ad92936b4652e2d80614` | `77761327c0f5309e0190a1334b0dab1c377603fbd3844a3c4d36fdafcb326608` |

The original writer is `outputs/milestone-31-source/study.cjs`; `sim.cjs` constructs each frame as `[time, ...perVehicle(x,y,z,qx,qy,qz,qw)]`, written Float64 little-endian. Each original frame has `1+7*N` values; cadence is one second, with terminal records as applicable. The JSON carries replay metadata, full 17-component initial/final states and science samples. Full-state checkpoints are written at 20/60/120/180 seconds, not at 40 seconds. Do not confuse those checkpoints with the complete one-second **pose-only** stream.

The actual audit inputs were committed at:

`07e5165fa56f2f23bab24562b278dda1c82ed05e`

| Input path | Bytes | SHA-256 from committed manifest |
|---|---:|---|
| `research/m31-restart-2026-10-15/viewer/data.json` | 41823 | `f69cae28818dd0802863b512af96a448ffcd3aa7aa8824f528b4ed59032d613c` |
| `research/m31-restart-2026-10-15/viewer/snapshots.bin` | 3360000 | `c9918697fc61576a9c0454cda354a8d66f42b0b6e21e082cdbf12054b372c927` |

`research/m31-restart-2026-10-15/build-viewer-data.py` documents extraction of exact saved poses, with no interpolation. The compact metadata retains original input hashes. It stores both primary and refinement arrays; **select only `samples[].offsets[0]`, the primary array**, for this audit. Original numerical discrepancies in this metadata are historical context, not new domain results.

## Compact binary layout and exact ranges

`snapshots.bin` has **no embedded binary header and no embedded timestamps**. It is a concatenation of Float64LE arrays. Its sidecar schema is `m31-audit-saved-poses-v1`, `valuesPerDrone=7`, quaternion order xyzw, position units metres. Each vehicle occupies seven values `[x,y,z,qx,qy,qz,qw]`; original vehicle index/order is retained. Sidecar offsets are **Float64-value offsets**, so multiply by eight to get byte offsets. Read exactly `7*N` values (`56*N` bytes) at each selected range. A compact record is not a full 17-component dynamic state; do not fabricate missing velocities or motor states and label them historical.

| Case | Time s | Primary value offset | Byte offset | Byte length |
|---|---:|---:|---:|---:|
| wide1000 | 0 | 0 | 0 | 56000 |
| wide1000 | 20 | 14000 | 112000 | 56000 |
| wide1000 | 30 | 28000 | 224000 | 56000 |
| wide1000 | 60 | 42000 | 336000 | 56000 |
| narrow1000 | 0 | 70000 | 560000 | 56000 |
| narrow1000 | 20 | 84000 | 672000 | 56000 |
| narrow1000 | 30 | 98000 | 784000 | 56000 |
| narrow1000 | 60 | 112000 | 896000 | 56000 |
| wide5000 | 0 | 140000 | 1120000 | 280000 |
| wide5000 | 20 | 210000 | 1680000 | 280000 |
| wide5000 | 30 | 280000 | 2240000 | 280000 |
| wide5000 | 60 | 350000 | 2800000 | 280000 |

The selected payload is 1,568,000 bytes: all seven pose values for all 28,000 vehicle records. Validate both complete-file hashes, sidecar schema, run IDs, counts, times, offsets, file bounds and finite values before geometric work. Freeze these exact ranges in the new protocol. Read the binary itself, not rendered/decimated viewer objects.

There are no per-vehicle active/arrived flags in this compact payload. Audit **every saved vehicle without filtering**, both as a source and as a receiver. Do not infer active eligibility from position, course finish, renderer visibility or crossing counts. M31's saved state list retains all vehicles, but this audit makes no claim about a counterfactual controller's active subset.

## Geometry to classify, without evaluating aerodynamic values

Freeze the unchanged M28 definitions from `outputs/milestone-28-source/aero.cjs`, with dependencies `outputs/step03a-source/wake.cjs`, `outputs/step02c-source/physics.cjs` and `outputs/milestone-26-source/grid.cjs` at the original commit. No call to `fields`, `effectiveThrust`, any receiver root, derivative, integrator, controller or simulation entry point belongs in this audit.

First inspect every pose quaternion without renormalizing it. A prospective input-integrity requirement can use `abs(norm(q)-1)<=1e-12`; preserve any violation as an input failure rather than correcting the data. Compute source/receiver axis `a_i=R(q_i)[0,0,1]`. The exact production orientation criterion is `a_i.z < cos(20*pi/180)`. Test it for **every vehicle**, even an isolated one. The old M31 `maxTiltDegrees` is the maximum absolute Euler roll/pitch used by that simulation, not this axis-z test; it is not a replacement for the audit.

Record all tilt failures and margins. Production `fields` would stop at its first tilt failure before any pair loop. The audit may continue its geometry classification to quantify coverage, but every pair result for a tilt-invalid snapshot must be labeled **diagnostic hypothetical geometry, not a valid field output**.

For every distinct ordered pair `(receiver i, source j)`, preserve the production center-distance gate `||p_j-p_i|| < 3 m`. For candidates, inspect **all four receiver rotors** in the frozen rotor order. Let `x_ik=p_i+R(q_i)[rotor_x,rotor_y,0]`, `v=p_j-x_ik`, `d=v dot a_j`, and `r=||v-d*a_j||`. Let `D=2*sqrt(2)*0.028`, `dmin=2.5*D`, and `H(d)=0.07668*(d+5.817*D)`.

Use the exact branch order and strict/non-strict inequalities below. Do not treat skipped points as validated far-field points.

| Category | Exact policy |
|---|---|
| `outside-center-neighborhood` | center distance >=3 m; all four rotor/source combinations skipped by candidate policy |
| `nonpositive-downstream` | candidate, d<=0 |
| `downstream-cutoff` | candidate, d>=2.5 m |
| `invalid-near-wake` | candidate, 0<d<dmin and r<0.15 m; production would throw |
| `near-field-policy-skip` | candidate, 0<d<dmin and r>=0.15 m; production silently skips, not a supported continuation |
| `radial-cutoff` | candidate, dmin<=d<2.5 and r>=3*H(d) |
| `formula-support-eligible` | candidate, dmin<=d<2.5 and r<3*H(d) |

Within formula-support-eligible geometry, record downstream-fade membership (`d>2`) and radial-fade membership (`r/H(d)>2`) as separate flags. Also record the axis-dot projection sign: the model clamps it at zero but still follows its formula branch. For tilt-valid unit axes it is positive; on tilt-invalid snapshots this is only hypothetical geometry. Do not compute wake speed or claim a positive numerical aerodynamic contribution merely from the support label.

Self-pairs are excluded and counted separately. Keep receiver/source roles distinct: an unordered close pair may give different classifications in its two directions and across its four rotors. An invalid near-wake tuple necessarily lies within the 3 m center gate: for unit axes its rotor/source distance is below `sqrt(dmin^2+0.15^2)`, plus at most `sqrt(2)*0.028` to the receiver center. Thus the independent complete center-pair check can verify that candidate enumeration has not omitted any possible near-wake exception.

## Independent complete coverage check

Use two independently implemented geometric paths on all 12 snapshots, without evaluating the aerodynamic kernel:

1. Primary: production-style radius-3 grid enumeration, stable source-ID order, double-cross quaternion rotation and the exact branch definitions above.
2. Independent: direct all-pairs center enumeration, independently written quaternion matrix rotation, explicit rotor placement/projection and independent category accounting. Do not import the primary grid, rotation or classification helper into this checker.

Compare exact candidate/event sets and per-receiver/per-category counts, not just global totals. Per-receiver temporary lists permit complete tuple comparisons without retaining hundreds of millions of tuples. Record deterministic digests of complete sorted event sets, plus explicit witnesses. Numeric geometry comparisons may use a prospectively declared absolute tolerance, for example 1e-12 m and 1e-12 for axis components, but **branch predicates retain their exact original inequalities**. A mismatch near a threshold is unresolved arithmetic sensitivity, not permission to move the threshold or accept one implementation selectively.

Record signed margins to center radius 3, axis-z threshold, d=0, d=dmin, d=2.5, r=0.15 and r=3H(d). Report counts within the declared near-threshold reporting band and the smallest absolute margin with its tuple ID. Such a band is a diagnostic label, not a new model tolerance. A classification mismatch anywhere blocks a completed agreement claim and any subsequent field evaluation of that snapshot.

Domain failures are the scientific outcome being audited: collect all invalid tuples and all affected vehicles instead of aborting after the first one. Input corruption, nonfinite/nonunit inputs, an implementation discrepancy, or a resource cap must be retained as a distinct incomplete/failed audit state. Do not call a partially examined snapshot domain-clear.

## Counts, bounded storage and prospective caps

The following are schedule cardinalities derived from the declared counts, not results from examining saved geometry:

| Quantity | Each N=1000 snapshot | Each N=5000 snapshot | All 12 snapshots, one pass |
|---|---:|---:|---:|
| Vehicle poses | 1000 | 5000 | 28000 |
| Distinct ordered center pairs N(N-1) | 999000 | 24995000 | 107972000 |
| Logical rotor/source tuples 4N(N-1) | 3996000 | 99980000 | 431888000 |

There are eight N=1000 snapshots and four N=5000 snapshots. Two complete geometry implementations have an upper logical workload of 215,944,000 ordered center-pair checks and 863,776,000 rotor/source classifications; actual rotor geometry is needed only inside the radius-3 candidate gate. Do not count those two checks as twice as many independent physical observations.

Proposed frozen caps: **120 executable wall seconds, one supervised process/invocation, 60,000 pose checks, 220,000,000 center-pair examinations, 900,000,000 rotor-geometry classifications, 256 MiB working-memory ceiling, 64 MiB new raw evidence with 1 MiB reserved for failure records, zero aerodynamic-field/force calls and zero integrated seconds.** Count failed operations too. Use small per-receiver or blocked buffers, not N-by-N-by-rotor materialization. Existing input files are read-only; executable time includes integrity checks and both audit implementations. These are resource limits, not a runtime estimate or a speed benchmark. If exhausted, retain completed snapshots and exact unexamined scope; do not retry, extend the cap or replace a 5000-vehicle case with a subset.

Freeze snapshot order before execution, preferably time-major with wide5000, wide1000, narrow1000 at each of 0/20/30/60 s. Complete and compare both implementations for each snapshot before advancing, so any partial stop has explicit complete/incomplete units. Resource accounting should identify the current snapshot, receiver, source and rotor on interruption.

Store complete per-vehicle category counts and role participation, exact total invalid-pair/invalid-rotor counts, global event-set digests, and a bounded deterministic witness set (for example the first 256 lexicographic invalid/boundary/mismatching tuples per category per snapshot). Explicitly distinguish a capped witness list from complete counts; continue examining every pair after the witness quota fills. A cap on saved witnesses is not geometry subsampling. Reserve enough failure storage to retain current inputs and disagreement details.

For every snapshot report: all-vehicle tilt count; whether production would reject before pair processing; candidate ordered-pair count; all seven rotor-policy counts; invalid distinct ordered-pair count; affected receiver/source IDs and counts; per-receiver supported-source counts; core/fade flags; nearest boundary margins; exact checker agreement; and completion status. Account for every nonself rotor/source tuple: category counts must sum to `4*N*(N-1)`, including the four-per-pair outside-center skips. Report supported geometry even if no near-wake exception occurs; mere absence of an exception does not mean every interaction lies in the far-field model.

## Field-evaluation gate and permissible interpretation

**Aerodynamic field evaluation is outside this audit regardless of outcome.** A later separately frozen field-value study may consider only snapshots for which every required pose/tilt test, every ordered-pair/rotor near-wake test and the independent geometry agreement check completed successfully. A single tilt or near-wake failure invalidates a whole unchanged `fields(states, 'sum-rotor')` call on that full saved fleet. Do not delete an offending source, drop arrived drones, clamp tilt, weaken the near-field rule or report a force from an accepted subset as the whole-flock result.

Passing geometry means only that the declared M28 implementation would not encounter its geometry-domain rejection on those exact poses, subject to the arithmetic audit. It does not establish physical model adequacy, correct multiwake aggregation, obstacle/ground interactions, flight-reference convergence, execution speed, browser performance or predictor generalization. Near-field-policy skips remain an explicit model gap even in an otherwise executable pose set.

This audit addresses the unresolved connection between small prescribed encounters and retained local-3D flocks up to 5000 vehicles without starting another integration campaign or tuning against the exposed predictor cases.
