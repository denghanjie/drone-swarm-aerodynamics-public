# Independent evidence and correctness-bridge source review

**Disposition: accepted for prospective source freeze, with no remaining evidence-review blocker in the versions pinned below.** This accepts the declared source design and saved-input bridge. It is not a numerical result, a permission to bypass the publication gate, or a claim that the browser attempt has succeeded. The frozen manifest, public push, and exact public verification must precede the sole numerical launch.

Reviewed on 18 October 2026, with final source inspection and export-closure hashes completed at approximately 12:06 UTC. This reviewer read source and retained JSON metadata and computed file hashes/lengths only. The reviewer did not import or execute the exporter, decoder, browser harness, supervisor, analyzer, initializer, controller, native query, derivative, integration, or reference. The parent reports that the one saved-only export completed under an external 30-second timeout with `-I -B`; this review independently checked its source, receipt, and referenced-file identities, without repeating it. No old artifact was edited. This review is the reviewer's sole new output.

## Exact reviewed versions

Paths below are relative to `research/m31-cost-decision-2026-10-18`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/export.py` | 3,414 | `5f3069485d0ca5df1419a1b4eaccf79168e9775e5fc62fa28c4807622489e791` |
| `source/browser.js` | 11,856 | `de39b438747f4c598531285f93120f1f155c35c0b48c924f6ee67c4760a535da` |
| `source/run.cjs` | 4,930 | `57674c93abc8ab55d77804b2bcf8121bf70315ac3a4762f9e7f6c21dbac70339` |
| `source/supervise.py` | 2,230 | `acfe8a2edad33ddeae1e1da5006483d98156d6f41d62aa0947abdf14241f0236` |
| `source/analyze.py` | 5,239 | `8a3db4eb15901e6e58616c2d45349bc530c09ee1650a1121953653f2ac8714f7` |
| `PROTOCOL.md` | 7,581 | `23722fbf799ea52972a17b1d35d41913d47864fb2dd41171e3c8131ca529ee27` |
| `EXPORT.json` | 5,478 | `89fe9502d2b99f678f4c193ed0a632d7cbdbebb686ee9b9bd3a8dbaf0f0df5a0` |
| `expected.json` | 2,554,204 | `e135b68c15c0198cc72c833c0b28d018353f016dcae30ab4cbe5e95d060cde1e` |
| `input-words.json` | 343,903 | `e007c459fd1ab1a796a27b6455f4ee3bfe27766fb63ff9e65a4f679a75b18d0f` |

The host comparison removes only the baseline file's final newline. Its actual comparison bytes have length **2,554,203** and SHA-256 **`baee267d0d463ff059f8e61575c8a60f395d9713f9ac8a8a8325875f7c8408d7`**. The file pin and the eventual actual-output semantic pin therefore intentionally have different lengths and hashes. This review independently confirmed that no other byte is removed by that trimming.

## Saved-input provenance

The exporter binds the old `research/m31-native-tree-state1000-2026-10-17/result-manifest.json` to SHA-256 `59be1b771384587262d9925742e7ae9bb865b15b952cb3f2e23ea9d4b075749d`, 434,148 B. That manifest pins the old successful checker to 6,326 B / `b1a7d6144c24f25c7e6cc13e1a6617092da65310c797f8728d8eda2ff8626619`. The exporter requires the single case `tree-t0-n1000-a` and F descriptor SHA-256 `2c1dacc72cb00ab1685233fd2385518e6df66993bd0175f3e8b3d2f858e50bd9`.

The retained decoder is `research/m31-native-tree-browser-probe-2026-10-17/source/compact-check.py`, 18,319 B / `87229101f84c877d70fcadabfde1cf2b88bb530476eefe9dd89da478a7796bee`. Inspection of its `Resolver` confirms bounded descriptor/chunk decoding, per-pin size/hash checks supplied by the exporter, exact byte/element accounting, lossless hex-word decoding, and preservation rereads. The module imports standard-library readers and does not execute a scientific producer merely by being loaded. The exporter's `sys.dont_write_bytecode=True` prevents its import from creating bytecode in the old package.

`EXPORT.json` records `savedOnly: true`, `producerCalls: 0`, 22 read pins, the old result-manifest pin, the two generated-file pins, and 15.74005079176277 seconds elapsed. This reviewer rehashed **all 25 unique files** in the receipt's read/result-manifest/output closure; every size and hash matched. The receipt's elapsed time is a retained parent/exporter measurement, not a repeated timing by this reviewer.

The F record's `raw` field is the **already projected input** passed to the old native query. It must not be confused with the old stage's `rawBeforeProjection`. The old frozen scientific checker binds F.raw to `stage.nativeInput`, stable IDs, the canonical input digest, and the single qualified first projected state. The current exporter takes `native.raw` directly, without a seed regeneration, fresh projection, controller call, or derivative computation. Qualification of that relationship is inherited from the pinned old checker; this source review does not rerun its arithmetic.

## Exact semantic comparison

The fixed selected fields are `diagnostics`, `status`, `reason`, `constants`, `raw`, `ids`, `prepared`, `coefficients`, `solution`, `loads`, and `consumption`. Both independent Python export and browser normalization exclude exactly these historical diagnostic paths:

- `diagnostics.buildPhasesMs`
- `diagnostics.geometryWork.gatheredNonselfCandidates`
- `diagnostics.screen.orderedPairVisits`
- `diagnostics.screen.componentTests`

Other selected diagnostics remain in the comparison, including admission, graph/schedule, residual, and work fields retained by the original equivalence check. Method labels, timing, and tree-witness representation are outside this declared projection. Schema/model identity follows the pinned producer source and provenance; it is not an additional compared semantic field.

The transport decoder leaves scientific word strings as 16-character lowercase hex. The exporter converts remaining numeric values, including numeric IDs/counters, to big-endian binary64 hex with `struct.pack('>d', ...)`; booleans, nulls, strings, arrays, and object structure are retained. Browser normalization uses a DataView with the same byte order. The comparison is exact equality of this explicitly normalized projection, with no numerical tolerance, rounding, scalar reduction, or checksum-only substitute.

Each call reconstructs a fresh ordinary Array input using DataView decoding of the saved state words. This preserves signed zero and conforms to the frozen query's dense 17-element Array requirement. The supplied IDs remain numeric in the input file. The actual submitted input is converted back to words after the query and compared to the saved input, detecting caller-input mutation. The native F implementation is loaded separately from the original `native-load.cjs`; H/H0 use the frozen `native-tree.cjs`, which accepts those tree methods. No prepared state or built tree is reused across calls.

Every completed query is encoded outside the measured query interval. On a success path all selected fields must exist, the entire canonical output must equal the saved baseline, the input must remain unchanged, and status must be `native-success`. This applies to all 16 warm-up calls, all 96 measured calls, and all four instrumented diagnostic calls, rather than a sample or only the first call.

The host receives the **full actual canonical semantic string for every call**. It independently compares bytes and SHA-256 with the baseline, writes an exclusive content-addressed blob for a new output, and verifies exact existing bytes before deduplicating. Every query row retains that blob's path, size, and SHA-256. The later Python analysis independently rereads and rehashes each of the 116 referenced blobs and requires exact baseline bytes. Sharing one blob after 116 byte-identical outputs does not replace those 116 comparisons.

## Failure evidence and preservation

The first draft could throw on absent success-only fields or null diagnostics before recording a refused query. The reviewed revision resolves this: it builds the available projection, records missing-field inequality, safely accesses optional timing/diagnostic metadata, and sends the encoded refusal/failure body along with the semantic bytes before stopping. A differing semantic blob and its query row are persisted before the host throws on mismatch.

The additional refusal/encoding body shares a 12 MiB failed-call allowance with the semantic blob. If that body would exceed the allowance, the host retains an explicit `failure-body-limit.json` receipt. A payload beyond the primary output cap or a failure before a query returns cannot be promised complete capture. The protocol now states this limit rather than promising universal complete failure evidence. No failure triggers another scientific attempt.

The earlier missing post-run preservation check is also resolved. The analyzer checks the source-manifest hash against the publication receipt, requires the receipt's remote/local equality flag, and rehashes every manifest file before accepting results. The frozen manifest must include these exact sources, protocol, exported baseline/input and export provenance, the old saved-record dependency closure, and the exact reused browser bundle. The runner checks its manifest pins before launch. Those manifest and publication artifacts are still prospective at this review's close; their contents and public equality must be established by the parent before execution.

## Timing schedule and analysis

The four cyclic orders are F/H/H0/HC, H/HC/F/H0, HC/H0/H/F, and H0/F/HC/H. Four warm-up blocks precede 24 measured blocks, with each measured block containing each arm once and each arm occupying each position six times. The four final diagnostic calls are F/H/HC/H0. Source loops and the independent analysis require 116 total calls, 116 query files, and 116 transfer files. The analyzer checks call number, kind, block, position, arm, transfer-call binding, successful closure, and all complete semantic comparisons. A failure file prevents acceptance.

H disables tree-witness capture, HC enables it, and H0 disables capture while traversing without group omission. The diagnostic wrappers affect only the final four calls and are restored in `finally`; they wrap the actual tree module's build/gather functions. Their scope includes combined gather/traversal/sort/capture activity and does not separately identify every subcomponent. They are excluded from primary decisions.

The **primary outer time includes fresh binary64 input decoding and the submitted-input immutability check**, as well as the full native call. It is therefore a declared call-boundary cost, not solely the native internal timer. Native internal timing is retained as a secondary measure. The immutable native implementations still perform prepared-evidence construction, validation/admission, geometry/tree work, solve, residual, loads, and complete load/ID/status consumption. Witness-disabled H is not a newly stripped solver implementation.

Evidence encoding, semantic comparison, host transfer, and persistence follow the primary query timer. Persistence is included in the recorded transfer interval and must not be added to it again. The analyzer validates finite nonnegative native, phase, build-phase, encode, comparison, transfer, and persistence values; query time must be positive and below the fixed bound. Instrumented subphase measurements remain diagnostic reports and do not determine the decision.

The analyzer forms all 24 paired H/F ratios from matching measured blocks, uses the arithmetic mean of the middle two sorted ratios as the even-N median, and counts only strict H<F wins. The gate is exactly median ratio <=0.90 and at least 20/24 strict wins, contingent on all correctness/closure checks. It retains every pair, per-arm distributions and position medians, and HC/H and H0/F ratios. There is no outlier deletion, adaptive repetition, forced GC, or averaging of independently chosen unpaired populations. Phase medians are not summed into an asserted total.

The result can concern only this saved projected N1000 state, one browser process and warmed repeated queries. F already uses component screening. It cannot establish a generalized speedup, browser frame rate, trajectory performance, high-precision accuracy, physical validity, or novelty. Even a passing gate warrants only further investigation under the declared decision rule.

## Allocation and remaining launch gates

The current protocol allocates a new 11:57:26–13:57:26 UTC cycle on 18 October; it does not reopen the consumed 17 October execution. The saved export is single-use through an exclusive lock. Source review finds no new initializer/controller/derivative/reference/integration calls in the timing harness. The browser allocation is one attempt with at most 116 native calls, an exclusive result/private directory, a 180-second watchdog, and no retry. Export and analysis each rely on the declared external 30-second wrapper as well as cooperative guards.

Prelaunch admission checks expected.json <4 MiB, input <1 MiB, the old bundle <2 MiB, and prepared package <12 MiB. The inspected export sizes satisfy the first two. The supervisor monitors 32 MiB public and 128 MiB private disk limits and checks again after root exit. These are disk allocations, not OS memory limits or a zero-overshoot filesystem quota. The source records root process exit/close separately and does not claim every helper's exit has been verified. Private profile contents and log bodies are not part of this review or its publication.

The protocol's separately declared saved-only UI allocation is acknowledged; viewer implementation and `source/ui.cjs` are outside this five-source evidence review. This review does not assert that its UI checks have run or passed.

No numerical execution was performed by this reviewer. Launch remains contingent on freezing these versions and the dependency/input pins, completing the other independent protocol review, and establishing exact public source-manifest equality within the stated cutoff. Any later change to these reviewed sources requires an updated source review or an explicit review of the changed portion before launch.
