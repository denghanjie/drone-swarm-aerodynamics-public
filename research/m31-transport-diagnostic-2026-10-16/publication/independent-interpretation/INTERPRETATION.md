# New synthetic transport: public evidence interpretation

Review date: 2026-10-15 UTC. Scope: read-only interpretation of twelve public result, trace, and publication files from the completed synthetic trial. No private evidence, browser, probe, diagnostic runner, scientific source, or campaign saved reviewer was used. Exact input hashes are in `PUBLIC-INPUTS.json`.

**The new trial reached a browser-reported Local Network Access permission failure for its POST.** This is a specific boundary observation from this trial. It does not establish the underlying policy cause, an actual user permission decision, or the cause of the earlier scientific upload failure.

## Evidence and limits

| Public evidence | Supported observation |
|---|---|
| e15, result browserContext/origins | The page reported a secure context and the expected page-origin label; its effective origin differed from the constructed sink origin. Public host/port-role metadata describes loopback URLs. |
| e18–e21 | CDP linked OPTIONS `cdp-4` to POST `cdp-5` and reported a 204 preflight response with matching origin/method/header labels, `hasExtraInfo:false`, and zero encoded data length. |
| e23, e31 | One sink connection was recorded and later closed. |
| e24 | Audits reported `LocalNetworkAccessPermissionDenied` for `cdp-5`, `isWarning:false`, `localNetworkAccessRequestPolicy:PermissionBlock`, `initiatorIPAddressSpace:Unknown`, and `initiatorOriginLabel:other-origin`. Replay possibility was retained. |
| e26, e28, e29 | Playwright reported `net::ERR_FAILED`; the page reported `TypeError`; Network.loadingFailed independently associated `LocalNetworkAccessPermissionDenied` with the same POST ID, with `canceled:false`. |
| Result and trace | Zero sink HTTP request-entry records, zero OPTIONS/POST counts, no accepted body, no bytes written, no retained payload, and no acknowledgement. |

The correlated loading-failed event makes the Audits finding more informative than an isolated replayable issue. Official CDP definitions distinguish this permission-denial category from ordinary missing-origin or preflight-method/header errors. A page-level Fetch `TypeError` alone would not supply that distinction. [Official Network protocol definitions](https://github.com/ChromeDevTools/devtools-protocol/blob/master/pdl/domains/Network.pdl), [Audits protocol](https://github.com/ChromeDevTools/devtools-protocol/blob/master/pdl/domains/Audits.pdl), [Fetch standard snapshot](https://fetch.spec.whatwg.org/commit-snapshots/e9460d1b22ead1c6a72eeac37fb2ec0dc01aeb1d/)

**Do not describe the 204 as a response from the Node sink.** It is a CDP observation; the sink records no HTTP handler entry. The public evidence does not identify whether that preflight representation arose from interception, browser handling, or another path. It therefore does not prove that OPTIONS traversed the socket to the sink or that the sink's CORS handler ran. The observed connection prevents the broader claim that no socket connection occurred. Zero HTTP entries also does not prove zero TCP bytes were exchanged.

**Do not infer a loopback-classified initiator from the URL.** The DOM context uses the expected page-origin label, but the correlated Audits data reports address space `Unknown` and origin label `other-origin`. That lossy origin label cannot recover the exact value or explain the discrepancy. The WICG draft's loopback-origin exception is not enough to override this runtime observation or identify why the browser classified it that way. Instrumentation effects, origin/address-space assignment, and permission-policy state remain unresolved. No user denial, OS permission refusal, browser defect, or policy regression is established. [WICG Local Network Access, §2.2](https://wicg.github.io/local-network-access/)

## Completion and privacy

The public completion receipt records external capture exit 0 and 8.073 seconds. The worker reports one browser launch, one reserved fetch attempt, 32 events, no recorder drops/truncation/callback errors, and local recorder completeness. Those are capture/recorder observations; they are not successful delivery. The result remains `transfer-failed-before-sink-acceptance`, with qualification and historical-explanation flags false. Lifecycle records still distinguish candidate verification from final authority. **The campaign saved review had not passed at the time of this memo; its checker was still being prepared.**

A read-only inspection found 32 contiguous event IDs and confirmed the public trace's 7802-byte length and SHA256 against the result. Across the twelve inspected files (18014 bytes), the scoped scan found no literal URL, local absolute path, standalone 48-hex nonce, reserved nonce path, profile switch, sensitive header key, or explicit socket-address/port field. Error categories, stable IDs, semantic origin labels, and structural port roles remain readable. This is a bounded public-file inspection, not a universal privacy proof; no private trace was opened.

Key input pins:

- `results/result.json`: 2896 bytes; SHA256 `addc065f69deef0e962ec28cf009283dc2f593cfc7d91a7b78fedff016f2cb98`.
- `raw/trace.public.ndjson`: 7802 bytes; SHA256 `16b9231f2537874a61a4b2bf12ed80b8ea7c2993c12eb443b6306c5547a2f29f`.
- `publication/capture-execution.json`: 310 bytes; SHA256 `45449b964281e92789c6f73ad67e0fde45c3110f9fc812d1795000d87cc635f7`.

A useful public conclusion is: “The separate synthetic trial failed with a browser-reported Local Network Access permission error before any sink HTTP request entry was recorded. The underlying policy cause and historical upload cause remain unresolved.” No retry is implied or authorized.
