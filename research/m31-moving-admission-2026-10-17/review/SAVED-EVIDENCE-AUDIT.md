# Saved-evidence audit — overall gate failed

The saved package remains **failed**: `check.json` records `passed:false` and `advancement:false`. This audit found **0 discrepancies in 1,121 saved-byte, JSON, identity, count and ordering checks**. That result confirms consistency of the preserved evidence; it does not overturn the failed preregistered gate or independently repeat the scientific checker.

All 20 corruption mutations were executed and rejected, but only 19 triggered an intended preregistered failure family. The sole mismatch is `false-zero-active-leaf`: its saved error is `filter-work-counter-reconstruction`, while its required families are `node-zero-rule` or `node-zero-oracle-member`. Its `intendedCoreFailure` is false. The negative control therefore failed its targeted semantic-path requirement even though the mutation was rejected. No error family was relabeled, no frozen record was changed, and no checker or mutation was rerun.

## Provenance and immutable evidence

Source commit: `2a957d2b0bb26e731c8cd184bc13f51f673e9a0d`.

Source-manifest SHA256: `37a865330bbb86d0aef03dd3de775b830d7398abe69717b80c64860d4a8caa21`.

All 53 manifest file pins match current local bytes and the exact committed blobs. The manifest’s 10,425 bytes, SHA256 and Git-blob identity match the publication receipt. HEAD matched the source commit during this audit. The receipt records exact-commit HTTPS verification at 2026-10-16T22:00:35.509419+00:00. This audit relies on that saved transport receipt for the remote check; it performed no new remote fetch.

Index, checker, generation, attempt and supervision identities agree on source commit, manifest hash, config hash and recorded runtime. All 21 runner source-map hashes match local bytes. Saved candidate/generation descriptors, checker input/reference pins, lifecycle evidence pins, public logs and all four retained private raw-log pins were checked. The 35-file result set is complete and contains no unexpected files. Private directory paths are omitted from the published inventory.

## Complete capture and query schedule

Both saved runs have 64 stable IDs, 51 pose frames at 0.2s cadence from 0 through 10s, and full 17-word captures at 0, 5, 10. Each pose has 448 binary64 words. No terminal diagnostic or missing scheduled slot is present. Returned initial/final raw words match slot 0/slot 10; their pose projections and every scheduled capture match the same-time recorded poses. Each candidate input equals its saved generation-slot capture, and its canonical input digest and generation hash agree throughout the descriptors.

The 27-event journal is contiguous and binds the complete index. It records four fixed-control calls, both saved generation records, the generation-ready barrier, and then six scheduled calls. There are exactly 10 unique filtered method invocations and no replacement state or extra scored terminal. Timing arithmetic and phase prefixes are consistent; the raw-force refusal correctly has only its preparation phase.

## Saved scientific findings, subordinate to the failed gate

The saved checker reports all six scheduled states reached, independently verified, model-admitted and certified, with all four tolerance categories certified over a denominator of 6. Each scheduled reference record contains 16,128 logical nonself rotor/source pairs. These are the preserved checker's findings; this audit did not recompute forces, reference algebra or tolerance bounds.

All four fixed controls have their expected saved outcomes and verified flags: positive and distant-zero are certified; raw-force and order-incompatible are the expected checked refusals. The two run summaries report nontriviality informative, positive-edge times 0, 5, 10, post-initial tilt and each coordinate's relative-displacement witness, and changed edge sets. This audit checked witness presence and binding to saved graph edge sets, without recomputing the scientific thresholds. These favorable component findings do not qualify the experiment for advancement while the overall corruption-control gate is failed.

## Recorded closure and resources

Kernel supervision records success, exit 0, guardian exit 0 and a closed process group. Checker supervision records failure, exit 1, guardian exit 0 and a closed process group. Both record scientific-child absence before guardian release, final group absence, source/runtime rechecks and no containment violation. The guardian start/exit events match each supervision record. The checker failure is consistent with the saved scientific qualification gate, not an unclosed process group.

Kernel and checker attempts started at 22:00:45.737841 and 22:01:14.527753UTC, respectively, after source publication and before the 23:00 UTC launch cutoff. Recorded supervised wall times are 20.455118332989514s and 42.78275154065341s. Peak sampled group RSS values are 414,187,520 and 107,364,352 bytes. These are saved sampled observations; this audit makes no continuous-peak or live-process claim.

| Saved category | Bytes |
|---|---:|
| Kernel scientific evidence, including index/journal | 5,174,437 |
| Checker scientific evidence | 7,561,328 |
| Total scientific evidence | 12,735,765 |
| Metadata and public/private logs | 26,199 |
| Combined saved allocation | 12,761,964 |

The recomputed totals fit the frozen 192 MiB kernel, 64 MiB checker, 256 MiB scientific, 16 MiB metadata/log and 272 MiB combined caps. Published audit artifacts live outside the frozen results directory and are not counted as execution outputs.

## Audit scope and inventory

`SAVED-EVIDENCE-AUDIT-INVENTORY.json` contains the check-group counts, every inspected public file's byte/SHA256 pin and use, private raw-log basename pins, exact totals and limitations. Only saved file reads, hashing, Git committed-byte reads, JSON parsing, equality/count checks and descriptive integer timing arithmetic were performed. No scientific source import, force evaluation, generation, numerical probe, checker rerun or frozen-file edit occurred. Earlier source-preparation reading caps were not reopened; scientific source files were hashed as opaque bytes.
