# Proposed minimal fresh-state native-load transfer

2026-10-17. Source-only decision note. No execution allocation is made here. No fresh seed, snapshot-time literal, duration literal, generated state, native result, or reference result was selected or observed during this preparation.

## Decision

Advance to exactly two prospective N=64 post-initial moving snapshots, one from each separately seeded M31 Boids run, followed by one exact reference per snapshot and one F/L call per snapshot in one named Chrome process/profile. There are four fresh target calls. Keep timing repetitions closed.

This implements the conditional next step in `research/m31-native-load-baseline-2026-10-17/review/PROPOSED-CONTRACT.md`, section 4. The parent reports that the separate saved audit qualified all 12 retained calls, with all 14 arithmetic fixtures and four corruptions passing; its report SHA-256 is `e4b93e1b5d03f378b2d7ac254256fcb7deb2e3371dc4dd70136ec6c376974080`. Independent saved review remains a prerequisite to adopting that result as the completed retained-state numerical gate.

That pass supplies finite evidence that the unchanged native computation, delivered loads, and offline checker agree on the six exposed states. It supports asking whether the result transfers to two new inputs. It supplies no fresh-state evidence itself and does not convert the original browser supervisor's failed EPERM cleanup into a successful launch. Record separate fields for (a) numerical verdict and (b) operational completion. The new experiment must satisfy its own publication, launch, deadline, preservation, and cleanup contract. Any later timing decision requires both fresh numerical qualification and the new run's operational completion.

## Reuse and smallest source changes

Proposed new package: `research/m31-native-fresh-transfer-2026-10-17`. This is a new named source freeze; do not edit or reopen either preceding package.

| Function | Precise existing source | Minimal use/change |
|---|---|---|
| Actual Boids/dynamics generator | `outputs/milestone-31-source/sim.cjs` | Copy unchanged; call `run` only in the generation allocation. |
| Generator closure | `outputs/milestone-31-source/{grid,geometry,factory,factory-wide,wall-filter}.cjs`, `outputs/step02c-source/physics.cjs` | Copy all seven generator files under a private package source subtree preserving the original `milestone-31-source/../step02c-source` layout. Set the declared factory environment explicitly. No external workspace-only science imports. |
| Immutable capture/pose binding | `research/m31-moving-admission-2026-10-17/source/run.cjs`: `capture`, `projection`, `generate`, `optionsFor`, durable save/journal routines | Adapt into a generation-only entry. Remove all `M.method` calls, rational candidate imports, six-state schedule, old cases/cutoff, and old allocation. Preserve initial/final 17-word captures, frame identity, stop reasons, chronology, and failure evidence. |
| Generation validation | `research/m31-moving-admission-2026-10-17/source/check.py`: raw input, pose/capture, generation validation routines | Copy the relevant routines into the new checker; replace only the old run IDs/times/config bindings with the new two-slot contract. Do not run its old `main`. |
| Independent exact pair semantics | `research/m31-moving-admission-2026-10-17/source/pair-reference.py` | Copy unchanged; use `constants_from_graph`, `prepare_one`, `oracle_case` through the scene reference. Do not invoke its old fixture generator or `main`. |
| Independent scene/loads | `research/m31-moving-admission-2026-10-17/source/semantic-reference.py` | Copy unchanged; use `regenerate_scene` and its fixed reference roots/load boxes. Its extra hierarchy-plan calculation may remain as existing bounded overhead; no new rational candidate producer is needed. |
| Raw-word and graph adapter | `research/m31-moving-admission-2026-10-17/source/check.py`: `RawWordHelper`, `regenerate`, `graph_evidence`, `scene_reference` | Copy these small routines. Serialize roots/loads directly from `target['roots']`/`target['loads']`; remove `scene_reference`'s dependence on `validate_certificate`/`evidence.pop('independentReference')`. This serialization change needs review. |
| Constants/reference recipe | `research/m31-moving-admission-2026-10-17/source/spec.json` | Copy unchanged, or make a reviewed exact structural extraction of constants, PI, corners, limits, and reference recipe. Old `scenes`/timing declarations must never be evaluated. The smaller extraction is sufficient for the two unchanged helper modules. |
| Native F/L computation | `research/m31-native-load-baseline-2026-10-17/source/native-load.cjs`, `source/native-controls.cjs`, and `source/vendor/{reference-excerpt,anchor-kernel,lean-anchor,kernel,controls}.cjs` | Copy all seven unchanged. Preserve their exact arithmetic, 56-bisection O solve, residual, returned load law, controls, and two-million positive-term cap. |
| Browser delivery | Same baseline package: `source/browser.js`, `source/browser.html`, `source/build-bundle.py` | Copy/adapt package path and frozen schedule/counts; rebuild and byte-bind every standalone source slice. Preserve the Buffer adapter assertions, native ownership and consumption checks, durable per-call delivery. |
| Browser controller | Same baseline package: `source/controller.cjs` | Adapt fresh input-manifest binding, two-slot/four-call schedule, new schema and lifecycle. Replace inherited group ownership/`killpg` assumptions. |
| Native output auditor | Same baseline package: `source/check.py` and `source/checker-contract.json` | New named copy. Preserve exact rounding, Euclidean error, signed-load arithmetic, support/identity checks, all 14 fixtures and the four corruption laws. Replace retained-index/case/ref schema bindings and fixed-count checks with declared target/control counts. Never patch the frozen original module at runtime. |
| Simple child supervision | `research/m31-native-saved-audit-2026-10-17/source/run.py` | Reuse exclusive attempts, pre/post full pins, publication/runtime gates, direct retained-handle wait/kill/reap and public error redaction for generation, reference, and final checker. Browser ownership requires the separate change below. |

The native checker has explicit 64-row assumptions in `raw_input`, `reference_target`, and `audit_evidence`, plus a 12-call schedule and retained corruption case IDs. These are real integration changes, not merely a config swap. Permit only declared N=64 targets and the inherited controls' declared 2/3-row sizes in this experiment. Preserve the target arithmetic; change row-count expressions to the validated target size rather than opening an arbitrary-N route. Reuse fixed legacy raw-word semantic envelopes if desired, with new unique case IDs and explicit domain documentation; changing a domain string is provenance only and must be frozen consistently.

## Prospective generation contract

Reserve `fresh-a` and `fresh-b` without assigning seeds or times here. Before generation, freeze two distinct previously unused seed literals, their release/no-selection statement, initial-state recipe, duration, exact post-initial snapshot rule, dt, pose cadence, model/filter/search options, source/runtime hashes, and cutoff. Both raw initial states and scheduled snapshots must be durably preserved and hashed before any target aerodynamic computation.

The smallest same-family method is the unchanged wide-factory M31 generator with 64 drones, local 3D Boids, ideal observations, grid neighbor search, wall-priority filtering, airflow off, and the established dt=0.0025. This is a recommendation for adoption, not a completed freeze. Different seeds yield distinct deterministic realizations; they do not establish a statistical population or independent physical validation.

Source constraints matter: `sim.cjs` exposes full-state `progress` callbacks at multiples of 5 s or a stop; pose measurement runs at 0.1 s and `frameEvery` must be an integer multiple of that cadence. Recommend selecting each single scheduled snapshot as the run's terminal time, prospectively aligned with the existing callback/pose cadence, and keeping duration at most the prior 10 s horizon. The actual times/durations remain unset. This avoids changing the simulator or interpolating a snapshot. Alternatively, use its returned full final state at a prospectively aligned terminal time and explicitly validate that rule; do not assume arbitrary full-state callback times exist.

Capture IDs and all 17 native binary64 words: position, velocity, xyzw quaternion, body rate, and four actual nominal rotor forces. Preserve tilt and motor variation. The initial callback and streamed frames are copied before later simulator mutation. Save initial/partial records on failure; do not erase captured data when a run throws. Bind each scheduled full-state pose projection to the exact saved frame and terminal return, including signed-zero words. Preserve all stop reasons. A stopped, missing, malformed, or unavailable slot remains in the two-slot denominator, with no substitute seed/time or partial-state promotion.

For an informative moving transfer, require the declared positive-time capture, a genuine state change from its own initial state, and nonzero exact relative-coordinate change so a rigid translation cannot supply the whole motion evidence. These checks use raw saved words and require no initial aerodynamic solve. Report actual tilt and velocity; do not flatten states or select a later frame to obtain them. The fixed body-frame corruption witness must also remain available at its predeclared slot; an absent witness fails that assertion. Each fresh target must independently have at least one positive exact rotor coupling. Do not demand an initial-to-final positive-edge change: that would require extra initial reference work outside this minimal two-slot question.

## Exact reference and controls

After both generations are saved, one reference allocation processes the four fixed inherited moving-admission controls and the two fresh targets, once each, in frozen order. The four control literals/expected branches are in `research/m31-moving-admission-2026-10-17/source/config.json`: `positive` (three drones), `distant-zero`, `raw-force`, and `order-incompatible` (two each). Copy these exact literals; preserve expected exact admission/rejection and branch precedence. They are distinct from the 24 additional native microcontrols and must not silently disappear under a claim of deduplication.

The reference receives only raw words/IDs and the frozen common preparation/constant recipe, never native coefficients, roots, or outputs. Compute every logical nonself rotor pair: 4*64*63 = 16,128 per fresh state, 32,256 for both. The pair helper uses fixed 192-bit directed square-root bounds; the scene helper quantizes coefficients outward once at 192 bits, uses exact total-force weights, 192-bit source bounds, and exactly 128 cubic bisections. Preserve all rejected/reference-undecidable/resource statuses; no extra precision pass or adaptive refinement.

Important cap: the inherited spec declares `maxDrones: 180`, but `semantic.regenerate_scene` internally permits up to 216. The new entry must explicitly enforce the declared cap of 180 and the actual scheduled N=64 before invoking it. Merely copying the spec does not enforce that cap.

Save a self-contained reference record per case with input file and semantic hashes, common prepared words/constants, all pair statuses and positive coefficient enclosures, graph/order witnesses, roots, and signed rotor/collective/world-force/world-moment boxes. Its writer must serialize independent roots/loads directly; do not run the old filtered/hierarchy candidate solely to recover an `independentReference` field. Preserve the source/runtime/attempt identity and write an index binding all records. Both fresh references must be admitted, acyclic and descending-order compatible, complete, and positively coupled before the browser target stage.

One Chrome process runs the inherited 48 F/L screen controls, six paid ownership builds, nine Buffer adapter groups/56 assertions, and unchanged 24 native microcontrols once. It also runs the four inherited moving controls once per method: eight control calls, separately counted from four fresh target calls. The two admitted moving controls receive the same four-category exact load comparison; rejected controls pass only fixed status/reason/precedence assertions. No new literal fixture family is proposed. Review and document any genuine duplicate before freezing; do not delete coverage based on observed results.

The final auditor retains the 14 arithmetic fixtures and exactly four saved-output corruption laws. Freeze witness mapping by slot/control before any generation, not by searching outputs. A simple mapping is fresh-a for load-word, squared-force-law and ID association, and fresh-b for body-frame force. This is a proposed binding, still subject to source adoption. If a law has no actual word-change/tilt/nontrivial-root witness, report the assertion unavailable/failed and withhold overall qualification. Do not choose a different target afterward.

## Browser outputs and pass criteria

Use one newly owned profile and one fully named/pinned installed Chrome process; repeat none of the six retained targets. Target order is fixed prospectively, preferably fresh-a F,L then fresh-b L,F. Each call independently decodes the same immutable raw input and performs full current preparation, coefficients, solve, residual, load assembly and consumption. No reference coefficients, caches, previous ratios, warmed repetitions, or rendering are part of the experiment.

Persist all actual returned native rotor, collective, world-force and world-moment words, raw/prepared words, support, IDs, status, diagnostic residuals, and consumption/ownership evidence. Preserve an intent record before each call and a durable response before proceeding. Scientific refusal stays in the denominator; resource/internal failure ends the allocation and remaining calls are explicitly unattempted. Diagnostic durations remain diagnostics.

Every admitted target and admitted accuracy control must pass every category at every ID: rotor maximum normalized by mg/4, collective by mg, Euclidean world-force norm by mg, Euclidean signed world-moment norm by mg*R. Error boxes include reference uncertainty. Upper bound <=1e-8 passes, lower bound >1e-8 fails, overlap is unresolved. Preserve the exact frozen mg/R words. No average, relaxed tier, F/L agreement, residual, or componentwise vector maximum replaces these gates.

Also require unchanged raw inputs/prepared-operation graph and constants, exact positive-support agreement (with discrepancy witnesses), delivered-load arithmetic/ID/consumption correctness, F/L semantic-output parity, all fixed controls/assertions, and all four corruption detections. Overall fresh numerical qualification requires both slots and all four target calls qualified. The report must distinguish reference rejection/unresolved/resource limits from native refusal and from error-gate failure. A report may be complete yet scientifically unqualified.

## Operational supervision after the EPERM failure

Do not reuse the old `run.py`/`group-runner.py` lifecycle or call `killpg` unconditionally after a successful browser return. The saved-audit single-Python-child fix cannot by itself supervise Chrome's descendants.

Recommended small ownership change: the Python supervisor launches the pinned Chrome root and the pinned Node controller as its own retained `Popen` children, using a new private profile and a private loopback DevTools endpoint. The controller uses Playwright `connectOverCDP` to that owned Chrome, rather than launching a hidden detached tree. It must verify the actual Chrome product/version and all component pins, bind the endpoint to the unique profile and owned process, serve only allowlisted pinned bytes, and retain the existing verified-bundle delivery. Keep endpoint, PID, profile, command-line and raw logs private.

Normal close order: persist browser records; request CDP `Browser.close`/equivalent browser shutdown; wait for the specific Chrome root to exit and reap it; then finish/reap the controller. On failure/timeout, attempt bounded graceful shutdown and then terminate/kill only still-live retained handles. No name-based `pkill`, guessed PID, group signal, detached launcher, or signal after a handle has been reaped. Postrun source/input preservation and accounting run on failures too.

Chrome subprocess cleanup needs an explicit reviewable contract. A reaped browser root alone is not proof that all helpers exited. Require bounded private ownership/ancestry evidence for this launch and confirmation that its owned helper set is gone before operational success. Any lost ownership, orphan, permission error, missing close acknowledgement, or unconfirmed cleanup makes the stage operationally failed; it does not trigger another profile/process slot. The implementation must show how helper identity is checked without signaling unrelated processes or relying on PID reuse. If the available dispatch cannot enforce/verify this, stop before target calls for a source decision; do not label direct-root kill as full-tree containment.

This is an implementation obligation, not a claim of solved containment. Parent loss can defeat supervisor wall-time/cleanup/accounting; inherited per-process CPU/file limits remain, while no hard aggregate memory guarantee follows. State those limits openly. Keep one source-reviewed operational design and one scientific browser slot, rather than a series of launch experiments. Runtime/browser startup and identity checks belong at the front of that slot; they do not grant retries.

## Finite stage allocation recommendation

These are proposed caps for a later frozen allocation. No execution is authorized by this note. Stages are sequential, single-use, independently journaled; unused capacity cannot migrate into retries or new targets. Every stage verifies the source publication and complete source/runtime closure before scientific import and verifies preservation afterward. Later stages bind earlier closed attempts and output hashes without modifying the source manifest to insert result-dependent pins.

| Stage | Maximum work | Child wall / cleanup | CPU soft/hard | Scientific output cap |
|---|---|---:|---:|---:|
| Generation | One invocation; exactly two prescribed runs, no aero queries | 120 s / 10 s | 120/121 s, sole Node child | 16 MiB; 8 MiB per run |
| Exact reference | One invocation; four fixed controls + two fresh states, each once | 600 s / 10 s | 600/601 s, sole Python child | 64 MiB; 32 MiB per file |
| Named Chrome | One process/profile; fixed controls + four target calls | 120 s / 10 s | 120/121 s per inherited process, not aggregate CPU | 64 MiB; report <=32 MiB, journal <=24 MiB |
| Saved checker | One invocation; no new state/reference/native calls | 180 s / 10 s | 180/181 s, sole Python child | 32 MiB |

The sum is 1,020 s child wall plus at most 40 s cleanup, inside the prior proposed 1,500 s supervised envelope. Keep the overall 1,500 s cap as well. Scientific artifacts sum to at most 176 MiB; reserve 16 MiB for metadata/logs, total <=192 MiB, below section 4's 256 MiB science +16 MiB metadata envelope. Count duplicates, failed/partial files, private logs and atomic-write reserves. Chrome profile/cache storage needs a frozen bounded private scratch allowance and cleanup accounting; do not quietly exclude it from a purported whole-disk limit. Recommend a 64 MiB scratch ceiling with fail-closed periodic accounting: science + metadata/log + scratch <=256 MiB in total, still below the prior 272 MiB combined envelope.

Recommend sampled RSS stop thresholds of 1 GiB for each single-process stage and 2 GiB for the owned browser/controller tree, polled at <=250 ms. These are sampled stop rules, not hard kernel memory ceilings, and browser child sampling must use the same reviewed ownership set. If aggregation cannot be implemented soundly, omit the enforced-memory claim and adopt an explicit bounded-wall/no-memory-ceiling scope before launch. All per-stage deadline, output and cleanup checks require a live supervisor. Adopt the actual launch cutoff from the remaining authorized user window; this proposal does not extend that window.

## What remains before a run

1. Close independent review of the retained saved audit and record the separate numerical-pass/original-operational-failure premise.
2. Adopt this exact two-slot question; freeze unused seeds, times/durations, terminal rule, generation options, control/corruption schedule, resource/scratch/cleanup policy and cutoff before any generation. Check prior manifests/source only for seed reuse; do not probe candidate seeds.
3. Implement the small entries and reviewed deltas above; include the complete copied generator/native/reference source closure and all modified wrapper/build/check sources. Make a source diff that identifies every arithmetic-preserving vs provenance/schedule change. No old campaign `main`, fixture generator, rational candidate, or timing suite may be called accidentally.
4. Complete source-only review, syntax/JSON/bundle-byte checks, current runtime pin verification, and exact-commit source publication verification. Review the browser ownership/cleanup implementation specifically against the observed EPERM failure.
5. Issue one explicit staged allocation under the remaining window. Preserve each negative/partial outcome and close the attempt without replacement.

If both fresh states qualify, the next decision can authorize the already separate matched named-Chrome timing plan; none of its warmups/repetitions is allocated here. A two-state N=64 pass still establishes neither N=5,000 accuracy/performance, closed-loop aero flight, physical validity, broad portability, nor novelty. The original end goal remains unchanged.

## Inspection record

Only source/text reads and byte hashing were used for this note. No generator, candidate, exact reference, checker fixture, numerical module, or browser was imported/launched/evaluated. The following hashes identify principal inspected reuse surfaces; this is an inspection inventory, not the eventual complete execution manifest.

| Source path | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-native-load-baseline-2026-10-17/review/PROPOSED-CONTRACT.md` | 25856 | `2eb39856efa6b49d3c3ddf19269c4ab478d9a70f3358c0dd0701f3f7745ebdf2` |
| `outputs/milestone-31-source/sim.cjs` | 11475 | `2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e` |
| `outputs/milestone-31-source/grid.cjs` | 898 | `f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302` |
| `outputs/milestone-31-source/geometry.cjs` | 1462 | `e209e492fc523ab3c0c7df62745fb0d3dd7204f35e53309938a19d7895ed3d4f` |
| `outputs/milestone-31-source/factory.cjs` | 879 | `fe46384aac6150c45a2ba38e4494da16969aeab4a8875a8596f6ad8e53bb2c40` |
| `outputs/milestone-31-source/factory-wide.cjs` | 1712 | `8ea0d8784accfc039fee9ca2a2c0a86dc8e502b6d1003e4de54a8df8a999cc22` |
| `outputs/milestone-31-source/wall-filter.cjs` | 1182 | `8273cc40a9530748fe43e9ef0a4d9a995ee152f9968ce2368e61e2f205502512` |
| `outputs/step02c-source/physics.cjs` | 6115 | `0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1` |
| `research/m31-moving-admission-2026-10-17/source/run.cjs` | 24670 | `e1849f95cbd2bef9fbea1b4e45bb7f2b837bd6184711f60b2374d4e418d55460` |
| `research/m31-moving-admission-2026-10-17/source/check.py` | 68149 | `084f4f45aa353f7a7d8adc5c4a78eae4b09ee83fb2119741b01a317225d3fa69` |
| `research/m31-moving-admission-2026-10-17/source/pair-reference.py` | 44757 | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
| `research/m31-moving-admission-2026-10-17/source/semantic-reference.py` | 39634 | `ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c` |
| `research/m31-moving-admission-2026-10-17/source/config.json` | 5362 | `0a6b876edb63f13ce17ac81f996dea741e93abe72bdb28b7c6649626ffab278e` |
| `research/m31-moving-admission-2026-10-17/source/spec.json` | 296772 | `a47b9b920ddbbd14e1838e9c031a0b34dd1820f14959ef1295cef039e7f48d2f` |
| `research/m31-native-load-baseline-2026-10-17/source/native-load.cjs` | 16262 | `b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1` |
| `research/m31-native-load-baseline-2026-10-17/source/native-controls.cjs` | 11183 | `dad8f77ff170fee36d72594a84aa7a0f0092b8b51e93467c7b1445da85b2601a` |
| `research/m31-native-load-baseline-2026-10-17/source/vendor/reference-excerpt.cjs` | 2731 | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| `research/m31-native-load-baseline-2026-10-17/source/vendor/anchor-kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `research/m31-native-load-baseline-2026-10-17/source/vendor/lean-anchor.cjs` | 14840 | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| `research/m31-native-load-baseline-2026-10-17/source/vendor/kernel.cjs` | 16676 | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| `research/m31-native-load-baseline-2026-10-17/source/vendor/controls.cjs` | 5355 | `bf54381ee7f4dab8fbb19e48ada7e11c0f6d129cec1bcd21e5ce5075fc91f1ba` |
| `research/m31-native-load-baseline-2026-10-17/source/browser.js` | 30292 | `f8d5ef9cf6584d2bd4faabc89b2add64f466d9c295688c5ae3c10bc66099a87d` |
| `research/m31-native-load-baseline-2026-10-17/source/browser.html` | 296 | `2aa9f0ecfa7d4ceeec78596a289918bcf0520e9993bfed48f043e1e8ed26b371` |
| `research/m31-native-load-baseline-2026-10-17/source/build-bundle.py` | 2149 | `f5066b90733401a2b4cbae3af4e0676d57c19ab267dc7277c383685d8f566f2b` |
| `research/m31-native-load-baseline-2026-10-17/source/controller.cjs` | 17166 | `11e59e977a0549813ae466769406e418490786bd2feedb78b53d19a573d4dfeb` |
| `research/m31-native-load-baseline-2026-10-17/source/check.py` | 42628 | `bbf4a0fd042b0a19fe553ce3fd3be8e3775073fc958d38e19871c09c13ef09ef` |
| `research/m31-native-load-baseline-2026-10-17/source/checker-contract.json` | 9053 | `e648de28497b1ff830b51e9cd4e79be781283b2257ff4109b058949e9e64306f` |
| `research/m31-native-saved-audit-2026-10-17/source/run.py` | 14578 | `af90686eb0a927683109bc66f9a0f4dc837c6fd537c72d946228feb1aad31cc6` |

Parent-reported retained saved-audit report identity was independently checked by bytes only: `research/m31-native-saved-audit-2026-10-17/results/check.json`. Its numerical content was not re-evaluated.
