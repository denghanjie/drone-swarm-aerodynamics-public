# Supervision and guardian source review

**No remaining source blocker was found after the durability correction.** The scope is the declared non-hostile, no-scientific-descendant workload. This is source review, not a measured containment/cleanup test or permission to execute.

Final SHA-256:

- supervise.py: `053cc97e59830b838d95d73474b8eb597c4b23c1b6783f2555d4db79b9149868`
- guardian.py: `5c97c5a23556120226fab52955e427144d8ae69beb685e18d667bc6b66e1717a`

Recursive closed-set results accounting rejects unexpected files/directories and symlinks, includes all four private raw log files across both stages and their public copies, and enforces the declared 8 MiB index/journal, 64 MiB individual science/anomaly, shared 128 MiB science/anomaly, 96 MiB checker, 16 MiB logs/metadata, two 64 KiB supervision reports and 384 MiB aggregate categories. Final report capacity is reserved; final accounting catches public-copy growth. Sampling can observe a limit only after it is crossed, so these are fail-closed observed limits rather than instantaneous ceilings.

The source-manifest and publication-receipt bytes are retained and rechecked. Every manifest source pin and both runtime executables are checked before and after the child. Required membership includes the runner/canonical/checker/reference/guardian/supervisor chain. Checker admission requires successful closed kernel supervision, no terminal failure or anomaly, the exact eight kernel scientific files (index, journal, six shards), the same private-log directory identity and both kernel raw-log pins. Those pins plus kernel supervision are rechecked after the checker; emitted checker evidence is pinned. Actual external publication verification is a separate prerequisite represented by the receipt and was not performed here.

The new-session guardian retains its process-group leader until the child exits and the supervisor observes scientific-child absence. It writes lifecycle events, requires explicit release, and watches pipe loss and its 1810-second deadline. Supervisor tracks RSS, descendant structure, actual sample gaps and the 1800-second stage deadline. Failure signals only an owned live guardian group. Guardian finally terminates/waits/kills its direct child independently of whether lifecycle logging succeeded. Group absence is required for closed and successful qualification; terminal finalization failures cannot qualify or permit the next stage. This is not hostile-code or escaped-descendant isolation.

The only identified storage correction is complete and its preserved-to-final diff was inspected: exclusive attempt/report dump flushes and fsyncs file plus parent; results creation syncs the package parent; guardian event-log creation fsyncs file plus parent before launching the scientific child. This makes the sole-attempt and lifecycle records consistent with checkpoint durability intent.

Both final Python files passed independent standard-library AST parsing without import, main execution, bytecode, or child launch. No actual stage ran. No additional inherited semantic file was read; the cycle remains 7/16. Associated inventory records all new-source reads and snapshots.
