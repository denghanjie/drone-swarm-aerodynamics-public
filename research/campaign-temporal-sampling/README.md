# Temporal airflow study: recovered evidence checkpoint

**No airflow cadence is qualified. Both airflow-reference screens failed.**

Start with [restoration limits](implementation/RECOVERY-ADDENDUM.md). The raw arrays and core records are preserved, but this is not a complete restoration of the lost final archive.

- [Recovered historical report](implementation/REPORT.md)
- [Actual-record Three.js replay](implementation/demo/index.html)
- [Downloadable offline replay](implementation/temporal-airflow-evidence.html)
- [Attempted and skipped matrix](implementation/results/matrix-status.json)
- [Campaign and gates](implementation/results/campaign.json)
- [Raw dataset manifest](implementation/results/RAW-RETENTION-MANIFEST.json)
- [Published file identities](recovery/PUBLISHED-FILES.json)
- [Extraction provenance manifest](recovery/RECOVERY-MANIFEST.json)
- [Independent recovery review](recovery/REVIEW.md)
- [Frozen plan](implementation/PLAN.md)
- [Previously published literature audit](../research-audit-20261013/README.md)

The original source freeze is 16d106ee0d80adfaaf7fb4f70a24d9349b8ee27b; the raw-data checkpoint is b9bd5065d02561920af27468f5e4740b301bd174. Frozen code and raw Git objects are retained unchanged. No new experiment was run during recovery. Final publication metadata and its verification receipt belong to the recovery, not the original numerical execution.

To view locally, serve this repository with a local HTTP server and open implementation/demo/index.html under this directory, or download the self-contained HTML. Rendering remains unverified after the earlier browser restriction. This numerical study does not validate the physical model or real flight safety.
