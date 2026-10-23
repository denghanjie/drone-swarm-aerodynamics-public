# Prospective protocol and source review

2026-10-23 — `m31-phase-attribution-2026-10-23`

**PASS for source/design review; no remaining blocking issue.** The reviewed bytes are cleared for exact source freeze and the separate independent public source-identity gate. This does not establish that public verification, numerical allocations or any result has passed.

## Scope and completed checks

Review covered the protocol/schema/configuration, producer, independent auditor/design, shared gate and supervision code, finalizer, viewer/UI QA, and original wrapper/kernel timer placements. Work was limited to source reads, opaque byte hashing, Python AST parsing and JavaScript syntax checks. No scientific module was imported or executed, archive decoded, raw query log aggregated, phase total/ranking calculated, model run or UI launched. No network acquisition for this checkpoint occurred during review.

- Six Python source files passed AST parsing without imports. `source/ui.cjs` and `viewer/app.js` passed bundled Node syntax-only checks. An earlier generic `node` lookup failed because Node was absent from PATH; bundled checks then passed. This is a preparation environment detail, not an allocation failure.
- The auditor's AST-extracted literal `EXPECTED_CONFIG` exactly matches configuration.
- All 29 input pins, 95,752,652 bytes, matched independent local opaque byte hashes. This establishes local identity, not public retrieval or fresh scientific validation.
- Bundled Node matched its runtime pin: 121,304,480 bytes; SHA-256 `d0c6c74401e6a544bb4d4b2a9ded9c43298d4e6dcd5ebac4dd010c4c81774105`.
- All 23 reviewed identities below were rehashed before writing this review and still matched the inspection snapshot. Renderer dependencies are byte-bound; a complete semantic audit of third-party Three.js is not claimed.

## Accepted design and limitations

The population is fixed at 34,560 saved rows: twelve windows × 160 stages × two methods × nine repetitions (-1, 0–7), with original group/call order enforced. The expected 34,542 successes and 18 refusals derive from the fixed schema, not a new raw-log count. The sole known refusal is window 2/index 159, native-admission/near-field, native stage `build`, time word `400cf5c28f5c28f6`. Unexpected patterns fail.

The primary denominator is measured successful F outer time. Pooled and all eight repetition denominators must be positive. Exact descending leaf totals determine the leader, with alphabetical ties and exclusion of only timerResidual. Stable-majority requires at least one half of pooled outer time and the same winner in at least six of eight repetitions. Both conditions, all winners and exact numerator/denominator strings are retained. This is descriptive inspection priority only; earlier cost/coverage/keep failures remain unchanged. Prior exposure to individual timings is disclosed, with no blind or held-out claim.

Wrapper phases partition inner time; kernel phases are nested inside broad build. Replacing broad build with kernel phases plus signed buildUnassigned, then adding signed outerBoundary and timerResidual, must conserve outer time exactly. Absolute residual is bounded by 0.000001 ms; buildUnassigned/boundary cannot be below its negative. Values are never clamped. The refused finalization interval includes unclosed build plus catch/output work and is renamed unfinishedPhaseAndFinalization; absent kernel timing is unavailable, not zero.

Labels now reflect source boundaries: kernelIndex is screening/certificate work; kernelAdmission includes graph/reason checks, coefficient scaling and ordinaryLmax. Geometry includes candidate rowsFor cache/list work, center/rotor interactions and assembly, so it cannot isolate cache or norm savings. BuildUnassigned includes wrapper preparation/evidence/validation and kernel post-t4 work. OuterBoundary includes owned copy, calls/returns and timing-object construction, not pure copying. F reset is matched branch/timer overhead; C includes actual reset. comparisonMs is nested in partial encodePersistMs and neither is added to query time. F baseline comparison and C witness copying are asymmetric outside-timer evidence work that may influence later GC/cache state.

The producer uses Decimal precision 80 with Inexact trapping. The auditor independently parses decimal tokens into Fraction, constructs canonical decimal/JSON bytes, and reconstructs every transformed row, aggregate array, 216 group reconciliations, decision and 1,920 paired repetition-zero viewer rows. It rejects duplicate keys and invalid timing types, imports no producer/scientific code, binds producer output bytes and rechecks identities before passing. Shared common.py is limited to gates, reads, paths/configuration, output and supervision; independence is arithmetic/reconstruction, not complete infrastructure independence. Exact arithmetic preserves serialized rounded binary64 evidence without creating measurement precision.

Old scientific validation is consumed through the pinned prior audit and its 1,920 bindings, not recomputed from scientific CAS. Fixed prior manifest/publication identities and closure checks preserve the old composite transport history and failed qualification gates. Runtime success of these prospective checks remains pending.

The finalizer binds audited summary and independent viewer bytes plus inherited motion. New timing displays use audited evidence; old geometry counts are context. Exact signed-decimal BigInt ranking with alphabetical ties governs viewer/UI ordering; Number is display-only. UI source checks 1,920 saved position/status records, 1,920 paired annotations, headline/previousResult/partitions, controls, orbit/reset, desktop/mobile and altered-evidence rejection. These are prospective assertions, not completed UI results. Motion is explicitly earlier recorded trial stages. Screenshots are retained as previously instructed; installed Playwright is reused. Node is pinned; Python/browser/package dependencies are disclosed as unpinned.

## Execution boundary

Exclusive single-use locks and supervisors impose producer 300 seconds/128 MiB, audit 450 seconds/128 MiB, finalize 120 seconds/2 MiB including viewer pins, and UI 180 seconds/16 MiB. MiB bounds cap evidence output, not process memory. Each allocation runs once in that order only after exact source freeze, public push, independent public source/input verification and its recorded receipt. Failure is retained and stops the sequence; no post-freeze source repair or rerun is authorized. Identity/publication reads are administrative, not permission for numerical execution.

No causal acceleration, significance, uninstrumented throughput, physical accuracy, safety, novelty or scaling claim follows. Historical browser timings do not transfer to this Node/N64 population. Overall research remains unfinished; the stale paused goal must not be recreated/completed. Further optimization requires a new question and separately reviewed bounded protocol.

## Reviewed identities

Input descriptors are fully recorded in the hashed input-pins.json. This review does not include its own identity; the source manifest must pin its final bytes separately.

| Reviewed path | Bytes | SHA-256 |
| --- | ---: | --- |
| `research/m31-phase-attribution-2026-10-23/CLAIMS.md` | 932 | `a9b18363b80efd8d9079c0385d54778de05b996d319f08cc84a16f7fb8bdc315` |
| `research/m31-phase-attribution-2026-10-23/LITERATURE.md` | 1313 | `d20754ce2756d6a95f89d6a0010e32448bd14520c38e2735d4cbedbfdd37305a` |
| `research/m31-phase-attribution-2026-10-23/PRIVACY.md` | 584 | `998d417b3e6cfe7f3e36cbfc9dbc2c7c363e2f54ed2407d9faaa239578573848` |
| `research/m31-phase-attribution-2026-10-23/PROTOCOL.md` | 7633 | `122dce362b1b80ccd57bd974219add82e3a1dd08b25c76e6b92ed5240f4ef763` |
| `research/m31-phase-attribution-2026-10-23/RESTART.md` | 1120 | `597df1c386507b64766b69366b663add48e34c38984a708813d3a862963c82a6` |
| `research/m31-phase-attribution-2026-10-23/SCHEMA.md` | 2530 | `e6cdb308ddb93966638a3b9ab4516f322c9b82daeea53cb3eb5dc8adefc77d26` |
| `research/m31-phase-attribution-2026-10-23/SOURCE-CHANGES.md` | 1386 | `b4c8d8e8f4f3f2ebda2cd6ccebd05dda924dcd912f2dc2e1782b882597b68012` |
| `research/m31-phase-attribution-2026-10-23/config.json` | 1327 | `583215257483814146cfdcfe4d66ec0b60f6b9b3630887ecea54632734da714f` |
| `research/m31-phase-attribution-2026-10-23/input-pins.json` | 8428 | `f937a6027edfccac7f7359f5654f561c54540136b7c32e4e6b115cdb808a9479` |
| `research/m31-phase-attribution-2026-10-23/review/AUDIT-DESIGN.md` | 12709 | `f10b1ea21958b689dd12685ee02083cf0af133d1e56342b2f02a8b79460970d4` |
| `research/m31-phase-attribution-2026-10-23/runtime.json` | 760 | `4d8d7e591084f681559a694a11a41f858d4b4392c32fc7a0839c54dba40705c4` |
| `research/m31-phase-attribution-2026-10-23/source/analyze.py` | 7977 | `13527d4dce9688d2a030fa0791b42bbaaa8458699d02548b2cf219b1958b481f` |
| `research/m31-phase-attribution-2026-10-23/source/audit.py` | 38330 | `ff4b7c1d852395c9c771c573f96b7cbc67b2d383f2ceb54c9f8bed23e16013f7` |
| `research/m31-phase-attribution-2026-10-23/source/common.py` | 4258 | `54da09f029d5c62f4a9fd042adc42f5372ccb9164c6a7ee1bf771ebf1af643ed` |
| `research/m31-phase-attribution-2026-10-23/source/finalize.py` | 1563 | `34bb732308060791d1946d066019fce56ae99e4e09b89233c0e9ec3a70057273` |
| `research/m31-phase-attribution-2026-10-23/source/launch.py` | 896 | `e7c432425102a92602648e419ed424a546b3d10c843d02f1405b90af5414c6a0` |
| `research/m31-phase-attribution-2026-10-23/source/supervise.py` | 3067 | `7f4584bdb2b11da905ecb8d5c270edbeb3b648eb5c9efd03a173f62bb34cf5de` |
| `research/m31-phase-attribution-2026-10-23/source/ui.cjs` | 12210 | `c80280ac0e37600d6fc4f0aef9f8b4404ba2fb152dc178926685bd564a08ed0f` |
| `research/m31-phase-attribution-2026-10-23/viewer/app.js` | 9694 | `85a6a87e1a5e57ba07ff172017885ba4c5c04386159687687477388a677d58ed` |
| `research/m31-phase-attribution-2026-10-23/viewer/index.html` | 4853 | `113606cc8698081dc9d3d01f75cf139f19e55ab9e1b3fbdd47c85717cdc91591` |
| `outputs/step02b-source/vendor/three.module.js` | 603113 | `c8211c69345d2e9949dc7a8ac969380497aa0600a5a8ac6a459c8cd02dd9cb8a` |
| `outputs/step02b-source/vendor/three.core.js` | 1403455 | `eb077d2417f61d3e6d9264c317cabc4ea35769ed6b0ab533067292a550784c20` |
| `outputs/step02b-source/vendor/OrbitControls.js` | 38703 | `b97879c748170baadeb3fb84cea1ffdf4674e283dc06042f34e2acb95a76042c` |

**Clearance:** proceed to exact source freeze and independent public source verification. All numerical allocations and result claims remain pending. Changed source identities require a new review; this clearance cannot override a failed later gate.
