# Frozen prospective experiment: collective force versus full load feedback

## Question and status

After the completed motion-feedback checkpoint, does omitting the **added aerodynamic roll/pitch moment**, while retaining its collective force, materially change this one controller's short 16-drone trajectory? The prior maximum on/off position discrepancy was 1.102444 m over 2 s. This motivates a mechanism comparison; the seed, duration and controller have already been exposed. This is not fresh confirmation, physical validation, additive causal attribution, a stability certificate, a speed benchmark or a novelty result.

Freeze this protocol, exact config, all executable dependencies, independent reviewer and six reference recordings in a source manifest. Publish and verify the exact remote source bytes before any target execution. Syntax/source reading is permitted before freezing; model imports, controls, target computation and parameter trials are not. No new literature acquisition. All earlier allocations remain closed.

## Three arms

1. `off`: nominal rigid-body model, no mutual airflow solve.
2. `coupled`: unchanged current-pose coupled solve, applying effective-minus-nominal axial force and roll/pitch moment.
3. `force-only`: the **same coupled solve on this arm's own current state**, but apply only the collective force correction. Set the *added* roll/pitch torque to zero. Keep all nominal rotor torques (including nominal roll/pitch and yaw), gyroscopic dynamics and motor lag. This is a synthetic wrench intervention, not a physically realizable reallocation of individual rotor loads.

The unchanged source-total/ideal-power closure and lean geometry builder remain provisional. Each arm rebuilds its own geometry at every globally synchronized, quaternion-normalized RK4 stage, and updates the original local Boids controller every 0.01 s. Commands are held within each integration step. No arm is forced to follow another arm's evolving states or commands. All start with identical states; each then evolves independently.

Store `forces` as **modeled solved rotor loads** in every arm. `modeledCorrections` contains the unmasked effective-minus-nominal force and moment. `corrections` contains the actually applied force and moment. For force-only these differ in the torque field. The force-only `forces` must never be described as physically applied individual rotor thrusts. At the shared initial Boids state, full and force-only solved loads and force must match exactly; this equality is not required after the paths diverge.

## Fixed allocation and order

Maximum 12 trajectories. No tuning or alternate seeds.

- First: previous offset pair, fixed nominal commands, 0.5 s, force-only, at h = 0.005, 0.0025 and 0.00125 s. Positions [-6,0,4.5] and [-5.96,0,5.1] m; zero velocity/body rate; identity quaternion; nominal rotor state mg/4. This tests moment suppression under a nonzero modeled differential load.
- Next: original local 3D Boids, n = 16, seed 260201, duration 2 s, off and coupled, same three timesteps. They are repetition controls against the six pinned previous recordings. Same shared broad route/avoidance/controller and initial generator. No imposed flat height or prescribed per-drone tracks.
- Conditional on all first-nine completeness, reference, pair and sampled-refinement gates: run force-only Boids at the same three timesteps. Otherwise skip these three and retain failure evidence.

No comparison outcome (zero, small or large) is a validity gate. Do not stop early for a disappointing effect or extend for a promising one. A rejection of model domain, source consistency, contact envelope, finite state, wall/RSS/storage budget closes this allocation without a retry. The existing per-path recording catches a model rejection and preserves its accepted prefix; scheduled other diagnostic paths may finish within the same resource caps. Global resource failure terminates the campaign.

## Implementation and diagnostic gates

The unchanged adapter analytic controls execute once. These verify existing lever-arm force/moment bookkeeping. Additional force-only pair checks at every 0.1 s saved endpoint require full orientation/rates/horizontal drift within 1e-12 of their initial zero/identity values, applied moment zero, initial modeled pitch moment positive and initial collective correction negative. Vanishing pair rotation is expected **by construction**; it does not validate a physical approximation.

All force-only integration-stage scalar diagnostics require zero applied moment; endpoint vectors require force identical to modeled force and zero applied moment. For off/full, added forces and moments retain previous meanings. The saved-only reviewer independently reconstructs these quantities at every endpoint and first/last captured step stage.

For each of six off/full Boids paths, compare every shared saved sample's t, states, commands, forces, applied corrections, derivatives, geometry witness and group summary to the pinned old record with exact JSON numeric/structural equality. Ignore elapsed timing and new modeled-correction metadata. This is equality of stored numbers, not floating bit-pattern proof or independent physical evidence. Any mismatch disallows conditional force-only Boids execution.

Sample at 0.1 s including both endpoints. Existing maximum sampled discrepancies: position Euclidean m, velocity Euclidean m/s, sign-invariant full quaternion orientation radians, maximum per-rotor modeled load difference divided by nominal mg/4, and body-rate Euclidean rad/s. Adjacent-grid discrepancy must satisfy fine error ≤ tolerance, and fine ≤ 0.75 × coarse, unless both adjacent errors are below 1% of tolerance. Tolerances: position 0.001 m; velocity 0.001 m/s; orientation 0.0017453292519943296 rad; modeled rotor 0.001 hover units; body rate 0.001 rad/s. Below-floor passes do not establish observed RK order or rigorous trajectory error bounds. Load residual ≤ 1e-9; source/receiver mismatch ≤ 2e-9.

## Fixed analysis

At each timestep report all three Boids pairwise contrasts: off/full, off/force-only and force-only/full. These are nonnegative maximum sampled differences, not additive components. Also report maximum sampled body-axis angle (excludes yaw rotation about that axis) and body-rate difference. Full orientation distance must not be labeled tilt. For each path report maximum recorded stage tilt from vertical, modeled/applied added moment maxima, final group centroid, candidate swept separation and controller saturation count. Those diagnostics do not establish collision freedom, stability, measured thrust loss or physical flight limits.

Interpret force-only/full discrepancy relative to the **sum** of their observed medium/fine discrepancies only as descriptive numerical-resolution context, never a rigorous bound or significance test. Do not fit thresholds after reading outcomes. No statistical inference over seeds: one exposed seed, deterministic paths, no physical observations.

## Independent check and limits

Frozen Python/NumPy reviewer reads saved records only. Reconstruct modeled geometry and loads through the previously audited independent reference; reconstruct nominal body derivative plus applied wrench. Check modeled versus applied corrections separately, all saved endpoint arrays, first/last full RK stage witnesses, saved-slope step assembly, reference equality, gates, comparison statistics, schedules, source/reference/result hashes and decision counts. Do not reintegrate paths or regenerate Boids commands. Other integration stages have scalar candidate diagnostics and static source review only. Candidate contact checks are not independently reconstructed over all steps. Assertion count is an implementation-audit count, not independent experiments.

## Resource and evidence limits

One candidate invocation, 300 s wall under a single-process monotonic supervisor, cooperative 280 s guard, 768 MiB RSS; one saved-only reviewer invocation, 120 s and same RSS. No retries, extra pilot runs, paid resources, installation or downloads. Scientific directory aggregate cap 40 MiB, including both run records/logs and reviewer output. Candidate normal-write allowance 32 MiB reserves 8 MiB for failure retention; stdout/stderr total cap 4 MiB. Resource timing is accounting, not performance evidence. The prior six Boids records total roughly 16.36 MB; the added third arm motivates this prospectively larger evidence cap.

Save exclusive invocation locks, all successful and failed prefixes, stage diagnostics, controls, 0.1 s endpoints with full geometry, first/last step witnesses, raw output, independent checks, readable claim/limitation ledger, publication receipt and Three.js paired replay after the run. Viewer only displays saved records with raw SHA-256 checks, common spatial bounds, uniform colors and clear modeled-data labels; it runs no scientific solver. Preserve all previous packages and keep port 8876 serving.

## Literature and claim scope

Use the verified-scope citations in the prior motion-feedback bibliography and literature ledger: Reynolds (1987) for local flocking rules; Bauersfeld et al. arXiv:2403.13321v3 for inherited hover jet-shape motivation. No claim that either supports this synthetic moment mask, source-total closure, moving pose extension or receiver model. The prior Simmons–Hatke access attempt admitted no measurement; it remains closed. New work is original numerical diagnostic code. All force, moment, position and tilt results are simulation predictions. Do not infer a novel contribution without separate prior-art review and broader evidence.

## Decision and restart

If code/source/repetition/independent checks fail: diagnose saved evidence, preserve failure, and require a separately frozen repair experiment. If they pass: state the observed within-model sensitivity, whether below-floor gates limit integration-order interpretation, and what the synthetic mask removes. A following distinct question should be chosen only from recorded evidence and current physical limitations; no automatic parameter sweep. Overall 5,000-drone accuracy–computation and physical-validity goals remain incomplete.
