# Timing runner and canonical encoding review

**No remaining source blocker was found after the four corrections below.** This disposition covers the fixed six-scene timing/storage protocol. It does not authorize execution or establish measured times, scientific outcomes, runtime feasibility or correctness of the entire checker.

Final source SHA-256:

- run.cjs: `74764d0e32e1d4e24ba8bea42ccef29fd6a1ce28e98233741a1bb04e907a4d3f`
- canonical.cjs: `7112bccefcf00d85451e0c08ef937f46823e012fc806628a588489d34608b7d5`
- result-contract.json snapshot: `58f2f238b588ae4ee3c3d28d8825c469f24d03b43919e5942cd4bf9124c76c16`

The protocol/checker author directly confirmed that the final source contract supersedes the retained draft for anomaly path, failure fields, sourceFiles and summary schema. The accepted anomaly path is results/anomalies/first-mismatch.json; medianPairedRatio is declared separately from ratioOfMedians.

The outer timer surrounds the synchronous method call from raw-word admission through complete record return. It checks the three ordered hooks and reconciles four nonnegative stages to the positive outer duration. Clock/callback overhead is included without subtraction. The separate digest interval begins before context/common projection, includes canonical serialization followed by SHA-256 and reconciles those portions. Literal conversion is separate. Initialization, cap validation, journal/file work, shard/index serialization and supervision are outside the named intervals, as disclosed.

The runner executes warmup AB followed by measured AB, BA, BA, AB in spec scene order: 60 serial invocations. First measured complete/hierarchy calls are the sole full representatives. Every fresh return is digested before discard; the first warmup digest is the same-method repeatability anchor. Completed-call journal events precede qualification. A mismatch terminates without a replacement representative or retry. All four ratios, both method medians, median paired ratio and ratio of medians use reduced BigInt rationals.

Common entries now contain exactly {i,r,j,coefficient}, using input-index order followed by stable-ID conversion. This matches semantic-reference.py lines717-727 and the explicit final contract fields. The common envelope also includes prepared/result/solve/certificate; the whole-method envelope separately binds full status/branch/assembly/proof/work. Raw digest covers every input word and identity/order. Distinct versioned domains and manifest/spec hashes bind context; sourceFiles includes canonical.cjs.

The retained global arrays contain only small scene descriptors, trial metadata and summaries. Full scientific records are current-scene representatives plus the current return. Encoding transiently holds method/common strings; shard output creates another current-scene string. This is the declared lifetime policy, not a peak-heap or GC guarantee.

Within the declared JSON domain, recursively lexical ASCII key order, printable strings, safe integer/-0 checks, exact dense array order and quote/backslash escaping match Python's specified canonical encoding. Semantic digests omit a trailing newline; file pins include it. Explicit object encoding avoids JavaScript's JSON.stringify integer-key reordering.

Field/string caps, the shared 128 MiB shard/anomaly counter, 64 MiB per-shard cap and separate 8 MiB index/journal caps are enforced. Writes are exclusive, fsync the file and directory, and append/fsync journal pins before the next call. Supervisor remains responsible for aggregate/log/RSS/wall limits.

Resolved findings, with preserved snapshots and final deltas reviewed:

1. Failure events now include nullable anomalyRequiredBytes/anomalyAvailableBytes. They retain required/available bytes on mismatch while all offending file-pin fields stay null until durable full-file creation succeeds. Insufficient capacity produces explicit anomaly-retention-resource failure, no partial scientific record, success or retry.
2. Results directory fsync follows subdirectory/exclusive journal creation before run-start and any method call.
3. Exact enumerable array-index validation rejects sparse arrays whose missing key was previously hidden by an extra property.
4. The parent identified that the initial nested-result common entry differed from the inherited checker projection. The coefficient-only correction was checked against semantic-reference.py and the explicit contract; whole-method digests retain the omitted branch/status fields.

Both final JavaScript files passed node --check using the parent-specified pinned runtime. Initial PATH-based attempts returned command-not-found before parsing; these were administrative failures, not scientific allocations. No module was imported or evaluated and no model/generator/probe/old suite ran.
