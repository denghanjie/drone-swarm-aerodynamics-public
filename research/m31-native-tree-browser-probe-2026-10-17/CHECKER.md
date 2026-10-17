# Independent saved-evidence checker

This document describes the prospective checker source. It records no new execution or result. The frozen governing decision is `../m31-native-tree-design-2026-10-17/review/NEXT-EXPERIMENT.md`. Source and runtime publication, the live supervised attempt, and the fixed cutoff must pass before these entry points execute.

## Entry points and limits

`source/validate-saved.py` performs a single saved-data gate before fresh browser initialization. Its entire child allocation is 15 seconds within the shared 60-second overhead allocation. It reserves the last 3 seconds for preservation and durable closure. `source/reference.py` has 600 seconds, reserving 30 seconds for closure. `source/check.py` has 180 seconds, reserving 15 seconds for closure. These reserves reduce useful computation; they do not enlarge any allocation. Deadline or output exhaustion is terminal, without sampling, retry, larger caps or a weaker proof.

The Python entry points verify the enabled configuration, fixed 120/600/180/60-second envelope, live run token, stage allocation, publication preceding the attempt, exact source manifest, private-directory binding and isolated pinned Python executable before importing scientific helpers. The checker imports only frozen saved-word arithmetic/coverage functions and the new decoder; it never imports the browser/native producer. Only the reference entry point calls the unchanged prepared exact-reference procedure, and only on four 64-drone saved stages.

## Full transport reconstruction

Each journal row has a contiguous zero-based sequence, kind, exact `results/records/NNNN-kind.json` pin and three finite nonnegative transport timings. Each descriptor is at most 2 MiB, contains at most 128 distinct named fields and refers to typed field streams. Every nonfinal shard is exactly 1 MiB; the last is positive and at most 1 MiB. Shard paths are content-addressed and every first decode verifies exact lengths and SHA-256 before interpretation. Ordered shard concatenation is mandatory.

Streams and records have fixed limits: 96 MiB binary bytes, 16,000,000 decoded elements, depth 64 and a bounded declared logical-JSON diagnostic of 256 MiB. Numeric scalar/array tags must decode finite binary64 values. Hex-word tags preserve all 64 bits, including signed zero and nonfinite bit patterns represented as words. Strings use strict UTF-8. Integer-array tags preserve exact unsigned integers. Empty optimized arrays, duplicate object keys/record fields, unknown tags/descriptor fields, wrong chunk boundaries, truncated/trailing bytes and incorrect element or byte totals fail. Element counts include containers, scalars and object keys. Optimized arrays include each scalar's depth and element count.

The `jsonBytes` value is a bounded producer diagnostic. Python does not claim to reproduce JavaScript number-to-decimal formatting. Binary bytes, literal words, decoded values, structural lengths and element counts are checked independently. There is no compression.

Actual independently encoded equal field streams may share immutable shards. The decoder caches only a previously verified identical ordered pin/length/element identity, after revalidating all descriptor and chunk fields even on a cache hit. This permits shared object identity to accelerate subsequent equality checks. It does not substitute a producer equality flag for data. The cache is cleared after each stage/case; every used record and shard is rehashed before a passing result. Completed prerequisite output indexes are bound to the supervisor's recorded output hashes and rechecked at closure.

Disk caps remain 32 MiB per file and 256 MiB combined results/private logs/profile/scratch, including closure allowance. The stream cap is a logical decode bound, not permission for a 96 MiB file or an aggregate-cap increase.

## Exact compact tree proof

The checker rebuilds the entire deterministic tree from saved raw center words using the frozen independent constructor. This preserves rounded widest-axis widths, lowest-axis ties, stable canonical-ID sorting, floor-median splits, capacity-eight leaves and signed-zero extrema. Every saved node, bound and leaf member must equal that reconstruction. All canonical IDs and every receiver are present.

For each receiver, the leaf dictionary expands to actual visited leaves. Each dictionary entry is ordered, distinct and used. Actual gathered indices have one canonical runs/literal encoding: increasing nonoverlapping maximal runs only when two integers per run are strictly shorter than the literal sequence; ties use literals. The decoded bitset must equal the union of visited-leaf members and include self exactly once. Culled subtrees must be disjoint from one another, retained members and self. Their union with retained members must equal the complete source set. Thus every retained and omitted source is covered; no receiver/source sample substitutes for the partition.

For an endpoint difference x, exact nearest-even boundaries are:

- RN(x) >= 4 exactly when x >= 4 - 2^-52.
- RN(x) <= -4 exactly when x <= -4 + 2^-52.

Both midpoint ties select the even word at magnitude four. Coordinates are decoded as exact dyadics and scaled to integers with at least 52 fractional bits. Sorted coordinates and inclusive/exclusive prefix masks form each node's six ordered successful-predicate sets. The order is minimum-x, maximum-x, minimum-y, maximum-y, minimum-z, maximum-z. Each saved cull must use the first successful axis/side and its exact frozen RN subtraction word.

Receiver ancestry masks recover every visited node. For each visited-node mask, remove the receivers succeeding at each ordered predicate and count the remaining set before each test. This obtains all node-visit and endpoint-comparison counters, including H0's first-success test cost despite its disabled omission. H requires the exact successful cull masks; H0 has no culls and retains all sources. Partition plus ancestry and first-success checks forbid descent below an earlier successful H cull. Monotonic rounded subtraction and the reconstructed extrema prove the cull for every descendant.

Fallback retains all pairs and requires the exact independently determined reason, empty tree/receiver/dictionary payload and exact zero tree counters. Every tree and work counter is checked. This replaces N-by-node Fraction subtraction and repeated N-by-source coverage expansion with exact integer/bitset work; it does not relax coverage.

## Native payload and coupled dynamics

The complete ordered browser journal is required: source, factories, twelve wiring controls, then four fixed cases with initial/controller records, four groups of three native records plus their stage, one step, safety and case summary, followed by the driver summary. The checker independently binds the exact bundle/source slices, all eighteen executed factory IDs in order, the local wide-factory shim and all 56 adapter assertions before scientific factories.

Every stage has the registered case/seed/stage grid and method order. All three methods bind the same exact native-input digest and successful unchanged-input record. The entire semantic native payload must agree, including raw/prepared values, positive CSR source order and coefficient words, solution/root words, loads, status, graph/admission diagnostics and residuals. Only method/tree/timing metadata and the explicitly registered gathered-candidate, screen-pair and component-test work differences are excluded. The whole diagnostics object is never dropped.

The F payload independently receives raw/prepared/stable-ID, complete CSR, positive-word, solution/load and full consumption-digest checks. Exact full-payload equality transfers these checks to H/H0. H/H0 independently receive their full tree proofs. Logical work remains N(N-1); saved work counters are bound to actual partition cardinalities. Native residual gates remain 1e-9 and 2e-9.

H's actual delivered rotor/collective/world-force/world-moment words must equal each derivative's consumed words. The inherited exact rational nearest-even auditor checks every projection, square-root rounding cell, norm division, force acceleration, body moment conversion, nominal yaw, gyro term, quaternion derivative, nominal motor state and motor lag. It checks all four stage inputs, fixed commands, RK weighted sums, accepted endpoint projection and exact state/ID chains at every N.

There are 44,256 primary drone-stage derivatives, plus six fixed wiring derivatives: 44,262 audited derivatives and 752,454 scalar derivative components. Literal input/load/identity words remain exact. The inherited rational arithmetic auditor identifies positive and negative zero numerically for its arithmetic comparisons; this narrower zero-sign convention is recorded explicitly.

Controller scope is deliberately narrower: pinned unchanged controller/Grid/initializer provenance; complete actual saved state and neighbor IDs; sorted, unique, in-range neighbor IDs; stable-ID/command consumption; exact elementary target-height/velocity arithmetic and command clamps. There is no fresh independent all-pairs neighbor-membership/exclusion recomputation at 64, 1000 or 5000, and no new transcendental steering oracle. Initial states are the actual pinned initializer outputs, not independently regenerated samples.

## Four exact references

Only the four ordered `tree-t0-n64-a-step0-k1` through `k4` saved projected states enter the unchanged prepared reference. The count cap stays 180, interval precisions stay 192/192 bits, root bisections stay 128 and suffix budget stays 30,000 per stage. The realized full scalar maximum is 16,128 per stage; four stages cover 64,512 logical rotor/source pairs. There is no 1000/5000 reference or subset substitute.

The checker audits complete reference coverage and prepared-reuse counters, then applies the unchanged normalized 1e-8 rotor, collective, world-force and world-arm-moment category gates, body-frame reference bound and conversion-only frame bound. Reference refusal cannot pass.

The inherited compatibility field `inputFile` deliberately points to the actual stage transport descriptor pin; all of that descriptor's shards are decoded and verified. It is not a fabricated raw-input JSON sidecar. `inputSha256` separately binds the canonical `nativeInput` word object, and the reference's full saved input must equal it.

## Cost and interpretation

All 48 query times and fixed method orders are reported. Common projection/input-evidence/derivative, initialization/controller/RK/endpoint/safety work, encoding, semantic comparison, serialization, transfer, persistence and all-arm wall times remain visible. Every duration is finite and nonnegative. Source/factory journal timing is retained. Driver and case summaries bind to the underlying records. Host journal transfer/persistence timings precede final descriptor/journal acknowledgment, so final append times must be at least those values, not artificially equal to them.

Full payload validation costs at least O(actual saved CSR entries + state words); exact derivative/RK checks still cover all drones and can dominate. Compact proofs remove specific redundant quadratic Fraction loops, but no runtime guarantee is claimed. A fixed deadline failure is an operational limitation, not justification for skipping rows.

`passed` means the full correctness/transport/stage proof succeeded. The separate `engineeringPassed` requires fewer gathered nonself candidates and a four-stage H/F query-time ratio at most 0.80 in each of the two 5000 cases. A correctly checked negative engineering outcome is a normal completed result. A native-equivalence pass at large N establishes neither independent exact-load accuracy there nor a standalone 2.5 ms production step.

## Dependency closure

The complete exact helper path/hash map is `MODULES` and `FIXED_PINS` in `source/reference.py`; these values are checked before imports. It includes the frozen native-tree checker, coupled-stage checker, native arithmetic checker, prepared coverage auditor, pair/semantic/tree/prepared references, reference spec and existing saved fresh64 input. The saved gate additionally fixes the old tree `source/cases.json`, `results/work.json` and all 126 original native sidecars listed by that work index. Every sidecar must be in the new source manifest with the exact old pin. No frozen package is edited.

## Source review boundary

The checker author separately reviewed the candidate collector and adapter source authored by the candidate agent. Read-only textual comparison found the embedded kernel equal to the frozen `kernel.cjs` after changing only its export to the enclosing return. The wrapper tail differs from the frozen native wrapper only in compact tree serialization and null-preserving partial capture. Tree construction, first-cull arithmetic, gather ordering and traversal are unchanged; the added collector encodes the actual array before returning that same array and interns leaves only after full equality. The old/new adapter diff preserves projection, nominal loads, binding, force/body-moment/yaw/motor consumption and RK expression order. The new three-arm loop copies inputs inside each timer, captures each actual result, persists before rejecting a semantic mismatch, and drives the derivative from H only after all arms agree.

The checker author reviewed the midpoint/partition argument and the full derivative/RK and four64 reference boundaries described above. This is a source review, not an executed numerical qualification or a self-issued independent certificate for the new checker. A separate candidate-author review covered the new checker integration, identifying the optimized-array depth and codec-result-field mismatches before closure. Parent review and parser-only validation remain separate prerequisites to a published freeze; actual saved-data qualification remains a supervised pre-exposure prerequisite.
