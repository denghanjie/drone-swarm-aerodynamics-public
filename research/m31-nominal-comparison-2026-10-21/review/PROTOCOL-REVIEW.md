# Independent prospective protocol and source review

21 October 2026. Package: `research/m31-nominal-comparison-2026-10-21`.

**Disposition: source accepted for the four prescribed single allocations, conditional on complete source/input freeze, independent manifest coverage verification and exact-public source verification before launch.** No source-level blocker remains in the candidate identified below. No outcome is assumed. Earlier allocations stay closed.

This review covers the protocol, historical assessment, configuration/runtime identity, producer and byte gate, supervisor, independent audit and contract, finalizer, paired viewer/UI verification, source-reuse note, claims, literature and restart. Relevant inherited adapter, controller/safety, physics, initializer, grid, storage and baseline metadata were read. Python abstract-syntax parsing, JSON parsing and four JavaScript syntax-only checks passed. No scientific module, initializer, controller, nominal flight, native query, storage qualification, audit, finalizer or browser was executed by this reviewer. Only this review was written.

## Question and historical scope

The defensible question is whether removing the implemented coupled-load intervention changes the descent and terminal outcome of the two exposed N64 configurations over the fixed five-second horizon. The historical assessment identifies earlier N16 off/full and force-only work, plus an N64 nominal/coupled comparison through the current adapter over 20 milliseconds. This is therefore a targeted extension on specified paths, not a first off/full experiment, a new flocking method or a novelty result. The assessment appropriately limits its absence finding to the named inspected work and discloses incomplete broad searches.

Both arms start from the same saved states and evolve their own closed-loop motion. Differences include changed neighbors, steering and subsequent controller outputs. This can establish a finite-path contrast under the implemented model intervention; it cannot separately identify direct force, torque, motor-lag or individual Boids contributions, validate aerodynamic accuracy, demonstrate a controller cure or imply real-flight safety. Two seeds and paired time steps do not establish population reliability or independent replications.

## Intervention and scheduling

The four prescribed cases are seeds 2026102001 and 2026102002, each at h=0.005 and 0.0025 seconds, N=64, with a 0.01-second controller interval. All full paths would total 6,000 completed integration steps and 24,000 derivative stages. Early inherited safety stops reduce those totals; the fixed subsequent cases still run. No replacement, tuning or rerun is permitted.

Only the nominal arm is newly produced. The existing projected adapter's `arm: 'off'` branch constructs nominal loads from the current projected motor state and orientation. The same consumption/integration functions retain motor lag, nominal reaction yaw, gyroscopic terms and quaternion projection. The source does not import the native solver; injected query/evidence stubs throw if invoked. The independent audit also requires zero stage-level native calls and null native evidence. Nominal thrust is not fixed-hover thrust and is not substituted directly from the new commands.

The motion wrapper is byte-identical to the original admission wrapper. It retains local 3D Boids, wall-priority filtering, target construction, actuator law and inherited endpoint safety/contact functions. The same wide-factory and physical sources are used. The source-reuse identities and final transitive dependency pins remain essential to the single-change claim.

Each nominal initial state is generated once per case by the pinned original initializer. The auditor does not regenerate it: every ID and all 17 state words must equal the corresponding original journal's initial record. Same-seed coarse/fine initial words must match exactly.

The producer preserves two segments: local 0..1 with origin 0, then local 0..4 with origin 1. The boundary uses the nominal arm's own full state, never the coupled t=1 state. Its encode/decode round trip preserves binary64 words and performs no additional normalization or initialization. Local step indices restart, and a controller update is due at local zero of each segment. Commands then remain held for two/four steps and all four stages. This reproduces the baseline's segmented clock arithmetic; it is not a claim of bitwise equivalence to an uninterrupted run.

## Stopping and evidence

Every reached initial, controller, stage, endpoint, safety and case-end record is retained. After each completed integration step, the unchanged safety function returns all inherited issues. The first nonempty issue array ends that path, retaining its triggering endpoint and issue identities; no second segment follows a first-segment stop. Arithmetic, malformed output, forbidden native invocation, persistence or resource errors end the entire allocation rather than masquerading as an ordinary safety stop.

There is no native aerodynamic-domain admission test on the nominal path. Completing it would not demonstrate that the coupled solver supports those later states. A stopping/horizon endpoint has no additional force evaluation.

The unchanged, previously qualified Journal uses 16 MiB raw blocks, 32 MiB compressed parts, a 4 MiB line cap, contiguous offsets and aggregate raw/compressed identities. Its prior passing qualification and supervisor are public-pinned and checked; no repeated storage allocation is needed. Unexpected failure can lose buffered records, as disclosed, and leaves an incomplete failed allocation. It must never be repaired into a passed result by deleting failed evidence.

## Independent audit

The standard-library Python auditor imports neither producer JavaScript nor an earlier auditor. Its scalar/projection/derivative/RK helpers are adapted from the prior independent Python implementation. Independence is from the JavaScript producer, not a newly independent third version of those helpers. Its own streaming reader independently checks new JSONL, gzip, parts, raw/compressed hashes and exact record order.

The audit fixes the complete configuration and budgets, checks public source and successful producer closure, rejects extra output files, and reconciles all stage/step/safety totals and physical output bytes. Before/after source and evidence checks prevent a passed report from referring to changed inputs. The source dependency traversal is textual and does not import scientific modules.

For every nominal vehicle/stage, it independently checks raw-stage construction, projection, held commands, nominal rotor sum, rotated force and arm moment, consumed load binding, body moment, reaction yaw, gyro term, all 17 derivative components, RK weighted endpoint and next-state binding. Basic arithmetic follows the frozen operation order and exact saved words. Each positive saved projection root may differ by at most one ULP from Python `math.sqrt`; the saved root is then used downstream, with comparison/difference counts reported. This is consistency under a declared tolerance, not an exact-rational, correctly-rounded, formal error-bound or cross-platform proof.

At each reached segment join, all 64×17 nominal boundary words must match. The audit enforces local controller/stage/endpoint clocks, immediate prescribed record ordering, completed off stages, no refusal, first recorded safety stop and exact case-end/index/termination-issue linkage.

The audit checks controller-state/command association, neighbor-ID shape/order, target binding and target-z arithmetic. It does **not** regenerate neighbor membership, Boids steering, yaw trigonometry, controller decisions or saturation. It validates safety-record linkage and issue fields without independently recalculating vehicle-limit decisions or contact geometry. The unchanged inherited source and explicit omissions are part of the evidence boundary; a passed audit is not a safety certificate.

## Reused baseline and comparisons

The audit pins original public result commit `637c25294f162bea39970d12df0206f25dead889` and continuation commit `a0f595f34a4f9ef8cef516caa0cde60053e0eade`, their exact manifests, publication receipts, successful audits/closures, indexes and replay exports. The stricter required metadata fields were checked against the existing files and are compatible. Original/continuation manifest identities remain the previously verified 100-pin/157-pin results.

Four original first compressed parts supply only their initial JSONL records after whole-part byte verification. The complete original/continuation trajectories are not rescanned or re-audited. Their previous audits are reused trust, explicitly disclosed.

The coupled export join keeps the original t=1 endpoint, removes exactly the duplicated continuation initial endpoint and retains all 5,775 known saved frames. The new audit checks local frame schedules, actual timestamps, index outcomes, boundary positions and final positions against full index states. Prior full-state continuation verification remains reused evidence rather than a new check of every coupled boundary word.

Off/coupled comparisons use integer `globalStep` at the last endpoint available in both same-dt paths, preserving each actual saved time and safety flag. Maximum/RMS center separation, mean-height difference and ID17-height difference are off minus coupled. Per-arm initial-to-final summaries are separate from common-prefix comparisons. A stopping endpoint may be integration-complete while its safety flag is false; both facts remain explicit.

Nominal coarse step k is compared with fine step 2k only through their common saved prefix. The reported maximum is over those endpoints and vehicles, not continuous time, and supports resolution sensitivity rather than convergence order or physical accuracy. A missing suffix is never fabricated.

Coupled final ID17 velocity is available from its pinned final full state. Coupled intermediate velocities and contact identities are absent from the selected replay/index representation; the export leaves them null with a disclosure instead of inventing a velocity difference or new stopping identities.

## Budgets, byte retries and closure gates

| Allocation | Success wall, including cleanup | External deadline | Output cap |
| --- | ---: | ---: | --- |
| Producer | 1,200 s | 1,220 s | 2 GiB, including 1 MiB reserved for closure |
| Audit | 1,200 s | 1,220 s | 128 MiB |
| Byte finalization | 120 s | 140 s | 2 MiB plus at most 64 KiB viewer pins |
| Display | 150 s | 160 s | 16 MiB |

Exclusive supervisor locks/output directories enforce one authorized attempt. Supervisors record return code, wall and byte caps, terminate the owned process group and reap the child. A zero-return child that exceeds the successful wall or output cap fails. The existing localhost server stays outside that group. Explicit non-assert checks reject optimized Python in the supervisor, finalizer and auditor.

Verified file reads allow at most three attempts per operation on I/O failure or length/hash mismatch, before exposing accepted bytes. Separate gate-before, consumption and gate-after operations have separate bounds. Parsing, arithmetic, browser launch and whole allocations are not retried. Producer/audit events, finalizer gate JSON and UI gate JSON preserve anomalies, including caught gate failures. Forced termination is a failed phase; partial internal outputs cannot override the supervisor.

Finalization requires passed producer/audit supervisors, closed successful exits, complete index, no failure evidence and exact audit/export byte/hash binding. It gates sources before/after. Display additionally requires passed finalization, rejects late failure files and rechecks all pinned bytes and audit/export bindings before/after. Browser code checks its data against the audit's pin and passing producer/audit supervisors.

## Display, privacy and publication conditions

The paired viewer displays saved endpoints only, aligns by discrete step and labels each pane's actual saved time. Unavailable suffixes hide that arm's cloud, highlight and trail and display an explicit absence message. They are not frozen as apparent continued flight. The floor now uses the actual modeled extent 102×20, center (-9,0,0), z=0; the QA snapshot reads its actual position rather than a constant. The 0.075-radius sphere and larger visibility halo are distinguished. Other obstacles are explicitly omitted.

The single UI allocation is designed to check every available buffer in both arms, missing suffixes, timestamps, ID17/floor, outcomes, selection/playback/orbit/reset, desktop/mobile overflow and screenshots, page errors and corrupted-data refusal. Float32 drawing buffers are compared to float32 conversion of saved positions; this is not a GPU-pixel or binary64-rendering guarantee. Screenshots and runtime outcomes still require result review.

The source/text scan found no private absolute paths or tested secret patterns. Generated logs and screenshots require their own result-stage privacy check. Literature access limitations and the lack of novel/physical claims are preserved. Browser/OS/system-library dependencies are not hermetically frozen, as disclosed; no performance claim is allowed.

Before launch, freeze this review and every reviewed file below, all transitive scientific/byte/viewer dependencies, unchanged-source provenance, exact baseline manifests/receipts/indexes/audits/exports/closures, storage qualification/supervisor, descent input descriptors and the four exact original first-part pins. Verify coverage and hashes independently. Then commit/push and separately verify the exact-public source manifest and receipt. Listing and verifying some files is not proof of complete dependency coverage.

After execution, require all closure gates, independent saved-result review, screenshot/privacy inspection and exact-public result verification. Preserve every failure and original coupled stop. No failed allocation may be reopened by editing this frozen package.

## Reviewed candidate identities

Paths are relative to this package. These source-only identities precede creation of this review.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `PROTOCOL.md` | 7,271 | `7737359bf82b04328d93a5b1e73c883605ba92d9562dde30065d2c069f1a0400` |
| `AUDIT-CONTRACT.md` | 16,594 | `beee6819534419a82eb36d51a797899500708f4a920236cc4ef666152f37629f` |
| `HISTORICAL-CHECK.md` | 11,765 | `48864a2bb5abe214a8edc56a55654cfabb272eb270c24357bb1cdd8d1d3e48a9` |
| `SOURCE-REUSE.md` | 1,772 | `89c76c21b3e2e24ffc2d1532f895d792009db09295cc07b394d0b228d7671fc1` |
| `CLAIMS.md` | 725 | `fda6b753e1fdf81b661583d7ba30c116cfd61109dc34e202626605d3a67d6756` |
| `LITERATURE.md` | 1,203 | `2f2d6751f4372dadc51b6ef15a81092517229b16d6b9b706068a0a2385849469` |
| `RESTART.md` | 834 | `5a254d8825ec0fe5ecbbe22418d67682e3992efdfdd3e4a2099278e838dff90d` |
| `config.json` | 921 | `ed09ce4eb9d6cf48a27ea7e3273baf01bf09dece5e18a6e318c81145a3e9dad7` |
| `runtime.json` | 113 | `8347eef171a70a8e9ecd298684ee4c8e445b907aeb61630a26d105670641d225` |
| `source/run.cjs` | 5,686 | `7769bf1786593399be24a8e2b18ab3f71080c715ce63a2db2630b3b72b939393` |
| `source/gate.cjs` | 1,271 | `91b158731394a60a87f131ac28102acdc5143e5369c945bc1b4baa2a4e2916ab` |
| `source/supervise.py` | 2,145 | `0800ce4580471a41b49514ec92a10ecc8e29d969c03b140928699142d45c6a9d` |
| `source/audit.py` | 59,287 | `9db7b2f7d77d2af5ca8d99a9e22f0964e553b92040bdeb4800ca2e4774206301` |
| `source/finalize.py` | 2,395 | `440403f858a1b9ef51d96ac6148d667baa328038a3ece23a751ea2afe1908374` |
| `source/ui.cjs` | 7,660 | `4f7297089d2b00c706ac37e39106e955051878e7c4a52b17898323673798f9d5` |
| `viewer/app.js` | 7,490 | `433d9e5f96a0b0bfbf25dd32e70bfa1dace0ae4108ff8005658345c2158c7d47` |
| `viewer/index.html` | 4,260 | `62133580a468d0a0f104221bb1cee1f916fba20a9624a5820625fdd9fd18eb81` |
