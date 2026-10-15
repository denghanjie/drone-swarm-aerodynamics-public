# Receiver experiment: complete static follow-up review

Repository: <REPOSITORY_ROOT>
Campaign: research/m31-browser-receiver-2026-10-16
Review date: 2026-10-16

This is a static source/protocol review of the snapshot identified below. It supersedes no prior record and does not authorize execution. The original review at /tmp/m31-browser-receiver-static-review.md remains unchanged. No scientific module import, numerical root/field/geometry evaluation, saved input-matrix interpretation, input generation, shader parsing/compilation, browser/GPU launch, dispatch, benchmark or checker execution occurred in this follow-up. Operations were text reads, file listing, SHA256/byte inspection, declared-count arithmetic, and writing this note outside the repository. No repository files were edited.

Decision: do not launch this snapshot. The core representation/reference design resolves the earlier numerical-contract concerns, but four execution/provenance failure-path gaps remain. Fixes must be statically reviewed and included in the final source freeze.

## Blocking findings

### 1. A successful readback can be discarded before host persistence

Location: source/browser.js lines 32–35; source/experiment.cjs lines 46–47 and 62.

The browser copies mapped output into an ordinary Uint32Array-derived array and unmaps it, then awaits popErrorScope and throws on validation, loss or uncaptured errors. The driver receives words only after that await and these checks. Consequently, a successful mapped readback followed by an error is never written to *-gpu.u32. A hanging popErrorScope also causes the outer 30-second deadline to reject without retaining the already available readback. This contradicts the prospective protocol and preflight resolution that raw GPU words are persisted before dependent validation.

Required change: persist copied words immediately, before awaiting later API validation. A narrowly scoped host persistence callback or two-phase readback/persistence followed by bounded validation can meet this without another dispatch. Return or retain structured API outcomes and stop after their rejection. Merely returning words alongside an error instead of throwing addresses rejection but does not address a later promise that hangs. Preserve the single complete-batch deadline across both phases. Input/returned word counts and byte coverage should remain independently checked, with raw bytes available on failure.

### 2. GPU shutdown failure skips browser cleanup; the supervisor does not always reap remaining group members

Location: source/experiment.cjs line 90; source/run-once.py lines 14–21.

The GPU shutdown and browser.close calls share one try block. If shutdownReceiver rejects or its two-second wrapper times out, browser.close is skipped. The supervisor kills the process group only when waiting for the Node leader times out, or on an exception while that leader is still alive. On a normal leader exit it records terminal/closed without checking or terminating remaining group members. Thus the source does not establish the promised whole-process-group closure on every terminal path. This is a control-flow gap, not an observation that Chrome currently survives.

Required change: independently attempt both bounded cleanup steps, collect both failures, and make the supervisor perform final cleanup/confirmation of its owned process group even after the leader exits. Keep termination one-shot; do not retry initialization or dispatch. Qualification must fail if cleanup cannot be confirmed. Handle an already absent group as a successful cleanup condition rather than allowing ProcessLookupError to bypass the ledger.

### 3. Initialization failures can erase adapter and compilation diagnostics

Location: source/browser.js lines 10–18; source/experiment.cjs lines 76–80.

Compilation messages and adapter metadata are local values until initializeReceiver returns. createComputePipelineAsync rejection, popErrorScope rejection, or a later initialization timeout prevents capability.json from being written and loses the compilation diagnostics already obtained. The explicit shader-compilation-error branch returns messages but omits the fetched shader, so the driver also skips the served-shader identity comparison on that branch. The protocol says compilation is recorded and warnings retained; successful-path-only capture is insufficient for this sole attempt.

Required change: retain phase, exposed adapter information, actual served source identity and compilation messages as they become available, before a subsequent API await can fail or hang. Catch async-pipeline errors with their name/reason/message and preserve available scope/loss outcomes. Use structured terminal outcomes while preserving a separate unsupported status. This must not create a fallback adapter, additional request/compile, rescue or retry.

### 4. The executed browser runner is not bound to the frozen source

Location: source/experiment.cjs lines 69–70 and 75–77; source/browser.html module script; source/browser.js shader fetch.

The local freeze verifies files on disk, while page.goto loads browser.html and browser.js from an already running localhost server. Only the shader text is content-checked, and that check happens after initialization. A stale or wrong server root can serve a different browser.js whose ready flag and API names still match; the current driver would not establish which frozen runner actually executed the GPU API sequence. The local freeze alone does not bind HTTP-delivered JavaScript to those local files.

Required change: bind the actual document/runner bytes used by the page to the frozen inputs before initializeReceiver. A deterministic route serving frozen captured bytes, or equivalent verification of the actual loaded responses, can avoid stale-server ambiguity. Verify the shader before createShaderModule, not solely after successful initialization. Ensure the shader digest is checked against the frozen snapshot, not an independently reread mutable file. Keep the served HTML/module source in the freeze.

## Resolved numerical and accounting concerns

- The revised input struct stores u32 words. All-ones exponent and nonzero pad checks occur before input float bitcasts, so the frozen NaN/infinity guards do not first enter the floating-point domain. Runtime finiteFloat remains a bounded-experiment diagnostic, not a portable arbitrary exceptional-arithmetic certificate.
- Positive original inflows must remain positive after packing and satisfy Uq/viq >= 2^-120. The zero path is separately admitted. No clipping, filtering, alternate initialization or enlarged domain is introduced. This resolves the earlier reciprocal/subnormal concern for admitted inputs; it is not a claim over all real U in [0,128].
- The shader retains alpha=U/vi, min(1,1/alpha), the written Newton polynomial/derivative, strict 1e-15 threshold, at most 12 updates, and final f0*x. Source grouping is appropriately distinguished from actual compiler rounding/fusion behavior.
- R64 uses 24,000 previously saved I roots/brackets plus 32 new scalar roots. Q64 solves decoded-U/decoded-vi alpha and A64 solves returned shader alpha directly. The independent reference does not reconstruct vi from packed f0. The old root/field routines are not imported or re-solved by this driver.
- New reference records are charged before evaluation and Q/A results append separately before comparison. Qualification failures retain either a complete prefix or the thrown root detail. Saved original matrices/root audits are crosschecked by declared shape/order, matrix/audit force equality and equation/bracket diagnostics without re-solving.
- Root X and host residual gates use A/returned alpha. Represented power uses alphaQ and therefore includes shader division error. Original rho/area power is separately reported. The 1e-7 N total rotor gate is explicitly a new engineering target, while the older 1e-12 N count remains diagnostic. No physical or full-flock qualification is inferred.
- The signed decomposition includes packing, division, Newton result and final multiplication. Operands are retained for reconstruction; absolute component maxima are not presented as an additive signed decomposition. The stored power model and ideal-power limitation are explicit.
- Threshold/cap stop codes are metadata, not certification. Finite/range, exact zero identity, integer iteration/status, threshold and cap checks precede gate acceptance. Unexpected invalid sentinel/nonfinite output terminates. Numerical gate failures finish only that already scheduled batch's reference attribution, then prevent later batches.
- Outer initialization/batch deadlines fix the original readback-only timeout weakness. The external one-attempt lock and reservation are permanent; the cleanup gap above must still be closed.

Declared-count arithmetic agrees: 4 dispatches; 24,032 valid GPU roots plus 5 invalid guards; 288,384 maximum Newton update slots; 48,096 new host roots and 4,617,216 reserved bisection slots; zero field evaluations and integration steps. Workgroups 1+1+63+313=378 imply 24,192 lanes, with 155 inactive lanes beyond 24,037 records. Inputs total 384,592 bytes, GPU outputs 769,184 bytes; original rows plus Q/A streams bring the scientific binary payload to 4,998,896 bytes before JSON. The largest batch needs 320,000 input plus 640,000 output plus 640,000 readback bytes, totaling 1,600,000 GPU buffer bytes. These are static reservations, not measured runtime work or memory use.

## Nonblocking clarifications and release conditions

1. Unsupported currently has output.pass=false and output.status=unsupported while the process may exit zero. This is acceptable only if downstream qualification always reads the explicit scientific outcome; a zero supervisor exit means the process ended, not the full suite passed. Consider copying the terminal scientific status into the outer ledger.
2. The final receiverHealth page.evaluate has no local deadline. The 180-second supervisor still bounds the attempt; applying a short explicit health deadline would make the stated failure path easier to diagnose.
3. The u32 serialization helpers coerce with >>>0. The current browser path constructs every returned element from Uint32Array, which establishes exact uint32 provenance in the frozen intended implementation. Explicit integer/range validation before coercion would avoid silently normalizing a malformed transport result and would make the driver contract self-contained. Persist a malformed-return diagnostic rather than treating normalized words as the original return.
4. New-root qualification relies on the frozen solver to supply a finite/integer iteration count and finite bracket endpoints. Its source does so for the admitted arguments. Explicit validation could make that contract self-contained, but no additional root run is warranted.
5. The ordinary 2 MiB terminal reserve is ample for the fixed-size summaries visible here, but terminal file enumeration/hashing and JSON write errors are not themselves protected by a minimal fallback result. The supervisor's permanent terminal ledger must remain authoritative when a richer diagnostic cannot be written. Do not claim every failure necessarily yields result.json.
6. The final freeze/publication/independent-pin-verification step remains pending in the reviewed snapshot. It must include all executable sources (including HTML/module runner), config/schema/protocol, constant encodings, dependency identities, the reused I matrices/root audits and prior provenance required by the protocol. This review is not verification of a not-yet-created freeze.
7. Compilation diagnostics, source identity and loss/error handling must be recorded without claiming unavailable adapter/backend properties. An unsupported/failed/partial attempt cannot qualify the fixed suite. The separate saved-only review remains unspent and closed until its own authorization; no checker was prepared or run here.

## Reviewed snapshot identities

| File | Bytes | SHA256 |
|---|---:|---|
| source/experiment.cjs | 15201 | `a8d014547092e72de60c63eec9f69c81475afe709c1ac1aa97155ddfd3e21ea1` |
| source/browser.js | 4221 | `dcac798ef7410162cd96cd763a81d29a4f7ed06c46621478d4c9a4949631d829` |
| source/reference.cjs | 796 | `4628e2a3a4d843868810bea070153fe22798cfe3e73fd483492ca329558d497d` |
| source/receiver.wgsl | 3318 | `dc64e23b3905d635f0d1de4d56233c2380455e89c2f50ee5a59c67baca6f1555` |
| source/run-once.py | 2305 | `d880585cf565558186f61e834602cc96da131e8fcf6f77ff334c597c4e515b55` |
| config.json | 2311 | `40d9ac60a1bc2b031999fd079866db3865039b2067fe960e453c2b58efb216ae` |
| schema.json | 1218 | `9a8d8d440360c3c19f48a28eea5e58cc9535e47e947bc850994db1477747964b` |
| PROTOCOL.md | 10950 | `70bc96b01e3688a98cd1da5afce7bb7e0d26cea5f5c0037dd597139848128d2c` |
| constant-encoding.json | 6372 | `a3cab7f30b4490308464d1016bbe19539a8d197fb77076860f523c484c54005e` |

Additional static context read: source/browser.html, PREFLIGHT-RESOLUTIONS.md, API-EVIDENCE.md, KERNEL-NOTE.md, and DRAFT.md. The initial review remains the source for the dated WGSL finite-math/bitcast analysis. No fresh browser or numerical evidence was acquired.
