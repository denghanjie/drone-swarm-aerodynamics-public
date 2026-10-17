# Execution and audit

This is a single-use recorded allocation. Do not rerun an occupied stage or overwrite its evidence. Reproduction in an independent checkout requires a separately declared allocation and distinct result storage; it must not rewrite this historical record.

Read PROTOCOL.md, EXECUTION-ALLOCATION.md, runtime.json and the source manifest. Resolve the matching pinned Python/Node and Chrome/Playwright installations. Environment values supply local paths without embedding personal installation paths in public files:

- `RESEARCH_NODE`: pinned Node executable.
- `RESEARCH_NODE_MODULES`: directory containing pinned Playwright packages.
- `RESEARCH_CHROME_CONTENTS`: matching Chrome application Contents directory.
- `RESEARCH_BROWSER_PROFILE`: fresh nonexistent private profile directory.
- `RESEARCH_PRIVATE_LOG_DIR`: private directory outside the public repository; stage logs are exclusive.
- `RESEARCH_EXECUTION_CONTEXT`: `tool-require-escalated` for the registered tool dispatch.

From the repository root, the registered commands are:

```text
PINNED_PYTHON -I -B research/m31-native-load-baseline-2026-10-17/source/run.py browser SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
PINNED_PYTHON -I -B research/m31-native-load-baseline-2026-10-17/source/run.py check SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
```

The supervisor verifies source and runtime pins and source-publication.json before launching a retained group guardian. The controller verifies and serves only source and raw inputs to named Chrome. It saves all fixed calls to an exclusive journal and final output. The checker compares actual delivered words with the independently verified saved exact-reference enclosures; it does not repeat the earlier exact-reference solves. Administrative source packaging uses source/build-bundle.py once before freeze and executes no scientific factory.

Inspect results/browser-attempt.json and results/check-attempt.json before interpreting outputs. A completion flag means the bounded stage completed, not that scientific qualification passed. In results/check.json, `passed` denotes accepted record integrity and checker fixtures; `decision` distinguishes qualified from unqualified. Raw call times in browser.json are diagnostic observations without warmup/repetition and must not be promoted to a performance result.

The public source manifest binds all scripts, fixed cases, reference evidence and their provenance. A later result manifest binds actual outputs, analyses, viewer and review records. Publication receipts identify the exact remote commit and manifest bytes. Current local server 8876 is retained for visualization; the qualification controller's route handler serves pinned source/input bytes without changing that server.
