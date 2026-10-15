# Independent static adversarial review: ordinary-heap control channel

Reviewed 15 October 2026 UTC, before source freeze and the 23:00 UTC new-launch cutoff. **No unresolved static blocker was identified in the exact reviewed source below for the protocol's narrow one-fixture engineering question.** This is a source review, not an observed transfer, runtime admission, authorization extension or scientific result. Integrated/frozen bytes must match the reviewed hashes.

Scope: read the prior NEXT-TRANSPORT-OPTION, installed-version API rationale/source-inspection receipt, new PROTOCOL/config, complete worker/browser/validator source and source contract, and all four copied lifecycle wrappers. Compared wrapper derivation hashes/diffs and inspected author-provided inert-check evidence. This reviewer did not import/execute operational code, run the pure fixtures, launch a browser, issue network requests or perform experiments. The author reports 31 passing pure validator fixtures and parser-only checks; those claims are attributed, not rerun here. Independent saved-checker implementation and later viewer behavior are outside this memo.

## Findings resolved before this snapshot

1. Required but nonenumerable envelope fields could pass shape checks and then disappear from JSON.stringify. The validator now requires own **enumerable data properties**, with an inert rejection fixture.
2. A successful return delivered after the 34-second work stop could proceed to JSON retention or exclusive output open. An explicit stop flag and monotonic guards now protect post-return validation, JSON retention and every JSON-write iteration, Buffer conversion, binary open and every binary-write iteration. Late returns at or beyond the recorded 10-second evaluate interval are rejected from persistence.
3. The evaluation counter previously advanced before readiness/retained-start checks. It now advances immediately before the only evaluate expression; failed pre-call observation cannot claim an API invocation.
4. Host phases now distinguish return validation, JSON retention, Buffer conversion and binary persistence. Finalization stderr applies the same category sanitizer as other public error records.
5. The observer's mandatory frozen-source list now includes the imported validation module. The derivation receipt records this additional adaptation.

## Checked boundaries

|Boundary|Static assessment|
|---|---|
|Single payload extraction|Exactly one explicit page.evaluate expression; no secondary evaluate, waitForFunction extraction, binding, console-data fallback or alternate encoding. The in-page latch is set before constructing its own Uint8Array and dense Array.from result. Outer permanent locks consume an interrupted invocation.|
|Network/security scope|No payload fetch/XHR/WebSocket or HTTP sink code; no permission grant, policy edit or added security flag. Launch options match the preceding diagnostic. Exact frozen HTML/script routes and navigation GETs are distinct from payload transfer; applicationFetchCalls is a source declaration, while observed request counts are separately recorded.|
|Pre-Buffer validation|Exact own envelope keys, plain-object/array prototypes, enumerable data fields, exact declared/actual length, exact array own-key count and own data descriptor at every index. Rejects holes, extra keys, accessors, typed arrays, coercible values, null/undefined, nonfinite values, floats, out-of-range numbers and negative zero before Buffer.from(actual.values).|
|Actual bytes and persistence|The received Buffer is derived only from validated returned values. The frozen expected fixture is used only for comparison. Valid-shaped wrong content still enters the sole exclusive binary-write path. Partial writes advance by actual reported bytes; zero/error writes fail; the partial file is retained. Close, length completion, actual digest, equality to returned bytes and equality to fixture are separate. No overwrite, deletion, repair or retry path was found.|
|Timeout/cleanup|Installed evaluate semantics are not bounded by setDefaultTimeout. A host race imposes the planned wait deadline but is explicitly not cancellation. Timeout/rejection/late-return paths do not extract again or persist payload bytes. Browser close is bounded; external registry/group ownership supervision remains necessary. Last substantive phase is preserved independently of terminal state.|
|Private/public separation|Public trace is a selected field projection with fixed or lexically filtered categories, numeric/Boolean fields, normalized URL/origin labels and exact allowed complete header values. Arbitrary console/error text, raw URLs, process/profile identities and private paths are excluded. Valid returned JSON has a fixed safe schema; rejected arbitrary content is omitted in favor of a bounded explicit projection with originalRetained=false. Private originals and public traces share accounting, not publication scope.|
|Lifecycle and resource evidence|Retained 60-second caller / 40-second worker / 34-second substantive / 58-second supervisor-cleanup limits, 8 MiB combined retained accounting, 2 GiB sampled RSS and 2,048-event cap. Actual exit/reap/pipe evidence, registry completeness and final scans are conjunction gates. A caller kill or browser.close alone never proves detached descendant closure. Missing receipts/ownership or instrumentation loss reject the complete claim.|

## Interpretation limits to preserve

The worker's final reread occurs before complete external closure; it cannot replace the independent saved review. The saved reviewer must independently read the received file and frozen fixture after closure and compare actual bytes, lengths and hashes. A valid wrong-content transfer may have complete local observation and exit zero while remaining a content mismatch. Invalid representations are deliberately not retained wholesale, so their precise rejected original cannot later be reconstructed independently from the safe projection.

The recorded host evaluate interval includes host return/error-event recording before the finally timestamp; it is not isolated protocol transit time. Validation timing includes validation/JSON serialization and, on rejection, may include projection retention; it excludes successful JSON disk writing, Buffer conversion and digest. Persistence timing includes local write/close and recorder effects. Browser construction uses a separate performance clock. No subtraction, zero-copy, scaling, reliability, GPU lifetime, historical-cause or physical-validity conclusion follows.

Deadline guards are cooperative and do not interrupt an in-progress synchronous OS call; the independent process supervisor and actual exit evidence remain essential. Sampled RSS does not bound transient or GPU-driver peaks. No power-loss durability claim follows from close and reread. Public artifact publication must use the declared derivatives, not private scratch/registry/exception originals. No launch at or after the original cutoff is admitted by this review.

## Reviewed byte identities

Campaign-relative operational names below identify staging files intended for exact copy into the new campaign. The parent must compare integrated bytes before freeze; later changes invalidate the corresponding part of this review.

|Path|Bytes|SHA-256|
|---|---:|---|
|`source/diagnostic.cjs`|25697|`d7d66e8ac7ea7badd33690373d2c60d5371dac3e28cec688e225d46b29339d76`|
|`source/validation.cjs`|2577|`a59775434b45cff80e5fad387e610f0fa7829cd091ca9f14f1d96c1971fe42aa`|
|`source/browser.js`|650|`9e7df97d1888bc53888291a39b89ff9cc38e37f1e32598b10415bc114fb7742f`|
|`source/browser.html`|217|`49dac6a71d8aca055ac10ea1fea38edef559be36953b2312f8470937068be82a`|
|`source/validation-tests.cjs`|2907|`a23b8e6467dfbc0c50e84dcd258c559bab5ce52ccf084fbbf3456f0870dd4a15`|
|`SOURCE-CONTRACT.md`|11827|`752e86a035ab802ada771a46cbbf0c8f2a6fc737edad6a0e819aec5deeaf7a53`|
|`STATIC-CHECKS.json`|1517|`adbfa4821a5757a2e69321fbb9ecf72de1d1718ab964e8b815c3450687c8a2cd`|
|`PROTOCOL.md`|6945|`d663f8c69886987bdb5a45d970e6eac0de955988cca6764e5f5dafe40dca63f5`|
|`config.json`|328|`87c1a5ecea1759f4bcfcfc0fafad6d4a82561e1dfdcb96183b9ba0461c61e6ed`|
|`SOURCE-DERIVATION.json`|1855|`4aabcfdeb20011bde14b575ffa40f66661f043c331a7a2f72f575b75f1c376b3`|
|`source/capture-transport.py`|13024|`51f05741774405fc5a1538fa91df6d9a763dedc89174b55e026edfa23d4c3e67`|
|`source/observe-transport.py`|32249|`a4df30adfec12452a7fdb29d79d0de70bdd53f40d807802dbcd7b9db57926ebc`|
|`source/run-once.py`|5069|`7d6d0cbdeab682cde0727a209e427420f43ed44521390b00d4479548960579c3`|
|`source/process-registry.cjs`|2737|`e9a7b179ce8d75fa70f633f553bc825636b550f1438de6e48d9a6d69ca5fae43`|
