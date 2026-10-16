# Coupled-cost launcher failure: supported interpretation and prospective admission check

Source-only review, 2026-10-16. Read the saved candidate supervisor record, immutable runner and saved reviewer supervisor/output in `research/m31-coupled-cost-2026-10-16`. No candidate, checker, diagnostic child process, simulation, geometry, load calculation or timing test was launched by this review. No scientific source/result was edited. File reading and this note are the only work performed.

## Exact supported statement

> The candidate allocation was consumed and closed after its supervisor recorded a PermissionError during launch or monitoring. Its recorded supervised interval was 0.0021168338134884834 seconds, return code was unavailable, and no RSS sample was obtained. Only the consumed lock and empty stdout/stderr were inventoried; no valid candidate control, qualification or timing outputs were retained. The record does not identify the denied operation or establish that the candidate process never briefly started. The separate saved-record audit completed with an incomplete/failed coverage result. No coupled-cost comparison can be inferred, and the closed allocation is not retried.

The candidate record pins source commit `4fdcc83fe870c110679a72666029d4cbc987e22c` and manifest `6c653f2665428b342dff7f7265c03c94a20f8d8b0ade42841972378f73b68a31`. It has returncode null, exception_class PermissionError, rssSamples=0, rssSampleErrors=0 and externalSampledPeakRSSKiB=null. Its two child log files are zero bytes. The reported elapsed interval starts after source checks and lock creation; it is not necessarily the total tool/preflight duration. This was an early exception, not evidence that the 300-second wall allowance was exhausted.

The later reviewer supervisor records exit code 1, about 0.426 seconds, two RSS samples, no RSS sample errors and empty stderr. Its saved review has pass=false, complete=false and missing candidate coverage. This is a functioning saved-record audit reporting absent/incomplete evidence, not a numerical qualification of the planned methods. The coordinator identifies this reviewer invocation as outside the sandbox; the supervisor JSON alone does not record or authenticate that permission context. Neither its successful process execution nor its exit code supplies the candidate's missing launch stage.

## Why the candidate's exact failure site remains unknown

The relevant immutable runner sequence is:

1. Open the two child log files.
2. Assign `proc = subprocess.Popen(..., start_new_session=True)`.
3. While the child runs, launch `/bin/ps` through `subprocess.check_output` for RSS.
4. Catch only ValueError and subprocess.SubprocessError around that RSS operation.
5. The outer BaseException handler saves only the exception class. If a child is still live, it sends process-group SIGKILL and waits, but does not assign that cleanup return value to the saved returncode field.

PermissionError is an OSError subclass, not a subprocess.SubprocessError. Consequently, either a candidate-launch PermissionError or a PermissionError while launching the first RSS helper can reach the same outer handler. The latter path may follow a successful candidate Popen while leaving both RSS counters zero: the inner error-counter clause does not catch PermissionError. Cleanup may reap a child while the saved returncode remains null.

The record lacks an explicit stage, successful-child-creation flag, helper-attempt counter, exception errno and cleanup outcome. It therefore cannot distinguish those paths. Empty logs and absent artifacts establish absence of retained valid scientific output; they do not prove absence of transient candidate execution, module initialization or hidden partial computation. The very short interval is not sufficient to reconstruct event ordering or rule out a briefly running child.

After this record was read, the coordinator reported a separate default-context `/bin/ps` read returning `operation not permitted: ps`. That makes monitoring-helper denial a supported plausible explanation, but it does not retrospectively identify the historical failing operation. The coordinator also identifies the successful saved-review launcher as host-approved: its two RSS samples show that the shared runner could launch and monitor that Python reviewer in that context. This does not establish that the Node executable or a default-context Node launch is admitted. These are later infrastructure observations, not candidate scientific outputs or a repair of the closed allocation.

Do not state that Node was definitely blocked, that `/bin/ps` was definitely blocked, that no candidate instruction ran, or that all science budget is therefore still available. Do not call this a model-domain failure, a negative speed result, a zero-duration query or an automatic approval-review rejection. The saved evidence shows an operating-system PermissionError, without the denied operation or approval-review reason. The consumed lock and failed evidence remain immutable.

## Minimal prospective infrastructure-admission experiment

Recommendation only; no test is authorized or executed by this note. Before considering any replacement scientific allocation, freeze a separate two-context launcher diagnostic. It must not import scientific modules or read model states/reference arrays. Use the same intended Python/Node executables and process-group creation mechanism, with independently saved new source/config hashes and new diagnostic locks/output directory.

**Payload:** a tiny Node child writes one fixed READY token, waits for a parent acknowledgement on stdin, writes one fixed DONE token and exits zero. A fixed short timer exits nonzero if acknowledgement never arrives. This is an echo/handshake child only: no model imports, target paths, numerical workload, geometry, controls, roots, benchmark loops or state files. The bounded handshake keeps the harmless child alive long enough to exercise the RSS-helper launch; an immediately exiting echo could accidentally skip that path and leave the relevant issue untested.

**Exactly two predeclared invocations:** one in the normal/default permission context and one through the ordinary approved escalated context, using identical diagnostic bytes and payload. One child launch and at most one `/bin/ps` helper attempt per invocation. These are a fixed infrastructure contrast, not retries of the scientific allocation; record both outcomes, including a default-context failure. Do not infer escalation approval from a PermissionError or bypass normal tool authorization. The permission-context label must be tied to the actual tool/approval receipt, not merely self-reported by the child.

Use a small explicit budget, for example ten seconds per diagnostic invocation, at most three seconds of child handshake lifetime, 64 KiB combined logs per invocation and 256 KiB total diagnostic evidence. No installation, network operation, device/browser change, optimization flag, environment switch beyond the two declared permission contexts, or adaptive extra attempt belongs in this test. A cap or unexpected failure ends that arm and remains visible.

Persist explicit before/after stage markers for:

- log-file opening;
- child spawn attempt and Popen return, including whether a child handle was obtained;
- READY observation;
- RSS helper attempt, helper spawn/return and parse outcome;
- acknowledgement/release;
- normal wait and its actual return code;
- any cleanup kill/wait attempt and its actual outcome;
- final completion or failed stage.

For each exception retain the active stage, class and safe errno. Keep arbitrary path-bearing exception text private or sanitize it; executable file hashes and public-safe labels are enough for the public record. Record helperAttempts, successfulSamples and failedSamples separately, and catch OSError explicitly around the helper so a denied helper cannot masquerade as an unattempted sample. Preserve the primary exception separately if cleanup also fails. Assign the reaped return code even on cleanup, and distinguish `child_handle_obtained:false` from a child that started but was terminated. A null return code must have an explicit reason.

Use append-only small stage records or bounded exclusive per-stage files so a later failure does not erase the last known successful step. A stage-before marker alone means an attempt, not success. Parent-observed READY/DONE tokens help distinguish an OS process handle from actual Node payload execution. Raw private PIDs may be retained locally if necessary for cleanup, but public output need only expose childCreated/childReady/reaped booleans and public-safe stage identity.

## Admission and decision boundary

A successful arm requires a returned child handle, observed READY, successful declared monitoring helper/sample, observed DONE, exit code zero, completed cleanup state and all limits respected. A helper failure must remain a failed monitoring admission even if the echo child itself works. Neither an uncaught exception nor an unknown stage can be relabeled successful. If default fails and the approved escalated arm passes, the supported finding is only that this particular launcher/monitoring path worked in that declared context. It does not prove a universal sandbox limitation or predict that a 300-second scientific run will finish.

After inspecting both diagnostic records, any replacement scientific campaign needs a new prospective allocation, corrected separately frozen runner, complete source/dependency/remote verification and new locks. Preserve the failed campaign and explain its unknown transient-execution exposure; its absence of valid recorded outcomes does not restore its allocation. The prior scientific kernel need not be tuned in response to this infrastructure result. No performance, physical-accuracy or model-admission conclusion follows from echo-only infrastructure admission.
