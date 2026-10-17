# Source diff inventory

This receipt describes source-only changes owned by the protocol implementation author. Textual `diff -u` was inspected against the retained files; no candidate import, syntax execution, numerical test, browser, network, bundle execution, Git operation, or benchmark was performed.

## Owned draft files

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `source/native-load.cjs` | 17214 | `05d9fcb5aa9fc8d3f4812a14e469096f5c3d6110b18f7b164496df7e21dd530b` |
| `source/kernel.cjs` | 16690 | `42cb6deeb32e9b5bd633679d3ea58489940009a9f77f690a0368b6f22de2a971` |
| `source/tree.cjs` | 4362 | `23e7b4393321d4a6cc83906a2d02319dd7a37b2a2f63ae165fe4558eca73f422` |
| `IMPLEMENTATION.md` | 13066 | `0d9899dc0536d365c1b80c07875e61a9aebda796d2dd53aa04e939a123b1debd` |

These hashes are draft identity pins for parent review, not an execution manifest. This inventory does not self-hash. The parent must include final reviewed versions and all peers' source files in any later frozen manifest.

## Native wrapper diff

Base: `../m31-native-fresh-transfer-2026-10-17/source/native-load.cjs`.

1. Line 5 points `require` at the candidate `./kernel.cjs`.
2. `query` at line 205 defaults to H, accepts H/H0, and adds a trusted optional fourth argument. Existing input/guard validation order is preserved.
3. The build call selects H/H0 directly and adds a requested-evidence sink. The sink adds canonical stable IDs to the tree record and retains partial coverage if build throws.
4. Line 266 attaches the optional `tree` field after the original success/refusal result is assembled. Original timing instrumentation remains, but is outside equivalence comparison.
5. `encodeEvidence` at line 303 adds `tree` encoding: endpoint/difference floats become 16-digit words; node members, receiver leaf/gathered arrays, canonical IDs, and counters are copied.

All constants, limits, data-property checks, canonical input copying/sort, validation helpers, prepared geometry/normalizers, native schedule/solve/residual calls, error translation, load and moment arithmetic, full-load-word consumption, and existing evidence field encodings remain unchanged. The F comparator itself remains the original module and has no route into these new methods.

## Kernel diff

Base: `../m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs`.

1. Header identifies the source-only fork. Requires point to the three retained numerical dependencies; `./tree.cjs` is added.
2. `buildAssembly` accepts optional evidence settings. The whole-scene `screenPredicate` and its call remain unchanged. The legacy unencoded certificate reason changes from `all-pairs-selected` to `center-tree-selected` to avoid mislabeling H.
3. Requested coverage is created after the predicate and published to the sink. Ineligible scenes retain the original `lean.build` delegation, with only evidence-completion marking added after it returns. Tree construction occurs strictly after the fallback branch.
4. Each receiver retains its original `guard()` and point sums. After the original row scratch reset, the tree gathers/sorts candidates. Only `for (let j=0;j<n;j++)` becomes `for (const j of candidates)`; the original order/uniqueness check, self skip, component screen, center norm/guards, rotor classifier, and immediate positive consumption remain unchanged.
5. A requested `completedReceivers` increment follows the original receiver's dependency checks.
6. Assembly metadata labels the always-selected ordinary assembly as `lean`; H/H0 cannot enter the retained typed branches. Requested coverage is marked complete immediately before the original build return.
7. Exported `build` accepts only H/H0 and forwards options. The unrelated kernel convenience `query` function is removed; native-load retains the complete authoritative path. Schedule, fullGraph, solve, residual, cached and checksum are still direct unchanged anchor exports.

There are no changes inside preparation, `screenPredicate`, `finishScreen`, `typedChunks`, the positive classifier, positive-term cap throw, scaled-cap expression, graph/admission arithmetic, `a` construction, ordinary row sums, or numerical solver dependencies. Removing pair visits is permitted only when a node comparison certifies the original component screen; all other sources reach the original body in canonical order.

## New tree module

`source/tree.cjs` is new. It exports coverage creation, tree construction, gathering, and leaf capacity 8. Its only floating operations are min/max bounds, rounded axis spans used to choose a split, and rounded endpoint subtraction for the ±4 predicate. It contains no rotor preparation, coefficient/root/load arithmetic, imports, guard calls, source aggregation, positive approximation, or timing code. Canonical index ties are stable-ID ties because native capture has already sorted IDs. Source geometry is read, never written.

## Retained immutable dependency pins

All paths below are relative to `../m31-native-fresh-transfer-2026-10-17/source/`. They were read and hashed, not edited.

| File | SHA-256 |
| --- | --- |
| `native-load.cjs` | `b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1` |
| `vendor/kernel.cjs` | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| `vendor/anchor-kernel.cjs` | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `vendor/lean-anchor.cjs` | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| `vendor/reference-excerpt.cjs` | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |

The numerical-equivalence claim is pending. Parent review should check this complete diff, the checker comparison allowlist, exact tree reconstruction and corrupted-evidence controls, the exposed status of the saved64 input, the disabled execution configuration, and the independent outer resource supervisor before authorizing any run. No 5000 benchmark or 5000-ready containment is implied by this source receipt.
