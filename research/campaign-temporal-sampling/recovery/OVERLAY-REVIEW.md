# Final recovery overlay review

Review scope: public entry-point documentation, restoration warnings, display-only banner, serialization provenance, final file inventory, relative links, and dense reconstruction instructions. No scientific run, aerodynamic replay, historical binary reconstruction, browser rendering, or remote write was performed.

Verdict: suitable for publication as an explicitly incomplete evidence-recovery checkpoint. It must be overlaid on the retained raw tree, not substituted for that tree.

- The current README and restoration addendum clearly separate surviving evidence from missing full replay/compatibility records, sidecars, original audit receipts, and later archival material. The preserved historical report and offline HTML are unchanged; their historical complete-retention wording is explicitly qualified.
- Both airflow-reference screens remain failed, no cadence is qualified, and no physical-validation or general flight-safety claim is introduced. Reported timing remains a historical supervised duration, not a regenerated benchmark.
- Current entry-point Markdown/HTML links resolve against the retained base tree plus overlay. Known unavailable links in preserved historical documents remain disclosed. The demo change only corrects presentation text and adds a recovery warning; rendering remains unverified.
- The extraction and formatting scripts are explicitly labeled archival staging provenance with unavailable-layout dependencies. They are not presented as portable checkout commands. The separately tested dense utility has portable instructions, verifies ordered parts and both original joined identities, preserves inputs, and refuses mismatched destinations.
- `PUBLISHED-FILES.json` records final repository-relative paths, sizes, SHA-256 values and Git blob identities. It explicitly excludes itself from recursive hashing; the containing Git tree supplies its own immutable identity. The earlier extraction manifest retains staging labels and source-literal hashes as provenance.
- The reviewed transport utility is unchanged from `TRANSPORT-REVIEW.json`. All 17 original raw objects remain inherited from the base tree; this overlay introduces no replacement raw array or numerical-source change.

Publication still requires a final Git tree check of the retained raw identities and the intended branch update. This local review does not represent that future remote verification as already completed.
