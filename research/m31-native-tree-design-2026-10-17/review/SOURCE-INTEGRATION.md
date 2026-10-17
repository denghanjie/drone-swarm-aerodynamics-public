# Source integration review before qualification

Reviewer role: `/root/m31_protocol_challenge`, author of the candidate native wrapper, kernel fork, and tree. I am not an independent reviewer of my own implementation. The Python checker and fixed control plan were authored separately; the harness and supervisor were authored by a third contributor. Shared task context and retained numerical dependencies further limit independence. This review checks source integration, not numerical truth or an independent physical reference.

The bounded read-only review began at 2026-10-17 03:30:44 UTC. The checker author confirmed its checker/cases/control-protocol files closed at 03:31:05 UTC before this review file was written. I read the complete checker, harness and supervisor sources, configuration, cases, relevant protocols, and candidate interfaces, and recorded byte hashes. I made no edits to those files. No candidate import, syntax/test execution, science, browser, network, Git operation, or benchmark was performed. This separate review file is the sole review artifact I wrote.

## Conclusion at source review

I found no functional integration blocker in the reviewed source identities. The producer/checker interfaces, exact case allocation, certificate reconstruction, narrow semantic allowlist, refusal handling, mutation-control rejection paths and supervisor completion fields agree. This is a source assessment only. It neither authorizes execution nor supplies passing qualification evidence. The configuration reviewed here is disabled; a later enabled configuration and publication/runtime bindings require the parent's distinct freeze review.

One documentation clarification was sent to and resolved by the parent before freeze. The earlier `PROTOCOL.md` phrase “guard checks” now says “geometry/admission checks”; `SOURCE-REVIEW.md` now says “geometry/admission/refusal diagnostics” and explicitly lists cooperative-guard failure injection among untested paths. I read those corrected lines and recorded their updated hashes below. `CONTROL-PROTOCOL.md` already explicitly excluded injected cooperative-guard failures. No executable control allocation changed. No actionable source issue remains from this integration review.

## Interfaces and native semantics traced

The harness invokes the retained original `native-load.query(input,'F',guard)` and candidate `query(input,'H0'|'H',guard,{treeEvidence:true})`, in exactly F, H0, H order for each case. Each arm receives a freshly decoded ordinary input from the same saved word recipe. `Object.is` input-preservation comparison handles the deliberate NaN control without JSON-number conversion. The CommonJS cache allowlist includes both native wrappers, both kernels, the new tree, the shared anchor/lean/reference closure, and the harness itself. Original F resolves only its original modules.

The checker expects the actual `encodeEvidence` schema. Pre-build input failures retain null raw/IDs/prepared/tree because `captureInput` assigns its completed canonical array only after it returns. Domain and graph refusals retain completed build coefficients/prepared geometry and complete tree coverage because native preparation precedes `validateBuild`. On ineligible scenes H/H0 use the original lean fallback, retain empty node/receiver evidence and zero tree counters, and report all-pair geometry visits with zero component-screen tests. These distinctions match `raw_binding`, `certificate`, and `verify_case`.

The copied candidate body retains the original preparation, component screen, immediate rotor consumption, positive append and 2,000,000-term throw order, scaled-cap calculation, graph/admission, coefficient scaling, solve/residual, loads and FNV consumption. H/H0 source arrays are sorted canonically before this body. No source check in this review supplies dynamic evidence for the unexercised positive-term resource limit or memory/deadline failures.

## Independent tree reconstruction and equality boundary

The checker reconstructs raw centers from canonical state words. Its rational binary64 decoder, RN-even conversion and signed-zero subtraction implementation are separate from the JavaScript producer. The reconstruction agrees with candidate node extrema, rounded widest-axis selection, lowest-axis ties, canonical-index/ID ties, floor-median splitting, preorder IDs and leaf capacity 8. Leaf member order is the order inherited from the same recursive split, followed by sorted gathering for actual classification.

Both implementations evaluate axes 0 through 2, minimum-positive before maximum-negative, stopping at the first satisfied predicate. H0 still pays those predicate comparisons but ignores any omission decision. The checker independently reconstructs every visited leaf and actual H cull, tests every omitted member against the original component screen at this bounded size, requires complete disjoint membership coverage, and compares the actual sorted gathered list including self. It recomputes all twelve tree counters, including `completedReceivers`; a partial record cannot satisfy its completed-case acceptance rule.

The exact semantic allowlist in `semantic_payload` removes only:

- `method`, `tree`, `timing`;
- `diagnostics.buildPhasesMs`;
- `diagnostics.geometryWork.gatheredNonselfCandidates`;
- `diagnostics.screen.orderedPairVisits` and `diagnostics.screen.componentTests`.

The three enumeration counters are separately reconstructed. Logical directed-pair and skipped-center-norm accounting remains in equality. Unknown fields remain compared by default. All existing encoded raw/prepared/CSR/solution/load words, source order, status/reason/stage, constants, admission/graph/residual diagnostics and consumption remain in the comparison. The existing native diagnostic fields retain their original JSON serialization convention; this review does not turn those into a newly word-encoded format. New endpoint and cull-difference fields are explicit binary64 words.

The checker independently validates raw/prepared bindings, CSR positive domains and ascending nonself source order, load/solution ID association, and FNV consumption. It does not independently recompute positive aerodynamic coefficients or roots; equality to unchanged F is the relevant finite implementation claim.

## Fixed expected behavior and mutation controls

The reviewed case source has 42 cases, yielding 126 queries with 34 expected successes and eight expected refusals per arm. The 18 component faces and nine strict-radius controls agree with the hardcoded checker placements. The four-drone positive fixture has two vertically separated upstream sources for the lowest receiver; the permuted fixture uses the same stable IDs and state words. Thus the planned source-order corruption targets a row with at least two positive sources instead of relying on a single-entry row.

The expected refusal precedence is consistent with source inspection: missing/duplicate ID, raw nonfinite and nonpositive force fail during input capture; near field and large finite source scaling fail native admission; the sideways-axis source below its receiver passes geometry/admission but fails graph ordering. The finite 513-separation malformed-quaternion case takes ineligible lean fallback, retains geometry refusal and eight invalid rotor classifications before the outside-neighbor screen. These expectations remain hypotheses for the eventual fixed run, not observed outputs.

All 15 saved-record mutations target fields that the checker reads before or during full equality. Missing/duplicate/self candidates and added false culls fail receiver-certificate equality; node bounds/membership fail reconstruction; raw/prepared changes fail binding; reversed positive sources fail CSR order; a still-positive coefficient or alternative positive root fails native semantic equality; changed load/consumption fails independently reconstructed FNV; admission and refusal-status changes fail their explicit expected checks. The mutation routines operate on deep copies of already saved primary rows and add no producer queries. A mutation must fail at its specifically declared reason; an unrelated exception cannot count as successful detection.

The corrected span fixture subtracts `3d20000000000000` (2^-45) from the successor of 256. This is half the spacing above 256 and ties to even 256. The former quarter-ULP operand is not in the reviewed fixture. The 16 subtraction fixtures and six threshold checks are checker sanity controls, not independent JavaScript conformance tests.

## Harness, artifact and resource bindings

The disabled configuration, harness and checker agree on stage order, 120-second work allocation, 45-second check allocation and 180-second total reservation. The work completion fields required by the supervisor are populated only after all fixed cases, input checks and source-preservation checks. Checker acceptance supplies `complete:true` and `passed:true`; failed checker exit remains terminal before supervisor success. The checker also requires completed work status and reason, runtime/preservation flags, exact case/method sets and exact journal order.

Every sidecar has a fixed case-index/method path, byte/hash descriptor and full-body equality to its work row. The full journal is bound both to its descriptor and to `work.json`; source/publication/runtime pins and earlier output identities are rechecked. The work attempt file remains unchanged while Node owns the stage; the supervisor updates it only around stage boundaries. The checker imports no producer or scientific helper.

The source keeps the documented constraints: no retries, replacements or result overwrites; at most 64 drones; no new exact-reference run; no browser or integration; no 5000 benchmark; no speed/physical/novelty claim. There are no inner tree guard polls. The optional gathered lists can grow quadratically. Outer userspace polling plus direct-child wall/CPU/file limits does not establish an OS memory limit or equal failure behavior. The parent must still observe final supervisor exit and maintain the registered cutoff after final report writes.

## Reviewed byte identities

These pins identify the source text reviewed, not a self-contained execution manifest. Paths are relative to this package.

| File | SHA-256 |
| --- | --- |
| `source/check.py` | `1f40c7b3dc3f962eb623e5d7d2f848d03fc2decb0425e72733ba02722a76782b` |
| `source/cases.json` | `9cf2a3e99bd645abeb83e92eeb6efcdff81cf2ad71a1e31db8ce8ff9667ba0e1` |
| `source/harness.cjs` | `3fc8171bf88319abef03f92c586fae21c18dcd2c6425d2d04a5bce8207569b62` |
| `source/run.py` | `7bcb0f9c351fdfb4753cbe7fc6649e23b25c88e2d91bf73fcf2df4f7d6902fb8` |
| `source/native-load.cjs` | `05d9fcb5aa9fc8d3f4812a14e469096f5c3d6110b18f7b164496df7e21dd530b` |
| `source/kernel.cjs` | `42cb6deeb32e9b5bd633679d3ea58489940009a9f77f690a0368b6f22de2a971` |
| `source/tree.cjs` | `23e7b4393321d4a6cc83906a2d02319dd7a37b2a2f63ae165fe4558eca73f422` |
| `config.json` — disabled | `267fec6ebcbdd014fcdcd3e1bfe62c740eae8dfdbb0daf2f20c88c9935b3b7c3` |
| `CONTROL-PROTOCOL.md` | `b66c7dc495b860cd3abd8b729e2b7aa97e7822be5b91be547da19b83d69daec2` |
| `PROTOCOL.md` — clarified wording | `766255962e1b76c996abb9989ce231be017011ff3665d0e52ddc1893c2a2e1fc` |
| `SOURCE-REVIEW.md` — clarified wording | `e21570fb09148819e88507a9ff880265834670207c794e6f0d310f757019f75c` |

Any further source changes or configuration enablement after these identities must be separately represented in the final source freeze. No review statement above reports a passing scientific result.
