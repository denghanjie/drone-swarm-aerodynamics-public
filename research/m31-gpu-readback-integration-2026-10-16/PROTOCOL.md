# Proposed GPU readback integration contract

Status: STATIC ONLY. executionAllocated=false; all launch/review timestamps null. No operational entrypoint or saved-evidence checker has been invoked. Original overnight cutoff remains closed; no historical allocation is reused.

## Question and fixed test

Can a single new GPU lifecycle return and persist the actual 128 bytes of the fixture after cleanup? The fixed public fixture is defined in the prior preparation's PROPOSED-PROTOCOL.md and SOURCE-CONTRACT.md, retained unchanged. It has32u32 words:4prefix,17active,11suffix; workgroup8,dispatch3,guard i<17. Expected SHA256 ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951; initial SHA256944fbd39dc3fa2a2b8c9a2eef1c9c02b812911f4831b22c6c4e17cfe6a770e3a. Independent references agree in pure tests; this is not observed GPU output.

The normative arithmetic/layout gap identified in the historical protocol is resolved additively in WGSL-SOURCE-RECEIPT.json and the new STATIC-REVIEW.md. It does not resolve runtime behavior. Original historical wording is preserved.

## Prospective admission and resource contract

Config identity version1/scope synthetic-gpu-readback-host. Require executionAllocated exactly true and four actual whole-second UTC Z timestamps: notBeforeUTC,stopNewLaunchUTC,reviewNotBeforeUTC,reviewStopNewLaunchUTC. Both windows must be ordered; the relevant phase clock is in[start,end). No disabled/null/invalid window may read runtime evidence, reserve locks, create outputs or start processes. The only pre-admission file access is bounded configuration/source loading.

Draft launch constraints: caller60s, worker40s, observer cleanup58s; host payload evaluate12s exceeds page cleanup10s. Host substantive ceiling34s and browser close3s are internal restrictions, not extra allocations. Existing wrapper ownership and sampled RSS design is copied into a new namespace;8MiB combined result/diagnostic accounting,2GiB sampled owned RSS,2048trace-event ceiling. These proposed limits allocate no time. Their successful enforcement is untested here.

One reserved invocation with no retries; no extra browser/device/dispatch/extraction, fallback output, permission changes or HTTP sink. Failures and skipped stages remain terminal in the later allocated campaign. A later saved-file review needs its own adopted limits and external supervisor before launch.

## Evidence and decision

Host retains a bounded validated envelope even when the page reports failure. Malformed returns get a bounded rejection projection; original arbitrary objects are not public evidence. Valid wrong bytes remain actual evidence. Bytes are exclusively persisted if present; partial writes and close failures are preserved. Compare returned-to-file equality separately from agreement with the independently derived fixture. Report page claims as self-reports, host observation as host observation and external lifecycle closure separately.

Worker kind synthetic-gpu-readback-diagnostic. Legacy transport wrapper/observer/capture receipt kind strings remain for structural compatibility, bound to new source/freeze identities. The new external completion receipt kind is actual-gpu-readback-capture-tool-completion; it requires actualCaptureExitCode,actualFullElapsedSeconds,toolSessionCompleted,source identities, plus externally recorded captureStartedUTC/captureCompletedUTC. Ordered UTC timestamps must place capture start inside the launch window; cleanup may finish later within the full wall budget. These receipts are future evidence, absent now.

A complete future independent comparison must check source/file identity, returned shape, actual bytes, expected bytes, accounting and external termination without importing the producer. A complete recorded evaluate rejection,envelope-rejection projection,page failure or valid byte mismatch may pass record integrity while readback fails. Partial writes,failed closes and incomplete external lifecycle remain integrity-incomplete under this checker; preserving them does not promise an aggregate pass. Failure must never become a scientific qualification. A single successful tiny test could support only that fixture and environment, with no reliability-rate, realistic-transfer-performance or physics inference.

## Deferred prerequisites

Complete independent source review, a bounded saved-review supervisor, private runtime provenance and safe public projection, strict prospective allocations, exact operational source freeze, publication and independent retrieval are required before launch. This static publication manifest is not that freeze. No final operational evidence manifest, fresh allocation or runtime-result folder exists now.
