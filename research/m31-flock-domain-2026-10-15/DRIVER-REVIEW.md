# M31 saved-flock domain audit — final static review

Review date: 2026-10-15. Reviewer: independent protocol/source challenger.

**Disposition: no remaining static blocker identified in the reviewed revision.** This clears the source and protocol for the parent's prospective freeze and single bounded invocation. It is not an audit result, a guarantee of completion within the caps, or evidence of physical validity.

## Scope and reviewed revision

Read `PROTOCOL.md`, `config.json`, `source/experiment.cjs`, `source/independent.cjs`, and `source/run-step.py` under `research/m31-flock-domain-2026-10-15/`. Rechecked the final integrated driver against the independent module's actual exported API. This review performed no pose decoding, geometry evaluation, aerodynamic field calculation, integration, solver run, or experiment invocation. No repository files were edited; this report is the only new file from the final review.

SHA-256 fingerprints of the reviewed files:

| File | SHA-256 |
| --- | --- |
| `PROTOCOL.md` | `910b7a2815afd162a9b5ea0792cb07d4d35e82ca6eb2e4aec53b6a257f045dc7` |
| `config.json` | `d700be30a35ffdfc2329688b1b9b9a0c40680a4e3d73c50e303ace23c437a97c` |
| `source/experiment.cjs` | `e16a53f71e8e527112902f2c1b59e22e36bd1039d5dc0119d105d8115403730c` |
| `source/independent.cjs` | `b75ae9c2bef28b7f245ad2d244bb287afb51c46dbbc81581cec380435c78711f` |
| `source/run-step.py` | `dd873e7834148d545f92ba687401726dfdcbb1c55472c8ae25ad3c30a9b65e8a` |

## Input and classification fidelity

The fixed input is the primary compact export at commit `07e5165fa56f2f23bab24562b278dda1c82ed05e`, with historical base `c591ce2b195fa01b895d4ba881a44a4b92fdd703`. Both metadata and binary hashes, plus the 3,360,000-byte binary size, are pinned independently in config and checked before decoding. The metadata hash is `f69cae28818dd0802863b512af96a448ffcd3aa7aa8824f528b4ed59032d613c`; the binary hash is `c9918697fc61576a9c0454cda354a8d66f42b0b6e21e082cdbf12054b372c927`.

The driver uses exact times 0/20/30/60 seconds, case indices 0/1/2, and `offsets[0]`. Offsets are Float64 values, multiplied by eight; the binary has no header or embedded timestamps. The primary value offsets are respectively `[0,14000,28000,42000]`, `[70000,84000,98000,112000]`, and `[140000,210000,280000,350000]`. This selects twelve snapshots and 28,000 poses from wide1000/seed2001, narrow1000/seed2002, and wide5000/seed2001. All saved vehicles are sources and receivers; active/arrived status is not inferred.

The production-style checker retains the M26 grid, original quaternion rotation and rotor ordering, M28 constants, and M28 geometry branch order. The independent module imports nothing, uses explicit quaternion-matrix rotation, and enumerates every nonself source directly. Its `axes`, `worldrotors`, `centerChecks`, `eligible`, and `nearEvents` outputs are integrated correctly. The independent nonnegative clamp before the axis-projection classification is equivalent to the driver's raw-dot `<=0` test for finite inputs.

Exact indexed code-vector equality, count equality, eligible counts, ordered code-3/code-4 event identities, and near-event coordinates are checked. Axes and world rotor coordinates are compared to the frozen `1e-12` absolute tolerance. The two tilt predicates are compared exactly in addition to numeric axis comparison. Tilt is defined by body-axis z versus cos(20 degrees), not by maximum Euler angle. Quaternions are not normalized; unit-norm defects are separately reported with the frozen `1e-10` tolerance. Pair census after a tilt failure is explicitly hypothetical geometry, not a computed load.

Accounting asserts code-vector length `4*N`, independent center checks `N-1` per receiver, twelve completed snapshots, and 107,972,000 total nonself center checks. Code zero correctly includes self and excluded source centers, with snapshot summaries separating `4*N` self rotor entries from outside-center entries.

## Evidence, failures, and bounds

Issues raised during review were resolved before freeze: independently pinned input hashes; current snapshot/offset context before decoding; structured count/event/source-pose/tilt mismatch context; exact tilt-decision comparison; full enumeration assertions; explicit self/outside-center accounting; and compact evidence storage. The unused retained receiver-row array was removed.

Each completed receiver row stores both code hashes and the complete indexed primary vector using zlib deflate/base64. A saved-data reviewer can inflate it and recover every source/receiving-rotor code, including every code-3 and code-4 identity, without geometry recomputation. Full geometry is retained for code-3 exceptions. Code-4 geometry is omitted from storage, but all code-3/code-4 downstream and radial values are compared between implementations before row writing. Per-receiver norm errors, tilt flags, counts, and boundary information are retained. Boundary proximity is expressly limited to inspected predicates and native units; it is not a robustness certificate.

Caught failures retain current context, last completed receiver, counters, and partial summaries within the reserved evidence budget. The protocol correctly limits hard-termination guarantees to already-written evidence. The supervisor provides an exclusive execution lock, duplicate/terminal guards, process-group termination and reaping, interruption handling, and post-exit cap checks.

Final prospective limits are 300 executable seconds, 110,000,000 independent center checks, 864,000,000 combined eligible rotor classifications, and 64 MiB raw evidence with 1 MiB failure reserve. The exact planned center count is 107,972,000; the worst combined rotor count is 863,776,000. The driver's cooperative wall guard begins at 298 seconds; the external supervisor initiates termination approximately 1.1 seconds before its deadline. These are stopping mechanisms, not promises of complete output. No 256 MiB memory acceptance limit is claimed or enforced. The final protocol intentionally supersedes the earlier design memo's proposed time/memory caps.

The source contains no aerodynamic field call, wake-amplitude computation, receiver force law, dynamics, controller, or integration invocation. Geometry-only scope is coherent. Freeze/push, execution, saved-evidence arithmetic review, viewer work, privacy review, and manifest verification remain parent responsibilities under the protocol. A completed domain failure is an admissible finding; it cannot be relabeled physical validation, continuous-flight coverage, cadence qualification, or an acceptable trajectory reference.
