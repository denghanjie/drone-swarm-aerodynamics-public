# Historical swarm transfer: independent static review

Date: 2026-10-16. Package: `research/m31-swarm-coupling-transfer-2026-10-16`.

## Scope and conclusion

This is a source/protocol review before the allocated target invocation. No candidate, reference function, extractor, numerical checker, geometry calculation, load solve, or target-state decoding was executed by this reviewer. Source text, public input sidecar, historical physics source, prospective documentation and runner text were inspected. Source-file hashes below identify the reviewed revisions; input-byte hashes were read from the sidecar rather than independently recalculated here. The independent numerical checker is a separate agent's deliverable and is not approved by this note.

The inspected candidate implements the declared historical rotor identities, complete directed pair census, canonical sparse ordering, full-snapshot rejection and conditional ordered/Picard solves. Four concrete failure-retention/guard findings were reported and corrected before freeze. No remaining blocking candidate-source discrepancy was found in the inspected revision. This conclusion is conditional on the final manifest including the complete source/input set and on the declared remote verification occurring before invocation. It is not an admission, numerical correctness, runtime, physical-validity or publication-verification result.

## Input lineage and geometry

The extractor fixes the four prescribed records in the declared order: N=1,000 at 20 s, then N=5,000 at 20, 60 and 180 s. It verifies each original JSON length and SHA-256, exact time, vehicle count, 17 finite numeric values per vehicle, and binary64 roundtrip equality. It writes complete rows without selection, normalization, motor clipping or rescaling. Exclusive creation prevents silent replacement. Relative historical source paths, original and derivative hashes, component schema and rotor offsets are retained in the index. The published original pins agree with the prior static admission note. The original JSON files themselves were not rehashed in this review.

The candidate uses positions 0:3, saved xyzw quaternion 6:10, and four nominal motor-lag thrusts 13:17. Its double-cross rotation and corners `(a,a),(-a,a),(-a,-a),(a,-a)` preserve historical yaw and motor identity. These match the historical `physics.cjs` rotation, wrench ordering and state declaration. Axes and offsets come from that quaternion without normalization. Finite-state, quaternion/axis/frame checks, positive nominal checks and tilt census use the prospective tolerances. A failed nominal contract leaves geometry census intact; nominal-dependent cap/diagnostic values become null as declared.

The copied `reference-excerpt.cjs` was compared byte-for-byte with the prior published small-case package's excerpt; it matches. The candidate's constants and center tests match that excerpt. Each directed nonself center is visited once; outside-neighbor/self entries remain symbol 1, center-guard failures become four symbol 11 entries, and every eligible center gets all four rotor calls. Full symbols use `[receiver,source,rotor]`; no rejection is used as a solver zero. Only positive terms enter receiver-rotor CSR, with ascending source IDs. Unique vehicle dependency sets recover the graph without repeated rotor edges.

Actual deterministic height-descending/id-ascending rank controls eligibility. The code separately reports equal-or-reversed-height edges. Thus a valid tie order does not become a claim of strict geometric descent. Depth is computed only for an eligible order, with roots at depth zero.

## Admission, solve semantics and accounting

The solve gate requires both entire-snapshot admission and actual sorted-order eligibility. Every symbol 4 or 11 rejects the entire snapshot, as do invalid geometry/nominal values and scaled-cap violations. A rejected case retains census/artifacts and `solutions:null`; it receives no partial-subset solve or replacement case.

The coefficient and map formulas follow the frozen four-root contract. The direct pass updates nodes in dependency order. Picard is synchronous from all ones, retains every iterate, stops after the first log-change at most 1e-11, and caps updates at 64. Every nonzero-alpha root performs 56 loop iterations; alpha zero returns exactly one. The code counts loop iterations without claiming guaranteed interval halvings.

Each direct/Picard result has separate final-map work and residual values. For Picard, saved `rotors` belongs to the final update that produced returned `y`; `residualMap.rotors` belongs to evaluating the map at returned `y`. The checker must preserve this distinction. Positive-term multiplications, root closures and bisection iterations are counted in the appropriate solve/residual work objects. Geometry center tests, eligible centers, rotor calls and retained positive terms are separate.

`complete:true` means every selected census record finished; it does not alone imply Picard convergence or independent numerical acceptance. The numerical checker and final report must enforce the conditional convergence/force/work criteria separately. Positive finite input nominal forces alone do not guarantee that a fixed 56-iteration root closure has adequate relative accuracy for every imaginable magnitude; the frozen-input independent tolerance check remains necessary. No claim about the actual input magnitudes is made here.

## Findings and corrections inspected before freeze

| Initial finding | Correction inspected | Status |
|---|---|---|
| Output-budget exhaustion could prevent the catch block from writing its own failure/partial record. | Normal candidate writes stop at 255 MiB. A 1 MiB reserve supports compact failure JSON and an index of already-written case records, with an absolute candidate cap of 256 MiB. | Resolved for controlled candidate output exhaustion. |
| Arbitrary exception messages could contain absolute filesystem paths. | Catch retains only a small controlled phrase set or a generic execution-exception phrase, plus exception class. | Resolved in candidate JSON. Raw child stderr still requires publication privacy review. |
| Failure progress retained only phase/receiver/update, despite promised work counters. | Geometry progress retains its live geometry-work object; direct/map progress retains live solve work; residual progress also records completed solve work. | Resolved for available caught-failure counters. |
| Direct pass and residual maps did not guard each receiver. | Direct and map loops check RSS/internal time for every receiver; Picard also guards at each update. | Resolved. |

The final schema explicitly states that an external hard timeout can precede candidate catch. In that event the exclusive lock, already-written artifacts and supervisor timeout record remain evidence; it must not be described as a complete current-snapshot census. A process crash or underlying disk failure cannot be made into a guaranteed complete evidence record by the candidate catch. This is a retention limit, not an observed target failure.

## Runner and publication requirements

Both runners require an expected manifest hash and source commit. They verify the current commit, exact committed manifest, each manifest file's bytes/hash and its committed bytes before consuming an exclusive invocation lock. They refuse optimized Python so their provenance assertions remain active. They invoke a single child, enforce 180/240-second timeouts, retain existing output, record safe supervisor exception class or timeout, inventory artifacts, and exit nonzero for a nonzero/absent child return code. They do not silently retry.

Remaining publication follow-through:

1. The final source manifest must include candidate, copied reference, extractor, both runners, independent checker, protocol/schema and all four extracted inputs plus their index. The manifest was not yet finalized during this review. Verify its actual remote commit/hash before starting either allocation.
2. Raw child stderr can contain runtime tracebacks/host paths for uncaught failures. Privacy-review all result/log files before publication, preserving public-safe failure facts and raw-file provenance rather than copying private paths.
3. The reviewed final protocol clarifies that the 256 MiB cap applies to candidate scientific artifacts and compact failure records. Supervisor logs, locks and provenance bookkeeping are separate and must be inspected before publication; an unexpected large log remains a failure requiring review, not permission to rerun. Report this scope accurately, including the separate review output, rather than treating 256 MiB as an already-measured total filesystem footprint.
4. No tool-level success, exit zero, census completion or lack of admitted states replaces independent exact-symbol/CSR/work checks. Numerical boundary disagreements remain disagreements under the frozen contract.

## Reviewed source identities

Hashes below are static source-file fingerprints, not target execution results.

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 11111 | `c5c2b18449650116d15effd8f070b663f9af2715a833cf73d91bc43f5cf87822` |
| `SCHEMA.md` | 6422 | `8d4833b9bfbd7eb44596b7104b2c9343f34a1fecc1fa0c53ea9c2bcfc527a0e2` |
| `source/experiment.cjs` | 11411 | `b31889c7450cc9f43cc185717d369a8968f59c745f70d9e973c23959cded1bb7` |
| `source/extract-inputs.py` | 2512 | `19e49fc8333940db76c2457e12e5875cf9ca0c86a8513540b7e47bba1967575a` |
| `source/reference-excerpt.cjs` | 2731 | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| `source/run.py` | 2283 | `ad3a5ac99cbb37508333d5d79dce795d670f1ba7ecb89ba46cd6f5aaf33ae8a7` |
| `source/run-review.py` | 2395 | `8db5eeb2a1f4b8b3f6fee8403fd3026b6a07727c4e95a4f18369993b08069940` |

Subsequent source changes require explicit review of their diff; this review does not automatically apply to later bytes.

## Pre-freeze addendum: quaternion addition grouping

The checker author identified one floating-point evaluation-order correction after the preceding review. In `rotate`, the old expression `x+q[3]*t[k]+u[k]` evaluates as `(x+q[3]*t[k])+u[k]`; it has now become `x+(q[3]*t[k]+u[k])`. This matches the historical `add(v,add(scale(t,q[3]),cross(q,t)))` grouping exactly. The mathematical rotation and rotor identity are unchanged, but the parentheses matter to floating-point reproduction near strict support boundaries. The initial review's rotation agreement statement should be read with this correction.

The revised candidate is 11,413 bytes, SHA-256 `ba7ae6e9dad0b348243719813cc2ecc47f9d904f571a036ed752389eab3140b5`. Reversing only this two-parenthesis insertion reproduces the previously reviewed SHA-256 `b31889c7450cc9f43cc185717d369a8968f59c745f70d9e973c23959cded1bb7`, establishing that this is the complete intervening candidate diff. It was compared statically with the original historical rotation source. No candidate/target code or geometry was executed. The static review applies to the revised candidate hash, subject to the same remaining manifest/publication/numerical-check requirements.
