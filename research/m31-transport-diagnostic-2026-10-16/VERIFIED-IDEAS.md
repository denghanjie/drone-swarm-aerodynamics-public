# M31 transport: verified documentation ledger

Prepared date: 2026-10-15 (UTC). Scope: static official-document review only. No browser, transport probe, permission change, environment change, scientific execution, or saved-review execution was performed for this memo. Source passages were read, not merely found in search snippets. See `SOURCES.json` for versions and passage locations.

**The original transport cause remains unresolved.** A saved page-level `TypeError` cannot establish CORS, Local Network Access (LNA), a connection failure, or a particular server response. This ledger supplies interpretation rules for a separately authorized diagnostic, not evidence that any candidate occurred.

## Verified ideas

| ID | Official documentation establishes | Consequence for interpretation |
|---|---|---|
| F1 | Fetch rejects a network-error response with `TypeError`; request construction may also reject. HTTP error status alone does not imply rejection. A CORS check can hide an otherwise received response. | Record the failing phase and exact browser/server evidence; the exception text is not a cause code. |
| F2 | `application/octet-stream` is outside the CORS Content-Type safelist. For a cross-origin CORS request, this header requires preflight handling, subject to the separate preflight cache. Preflight success requires an acceptable 2xx response and matching origin/method/header authorization. | Capture OPTIONS and its response when observed. No observed OPTIONS alone does not prove that preflight was unnecessary. |
| F3 | An opaque response hides readable response details. | Changing to `no-cors` would not supply a readable persistence acknowledgement. |

F1–F3: [WHATWG Fetch, immutable snapshot](https://fetch.spec.whatwg.org/commit-snapshots/e9460d1b22ead1c6a72eeac37fb2ec0dc01aeb1d/), §§2.2.2, 2.2.6, 3.3.3, 4.8–4.9, 5.6. These rules do not determine which path the saved attempt took.

**Origin and network address space are different inputs.** Origins compare scheme, host, and port; two HTTP URLs at `127.0.0.1` with different ports are cross-origin. Preserve the actual initiating origin, including an opaque origin if applicable, instead of inferring it from the destination. [RFC 6454, §§3.2, 5–6](https://www.rfc-editor.org/rfc/rfc6454.html)

**LNA cannot be inferred from “localhost.”** The 7 August 2026 WICG draft excludes loopback-origin requests from LNA checks in §2.2. It is a draft, not a deployed Chrome 155 guarantee. Its implementation note describes narrower rollout coverage than Chrome 142 release notes, which cover public→local/loopback and local→loopback. Chrome 145 release notes split the earlier permission into `local-network` and `loopback-network`. The June 2025 launch article is historical context and says LNA replaced the paused PNA-preflight approach. Do not confuse ordinary CORS preflight with that earlier PNA mechanism. [WICG LNA §§2.1–2.4](https://wicg.github.io/local-network-access/), [Chrome 142](https://developer.chrome.com/release-notes/142), [Chrome 145](https://developer.chrome.com/release-notes/145), [historical announcement](https://developer.chrome.com/blog/local-network-access)

The Chrome 155 release-note check was limited: the old developer.chrome.com URL failed to open; the [ChromeStatus 155 page](https://chromestatus.com/release-notes/155) was accessible, displayed Preview and an October 6, 2026 stable schedule, and contained no matching LNA passage in the retrieved text. This is not evidence that Chrome 155 made no relevant changes.

## More discriminating browser evidence

The following fields are verified against current CDP master, **not a version-pinned Chrome 155 schema**:

| Event/type | Useful fields or interpretation |
|---|---|
| `Network.loadingFailed` | `errorText`, `canceled`, optional `blockedReason`, optional `corsErrorStatus` |
| `Network.requestWillBeSentExtraInfo` | Allowlisted request headers; optional `clientSecurityState` with initiator secure-context, IP-address-space, and LNA policy |
| `Network.responseReceivedExtraInfo` | Allowlisted response headers, `statusCode`, `resourceIPAddressSpace`; may reveal status when CORS prevents normal response delivery |
| `Network.responseReceived.response` | Optional `remoteIPAddress`, `remotePort`; these belong to `Response`, not ExtraInfo |
| `Network.requestWillBeSent.initiator` | Optional related request ID can correlate preflight |

ExtraInfo events can be absent or arrive out of order. A request-will-be-sent event is not server-receipt evidence. Explicit CORS errors distinguish preflight failures, missing origin headers, and LNA permission denial. **Missing fields or events do not establish absence of blocking.** [Official Network protocol source](https://github.com/ChromeDevTools/devtools-protocol/blob/master/pdl/domains/Network.pdl)

`Audits.issueAdded` can provide `CorsIssueDetails`: `corsErrorStatus`, `isWarning`, affected request, and optional initiating origin, resource address space, and client security state. Preserve warning versus error and correlate the affected request. `Audits.enable` sends previously collected issues too; receipt after enabling does not prove the issue arose during the diagnostic. Missing issues or optional fields are inconclusive. [Official Audits protocol source](https://github.com/ChromeDevTools/devtools-protocol/blob/master/pdl/domains/Audits.pdl)

Exact Chromium `net::ERR_*` values can distinguish refused/reset/closed connections, empty or invalid responses, and local-network permission/check failures. They classify an observed error; the list does not prove any error occurred. Current main is not a Chrome 155 pin. [Chromium net error definitions](https://github.com/chromium/chromium/blob/main/net/base/net_error_list.h)

## Prospective interpretation and privacy rules

These are methodological recommendations, not observations or execution authorization:

1. Record browser build, actual page and sink origins, secure-context result, request method, body type, declared Content-Type, byte count, and every intentionally changed condition. A future single 3840-byte Uint8Array POST can characterize that new attempt only. Matching origin relationships alone does not make it an exact reproduction.
2. Start listeners before the attempt. Correlate preflight and POST by request IDs and sanitized endpoint labels; retain ordering without assuming optional events must appear. Record unsupported domains/fields and absent observations explicitly.
3. Capture sink-side boundaries separately: connection/request entry, OPTIONS response, POST header admission, body complete, byte count/hash, persistence completion, response finish, close/error. A log placed only after admission cannot rule out earlier server receipt when absent. Response finish alone does not prove the browser read the acknowledgement.
4. Report success only at the boundary actually supported. Browser fetch success, sink receipt, exact-body persistence, and readable acknowledgement are different claims. A new success does not explain the original failure; a new failure does not retroactively identify its cause. Neither result supplies GPU output or validates the failed scientific campaign.
5. Keep a bounded structured trace. Preserve scheme/host/port and opaque endpoint labels needed for origin analysis; remove nonce-bearing query strings, private paths, cookies, authorization, post bodies, stack URLs, and unrelated requests. Use case-insensitive header allowlists. Do not dump whole ExtraInfo or Audits objects: they can contain cookie information or URLs. Do not change permissions to obtain a preferred outcome.

DevTools documentation supports cautious interpretation of provisional headers and recording windows; its sanitized HAR excludes common sensitive headers, but that does not replace explicit sanitization of application-specific URL tokens. [Chrome Network reference](https://developer.chrome.com/docs/devtools/network/reference)

## Status

Documentation supports a better-observed, bounded transport diagnostic. It does not resolve historical causality or authorize another attempt. No campaign/viewer files were modified by this review.
