# One synthetic transfer: observed boundary

Source commit: `fe2c19a30b4605ec755e8e7103946d7ef037a76a`. Source freeze: `3a2f596279d7720ad16ca4eb07685061ecb54769c6c86867750d23d75327d7d8`. This is one instrumented synthetic observation, not a numerical or physical experiment. The [frozen protocol](PROTOCOL.md) was published and independently retrieved before invocation.

## Direct observations

The worker allocated one 3,840-byte heap fixture and reserved one fetch. Both page and sink use loopback URLs with different ports. The page reported its intended origin and `isSecureContext:true`. Chrome 155.0.8059.80 and the pinned runtime files passed before/after admission.

In [the public trace](raw/trace.public.ndjson), `e18` records an OPTIONS intent (`cdp-4`, related to `cdp-5`); `e19` records the POST intent (`cdp-5`). `e20` records a browser-side 204 response for OPTIONS, with zero encoded bytes at `e21` and `hasExtraInfo:false`. The sink recorded one socket connection (`e23`) but **zero HTTP handler entries**, zero OPTIONS/POST entries, and no matching reservation acceptance. Therefore the browser-side 204 must not be attributed to this Node sink. The trace does not establish where that response was generated.

`e24` records a non-warning CORS audit for the POST with `corsError:LocalNetworkAccessPermissionDenied`, `localNetworkAccessRequestPolicy:PermissionBlock`, and `initiatorIPAddressSpace:Unknown`. Its sanitized initiator origin is `other-origin`. `e29` also records the same CORS error in the POST's loading-failure event; Playwright records `net::ERR_FAILED` at `e26`, and page JavaScript records TypeError at `e28`. No payload file exists and no acknowledgement was received.

All 32 attempted trace events were retained as 32 public/private pairs; recorded dropped, truncated, callback-error and observer-error counters are zero. The final local cleanup barrier is `e32`. These are local recorder-health observations, not proof that Chrome emitted every possible event.

## Lifecycle and resource evidence

The outer command actually exited 0, with its complete 487-byte summary retained. The conservative tool observation from before invocation through final completion was 8.073 s; the caller measured the observer's completed lifecycle at 1.610274791 s. Neither duration is a speed benchmark. Node, relay and observer exited 0 because a completely observed failed transfer is a valid diagnostic outcome.

Owned process groups were recorded absent; no kill signals or cleanup errors were recorded. There were 26 RSS samples, with peak sampled owned RSS 1,030,946,816 bytes under the 2 GiB cap. This excludes any claim about unobserved transient/driver memory peaks. The diagnostic accounted for 29,948 bytes before the separately accounted publication copies and external completion receipt.

See [worker result](results/result.json), [observer budget](results/budget.json), [capture receipt](results/capture.json), and [actual tool completion](publication/capture-execution.json). The saved-public-evidence review has its own source, invocation and external completion records; its final scope is documented separately.

## Supported conclusion and limits

**Chrome reported a local-network-access permission boundary for this synthetic POST, before any HTTP request was recorded by the sink.** This statement is about one fixed trial. It does not establish that a person denied a prompt, identify the implementation path behind the policy decision, or establish an inherent inability to transfer data in this environment.

The earlier GPU-backed upload had different backing storage and preceding runtime state and lacked these diagnostic events. Its original cause remains unknown. This new observation does not repair that failed experiment or its failed saved review. No new scientific or transport successor is allocated by the result. No browser setting or permission was changed.

See [verified official documentation](VERIFIED-IDEAS.md) and its machine-readable [source ledger](SOURCES.json). Documentation motivates interpretation; the error category attributed here comes from this experiment's actual events. The draft loopback exemption is not treated as proof of Chrome's deployed classification, particularly given the recorded Unknown address space and sanitized other-origin audit value.
