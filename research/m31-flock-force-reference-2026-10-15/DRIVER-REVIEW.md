# M31 full-flock static force reference — independent pre-execution review

Date: 2026-10-16 Asia/Shanghai. Scope: static source/protocol review only.

**Disposition: no remaining static blocker identified in the fingerprinted revision below.** The source is consistent with the selected reference-only question and prospective gates. This is clearance for the coordinator's freeze/review/push procedure, not an experimental result, performance estimate, physical validation, or guarantee of successful bounded completion.

Read `PROTOCOL.md`, `config.json`, `schema.json`, `source/experiment.cjs`, `source/independent.cjs`, `source/run-step.py`, the independent API/method note, restart note, and supplied compensated-summation source note/BibTeX. Rechecked the latest driver after the coordinator's pre-exposure repairs. The prior domain manifest/result hashes were checked by file hashing. No module was imported or executed; no syntax execution, fixture, pose decoding, geometry, wake field, receiver root, force calculation, integration, or benchmark was run. No repository file was edited by this reviewer; this report is written under `/tmp`.

## Reviewed fingerprints

Paths are relative to `research/m31-flock-force-reference-2026-10-15/`.

| File | SHA-256 |
| --- | --- |
| `PROTOCOL.md` | `2f27d45cf7dd26fd36225dbd7c834b7cb5205638d51e0fef3b9972c4100e8e13` |
| `config.json` | `1c21e7c00c4da0375b3362ef03823296f7d45a6abf8431f3c30fdb41fc82f790` |
| `schema.json` | `ed864fb1d79e64bb81c0e7bc59d637912847372c7c72e013e5638823aebdabb3` |
| `source/experiment.cjs` | `b3dc10c5b92d4e0a98920b86f6870005c742b2290edad0dcbd6ae516d4b50a41` |
| `source/independent.cjs` | `4e1e31c00184f3dc82db8c040f5ba79313c724881d30b7c1581ddb26488270ee` |
| `source/run-step.py` | `2045fd2ffdf8aec221ed47eb651c654f1ff22879931ee074a70cf42a4e35978c` |
| `compensated-summation-source.md` | `68e55600dc20f873b97aeb858bb036cd94ef68c14501e1acfe49f467d83ab985` |
| `sources.bib` | `345d07c83cef42f91599483af06265a48b9c89d77c68780d32234a78a96a2ef1` |

The source note records a separate literature agent's primary-source inspection. This reviewer checked its relationship to the implemented recurrence and interpretation; I did not independently revisit its external publication URLs or source scan.

## Scientific inputs and independence

The driver pins metadata and binary hashes and byte length before decoding, uses primary case indices0/1/2 at exact times0/20/30/60, checks offsets and snapshot pose hashes against the pinned domain result, and hashes each prior receiver file against the pinned domain manifest before use. The actual manifest/result hashes match config: respectively `d6589044982631ba85fcf325c3c14f3752a827f0ce6b4fb96fd21e3f061edf4b` and `7e8cf6d53fe4a94c7c6faaf1bc1af36dfd1f30da6b519680c3a82d84ab2f5584`. The completed prior checkpoint is pinned as `770c2e77867b039e20ff5082e9299298aebc5642`.

Every saved vehicle is included. Quaternions are retained, finite, and checked against the1e-10 unit-norm assumption; no normalization is performed. The17-state construction correctly places position, zero velocity placeholders, quaternion, zero body-rate placeholders, and four prescribed nominal thrust values. The equality check against `F.P.m*F.P.g/4` enforces f0=0.0662175N. These are clearly new prescribed receiver inputs, not missing historical motors or a tilted-hover equilibrium. No derivative, controller, motor ODE, or integrator is called.

The independent module has no imports from production helpers. Its matrix rotation, direct nonself enumeration, branch order and strict predicates, factored fades/profile arithmetic, and same-pass code vectors agree with the declared protocol. Codes are matched by hash to both saved domain implementations. Counts include all4N code slots; contributions include code6 and code7. Ascending source order is retained. Neumaier correction uses each already evaluated term once and leaves the ordinary sum as the fixed comparator; neither an extra field pass nor outcome-dependent reference selection occurs.

## Callback/counter accounting

The driver correctly distinguishes independent guard **cumulative** counters from callback **per-receiver** counters. Snapshot baselines are added once; callbacks occur in ascending order and assert N−1 center checks,4N code length, saved counts, eligible counts and contribution counts. The final returned independent counters are reconciled with production and prior-domain totals. Counter updates precede callback assertions, so completed independent receiver work is not omitted on an assertion failure.

Successful coverage is fixed at12snapshots,28,000vehicles,112,000rotors,24field calls and112,000receiver calls per implementation. The final checks require107,972,000 independent center checks,75,028,480 combined eligible rotor visits, and491,535 support contributions per implementation through per-snapshot equality and the final production total. The fixed calls and per-snapshot coverage imply12production plus12independent fields. Production fields remain unchanged and are externally bounded; returned work is accounted after the call. Guards at independent receiver boundaries are not misrepresented as per-instruction guards.

The separate contributor-presence loop inspects code bytes, with early exit at code6/7. It performs no geometry or field evaluation. Its conservative whole-campaign bound is4 times the sum of snapshot N², or432,000,000 inspections, including self slots. This is distinct from107,972,000 nonself distance checks and the eligible rotor-visit counters. It enforces exact zero inflow when no retained contributor exists without treating a zero-projection contribution as absent.

## Roots, loads, gates, and storage

Each receiving rotor invokes production Newton and independent bisection exactly once; inherited `receiverWrench`/`loads` exports are not called to duplicate roots. Both solvers use their own inflow for alpha, residual and ideal-power checks. All declared finite/range/zero-inflow/root-bracket/residual/power gates are applied per rotor. The protocol correctly describes bisection brackets and rounded-zero residuals as binary64 diagnostics, not formally verified enclosures.

The two wrench paths use their respective signed rotor formulas and retain roll/pitch from effective rotor thrust. Both explicitly set modeled yaw to nominal zero, correct for the equal prescribed inputs. World force, nominal world force and world moment now use each implementation's own rotation function; force change is the difference of the corresponding rotated forces. This preserves the declared units and excludes gravity/gyro/contact terms. Every body/world load comparison is checked, with separate discrepancy summaries now including world force change.

The binary row order and all schema columns map correctly to writes:16Float64 values per rotor and35per vehicle. The vehicle order is T pair; primary/independent body moment triples; world force triples; world-force-change triples; deltaT pair; world moment triples; axis triples; quaternion norm error. Rotor order contains the three inflows, two thrusts, two roots, two alphas, two residuals, bracket endpoints, iteration count and two powers. Thus112,000×16×8=14,336,000 rotor bytes and28,000×35×8=7,840,000 vehicle bytes, total22,176,000bytes. Per-snapshot file-size assertions plus exact receiver coverage enforce these totals. One metadata row is written for every completed vehicle. Scalar arrays retain zeros; nearest-rank distribution summaries have the declared denominators.

## Pre-exposure repairs and failure evidence

Verified coordinator repairs include independent world-vector rotation; structured code-hash mismatch evidence with first differing source/rotor/code and source pose; a completed rotor-evidence prefix for a failing receiver; and accurate protocol wording limiting failure witnesses to values actually available at the failing stage. The code mismatch diagnosis inflates already saved domain evidence and does not reevaluate geometry.

Three final reviewer recommendations were applied before exposure: the independent guard now retains the current receiver pose, nominal thrust and offset; world-force-change comparisons have their own max/RMS accumulator; and a previous rotor's root witness is cleared before the next rotor's inflow checks. These fixes close the identified provenance/reporting gaps without adding scientific evaluation.

Caught failures save current context, available field/root/load witnesses, completed rotor prefix, counters, previous completed receiver and partial summaries. Completed evidence is written as rotor/vehicle/metadata streams. An interruption between these writes can leave unequal partial stream lengths; only the recorded completed receiver prefix and complete rows may be treated as retained coverage. The protocol does not promise unavailable receiver-level data from an interrupted unchanged production field call or an externally killed process. No post-failure field rerun is allowed.

## Cap semantics and interpretation

The one-shot design uses300s executable wall,64MiB new raw evidence with2MiB failure reserve, the frozen operation caps, and96independent root iterations. Production's12-iteration limit remains source-defined. The driver checks actual prospective write sizes, preserves the reserve, and never drops requested rows to fit. The supervisor provides an exclusive lock, recorded-ID/terminal protection, process-group termination/reaping, interruption handling, and final cap reconciliation. Its wall deadline and the cooperative298s guard are stopping mechanisms, not a guarantee of complete evidence. No memory acceptance threshold or speed benchmark is claimed. Prior domain evidence is referenced rather than duplicated into the new raw cap.

The protocol correctly limits qualification to the finite static equations on these prescribed inputs. It does not infer historical aerodynamic loads, physical validity of27g scaling or multiwake addition, wall/ground effects, trajectory convergence, cadence acceptance, spatial approximation quality, novelty, or real-flight safety. Earlier failed/incomplete temporal and trajectory campaigns remain unchanged. The coordinator must still freeze/push/verify all required sources and inputs, run at most once if selected, and perform the separately bounded saved-data review and publication checks.
