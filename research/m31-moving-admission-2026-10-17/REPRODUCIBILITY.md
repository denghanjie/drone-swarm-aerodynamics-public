# Official one-shot reproduction boundary

Before any official invocation, read PROTOCOL.md, RECORD-CONTRACT.md, source/config.json, source/result-contract.json and SOURCE-DECISION.md. The complete source manifest must be publicly committed and independently retrieved at that exact commit; source-publication.json records the byte-for-byte manifest/local/Git verification. The working HEAD must stay at the verified source commit during both scientific stages. No old allocation is reopened.

Use the locally pinned executables through explicit paths (paths themselves remain private):

```sh
export RESEARCH_NODE=/absolute/path/to/pinned/node
export RESEARCH_PRIVATE_RUN_DIR=/tmp/new-private-moving-admission-run
/absolute/path/to/pinned/python3 -I research/m31-moving-admission-2026-10-17/source/supervise.py kernel
/absolute/path/to/pinned/python3 -I research/m31-moving-admission-2026-10-17/source/supervise.py checker
```

Run the checker only after the kernel supervision report establishes successful process closure and unchanged source/runtime/evidence. No second official invocation or removal of attempt markers is allowed. A third-party reproduction needs a separately declared allocation namespace and its own source/runtime/provenance review; the published official supervisor deliberately refuses use after its fixed overnight launch cutoff. This timestamp is a provenance boundary, not a mathematical dependence.

The source/run.cjs runner makes four fixed-control calls, then generates and saves both trajectories, then evaluates the six prescribed snapshot slots when reached. All data remains tied to source/config/runtime identity. The saved-only Python checker uses independent exact helpers, applies20intentional corruption recipes and reconstructs the six-state decision. Kernel/checker wall/RSS/output caps are containment, not performance guarantees. Both helpers and all scientific JavaScript modules are inherited byte-for-byte; generator source files remain at their original repository paths and are manifest-pinned.

No scientific imports are needed to inspect saved records. Read results/index.json for every scheduled slot, results/generation for original full-state captures and replay poses, results/scenes for calculated outcomes, results/reference for independent pair/graph/load evidence, results/check.json for integrity/admission/nontriviality decisions, and supervision/log records for lifecycle evidence. If a stage fails before any of these files exists, preserve the failure and do not infer absent data.

The Three.js viewer reads saved evidence only. Its playback rate is unrelated to the scientific method’s execution rate. Every result must be accompanied by its plain-language milestone summary, claim ledger and updated restart instructions before public closeout.
