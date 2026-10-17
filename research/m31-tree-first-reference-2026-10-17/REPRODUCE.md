# Reproduction and scope

This package preserves one preregistered finite-corpus comparison of two exact reference dispatchers. Read PROTOCOL.md and the review documents before interpreting results. Its prospective driver deliberately refuses after the historical window and refuses repeated use of the same output directory. Do not remove these gates to call a retrospective run the original experiment.

The original launch command was planned as:

```text
PINNED_PYTHON -I -B research/m31-tree-first-reference-2026-10-17/source/run.py REPOSITORY SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
```

The manifest identifies the executable bytes/version and all source/evidence dependencies; source-publication.json records the exact published commit. A later reproduction needs a separately documented allocation, fresh result directory and clear provenance, preserving this package unchanged. The algorithm can be reviewed directly in source/tree-reference.py; source/validate.py is an independent small-case comparison path, while source/corruptions.py binds six fixed adversarial mutations. Results are not a benchmark. The model and arithmetic law remain those of the frozen fresh-transfer sources.
