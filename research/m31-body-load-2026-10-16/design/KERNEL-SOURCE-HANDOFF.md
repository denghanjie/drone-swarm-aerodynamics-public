# Body-load source-only draft

Prepared in an isolated private scratch directory; no scientific import, generation, shader compilation, GPU dispatch, root, profile or benchmark was executed. `generator.cjs` was checked with `node --check` only. Shader checks are text/structure checks, not a compiler result. Parent owns integration/freeze; final source indices and the coordinated schema are authoritative.

## Interfaces

`generator.cjs` exports `specification()` (literal protocol metadata only) and `generateFamily(familyID,{guard,charge})`. IDs are exactly 1,2,3,4. The caller invokes one family at a time. Returned fields:

- `states`: ordinary array of N ordinary 17-number arrays; authoritative original binary64 values.
- `permutation`: actual receiver/source ID -> lattice index; `inverse` and `inversePermutation` are aliases for the inverse mapping.
- `designatedReceiverIds`, `designatedSourceIds`, and paired `designatedPairs`.
- `coreFlags`, lattice-indexed `permutationDigests`, `audit` and `metadata` (aliases).

The generator uses only built-in crypto, required inside the explicit generation function. Namespace has no source-commit salt. All scientific/input work is deferred until that explicit call. No generator output has been realized during source preparation.

Failure attaches `error.partial` with `kind:'generation'`, actual allocated typed buffers, and metadata. `stateValidity[id]` distinguishes completed rows from uncomputed zeros. Metadata includes completed-state/hash/inverse/designated/audit counts, stage/context and failed family. The catch retains references only, without a second pass or failure-time numeric copy.

Successful counter totals for each family are `generatorHash=14*N`, `permutationRows=N`, `generatedStates=N`, `returnedStateRows=N`, `designatedGeometryChecks=4*designatedCount`. On failure, counters represent actual reached work. Guard stages are generation-start, permutation-hashes, frame-construction, state-generation, designated-geometry-audit, row-materialization and generation-complete. Fixed designated/core counts are 25/17, 400/298, 4500/3370 and 2500/1872.

`body.wgsl` entries are `mainBody`, `controlPairs`, `controlRoots`, all workgroup size64. Main bindings0..5: constants32u32, nodes8u32/N, offsets4paddedvec3/N, nominal4u32/N, policyu32/N², output64u32/N. Stored nodes are `[px,py,pz,pad,ax,ay,az,pad]`; internal constructor mapping is explicit. Controls use only constants0, fixture input6 and output7, each64u32/fixture. The fixed control ABI and 256/480/288-byte record layouts are in `schema.json` and `design/INDEPENDENT-REFERENCE-REVIEW.md`.

Main firstFailureSlot is row-local source*4+rotor for field (center rotor0), rotor for root, component for body, zero for admission; success is0xffffffff. Header receiverID supplies row identity. All four roots are attempted after a complete field before the all-root-terminal bit is set. Signed final update is nextX-previousX. Masked numeric payloads are positive zero. Field partial sums are not exposed as complete root inputs; policy-prefix evidence and header counts remain available on failure.

The caller must provide newly zero-initialized policy/control-output storage for each case/batch. A receiver writes each visited pair policy word once, including any partial terminal word on failure. Unvisited words remain zero/unwritten; reusing uncleared policy storage would invalidate this contract.

## Static constraints

The input design and conditional geometry proof are in `design/INDEPENDENT-INPUT-DESIGN.md`. Candidate host preparation must use the production double-cross rotation; independent R uses its matrix rotation. This source generator uses the latter for the construction/frame and designated input audits only. It does not prepare a substitute Q interface or evaluate fields/roots.

One ordinary-f32 A path only; fixed source strength; ascending sources; four serial rotor accumulators; no full-term raw or L1/reduction certificate. Signed zero and positive subnormal nominal/U canonicalize to+0 with flags. Normal positive roots get12 updates; vi and high r must be normal positive, solved x>0; high-rzero is invalid. Low alphazero/subnormal stays flagged and still receives12 updates. Nominal yaw/body are assembled from canonical nominal values.

The separate science300s / saved-review120s envelopes are not launched or exercised by these files' source preparation. GPUraw208MiB, retained corpus768MiB and processRSS4GiB remain integration caps, not proof of execution feasibility.
