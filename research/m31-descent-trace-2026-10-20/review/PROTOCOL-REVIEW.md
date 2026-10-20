# Independent prospective source review: saved-evidence descent trace

Date: 20 October 2026.

Reviewer role: independent protocol and source challenger, separate from the extractor author and the independent audit author. This is a source review of `research/m31-descent-trace-2026-10-20`, not a result review.

## Disposition

**Source design accepted for the prescribed single saved-evidence extraction, audit, byte-only finalization and display allocations, conditional on the complete source/input freeze and exact-public source verification described below.** No source-level blocker remains in the candidate identified in the hash table. This review does not declare any new extraction, audit, display or scientific finding successful. It does not reopen any former allocation.

The reviewer read the protocol, input descriptors, all new Python and JavaScript sources, viewer HTML, dependency pins, runtime note and literature scope. The reviewer also checked relevant existing index, archive, replay, publication, closure and supervisor metadata and read the physical-controller and floor source. Python abstract-syntax parsing, JavaScript syntax-only checking and JSON parsing passed. No new raw-journal extraction, numerical audit, storage allocation, simulator import, native invocation, finalizer execution, browser launch or UI allocation was performed in this review.

The accepted task is computational-only and observational. It selects a drone and paths after their stopping behavior was known. It can describe saved controller requests, motor state, orientation and delivered model force; it cannot establish a causal defect, a successful intervention, real-flight validity, safety, aerodynamic accuracy or novelty.

## Fixed evidence and selection

The input contract selects exactly eight saved journals: the four original first-second paths, followed in the same case order by their four exact-state continuations. The cases are:

| Case | Original controller/k1 pairs | Continuation pairs | Combined pairs | Joined replay endpoints |
| --- | ---: | ---: | ---: | ---: |
| `seed2026102001-h005` | 100 | 362 | 462 | 925 |
| `seed2026102001-h0025` | 100 | 362 | 462 | 1,848 |
| `seed2026102002-h005` | 100 | 400 | 500 | 1,001 |
| `seed2026102002-h0025` | 100 | 400 | 500 | 2,001 |
| Total | 400 | 1,524 | 1,924 | 5,775 |

These are prospective input and verification counts, not newly measured outcomes. The 75 compressed parts comprise original part counts 3/6/3/6 and continuation counts 9/18/10/20. Input descriptors match the existing original archive/index and continuation index. The independent audit checks the fixed stream order, case IDs, origins, sample counts, time steps, part names, offsets, lengths and hashes, including each part's exact identity in both the prior public result manifest and the new source manifest.

The selected record is always ID 17. At each saved controller update, the immediately following record must be the corresponding completed k1 stage. The excerpt preserves the full selected controller row, derivative/consumed row, prepared native row and delivered load row, including their original binary64 words. Complete source-line sequence, byte offset, byte length and SHA-256 are retained. All journal bytes are scanned and hashed for provenance; only the prescribed controller/k1 pairs receive the new descriptor calculations.

The source audit independently requires all 64 row IDs to be canonical and unique before selecting ID 17. It checks:

- Controller step and control-index cadence, exact relative/original timestamp words and exact time-step words.
- Immediate controller-to-k1 sequence adjacency, completed stage status, stage identity and saved native-success status.
- Controller state against the latest saved endpoint; controller raw state against enclosing raw state and the k1 raw-state row.
- Projected state against enclosing native input and saved native raw input.
- Controller commands against k1 commands and the enclosing held-command array.
- Nominal motor words against the saved motor-state words and prepared forces, plus prepared center against saved position.
- Full selected consumed rotor, collective, world-force and world-moment words against the same-ID delivered load.
- Each continuation's entire 64-by-17 initial-state word array against its own original final-state array.
- Case-end records against the corresponding existing index entry, and the separately reported final endpoint against the last completed saved step.

The selected k1 is the motor state before it responds to the freshly updated command. A command/delivery mismatch may include motor lag and attitude effects. The viewer and reporting must retain this distinction.

## Scientific descriptor review

World +z is up. The reviewed scalar construction uses saved state and saved target data, rather than regenerating Boids, controller commands, native loads or a trajectory.

The saved target is checked using the frozen operation order:

```text
targetZ = z + (2.5 * desiredVz + 1.5 * vz) / 6
requestRaw = 6 * (targetZ - z) - 4 * vz
requestedNetAcceleration = clamp(requestRaw, -4, 5)
```

Reading the prior physical-controller source confirms this vertical request expression. The algebraic expression `2.5 * (desiredVz - vz)` must not be substituted with a claim of bitwise identity; floating-point cancellation and operation order differ.

Commanded total thrust and nominal motor-state total thrust are separate left-associated sums of their four saved values. The saved native prepared axis-z component is multiplied by the nominal total to produce nominal vertical force. This uses the saved native orientation deliberately, because native projection can change quaternion words. Delivered vertical force is the saved native world-force-z component, bound to the consumed load. The derived acceleration `deliveredFz / 0.027 - 9.81` must match the saved vertical derivative word. The weight denominator is `0.027 * 9.81`.

The 15 reported descriptors are height, actual and desired vertical velocity, target height, raw and clamped vertical request, commanded and nominal total thrust, native axis-z, nominal and delivered vertical force, nominal-minus-delivered force, nominal and delivered weight ratios, and delivered net vertical acceleration. The audit separately implements this arithmetic and also binds the prepared native-total word to the nominal sum.

Nominal-minus-delivered force is a same-state algebraic comparison. It is not an airflow-off rerun, an estimate of an alternate trajectory or a decomposition establishing which controller or Boids mechanism caused the descent.

Each case retains the first and last sampled values, minimum and maximum of all descriptors, six strict-sign counts and first matching saved samples. The two paired conditions distinguish desired upward motion while moving down from requested upward acceleration while accelerating down. The first match is a sampled observation, not a continuous onset time; counts are not durations. The final completed endpoint is reported separately from the final controller sample. All paths and extrema remain reportable even if the proposed interpretation fails.

The two seeds give different initial locations to ID 17. The second seed is descriptive context, not a matched causal control. The two time steps and four exposed paths must not be pooled as independent trials or represented as held-out confirmation.

## Independent audit boundary

`source/audit.py` was authored separately and does not import `source/extract.py`, a simulator, controller module or native module. It reselects the rows directly from the saved journals, independently checks bindings and cadence, reconstructs the 15 descriptors, predicates, extrema, first matches, summaries and final endpoints, and compares the extracted trace and display data to those reconstructions.

The audit uses stricter artifact JSON parsing, including duplicate-key and nonfinite-number rejection. It checks the exact 1,924 trace lines, semantic structure, finite numeric values by binary64 words, output closure, extraction source commit, extraction receipt and output-size binding. At completion it rechecks the source publication and extraction report/trace/view pins.

The byte verification, gzip streaming and source JSON parser in `source/common.py` are shared. Storage parsing is therefore **not independently implemented**. This boundary is explicitly disclosed in both the protocol and audit report design. Agreement supports independently written selection and scalar calculations within that shared parsing boundary; it is not a second aerodynamic solver, a full independent trajectory integration or formal numerical error analysis.

## Prior-public evidence gates

The audit requires the following exact prior public result identities:

| Prior checkpoint | Public result commit | Manifest bytes | Manifest SHA-256 | File pins |
| --- | --- | ---: | --- | ---: |
| First second | `637c25294f162bea39970d12df0206f25dead889` | 20,563 | `a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b` | 100 |
| Continuation | `a0f595f34a4f9ef8cef516caa0cde60053e0eade` | 33,149 | `90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81` | 157 |

For each, it checks the existing publication receipt's commit, manifest path/size/hash, verified pin count, exact-commit public URL and remote/committed byte-equality flags. Required prior metadata and all 75 journal parts must have identical pins in the prior result manifest and new source manifest. Original archive reconstruction metadata must match the journal descriptor.

The existing original native/audit/display/archive closures and continuation storage/native/audit/UI closures are required to be `closed-passed` with one attempt. Prior native/audit successful exit records and supervisor wall results are also checked; continuation supervisor output-cap results are required. The reviewer read these existing small records and confirmed that their field names, schemas, status values and source-commit associations match the audit's checks.

These checks consume saved publication evidence. They do not make a fresh network request from the numerical audit or reopen the prior audits. The new source-publication gate remains a separate prospective requirement.

## Byte reads, allocations and failure handling

The retry wording and code now agree: **each verified-read operation has at most three attempts**, including its first attempt. Separate gate-before, journal-consumption and gate-after checks of the same file are separate operations. This is not a maximum of three reads of a file across an allocation.

Every accepted operation verifies whole-file length and SHA-256 before returning its bytes for consumption. Failed attempts record repository-relative path, operation number, attempt number and mismatch details or OS error number. Persistent failure raises and closes the phase. No whole extraction, audit, finalizer or UI rerun is authorized. The unchanged old locks and failure evidence remain authoritative.

Extraction and audit reports/failure records retain the common reader's anomaly events. The finalizer now has its own supervised allocation and report/failure records retaining those events. Display gates emit structured success/failure records, and `source/ui.cjs` retains their output in `ui/gates.json`, including caught gate failures. An external forced termination remains a failed phase; downstream consumers must use the supervisor result and cannot infer successful closure from a partial artifact or an earlier success-looking internal report.

The common helper and supervisor explicitly reject optimized Python with a non-assert exception, including an inherited optimization environment setting. This prevents assertion-based selection, pin and budget checks from being disabled by optimized Python.

| Phase | Successful wall bound | External timeout | Output bound |
| --- | ---: | ---: | --- |
| Extraction | 900 s | 920 s | 32 MiB; trace separately below 28 MiB |
| Independent audit | 900 s | 920 s | 2 MiB |
| Byte-only finalizer | 900 s | 920 s | 2 MiB reports plus at most 64 KiB viewer pins |
| Display | 150 s | 160 s | 16 MiB |

Exclusive supervisor launch locks and exclusive output creation prevent authorized whole-phase retries. Supervisors record return code, wall time and output size/cap status, terminate the owned process group and reap the child. The successful wall bound is stricter than the external timeout. A process that exits zero after the successful wall bound still fails its allocation.

Finalization requires passing extraction and audit supervisors, a passing 1,924-sample audit, absence of extraction/audit failures, and exact audit-to-view length/hash binding. It writes viewer pins and repeats the source gate. Pre/post display gates additionally require passing finalization, absence of all three phase failure files and exact current pinned bytes. Partial viewer pins left by failed finalization cannot authorize a display allocation.

The fixed localhost server is outside the allocation process group. Browser ownership is constrained to one launch of the existing configured Chrome executable. No installation, purchase or new scientific executable is part of this task.

## Viewer and display verification design

The viewer uses the two existing audited full-cloud replay datasets. Their dependency length/hash pins were checked against the existing files, and each prior audit binds its replay data. Original final positions and continuation initial positions agree for all four cases.

For each case, the viewer keeps the original final endpoint at original time 1, drops the equal continuation initial endpoint, and adds 1 to subsequent continuation times. The prescribed totals are 5,775 joined endpoints and 1,924 controller samples. Saved endpoint positions are held; no new state is interpolated or evaluated. The force/velocity cards use the most recent saved controller sample at or before the endpoint time, and show that sample's own timestamp.

ID 17 is highlighted by an orange sphere with modeled radius 0.075 and an explicitly labeled larger wire visibility halo. Its trail follows saved positions. The floor plane at z = 0, with dimensions 102 by 20 and center (-9, 0, 0), agrees with the read factory floor extent. Other obstacles are explicitly omitted. The chart distinguishes nominal from delivered support and states that its lines connect samples without evaluating intermediate forces.

The display source checks every joined full-cloud position buffer against float32 conversion of the saved replay, every ID-17 focus position, floor height, selected held sample, sample/endpoint time label, support label and case count. It requires that all 1,924 samples are encountered. It also checks selection, slider, playback, orbit, reset, viewport overflow, desktop/mobile screenshots, absence of page/console/HTTP errors and refusal of a deliberately corrupted trace. It performs source/evidence gates both before and after the browser check.

These are prospective checks, not performed UI results. Publication still requires inspection of the produced screenshots and confirmation of a passing complete display receipt. A WebGL position buffer uses float32 for drawing; this must not be described as preserving binary64 geometry in the renderer. Exact saved words remain in the evidence.

## Reporting, privacy and literature

The new source/text scan found no private absolute machine paths or apparent secret material. Localhost references are intentional. The exact-commit public repository URL and literature URLs are public provenance. Runtime paths in generated errors are sanitized to repository labels; generated reports, console records and screenshots still need a separate result-stage privacy check.

The literature note keeps the existing access limitations: Reynolds's author abstract/citation/explanation was previously inspected, but the PDF body was not successfully inspected; relevant pages of the Vásárhelyi article were inspected, while its supplement was not read. No new literature search was performed here. Neither reference validates the saved load model or this controller, and this trace supports no novelty claim.

Result reporting must publish success or failure, all four case summaries, the exact excerpts, audit and phase receipts, independent result review, viewer and restart instructions without deleting old failures. A future focused intervention would require its own prospective protocol; it is not authorized by a favorable descriptive trace.

## Remaining prelaunch and result gates

Before any new allocation, the parent must freeze the full reviewed package, this review, all 75 exact public part pins, both prior result manifests and publication receipts, required prior indices/archive/closure/exit/supervisor files, both audited replay datasets and their audit records, and the actual viewer/module and referenced scientific-source dependencies. The reviewed files below must retain these exact identities. The manifest must have unique repository-relative paths and cover every file used by the source and display gates; a gate that verifies listed files is not by itself proof that the list is complete.

The source freeze must then be committed and pushed, and the exact-public source-manifest bytes separately retrieved and compared to the committed/local bytes. The source-publication receipt must identify that exact commit and manifest, record successful byte equality and the complete verified pin count. This review does not substitute for that receipt. The reviewer can inspect final manifest coverage after inclusion of this review without running any allocation.

Execution must preserve each single allocation's locks, logs, failures and output. Passing extraction alone does not authorize a scientific claim or displayed result: audit, finalization, display closure, independent result review and exact-public result verification remain required. If a phase fails, retain its evidence and stop the dependent sequence; do not amend frozen code and retry under this allocation.

## Reviewed candidate identities

All paths below are relative to `research/m31-descent-trace-2026-10-20`. Hashes identify the source-only candidate inspected before this review was written.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `PROTOCOL.md` | 6,512 | `a314bb93845307777571bcf6f94c0ffbfa7ee7af1a01d95ee796142eb30ae0db` |
| `RUNTIME.md` | 856 | `d0a15a6b88b2954f7cd03c36c0558e099b60eb7e319fac6b8aa73d2ab02fb3f7` |
| `LITERATURE.md` | 975 | `e400c23fb176c6c4b97015decaf52bcaf80f9b49973b6a65d68f2324646922b1` |
| `inputs.json` | 22,762 | `dc27050112c8038354769693afe32d570c1821242ab7fe1f04e0e747c919d012` |
| `source/common.py` | 3,435 | `5ce64d9740f1bc1b5394c49da871519195388721e439cf9f34c5c2bd2649140c` |
| `source/extract.py` | 5,712 | `8c2caaf08cdbfb1b11b542d95c45c2e357aba1ab6ade754e49aecbd2dbc0c289` |
| `source/audit.py` | 31,292 | `8ebd766f5a39e56acdfd9670bed8df8ebd3806b227e218d957a60cf61abd8ddb` |
| `source/supervise.py` | 1,889 | `d4afe8725356b4900c7a9e273e2ee20038658946b2031f85de9a8ca5871565d3` |
| `source/finalize.py` | 1,173 | `2d31531a6cfdf9cfc62863f8c9ecb00523c52718cc0e7b9dcb68f3d626827aaa` |
| `source/check-display.py` | 908 | `194be14ac508e27fee59dcc97e70ebee7980ce2d813db2c29572f1783ca7b0ff` |
| `source/ui.cjs` | 6,702 | `0ca03d20899033ca35129805f07ca172762f2fdcc1415d47e10dec50fcda05da` |
| `viewer/app.js` | 7,991 | `9a60f2d5c8a5fce123bb38729720f7c9c00579887afd29e0afe2e674d3cdccb6` |
| `viewer/index.html` | 4,816 | `38d8f465cfdcb5ac0151bc0c8a27d7d6dbde02e14590adb51ab07cfa84630750` |
| `viewer/dependencies.json` | 827 | `2dacfa1a85c22f512fcbbf03b03193ebd551c6811c014831a7c6520302c2e636` |

Python sources were parsed with `ast.parse` without imports or bytecode generation. Both JavaScript files passed Node's syntax-only check. JSON files parsed successfully. Those checks establish syntax only, not numerical correctness, runtime completion or display appearance.
