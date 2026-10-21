# Independent saved-data audit contract

21 October 2026, Asia/Shanghai. This contract and `source/audit.py` are prospective source. They must be independently reviewed, frozen, publicly committed and verified before the new producer allocation. Source inspection and syntax parsing do not execute or qualify this audit.

## Allocation and independence

One audit allocation has a 1,200-second successful wall limit, a 1,220-second external termination boundary, and a 128 MiB output cap. The supervisor's measured success wall includes cleanup. An exclusive `audit-supervisor-launch.lock` and newly created `audit/` directory prevent a second attempt. Unexpected failure, timeout, malformed evidence or persistence failure closes the allocation. No numerical retry, changed tolerance or repaired rerun is authorized by this contract.

The auditor uses only Python's standard library. It does not import or execute the producer, JavaScript scientific modules, the initializer, controller, contact geometry, native airflow code, browser or any earlier audit. Binary64 word, rotation, projection, derivative, RK endpoint and safety-record helpers are copied or adapted from the independently written continuation Python auditor. This preserves independence from the JavaScript producer; it does not create a third independent implementation of those Python helpers. The nominal force/moment reconstruction and new segmented traversal, baseline join and comparisons are implemented here. The new journal reader independently parses saved JSONL and does not import the producer's Journal implementation.

The coupled baseline is reused evidence. Its published audit and export are trusted after exact provenance and closure checks. This audit does not rescan or recompute the coupled trajectory. The sole journal-prefix exception reads each original initial record to establish the exact shared starting states.

## Public source and successful producer gates

Before examining new trajectories the audit requires:

- A full source commit and a publication receipt with the exact source-manifest SHA-256, exact verified pin count, and true remote/local and committed/local equality flags. The offline auditor checks the existing verification receipt; it does not perform a fresh network fetch.
- Unique safe repository-relative source paths, regular files without symlink traversal, finite file-size bounds and exact SHA-256/length matches. All listed sources are verified before and after the audit. Mandatory coverage includes this contract, auditor, configuration, protocol, runtime identity, producer and supervisor.
- The exact four-case configuration: seeds 2026102001 and 2026102002, each at h=.005 and .0025, N=64, control interval .01, the 0..1 and local 0..4 segments with origins 0 and 1, maximum 6,000 completed steps and 24,000 stages, zero native calls, 1,200 seconds, 2 GiB producer outputs and 4 MiB raw records. No alternative case or parameter is accepted.
- Known unchanged SHA-256 identities for the inherited adapter, physics, simulation, grid, geometry, motion and lossless Journal sources. Literal relative CommonJS dependencies are followed as text and must be pinned. The native-load module must not occur in this static dependency closure. No JavaScript is imported by this inspection. The frozen producer performs the runtime-executable check and supplies throwing native-query/evidence stubs.
- A complete `m31-nominal-comparison-v1` index without failure; its source commit and exact config; zero recorded native calls; internally closed zero-exit producer receipt; externally closed zero-return producer supervisor with no timeout, passing wall/output caps and wall at most 1,200 seconds. Launch and index must name the same public source commit.

The result directory must contain only launch/index/exit files and the ordered journal parts listed by the audited index. There is one journal per reached segment, four to eight journals depending on safety stops. A stopped first segment has no second journal. All physical bytes must match supervisor accounting and the 2 GiB cap. `outputBytesBeforeIndex` equals the launch bytes plus all compressed part bytes. Stage, endpoint and safety totals are independently reconciled with the index.

## Prior evidence and exact initialization

The original result is pinned to public commit `637c25294f162bea39970d12df0206f25dead889`, manifest length 20,563 and SHA-256 `a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b` (100 pins). The continuation result is pinned to `a0f595f34a4f9ef8cef516caa0cde60053e0eade`, manifest length 33,149 and SHA-256 `90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81` (157 pins).

Both exact publication receipts, manifests, result indexes, audit reports, audited viewer exports, producer/audit exits, supervisors and allocation closures must be source-pinned and bound to the corresponding public result manifest. Prior evidence audits must have passed, with all attempted native stages admitted. The prior reports' index/export/producer-closure pins must match the selected bytes. All prior closure phases must be closed-passed with one attempt. The continuation's previously successful lossless-storage qualification and supervisor are also checked as published evidence; no new storage qualification runs.

The frozen descent `inputs.json` and original archive mapping identify exactly the first compressed part of each original case. These four first-part pins must equal their original public-manifest pins and the current source pins. Each whole first part is byte/hash verified before a gzip reader obtains its first bounded, newline-terminated JSONL record. The record must be sequence zero, kind initial and the correct case. Its uncompressed line hash, byte length and offset zero are retained. This is a verified prefix extraction, not a new complete baseline-journal audit.

Every new initial ID 0..63 and all 17 words per ID must exactly equal the corresponding saved original initial input. Both resolutions of one seed must share those exact words, and the two seeds must differ. The initializer is not rerun by the auditor. At every reached second segment, all 64×17 initial words must equal that nominal path's own final first-segment words. No additional normalization, reset to the coupled state or new initialization is allowed at the join.

## Byte handling and record order

The continuation Journal format has 16 MiB raw blocks and 32 MiB compressed parts. Descriptors must have canonical contiguous part names and offsets, bounded lengths, complete aggregate compressed/raw hashes and exact record counts. Nonfinal parts are exactly 32 MiB. The audit exposes no bytes of a part to gzip or JSON parsing before the full part's length/hash match succeeds. It then streams concatenated gzip members forward and checks the compressed aggregate and complete raw JSONL byte/hash totals.

Every JSONL record is at most 4 MiB and ends in a newline. Duplicate JSON keys, nonfinite/overflowing JSON numeric literals, missing records, unexpected order, extra records and noncontiguous sequence numbers fail. Each new completed frame retains step-record and safety-record uncompressed sequence/offset/length/SHA-256 provenance. Hashes include the newline.

Each verified-read operation permits at most three byte-read attempts on an OS error or length/hash mismatch, before any bytes from that operation are consumed. Each anomaly is logged with path, operation number, attempt and error or observed identity. Gate-before, evidence consumption and gate-after are separate verified-read operations. Parsing, arithmetic and entire phases are never retried. A newly captured small result without an established expected hash has one read; its captured identity is rechecked before success.

Each segment follows exactly: initial; controller whenever its local step is due; k1, k2, k3, k4; completed step; safety; the next step or case-end. Adapter IDs remain local to their own journal. All controller, stage and endpoint arms must be `off`. Controllers are due at local step zero of both segments and then every two or four integration steps. Their commands are held unchanged across all four stages and until the next scheduled update.

All new stages must be completed with null reason, zero native calls, null native evidence and no thrown/malformed/failure evidence. A native refusal is impossible in this nominal branch and fails the audit. Unexpected stage or endpoint failures cannot be reclassified as orderly safety stops.

After each completed endpoint exactly one safety record is required. The audit checks recorded issue kinds, IDs/order, recorded finite distances/clearances and the equivalence of `pass` with an empty issues array. It does not recompute obstacle or swept-contact tests, vehicle-limit decisions or a safety certificate. The first nonempty issues array ends that segment and entire path immediately, retaining its completed endpoint. Segment and whole-case `terminationIssues` must exactly reproduce those issues. Status/reason, counts, final full state and nominal last time must exactly match both case-end and index. No suffix or second segment may follow a safety stop. Horizon completion requires all prescribed steps with empty termination issues.

## Independent arithmetic

All saved state and scalar words are 16 lowercase hexadecimal digits interpreted as finite IEEE binary64, with canonical IDs 0..63. Basic arithmetic follows the frozen JavaScript operation order and is compared by exact words, retaining signed zero. This is binary64 consistency on the audit runtime, not an exact-rational or cross-runtime accuracy proof.

Each saved positive quaternion norm must be within one ULP of Python `math.sqrt` of the independently recomputed norm square. The saved norm is then used in all downstream comparisons. Counts of root comparisons and one-ULP differences are reported. Every nominal stage and completed endpoint has its saved norm evidence; a missing root is not reconstructed or silently accepted.

Checks cover all 64 vehicles, every reached integration stage and all completed endpoints:

- Controller state equals the current endpoint. Local step/control indices, relative and origin-adjusted clocks match the fixed schedule. Neighbor-ID shape/order, finite desired velocity/target/quaternion/commands, x/y target binding and saved target-z arithmetic are checked. Neighbor membership, steering, yaw trigonometry, actuator law and saturation decisions are not regenerated.
- Raw stages equal the saved base and preceding checked derivative: k1 base; k2 base+h/2·k1; k3 base+h/2·k2; k4 base+h·k3. Clock and dt words are checked in the original segmented operation order.
- Quaternion norm-square/projection and non-quaternion word preservation are checked. Per-row raw/projected words and held commands must equal their enclosing stage evidence.
- Nominal loads are reconstructed from the projected motor-state words, not the instantaneous commands. The body z axis is rotated with the saved quaternion. Collective is the left-to-right four-rotor sum; world force is axis times collective. Each of the four fixed rotor offsets is rotated, its cross product with the axis is multiplied by that rotor force, and world moment is accumulated in rotor order. All consumed rotor, collective, world-force and world-moment words must match.
- Body-arm moment rotation, nominal reaction yaw with the unchanged sign convention, total body moment and gyroscopic term are checked. All 17 derivative components are checked: position rates, nominal acceleration/gravity, quaternion rate, angular acceleration and motor lag. This verifies the implemented yaw/load convention without claiming physical validity.
- The RK weighted sum is exactly `base + h * (((k1 + 2*k2) + 2*k3) + k4) / 6`, followed by the saved endpoint quaternion projection. The resulting full state must become the next controller/step input or final case state.

A final endpoint has no newly computed aerodynamic force. The nominal paths have no coupled native-domain test, so a completed nominal path cannot establish that coupled airflow admits those states.

## Saved coupled join and comparison scope

The coupled replay consists of the four original audited frame lists followed by the continuation frame lists with exactly their duplicated initial boundary frames removed. The join verifies the old index/export outcomes and frame counts, canonical 64-position buffers, local step order, exact saved relative-time arithmetic, continuation `1 + relativeTime`, boundary positions and final positions against full index state. All 5,775 existing coupled frames are retained. The first seed's two saved stops and the second seed's two completed horizons are fixed provenance, not newly generated results.

Both arms export integer `globalStep` along with the actual saved timestamp. Matched off/coupled comparison uses the largest integer step available in both same-dt paths. It computes only that last common endpoint's maximum and RMS per-drone center separation, mean-height difference, ID17-height difference and each arm's mean displacement from its shared initial state. Differences are off minus coupled. It preserves each arm's saved time and safety flag. It never aligns by floating-point time equality, interpolates, extrapolates, pads a stopped path or treats later off-only motion as a matched comparison.

Per-arm initial-to-final summaries report mean dz and ID17 final z/vz. Coupled final vz is available in the pinned final index state. Coupled intermediate per-frame vz is absent from the old viewer export; the last-common comparison therefore sets coupled ID17 vz to null and computes no velocity difference. The baseline export/index retain stop reason and safety flag but not contact identities; those identities remain null with an explicit disclosure. New nominal termination identities are retained directly from their saved safety issues.

For each seed, nominal coarse step k is paired with nominal fine step 2k through their shared completed prefix, including the initial endpoint. The export reports maximum per-drone center discrepancy over those common samples, its identities and actual saved times, plus last-common positional descriptors. These are dependent resolution-sensitivity checks on the same initial configuration. They are not independent replicates, convergence-order estimates, physical accuracy estimates or a continuous-time maximum.

The off path develops its own later states, neighbors and controller outputs. This is a contrast between two implemented model paths, including feedback changes, not an isolated force contribution or a validation of the aerodynamic law. Two seeds do not support population success probabilities or a real-flight safety claim.

## Outputs and success meaning

`audit/viewer-data.json`, schema `m31-nominal-comparison-view-v1`, pins the source commit/manifest and producer index, sets `physicalValidity: false`, names ID17 and floor z=0, and exports four paired cases. Each case has its seed/dt/cadence, `off`, `coupled`, and `comparison`. Both arms contain every saved initial/completed endpoint, status/reason, nominal and saved last times, segments and final motion summary. Off frames additionally contain ID17 vz and source-line provenance. Exactly one duplicate segment boundary is removed. A stopped arm has no invented frames beyond its own endpoint.

`audit/audit.json`, schema `m31-nominal-comparison-audit-v1`, contains evidence pass status, source/producer/prior publication pins, four initial-prefix receipts, new journal descriptors (part names relative to `results/`), static dependency closure, counts, actual nominal outcomes/termination IDs, comparisons, resolution sensitivity, read anomalies, arithmetic scope and omissions. `viewerPin` identifies the exact viewer bytes. `passed` concerns this contract; `allNominalPathsCompleted` is a separate outcome.

`audit/launch.json` and `audit/exit.json` record the local allocation. Failure retains a false audit report, or a separate failure file after a late error, and exits nonzero. A partially written viewer is unusable after any failure. Finalization/display must require the passing audit, no failure file, exact export pins, internally closed zero-exit audit and externally closed zero-return audit supervisor with both wall and output caps passed. The external audit supervisor receipt is created only after the auditor exits, so the auditor cannot self-certify that final closure.
