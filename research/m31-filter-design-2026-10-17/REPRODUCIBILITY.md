# Reproduction and interpretation

This package has one official kernel allocation and one official independent-checker allocation. Source publication and exact remote byte verification must precede either. The public receipt identifies the source commit; the source manifest pins the new implementation, independent helper, inherited baseline dependencies, fixtures, protocol, reviews and runtime binaries.

The official invocation uses the pinned Node and Python binaries already available to the research environment. Paths are supplied locally rather than published:

```sh
export RESEARCH_NODE=/absolute/path/to/the/pinned/node
export RESEARCH_PRIVATE_RUN_DIR=/tmp/m31-filter-correctness-private-run
/absolute/path/to/the/pinned/python3 research/m31-filter-design-2026-10-17/source/supervise.py kernel
/absolute/path/to/the/pinned/python3 research/m31-filter-design-2026-10-17/source/supervise.py checker
```

The checker may start only after the kernel supervisor reports successful execution, closed processes and unchanged identity pins. Scientific qualification additionally requires the independent report's full correctness/coverage/control gate. A successful process exit alone does not qualify the model. The public source receipt must match the local manifest; code refuses an absent or mismatched receipt. Environment variables do not alter fixtures or acceptance thresholds.

The existing attempt marker prevents rerunning either official stage. Preserve failed/partial output. A separate independent reproduction requires a clean source checkout, its own new attempt namespace and a verified receipt for that exact source; do not erase this package's attempt markers, overwrite evidence, or alter its frozen limits. A different runtime needs separate qualification rather than editing the binary pins. No paid resource or dependency installation is required by the official attempt.

Inspect `results/filter-results.json` and its110-event journal for all108 ordered records. `results/reference.json` retains the independently reconstructed values; `results/independent-check.json` records validation and16 deliberate corruption controls. Supervision records include elapsed containment time, sampled memory, actual sample gaps, scoped process lifecycle and output identities. These are not method-performance benchmarks. Private raw logs remain private; any public copies must retain documented sanitization and exact public hashes.

The viewer reads saved evidence only. It renders the selected pair's prepared geometry and shows fast-zero/fallback decisions, raw preparation refusals and arithmetic checks. Its hashes bind the saved records. Rendering is not a new experiment or a real-time aerodynamic simulation.

The source-based enclosure argument, finite experimental validation, later total-cost performance, physical-model validation and originality are separate claims. Keep that distinction when reproducing or citing this checkpoint.
