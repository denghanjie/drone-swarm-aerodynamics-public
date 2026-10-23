# Bounded primary-source acquisition ledger

23 October 2026. Scope: static primary-source reading for the numerical contract of three-argument JavaScript `Math.hypot`, the Node `v24.19.0` source, and the gap between source inspection and an executable guarantee. Authorization capped acquisition at four search queries and six primary opens. No source code, numerical experiment or model was executed; no package, paid resource or installation was used.

**Closed totals:** four search queries in one batched search call; six primary open operations across four unique URLs, including two subsequent views of the same source file; two find operations within already opened pages. No subsequent acquisition is implied by this ledger. The prior Verlet/LAMMPS reading was reused without a new request to either publisher.

## Search record

Queries, in submitted order:

1. `site.tc39.es/ecma262 Math.hypot implementation-approximated`
2. `site.nodejs.org "v24.19.0"`
3. `site.github.com/nodejs/node "v24.19.0" "math.tq"`
4. `site.chromium.googlesource.com/v8/v8 "MathHypot" "compensation"`

Primary results included the ECMAScript 2025 clause, the official Node release-page source/index, and V8 source locations. Secondary results appeared in the returned search set but were not opened or relied upon. The Node release result identified the version and distribution links; those distribution artifacts were not downloaded or authenticated in this allocation. Search results did not establish an immutable source commit or local-binary mapping.

## Primary open record

| Operation | Requested URL or view | Outcome and substantive coverage |
|---|---|---|
| 1 | [Live Math.hypot specification page](https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-math.hypot) | Successful response, initially table-of-contents viewport; title identified a live 2027 draft. A later find exposed the target clause. |
| 2 | [Node-tagged math.tq](https://raw.githubusercontent.com/nodejs/node/v24.19.0/deps/v8/src/builtins/math.tq) | Successful text response; first viewport ended before the relevant implementation. |
| 3 | [Node-tagged v8-version.h](https://raw.githubusercontent.com/nodejs/node/v24.19.0/deps/v8/include/v8-version.h) | Successful complete short header view; source version macros read. |
| 4 | Same math.tq, requested extracted line 270 | Successful subsequent viewport; exposed FastMathHypot through extracted line 429, including the three-argument branch. |
| 5 | [Live implementation-approximated definition page](https://tc39.es/ecma262/multipage/overview.html#sec-implementation-approximated) | Successful page response, but returned viewport showed the table of contents, not the substantive definition. No definition text is treated as verified. |
| 6 | Same math.tq, requested extracted line 430 | Successful view included the entire returned file and the builtin dispatch/general loop through extracted line 474. No code was executed. |

The two find operations were: `onlyZero` on the opened numbers-and-dates page, which exposed Math.hypot extracted lines 3067–3088; and `approximation` on the opened overview page, which returned no match. The latter retrieval limitation is retained rather than treated as a successful definition verification. There were no reported HTTP/access failures and no retries outside these counts.

In the extracted raw-source view, lines are numbered from zero. FastMathHypot appeared at extracted lines 368–429, the three-argument branch at 406–427, and MathHypot dispatch/general fallback at 431–474. These correspond to ordinary source lines one greater. The cited source header begins with V8 authorship and a BSD-style license notice. Only a short exact excerpt is reproduced in [LITERATURE.md](LITERATURE.md).

## Preservation and mapping limits

The tools returned browser-extracted text. No byte-preserving copy of a remote source, official distribution archive, signature, checksum file or release build manifest was downloaded. Consequently there is **no acquired raw-source SHA-256 or authenticated source-to-binary mapping** to report. The Node URL is tag-qualified but was not resolved to an immutable commit. A hash of an extracted tool response would identify that response, not the served raw file; no such hash is substituted for a raw-source identity.

Local static reading included the previous runtime record, previously verified neighbor-list ledger, and targeted source/context text. The runtime record's SHA-256 is `74c139dd6fb007cc20fbdec1615ceec8695174b654cd8498d0d73122eec71243`; the retained literature ledger's SHA-256 is `9a514f8e340a5d4146c08d21603c4ef1a29c512e5b44dae78496309a9db52076`. Byte hashing is documentary identity work, not numerical research.

A local text search intended to locate runtime metadata was broader than intended: its output included existing audit/result-manifest text and was truncated. No new values, calculations or claims were derived from that incidental output; the subsequent read was restricted to `runtime.json`. Initial directory inspections occurred before the parent created the new checkpoint folder and reported it absent. No unrelated file was modified.

## Result of the bounded reading

The specification clause supplies no quantitative lower-error guarantee. The source describes a specific three-argument path, but the acquired evidence does not prove its error bound or establish that the identified local executable realizes that exact arithmetic. Source-level analysis, executable provenance and a moving-box-to-F equivalence argument are distinct obligations. A separate static provenance investigation may address the mapping gap; it must have its own explicit acquisition record rather than silently extend this closed one.
