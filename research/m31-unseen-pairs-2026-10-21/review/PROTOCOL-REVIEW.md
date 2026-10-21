# Independent prospective protocol/source review

21 October 2026. **Accepted for source freezing**, limited to the candidate bytes below. No unresolved source-review blocker remains. This acceptance does not replace the complete dependency manifest, scoped privacy review, public source commit, independent manifest check or independent exact-public verification required before execution. Any later source change needs review of the changed bytes.

This was source-only inspection: text/diffs, Python AST and JSON parsing, JavaScript syntax checks and byte hashes. No initializer, controller, native model, simulation, audit, finalizer, storage qualification or browser/display allocation was executed or imported. Only this review file was written. Prior evidence, failures, locks and receipts remain untouched.

## Design and implementation findings

The prescribed order is original then memory for seed 2026102101, followed by original then memory for seed 2026102102. All four paths use N64, dt .005 s, .01 s control cadence and five seconds split at t=1. Both arms retain full F coupling. Each path initializes independently; exact equality of every paired 64×17 saved initial word and inequality between the two saved seed arrangements are audit requirements. These checks do not independently validate the initializer. Each reached second segment must inherit its own physical state, with no cross-arm substitution.

Both controllers are direct unchanged imports. Original target-z arithmetic remains `z + (2.5*desiredVz + 1.5*vz)/6`. Memory keeps the previous-error rectangle update, gain 2.5, clamp [-5,+5], positive-zero initialization, update count and exact target grouping. All memory words/counts cross t=1 unchanged; the t=.99 error is integrated once at the next control. Original memory stays null. The auditor derives original global indices without changing its inherited schema and checks the memory controller's saved indices. The integral clamp is not saturation-aware anti-windup.

Primary paired completion categories cover all four possible combinations. Each arm's stop/refusal reason and terminal time remain distinct. Secondary positions use the last common integer completed step, including initial step zero, with actual saved times and separate terminal summaries. Own-request vertical MAE is accumulated by ascending ID and then increasing common global control index. Both means, memory-minus-original, counts and actual windows are retained. A controller emitted before a subsequent refusal remains an observation of the current state. Empty common samples produce unavailable/null fields. Different evolving requests explicitly preclude a common-reference tracking interpretation; results are not pooled across pairs or with exposed history.

The producer retains the last completed physical state after a structured refusal and the latest emitted memory update without rollback. Refused trials remain separate from endpoint lists; a first-stage refusal therefore retains initial frame zero. Endpoint issues stop at the first affected completed endpoint. Unexpected, malformed, persistence or resource failures close the allocation and cannot be presented as four complete paths. Subsequent prescribed paths may follow only an orderly scientific stop. All reached journals are checked: four to eight according to segment reach.

The bounds align across config, runner, supervisor and auditor: 16,000 attempted native calls/stages, 4,000 completed steps, 2,400 successful producer/audit seconds including cleanup, 2,420-second external boundaries, 4 GiB producer and 128 MiB audit output. Full-horizon counts would be 2,000 controller records, 128,000 rows, 64,000 memory rows and 63,872 nonfirst memory integrations; actual counts must reconcile with reached records. The 4 MiB record limit, inherited qualified Journal, closure reserve, exclusive launch locks, new directories and bounded verified-read retries remain. Finalizer/display bounds and failure gates remain in force. No numerical, parsing or arithmetic retries are allowed.

The standard-library auditor checks both new streams, not an old baseline export. Its native evidence, projections, load consumption, derivative and RK arithmetic helpers retain their inherited implementation. Geometry-derived coefficients, native solve/residual model, initializer, steering, neighbor membership, inherited actuator/saturation law and contact decisions are not regenerated. The one-ULP saved-root policy and refusal norm reconstruction are disclosed. Source and result-byte gates are distinct from numerical validation. The new export has two pair entries; compatibility key `coupled` means the newly audited original controller, while both arms physically remain coupled. There is no resolution study.

The initial unconditional playback-advance assertion was a valid zero-step blocker and was corrected before freezing. UI QA now chooses an advancing pair if available; otherwise it verifies frame zero remains and records advancement unexercised. It checks saved position/time buffers, missing suffixes, outcome/refusal labels, common-window own-request MAE and its reference caveat, selection, orbit/reset, captures and corrupt-evidence refusal. Actual branch coverage still requires the later authorized display allocation and must be disclosed from its outcomes. The protocol's journal count wording was also corrected.

## Exposure, provenance and static checks

`SEED-EXPOSURE.md` and both search receipts retain the terminated working-tree attempt, the 30-second tree-enumeration timeout and the incomplete 120-second index-content search. No absence inference is drawn from these failures. I independently rechecked all 74 listed files in the completed scoped receipt against the published transfer manifest: 558,175 bytes matched their pins and contained neither decimal proposed seed. The receipt also reports checking 12,677 tracked filenames. I did not repeat that filename enumeration or expand the search. Prior use outside the completed inspected scope remains unestablished; the directory name proves neither universal novelty nor strict held-out status. Seeds/settings were fixed before any new scientific execution or outcome screening, as recorded prospectively.

Historical and literature notes correctly identify the exposed first-seed/transfer results and established compensation/integral-control context. No new literature acquisition or exhaustive novelty claim is made. Two fixed date-based examples at one resolution support finite descriptive comparisons, not a population success rate, statistical significance, general stability, physical aerodynamic validity, flight safety, optimality or a new integral method.

The retained transfer receipt binds commit `341cfa5e9bec84c0615825b82665385469d84a2b`, 198 pins and manifest SHA-256 `530b5b76624dfea7e21127832e552af9deeab7358816ed164cfa00a0130b872a`; the retained continuation storage receipt binds commit `a0f595f34a4f9ef8cef516caa0cde60053e0eade`, 157 pins and manifest SHA-256 `90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81`. These were local receipt/manifest identity checks, not new public fetches or historical trajectory audits.

All nine immutable inherited source hashes match the auditor constants. Original motion is 2,836 bytes, SHA-256 `c8cf434a23b6c7450eabbadb5bb371398d7a8d8c8810615667822529e8d12373`; memory motion is 3,848 bytes, SHA-256 `f7966691b52f2e14c2fbba82ed136fc99cf7a87b8d53725e08be9923128cea16`. The literal producer dependency closure contains 18 source files including both controllers and native-load. Final auditor/contract identities match those supplied by the independent auditor. Python AST, JSON and JavaScript syntax-only checks passed. The syntax-check runtime matched its 121,304,480-byte pin, SHA-256 `d0c6c74401e6a544bb4d4b2a9ded9c43298d4e6dcd5ebac4dd010c4c81774105`; Node option/path injections were removed for those checks. Scoped scans of these candidate text files and this note found no private home/temp paths or tested key/token patterns. That is not a universal secret guarantee.

## Reviewed candidate byte identities

Paths are relative to this study directory. This table is a review boundary, not the complete dependency/publication manifest.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `PROTOCOL.md` | 9097 | `493fd522c5d50a6795b5bfd8f4a6fe70d618365fd91cc73d25ffadce21a0ed02` |
| `config.json` | 1435 | `e169a205f767cd35a148d1e7084444b91eeec6c5be0d815eff3f8e6b3d341101` |
| `runtime.json` | 113 | `8347eef171a70a8e9ecd298684ee4c8e445b907aeb61630a26d105670641d225` |
| `AUDIT-CONTRACT.md` | 23159 | `27a100f84c882ecc54dfbf31069c655940271e283451ba1dd34b608d50ec45c1` |
| `HISTORICAL-CHECK.md` | 5596 | `8d9645bbd944a6b2ef1e10d06aeff2f4a005934e503fab232d787f40b5ce9b4e` |
| `LITERATURE.md` | 3349 | `680a4eb253d939508ccca71dc312775415e1c5d5f9763bae593304824c989717` |
| `PRIVACY-SOURCE.md` | 549 | `bd832ca60a709a10c3ce0048157cdafff18462e77d0e5e615a6a01120a27b30c` |
| `SEED-EXPOSURE.md` | 1860 | `3594483b3dd107b0fd8d53c26a6782a948b53330b48d685361030034a22f245c` |
| `seed-search.json` | 1582 | `ebd16bad59f41596e3b158adbdb5b11d31b9b1ed032264eef50086f072f43141` |
| `seed-search-scoped.json` | 5668 | `cd1852005b489050b361b9c170231f7ab530fc6ef457db973e94917c1158aba9` |
| `source/run.cjs` | 7037 | `b7709d207db941377868bd5928d601ea5ee21cd98aa2a342ec90eefb64c2ce9b` |
| `source/audit.py` | 72701 | `edc1dbc139f7dadb05735e3afb18b3a2da4d53ec77c22f0d5e65ef4817f59b37` |
| `source/supervise.py` | 2145 | `4581d0e88e1eff5343fd2f6df742c729385c6b8aa665fed20f071f088c59ea7b` |
| `source/gate.cjs` | 1271 | `91b158731394a60a87f131ac28102acdc5143e5369c945bc1b4baa2a4e2916ab` |
| `source/finalize.py` | 2395 | `440403f858a1b9ef51d96ac6148d667baa328038a3ece23a751ea2afe1908374` |
| `source/ui.cjs` | 9397 | `2ce570c7d804a2f0a47cdf5fffa01ad196d0329b9d629d62a73eb4c8773195af` |
| `viewer/app.js` | 8502 | `0c0e6d85f4333348b860b77bd9004aa7ad7ff910fffe1c5990abe588dba322a1` |
| `viewer/index.html` | 4980 | `a31edc8a87765b88a42755058aa8f5db914ed13c3360cb045225bed8da3efc2e` |
