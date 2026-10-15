# Static proposal: one tiny-byte browser transport diagnostic

Status: proposal only, following the terminal result reported by the coordinator as `22ca9e4`. This document allocates no execution, creates no freeze, and authorizes no browser launch, transport probe, retry or scientific work. The independent auditor is deciding whether a separate diagnostic is authorized. All earlier source pins, results, locks and failed reviews remain immutable. Nothing in a future diagnostic could repair or requalify either failed scientific campaign or either failed saved review.

## Question and smallest useful test

Can one fresh headless Chrome page, served with Playwright route fulfillment at the same original loopback origin, POST one fixed16-byte heap `Uint8Array` to a separately listening loopback Node sink using the original method/header/response pattern, persist those exact bytes and read back a valid receipt?

One browser launch, one fresh context/page and one application `fetch` are enough to falsify the narrow claim that this transport pattern currently succeeds for the fixed tiny payload. Browser-generated OPTIONS and browser/HTTP implementation behavior are observed, not counted as additional authorized application fetches. There is no Node HTTP probe, same-origin control arm, header variant, permissions variant, retry, follow-up request, GPU setup or adaptive rescue. In particular, do not silently add a second request to diagnose the first failure.

The page would contain only a new transport function. It must not import, serve, evaluate or call the old runner, `browser.js`, `body.wgsl`, numerical host, wake/field model, root solver, generator, runtime helper or scientific driver. It must not touch `navigator.gpu`, create an adapter/device, compile a shader, allocate/map a GPU buffer, generate scientific inputs or reconstruct missing GPU output. The body is a literal heap byte array, independent of scientific data:

```text
Decimal: [0,1,2,3,16,32,64,127,128,129,200,240,252,253,254,255]
Hex:     000102031020407f8081c8f0fcfdfeff
Length:  16
SHA256:  72c0645152e8bea4b87bb7dd50469d260bdb1e10aec14f2dac372a045eebff9b
```

The digest above was calculated from that literal during static preparation; no scientific generator or runtime target was executed.

## What the frozen source establishes

All following references are to `research/m31-body-runtime-replication-2026-10-16/source/`.

- `experiment.cjs:24–43` creates a new `http` server bound to `127.0.0.1` on an ephemeral port and awaits its listen callback. The fixed response headers allow origin `http://127.0.0.1:8876`, methods `POST, OPTIONS` and request header `Content-Type`. OPTIONS gets204 without touching a reservation. A matching unused POST marks its reservation started before validating Content-Length or opening a file.
- `experiment.cjs:83–89` creates a fresh page and route-fulfills exact HTML/JavaScript/shader URLs whose origin is `http://127.0.0.1:8876`. The source does not start an HTTP server on8876. The sink is already listening before navigation.
- `browser.js:104–110` awaits GPU mapping, obtains a `Uint8Array` view, then calls `fetch(sinkURL, {method:'POST', headers:{'Content-Type':'application/octet-stream'}, body:bytes, signal})`. The persisted-readback counter increments only after an OK response and accepted JSON byte-completion receipt.
- The page origin and sink have the same host but different ports, so the POST is cross-origin. `application/octet-stream` is not a CORS-safelisted Content-Type; a fresh request normally requires preflight. The original server has an OPTIONS path and explicit CORS response fields. Merely observing a cross-origin URL does not establish a CORS defect.
- The saved API record reports `TypeError: Failed to fetch`, a submitted15-active/64-lane pair-control dispatch and no persisted readback. The saved sink reservation has `started:false`. That excludes entry into the matching unused-POST reservation branch under the recorded source, but does not prove that the server received no OPTIONS, no unmatched POST or no malformed connection. The source retained no request-level sink trace or CDP network failure record sufficient to distinguish those cases.
- The original Content-Length assertion, filesystem open and byte-write checks occur after `started=true`; on their own they do not explain the saved `started:false` value. Likewise, a receipt-read failure after a completed matching POST would not leave that reservation unstarted. These are control-flow constraints, not a completed causal diagnosis.
- The generic fetch error does not name its network cause. The source puts fetch after mapping, but the terminal health snapshot overwrites the intermediate stage and no direct per-operation event was retained. `readbackBytes:0` must not be described as proof that mapping was never reached.

## Read-only hypotheses and discriminating evidence

| Candidate explanation | Why it remains plausible or limited | Observation needed from the new test |
| --- | --- | --- |
| Preflight/policy rejection before matching POST | The request is cross-origin and uses a non-safelisted Content-Type. A local/private-network requirement, if actually requested by this browser, is not explicitly answered by the old headers. No version-specific policy claim is established by current evidence. | Server OPTIONS entry/response headers correlated with CDP request/response/failure data, actual Origin and Access-Control-Request-* headers, plus a browser-reported blocked reason or CORS status when available. |
| Local connection/listener/address failure | Generic fetch failures can arise before an HTTP request reaches the handler. The original code awaited listen, but lacks socket/error/request chronology. | Listen callback and bound address, server connection/clientError/socket events, browser network error text, and whether any HTTP request was actually accepted. |
| Reservation/path/origin mismatch | A wrong path can return409 before setting started; actual Origin may differ from an assumption. The current source intends matching values but did not retain the request. | Exact private request URL-to-reservation binding, sanitized matched-reservation flag, method, actual Origin and response status. |
| Response-side browser rejection | An HTTP response may exist even if JavaScript receives a generic failure. Successful matching POST would normally set started; it is not supported by the old unstarted reservation. | Node response-finish event, persisted bytes, CDP response/extra-info and browser loadingFailed/fetch settlement. |
| GPU-backed body/lifetime or larger-payload context | The original body came from a mapped GPU range and was3840 bytes. The proposed body deliberately lacks that origin and size. | This tiny-byte test cannot isolate these factors. Success leaves them and transient historical conditions unresolved; no GPU body variant is authorized. |

A missing optional CDP field means “not observed,” not “no such error.” A browser request-intent event is not proof of server receipt. A Node response-finish event means the response was handed off by Node, not proof that browser JavaScript accepted it. A matching receipt and independently verified file are required for transport completion.

## Prospective setup to preserve useful similarities

If a separate diagnostic is authorized, freeze new source and a new namespace before any launch. Never reuse an old output directory, nonce, lock, sealer invocation or old runner entry point. A proposed namespace is `m31-transport-only-2026-10-16`; naming here creates no campaign.

Preserve these transport-relevant features where verifiable:

1. The same recorded Node/Playwright versions and the explicitly selected Chrome155.0.8059.80 loader/framework/helper pins, fresh headless profile, ordinary `chromium.launch({channel:'chrome', executablePath, headless:true, timeout:15000})`, and default browser context. Current identity must be checked by newly reviewed byte-only preparation if adopted; do not invoke the old runtime helper or assume saved pins prove the current installation.
2. The same page origin `http://127.0.0.1:8876`, with only newly frozen minimal HTML and transport JavaScript supplied by exact Playwright routes under a new pathname. No port8876 server or proxy is introduced. Record the route hits and the page's actual `location.origin`, URL, `isSecureContext` and ready marker.
3. A new Node sink listening on IPv4 loopback with a new ephemeral port. Require sink port different from8876; if that condition fails, stop the sole attempt rather than rebinding or silently testing same-origin transport. Record listen success before navigation/fetch.
4. One private nonce/reservation path beneath `/evidence/`, one exclusive16-byte file, and the same CORS fields/status behavior as the frozen sink. Keep the original POST Content-Length requirement; log the observed header before testing it. Do not add an allow-private-network header, permissive wildcard, credential change, security flag or permission grant during the run.
5. Exactly one `fetch` from the page with method POST, header `Content-Type: application/octet-stream`, the fixed heap `Uint8Array`, and an AbortController. Preserve default credentials and redirect behavior. The sink emits no redirects. An unexpected redirect is a recorded deviation that cannot count as successful replication of the intended pattern; any browser automatic traffic remains bounded and observed, never a manually launched second attempt.

Differences must be explicit: new diagnostic source/page path/profile/nonce/port; heap bytes instead of a mapped GPU buffer;16 bytes instead of3840; no GPU initialization or prior shader fetch; shorter preparation history; additional logging/CDP instrumentation; potentially changed runtime/OS/network-policy state since the failed run. These prevent either outcome from being attributed retrospectively to the original failure without further evidence.

## Exact evidence required before the sole fetch

Install observers before navigation and reserve the sink before invoking the page function. Each evidence record has its own schema/kind, monotonic timestamp in that process, sequence number and normalized request identifier. Relate browser/host events by request/reservation identity; do not compare independent clocks as if already synchronized.

Browser/Playwright evidence:

- Navigation/route-fulfillment identities and hashes for the two new inert files; actual page origin and ready state.
- `request`, `response`, `requestfailed`, console, pageerror, crash and close events, filtered to the diagnostic page and sink.
- A page-operation trace: fetch-entered, fixed body length, response-received/status, receipt-parse outcome, receipt fields, exception name/message, abort-requested and final settlement. Record an operation's transition before moving to the next; final status must not erase the last reached phase.
- A newly attached CDP session with Network logging enabled before the fetch. Retain bounded projections of `Network.requestWillBeSent`, `requestWillBeSentExtraInfo`, `responseReceived`, `responseReceivedExtraInfo`, `loadingFinished` and `loadingFailed`. Include actual method/origin/header allowlist, status, errorText, blockedReason and corsErrorStatus when present. Browser Log/Audits events can be retained if the frozen implementation supports them; support/absence must be recorded. No policy override or network request is made merely to enable logging.

Node sink evidence:

- Listen callback/address and listener error/close, accepted connection, socket error/close, and clientError events; use logical connection IDs and bounded records.
- A request-entry event **before** method/path/reservation branching, containing method, matched-reservation status and an allowlist of Origin, Content-Type, Content-Length and Access-Control-Request-* fields. This is essential because the old started flag omitted unmatched requests and OPTIONS.
- OPTIONS response status and actual emitted Access-Control-Allow-* fields, response finish/close/error; no synthetic assumption that a sent header reached Chrome.
- POST reservation transition, declared length, exclusive-open success/error, body chunks/total, aborted/error/end, actual successful write lengths, close, final file length/hash and response status/finish. Preserve any partial file and failure state.
- After closing the file, independently read its16 bytes and compare byte-for-byte and SHA-256 to the frozen literal. The response is accepted only when it states `complete:true`, `bytes:16`, and the independently verified digest. Compare corresponding stable fields across records, not whole objects with different envelope fields—the failed saved review demonstrated why record-shape assumptions require explicit inspection.

Private raw URLs/nonces, request IDs, process/profile identities and potentially sensitive console/error details remain in bounded private diagnostics. Publish normalized event chronology, method/status/policy evidence, byte/hash results, complete/incomplete flags and counts. Exclude cookies, authorization headers and unrelated traffic. Public normalization must preserve the specific browser error category without exposing private path tokens. All private and public diagnostic bytes count within the same adopted output cap.

## Prospective bounds and lifecycle requirements

These are proposed ceilings only; no allocation is made by this draft. A compact diagnostic could use one60-second whole-lifecycle allowance, a5-second fetch abort deadline, a16-byte payload/file cap, a1MiB total evidence cap, and the already understood sampled4GiB owned-process ceiling. Freeze exact work/cleanup/hard boundaries and output reserves only after adoption. The fetch timeout is one terminal result, not permission for another request.

The logging plan must be bounded before implementation: for example at most256 selected events, at most512KiB combined private event data, at most64KiB public event projection,16KiB combined retained process pipes and reserved final provenance within1MiB. A missing event due to truncation/overflow/timeouts makes the diagnostic incomplete; it must not be classified as evidence that a network stage never occurred.

The earlier science lifecycle design, rather than the saved-review direct-child-only assumption, is the relevant ownership precedent. A browser test has detached Chrome descendants. If reusing that design, copy only separately reviewed lifecycle instrumentation into the new namespace: pre-spawn Chrome executable/profile intent, bounded private registry, Node in the owned relay group, exact ownership proof before any browser-group signal, no signals after confirmed absence/reaping, bounded probes/drains, final byte accounting and an external capture measuring actual observer completion. All changed paths, commands, timers, caps, freeze fields and output accounting require fresh static review. Never invoke or import the old scientific wrapper/observer/registry as a shortcut.

The saved-review wrapper cannot be reused unchanged: its “checker creates no descendants” ownership premise is false for Playwright Chrome. A final direct Node exit, `browser.close()` promise or captured pre-exit success flag alone is not enough to establish complete lifecycle closure. On uncertain ownership, do not kill shared groups or guess PID authority. Preserve a failed/incomplete sole diagnostic and stop.

No lifecycle artifact is supplied or frozen here because authorization and allocation are still pending. A later source implementation must keep actual final tool exit and the complete bounded capture summary conjunctive, account all private diagnostics/locks/receipts exactly once at their respective phase boundaries, and expose no scientific qualification field that can become true.

## Predeclared dispositions

- **Tiny transport completed:** exactly one intended application fetch; valid origin/setup; a matching POST observed; exactly16 expected bytes exclusively persisted and reread; matching browser-visible receipt; complete bounded traces; and verified final process/output closure. This shows only that the selected tiny transport pattern succeeded in this new invocation. It does not repair the old missing output, establish the original cause or validate GPU/physics behavior.
- **Observed transport failure:** the one fetch fails or is aborted, with complete evidence identifying its last observed phase and any browser/server-reported cause. A specific CORS/private-network/connection explanation is reported only when matching trace evidence supports it. Otherwise use “transport failed; cause unresolved.”
- **Diagnostic incomplete:** environment/launch/route/observer/logging/cap/ownership/closure failure prevents the stipulated inference. Preserve partial evidence; no retry, fallback origin or alternate policy setting.

No outcome authorizes a third scientific campaign, a corrected saved review or missing numerical work. Any later action would need a new explicit scope decision.

## Static preparation record

Read the frozen experiment/browser sources and saved failure JSON only. Computed one digest for the literal16-byte diagnostic payload. Wrote this proposal under `/tmp`. No old source, result, lock or publication was changed. No browser, transport probe, runtime helper, GPU operation, root/generator/field function, diagnostic implementation, sealer or reviewer was executed.
