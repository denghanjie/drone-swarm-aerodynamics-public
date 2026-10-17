# Independent native-load checker source handoff

2026-10-17. This directory contains source only. The checker, its arithmetic fixtures, its corruption checks, native kernels and browser have **not been executed**. Only source reads, metadata/file hashes, JSON structure reads and an AST syntax parse were used while drafting. No new seed, state, trajectory, coefficient computation or reference solve was performed.

Install `source/check.py` and `source/checker-contract.json` under the fixed package `research/m31-native-load-baseline-2026-10-17` in the repository. After all source is reviewed, the parent supplies a source manifest and named runtime pins. The later checker command is:

    python -I -B source/check.py ROOT MANIFEST_SHA SOURCE_COMMIT

`ROOT` is the repository root, not the package directory. The checker verifies the source-manifest digest, every source file pin, its own installed location and the current Python executable pin before target output inspection. It writes `results/check.json` exclusively, with a 32 MiB report cap. Valid complete records exit 0 even if the scientific decision is `unqualified`; `passed` means integrity and checker-fixture acceptance, while `decision` records native-load qualification. Invalid/incomplete/malformed evidence exits 1 and cannot overwrite an existing report. Scientific refusal in a complete 12-call record remains a counted, unqualified outcome.

## Exact audit and frozen scope

The scope is six retained 64-drone states, one F and one L call per state, in the alternating case-major order frozen in the contract. The checker does not import the producer, scientific modules or a historical checker. It reuses the pinned saved normalizer reference loads, prepared-word geometry and complete positive-pair evidence. It verifies saved reference source/schema identity and exact reference pair coverage, admission and ID association. Existing exact reference computations are not repeated.

Two digests have distinct roles. `inputFileSha256` hashes the saved raw file bytes. `semanticInputSha256` hashes canonical compact sorted-key printable-ASCII JSON for `{domain:"m31-moving-admission/input/v1",id:caseId,input:raw}`; it must match the saved reference's `inputSha256`. Both the browser call and its native wire evidence carry these explicit fields. The raw file is the only scientific input supplied to the browser.

The authoritative accuracy operands are the delivered rotor, collective, world-force and world-moment binary64 words. Each is decoded by integer bit decomposition into an exact Fraction. The checker compares them to the saved rational load boxes and computes exact squared normalized error bounds. The four independent primary thresholds are each `<= 1e-8`, with reference uncertainty included. A squared upper bound at or below `1e-16` passes; a squared lower bound above it fails; overlap is unresolved. Euclidean vector errors sum all three squared component distances. The reported square-root intervals use exact integer square roots at 192 fractional bits, while verdicts use the exact squared bounds directly.

An independent exact round-to-nearest-even routine checks that the delivered native loads follow the declared linear `f*x`, collective left fold, actual-axis force and signed lever-cross-axis moment arithmetic. This consistency check does not replace the independent reference-load comparison. Source y/root ranges, positive finite coefficient arrays, rounded native scaled caps, declared admission/order/input diagnostics, and the new native residual engineering guards (`1e-9` and `2e-9`) are also checked. These residual thresholds are not primary accuracy certificates. The native positive CSR support is compared with every saved exact positive pair; coefficient error bounds are diagnostic only. There is no online certification or uniform native/exact bridge claim.

The status/ID/load consumer checksum is independently reconstructed from all status characters, safe-ID binary64 words and all 11 delivered load words per drone. F/L native output parity is reported. A valid record with an identity, support, load-formula, checksum or primary load-error failure is unqualified. Missing or malformed required successful evidence is invalid.

## Browser and ownership evidence

The checker cross-binds the named Chrome version, platform, Node/Playwright metadata and verified component counts to the frozen runtime file. It compares the browser source receipt to the pinned bundle index, verifies all seven bundle slices against their standalone source bytes and checks the executed factory allowlist. This is provenance for the verified runner, not full transitive runtime attestation.

It requires the nine/56 adapter assertions, every inherited control record's checks and saved F/L parity, all 24 wrapper status/assertion/immutability checks, the six individually journaled ownership builds and their retained storage equality. Wrapper controls and the 12 target calls must additionally retain the predecessor chain of the last successful result and assert disjoint current input/output storage, unchanged prior results and disjoint prior storage. Native-control correctness beyond these saved assertions belongs to their reviewed source; independent exact target accuracy is evaluated separately.

## Prospective fixtures and corruptions

Fourteen fixed arithmetic assertions are defined in `arithmetic_fixtures()`: exact binary64 decoding, signed zero/subnormal values, normal/subnormal ties-to-even, negative rounding, inside-box distance, a Euclidean 3-4-5 case, threshold equality/failure/overlap, square-root enclosure and signed cancellation. A future checker invocation runs these after source/runtime identity gates and **before reading target result outputs**. None was run during drafting.

Exactly four corruption checks are defined, with no target search, replacement or extra native query:

1. `run-a-t0/F`: zero the delivered first rotor-load word.
2. `run-a-t0/F`: apply the squared-force law to **all 64 rows**, updating solution T and native load assembly consistently. Check for a nontrivial ratio and at least one changed delivered word, then require a detected rotor formula error.
3. `run-a-t5/F`: replace world force by the body-frame vector `[0,0,collective]` for **all 64 rows**. Check for tilt and at least one changed word, then require a detected world-force formula error.
4. `run-a-t0/F`: duplicate the second drone's load ID onto the first row, requiring the specific load/solution ID-association rejection.

The two all-row transformations are fixed prospectively to avoid selecting a favorable witness. They inspect total category failure counts, not a truncated witness list. An unavailable clean witness closes qualification and is recorded; it does not authorize another case. Detection must use the intended arithmetic/ID gate, so a stale checksum alone cannot make a corruption test pass. These tests run only in the future authorized checker invocation.

## Handoff status

The contract has complete input/reference/index pins and fixed control expectations. Parent source/runtime manifest construction remains separate. `requiredBrowserEquals` contains concrete completion/identity flags; runtime and source-receipt binding is implemented independently in code. No placeholder, fresh input generation, performance repetition or execution allocation is included. Parent and the evidence reviewer have read the core arithmetic/control implementation; source parsing alone is the only validation performed so far.
