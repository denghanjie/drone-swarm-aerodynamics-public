# Coupled-stage source implementation draft

This package is source-only, unfrozen and unexecuted. The previous scientific window ended at 03:00 UTC on 17 October 2026. The parent reports a new user-authorized window from 03:06:20 to 05:06:20 UTC; execution is still prohibited until source review, closure and public verification are complete. This drafting phase has not imported the candidate, run syntax or scientific tests, launched a browser, used the network, or changed Git state. The parent owns the final authorization binding and launch allocation.

## Owned files and injected interface

This note describes `source/adapter.cjs`, `source/browser-driver.cjs` and `source/science-config.json`. The supervisor, browser loader, bundler, reference and checker are separate collaborators' files. The driver exports only `createDriver`; it has no CLI, fetch, browser launch or automatic experiment.

```js
const driver = createDriver({physics, swarm, Grid, geometry, native});
const summary = await driver.run({config, initialInput, append, guard});
```

The supplied dependencies are frozen byte-identical slices from the previous native-fresh package: generation `step02c-source/physics.cjs`; generation `milestone-31-source/{sim,grid,geometry,factory,factory-wide,wall-filter}.cjs`; and the native load module with its existing kernel dependencies. The loader supplies its factory-selection `process.env.FLOCK_FACTORY_VARIANT='wide'` shim and existing Buffer compatibility shim. No other module is required by these two files. The local driver requires only `./adapter.cjs`.

`initialInput` is the verified saved `fresh-a-t5.json` object with 64 ordered IDs and 17 binary64 hexadecimal words per drone. Its exact path, 21,955-byte size and SHA-256 are in the science configuration. The supervisor must verify the actual file before passing it to the driver. The driver verifies shape and ID order but does not pretend to validate a filesystem hash from an object alone.

`append(kind, record)` is asynchronous and must acknowledge only after durable persistence. `guard()` is the supervisor's synchronous cooperative resource/deadline guard. The driver is single-use. It returns a small production summary; complete stage evidence is retained through append events. A producer `complete:true` is not independent qualification.

## Fixed scientific counts

The continuation retains the original dt=0.0025 seconds and lasts 0.02 seconds from original time 5. The coupled arm uses eight full-swarm steps, four simultaneous stages per step, and exactly 32 native F calls if complete. Each one requires an independent reference state that is admitted and has passing load bounds. A refusal is a failure; it does not reduce the denominator or trigger a replacement state.

The matched off arm has eight steps and 32 nominal-load derivative stages, zero native calls, and its own evolved states and control updates. Both arms start from the same saved input. Local Boids/control updates occur at relative time 0 and 0.01, using each arm's actual state. The inherited broad route, grid neighbors, wall-priority filter, controller, actuator limits and motor lag remain in use. Safety checks preserve the inherited vehicle-height, obstacle-segment and drone-segment contact checks.

Before the main continuation, the fixed control suite consists of:

- Twelve wiring groups: five expected acceptances and seven expected rejections. The positive groups consume six single-drone derivatives because the ID-permutation group contains two drones. No group calls native F or an independent aerodynamic solve.
- Nine manufactured runs: three analytic cases at dt=0.0025, 0.00125 and 0.000625 over the common 0.01-second interval. These require 4, 8 and 16 steps per case, 84 total steps and 336 derivative stages. They have zero native calls. Each case emits one additional analytic/refinement summary.
- One raw first-k2 quaternion diagnostic, derived from the primary first k1, with zero additional native or reference evaluations.

The loader separately reruns its 56 fixed Buffer shim assertions. Those are infrastructure checks and are not counted as native calls, independent aerodynamic states, wiring groups or manufactured stages. Prior Buffer qualification remains provenance only.

## Projection and RK expression graph

Every whole-swarm stage first owns a copy of its raw 17-component states. For q=[x,y,z,w], the explicit binary64 expression is:

```text
s = ((x*x + y*y) + z*z) + w*w
n = sqrt(s)
q_projected[j] = q_raw[j] / n
```

All products, additions, divisions and the correctly rounded square root are individually binary64 operations. Invalid/nonfinite states and zero or nonfinite norms fail. This intentionally replaces the earlier adapter's unspecified `Math.hypot` projection evaluation with an independently reconstructible expression graph. The projected quaternion is used consistently in native preparation, qdot, inverse frame conversion and all derivative geometry. Nominal motor states are unchanged.

For each accepted common base y, the raw stage arrays are y; y+(h/2)k1; y+(h/2)k2; y+h*k3. Each is projected before evaluation. The raw endpoint component is evaluated as:

```text
y + h*(((k1 + 2*k2) + 2*k3) + k4)/6
```

The endpoint is then projected. Intermediate stages do not overwrite the common base. Raw endpoint and failed final projection evidence are retained, as are all completed stage records preceding a failure. Main stage IDs are exactly `coupled-step0-k1` through `coupled-step7-k4` and `off-step0-k1` through `off-step7-k4`.

The raw diagnostic records deterministic sqrt-of-rounded-squares norm and defect before the first k2 projection. It checks only the declared norm prerequisite at 1e-10; it is not a full preparation attempt. The frozen native geometry implementation uses `Math.hypot` for its own norm predicate, so the diagnostic is not claimed to reproduce that library operation bit-for-bit. A passing diagnostic implies neither complete geometry validity nor modeled-domain admission. Projection is prospectively selected and is never activated as a rescue for this diagnostic.

## Total-load consumption

The native interface returns total delivered world force and world thrust-arm moment. Neither quantity is an external correction. For each stable ID, the adapter begins with the frozen `physics.derivative(projectedState, command)` to preserve position kinematics, quaternion kinematics and first-order nominal motor dynamics. It then replaces translational acceleration with worldForce/m and subtracts gravity from its z component.

The adapter inverse-rotates native worldMoment with conjugate projected quaternion using the frozen `physics.rotate` expression. This gives `bodyArm`. It computes the nominal actuator wrench from state components 13–16 and retains its yaw reaction component as the explicitly provisional policy:

```text
totalBody = [bodyArm.x, bodyArm.y, bodyArm.z + nominalYaw]
gyro = cross(omega, [omega.x*Ix, omega.y*Iy, omega.z*Iz])
omegaDot[k] = (totalBody[k] - gyro[k]) / I[k]
```

The native thrust-arm moment includes no reaction yaw. Delivered thrust is not written into the motor state; motor derivatives remain (command - nominalMotor)/motorTau. This draft changes no physical coefficients or aerodynamic law.

The binding layer requires exact stage-token agreement, exact projected input words, exact native raw-state association, unique complete stable load IDs, and finite correctly shaped load vectors. Native output order may differ: consumption maps by stable ID. The caller creates the stage envelope; a previous stage's raw input or ID association cannot be silently reused.

## Evidence and persistence

Each main stage append uses schema `m31-coupled-stage-v1` and includes the arm, step/substage, relative and original time words, dt, status, native-call count, raw pre-projection state words, command words, canonical projected `nativeInput`, encoded native evidence and per-drone consumption records. Each per-drone record carries raw/projected state words, norm-square and norm words, command and nominal-motor words, delivered rotor/collective/world-force/world-moment words, body-arm moment, nominal yaw, total body moment, gyroscopic term and the exact 17 consumed derivative words.

Every successful native result is encoded before load binding. Refused results remain encoded. If the result schema prevents the normal encoder from running, `nativeMalformed` retains the encoder error and a schema-independent snapshot of the entire response, with exact binary64 words for numeric values, explicit accessor/unserializable markers and cycle references. A thrown native call is likewise retained. Failed stages are appended and stop that arm. The matched off arm may still produce its fixed independent evidence; no failed coupled stage is retried or replaced.

Scientific work is caught before one durable stage append outside the catch. An append failure propagates as a persistence failure; it cannot mutate a frozen record, create a second stage append or be reclassified as a new numerical outcome. A filesystem failure can prevent durable storage; neither the adapter nor driver claims otherwise. The supervisor must preserve its first operational error and available journal.

The native evidence carries `semanticInputSha256` and `inlineInputCanonicalSha256`, both for compact canonical UTF-8 nativeInput JSON with no newline. These names do not assert that a file already exists. The controller separately saves each primary canonical input sidecar before acknowledging the stage and indexes its actual `{path,bytes,sha256}` under `result.inputs[stageId]`. The reference verifies the actual sidecar bytes equal canonical nativeInput and only then supplies the old audit's truthful `inputFileSha256` field. The producer never substitutes a hash for derivative-consumption evidence.

Step records contain the accepted base, ordered stage IDs, raw endpoint and projected endpoint. Controller records contain input states, stable neighbor IDs, requested velocity, target values, command words, desired quaternion and saturation flags. Safety and arm summaries are separate records. Manufactured runs contain the same stage/step schemas nested under their run ID and an explicitly prescribed force law; they cannot be mistaken for native output.

## Fixed controls and interpretation

The wiring controls are null-load equivalence; a tilted unequal-force/moment case; nominal yaw retention; nominal motor-lag retention; reversed output IDs; duplicate IDs; missing IDs; stale stage token; stale raw result state; nonfinite force; zero quaternion; and nonfinite quaternion. Exact fixture constants and expected rejection reasons are in science-config.json. The tilted fixture has a 90-degree y-axis attitude, delivered world force [0.15,0,0], world arm moment [0,-0.00028,0.0014], unequal nominal/delivered motors and nonzero angular velocity. It gives a nonzero witness for the independent checker's missing-moment and wrong-frame mutations. Native algebra, finite controls and independent saved-evidence tamper tests are separate checks.

The manufactured cases prescribe world force [0,0,m*g] and zero world arm moment. Equal nominal motors imply zero reaction yaw. The rotor and collective entries are nominal actuator observables, not a claim that native physics yields that manufactured world force. Exact solutions are constant-velocity translation; constant principal-axis z rotation; and equal motor relaxation toward a constant command. The checker must independently bound analytic endpoints rather than trusting producer `exactFinal`, errors, pass flags or summaries.

Position, velocity and angular-velocity errors are Euclidean; attitude uses twice the sign-invariant quaternion chord; motor error is the maximum absolute rotor error divided by mg/4. The finest-grid limits are respectively 2e-12, 2e-12, 2e-12, 2e-10 and 1e-8. The fixed 1e-12 roundoff floor exceeds 4,000 binary64 epsilons at unit scale. Each refinement must contract by at least one half or fall below the floor, and the finest error must meet its component limit. Coarse-grid errors may exceed the finest-grid tolerance. All errors are retained. This is an analytic endpoint and refinement check, with no observed convergence-order claim.

Qualification still requires the independent checker to establish all 32 primary reference bounds and non-refusals, exact consumption/RK chains for both arms, stable associations and expected counts, finite controls, adversarial sensitivity, and the initial nonzero influence propagating into evolved states and the second control update. The controller logic is inherited rather than a new Boids algorithm. Passing this short exposed-state continuation would not establish robustness, continuous-time trajectory accuracy, mission success, measured aerodynamic accuracy or 5,000-drone scaling.

The checker also reconstructs neighbor membership from saved controller positions: each coordinate subtraction is rounded to binary64, matching the arguments passed to Grid's `Math.hypot`, and their squared sum is then evaluated exactly. Self is excluded and stable IDs remain ascending. A distinct pair within 2^-40 times the squared neighbor radius of the squared-distance boundary fails qualification; the producer's steering code is unchanged. Exact stored words bind inputs, delivered loads and consumption. The rational arithmetic checker treats positive and negative zero as the same numerical value when reconstructing arithmetic; it does not establish every computed zero sign bit. The final protocol states this limitation and the fixed feedback-difference gates.

## Review state

These files have only been drafted and inspected as text. No syntax validation, imports, bundle execution or numerical evidence is reported. No source closure or freeze is performed here. The parent owns reconciliation of the protocol, independent checker, exact reference, resource supervisor and source manifest before any new approval request.
