# Post-unit static-review corrections

The complete implementation source/config tested in unit attempt 01 is retained under `unit-attempt-01/` with adjacent SHA-256 manifest. It passed the 23 synthetic fixture groups; no compatibility or fresh Boids numerical case had run.

Before source freeze, mandatory static-review corrections were applied:

1. Export campaign helpers before invoking the entry point, so the raw reconstruction module can resolve them during circular module initialization.
2. Recheck the hard total deadline after the final execution-validity serialization. Any overrun is invalidated and logged as emergency cleanup.
3. Prevent phase-biased diagnostic display traces: each 10 ms bin now reports the maximum sampled endpoint/one-sided error across the whole bin. This changes no dynamics, quadrature, reference gate or error screen.

The initial fixture pass applies to the retained snapshot, not automatically to these corrections. Relevant checks must be repeated before execution authorization.
