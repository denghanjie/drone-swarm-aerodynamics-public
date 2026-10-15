# Static integration review: tiny WebGPU readback preparation

This review is source preparation only. It does not allocate or execute a diagnostic, saved-evidence review, browser, GPU operation or network request, and does not extend the original overnight launch cutoff. No historical campaign is reopened. The host and independent checker must remain unallocated, with null execution/review windows, throughout this preparation.

## WGSL primary-source gate resolved

The coordinator supplied the cached dated primary document. This reviewer independently read its header and targeted normative passages, and recomputed its file digest without retrieving anything from the network:

- **Title:** WebGPU Shading Language.
- **Publication:** W3C Candidate Recommendation Draft, 21 September 2026.
- **Dated URL:** <https://www.w3.org/TR/2026/CRD-WGSL-20260921/>.
- **Size:** 3,103,863 bytes.
- **SHA-256:** `9250717a0c888ce0f1bb2781a669e44ccf6e201b7e76d04fca8fe2c83926cc4c`.

This closes the specific unsigned arithmetic, array layout and byte-order source gap recorded in the preceding static review. It establishes the specification contract for the pinned fixture, not successful compilation, runtime conformance or actual output.

The verified passages define u32 as unsigned 32-bit, with concrete integer overflow reduced modulo 2^32; addition, multiplication and XOR apply to u32. They admit fixed host-shareable u32 arrays. A u32 has size/alignment four; array stride rounds element size up to its alignment. Array elements occupy successive stride offsets. Integer buffer layout places the least significant byte first and explicitly implies little endian. These rules support the intended representation; they do not establish runtime conformance.

Exact passages inspected: [6.2.3 Integer Types](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#integer-types), [8.8 Arithmetic Expressions](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#arithmetic-expr), [8.10 Bit Expressions](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#bit-expr), [6.5.2 Host-shareable Types](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#host-shareable-types), [14.4.1 Alignment and Size](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#alignment-and-size), [StrideOf](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#strideof), [element stride](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#element-stride), and [14.4.4 Internal Layout of Values](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#internal-value-layout).

For this fixture, stride = roundUp(4,4) = 4, alignment = 4 and size = 32 × 4 = 128 bytes. Prefix words 0–3 occupy bytes 0–15; active words 4–20 occupy bytes 16–83; suffix words 21–31 occupy bytes 84–127. The shader's arithmetic depends on runtime `gid.x`, so the wrapped product is XORed before the separately wrapped final addition. With `i < 17`, the shader writes only `4+i`. Raw bytes need no swapping. The initialized sentinels and expected values remain unchanged. Expected 128-byte SHA-256 is `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951`; initial sentinel SHA-256 is `944fbd39dc3fa2a2b8c9a2eef1c9c02b812911f4831b22c6c4e17cfe6a770e3a`.

The prior API-source review remains relevant: successful mapping makes this buffer's mapped bytes accessible; unmap detaches the mapped ArrayBuffer; a new ordinary Uint8Array copy made while mapped has separate ownership; buffer/device destruction API returns are not physical reclamation proof; scope nulls and pipeline resolution do not replace independent device-loss observation. That cached WebGPU API document was W3C CRD 15 September 2026, SHA-256 `7c67681430753937fd878fcbab9c2f0e93d757bdc24de6f3789ea0ff6c6f2438`.

## Integration source findings

All campaign-relative paths below refer to `research/m31-gpu-readback-integration-2026-10-16/`. These are source findings, not observed runtime outcomes.

The disabled `config.json` has version 1, scope `synthetic-gpu-readback-host`, `executionAllocated:false`, and all four launch/review timestamps null. `source/admission.py`, the host policy and the review policy require an explicit true allocation, matching identity, exact seven resource limits and valid whole-second UTC windows before admitting their operational work. The lifecycle wrappers begin elapsed accounting before the config gate and defer timers, locks, process launches and result writes until admission. No source freeze, runtime provenance or operational readiness is supplied by this static review.

`source/capture-transport.py`, `source/observe-transport.py` and `source/run-once.py` retain separate caller/observer/relay completion boundaries. Permanent exclusive locks reserve the invocation. The observer checks required frozen inputs, including the actual root `expected.bin`, before launching the relay. The relay records intent before its Node child; the browser registry records the unique detached Chrome/profile intent before spawn. The observer restricts signals to its unreaped relay group or a freshly identified registered browser group, and reports incomplete closure when ownership cannot be confirmed. A caller kill does not imply descendant closure. RSS is sampled; private process/trace accounting remains an observer report rather than something the public checker independently rereads.

The Node host has one payload `page.evaluate` call with its counter immediately adjacent. It checks the launch window and reserves a full 12-second evaluation allowance before calling it. That allowance exceeds the page's full ten-second work/cleanup interval. A timeout remains non-cancellation; a late result is not persisted or extracted again. The host serves only the frozen HTML and page source through fixed routes and blocks other application routes. Runtime checks and later process-closure evidence remain separate from page/device cleanup observations.

`source/host-logic.cjs` validates the actual decoded envelope before serialization or byte coercion. A valid envelope is retained as `raw/returned.json`; a malformed return retains only a bounded rejection projection that explicitly does not preserve the original object. `raw/received.bin` receives only actual validated byte values, including wrong values and values from a failed page run. Exclusive writes record actual partial counts and actual close results, with a work guard before every data write. Expected bytes are comparison inputs only. Browser-close return, host reread, source hashes and page phase flags do not become independent persistence or physical resource-reclamation proof.

The host's exit zero and `localObservationComplete` describe a complete local observation. They may accompany an honestly retained evaluate rejection, rejected-envelope projection, page failure or byte mismatch. The saved checker therefore must assess the actual artifacts and failure branch, rather than equating exit zero or a lifecycle candidate with a correct readback.

## Saved-file checker scrutiny

The checker uses bounded regular-file reads, rejects symlink traversal, checks stable file metadata around each read, and rejects duplicate JSON keys, non-finite tokens and negative zero. Recursive projection equality distinguishes booleans from integers. It pins required source/reference inputs and independently reconstructs the 128 expected bytes. It inventories public files against an exact allowlist, stops directory scans at 128 entries, reads retained actual return JSON and persisted raw bytes, checks their individual receipts, compares return-versus-file and each-versus-expected separately, and checks host trace/write-count projections. It does not repair a missing or wrong file.

The independently implemented page-envelope check labels phases as page self-report. Complete page failures with bytes and valid wrong-byte returns can pass record consistency while remaining unsuccessful readbacks. Settled evaluate rejection, a retained malformed-return projection and a validated no-byte page failure have separate branches. The malformed original object cannot be independently classified from its projection, and the checker explicitly says so. Incomplete/partial persistence does not receive a complete record-integrity candidate; its retained partial artifact remains available for separate failure analysis.

External capture completion, relay/observer/caller receipts, bounded trace chronology and public output-accounting equations are checked against actual saved files. Historical process closure is a recorded external observation, not a process event re-observed by this reader. A returned review summary keeps `recordIntegrityVerified:false`, requires an external reviewer completion observation, and retains `gpuExecutionIndependentlyAttested:false`. Final interpretation must combine complete review integrity with the narrow byte/page conditions; a nested byte finding alone cannot establish a complete engineering outcome.

## Corrections and final review state

| Finding | Disposition |
|---|---|
| Root config originally lacked the version/scope identity required by the host. | Corrected and reread: all admission layers now use the same identity. |
| Observer's mandatory source inventory omitted the root expected fixture. | Corrected and reread: `expected.bin` is a required frozen input. |
| Wrapper elapsed accounting originally began after the admission gate. | Corrected and reread: monotonic accounting starts before the gate; timers, locks, processes and outputs remain after admission. |
| Review JSON parsing rejected integer negative zero but accepted negative-zero floats, unlike the pinned JavaScript validator. | Corrected and reread: parse-float and page numeric validation reject negative zero and non-finite overflow. |
| Public directory inventory needed an early file-count bound and precise path scope. | Corrected and reread: scans stop at 128 entries and manifest files must belong to an exact allowlist. |
| Final output mutation guards needed to match the declared finalization deadline. | Corrected and reread: report, summary and stdout writes have guards before 29 seconds; the 30-second alarm remains armed. |
| Reviewer alarm setup preceded admission, and an existing output-directory failure could retain an output target. | Corrected and reread: alarm setup follows admission; the output target is assigned only after exclusive creation of a fresh directory. |
| Nested byte/page candidate could be true when a later source/lifecycle group failed. | Corrected and reread: renamed `pageAndBytesCandidateOnly`, with explicit conditional scope in the input contract. Overall `recordIntegrityCandidate` requires all five groups and external completion remains outstanding. |
| Python nested equality could conflate booleans and integers in reported projections. | Corrected and reread: recursive `strict_equal` is used for named shared fields, page report and browser context. |

No remaining material static blocker was identified within the inspected implemented components. This finding is not launch readiness, runtime validation or an allocation. The separate saved-review supervisor and the other prerequisites below remain required.

The host author's retained validation record reports 25 inert test cases and six syntax checks. The checker author's retained record reports 37 pure/scratch cases passed and zero failed, including the added nested boolean/integer distinction; its static record reports four AST parses only and explicitly states that the full checker main was not invoked. This reviewer read those records but did not rerun the tests, import operational modules or invoke the diagnostic or saved-evidence checker.

## Final inspected source and record identities

These hashes were recomputed from the actual integrated copies after delivery. All eight files in `review/` were also compared byte-for-byte with the author's frozen delivery and matched. These review pins are not the future complete operational source freeze. Paths remain relative to the campaign directory stated above.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `config.json` | 415 | `b028e13800c513fc966d8634753b9a9eda244e1f751133e3ce6a94bec4d33c4b` |
| `source/admission.py` | 2,522 | `54177672b4de59274d9bbc973b49ccb6220386260a1953c083ed55ed10dcf42e` |
| `source/capture-transport.py` | 13,431 | `fa905f47d571492ead718e76ca4b442be3656baceda083d08b0cc2ccbd8f000e` |
| `source/observe-transport.py` | 32,526 | `aacb3daa611f7f3893b27ebf0b6bed0ff2a434d7042d1d10f429e833cf31069e` |
| `source/run-once.py` | 5,472 | `1aea5fc37e9a17a22a1926cb7f3896ec68045e0babfdba17ee3cc6d76785cd2d` |
| `source/host-worker.cjs` | 28,543 | `43d743884a62c50d6b1eb67eee0138156e59db6e6dfb81fc46fd3d34c68b8f4c` |
| `source/host-logic.cjs` | 4,235 | `6d81f6fbcff5448d08cd9a9c2fa47eb3f5f1d3efc2451e20c3625b9b3d0175dc` |
| `source/process-registry.cjs` | 2,771 | `4391b9760f9cb4f8375b475b1cec4ef948a82534e0cd8f459cdad6ccaaaf0dd8` |
| `source/gpu-readback-page.js` | 16,295 | `2852f5e0b7fd6362fa5eced1fe2cfabfe86d103347ad6cb7aea56926e2cbfdaa` |
| `source/validation.cjs` | 15,146 | `d8a9865f5dced23c8f7564ab18a18aa0c889fe5e76026e33a3f1176fa5d11243` |
| `source/fixture.wgsl` | 284 | `64c0b55164b6dabfa2c88845913221c96bad1ad89b2c16b9aefe70134d652d59` |
| `source/FIXTURE.json` | 1,774 | `ab3cedfe660bc1afa498c6dfbdbfd38d7f89f716ac5edecce28e70d0f127f801` |
| `source/browser.html` | 235 | `a7de83bae32a843934d8084e0c0c8ec7fc20841f440043b20c900830f91cb2c4` |
| `expected.bin` | 128 | `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951` |
| `review/check_saved_files.py` | 38,838 | `83b9b3c3b619c8857f4ca39427d9036156fb281a4f6e92e3cc017e9896cc4b39` |
| `review/review_primitives.py` | 19,752 | `e36a32c78a27a9ffe5c266b3d9fa687a9ae8b2bf01c56cd79e43bca1a5f9dca9` |
| `review/byte_primitives.py` | 3,656 | `c8b24ee9ce9bf9bb364433fd065914efbafce79af6a252ca0cfd953a4ef5e7c8` |
| `RESULT-SCHEMA.md` | 6,836 | `a9d49488ab20b133921132c4509e187a8abc4b13e25a63ce817181f9fefd29c7` |
| `SOURCE-CONTRACT.md` | 6,020 | `7edf36b72047d02a9b1433628471d55ea88ee97b766676fe59dc357c689c26d2` |
| `review/INPUT-CONTRACT.md` | 9,328 | `f6ee26f3449816851a23a42716e6d228e830df0043db5f55e75cf653a73385ff` |
| `review/PRIMITIVE-DERIVATION.md` | 1,053 | `b93c15b817b521637fb4bb10bb8baae46d1e08394221948e0b6121dad4b2d6c2` |
| `STATIC-CHECKS.json` | 1,918 | `14639065709b8a9552f2600bfcb2fa5eedc5c34a0ff9fb7e4f3ed7d9a8999e2d` |
| `PURE-TEST-RESULTS.txt` | 1,618 | `a76977373da94088e9d5be19013561d9a7b2ffb7ec85fd615c461a209745a515` |
| `review/STATIC-CHECKS.json` | 4,736 | `5ee3cea7e27ef94c171d958e46c410579ef7b40fdbaa2d47dc500068bef26104` |
| `review/PURE-TEST-RESULTS.json` | 3,227 | `68eed7a03d5d2579988376451e38b5701371813628ba2e2c1c56d8213f685de8` |

## Remaining launch prerequisites

The WGSL normative gate is now closed. The package still requires a separately reviewed external supervisor for the saved-file checker, new runtime provenance, a complete source freeze and independent retrieval, and explicit future diagnostic/review allocations. The delivered config must remain false/null during preparation. A prospective invocation must produce and retain the actual caller completion evidence and final public manifest; later review must reread those closed actual files. None of those observations can be manufactured by this source review.

Even a complete positive record would concern the fixed 128-byte integer transfer in the admitted environment. It would not attest hardware execution, explain missing historical outputs, establish f32 accuracy, realistic output-size costs, general driver reliability, 5,000-agent performance or aerodynamic validity.
