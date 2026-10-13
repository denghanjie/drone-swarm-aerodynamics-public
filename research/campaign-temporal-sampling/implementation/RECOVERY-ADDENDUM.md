# Restoration limits and negative result

This recovery checkpoint was assembled on 2026-10-13 after the latest local working directory became unavailable. Its cause is unconfirmed. It preserves evidence from the original campaign; no simulation or aerodynamic replay was repeated to fill gaps.

The historical REPORT.md and offline viewer are recovered unchanged from the user-reattached artifact (SHA256 622ad9c80779dfef9434b92fc18cbc5d57c7b85a340e76a0a42dc0c2e0b54115). Their complete-retention statements described the pre-loss workspace, not the current completeness of recovered metadata. Read the gaps below before relying on those statements or their links.

## Preserved and restored

- All 15 raw datasets remain in Git: 13 whole gzip files plus 4 lossless parts for the 2 dense-state gzip files. Raw objects were pinned in commit b9bd5065d02561920af27468f5e4740b301bd174.
- Frozen source, configuration and plan are unchanged; all 61 source-manifest identities pass.
- The attached viewer preserves 30 direct JSON records, 4 module strings and 5 text entries (two license aliases). These restore campaign/gate/execution summaries, all 10 fresh full-run records and 10 common-state sidecars.
- Two dense sidecars were recovered from the complete nested objects in driver run records; their original standalone whitespace is not claimed. Six larger full-run JSON files also match existing immutable Git blobs byte-for-byte. Other JSON may use a documented restored serialization.

## Not recovered

The two full conditional replay JSON files, full compatibility-run JSON and its sidecar, two instantaneous-inflow sidecars, original invocation/checkpoint/recomputed receipts, browser failure receipt, later literature/claim ledgers and packaging/history files are not recovered in this checkpoint. Report tables and viewer summaries are retained, but they are not substitutes for the missing full diagnostic records. Some historical report links therefore remain unavailable. Original raw arrays survive and may support a separately recorded future derivation; no such derivation is represented as original evidence here.

## Scientific result remains unchanged

The original campaign attempted 11 coupled runs (one compatibility + 10 fresh), skipped 4 planned coupled rows, and completed 2 conditional saved-path diagnostics. Both physics screens passed, both airflow-reference screens failed, and no cadence is qualified. The recorded supervised window was 51.135539888 seconds. A completed animation or collision-free record is not physical validation or general flight safety. This remains an unvalidated physical model and a small N = 16 numerical study, not a 5000-drone browser performance result.

## Verification and reconstruction

The current recovery audit verifies retained identities and report/record consistency. Binary Git IDs and lengths are recovered; this recovery did not download and independently rehash every binary. The earlier audit was reported before workspace loss; it is not falsely recreated here. The new offline-only utility verifies all 17 Git objects, joined dense hashes and existing destinations before reconstruction. See ../recovery/reconstruct_dense_recovery.py and its manifest/tests. It is a new recovery utility, not the lost original. Run from the repository root: python3 research/campaign-temporal-sampling/recovery/reconstruct_dense_recovery.py --root . --verify-only

Remove --verify-only to join the two dense gzip files locally; original parts remain. Missing diagnostic records are not regenerated. Browser-rendered QA was blocked before the loss and has not been rerun; source/data checks do not prove rendering.

## Extraction tooling provenance

The preserved extraction and JSON-formatting scripts are archival staging provenance, not portable checkout commands. They depend on the original temporary recovery layout and can write extraction outputs/manifests. Do not run them over this published evidence directory. See [extraction provenance](../recovery/EXTRACTION-PROVENANCE.md). The dense reconstruction utility above is the separately tested, portable command.

[Published file identities](../recovery/PUBLISHED-FILES.json) records the final repository paths, sizes, SHA-256 values and Git blob identities for this overlay. The earlier extraction manifest retains its original staging paths and literal hashes; those are provenance labels, not a map of final public filenames.
