# Retention addendum: post-loss recovery, 2026-10-13

This addendum is newly recovery-authored. It supplements the preserved historical report and README without silently editing their original wording or manufacturing missing evidence.

## Historical completeness claims

The historical report says:

> Full source dependencies, configuration, two separately recorded analytic fixture attempts, raw arrays, all gates, all conditional diagnostics, terminal states/held scalars, event hashes and stopping/skipping reasons are retained. No failure was overwritten to produce a successful result.

It also says:

> Retention is complete for the preregistered saved data, not every intermediate step of every run.

Those claims were written for the **pre-workspace-loss** package. They are retained as historical statements, not a certification that the currently recovered package is complete. Some evidence survives in a reattached standalone viewer or in already uploaded Git objects; other original files have not been recovered. The historical README also contains links and a reconstruction command whose original targets are now missing.

## Recovered evidence

- **Frozen source/configuration:** Source-freeze commit `16d106ee0d80adfaaf7fb4f70a24d9349b8ee27b` and uploaded tree `62e8d56e6500228cc536f6966d921697ec0bc3ad`. All 61 frozen source-manifest SHA-256 values, source aggregate, compact-manifest identity, plan, and exact evaluator match. The 163 recovered source/review/robustness text files match their Git identities. Both pre-campaign synthetic robustness attempt records survive.
- **Original standalone viewer:** The reattached HTML has SHA-256 `622ad9c80779dfef9434b92fc18cbc5d57c7b85a340e76a0a42dc0c2e0b54115`, matching its previously recorded identity. Extraction preserved the attachment unchanged.
- **Embedded records:** Thirty direct JSON literals, the historical report/README and other embedded text/module strings survive. These include all ten fresh coupled-run records and common-state sidecars, campaign status, compatibility summary, matrix status, original retention manifest, supervisor/execution-validity records, cadence summaries, and viewer-selected replay summaries/traces. Extraction preserves embedded values and records original literal slices; public JSON may use documented restored serialization. Original file-byte identity is claimed only where independently verified against an existing Git object or original receipt, as recorded in the publication provenance.
- **Two dense sidecar objects:** Full structured metadata survives nested in the corresponding fresh-run `denseStates` objects. Newly extracted standalone sidecar copies are semantic recoveries with recorded provenance, not proven byte-identical copies of the original sidecar files.
- **Raw transport identities:** A complete, non-truncated Git tree inventories 17 binary objects totaling 64,975,968 stored bytes. They represent 11 common-state gzip files, two fresh-inflow gzip files, and four parts for two dense gzip files. The uploaded tree differs from the source-freeze tree only by these 17 blobs and their containing directories. All 139 Git tree identities reconstruct from the inventory.

The historical numerical conclusion remains limited: physics-step screens passed, airflow-reference screens failed, four planned coarse coupled rows were skipped, and no airflow cadence was qualified. Selected replay summaries are conditional diagnostics, not a substitute for the missing full replay records. Recovery-time checks do not establish new numerical or physical validation.

## Not recovered

Paths below are relative to `research/campaign-temporal-sampling/`:

- Full replay records: `implementation/results/replay/s840131-p1-a4.json` and `s840137-p1-a4.json`.
- Full compatibility run record: `implementation/results/runs/s4301-p16-a64.json`. Its summary and raw-object identity survive.
- Three original sidecars: `implementation/results/raw/s4301-p16-a64.states.f64.gz.json` and the two `implementation/results/replay/s84013{1,7}-p1-a4.fresh-inflow.f64.gz.json` files. Some identity/shape metadata survives in the original retention manifest.
- Original `implementation/results/recomputed/reference-gates.json`, `implementation/results/recomputed/verification.json`, `implementation/results/last-checkpoint.json`, and `implementation/results/invocation.json`.
- Original `implementation/viewer-qa/browser-check.json`, `coordination/CLAIM-EVIDENCE-LEDGER.md`, and `implementation/publication-history/pre-label-correction/` history.
- Original `coordination/dense-transport-parts.json` and `coordination/packaging/reconstruct_dense.py`.

The new `raw-recovery-manifest.json` and `reconstruct_dense_recovery.py` replace the last two items for future transport checks only. They are not represented as the original files. Other missing records have not been fabricated from summaries or recreated by rerunning numerical work.

## Raw-content verification boundary

Recovery checked remote Git tree identities, metadata consistency, recovered source hashes, and synthetic reconstruction behavior. **No historical raw binary payload was downloaded or reconstructed during this recovery preparation.** Original compressed/uncompressed identities remain reported metadata until the corresponding contents are independently checked.

The two dense reconstructions require, respectively:

- Seed 840131: 13,371,234 compressed bytes; SHA-256 `94a3799c2e6f177b2d3bd1a9d20fd0b7cd659a1150f509bf47796644cf3605aa`; Git blob SHA-1 `187e90cc3a8c97be30534af54708c2c8e0632d54`.
- Seed 840137: 13,365,454 compressed bytes; SHA-256 `4464824125d4b6aafeb61b3e875eefe3d9afaf07f191d7cda9a042c76fa0ca65`; Git blob SHA-1 `a1add7fd64cc019081446a6525e7a7dada97b2d1`.

These identities come from the recovered original retention manifest; compressed SHA-256 and size also agree with the nested original run metadata. New reconstruction can establish that retained parts produce these original compressed files. It cannot recover the absent provenance and diagnostic records, establish physical accuracy, or authorize a new simulation/replay budget.
