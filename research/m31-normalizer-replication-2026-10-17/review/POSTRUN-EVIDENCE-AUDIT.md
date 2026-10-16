# Independent saved-evidence audit: M31 normalizer replication

Date: 2026-10-17

**Disposition: accepted as a complete, internally consistent negative benefit result within the registered finite comparison. No saved-evidence discrepancy was found.** The checker finished its evidence processing and returned exit 1 because the registered benefit gate failed. This is not an overall scientific pass, a containment failure, or evidence that every individual candidate call was slower.

## Scope and immutable evidence

This audit read saved JSON/text, hashed saved files, compared local files with read-only Git blobs, and recomputed timing fractions with exact integer arithmetic. It did not execute or import project modules, rerun either scientific stage or checker, reproduce the model calculations, perform new mutation controls, probe live processes, or change source/results. Numerical validity and finite corruption-control outcomes below are inspected claims of the pinned checker; this audit independently verifies their completeness and binding, not the underlying numerical operations again.

Source commit: `08ed31c184f88f95217dca689d3727c44c75e8c4`.

The machine-readable inventory is `review/POSTRUN-EVIDENCE-READING.json`: **338,226 bytes**, SHA-256 **`a4b9198380bb4872548dc80e517754e73ac1ebe8aad520c1d9525c3eb760c259`**. It records every file pin, 489 expected-pin comparisons, the 24 pair calculations, all six exact medians, source closure comparisons, control rosters, and both raw lifecycle/failure streams. All 274 unique pinned files were rehashed unchanged at audit completion. Paths in the following table are relative to this package.

| Evidence | Bytes | SHA-256 |
| --- | ---: | --- |
| `source-manifest.json` | 35495 | `0ed9fb1e8593306db4fbf0414df69775108c62989a7855718a7fc940475eb277` |
| `source-publication.json` | 875 | `39efd67b102e844b45fbf4e4015f97887bc7fd5f4e2c94256d076a786f070bd7` |
| `results/index.json` | 71308 | `3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393` |
| `results/check.json` | 53226 | `f7f25b6696f5d5dd3231c12c97a7c7f3f49ca10a9751f23796facf51da55e7d4` |
| `results/kernel-supervision.json` | 34602 | `a6e3da0fb596254627eb7035ba10a87676645af6b8d85e20f8e2c53a3f12a6b6` |
| `results/checker-supervision.json` | 39704 | `f3daa89b5e3d96e46b4c2b703b0705be6e52ffc619111c09bf150e01ab1c93c5` |

## Source and consumed-pin closure

All **169 source-manifest entries** match both local bytes and the exact committed bytes. The manifest itself also equals its committed blob and its receipt pin. The manifest includes inherited supporting evidence as well as code; 169 is the manifest-entry count, not a claim that all entries are executable source. Index, checker, attempt, authorization, and supervision identities bind to the same commit, manifest, and configuration. Configuration SHA-256 is `ef3a5378b3fc1abf3899e83448857f46c2a518281eca3f26c9f620c46db9aa22`.

All **83 unique checker-consumed input pins** and **12 reference-file pins** match saved byte counts and SHA-256 hashes. The reference roster is exactly four controls, six scheduled states, and two lifetime inputs. Pins supplied by the index and both supervision reports also match, including the kernel index, final checker report, raw guardian events, authorizations, failure journals, and published logs.

The pinned publication receipt records exact remote verification of 169 manifest entries at `2026-10-16T23:33:01.978830+00:00`. Kernel and checker attempt timestamps are respectively `2026-10-16T23:33:16.855967+00:00` and `2026-10-16T23:34:56.125407+00:00`, after publication verification and before the cutoff `2026-10-17T01:00:00Z`. This auditor independently checked local and committed bytes; the remote-download statement is receipt evidence, not a new independent network verification.

## Primary timing result, recomputed directly from the index

The primary measure is parent monotonic spawn-to-exit wall nanoseconds for an isolated worker. Each scheduled state has exactly four pairs in fixed order **AB, BA, BA, AB**, where A is baseline and B candidate. Both calls in each pair share the recorded immutable input and exit 0. The scheduled records also match their entries in the flat index call roster.

For each pair the audit recomputed `candidateWallNs / baselineWallNs` as a reduced exact fraction. It sorted the four fractions by integer cross multiplication and averaged the middle two exactly. A win means a strictly smaller candidate wall time. Every pair's raw nanoseconds and reduced fraction, each median fraction, and every win count agree with `check.json`. The inventory's `timing` array preserves all 24 pairs, their orders, and absolute wall times.

| State | Exact median candidate/baseline ratio | Decimal display | Wins / 4 | Median ≤ 0.9 | Wins ≥ 3 | Benefit |
| --- | --- | ---: | ---: | --- | --- | --- |
| run-a-t0 | `939672151254379361/926041237531373472` | 1.014719553699 | 2 | fail | fail | fail |
| run-a-t5 | `1558468235150017927/1606608464821991736` | 0.970036116001 | 3 | fail | pass | fail |
| run-a-t10 | `2211549683045486037/2254900260456865676` | 0.980774946825 | 3 | fail | pass | fail |
| run-b-t0 | `9725081758844211/10125451167286664` | 0.960459104308 | 4 | fail | pass | fail |
| run-b-t5 | `3633397414381902903/3852411556117607528` | 0.943148820279 | 2 | fail | fail | fail |
| run-b-t10 | `1272160656642773/1302631713487500` | 0.976608079990 | 3 | fail | pass | fail |

All six median ratios exceed the registered 0.9 maximum. Run-a-t0 and run-b-t5 additionally miss the minimum three wins. Consequently the every-state benefit gate fails. The table is a descriptive fixed six-state comparison with four balanced pairs per state; it supplies no pooled estimate or confidence interval treating states/frames as independent trials. Secondary method-return timings, trajectory generation, and viewer playback speed are not substituted for this primary measure.

## Checker completeness and the negative-result distinction

The index has `error: null`, completed status/stage, two generation runs, all six scheduled states reached, and zero missing scheduled states. It records 48 scheduled scene calls and eight fixed-control scene calls, with the separate direct and lifetime transcripts present. Both generations have 51 recorded frames, reach 0, 5, and 10 seconds, and have no reported stop reason. The fresh registered seeds are 26171021 and 26171022; the generation configuration uses 64 drones, Boids, and airflow off.

The saved checker reports:

- `recordIntegrityPassed`, `equivalencePassed`, `admissionPassed`, and `fixedControlsPassed`: true.
- Six of six scheduled states reached, model-admitted, independently verified, and certified; every scheduled outcome reports both arms verified/certified and equivalent.
- Informative nontriviality and passed lifetime checks, with both lifetime inputs independently verified and certified.
- All 42 corruption controls executed and rejected in their intended failure families: 21 unique recipes for each arm, with matching recipe rosters.
- All six cache controls executed and rejected in their intended failure families: five direct-transcript controls and one lifetime state-binding control.
- `benefitPassed`, `passed`, and `transferAuthorized`: false. The sole top-level error is `correctness-admission-or-benefit-gate-failed`.

The two positive fixed controls are admitted/certified in both arms; raw-force and order-incompatible controls are verified refusals in both arms. Those intended refusals are successful control evidence, not missing scheduled certifications. The populated outcomes, performance, references, controls, and 83 consumed pins support a completed negative decision rather than a partial checker abort.

## Saved lifecycle, first failure, and output closure

Both raw guardian files are newline-complete, contain the exact five-event roster, and equal their supervision copies. Both raw authorization documents equal their report copies. The audit checked the recorded order from supervisor start through guardian startup/ready, a positive owned leader sample, authorization, child start/exit, a sole-leader release observation, release, and two absence probes. Supervisor identities match attempt and authorization records. Each release sample contains only its guardian, with positive RSS, and each report records known guardian wait status and guardian exit 0 before successful closure.

| Stage | Child exit | Supervisor success | Normal release / closed | Wall seconds | Peak sampled group RSS bytes | Samples |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| Kernel | 0 | true | true / true | 84.276048083790 | 446169088 | 978 |
| Checker | 1 | false | true / true | 44.404171499424 | 115982336 | 505 |

Kernel supervisor PID/PGID is 38144, guardian group 38491. Checker supervisor PID/PGID is 39767, guardian group 40111. Each has two timestamped recorded absence probes for its own group, an observed absent scientific child before release, no cleanup signals/actions, no secondary failures, and source/runtime postchecks reported true. Saved peak RSS covers the retained-leader and release observations and stays below 1 GiB. Both stage wall times are below 600 seconds. Maximum recorded sampling gaps are approximately 0.179118 and 0.093653 seconds respectively; sampled RSS is not a continuous peak measurement.

The kernel failure journal is empty. The checker's 108-byte failure journal contains exactly one entry, with role `firstFailure`: `child-exit`, exit code 1, monotonic time 5619468289898333. It exactly matches the supervision primary, whose durability and journal durability are true. No missing-output or persistence error replaces it. This preserves the negative checker result through normal process-group closure.

The closed results tree contains **103 files / 42,143,336 bytes**. The checker pre-report accounting is 42,103,632 bytes; adding its final 39,704-byte supervision report yields that exact closed-tree total. Its saved breakdown is 33,203,702 kernel bytes, 8,861,408 checker bytes, and 38,522 metadata/log bytes before the final report, with zero unclassified bytes or violations. The final report adds to metadata. These totals remain within the registered 192 MiB kernel, 64 MiB checker, 16 MiB metadata/log, and 272 MiB combined limits. All four published stdout/stderr logs are empty and pinned. Private raw logs are reported empty; their private paths were not opened by this auditor.

## Limits on claims

The execution-context label is explicitly a caller attestation. The parent reports that both actual dispatches used `require_escalated`; this auditor did not independently inspect those external tool records. Runtime executable bytes were not reopened; saved runtime declarations and postcheck claims are bound through the pinned reports.

Process closure is supported by saved sampled observations, waited-status claims, and two recorded absence probes per group. This review adds no current live absence check, hostile-escape guarantee, or continuous memory evidence. Its scientific conclusion is limited to the frozen finite comparison: saved correctness/admission evidence remains positive, while the registered primary speed-benefit gate fails on every state. It does not authorize transfer, a persistent-browser speed claim, physical-validity claims, repair, or another scientific run.
