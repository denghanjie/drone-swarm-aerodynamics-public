# Pre-execution source review

This review is of source and interfaces. It does not establish numerical success. The protocol, runtime pins and executable dependency closure must be frozen before the sole attempt.

The implementation, independent rational checker and process supervisor were prepared separately. The parent read their complete interfaces and the inherited physics/grid/native evidence contracts. A second reviewer checked dependency resolution, command/state binding, checker expression order and supervision failure paths. Agent agreement is not experimental evidence.

Resolved before execution:

- Reused the earlier whole-swarm projected-stage structure; the two bridge-design drafts remain unadopted.
- Replaced total force/moment exactly once, retaining nominal actuator dynamics and provisional nominal reaction yaw.
- Changed quaternion normalization from the old hypot expression to a specified rounded sum/square-root/division expression; preserved this as an explicit method change.
- Fixed a persistence path that could try to mutate an already-frozen record after append failure. Each stage now has one durable emission attempt outside the scientific catch.
- Distinguished inline semantic hashes from actual persisted input-file hashes. Every primary stage sidecar is written and synced before journal acknowledgment; the independent checker verifies its exact bytes.
- Reconciled the analytic suite to a 0.01-second interval: 9 runs, 84 steps, 336 stages.
- Corrected independent endpoint timestamp reconstruction to match the declared grouping, `5 + (t + h)`.
- Required saved-word evidence of a nonzero load change, subsequent state change and second-controller-command change, rather than merely a successful native return.
- Kept finite work, output and shutdown limits inside one 960-second allocation. Failed runs preserve partial evidence and cannot rerun in place.

Important limitations retained:

- Exact rational reconstructed arithmetic identifies both signed zeros numerically; no blanket bit-identical derivative claim.
- Independent neighbor membership uses rational squared distance on rounded coordinate differences and excludes cases within a fixed relative 2^-40 margin of the squared 1.8 m boundary. Such a boundary case is unresolved. This is an acceptance margin, not a proof of all libm implementations.
- Controller trigonometry and full Boids steering are source-bound, not independently regenerated. Elementary target arithmetic, neighborhood IDs and actual command consumption are checked.
- Dense native input capture remains the production boundary. The small adapter's generic array predicate is not a fully adversarial JavaScript-object validator.
- The reference uses previously verified exact routines; the new checker audits saved partition evidence but does not rerun every exact zero predicate.
- Process ownership and byte polling do not imply OS-level memory containment or guaranteed shutdown of every helper under host failure.
- Physical-model validation, general trajectory convergence, scaling and novelty remain unresolved.

Parent syntax checks use only Python AST parsing and Node `--check`, with no candidate imports. The source bundler reads and concatenates frozen bytes and records source offsets; it does not evaluate factories. The publication receipt will bind the final executable source manifest to its public commit before any scientific launch.
