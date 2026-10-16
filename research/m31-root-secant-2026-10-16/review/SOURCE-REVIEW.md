# M31 causal saved-root secant: independent static source challenge

Date: 2026-10-16. Repository-relative package: `research/m31-root-secant-2026-10-16`.

## Scope and disposition

Reviewed the candidate, supervisor, configuration, prospective protocol, independent reviewer, and `review/INDEPENDENT-METHOD.md`. The integrated `source/review.py` was hash-checked and matches the reviewed submission exactly.

**No unresolved substantive static findings remain in the revisions identified below.** The causal interface/trace, current-state wrench and error formulas, invalid-domain handling, primary/secondary coverage, strict scientific gates, independent reconstruction, and operational closure controls are consistent with the prospective design. The corrections recorded below were made before any candidate scoring.

This is a source disposition, not execution evidence, a numerical result, or a claim that the one-shot invocations will complete. No candidate, reviewer, controls, scoring, simulation, historical solver, or extracted function was executed or imported for this review. No new scientific data or external source was retrieved. Existing scientific allocations remain closed. The final manifest, privacy/source publication, independent remote verification, and later execution/review closures remain separate prerequisites and evidence.

## Findings resolved before freeze

1. **Missing RSS samples could previously pass.** The original supervisor success predicate allowed a child that exited before the first successful RSS observation to qualify. The revised `source/run.py:133` requires `rssSamples > 0`, while positive sample recording, cap checks, and exit-race recording remain at lines 81–93. A fast child with no observation is therefore incomplete instead of silently successful.
2. **Some consumed-invocation failures bypassed closure assembly.** Configuration parsing now precedes lock consumption (`source/run.py:21–25`). Cleanup captures non-race kill failures at lines 99–117. Final pin verification, file accounting, and artifact hashing are guarded at lines 121–130, retain a `finalizationError`, and force failure. A failure to physically write a closure cannot be guaranteed away by source code; the exclusive lock and partial files remain evidence, and there is no authorized retry.
3. **Finalization time and manifest immutability were omitted from final checks.** The revised supervisor hashes the manifest itself as well as its listed inputs at line 122, records elapsed time after hashing, and rechecks elapsed time after the first serialization at lines 137–141. This closes the identified pre-hashing timing gap. Runtime remains sampled operational evidence rather than an OS-enforced instantaneous guarantee.
4. **Candidate admission initially hashed provenance without asserting its semantic success.** `source/candidate.py:159–167` now checks successful/complete prior review with no failures, prior supervisor success/return code, input/review/closure membership in the old result manifest, and publication-manifest evidence after exact dependency hash checks. Lines 178–179 additionally check completed trajectory identity and duration. The reviewer checks the longer ancestry chain independently.
5. **The two phases needed an explicit review storage allocation.** Candidate results now have a 6 MiB ceiling including their closure; both phases together retain the 10 MiB ceiling, leaving at least 4 MiB for review. Each phase reserves 128 KiB for its closure, aggregate logs remain capped at 1 MiB, and the new package remains capped at 16 MiB. The reviewer freezes the extra candidate limit and checks candidate closure accounting against it. Cap failures retain partial evidence; no truncation converts a miss to a pass.
6. **Strict qualification initially depended on tolerance-accepted candidate scalars.** The reviewer correctly reconstructed errors but initially used candidate scalars for both exact saved extrema and scientific gates. The final revision separates those roles: `checked_errors` returns independently reconstructed event maxima (lines 231–251); `strict_independent_summary` computes strict primary qualification from those maxima (lines 438–454); lines 519–523 compare all six gate booleans and final qualification with the candidate. Both the independent event maxima and strict primary summary are retained. Thus a near-threshold discrepancy within the numerical comparison tolerance cannot silently flip a strict gate. Exact saved extrema/first-tie reductions continue to use the independently validated retained scalar values, avoiding an unnecessary requirement that two floating-point implementations select the same tied location.

## Candidate analysis

- `predict` accepts only one/two preceding fresh `(index, time, roots)` tuples and target time. Cold start copies the last fresh roots; later predictions use the actual-time secant factor. The driver writes and flushes the prediction with predecessor IDs before admitting the current oracle, then advances history with the saved fresh root even when the candidate root is invalid. Loading the immutable input into memory is explicitly allowed; this is causal computation, not hidden-data evaluation.
- Effective rotor load is current nominal motor thrust times the selected ratio. Aerodynamic correction is effective minus current nominal thrust. Quaternion rotation of the axial collective correction and the motor-corner roll/pitch sums match the prescribed wrench, including zero aerodynamic yaw. Error denominators are `mg/4`, `mg`, and `mg*sqrt(2)*arm` for rotor, force, and moment respectively.
- Event admission verifies ordered IDs/times/roles, predecessor cache index, finite state/command/root shapes, positive motors, unit quaternions, command range, fresh admitted/descending metadata, residual/mismatch limits, direct witness/cache equality, and fresh root/load/correction correspondence. Held loads are reconstructed from preceding fresh roots at the current state and compared with stored LEFT data. No geometry or historical solver is rerun.
- Finite ratios outside `0 < x <= 1` retain load/error diagnostics and per-rotor invalidity records. Nonfinite roots serialize as null plus a named reason. Uncomputable predicted errors are unscored; the fixed remaining schedule continues. No clipping, oracle fallback, correction, selective reset, or fit is present.
- Primary coverage is all 200 positive targets, including cold start and terminal audit. It requires every target scored, zero invalid roots, all three absolute thresholds, and no worse complete-set maximum than hold. Missing predicted errors make complete-set maxima null while finite diagnostic maxima remain separately labeled. The 199-target secondary set has no qualification and cannot rescue a primary failure. Complete paired event maxima and better/equal/worse counts remain visible.
- The five fixed candidate fixtures are generated in the sole candidate invocation: startup, constant, irregular-time linear, finite overshoot, and nonfinite/invalid serialization. Their generation does not add a separate invocation or physical case. The candidate uses standard-library support and creates no descendant processes.

## Independent reviewer analysis

The reviewer imports neither the candidate nor any historical scientific solver. Its NumPy implementation independently constructs the secant from prior saved roots/times, rotates forces via quaternion cross products, forms body moments from the motor-coordinate matrix, and reconstructs every rotor/force/moment error. It verifies the full prediction trace and full retained event records, initial/final source identities, all 201 event roles, current/fresh/LEFT/RIGHT cache identities, fresh admission metadata, and corresponding corrections. It checks old and new exact pins, source ancestry, prior review/closure success, publication-manifest evidence, candidate supervisor closure, required artifacts, and candidate byte accounting.

The five candidate fixtures are checked against independently written expectations. Additional internal reviewer algebra checks exercise its own startup/constant/nonuniform-time, invalid-domain/nonfinite serialization, identity-force, and single-rotor moment-sign calculations inside the sole reviewer invocation. They are algebra checks, not new physical trials. Independent primary qualification now uses independently reconstructed error maxima, with strict threshold and hold comparisons and no comparison-tolerance relaxation. Any disagreement records an audit failure even if the candidate reports a scientific pass.

Reviewer output distinguishes audit integrity from scientific qualification. The saved-only reviewer has the same 200-target primary/199-target secondary scope, preserves invalid locations, and records limits of inherited geometry and exposed-data interpretation. Runtime dependency availability, actual assertion success, and actual resource completion remain untested here by design.

## Operational and scientific boundaries

The supervisor uses one exclusive lock per phase, a single child in a new process group, sampled RSS/time/storage monitoring, child termination/reaping, source/output immutability checks, and closure accounting. A scientific miss can still be an intact experiment; monitor, source, audit, or resource failure cannot become scientific evidence. Sampled limits do not establish instantaneous peak memory/storage or algorithm speedup. Failure evidence is retained and allocations are not repaired or rerun.

This is an exposed-data saved-endpoint diagnostic of extrapolating the coupled rotor-root variable. It does not establish a newly integrated secant trajectory, hidden-test generalization, between-refresh validity, feedback-predictor stability, adaptive-trigger utility, fewer actual solves, wall-time speedup, a physical guarantee, or novelty. The old hold result and closed allocations are unchanged. Any later visualization must use the original saved poses and label the added evidence as same-state errors.

## Final reviewed identities

| File | SHA-256 |
| --- | --- |
| `source/candidate.py` | `fff0d48c94c31166ec9b0835ed50c25140a37aeaf1f69a2b7333e1a4e9754670` |
| `source/run.py` | `e2fe36428f2c76508ab33726db7f02ef2945919586f6e7c80a05d78a5e917ab7` |
| `config.json` | `0dd1fbc9ccda854b7c0bbf35a2b4e0fcffb72538f2a192d3c6549d25c468e1b8` |
| `PROTOCOL.md` | `7a44018dd9b7f139013f3d901ec0fbf6664adf4a30ebabd95ae437fddbc98cb9` |
| `source/review.py` | `d86d9e86148417ecadd415a885c63592d62a7412df672dc9d1d50a9eb9492192` |
| `review/INDEPENDENT-METHOD.md` | `b40b61758d022dadf2db945c85f5a09c8eea66ef6a81e06e22b12314d7f32b9c` |

Earlier reviewed checkpoints are retained here to identify the revisions in which the resolved findings were raised. The candidate hash was already the final value above after its provenance additions; the supervisor and resource limits changed subsequently. The reviewer checkpoint below already included the candidate cap but preceded the strict independent qualification correction.

| Earlier reviewed file | SHA-256 |
| --- | --- |
| `source/run.py`, before supervisor corrections | `22af9d8c779d94be1e906a4b0eb860d5aa31695970855e131c9b8eed9efea189` |
| `config.json`, before explicit candidate cap | `06a5335e747359f69af629c17843f1ef5b63bab09bc48e398618ef1b94ae6b8e` |
| `PROTOCOL.md`, before explicit candidate cap | `7bebee79c761e4201bfd092de473c72ff7f265c2990ac0aacc1f38cadfd2bef5` |
| Reviewer submission, before strict independent gates | `a75fdace76f46a53682b57b4822d0c269ecd3d2820a76069e7494a6872d08c4e` |

Line references above refer to these revisions. This review should be pinned in the prospective source package. A change to the reviewed scientific, admission, gate, or supervisor logic requires a scoped static follow-up before freezing; it does not authorize a new scientific run.
