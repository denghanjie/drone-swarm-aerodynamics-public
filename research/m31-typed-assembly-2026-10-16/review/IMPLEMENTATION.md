# Typed receiver-row builder: source-only implementation

Implemented the adopted `BUILDER-DESIGN.md` in this isolated directory. No module was imported, no fixture or state was constructed, and no numerical, diagnostic or timing workload was executed. JavaScript validation is syntax-only (`node --check`). Correctness and performance remain unqualified until a separately frozen and authorized campaign.

## Files and interface

- `kernel.cjs`: new matched scalar-lean and typed assembly paths.
- `anchor-kernel.cjs`: byte-identical copy of the frozen kernel, SHA-256 `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a`.
- `reference-excerpt.cjs`: byte-identical frozen reference, SHA-256 `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e`.

Exports retain `constants`, `build`, `schedule`, `fullGraph`, `solve`, `residual`, `query`, `cached` and `checksum`. The solver, graph-depth calculation, residual, cached query and checksum exports are the original anchor functions.

| Operation | Behavior |
| --- | --- |
| `build(states, 'all', fullSymbols, guard)` | Delegates directly to original all-pairs builder. |
| `build(states, 'grid', fullSymbols, guard)` | Preserves original API by direct delegation; not a proposed new campaign arm. |
| `build(states, 'lean', fullSymbols, guard)` | Shared scalar classifier with ordinary row tuples, Set dependencies, boxed global source/K arrays, then typed CSR. |
| `build(states, 'typed', fullSymbols, guard)` | Same classifier; N-capacity typed rows, fixed 4,096-entry typed chunks, unique ascending dependencies, then independently owned typed CSR. |
| `query(states, 'A', guard)` | Direct original all-pairs+ordered query, unchanged clocks and code. |
| `query(states, 'L' or 'T', guard)` | Corresponding new builder plus original ordered solve, residual and checksum. |
| `query(states, 'B' or 'C', guard)` | Delegates to original API for compatibility; not part of proposed A/L/T comparison. |

L/T return the original canonical fields and an additional `assemblyStats` object. This object is descriptive construction metadata and must stay outside canonical matrix, graph and solution fingerprints. Both L/T certificates are exactly the original all-pairs certificate, including `reason: 'all-pairs-selected'`; no grid-certificate difference is used to excuse a canonical mismatch. A is not modified to attach new counters.

## Preserved and changed operations

`prepare` is copied verbatim from the anchor; a source-text comparison confirms equality. Rotation grouping, original states and rotor identities, nominal forces, S0 totals and input admission remain unchanged. Both new arms compute the four `p_center + offset` points once per receiver in Float64 scratch, read source position/axis scalars once per eligible source, and inline the same four-rotor scalar classifier. They share a lazy projection cache: the dot product is computed only at the first rotor reaching the original projection branch. No projection-based early rejection is introduced.

The exact center guard runs before the strict radius skip. Rotor invalid, down, near-field, radial-support, projection, speed and scaled-cap branches retain their order and parenthesized arithmetic. The complete `i -> j -> rotor` scientific evaluation order remains canonical. Each rotor is classified and consumed before the next rotor is evaluated; computing four classified outputs first would have moved positive-cap failure past later work, so this implementation uses scalar scratch values inside the shared rotor loop instead. Full symbol storage and the complete symbol census are retained at `[i,j,r]` indices.

L retains ordinary `[j,K]` tuples, a Set, dependency sort and boxed global source/K accumulation. T removes those coefficient representations: append positive K to its rotor's typed row, and append j to that receiver's ordinary dependency array once after processing the source's four rotors. Ascending j already gives unique sorted dependencies. Dependency output arrays retain the anchor's public representation and own their contents. T does not introduce a dense coefficient matrix or a second geometry pass.

Both arms increment the global positive-term count immediately after the positive append, reject `> 2,000,000` before later rotor/scaled-cap work, and preserve the existing error text. N is a structural row capacity, not a positive-term budget: an impossible row overflow throws instead of truncating. The identical K-to-a expression, canonical row/source order, ordinary-bound summation, graph eligibility, source-S0 model and anchor solver remain in place.

After each receiver, T copies four row prefixes in rotor order through its fixed chunk writer. At finalization it allocates exact-length source/K arrays and copies every used chunk prefix once. No result aliases a row or chunk view. Chunk references are released after copying, with no claim about garbage-collection timing. Each build owns its scratch; retaining an earlier result while later builds run cannot mutate its CSR through this implementation. Input `states` references retain the original anchor's semantics.

## Assembly counters and payload accounting

Let N be vehicles, M retained positive rotor/source entries, and C=ceil(M/4096), with C=0 when M=0. All counts below describe source-level operations or typed backing payload, not observed heap allocation, GC cost, resident memory or speed.

| T field | Meaning |
| --- | --- |
| `rowCapacityEntries` | N per rotor row; four ID and four K rows. |
| `rowLengthsAtLastReceiver`, `maxRowLengthEntries` | Logical lengths; unused row tails are never copied. |
| `rowGrowthCount` | Zero; the eight owning row arrays are allocated once per build. |
| `rowScratchIdBytes`, `rowScratchKBytes`, `rowScratchBytes` | 16N, 32N and 48N payload bytes. |
| `rotorPointScratchBytes` | 96 bytes common to L/T. |
| `chunkPolicyCapacityEntries` | Fixed 4096, not selected using results. |
| `chunkCount`, `chunkGrowthCount` | C allocations of chunk pairs; max(0,C-1) subsequent pair additions. |
| `chunkTypedArrayAllocations` | 2C owning typed arrays; ephemeral subarray-view objects are not counted as backing allocations. |
| `chunkCapacityEntries`, `chunkUsedEntries`, `chunkSpareEntries` | 4096C, M and 4096C-M logical ID/K pairs. |
| `chunkAllocatedPayloadBytes` | 12*4096C. |
| `rowToChunkCopySegments`, `chunkToFinalCopySegments` | Prefix-copy segments; each segment makes an ID copy and a K copy. |
| `rowToChunkCopiedEntries`, `chunkToFinalCopiedEntries` | M each, counted as logical ID/K pairs. |
| `rowToChunkCopiedBytes`, `chunkToFinalCopiedBytes` | 12M each. |
| `finalSourceBytes`, `finalKBytes`, `offsetBytes`, `scalingBytes` | 4M, 8M, 4(4N+1), and 8M if nominal inputs admit scaling. |

`finalizationOverlapKnownPayloadBytes` sums the row scratch, 96-byte point scratch, offsets, all chunk payload and final source/K payload while the final copies coexist. `allocatedAssemblyTypedPayloadBytes` additionally counts the later scaling array; it is a cumulative allocation accounting value, not a measured simultaneous peak. Prepared geometry and optional symbols are reported separately as `commonPreparedGeometryBytes` and `commonSymbolBytes`. JS row/tuple/Set/dependency containers, chunk-list/view objects, nominal arrays, object headers and runtime overhead are unmeasured.

For L, typed row/chunk counts and bytes are zero, ordinary row capacity/growth are unknown (`null`), and logical tuple/Set/global-entry/copy counts are reported. These counts are cumulative source-level constructions, not simultaneous live allocation counts. L's typed-payload accounting deliberately excludes its unmeasured ordinary-array storage. Do not compare that partial number with T as a total-memory result; later supervised RSS and native memory metrics would be needed.

The metadata is assembled inside the full query and contributes to its total/remainder time. L/T share the same scalar implementation and common counters; T-specific copy/allocation counters belong to the proposed assembly mechanism. A remains the external immutable anchor. Source operation differences predict neither V8 allocation behavior nor a speedup.

## Static verification and pending work

All three JavaScript files passed `node --check` using the available bundled Node parser with inherited `NODE_OPTIONS` removed for that syntax-only command. No require/import was evaluated. The first PATH-based parser lookup found no `node`; it did not launch anything, after which the known bundled executable was used. Immutable anchor/reference byte equality and copied preparation text equality were checked by ordinary file reads.

Pending a separate authorization and freeze: independent source review, fresh-input generation under its own declared scope, full A/L/T symbols/CSR/domain/graph/solution equality, guard cases, owned-buffer retention controls, logical capacity/copy assertions, and bounded complete-query comparison. No equality or throughput finding is claimed by this implementation delivery, and no old allocation is reopened.
