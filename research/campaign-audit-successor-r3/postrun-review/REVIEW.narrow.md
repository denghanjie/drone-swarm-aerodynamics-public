# R3 retained-evidence review: results-only summary

This separate publication derivative reports aggregate findings from the completed local review. Original reports and evidence remain unchanged. Broader inventory publication is pending; this results-only subset is incomplete for full reproduction.

## Supported partial findings

- **81 synthetic cases** passed. Their retained required case metadata and counts agreed with the adopted requirements.
- All **11 baseline/candidate artifact pairs** were byte-identical: 22 files, 272,572 bytes total.
- **19 saved-state cases** fully passed. The twentieth case completed its paired baseline/candidate observation but failed its historical-anchor check before finish. Its saved active-case label does not mean a job is still running.
- Of **229 required named cases**, **100 fully passed, one failed while active, and 128 were unattempted**. The failed child reports **20 paired observations**, including that twentieth case, and 19 completed anchors.
- **82 jobs** were planned: one passed, one failed, and 80 never started. All **64 performance jobs** and the independent full-corpus correctness gate were unrun.

## Aggregate resources and limits

Final accounting records **4.2006738310046785 s wall** and **5.604814999999999 s process-tree CPU**, before its own 931-byte write. No exact post-write time is retained. Terminal logical storage reconciled to 1,998,424 bytes for the new study and 140,445,684 combined bytes at that point; later static documentation adds storage. These observations are not benchmark results.

Peak child RSS was 238,829,568 bytes; the conservative serial-tree bound was 263,184,384 bytes. Active-tree RSS was sampled. The final in-window frozen/runtime checks were explicitly skipped after failure. Later static review does not retroactively supply those checks or a gate pass.

Full correctness, speedup, a qualified numerical reference, and physical validity remain unestablished. The raw failure capture and detailed inventories remain outside this subset. No scientific code was rerun to produce this summary.

[Original synthetic receipt](../implementation/results/receipts/synthetic.json) · [Original failed saved-state receipt](../implementation/results/receipts/saved-json-states.json) · [Original final accounting](../robustness-review/results/FINAL-ACCOUNTING.json) · [Results-only milestone](../postrun-report/MILESTONE.narrow.md)
