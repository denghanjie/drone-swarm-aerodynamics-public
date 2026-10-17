# Audit execution and reproduction

Single-use historical allocation. Read source-manifest.json, source-publication.json, PROTOCOL.md and results/check-attempt.json if present. An existing attempt forbids repeat execution here. Independent reproduction requires distinct evidence storage and its own declared allocation.

From the repository root, with the pinned Python and a fresh private log directory outside this repository:

```text
RESEARCH_PRIVATE_LOG_DIR=PRIVATE_DIRECTORY RESEARCH_EXECUTION_CONTEXT=tool-require-escalated PINNED_PYTHON -I -B research/m31-native-saved-audit-2026-10-17/source/run.py AUDIT_MANIFEST_SHA AUDIT_SOURCE_COMMIT
```

The tool dispatch must actually be escalated; the environment label alone is not permission. The supervisor verifies exact public source binding before the child can import the unchanged checker. Original source pins and generated input hashes are verified again after execution. Original results/check.json and results/check-attempt.json must remain absent.

Interpret the new attempt first: completed requires child exit0, all checker integrity/fixture/corruption assertions and preservation. Read check.json decision separately. Original browser supervision remains failed even if the separate audit completes and numerically qualifies all twelve outputs. No browser is opened or numerical producer rerun by this audit. Keep the existing localhost8876 viewer server.
