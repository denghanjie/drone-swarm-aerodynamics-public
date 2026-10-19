# Independent static harness and viewer review

20 October 2026. Reviewed `source/run.cjs`, `viewer/app.js`, `viewer/index.html`, `source/ui.cjs` and the added `source/ui-supervise.py` as source text against `PROTOCOL.md`. Related cache/wrapper text was consulted to understand refusal and witness behavior. No module import, syntax run, numerical evaluation, audit execution, server launch, browser action or screenshot was performed by this reviewer. The numerical audit and subsequent candidate-efficiency patch have separate reviewers and are outside this review's approval scope.

**Final static disposition: no remaining blocking finding in the reviewed harness/viewer scope. The identified fixes are accepted by source inspection, including the final owned-browser containment change. This permits source freeze within this review's scope; it is not a rendered-UI pass, runtime-containment observation or numerical qualification.**

## Findings and fixes verified

| Area | Static result |
| --- | --- |
| Native-query allocation | The source has 12 two-arm control cases plus nine two-arm, eight-stage streams, including one warmup: 24 + 144 = 168 maximum complete calls. Measured order alternates four FC and four CF batches. No adaptive repetitions are present. |
| Candidate reset and timing | Candidate resets before every stream; its reset duration and all per-query durations enter the batch total. Each query timer includes the owned input copy and complete native query. Input-preservation/evidence work follows that timer. This is a query-sequence sum, not end-to-end elapsed simulation cost. |
| Exact comparison | Actual complete normalized semantic bodies are retained with exact-byte deduplication and compared by digest and file bytes. The exclusions match the declared method/timing/enumeration paths. Pair-comparison durations are now recorded separately. |
| Storage fix | `launch.lock` is now counted. Semantic bodies, witnesses, journals and ordinary records go through the counted writer. Normal records stop at 510 MiB, leaving 2 MiB for failure and exit records within 512 MiB. This repairs the previously uncounted journal and missing failure headroom. |
| Refusal witness fix | The duplicate-ID control now explicitly requires the complete cache snapshot to remain unchanged from the preceding call. The last fallback value belongs to that preceding call; it is not evidence of a new fallback on the refused input. |
| Fresh-output control fix | Force and attitude controls now require changes to hashes of actual derived loads, rather than merely changes to a whole record containing the modified raw input. Exact F/C comparison remains the principal correctness gate. |
| Cache events | The stream now asserts cold build at stage 0, box-exit rebuild at stage 6 and reuse at other stages. Actual witnesses are saved for controls and the first measured C stream, outside query timing. Independent candidate-completeness and mutation checks belong to the separately reviewed audit. |
| Viewer data boundary | The viewer imports only local Three.js/OrbitControls and reads saved result files. It checks result bytes against supplied size/SHA-256 pins and requires a passing saved audit before populating the scene. No scientific kernel is imported into the viewer. |
| User-facing claims | The page prominently identifies prescribed synthetic states and distinguishes numerical/computer-cost results from physical accuracy or safe flight. The misleading sentence about input checks being separately timed was changed to evidence checks. |
| Geometry QA fix | The planned UI script now obtains the actual rendered position attribute through a read-only snapshot, asserts exactly 3,000 coordinates and compares them with each saved frame rounded to Float32. This repairs the earlier reliance on a hard-coded `data-points` attribute alone. |
| Timing/decision QA fix | The planned UI script now compares every table cell and the displayed keep/stop text against saved values. The underlying saved-value arithmetic and its binding to audited native evidence are the numerical auditor's responsibility. |
| Reset QA fix | The planned UI script compares reset camera and target coordinates with their original values. Damping is disabled, avoiding a continuing damping state after reset. Screenshot change remains the proposed orbit evidence. |
| Failure-path QA | The planned corrupt-response test changes the view-data body while retaining its pin, expects identity rejection and requires no canvas. Desktop/mobile overflow, screenshots and page/console/HTTP error checks are present in the script. None has run during this review. |

## Display-QA completion findings resolved

1. **Explicit marker count resolved.** Every inspected frame's actual rendered position array must now have length 3,000 and equal the saved coordinates after the declared Float32 conversion. The independent audit remains responsible for admitting the underlying finite saved input and frame bindings.
2. **Timeout cleanup resolved.** The UI script's scoped `child_process.spawn` hook admits at most one launch of the exact configured Chrome executable, forces `detached:false`, and writes an owned-browser PID/group receipt. The external Python wrapper starts Node with a new session, allows at most 100 seconds, then sends SIGTERM and, after a 0.3-second grace, unconditionally attempts SIGKILL on that owned process group. Escalation no longer depends on whether the Node leader remains alive. This addresses both the original immediate-exit cleanup gap and the later leader-only-wait gap. A 90-second inner timeout can still omit `ui/qa.json`; in that case the outer supervisor receipt is the failure record and there is no UI pass. Actual group cleanup still needs the execution receipt; no browser was launched in this review.

A nonblocking robustness recommendation was sent to the parent: after `chromium.launch` resolves, require `launches === 1` so a future launcher that bypasses the scoped hook cannot silently satisfy QA. The current reviewed pattern records the admitted owned launch and is accepted for this frozen implementation.

The separate audit must independently bind view-data positions, timing batches and keep/stop arithmetic to the saved inputs/query records; a viewer checking `audit.passed` and file hashes cannot by itself perform that scientific binding. Its publication of pins is a saved-evidence trust boundary, not a security claim against simultaneous replacement of evidence and pins.

## Explicit limits

The tests cover one fixed finite panel and runtime. They do not demonstrate exact output equivalence for every input, arbitrary ordinal guards, every cap/resource failure or a general physical model. The candidate adds guard calls, so the present deadline-guard allocation must not be reported as preserving ordinal guard behavior.

The GPU receives Float32 positions; the source retains binary64 input evidence. The viewer should be described as plotting saved positions with normal rendering conversion, not preserving every binary64 coordinate bit on screen. The scene is a visualization, not an additional numerical computation of flight.

The active frontend testing workflow was consulted. Its rendered checks are reserved for the parent's single authorized saved-data UI allocation; the explicit static-only assignment takes precedence here. No page identity, layout, screenshot, orbit/reset behavior, WebGL availability or console-health result is claimed by this report. A frozen-source manifest and the parent's completed execution/audit/UI receipts are still required for their respective outcome claims.
