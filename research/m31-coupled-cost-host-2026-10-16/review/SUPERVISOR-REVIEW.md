# Host replacement: focused source review

Source-only review, 2026-10-16, of `research/m31-coupled-cost-host-2026-10-16`. Reviewed the supervisor diff, replacement execution amendment and unchanged reviewer's supervisor/resource checks. Compared the four numerical source files directly with Git commit `4fdcc83fe870c110679a72666029d4cbc987e22c`; all comparisons were byte-identical. This was not a new full kernel review. No supervisor, candidate, numerical module, saved-record checker, diagnostic child or timing workload was executed.

**Disposition:** no remaining blocking implementation finding in the focused review. Final source-manifest construction, publication and independent remote verification remain required before either separately authorized host invocation; they are not certified by this note.

Reviewed wrapper SHA-256: `e9a085abc9544292f5312ce148ab6fcda60146dbb754b11be87d9b762b824e26`.

Reviewed protocol SHA-256: `76ab49e4b7af3b91e6424c4f98554bb636718ce522b37aae94daf3f6351076a2`.

## Numerical identity and isolation

The following replacement files match the original immutable source bytes:

| File | SHA-256 |
| --- | --- |
| `source/experiment.cjs` | `af36eab1f047778fecb0b831db35cdb156f1e8c7517252605eceed94193fea23` |
| `source/kernel.cjs` | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `source/reference-excerpt.cjs` | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| `source/review.py` | `a0e7cc3fdbfe5374e935e86bbe771d896e512e87e173d08b715b390c239ae8d2` |

`SCHEMA.md` also retains its original hash, `02b19f672498c27e754b138e2de8c9232555a36595314fbe4084589a93de6bf8`. The candidate takes the new package path as its output base and resolves the same sibling swarm-transfer input/reference package; the reviewer also takes the new package/output paths. The wrapper's locks, logs and run records are under the replacement package's own `results` directory. These paths do not reopen or overwrite the earlier campaign.

The execution amendment preserves the 21 controls, eight qualification builds/16 solves, 84 full calls, 56 cached calls, tolerances, stopping rules and comparison criterion. The original scientific rules remain in the protocol, with the new allocation and host-dispatch amendment explicit. This supports numerical reuse without scenario selection or model tuning, while retaining the exposed-development-workload limitation.

## Supervisor findings

The changed wrapper records the phase and errno of supervisor exceptions, catches `OSError` from RSS monitoring, treats nonpositive RSS as invalid, and records actual reaped return status during cleanup. A live-child monitor failure produces `monitorErrors` and terminates the process group with the existing failure mechanism; it is not turned into a zero-RSS observation.

If an RSS attempt fails and the subsequent `proc.poll()` confirms that the child has already exited, the exception is retained in `monitorExitRaces`, the loop ends and the child is reaped normally. There is no extra RSS attempt or replacement invocation. This is an acceptable predeclared completion rule: it records an unsuccessful sample associated with confirmed completion, not proof that child exit caused the helper failure. A prior sample is not fabricated. The unchanged candidate reviewer still requires at least one positive-count external RSS sample, a finite recorded peak, successful child status and absence of supervisor exception/termination.

One blocking completion-status defect was found and corrected before this final review. Recording a zero return code during cleanup could otherwise make the wrapper exit successfully despite a supervisor exception. The final `supervisor_success` predicate now requires return code zero and no `exception_class`, `terminated_for`, `cleanup_exception_class` or `monitorErrors`; the wrapper's exit status uses that predicate. The protocol discloses both this condition and the separately recorded monitor-exit completion case. A scientific child failure therefore cannot become successful merely because cleanup completed.

## Bounds and remaining limits

The wrapper retains one 300-second candidate and one 60-second saved-review allocation, 1.5 GiB sampled child RSS limit, 0.2-second sampling interval, 4 MiB combined child logs and 132 MiB result-directory guard. The candidate's unchanged cooperative 295-second and scientific-output guards remain in its original source. RSS-helper waits are bounded at two seconds and child waits at five seconds. These are sampled/cooperative controls, not hard real-time whole-tool deadlines; process startup, filesystem work and final artifact hashing can extend total tool duration. The recorded supervisor interval ends before final artifact hashing, as before.

Phase fields are retained in the final run JSON rather than a continuously flushed journal. Abrupt supervisor loss or a final filesystem failure can still leave incomplete evidence; absence of a complete record must not be treated as success. The context string is a label, so actual host approval and dispatch receipts remain necessary. The wrapper verifies current Git commit, committed/local manifest bytes and every committed/local pin before consuming the new lock; the coordinator must independently verify the published remote checkpoint and include the frozen failure/admission dependencies in the completed manifest.

Both older scientific/review allocations and both infrastructure allowances remain consumed. This new execution allocation does not restore the old budget, locate the old PermissionError retrospectively, or establish that the old candidate never briefly computed. Any result must retain those limitations and satisfy the unchanged scientific qualification and saved-record audit before a timing claim is made.
