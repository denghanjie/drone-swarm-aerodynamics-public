# AUDIT-C1 implementation, static stage

No numerical execution is authorized by this directory. Candidate, adapter, exact corpus/fixture harness and benchmark child have only been syntax-checked. There is no claimed equality or speedup result.

## Entry and ownership

- Candidate: `src/branch-audit-c1.cjs`; narrow diff in `SOURCE-DIFF.patch`.
- Frozen oracle: `../../research-next/implementation/src/branch-audit.cjs`. Its exact aerodynamic module and snapshot dependencies are loaded read-only. `UNCHANGED-SOURCE-CHECK.json` verifies all 71 original source identities.
- Adapter: `src/load-audit.cjs` compiles the original CommonJS text. Only its `./io.cjs` and, in labeled synthetic tests only, `prepare` are injected. Original I/O code receives a different physical root and conservative new-study resource checks; raw, JSON, append, fsync, temporary-file and rename behavior remains original. Logical IDs and relative paths remain unchanged. Output roots must be strictly below this study's `implementation/results/`.
- `src/exact.cjs` compares Object.is values, key insertion order, descriptors, arrays/buffers and alias relations. The canonical output consumer uses a single reusable 64 KiB byte buffer, little-endian binary64 values, ordered own keys/descriptors and deterministic graph-reference indices. V8 serialization is used only to retain a failure reproducer; it is not a correctness digest.
- `src/context.cjs` handles paired observations, matching errors/class state, nonmutation and actual counters. Dedicated lifetime fixtures preserve real input references, frozen descriptors, reversed variant order, earlier outputs, and successful reuse after a guard failure.
- `src/corpus.cjs` streams all 35,597 endpoint rows, 220 original bracket sides/110 pairs, 23 JSON initial/final/exact-stop cases. All 35,840 available endpoint occurrences retain their original saved-signature anchor, including duplicate labels. Both complete historical preflights reproduce all three artifact types byte-for-byte; sparse retained paths have new replay aggregates, never claimed original full-stage replay.
- `config/synthetic-cases.json`: 73 deterministic cases, with independent-reviewable exact counters. Direct constructed pair packets and controlled `prepare` outputs are explicitly synthetic. Real `prepare` validation also runs. No retained real RK stages exist.
- `src/workloads.cjs`: four exact workload contracts precede 64 serial benchmark children. Full returned public samples and finish graphs are retained for each pass and canonically consumed outside its timing interval. Fresh audit construction, finish, normal audit work, current-observation capture and cooperative resource-check overhead are inside timing. The variant module is loaded once per child so the warmup exercises the same functions used for both timed passes. One warmup plus two timed passes, no calibration, extra pass, GC forcing or source tuning.
- `src/child.cjs`: refuses entry without a full coordinator release, frozen runtime/source/jobs and supervisor environment. Performance additionally requires the independent complete correctness gate and exact workload digest. No subprocesses or worker threads.
- Independent supervisor and cost validator: `../robustness-review/`. Independent semantic gate: `../semantic-review/`. These are reviewed by other workers, not implemented here.

## Static operation accounting

For one N16 observation, ordered center-distance calls fall from 960 to 240, while 960 rotor-relative radial hypot calls, all 960 public pair objects and 7,680 pair margins remain. This removes 720 redundant center-distance calls (75% of that specific operation), not 75% of total audit work. The old per-margin identity temporary is removed; margin/extremum records are allocated only when a comparison wins. Actual retained winner counts, allocations, GC behavior and wall/CPU savings are unmeasured.

## Future execution contract, not a release

From the study root, the supervisor uses:

`node implementation/src/child.cjs --job <frozen-job-id> --release <coordinator-release.json>`

Direct invocation without supervisor deadlines is rejected. No command in this README grants permission to execute the numerical modules. The parent must freeze all implementation/review/config/input files, verify runtime and storage, and explicitly release once independent reviews pass. `config/jobs.json` declares 18 correctness jobs and 64 performance children; correctness must complete before any benchmark.

Successful receipts are under `results/receipts/`; larger workload component/alias digest maps are equality evidence under `results/equality/`. Persisted paired audit outputs are under separate physical variant roots in `results/outputs/`. A first failure captures the current raw input/selector, first compared component or mismatching value, both available values/errors, and a separate last-durable checkpoint. A benchmark child cannot retrieve a prior baseline's entire output graph: it retains the prior exact component digest plus the current complete offending sample/component and reproducible source selector. Hard-kill evidence explicitly says when exact current data was unavailable.

The candidate cannot preserve accessor/proxy read counts after distance reuse, and does not claim universal JavaScript-object equivalence. The admitted corpus is finite plain data arrays. The old failed/partial campaign, scientific qualification, and remote-publication pause remain unchanged.
