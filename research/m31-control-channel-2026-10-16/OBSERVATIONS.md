# Observations and interpretation

Source commit `4edf40a7cbfa2d41414dc8a8a6ff0718d0fa5671`; source freeze SHA-256 `c36018ea48530e17c91bed62b5f062ff93577dd4328559c9dd9ca6d22e1d932b`, 30 pins, published and independently verified before invocation. Runtime: Node 24.19.0, Playwright 1.62.1, Chrome 155.0.8059.80, Python 3.9.6, Darwin arm 64. The selected runtime pins passed actual admission.

|Observed item|Saved evidence|
|---|---|
|One browser lifecycle and one payload evaluate call|`results/result.json`, ownership/closure fields in `results/budget.json`|
|Actual decoded return validated; 3,840 values|`raw/returned.json`, `returned` fields in worker result|
|Returned and saved binary SHA-256|`b92773fc3edb949a8a0d6e4a2f60ef2020ee2bd5bf6f8299c1448142a6cd3404`|
|Exclusive output file closed after one successful write of 3,840 bytes|`persistence` fields and saved trace; `raw/received.bin`|
|Independent post-closure byte equality with returned values and frozen fixture|`review/results/report.json`, `byteEvidence`|
|21 retained events; zero drop/truncation/recorder/callback errors, redirects or observed application payload requests|`raw/trace.public.ndjson`, `instrumentation`|
|Five independent review groups passed; zero errors; actual checker exit 0|Review report and external completion records|
|Capture, observer, relay and Node exits 0; complete recorded owned-process closure|Capture, budget, wrapper and external completion records|

The actual saved JSON is 13,971 bytes. This is a canonical encoding of decoded return values, not a capture of Playwright's internal wire traffic. Its size does not measure total memory or serialization overhead.

The recorded host evaluate interval is 44.146042 ms and includes host event-recording overhead. Browser construction uses a different clock. The external tool-call observation is 4.995 s, including dispatch overhead; the observer's recorded lifecycle is 1.620248959 s. These are single diagnostic observations, not benchmark statistics or an isolated network time. The saved checker completed with an external tool observation of 0.089 s.

Peak sampled owned RSS was 1,141,784,576 bytes. Sampling does not bound transient or GPU-driver peaks. The execution accounting reported 40,763 bytes; the reviewer accounted 47,455 bytes including its declared later public/review copies, and 48,021 bytes after the external review completion receipt was added. Source, documentation and presentation artifacts are publication material, separately inventoried in the final manifest. Private byte totals and process observations were checked for consistency by the saved-public-evidence checker, not independently reconstructed from private originals.

**Supported conclusion:** this single synthetic ordinary-heap payload reached Node through the existing automation connection, was persisted from the actual returned values, and matched exactly under independent post-closure comparison. The complete claim also depends on the saved source/runtime and lifecycle evidence, not byte equality alone.

**Not established:** GPU mapped-buffer lifetime, larger-output cost, reliability, the cause of the historical GPU failure, physical validity, swarm performance or novelty. Earlier browser-fetch denial remains unchanged; this trial exercised a different path without modifying permissions. The API rationale remains in [SOURCES.json](SOURCES.json) and the [installed-version inspection](../m31-followup-planning-2026-10-16/CONTROL-CHANNEL-API.md).
