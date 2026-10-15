# Final static privacy and interpretability review

Review date: 2026-10-15 UTC. Outcome: **no remaining privacy or interpretability blocker found in the three reviewed snapshots**, within the scope below. This is not transport execution approval, a lifecycle audit, or a successful transport observation.

## Reviewed source identity

Final copies are retained under `source-final/`; `FINAL-SOURCE-PINS.json` records:

| File | Bytes | SHA256 |
|---|---:|---|
| diagnostic.cjs | 26741 | 9467968ded4f8c2409eb30daa7b59dff768025f76a9004e017a65a5d2af92e8e |
| browser.js | 2173 | e892111089850920e9c8febe74429c57f3b2958f04b54906095b515d71d4dfd9 |
| SCHEMA.md | 14266 | e22d8f607e81b80b1c981280d58692ae4eeaf07aa90d470c18275d9517a50570 |

## Findings and resolution

The public projection excludes cookie/authorization header names, full URLs, the reserved path nonce, raw console/error messages, filesystem/profile paths, remote addresses, and actual sink ports from their source fields. Only exact complete known Content-Type strings are admitted. This last rule corrected a concrete review finding: checking only the MIME essence while returning the original value had allowed arbitrary parameters to pass through. A synthetic URL/token/path parameter fixture now verifies redaction.

Error evidence remains structurally useful: browser exception names, categorical `net::ERR_*` text, CORS/blocked categories, warning status, secure-context/address-space/LNA-policy fields, and failed-parameter presence are retained when available. The raw failed parameter and unconstrained text remain private. Opaque origins are preserved as `opaque-null`, distinct from unknown origin labels.

The page reports actual `location.origin` and `isSecureContext` before fetch. Public origin metadata identifies scheme, loopback host, and port roles without exposing the ephemeral sink port. `actualOriginsEqual` starts null and changes only after the browser-context observation is compared with the constructed sink origin. Unexpected effective origins stop the attempt and mark deviation.

PW, CDP, and sink IDs remain separate stable namespaces; related CDP IDs and initiator type preserve emitted preflight linkage. The sole-transfer label does not claim shared wire identity. Audits warning status and replay possibility are explicit. The schema states that missing events/fields cannot rule out a block, and that recorder completeness means local recorder health, not exhaustive backend emission. Persistence and acknowledgement remain separate claims. Redirects and multiple POSTs prevent an otherwise clean classification.

## Inert verification

`projection-checker.cjs` evaluated only the extracted sanitization definitions in an isolated Node VM with synthetic strings/headers. It imported only Node's VM and assertion modules; it did not import the runner. The VM had no `require`, `process`, `fetch`, `window`, or timer capability, and dynamic string/Wasm code generation was disabled. The checker itself used no filesystem, browser, or networking API; its synthetic code and inputs were embedded, and its result was captured from stdout.

All **25 assertions passed**, covering secret header names, known and unknown header values, the Content-Type parameter regression, opaque origins, endpoint labels, structured failures, sensitive text/addresses/ports, LNA fields, preflight IDs, absent optionals, and truncation accounting. This finite fixture suite is a projection contract check, not proof about every possible input or runtime event.

The tested diagnostic snapshot was SHA256 `eba4076827bf71158e6b39b1bd9f07f5e863472e7c0e4125e15498f78f88d099` (26660 bytes), retained under `source/`. After the test, the final diagnostic added only the multiple-POST deviation guard; the schema removed a staging-path reference. Static comparison verified that the final projection is byte-identical to the tested projection, SHA256 `915ca0c75ac006b94ff4c207c2146e10681193dac66145789bf0974c4ef95ae0` (3650 bytes). No second run was needed.

Evidence: `projection-only.js`, `PROJECTION-EXTRACTION.json`, `projection-checker.cjs`, `projection-result.json`, and both source manifests. The checker contains deliberately synthetic URL/token/path sentinels; they are not values from a transport attempt.

## Limits

The private trace intentionally retains exact selected values, including the ephemeral sink URL/token and raw error/console text. It must remain private and excluded from publication. Public outputs still require the planned post-capture privacy check. No browser, request, probe, diagnostic runner, scientific source, saved scientific review, or transport payload was executed by this reviewer. No actual transport failure was observed or explained. Earlier review memo and snapshots are retained unchanged.
