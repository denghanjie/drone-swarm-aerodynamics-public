# Independent robustness, failure-retention, resource and cost review

Status: STATIC PREPARATION IN PROGRESS. No audit/model imported, no trajectory decoded, no numerical fixture, geometry, replay, benchmark, fake-workload supervisor test, or receipt mutation test executed. Only source inspection, metadata inventories, file-byte arithmetic and syntax analysis are allowed at this stage. All outputs are prospective and do not constitute an execution release.

## Useful findings

1. Old research-next retained 133,854,607 logical bytes across 270 files at the first independent census. Even the entire proposed 16,000,000-byte new-study allowance remains below the combined 200,000,000-byte cap. Old evidence is neither deleted nor modified to create space.
2. The historical 35.093140530-second bucket includes safety/diagnostics work beyond the audit. Its division by 25,385 observations is only a planning proxy. Neither audit-only share, allocation/GC cost, Math.hypot share nor end-to-end speedup has been measured.
3. Full public-output consumption requires retaining and hashing every returned sample, not only finish aggregates. The implementer corrected this before freeze. In-memory sample retention, canonical graph encoding, digest work and garbage collection add startup/job CPU/RSS cost beyond the original 55.5-second audit proxy. Four additional correctness workload-contract jobs are needed to derive the benchmark semantic digests. The nominal 71.9-second estimate remains uncertain and excludes these additional costs; a resource stop is a valid outcome, not permission for more passes/time.
4. Correctness has 35,597 rows per variant, 220 saved bracket sides in 110 labeled brackets, 23 initial/final/exact-stop JSON cases, two whole original preflight reproductions, all named synthetic cases, and four workload-contract jobs. Retained real RK-stage sides remain zero.
5. The exact partial P1 state is tick50,768. The durable checkpoint tick50,688 and last common row tick50,752 are different data and must never substitute for that exact stop.
6. No numerical work is released. Final fixture completeness, bounded failure serialization, source identities, concrete storage forecast and gate interfaces remain pre-release blockers until their final source exists and is reviewed.

## Prepared independent artifacts

- supervise.py: one-shot Linux resource supervisor; phase ordering and fixed serial64 benchmark slots; mandatory independent correctness gate; separate monotonic wall/CPU limits; wait4 exited-process CPU/maxRSS; /proc live-tree accounting; Linux subreaper; no numerical subprocesses/worker threads; group termination; normal/failure retained-byte limits and atomic overlap accounting.
- validate_cost_receipts.py: independent exact receipt/count/digest validation, all64 child records, actual1+2 pass counts, semantic digest anchored to independently checked correctness, all8 paired ratios for each workload/seed, median/range, RSS allowance, baseline0.100-second screen, no outlier removal/extra passes/seed pooling.
- test_receipt_rules.py: deterministic synthetic negative-test definitions for missing/extra/measured pass, warmup contamination, configured versus actual counts, missing pair/margin, wrong digest/freeze, unconsumed output, excluded finish, instrumentation, invalid CPU/RSS and failure inclusion. Prepared, not executed.
- ROBUSTNESS-MATRIX.json: independent nine-family boundary/lifetime/persistence review checklist, corpus counts and declared future supervisor failure tests. Prepared, not executed.

## Resource accounting contract

Supervisor wall starts from the Linux process-start monotonic tick, conservatively including Python startup. Supervisor CPU is full process CPU; exited direct children are retained through wait4/RUSAGE_CHILDREN. Every live descendant contributes own CPU and already-reaped descendant CPU; live children are not replaced by supervisor-only process.cpuUsage. No more than one numerical process is permitted. Unexpected descendants invalidate qualification; Linux subreaper and process-group termination retain cleanup accounting.

Correctness, including identity checks and the independent receipt gate, gets at most180 wall and180 CPU seconds. Performance gets at most90 wall and90 CPU seconds. The supervisor begins final accounting by270 wall/CPU seconds, preserving the prescribed30-second allocation inside300, and therefore also respects the outer298 numerical-stop requirement. Unused phase time cannot extend another phase. Each child receives45/20 wall/CPU hard limits, a1-second cooperative reserve, external watchdog and supplementary kernel CPU limit. No next child is launched after any failed/incomplete/stopped job. An exclusive attempt marker prevents resetting/restarting the window.

RSS is polled while active and /proc values are approximate; wait4 preserves exited child maxRSS, including peaks between polls. Qualification also uses the conservative sum of supervisor maximum RSS and the largest serial child's maximum RSS against1GiB, so it does not require claiming sampled aggregate RSS is an exact instantaneous maximum. Children must each remain at/below512MiB. Unexpected descendants invalidate this serial bound. The watchdog's polling/OS scheduling granularity is disclosed; observed overshoots cannot qualify.

All output allocations count logical bytes, not compressed/physical blocks, including .partial files and existing target+temporary replacement overlap. Normal outputs stop before14,000,000 new bytes;2,000,000 remain reserved for failures. The combined old/new cap remains200,000,000. Children also independently reserve their writes; sampling alone cannot guarantee a peak-byte cap. No passing record may be truncated/deleted to fit.

A supervisor checkpoint records only completed durable work. It is never an exact interruption state. First disagreement must separately retain the saved selector or synthetic definition, exact raw input bytes, both available output/error values, mismatch path/index, partial state/counters and actual stop reason. If SIGKILL or failed writes prevent an exact capture, record that loss explicitly and block qualification. Broad whole-workload counterexamples require careful bounding against the2MB failure reserve before release.

## Fair cost interpretation

W-ENDPOINT uses257 observations/pass; W-STAGE-FIXTURE uses161. Exactly64 fresh children each execute one isolated warmup plus two timed passes, giving40,128 total observations and26,752 measured observations. Actual output lengths and completed passes must underpin counts. Per-pass results are consumed outside timing and include every public sample and finish output; finish is inside timing. Required per-observation resource guards are included in these elapsed replay times and cannot be called pure kernel cost. Loading, preparation, warmup, consumption, I/O and child shutdown still count toward full job/phase/window budgets.

Full raw timing pairs, warmups, per-pass values, job wall/CPU, independent maxRSS, all8 ratios, median and range remain visible for each workload/seed. A baseline shorter than0.100 seconds is inconclusive with no extra passes. C1 primary median wall<=0.80 and CPU<=0.85 plus7/8 wall ratios<1 must pass separately for both seeds. Stage medians must be<=1.05 wall/CPU separately. RSS median increase must be<=max(10% baseline,16MiB). No combined-seed averaging, selected-block removal, steady-state claim, inferred real-stage replay, persistence speedup or physical/reference qualification is permitted.

## Pre-release pending checks

- Complete implementer fixture definitions crosswalk to every ROBUSTNESS-MATRIX requirement, including same-object/frozen inputs and all persistence variants.
- Concrete complete normal-output/temporary/failure forecast. Large passing corpus-risk aggregates may be directly compared in memory with streamed receipts, but all required comparisons and first counterexamples must remain complete.
- Final jobs/receipt/freeze integration; source/old-input identity hashes and runtime flags; independent gate passed status and four semantic digest anchors.
- Static reinspection of final child failure capture, writer reserve mode, actual pair counts and no descendant execution.
- Coordinator explicit release and no competing browser/rendering/numerical/package/upload work before any numerical or timing work.

## Resource-interface primary documentation checked

Linux man-pages documents that RUSAGE_SELF includes all threads, while RUSAGE_CHILDREN retains waited-for exited children and descendant usage when intervening processes waited. Its child max-RSS value is the largest child's high-water value, not a simultaneous tree maximum. This is why this review requires per-child wait4 records and a separate conservative serial-tree bound. [getrusage(2)](https://man7.org/linux/man-pages/man2/getrusage.2.html)

The /proc stat specification defines utime/stime/cutime/cstime in clock ticks, and RSS in pages; it explicitly warns that the RSS field is approximate. The active census therefore cannot claim an exact instantaneous memory maximum. [proc_pid_stat(5)](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html)

wait4 provides a child's resource-usage record when it is reaped. It is the supervisor's only reaper; calling Popen.poll/wait first would lose that per-child record. [wait4(2)](https://man7.org/linux/man-pages/man2/wait4.2.html)
