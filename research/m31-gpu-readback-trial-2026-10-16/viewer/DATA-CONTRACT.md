# Recorded GPU-readback view

This source belongs only in `research/m31-gpu-readback-trial-2026-10-16/viewer/`. It displays the fixed 128-byte integer fixture, page claims, host observations and externally recorded review completion as separate evidence. It contains no diagnostic, live GPU compute, flight model, fabricated trial result or synthesized actual bytes.

The initial delivery deliberately contains no `binding.json` or `evidence.json`. A missing binding leaves the page pending with no result and does not import or instantiate the Three.js renderer. An invalid binding displays unavailable, clears trial details and keeps controls disabled. Renderer failure after successful data binding leaves the accessible word selector and byte table available.

## Future binding contract

After the separately allocated diagnostic and review stages are actually closed, the root creates the actual `publication/FINAL-DISPOSITION.json`. The agreed keys are `diagnosticTerminal:true`, `savedReviewTerminal:true`, explicit executed/skipped state fields as appropriate, `sourceCommit`, `sourceFreezeSHA256`, `byteReadbackVerifiedWithinFixture` as an explicit boolean, `scientificQualified:false`, and `scope`. Terminal means closed; it does not imply either stage succeeded. The root keeps scoped verification false until independent review and external completion support it.

Only then may the root explicitly invoke the installed `bind.py` with the absolute new trial directory. The script reads a fixed allowlist of actual files, requires the actual terminal disposition, rejects symlinks and changing files, caps aggregate reads at 8 MiB, and exclusively creates two presentation manifests. It imports no operational code and derives no trial outcome. Missing optional artifacts receive no descriptor and remain unavailable. A failed trial can therefore be bound without inventing its absent return, file, review or completion records. The source adapter has not been invoked in this preparation.

`binding.json` has schema `m31-gpu-readback-view-binding-v1`, exact path `./evidence.json`, byte length and SHA-256. `evidence.json` has schema `m31-gpu-readback-view-v1`, campaign `m31-gpu-readback-trial-2026-10-16`, fixture ID `m31-u32-readback-128-v1`, and a `files` list. Each file has exactly one recognized role, its fixed `../` campaign-relative path, actual byte length and SHA-256. The role/path mapping is explicit in `evidence.js` and `bind.py`; no arbitrary external URL or path is accepted.

The browser hashes the manifest and every declared backing file before displaying any trial data. Reads are streamed within declared lengths, aggregate payload bytes are bounded, redirects are rejected, and loading is capped at 15 seconds. These digests provide integrity relative to the supplied binding; they do not provide authentication independent of the repository. This viewer is a presentation adapter, not another saved-evidence checker.

A digest-bound malformed optional JSON record or trace is reported as undecodable, with its fields/events unavailable and its raw file still linked. Other intact records can remain visible. No replacement record or event is synthesized. A malformed required terminal disposition, unexpected path, byte-count mismatch or digest mismatch blocks the complete view.

## Bytes and comparisons

Actual return bytes come only from the digest-bound `raw/returned.json` values in the identified `synthetic-gpu-readback-envelope`. Values must be integer numbers from 0 to 255 with no negative zero; no byte coercion repairs malformed values. Actual saved bytes come only from `raw/received.bin`. Expected bytes come only from `expected.bin`, whose 128-byte length and pinned SHA-256 `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951` are checked before use. The viewer does not synthesize the expected array or substitute it for an absent actual input.

The layout contains 32 words × 4 bytes: prefix words 0–3 / bytes 0–15, active words 4–20 / bytes 16–83, suffix words 21–31 / bytes 84–127. Three.js displays one cube per byte; base strips indicate each word’s region. Cube color reflects the selected direct comparison: returned versus saved, saved versus expected, or returned versus expected. The table displays all three inputs simultaneously. A full word is decoded explicitly as little-endian u32. `—` means unavailable; it is never zero-filled.

Equal bytes are green, differing or missing positions within supplied inputs are coral, and an unavailable input makes the comparison gray. Partial files remain partial. Unexpected total lengths are reported; offsets beyond 127 are not drawn and their presence prevents exact fixture equality. All 128 positions, including both padding regions, count in the comparison. Byte equality alone never creates an overall successful result.

## Evidence scopes

- Page panels project the actual returned envelope’s status, phase counts, observations and failures, explicitly as page self-report.
- Host panels display actual return/validation, persistence, cleanup, local-completion and failure fields. Exit zero or local completeness can accompany wrong bytes or an honestly recorded failure.
- Capture completion uses `publication/capture-execution.json`; process closure is a retained external observation, not reobserved by this viewer.
- Saved review uses actual `review/results/report.json` and `summary.json`, plus declared manifest/output records. Group pass counts and `recordIntegrityCandidate` retain their recorded meaning; self-verified flags do not become true in the viewer.
- `publication/review-supervisor.json` and exact child stdout `publication/review-output.json` are separate from root’s `publication/review-execution.json`. The child checker has a 30-second bound inside the supervisor’s 35-second bound. Actual supervisor exit, actual full outer elapsed and projected checker exit stay distinct.
- Root’s `publication/FINAL-DISPOSITION.json` is displayed as the root’s retained conclusion. `byteReadbackVerifiedWithinFixture` is never inferred from the byte colors. Scientific qualification remains false.

Saved trace events preserve file order; the viewer makes no cross-clock timing or performance claim. The historical 3D Boids viewer remains linked with airflow off. The current view makes no drone, aerodynamic, floating-point, large-transfer or general-reliability claim.

## Source-only handoff

The existing control-channel viewer provided the visual design reference. The new source uses the existing local Three.js module and OrbitControls at `outputs/step02b-source/vendor/`; no dependency fetch or installation is required. The relative URLs assume the final campaign/viewer layout under the same repository server.

No browser, GPU, network, QA, actual artifact binding or operational invocation was performed during this source preparation. Future presentation QA and any corrections belong after actual artifact delivery and separate authorization. No old campaign or published file was changed.
