# 2026 centerline amplitude-screen checkpoint

The unchanged model's nominal predictions exceed six preselected published centerline velocities by 0.63–0.76 m/s. All six chosen graphical residual envelopes are negative, including the two approximately self-similar-stratum points. Unknown physical uncertainty and a measurement-quantity mismatch prevent a physical-validation verdict.

## Read and view

- [Measurement-plane viewer](demo/index.html): true-axis y=0 geometry, six actual sampled depths, observed/model comparison bars and complete numerical table. Normalized and nominal m/s displays; no flight or flow animation. Browser rendering has NOT been verified.
- [Scientific report](REPORT.md), [exact executed result](EPOCH2-RESULT.json), [numerical summary](PUBLIC-SUMMARY.json).
- [Source ledger](SOURCE-LEDGER.md), [verified bibliography](literature/references.bib), [literature-to-experiment ledger](literature/LITERATURE-EXPERIMENT-LEDGER.md).
- [Original prospective protocol, public edition](PLAN.md), [preserved first-epoch stop](GATE-STOP.json), [separate exact-decimal amendment](EXACT-DECIMAL-AMENDMENT.md), [public protocol history](PROTOCOL-HISTORY.json).
- [Independent extraction review](review/INDEPENDENT-EXTRACTION-REVIEW.md) and [saved-result review](review/EPOCH2-RESULT-REVIEW.md). These concern science/numerics; they are not a browser-render or public-package review.

## Provenance and limits

Exactly 18 kernel calls were made once after frozen extraction and independent review. EPOCH2-RESULT.json is byte-identical to the executed record: 11,196 bytes, SHA256 eaf189fa69b2b74913c741e6ac58c8e373956d034898807cd803c7f9e702c1fe. No model was run to prepare this viewer/export.

Public editions label removed artwork, changed links and historical framing in EXPORT-MANIFEST.json. The original figure SVG/PNG, selected original XML, operational access/authorization records and host logs are excluded. The source figure remains accessible through the primary article link and is identified by hash. Historical input manifests intentionally reference some omitted originals; this package does not claim an entirely self-contained extraction replay. The historical evaluator's public source-path adjustment changes its hash; its original release does not authorize running that edited copy.

The source is a 2026 PREPRINT, not a verified journal publication. Fixed nominal D=92 mm, r=0, kappa=1.0030572018956476. Graphical envelopes are not confidence intervals. Mean magnitude versus mean axial velocity, experimental errors, symbol placement and nominal-input uncertainty remain unresolved. No coefficient was fitted. The earlier 2025 ratio screen used a different normalization, geometry and nominal mass and cannot establish amplitude agreement here.

## Public layout and resources

Intended destination: research/campaign-velocity-2026-screen/. The viewer imports the existing MIT-licensed Three.js vendor from ../campaign-public-support-factorial/demo/vendor/; no 2 MB vendor duplicate is included. Serve the public repository through HTTP, then open demo/index.html. One event-driven WebGL scene; numerical table/report are the fallback.

This package passed source, numerical-data, privacy and link checks for publication. Static checks are distinct from browser behavior, which remains unverified. The repository commit history records publication status.
