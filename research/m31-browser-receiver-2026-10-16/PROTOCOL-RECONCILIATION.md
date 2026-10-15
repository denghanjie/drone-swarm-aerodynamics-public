# Receiver f32 final-draft protocol reconciliation

2026-10-16. Static source/config/schema review only. No scientific import, input decoding, root evaluation, shader compile, browser launch, field or benchmark was performed. Source hashing and an administrative UTC-clock read were the only checks beyond text inspection. No repository file was edited.

**Disposition:** the numerical question, revised accounting and claim scope reconcile. Resolve the remaining metadata/evidence-preservation items below before freezing. This is not a scientific pass or launch authorization. Final freeze/publication verification remains a separate prerequisite.

## Resolved design points

The earlier design challenge's three dispatches and 72,096 new host solves are **obsolete**. The final design reuses 24,000 original R64 roots from the closed independent-I evidence, solves only 32 new scalar R roots, and adds five invalid raw-word guard controls. The revised matrix is:

| Batch | Valid GPU roots | Invalid guards | Workgroups × 64 | New host bisections |
|---|---:|---:|---:|---:|
| scalar32 | 32 | 0 | 1 × 64 | 32 R + 32 Q + 32 A = 96 |
| invalid5 | 0 | 5 | 1 × 64 | 0 |
| fresh1000, exposed reuse | 4,000 | 0 | 63 × 64 | 8,000 Q/A |
| fresh5000, exposed reuse | 20,000 | 0 | 313 × 64 | 40,000 Q/A |
| Complete success | 24,032 | 5 | 378 × 64 = 24,192 | 48,096 |

Thus there are 24,037 input records and 155 inactive padded lanes. GPU Newton reservation is 288,384 updates; host bisection reservation is 4,617,216 iterations. Field and integration reservations are zero. The largest batch's 320,000-byte input and two 640,000-byte output/readback buffers total 1,600,000 GPU buffer bytes. The 32 MiB evidence cap, 2 MiB failure reserve, 180 s external wall cap, 175 s cooperative guard and independent 30 s initialization/batch deadlines are new limits. They do not reopen R8 or a previous campaign.

The selected controls are now correctly distinguished: Q uses the exact decoded Uq/viq quotient; A receives returned alpha directly; old R is reused rather than recomputed. The source uses independent alpha-parameterized bisection with [0,1], 96 steps maximum and strict binary64 reference checks. The separate f0/vi packing, final product term and signed telescoping decomposition are explicit. The positive-alpha admission bound 2^-120 supplies substantial normal/finite margin for the initial reciprocal; it is correctly not described as qualification of every positive real U in [0,128].

The four gate operands are unambiguous: delivered G/R force error ≤1e-7 N; G/A x error ≤1e-6; host cubic residual at returned alpha ≤2e-6; represented power ratio at Uq/viq ≤2e-6. The last gate includes division error. Original and represented x/residual diagnostics remain distinct from gates. Original-rho/area power deviation and the old 1e-12 N rotor comparison are retained without being relabeled as the new qualification. The power convention and finite component-only claim address the prior challenge.

## Remaining protocol/source reconciliation items

**1. Complete host validation of the stated termination metadata.** In `compareRecord`, code 2 currently requires twelve iterations but does not require `finalAbsStep >= Math.fround(1e-15)`. The protocol defines code 2 as twelve updates *without* the strict step threshold. Add that converse consistency check. For positive U, require returned alpha strictly positive as the shader does, rather than accepting alpha=0 under the generic nonnegative check. These checks do not introduce a new scientific method or tolerance; they verify the frozen output contract. Code 2 may still pass all accuracy gates.

Also clarify the protocol's compact update sentence: compute `step=abs(next-oldX)` before assigning the updated x, then test the saved step. The shader already does this correctly; wording that says “assign updated x; break if abs(next-x)” is ambiguous when read literally.

**2. Preserve already available GPU bytes on API-check failure.** `dispatchReceiver` copies mapped output into `returned`, unmaps, then awaits/checks `popErrorScope`, device loss and uncaptured error. If one of those checks fails, it throws and discards `returned`; the driver cannot write the raw bytes it already obtained. This falls short of the protocol's available-output retention rule. Return a structured failure containing available raw words/count and API diagnostics, or attach them to a serializable failure result. The driver should persist those words before declaring failure and must not evaluate roots or qualify the batch after the API failure. No extra dispatch is needed.

**3. Retain partial initialization diagnostics and distinguish failure classes.** If `createComputePipelineAsync` rejects, or requestDevice/compilation/error-scope handling rejects after metadata has been gathered, initialization currently throws without returning the collected adapter fields/compiler messages. The driver's terminal message alone does not preserve that evidence. Return or persist a structured initialization result covering its reached phase, adapter metadata, messages, pipeline error, loss and uncaptured-error state. Capability absence remains unsupported; compile/API failure remains failed. Neither can be retried. This was an explicit requirement in the earlier initial review and remains partly unresolved.

**4. Make failure accounting labels precise.** The driver increments `counts.dispatches` before the page operation, as required by attempt reservation. A failure before `queue.submit` can therefore record a dispatch count without an actual submission. Call this an attempted/reserved dispatch count on failure, and separately record submission/completion where available, or state that distinction in schema and reports. All four counts coincide on complete success, so the success reservation arithmetic above is unaffected. The API evidence note's submitted-dispatch wording should not conflict with this attempted-work policy.

## Freeze/provenance prerequisites

The inspected directory did not yet contain `freeze.json`; the driver correctly expects it before execution. The final freeze must include all consumed source/config/schema/constant encodings, the two I matrices, two source-audit streams, viewer pose sources, parent manifest/source provenance and saved independent review. Pin Node/Playwright resolution and the intended Chrome launch environment, while reporting the actual browser/adapter metadata during the sole attempt. A syntactically valid source-commit environment variable is not itself source publication verification.

The preserved original reference construction matches the independent-I source's `area=Math.PI*r*r`, not merely a decimal approximation. Existing R brackets, matrix/audit force equality and equations are checked without solving roots. The new original-reference rows synthesize F0/VI from those pinned expressions; do not describe them as separately stored original constant fields. The frozen audit/source provenance makes that reconstruction reviewable. The static constant-encoding file is an assertion to check at runtime; this review did not recompute its numeric encodings.

The driver hashes the served shader against disk before dispatch, but does not similarly reconcile the served browser.js/HTML. The localhost server is external to this runner. Final preparation should establish that it serves the frozen root and verify the served host module/HTML, or record an equivalent controlled-serving guarantee. A stale host module can change capability checks or transport while serving the same shader. This is a source-integrity prerequisite, not a request for a test dispatch or browser preview.

The API-evidence note requests actual-device limit metadata; browser.js currently records adapter limits only. The selected buffers/workgroup fit ordinary baseline WebGPU limits, and later pipeline/validation checks remain required, but record/check the relevant actual device limits to reconcile that documentation. Do not infer an unexposed hardware/backend identity. Intentional device destruction during cleanup must remain distinguishable from unexpected loss before evidence completion.

The root/field claims are appropriately narrow: one recorded environment, exposed numerical inflows, 32 fixed probes, five guards, fixed uploaded nominal/induced constants, one literal source-expression translation with allowed WGSL arithmetic behavior. No timing, arbitrary-parameter receiver API, wake/geometry/summation, body/world GPU load assembly, dynamics, physical adequacy or 5,000-drone coupled simulation is qualified. Keep the earlier design challenge in the history with its accounting clearly superseded rather than silently rewriting it as the final protocol.

## Inspected snapshot hashes

All paths below are under `<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16`.

| File | SHA-256 |
|---|---|
| PROTOCOL.md | 70bc96b01e3688a98cd1da5afce7bb7e0d26cea5f5c0037dd597139848128d2c |
| config.json | 40d9ac60a1bc2b031999fd079866db3865039b2067fe960e453c2b58efb216ae |
| schema.json | 9a8d8d440360c3c19f48a28eea5e58cc9535e47e947bc850994db1477747964b |
| source/receiver.wgsl | dc64e23b3905d635f0d1de4d56233c2380455e89c2f50ee5a59c67baca6f1555 |
| source/browser.js | dcac798ef7410162cd96cd763a81d29a4f7ed06c46621478d4c9a4949631d829 |
| source/reference.cjs | 4628e2a3a4d843868810bea070153fe22798cfe3e73fd483492ca329558d497d |
| source/experiment.cjs | a8d014547092e72de60c63eec9f69c81475afe709c1ac1aa97155ddfd3e21ea1 |
| source/run-once.py | d880585cf565558186f61e834602cc96da131e8fcf6f77ff334c597c4e515b55 |
| constant-encoding.json | a3cab7f30b4490308464d1016bbe19539a8d197fb77076860f523c484c54005e |

Relevant inspected files: [protocol](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/PROTOCOL.md), [driver](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/source/experiment.cjs:19), [browser host](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/source/browser.js), [API evidence](<REPOSITORY_ROOT>/research/m31-browser-receiver-2026-10-16/API-EVIDENCE.md). Any correction changes this snapshot and needs static reconciliation before final source freeze; it does not consume a scientific attempt.
