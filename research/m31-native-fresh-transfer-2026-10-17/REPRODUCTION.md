# Recorded execution and independent reproduction

This historical allocation is single use. Never rerun an occupied stage or overwrite saved evidence. A later independent reproduction requires a distinct package/allocation and prospectively fixed output paths.

Read PROTOCOL.md, EXECUTION-ALLOCATION.md, config.json and runtime.json. Supply local installations through environment variables rather than publishing personal paths: RESEARCH_NODE (pinned executable), RESEARCH_NODE_MODULES (pinned Playwright modules), RESEARCH_CHROME_CONTENTS (matching Contents directory), RESEARCH_PRIVATE_LOG_DIR (one shared private directory for all four stages), RESEARCH_BROWSER_PROFILE (fresh nonexistent directory nested inside that private directory), and RESEARCH_EXECUTION_CONTEXT=tool-require-escalated.

From the repository root, dispatch each separately after inspecting its predecessor:

```text
PINNED_PYTHON -I -B research/m31-native-fresh-transfer-2026-10-17/source/run.py generation SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
PINNED_PYTHON -I -B research/m31-native-fresh-transfer-2026-10-17/source/run.py reference SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
PINNED_PYTHON -I -B research/m31-native-fresh-transfer-2026-10-17/source/run.py browser SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
PINNED_PYTHON -I -B research/m31-native-fresh-transfer-2026-10-17/source/run.py check SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
```

Read attempt status, preservation checks and operational completion separately from numerical qualification. The exact helper uses fixed enclosures, without empirical physical calibration. Browser force/moment exclude gravity/rotor-reaction torque respectively. Single diagnostic times are not performance estimates. The existing local8876 viewer server is retained. Byte-only build-bundle.py was executed once before freeze; it concatenates source bytes without importing the scientific modules.

The source manifest pins the new source plus the previously published native/audit provenance closure. Source-publication.json binds its exact public commit; a subsequent result manifest will bind outputs and review. Use file hashes to inspect records without executing scientific modules.
