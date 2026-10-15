# Viewer source preparation — 16 October 2026

Delivered a new recorded-engineering viewer source for the GPU-readback trial. It includes a pending state, strict digest-bound file loading, three direct byte comparisons, 32 selectable words with 128 byte cells, an accessible byte table, independent evidence-scope panels, retained failures and trace inspection. No data manifest or result is included.

The source is prepared for the root-agreed final disposition and external-review receipt paths in `DATA-CONTRACT.md`. `bind.py` is source for a later explicit binding operation after actual terminal disposition exists; it has not been invoked.

Status: source authored and read only. No syntax execution, tests, browser inspection, screenshot QA, GPU work, network request, diagnostic, saved checker, binder execution or publication occurred. Rendering and interaction are unverified until later authorized QA. All edits were confined to the isolated delivery directory.

Install the source files together in the new trial's `viewer/` directory. Keep `binding.json` and `evidence.json` absent until real closed records are available. Preserve this pending/unavailable behavior for missing, malformed or digest-mismatched evidence; do not create demonstration trial results.
