# Static failure disposition: runtime-qualified body-load replication

## Disposition

The single science invocation is terminal and scientifically unqualified. Runtime admission and pipeline creation passed, but the first GPU control batch did not persist its required output. The complete field-to-body numerical question remains unanswered: no main family was generated or evaluated, and no saved GPU output is available for an accuracy comparison. Preserve the failed invocation and all partial evidence. Do not retry it, complete its omitted stages, or launch an automatic third runtime campaign.

This memo uses saved JSON, frozen source text, file metadata, and byte hashes only. It does not execute the browser, transport, runtime helper, scientific modules, generator, shader, or any numerical reference, and it does not decode scientific binaries. The separately allocated saved-only review has not been executed for this memo; its source, lifecycle, and freeze require independent clearance before its one permitted invocation.

## What the retained evidence establishes

The saved source commit is `f12d8c836e7b991ec33e6de662d00ed05dcce33e`. The local 12,606-byte source freeze has SHA-256 `c0c6b2fda84567a76025b2e5f06832cbc1dd5811c23a246df5623f46baf8f8a9`; all 57 frozen local pins still match. All files listed by the terminal result also match their saved sizes and hashes. The raw and results copies of `result.json` are byte-identical.

The saved runtime receipts report successful checks of the six named Chrome files before and after launch, and the actual browser version is `155.0.8059.80`. The capability record reports a nonfallback Apple/Metal adapter, the admitted default device limits, three compiled pipelines, no compilation messages, and no pipeline/validation/device-loss error at admission. This establishes the recorded admission outcome for this invocation; it does not pin every browser resource, operating-system component, or GPU driver.

The CPU control reference and host-only control records were saved. The worker reports one control construction, one control-reference call, one host-only call, 13 host admission controls, and 16 decoder controls. Its result contains 6,848 checks, but that count is not a count of successful GPU accuracy comparisons. The reference-status JSON reports completion/pass for its CPU work; this memo does not independently recompute that work.

`raw/controls-pairs-gpu-api.json` records the first control batch as `controlPairs`, count 15, one workgroup, `submitted:true`, 15 active invocations, and 64 launched lanes. Four buffers totaling 11,648 bytes were created; 3,968 bytes were uploaded. The required output was 3,840 bytes. Its readback entry remains `persisted:false`, the batch remains `completed:false`, and its nested error is `TypeError: Failed to fetch`.

The driver saved that API record and then rejected the unmet persistence premise. This explains the distinct top-level error in `results/result.json`: `Complete persisted raw readback`, in context `GPU controls-pairs`, with expected output size 3,840 and completion false. The sink's final reservation reports `started:false`, `complete:false`, zero active writes, and closed status. The required `controls-pairs-gpu-output.u32` file does not exist.

The frozen source increments `readbackBytes` only after a successful sink response and completion receipt. Its recorded value of zero therefore means no completed persisted readback was credited; it does not establish that GPU mapping or computation never occurred. The inspected browser control flow places the sink fetch after mapping and obtaining a mapped view, but it retains no output values that this memo could inspect. Submission and successful pipeline compilation are not substitutes for a saved numerical result.

The remaining GPU root control batch, handoff/control assessment, and all four main families were not reached. `cases` is empty, and there is no main-family or saved GPU output evidence. No claim about numerical agreement, numerical disagreement, or complete-query feasibility can be drawn from this failure.

## Attribution boundary

The supported classification is a browser-to-evidence persistence failure during the first GPU control batch. The nested fetch error and the unstarted expected POST reservation locate the failed contract boundary. They do not identify its transport cause.

The retained records do not contain a network request-failure reason, HTTP request/response trace, accepted POST, preflight transcript, or an independent transport diagnosis. The source contains an OPTIONS handler and response headers, but source configuration is not an observation of an actual request or browser policy decision. In particular, the evidence does not establish CORS, a Chrome-version policy change, a sink implementation defect, a GPU/driver defect, or any other specific network cause. No such attribution should be added to the result title, chart, or milestone narrative.

No browser rerun, curl/fetch probe, server probe, environment change, or transport rehearsal is authorized as part of this static disposition. Further causal diagnosis would require a separately justified and bounded plan after the current terminal record is closed; this memo grants no such invocation or budget.

## Cleanup and accounting

The saved batch API report has `validation:null`, no cleanup errors, all four buffers destroyed, and zero live tracked buffer bytes. Worker shutdown reports the device destroyed. The observer reports complete registry/group/pipe closure, one detached browser group confirmed absent, no group kill signals, no cleanup error, and zero RSS-probe errors. The caller reports no direct-observer kill. These are retained cleanup observations; they do not convert the failed work into a passing lifecycle candidate.

Actual Node, relay, observer, and caller exits are all 1. `publication/science-capture-execution.json` records the completed caller tool observation and binds its exact 493-byte final summary. The caller measured the full observer interval as approximately 2.053942167 seconds. The observer recorded 34 RSS samples and a peak of 1,143,390,208 bytes. These diagnostics are within the recorded limits and provide no timing advantage or performance claim.

Raw evidence comprises 22 files and 127,681 bytes. The final results directory comprises seven files and 13,661 bytes. Its count must be interpreted at the correct phase: the observer's terminal scan preceded its own budget and the later caller receipt. That earlier results snapshot was five files and 8,711 bytes. Adding 3,548 private science-diagnostic bytes, the 2,763-byte budget, and the 723-byte observer summary gives the inner accounted total of 15,745 bytes. The caller adds its 60-byte permanent capture lock, zero retained observer stderr, its 2,187-byte receipt, and its 493-byte final summary, producing 18,485 combined bytes. The observer summary retained privately is counted once. Publication copies/metadata created afterward belong to the later publication phase and must not be silently compared with the earlier scan as though they already existed.

Both final accounting flags are true, but both candidate success flags and all scientific/whole-lifecycle qualification flags remain false. The failure is the expected consequence of the nonzero worker/relay exits, not evidence of a timeout or incomplete process closure. A saved-only reviewer must preserve these distinctions and model the phase boundaries rather than treating successful failure capture as scientific qualification.

## Next decision

Use the one separately prepared 120-second saved-only review to audit retained hashes, shapes, direct consistency, the failed decision, and the lifecycle/capture chain. It must not generate inputs, solve reference roots, evaluate a wake, execute GPU work, repair the sink, or fill missing outputs. Its own source review, immutable freeze, deadline/output enforcement, and actual external completion are required before any integrity claim.

After that terminal review, publish the additive failed checkpoint with its exact source/result provenance, this limited attribution, the retained partial controls, cleanup/accounting records, and an actual-data view that visibly distinguishes saved CPU fixtures from unavailable GPU/main-family results. Preserve the earlier browser-version failure as a separate terminal campaign. Any later research proposal must be prospective, separately scrutinized, explicitly allocated, and compliant with the original launch cutoff; no remaining time or failed attempt is refunded.

The present evidence supports no physical-validation, flight-accuracy, speed, real-time, portability, or novelty claim. It also supplies no numerical counterexample to the declared body-output accuracy gates, because the necessary GPU output was not retained.

## Key evidence identities

Paths below are relative to this campaign.

| File | Bytes | SHA-256 |
|---|---:|---|
| `results/result.json` | 7659 | `a6a03d917e23fb7172f9c036441b0c05e9d92381f79803dbe1099bdf3d827acf` |
| `raw/controls-pairs-gpu-api.json` | 2093 | `3a7aecec9fcf82e0775776f89b7bb5d66010533a5d4f7539c4d7028c1f18032f` |
| `results/budget.json` | 2763 | `86ad50511f1f459a5bbc00980f399dd6f5f04259a71237aeece01321a7b672fc` |
| `results/capture.json` | 2187 | `94b7b9c05a0257922e68c360f8b54d2187c06469614410c56cd64a55bc790955` |
| `publication/science-capture-output.json` | 493 | `ea7f6a1c1471fb0bcc9285a93949fb3722079d5636532e477a80c312efdfc19a` |
| `publication/science-capture-execution.json` | 1016 | `64946543e2e8660e7ce9b57e7f2d7c9f0e9032c66d4f2bfe8396630425c939ed` |
