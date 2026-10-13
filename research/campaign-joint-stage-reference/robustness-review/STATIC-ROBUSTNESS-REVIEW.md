# Independent robustness and retention review

Status: **STATIC REVIEW READY FOR COORDINATOR FREEZE. No numerical fixture, saved-path diagnostic, compatibility run or new trajectory was executed by this reviewer.**

Current adopted plan SHA256: `b68a2a93b29e85b3784d874010c767ee7ba3eacfdcc71d4bb6b91d31606d4bba`.

The original 150 MB proposal remains historical. The coordinator prospectively adopted 200,000,000 retained logical bytes, with the same 2,000,000-byte failure reserve inside that cap, before any numerical result. Wall/CPU/job limits, model, seeds, stopping gates and the original eight-step research framework are unchanged. The later retention clarification truthfully distinguishes an exact H/P integrator input from an unavailable private failing RK stage.

## Finding and disposition

Static inspection supports proceeding to a hash freeze and then one supervised numerical window. This is permission to test the implementation, not a numerical pass, reference claim or physical-validation conclusion. Every fixture and all scientific gates remain prerequisites. The independent physics review owns the equation and model-target assessment.

The implementation preserves full-swarm stage assembly, a nonmutating normalized geometry copy, raw derivative state, unchanged held-input integrator and genuine local three-dimensional Boids. The retained historical failures and skipped rows are not replaced by a new successful label.

## Resource accounting

- Entire numerical window: at most 300 wall seconds and 300 CPU seconds, including fixture subprocesses, preflight, compatibility, numerical rows, comparisons, hashing, serialization and final records. Each job has a 45-second wall ceiling, including its writes.
- `supervise.cjs` starts its monotonic clock before imports and charges the fresh supervisor's full own CPU plus reaped descendants and live descendants. `getconf CLK_TCK`, worker startup and fixture-child CPU are included. `/proc` exit races may be ignored only for vanished processes; other census failures stop work. A peak total is retained to avoid temporary undercount from reaping races.
- The external watchdog samples every 25 ms, kills the detached worker process group, and prospectively reserves 1.5 seconds for shutdown/final evidence. The worker uses earlier cooperative stopping. Final checks invalidate qualification if even cleanup exceeds the cap. A polling watchdog is not an OS scheduling-latency proof; an observed overrun must be reported, never accepted.
- Per-job worker timings include final run-record serialization. The runner's narrower numerical-loop timing is explicitly labeled and is not substituted for job/window totals. Parent and child timing scopes are distinct.
- No restart, replacement seed, new refinement level, omitted validation or renewed numerical budget is authorized. The supervisor refuses a second execution attempt after its durable attempt marker.
- Publication/transport is a separately identified activity. Any analysis, checksum or record extraction that interprets campaign arrays must remain charged to the adopted numerical/analysis window; upload duration must not be represented as simulation performance.

## Retention forecast

`STORAGE-FORECAST.json` gives the independent conservative allocation. Mandatory fixed/count-bounded binaries total **149,713,040 bytes**, including:

- Original uncompressed arrays 27,857,152 B and preserved gzip fragments 26,736,688 B
- Sixteen new raw outputs 76,630,016 B; compatibility allowance 872,576 B
- 278,819 branch signatures at 32 B: 8,922,208 B
- Controller binary 4,377,600 B; held-field hash streams 2,358,400 B
- Whole-swarm first/worst category-bracket payload maximum 1,958,400 B, including extra raw off-manifold J states

The full independent allocation is **191,713,040 bytes**, including 4 MB static source/input metadata, 1 MB additional selected-stage allowance, 20 MB result/display metadata, 14 MB maximal atomic-write/partial overlap, 1 MB fixture/log allowance and the 2 MB failure reserve. It leaves 8,286,960 B below the adopted cap. The four missing initial J signatures in the earlier arithmetic were corrected prospectively (+128 B).

The implementer's 166,724,482 B estimate uses 8 MB metadata plus 1.5 MB viewer output and 1 MB atomic overlap. The exact mandatory binary counts agree. The larger independent number is the freeze's conservative bound; the smaller number is not a guarantee that complete evidence fits. Metadata allowances are explicit prospective envelopes, not measured output sizes. Recheck actual static bytes at freeze and stop if actual or projected retention exceeds the adopted cap; never truncate evidence to meet an estimate.

Refresh-role reuse is acceptable: an H/P refresh uses exactly the accepted endpoint already audited, references that sample's index/signature and separately counts refresh-role coverage. It does not duplicate hashes or normalize/change state. J3 common output is a declared view of its dense retained array. All actual files under `research-next`, including source, reviewer files, coordination files, partial files and duplicate forms, count.

## Failure and integrity retention

Resolved first-cut issues include direct/truncating writes, raw metadata overriding calculated identity, missing shape/bounds validation, absent signed margin extrema, loss of raw stage copies, partial derivative counts, endpoint-projection mislabeling, unbounded supervisor logs and stale worker acceptance.

- Raw/JSON writes now use exclusive `.partial` files, fsync, atomic rename and directory fsync. Temporary duplicates are charged. A failed partial is retained; a same-path automatic retry cannot silently overwrite it.
- Raw files have exact bytes, shape, little-endian Float64 encoding and SHA256; invalid identity, shape or row bounds fail closed. Reserved identity metadata cannot be overridden. Nonfinite failure values are explicitly encoded rather than silently coerced to JSON null.
- Compact signatures have a frozen observation schedule, actual prefix count, encoding and rolling hash. Appended chunks are fsynced. Interrupted files retain actual length, complete 32-byte records and trailing-byte count. A durable prefix is not an exact interruption state or proof that unwritten pending signatures survived.
- J guard failures retain raw stage, normalized geometry if created, commands, available field and derivative prefix, stage/drone and exact guard. Endpoint projection failure retains the combined endpoint, distinct from k4. A full-stage stream hash does not make general raw stages reconstructible.
- Unexpected H/P integrator exceptions preserve exact input, command, held inflow and vehicle identity but truthfully mark hidden failing stage unavailable. They halt and cannot establish a reference.
- An external kill retains an inventory and last durable checkpoint with `exactStoppedState=false`; it never fabricates an exact final stage. A row may have a separate exact cooperative failure record.
- Source, inputs, adopted plan, amendments, runtime and all independent fixture files are hashed before execution. Frozen originals remain unchanged. Non-wide factory overrides are rejected.
- Worker completion is provisional. The worker does not independently publish final acceptance. Qualification requires all scientific gates plus the outer supervisor's successful, uninterrupted, in-budget validity record. Failed/skipped rows cannot pass by omission.

## Independent deferred fixtures

All five files require `JOINT_REFERENCE_WINDOW_ACTIVE=1`, emit one machine-readable report and exit nonzero on failure. The campaign launches them as separately supervised jobs. They write no real output file themselves; the parent worker retains their stdout/stderr inside the same budget.

1. `test_joint_robustness.cjs`: 10 tests. Simultaneous coupled analytic stages, geometry-copy nonmutation, input guards, endpoint normalization, whole-field-before-derivative ordering, each failing stage, nonfinite derivatives and distinct combined-endpoint failure evidence; exact integer stage/event arithmetic.
2. `test_io_faults.cjs`: 9 tests. In-memory fault-injecting filesystem; exact LE/checksum roundtrip, malformed/truncated raw input, reserved metadata, fsync/rename, partial-write/rename interruption, old durable-file preservation, duplicate/temporary/reserve accounting and explicit nonfinite failure JSON.
3. `test_branch_boundaries.cjs`: 6 tests. Half-open valid-annulus boundaries, equality cases, one-sided ranges, equal-time k2/k3 risk with no endpoint bracket and endpoint-only flag semantics.
4. `test_watchdog_contract.cjs`: 4 tests. Actual supervisor source under a virtual monotonic clock/process tree; process-group kill request, live/reaped CPU accounting, partial inventory, overlap rejection and invalid failed cleanup. This tests the source's decision logic; it does not claim a real OS signal-latency test.
5. `test_runner_clock.cjs`: 2 tests. Actual `run.cjs` with synthetic dynamics/controller/field stubs, for J and H. Exactly 100 controller events, 1,601 common endpoints, old command through an event-ending step, new command only next step, and no terminal discrete refresh. These are scheduler fixtures, not genuine Boids trajectories.

**Total: 31 independent deferred tests, plus the implementer's fixtures.** `node --check` succeeded for all five reviewer scripts. Syntax parsing does not import or execute a model or fixture. Fixture success has not been observed. If a fixture fails after freeze, retain the attempt and stop; do not rewrite the source or reset the budget based on its outcome.

## Stopping interpretation

The allowed outcome is a bounded cross-checked numerical reference for the unchanged model and these prescribed windows, or a retained implementation/domain/numerical/resource obstruction. A smooth toy RK fixture does not establish model order. A branch hash is not a continuous-regularity proof. No outcome alone qualifies an operational airflow cadence, physical truth, safe flight, mission completion, browser speedup or 5,000-drone feasibility.
