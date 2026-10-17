# Attempt 02: preserved QA assertion failure

The single authorized attempt failed at `desktop camera aspect updates on resize`, before the frame/frustum loops and before either screenshot. The attempt is failed and unchanged; no retry was performed. Its eight startup/identity/scene checks passed, its aspect assertion failed, and its final preservation check passed. The camera repair has not yet received completed browser/frustum verification or visual signoff.

The QA author used `clientWidth / clientHeight`, which returns integer CSS layout dimensions, while the renderer uses the fractional dimensions from `getBoundingClientRect()` to set its camera aspect. Comparing those different measurements at a `1e-10` tolerance is invalid for a fractional CSS grid width. This is a definite harness inconsistency. The failed report did not save the runtime dimensions, so the precise numeric difference cannot be reconstructed from this attempt alone; no camera-framing success is inferred.

A proposed narrow correction is to compare the camera aspect with the same fractional scene rectangle used by the renderer, and save both the camera aspect and measured rectangle with the assertion. Viewer, poses, loads, scientific records and camera logic would remain unchanged. Any such correction and another attempt require separate parent authorization. The failed attempt stays intact.

Outer wall: 7.294242415577173 seconds. Child/supervisor exit codes: 1. Zero frame checks, zero final-scale combinations and zero screenshots were reached. No page errors, warnings or failed requests were recorded. Chrome 155.0.8059.80 / Playwright 1.62.1.

Cleanup succeeded: Browser.close requested; owned root exit and close code 0/null signal; reaped; no forced termination; private profile removed. Existing HTTP server PID 48039 remained untouched. All 505 protected scientific/source/viewer/prior-QA files matched before, after, and final current-byte checks. No scientific imports or calls occurred.
