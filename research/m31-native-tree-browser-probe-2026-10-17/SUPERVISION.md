# Browser tree probe: transport and supervision contract

This package is source-only and unexecuted at author handoff. `config.reviewed-disabled.json` has `executionAllowed:false`, null authorization and null cutoff. The parent owns the effective `config.json`, source/runtime manifests, source packaging, publication receipt and any future launch. No source-preparation instruction authorizes scientific imports, a fresh seed, a browser or a retry. Earlier completed packages remain immutable.

The scientific allocation is the four fixed t=0 cases and one real projected RK step described in `PROTOCOL.md` and `source/science-config.json`: 16 actual stages and 48 primary queries, with the registered F/H0/H permutations. The unchanged native positive-term cap is 2,000,000. The exact-reference drone cap remains 180; only the four fresh64 stage inputs receive exact-reference work. No warmup campaign, repeated benchmark, seed replacement, cap relaxation or longer trajectory is implemented here.

## Sole entry and ownership

The sole future entry is the pinned Python executable with `-I -B source/run.py MANIFEST_SHA SOURCE_COMMIT`. It reads the parent's effective `config.json`, checks explicit authorization and the fixed cutoff **2026-10-17 05:06:20 UTC**, and requires the full **960 seconds** before creating an exclusive attempt marker or spawning a child. Consequently the latest possible launch is **04:50:20 UTC**, subject to the actual entry checks. The monotonic total starts at supervisor entry and includes imports, source/runtime hashing, preflight, serialization, persistence, handoff and closure. No script extends the cutoff.

The supervisor requires a new, absent `results/` directory. All scientific results, shards, descriptors and journals are exclusive writes. Only the supervisor's own `run-attempt.json` is replaced, with an exclusive temporary file, file fsync, atomic replacement and directory fsync. A failed attempt is retained and cannot be resumed or retried in place. Parent authorization identifies the reviewed disabled manifest with `reviewedSourceManifestSha256`; the enabled configuration itself belongs to the actual execution manifest.

`source-publication.json` must bind the exact commit, manifest path/byte count/SHA-256, verified file-pin count, `remoteBytesEqualLocal:true`, `committedBytesEqualLocal:true`, and a verification time preceding the attempt. Publication is a separate gate, not a claim inferred from a local hash or commit string. Every immutable source/input pin, publication receipt and previous-stage result is checked before and after stage transitions. Previous bytes are checked **before** a replacement snapshot is accepted.

Private paths arrive only through environment variables: `RESEARCH_NODE`, `RESEARCH_NODE_MODULES`, `RESEARCH_CHROME_CONTENTS`, `RESEARCH_PRIVATE_LOG_DIR`, and `RESEARCH_BROWSER_PROFILE`. The profile must be fresh and inside the new private directory outside the repository. `RESEARCH_EXECUTION_CONTEXT=tool-require-escalated` is required; `NODE_OPTIONS` and `NODE_PATH` must be empty. Public evidence records private-path hashes, scoped runtime identities and private-log byte/hash metadata, never private path strings or browser command lines. The command line and PID record remain in the private directory.

The attempt schema is `m31-native-tree-browser-probe-attempt-v1`. Public scientific stage order is `browser`, `reference`, `check`. A separately labeled `saved-validation` preflight is present in `attempt.stages` but charged to the shared overhead allocation, not added to primary queries or fresh stages. Live children bind the source manifest/commit and a random supervisor token, whose hash alone is public.

## Fixed time ledger and cleanup

| Allocation | Seconds | Included work |
| --- | ---: | --- |
| Browser | 120 | Runtime/browser launch, fresh initialization, controls, all native arms, RK/common work, compact capture, encode/transfer/write, browser closure |
| Exact reference | 600 | Four fresh64 exact stage evaluations and their complete records |
| Saved checker | 180 | Complete source/input/result/coverage/RK/reference and engineering-gate validation |
| Shared overhead/closure | 60 | All supervisor work and preflight; **saved validation has a fixed maximum of 15 seconds inside these 60** |
| **Total** | **960** | Entire attempt, with no retry |

The controller uses its own Node `performance.now()` deadline at 110 seconds, leaving ten seconds within the 120-second browser allocation for closure/handoff. Browser JavaScript receives a duration and uses its own local clock. Python's monotonic epoch is never compared to Node or browser performance epochs. Python independently polls at 0.1 seconds and enforces child and total deadlines, including when the page is unresponsive. Existing scientific guard call sites remain unchanged.

The retained guardian pattern owns a process group for both saved validation and browser work. The guardian remains unreaped while its parent may need to signal that group. On success it records its direct child's return code, waits for the parent's release byte, then exits; the parent observes the guardian exit. On failure the parent kills and reaps its retained owned group. Saved validation's Python process owns/reaps its narrow Node codec child. The Chrome controller allows exactly one spawn of the byte-pinned launcher, fixes its profile, overrides Playwright's detached request to false, and captures that exact root's `exit` and `close` events before returning from spawn. Success requires both root events with code zero/no signal, successful context closure, and guardian release.

This is not an all-helper cleanup guarantee, an OS memory ceiling, or equal out-of-memory/deadline behavior for F/H/H0. Tree sorts and traversal retain long intervals without new cooperative polls. CPU/file limits and externally owned handles provide bounded supervision; they do not create a browser memory sandbox. Node peak RSS is process-lifetime `maxRSS` converted from KiB; Python macOS `ru_maxrss` is already bytes. Neither measures an isolated stage or aggregate Chrome tree.

Saved stage/attempt durations are diagnostic. Final fsync and interpreter exit occur after pre-final-report timestamps. A post-write deadline check and the caller's observed supervisor exit are required; the ledger explicitly does not certify its own process exit. Failed child elapsed time stays associated with that child. Saved-validation elapsed time remains overhead, including its failed path.

## Fixed disk and logical decoding ledger

The **256 MiB combined** ceiling counts all new result files, private logs, Chrome profile, guardian records and scratch. The existing **32 MiB per-file** ceiling applies throughout. The internal reservations below are frozen before exposure:

| Partition | Ceiling | Contents |
| --- | ---: | --- |
| Unique evidence | 160 MiB | `results/shards/`, `results/records/`, `results/saved-records/`, including saved validation and browser evidence |
| Private browser/log/scratch | 64 MiB | Entire private tree, including profile, logs and guardian state |
| Other public outputs | 30 MiB | Reference/check records, transport/index/journal files and related public outputs, excluding the attempt ledger |
| Final ledger allowance | 2 MiB | Attempt report and its temporary replacement, included inside 256 MiB |

The host checks available bytes before each shard/descriptor/journal write, and the supervisor independently monitors aggregate and partition totals. Private symlinks such as Chrome singleton links contribute their own `lstat` size and are not followed. Research-result symlinks are rejected. There is no compression assumption or filesystem-sparse-file discount. The per-file resource limit is not described as an OS aggregate-disk quota.

Transport limits are **1 MiB per binary shard**, **2 MiB per record descriptor and complete journal**, at most **4096 journal rows**, and, for each logical record, **96 MiB binary value bytes**, **256 MiB declared logical JSON bytes**, **16,000,000 encoded elements**, and recursive depth **64**. Objects count one container plus their string keys and values; optimized arrays count one container plus every element. The top-level record, represented in its descriptor, contributes one object and one key element per field. Descriptor fields are unique and bounded to 128. These are hard decoder/encoder resource limits, not assumptions that hostile or maximally large admitted evidence will fit.

The 256 MiB `jsonBytes` declaration is the producer's incrementally counted UTF-8 `JSON.stringify` size, without allocating the complete JSON string. The independent Python decoder treats this as a bounded declared diagnostic because JavaScript number-to-text formatting differs; it independently enforces binary lengths, element counts, depth, exact schema and native scientific shapes. There is no compressed-to-expanded ratio to trust. A large decoded Python/JS heap may exceed these byte counts because language objects have overhead; no heap/RSS cap follows from them.

For scale, at 2,000,000 positive terms, the two word arrays K/a require 32,000,000 binary bytes and source indices require 8,000,000. At N5000, CSR offsets add 80,004 bytes, before tags/other fields. Eight large-case stages at that maximum would exceed 160 MiB even if each actual F/H0/H CSR encoded identically and shared perfectly. Compact trace worst cases can also exceed logical element limits. The cap therefore cannot guarantee all admitted native inputs. A cap failure is a terminal observed operational limitation with preserved partial artifacts, not permission to omit evidence, reduce the native term limit, resample or raise a quota. No new state was generated to decide the limits.

## Lossless transport v1

`source/transport.cjs` is an evidence codec with no scientific dependency, filesystem operation or compression. The complete ordinary logical native payload is retained. Each top-level field is encoded independently in property order, allowing matching raw/prepared/CSR/solution/load streams to share storage across arms only after actual returned values have been encoded. The binary stream uses these tags; all lengths and fixed integers are big-endian:

| Tag | Exact representation |
| ---: | --- |
| 0 / 1 / 2 | null / false / true |
| 3 | finite IEEE binary64 number, eight bytes; signed zero preserved |
| 4 | UTF-8 string: u32 byte length then bytes; non-roundtrippable surrogate text rejected |
| 5 | ordinary array: u32 element count, recursively encoded values; empty arrays use this tag |
| 6 | object: u32 property count, recursively encoded string key and value for each property |
| 7 | lowercase 16-hex-digit word string as eight raw bytes; reconstructed as the same string |
| 8 | nonempty homogeneous word-string array: u32 count, eight bytes per word |
| 9 | nonempty nonnegative uint32 array: u32 count, four bytes per number; negative zero excluded |
| 10 | nonempty finite binary64 numeric array: u32 count, eight bytes per number |

Each stream is cut at canonical **1 MiB boundaries**, including through a scalar's bytes. Every nonfinal shard is exactly 1 MiB; the last is nonempty and at most 1 MiB. No unknown tag, truncation, trailing element/byte, duplicate key, missing/reordered shard, unbounded count, unknown descriptor field or inconsistent declared total can be accepted. Binary64 word strings retain NaN payload words as strings; the deliberate old input refusal remains representable without numeric JSON conversion.

A record descriptor is exactly `{schema:"m31-lossless-record-v1", fields:[{key,stream}], binaryBytes,jsonBytes,elements}`. Each stream is exactly `{schema:"m31-value-stream-v1",binaryBytes,jsonBytes,elements,chunks:[{path,bytes,sha256}]}`. Shard paths are `research/m31-native-tree-browser-probe-2026-10-17/results/shards/SHA256.bin`. All descriptor fields, counts, canonical path/hash syntax and lengths are validated before decoding or reuse. The independent decoder validates bytes/hashes even on cached-value paths.

`source/transport-store.cjs` hashes every newly encoded shard. If a same-hash file already exists, it reads and compares **all bytes** with `Buffer.equals`; hash equality alone cannot authorize a shared reference. Otherwise it performs an exclusive fsynced write and directory fsync. A descriptor is written only after its referenced bytes exist. A mismatch preserves divergent chunks already stored and fails; a resource limit can leave an explicitly incomplete prefix. No descriptor points to a presumed F result based on a boolean equality claim.

Browser records are `results/records/NNNN-kind.json`; saved regression descriptors are in `results/saved-records/`. `results/browser-journal.jsonl` has one durable lightweight row per record: `{sequence,kind,recordPin,serializationMilliseconds,transferMilliseconds,persistMilliseconds}`. It contains no copied native body. `browser.json` binds the journal path/byte count/hash/record count, runtime/source/bundle pins, saved-validation output, driver summary and Chrome-root completion fields. Complete data is reconstructed from each referenced descriptor/shard, not from a checksum or producer equality flag.

Native records are flat: metadata, every actual `encodeEvidence` field and audit timings. They are emitted separately for each arm, before later stage work. Stage/step records carry full state/derivative/RK data and native record references. Driver/query timing scopes belong to `IMPLEMENTATION.md`; no transport timer is silently included in, or subtracted from, a native query result.

The append acknowledgement reports complete append transfer waits and host shard/descriptor/journal persistence; persistence overlaps transfer and must not be added twice. Transport serialization covers packing, hashing and base64 CPU outside the binding waits. A journal row's timing fields are the prefix available before its own final descriptor acknowledgement; the driver's stored acknowledgement/append timings are the complete per-append diagnostics. The driver's summary excludes its own append to avoid a self-reference. Overall controller/browser time remains separately reported. Neither all-arm diagnostic wall time nor subtraction of intertwined F/H0 work constitutes standalone production frame time.

## Saved-only gate and bundle boundary

Before any browser spawn, `validate-saved.py` invokes the pinned Node `qualify-transport.cjs` and observes its exit. This gated child imports only the new transport/store/compact-codec helpers. It reads exactly the 126 byte-pinned prior native sidecars, in fixed case-index and F/H0/H order, replaces legacy tree representation using `compactLegacyTree`, encodes/shards the complete payload, and checks its lossless logical roundtrip. Its `saved-transport.json` binds every old source pin to the new descriptor. Six fixed codec sanity controls include a word array crossing the 1 MiB boundary. They are transport controls, not primary native queries.

The separately authored validator then applies its strict independent decoder and optimized coverage validation to these saved records and compares with the exhaustive old certificates, including the registered mutation laws and focused format corruptions. It may load the byte-pinned old saved-evidence checker as a standard-library helper without running its `__main__` or any producer/oracle. This reuse and shared dependencies limit independence. A successful gate requires `results/saved-validation.json` with matching source bindings and `complete:true, passed:true`. Both the supervisor and controller enforce this before fresh browser work. The full gate must fit its 15 seconds inside shared overhead; timeout is terminal.

`build-bundle.py` only packages exact source bytes into factories; it never imports/evaluates them. The parent runs this packaging step before freezing, and pins both `browser-bundle.js` and its byte-offset source ledger. Module IDs are full `./research/...` repository-relative identities. The module list includes the unchanged original F/vendor and wide factory/controller/physics closure plus new transport, compact-codec, tree, native-tree, browser-adapter and browser-driver. The loader checks bundle size/hash and each exact source slice before executing factories. It runs the inherited 56 Buffer adapter assertions, injects the wide-factory process shim only into the declared original factory module, and leaves global Buffer/process unchanged.

The browser controller serves only byte-pinned local HTML, bootstrap and bundle responses through its intercepted origin. One pinned Chrome root and one page are allowed. The standalone transport factory may initialize before the source record is persisted; scientific factories load only after bundle verification and Buffer controls. All initial states are subsequently produced inside the authorized browser allocation, never during source packaging.

## Handoff status

The author has performed source reads/writes and metadata inspection only. No new source module, codec test, saved validator, scientific query, browser, reference, checker or bundler was executed during drafting; no network or Git action was performed. Syntax checks, source integration review, frozen manifests, runtime metadata, publication verification and any eventual single attempt remain parent-controlled. Any fix after freeze must be represented by new reviewed/published source bytes before launch.
