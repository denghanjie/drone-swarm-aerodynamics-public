# Coupled-load protocol and supervision source review

Date: 2026-10-17, Asia/Shanghai. Scope: prospective scene/pair allocation, complete status and evidence handling, tolerance versus verification claims, numerical negative-control relevance, and adaptation of the retained-guardian supervisor. The reviewer owns `source/supervise.py` and `source/guardian.py`; inspection of those adaptations is an author record, not an independent-authorship audit. The separate mathematical reviewer owns the inherited theorem's applicability, signed-load propagation and general enclosure argument. The separately authored checker is an independent numerical implementation, still subject to source review and the publication gate.

No scientific program, adapter, coefficient module, generator, solver, reference, negative control or closed suite has been imported/evaluated or run in this review. No external retrieval or new agent was used. Source reading, copying, editing, comparison and file hashing are the only operations so far. No runtime/cap/cleanup or fault behavior has been tested.

## Initial status and prospective questions

The draft establishes a distinct small-scene coupled-load allocation, not a rerun of the closed pair suite or a full-scale browser experiment. Its fixed candidate work and independent reference work are prospectively bounded, with no adaptive result-driven retry. The broad design correctly separates model admission, certificate soundness, candidate accuracy/tolerance and eventual physical/performance conclusions.

At this initial writing, exact scene counts, source filenames, spec/contract and final model/checker implementation remain pending. The supervisor's mandatory-source list still awaits those names. Consequently this initial report is not a final source-gate approval. The following points have been sent to the parent for explicit treatment:

1. State the evidence policy for a global preparation failure. A stopped scene must distinguish planned `4*N*(N-1)` pairs, observed enumeration count and the global-preparation stop reason. Missing pairs must not be silently represented as zero interactions. Once preparation succeeds, the declared complete enumeration must continue after every pair refusal, preserving status priority and auditable membership.
2. Keep scientific verification, domain admission, certificate validity and tolerance achievement distinct. A correct loose certificate can verify while failing a declared tolerance; it must not disappear or trigger tuning. An unqualified/refused scene is not an admitted load certificate, even when its refusal is correctly verified.
3. Freeze the exact tolerance semantics: exact decimal rational versus RN binary64 dyadic encoding of `1e-8`, and the exact comparison of certified normalized-error upper endpoints with that value. A rounded native comparison must not silently become the proof gate.
4. Negative controls need proven witnesses. Replacing a root interval by `[1,1]` is meaningful only for an independently established affected root below 1. Setting an error bound to zero needs evidence that the actual candidate/model error is nonzero, for example separation from the independent reference interval; a positive but loose existing error upper bound is insufficient by itself.

The declared count of actual positive terms is relevant only after complete pair admission is established. On refused scenes, status counts must preserve unresolved/rejected terms rather than claim that the resolved positive count proves the entire model's positive-term count. The finite scenes cannot exercise a two-million-term overflow merely because a source guard exists. Stable-ID equality binds self exclusion; the ordered subdomain must use exact prepared center-z and stable IDs, not input-array position or rounded/native sorting evidence.

## Preserved originals and supervision adaptation

Before modification, the published current-pair supervisor and guardian were copied to `prefreeze/inherited-supervision/supervise.py` and `prefreeze/inherited-supervision/guardian.py`. Those copies preserve their original bytes. The working source copies are separately adapted. The original identities are recorded below.

The kernel output and saved-checker input become `results/coupled-results.json`; the journal remains that path plus `.jsonl`. The saved-checker command keeps the established CLI:

```text
PYTHON PACKAGE/source/check.py --spec PACKAGE/source/spec.json --input PACKAGE/results/coupled-results.json --manifest PACKAGE/source-manifest.json --output PACKAGE/results/independent-check.json --root REPOSITORY_ROOT
```

The stage wall limit changes from 120 to 180 seconds in the report and both live/final checks. The output budget changes from 16 MiB to 32 MiB in the report and both live/final checks. The 1 GiB sampled process-group RSS limit, nominal 0.05-second sleep and 64 KiB final-report reservation are retained. The guardian's independent fallback deadline changes from 130 to 190 seconds in both child-running and release-wait loops, maintaining the former ten-second margin. This prevents an inherited guardian deadline from prematurely truncating the newly declared stage; it does not extend the supervisor's 180-second scientific qualification boundary.

The unchanged controls include an exclusive attempt file before child launch; unique mandatory manifest coverage; source, runtime-executable, manifest and publication-receipt identities before/after; a saved checker admitted only after successful closed kernel supervision with matching source identity and unchanged output/journal; post-checker prior-evidence rechecks; retained guardian ownership through child reap and release; conditioned process-group signaling; two group-absence probes; separate raw/private and path-redacted published log identities; and a best-effort terminal-error record if finalization fails.

The wall clock includes launch, monitoring, cleanup, log publication, output hashing and identity rechecks, ending before the separately bounded final report write. Missing/failed finalization is unqualified. Output accounting includes current result-directory files, including prior kernel evidence during the checker, plus current private child stdout/stderr. Published copies and retained current raw logs both count. A report allowance is reserved before success and its actual serialized size is checked.

The guardian retains its best-effort failure emission and unconditional child cleanup, including SIGTERM handling and ignoring further SIGTERM during cleanup. Supervision remains sampled userspace management of reviewed subprocess-free scientific code, not hostile-code containment or an OS-enforced instantaneous cap. Transient peaks/short-lived or escaped processes, guardian-loss and identity/signaling races remain limitations. The stated sample interval is nominal; actual request gaps are reported. Executable pins do not pin every loaded library. A private-log path substitution is not a complete privacy review. No runtime result is implied by source preservation.

## Initial reading inventory

Two inherited content files have been read, within the sixteen-file cap. No package/source/review `AGENTS.md` existed at the checked new paths; the previously checked common ancestors had none. Original content identities:

| Inherited path relative to repository | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-current-pair-2026-10-17/source/supervise.py` | 11235 | `1c9f61f2e42cace199ca5ce80eaeae5f124562a63d2bb620529ce060b457a87f` |
| `research/m31-current-pair-2026-10-17/source/guardian.py` | 1656 | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |

Initial new-package source/document identities, excluding this authored report:

| Path relative to this package | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL-DRAFT.md` | 9968 | `02a2a72ec90a4a99206db5d6e047612896edb6bcf07047ff108a08115d62bddd` |
| `prefreeze/inherited-supervision/supervise.py` | 11235 | `1c9f61f2e42cace199ca5ce80eaeae5f124562a63d2bb620529ce060b457a87f` |
| `prefreeze/inherited-supervision/guardian.py` | 1656 | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |
| `source/supervise.py` (mandatory list pending) | 11244 | `66e291203318da25f7d7cd88104835cd9100e8eebdbc82a7a6a08553c90c29fa` |
| `source/guardian.py` | 1656 | `fe8940e154ffdea296c13fbfe14848977c2bf950789aa20e9bf28affb58084c8` |

## Addendum 1 — declared allocation and interface decisions

The new spec and result contract have now been read in full. Their prospective allocation is 19 scenes: 11 labeled admitted, six labeled rejected, and two labeled stress-unresolved. Those labels declare intended coverage; the independent checker must establish the actual exact branch/certificate facts rather than trust the labels. The fixed sizes give 2,632 planned nonself rotor/source pairs in total:

| Scene | Drones | Planned pairs |
|---|---:|---:|
| solo | 1 | 0 |
| far-pair | 2 | 8 |
| aligned-pair | 2 | 8 |
| stack-4 | 4 | 48 |
| stack-8 | 8 | 224 |
| stack-16 | 16 | 960 |
| two-columns-8 | 8 | 224 |
| tilted-4 | 4 | 48 |
| asymmetric-4 | 4 | 48 |
| asymmetric-permuted-4 | 4 | 48 |
| near-rejection | 2 | 8 |
| invalid-isolated | 1 | 0 |
| invalid-global-pair | 2 | 8 |
| scaled-cap | 2 | 8 |
| tiny-force | 2 | 8 |
| huge-force | 2 | 8 |
| center-range | 2 | 8 |
| upward-order | 2 | 8 |
| staggered-16 | 16 | 960 |

The case declaration contains literal raw-state strings, stable IDs in 0..65535 and explicit input order. There are no random draws or target arrays. The two asymmetric scenes retain the same ID/state associations in a different array order. This tests stable identity and coverage; it does not make native summation order or candidate proposals invariant. The 16-drone maximum and 960 pairs per scene cannot empirically cover the two-million positive-term threshold. No uniform, exhaustive or statistical coverage claim follows.

The contract resolves the initial preparation question: it retains a preparation record for every input drone, even when one is invalid; a global preparation failure has `plannedPairs=4*N*(N-1)`, `observedPairs=0`, empty pairs and `stopReason=global-preparation`. Otherwise all nonself pairs remain in input receiver/rotor/source order, including rejected and unresolved outcomes. Positive terms are counted by `result.status=positive`, not by a positive interval lower endpoint. They must be interpreted with admission status: unresolved/refused scenes do not acquire a complete admitted count by omitting their failures.

The tolerance is the exact rational `1/100000000`, not its binary64 conversion. The four categories are rotor, collective, worldForce and worldMoment; the declared comparison is integer `upper*100000000 <= S` with `S=2^96`. Candidate proposals are untrusted dyadics in `(0,1]`; their native 48-iteration/54-bisection recipe is pinned as source but is not independently rerun as native arithmetic. The checker must instead verify the recorded candidate's domain, exact rational load identities, complete row/defect enclosures, corollary factors, returned root/load boxes and independently certified reference containment. This is the appropriate separation between proposal generation and proof checking.

The certificate contract requires error bounds for the full returned load boxes relative to the exact recorded candidate loads, all three vector components and exact scene maxima. A reference alone is not enough if the returned certificate box is wider. Tolerance achievement and verification are separate; neither a stress refusal nor a sound but loose/tolerance-failed certificate may be represented as an admitted result meeting the requested error target.

Only `tiny-force:pair-normalizer` and `huge-force:pair-unresolved-range` are permitted stress refusals. The independent huge-force target can prove a cap rejection while the candidate reports range uncertainty; both statuses must remain visible. The exception cannot authorize an internal invalid-input error or false zero/rejection. Nine prospective negative controls are named, with first-in-spec-order independent witnesses for affected-root and nonzero-error probes. Missing witnesses fail control coverage. All controls must exercise the core validator independently of journal equality. Actual implementation of these rules remains pending source inspection.

The mandatory supervisor list is now settled: `PROTOCOL.md`, `MODEL.md`, `runtime-pins.json`, and `source/{spec.json,result-contract.json,interval.cjs,rational.cjs,adapter.cjs,pair.cjs,coupled.cjs,run.cjs,check.py,pair-reference.py,guardian.py,supervise.py}`. The independent pair helper must be pinned before the checker loads it; copying its definitions does not authorize rerunning the closed 322-case suite or its controls. Adding `coupled.cjs` and `pair-reference.py` changes the final supervisor identity to 11,292 bytes, SHA-256 `8cc277688ee4339f5b520acdd23894a2393db89e7c2335ce1ed391bd578ae52e`; the guardian remains 1,656 bytes, SHA-256 `fe8940e154ffdea296c13fbfe14848977c2bf950789aa20e9bf28affb58084c8`.

The 32 MiB budget is aggregate stage accounting, including prior kernel result-directory files during the checker and current private logs, with the final 64 KiB report allowance. A checker file-size allowance by itself cannot override that aggregate budget. No output-size or timing success has been measured. The exact final source inventory will be added after completed candidate/checker/protocol review; the inherited reading count is still two.

## Addendum 2 — prospective case refinement and reused byte identities

The parent amended only the four `tilted-4` records before any numerical execution: quaternion w changes from `.99498743710662` to `.99498743711662`, and each drone's four nominal forces become `.02,.04,.08,.16`. All scene IDs, sizes, other records, 19-scene count and 2,632 planned-pair count remain unchanged. This is a prospective near-unit/asymmetric-load probe; its name and selected literals do not themselves establish preparation acceptance or a nonzero error witness. Those facts remain for the independent exact checker. The original spec is retained in prefreeze evidence and in the reviewer's initial snapshot.

The initially read spec was 36,010 bytes, SHA-256 `21c59dedcc96984171baaa2c54af6e44e91dc9de1ad6e0cf3321c612be990004`; the amended spec has SHA-256 `a718c20358161fd12bbd24e8939a8859f36fd2982676c577846f4a10582c2afc`. The initially read contract was 4,786 bytes, SHA-256 `2158742782abbc0adc4d1aad7a653d6ad9a12ad7f6adc83f33681dfbc061e7f8`. These identities record source reads, not runtime observations.

The five reused files in the new package were hashed and match their previously reviewed source identities: `interval.cjs` `73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3`; `rational.cjs` `de2adde5459d37cc537709f7a488605d9c21d8eedf022efc0a3e9461d4d97333`; `adapter.cjs` `5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145`; `pair.cjs` `e9fb2f4d7e4d1da09f53c082cf09a3b01c906a9d77642ae333319118b2f568cc`; `pair-reference.py` `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0`. This cycle does not rerun their earlier suites or reevaluate their constants. New checker loading, helper selection, scene membership and source gates still require inspection. The new moment output must use all three components of the actual prepared offset-cross-axis map; inherited body roll/pitch reasoning does not establish zero world-z moment or exactly unit axes.

## Final addendum — source review and disposition

**Final disposition: no remaining blocking static issue is identified in this review's allocation, protocol, supervision, complete-status handling, tolerance/verification distinction or checker-control scope for the exact final snapshot below.** The final protocol/model decisions and prospective finite allocation are approved within that scope. This is a source-only conclusion; it is not a successful numerical result, performance/cap/cleanup test, remote publication receipt or independent proof of the reviewer's own supervision edits. The mathematical reviewer remains responsible for the inherited corollary and signed-load extension. Final source publication and independent exact-commit byte verification remain prerequisites to the sole kernel/checker stages.

### Findings and pre-execution resolutions

1. **Inherited guardian deadline:** retaining 130 seconds would have truncated the new 180-second stage. Both fallback loops now use 190 seconds; the supervisor's live and final limits remain 180 seconds. The original supervisor/guardian bytes were preserved before any change.
2. **Preparation and durability semantics:** the final contract separates planned pairs from observed enumeration and global-preparation stops, retaining every drone's preparation record. Once globally prepared, the source enumerates every nonself pair before applying refusal priority. The runner appends and fsyncs each completed scene. Its current scene remains in memory until completion; the protocol now explicitly disclaims per-pair crash durability. An interruption retains earlier completed scenes and supervisor/error logs. The individual `fs.writeSync` calls still lack an explicit short-write loop; journal/final equality must fail on malformed or incomplete evidence. No storage-durability behavior was tested.
3. **Nonempty domain:** the mathematical review prompted an explicit `N<1` guard. The original 7,398-byte `coupled.cjs`, SHA-256 `1621b5e6e89a8e419c7644143ae4f193c0331f97bc9b3537c6266fcccf8d7668`, was retained; the only inspected source delta adds the nonempty-domain check. No declared scene is empty, so the guard's presence is not a finite-case coverage claim.
4. **Wall-boundary wording:** the final protocol explicitly includes launch, sampling, cleanup, log publication, output hashing and identity rechecks in 180 seconds, ending before the separately bounded 64 KiB report write. Missing/failed finalization is unqualified. This resolves the initial ambiguity in an unqualified total-wall-time phrase.
5. **Independent-helper executed-source identity:** the first complete checker used `importlib` loader execution, which could accept a timestamp/size-valid bytecode cache outside the source pins. This reviewer identified that gap. The final loader reads one bounded source buffer, requires its exact indexed byte length and SHA-256 plus the immutable original helper digest, and compiles/executes that same buffer into a fresh module only after all local manifest entries are verified. It therefore does not consume an unpinned `__pycache__` artifact. This is future authorized-run code; no helper was loaded during review. The original 52,178-byte checker draft, SHA-256 `ade02e36987f1cdb07c121df5210d7c7f22e324aad776cb1c7ef3f3911a8e0f6`, and the 52,471-byte loader-only correction, SHA-256 `0f8158b2b3f897182bfeb8d92ee7612774ff92f6e7c4815862e9f8ba2b531842`, are preserved as source history.
6. **Stress exception too broad inside a scene:** initially, scene-ID/branch permission could let another ordinary pair in `tiny-force` become `unresolved/normalizer` without failing verification. That contradicted the promise that a stress refusal would not mask another pair error. The final contract and checker require exact pair identities: only `(i=0,r=0,j=1,normalizer)` in `tiny-force`, and `(i=0,r=0..3,j=1,unresolved-range)` in `huge-force`. Other pairs must match the independent oracle. The original oracle-compatibility condition is retained, so an exact early zero/preparation/geometry branch cannot be replaced by a stress refusal. The final protocol honestly states that this bounded exception retains unqualification and does not independently prove the internal reason for a refusal. No new numerical control or case was added to make this correction.

### Candidate and checker evidence rules inspected

The complete new candidate and runner source were inspected, as was the complete first checker draft and its two correction deltas. The candidate validates bounded unique stable IDs and all raw/prepared states before identity exclusion. Its `(receiver,rotor,source)` enumeration is exhaustive for the declared input order; it does not stop at a pair refusal. It chooses first proved pair rejection, then first unresolved pair, then positive-edge ordering failure, then positive-term resource rejection. Positive statuses count regardless of coefficient lower endpoint. It constructs rows only after complete admission. Neither nominal expected-class labels nor input-array positions replace exact admission or stable ordering.

The candidate uses fixed 48 synchronous native iterations and 54 bisections as an untrusted proposal. It records exact candidate bits, then rebuilds proof weights and loads using rational/directed arithmetic. The source does not replace exact nominal totals/weights with native values in the certificate. It uses actual prepared axes and separately prepared offsets, with all three cross-product/world-moment components and exact rational candidate-load identities. Its tolerance decision is the declared integer comparison. The runner writes the final document exclusively after all 19 scene records and completion are journaled.

The independent checker verifies bounded canonical manifest entries before loading the exact pinned helper source buffer. It regenerates only the new scenes; it never calls the old 322-case generator, old main or old controls. It verifies constant encodings, all raw input bits, all prepared fields, stable IDs/order and planned counts from the frozen declarations. It independently derives scene/reference outcomes and reports prospective class agreement; ordinary class disagreement fails verification. Stress/reference differences remain explicit. Candidate source hash reports are matched to the verified source inventory. The inventory is verified again after reference/control work; the supervisor separately preserves publication-chain and prior-kernel evidence identities before/after.

Every saved pair is checked even when another pair rejects or leaves the scene unresolved. Pair errors are accumulated through the entire pair list before the scene fails. Exact zero results, positive reference containment, K/scaledK caps and positive normalizer lower bounds are independently enforced. All pair identity/order and coverage counters are exact. Global-preparation failure permits no pair rows and no solve/certificate payload. Non-admitted scenes retain the first-priority witness and have no solve/certificate payload. No unresolved pair is silently assigned coefficient zero.

For admitted scenes, the checker builds complete rows from independently validated coefficients and candidate-derived exact weights. It checks that saved row sums contain the complete contraction, defects contain the recorded candidate's polynomial value, defect lower bounds are positive, kbar/Kbar satisfy the declared inequalities, and returned root intervals contain both the corollary bounds and independent topological reference roots. Fixed192 coefficient/source enclosures and fixed128-step exact rational cubic bisections bound denominator growth without adaptive refinement. Zero alpha returns root 1 exactly; an exact rational root discovered by comparison is retained. The checker does not rerun the native proposal to create an accuracy premise.

Every candidate rotor/collective/world force/world moment load is checked as a canonical exact rational identity from the recorded candidate. Every returned load box must contain the signed map of the full returned root box and the independent model-load reference. Normalized scalar errors cover the entire returned scalar boxes; vector errors cover all three coordinate extrema using exact squared inequalities against the positive normalization. The scene maxima dominate all per-drone error uppers. This checks a sound error bound on the claimed certificate box, not merely agreement at one reference point.

Verification, resolved-outcome accounting, model admission and tolerance remain separate. `qualifiedRecords` includes correctly verified rejected outcomes; it is not the number of usable load certificates. `admittedRecords` counts admitted models, and `tolerancePassedRecords`/`toleranceFailedRecords` distinguish their error-target achievement. A sound tolerance-failed certificate may still verify. The two explicitly refused stress scenes remain unqualified when those refusals occur. Neither `verificationPassed` nor a correctly verified domain rejection means that all 19 scenes admit a physical/model load solution.

The journal gate requires exactly 21 lines: exact header, 19 scene rows equal to the final result rows, and exact completion count. It is bounded and rejects duplicate JSON keys/nonfinite numeric tokens, malformed or missing evidence. The numerical validator used for baseline and every control does not consult the journal. Final verification requires the baseline, journal and all nine controls. An ineffective/missing control, missing witness, failed source recheck or report-write failure cannot produce a passing checker exit. The checker file budget remains subordinate to the supervisor's aggregate 32 MiB accounting.

### Numerical-control relevance

| Control | Why the corruption is wrong and how the witness is selected |
|---|---|
| missing-positive-pair | Removes the first independently positive interaction in frozen scene/pair order; exact membership/count/order must change. |
| false-root-one | Replaces a root enclosure by `[1,1]` for the first admitted rotor whose independent reference upper endpoint is strictly below 1. |
| altered-candidate | Flips one candidate bit while retaining old exact candidate-load identities. Positive nominal force makes a changed finite candidate alter its exact load; an invalid candidate also fails the domain gate. |
| false-error-zero | Selects the first admitted rotor whose exact candidate lies strictly outside the independent root interval, records the positive separating gap and strict normalized error lower bound, then sets its error upper to zero. A positive loose certificate width alone is not used as proof. |
| altered-lever-arm | Flips a supplied prepared offset bit, violating exact independently reconstructed preparation evidence. |
| altered-stable-id | Replaces a positive nonself pair's source ID by its receiver ID, violating the frozen nonself membership/order. |
| missing-scene | Removes the last required scene. |
| duplicate-scene | Replaces the second scene by a duplicate of the first. |
| reordered-scenes | Exchanges the distinct first two scenes. |

Each mutation is applied to an in-memory copy and sent through the same core validator as baseline. The original saved document remains the baseline; journal mismatch alone cannot satisfy any control. The positive/root/error witnesses are independently derived and retained in the report. A valid baseline and all required witnesses must exist before controls can pass. This is inspection of meaningful control design; none of the nine controls was executed by this reviewer.

### Exact final inventory and retained limits

The fresh-cycle inherited content count is **two files**, within the cap of sixteen. The new-package inventory below contains sixteen active source/document paths plus the two preserved original supervision copies. Reused arithmetic/pair/helper byte identities were checked against the previously reviewed identities; this cycle did not rerun their closed suites. The authored review itself is excluded from that inventory. No source manifest, source-publication receipt, scientific result, runtime executable byte content, remote source or viewer implementation was read by this reviewer. The runtime-pin JSON was read only as a declaration. No scientific code was imported, evaluated or executed; metadata-only file hashing/copying is not a numerical allocation.

| Final path relative to this package | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL-DRAFT.md` | 9968 | `02a2a72ec90a4a99206db5d6e047612896edb6bcf07047ff108a08115d62bddd` |
| `PROTOCOL.md` | 12710 | `b1c5293cdaead63c2a74387fcf63754ff2b16fe73029e655fa80240cce6018ba` |
| `MODEL.md` | 3295 | `70a267c26c142d2cccde4e8530f1be3fa619c3301964878d244d6dca8f8070c6` |
| `runtime-pins.json` | 248 | `842b2522133ed499f4706e071b09f3d100c5f4ed3f41d0fd135736c4dc191087` |
| `source/spec.json` | 35930 | `a718c20358161fd12bbd24e8939a8859f36fd2982676c577846f4a10582c2afc` |
| `source/result-contract.json` | 5372 | `69bf30351d34d73c69960679daed08eae6a6a75d5288ba3f7137017ceafb026f` |
| `source/interval.cjs` | 2815 | `73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3` |
| `source/rational.cjs` | 1188 | `de2adde5459d37cc537709f7a488605d9c21d8eedf022efc0a3e9461d4d97333` |
| `source/adapter.cjs` | 2400 | `5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145` |
| `source/pair.cjs` | 3579 | `e9fb2f4d7e4d1da09f53c082cf09a3b01c906a9d77642ae333319118b2f568cc` |
| `source/coupled.cjs` | 7421 | `898d6b154d7a7c683a5ecc182280ff5c56d8a94526e3038c1da38b125c5a0ae9` |
| `source/run.cjs` | 1413 | `2a3bf9f62ed2e296a4dd592f70a50430e17baad71c81396d1c04f4a0d4aa6004` |
| `source/check.py` | 52997 | `dd3675f60d12f347ab550f1588c31da54ba57f065b20a727120711bf144e6fd4` |
| `source/pair-reference.py` | 44757 | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
| `source/guardian.py` | 1656 | `fe8940e154ffdea296c13fbfe14848977c2bf950789aa20e9bf28affb58084c8` |
| `source/supervise.py` | 11292 | `8cc277688ee4339f5b520acdd23894a2393db89e7c2335ce1ed391bd578ae52e` |
| `prefreeze/inherited-supervision/supervise.py` | 11235 | `1c9f61f2e42cace199ca5ce80eaeae5f124562a63d2bb620529ce060b457a87f` |
| `prefreeze/inherited-supervision/guardian.py` | 1656 | `a015e8dd42b31f6f630cf651ae2d741dc33d410aa3e2649fb0a844d2e036e3cf` |

Finite static scenes and control design do not prove all-input correctness, threshold overflow behavior, physical accuracy, dynamics/flight safety, browser scientific equivalence, scalability or novelty. Sampled supervision, executable-only environment pins and scene-granularity durability retain their stated limitations. Publication/privacy/evidence audits, exact-commit remote verification and any actual numerical pass remain separate pending work. The original full-scale accuracy–computation goal remains incomplete.
