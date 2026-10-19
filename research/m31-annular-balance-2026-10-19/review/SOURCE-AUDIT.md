# Independent annular diagnostic source review

19 October 2026. Preparation and static inspection only. The evaluator, supervisor, protocol and independently authored saved-result auditor were read as source text. Python 3.12.14 parsed the three Python sources with `ast.parse`; no module was imported, no function or control was executed, and neither fixed comparison payload nor upstream metadata counts were inspected. Existing scientific packages remain unchanged.

**Static disposition:** the reviewed implementation is suitable for the prospective single evaluator and single independent audit after the separate protocol challenge, immutable public source freeze, exact-public retrieval and execution gates. This is source acceptance, not a successful numerical result or permission to bypass those gates. The independent auditor itself still requires the challenger's static review.

## Source identities reviewed

| Source | Bytes | SHA-256 |
|---|---:|---|
| `source/evaluate.py` | 12,812 | `317a6fb5e69a01d50bf4391ea0a3b686ff786acace6d00799370ea3b05671fee` |
| `source/audit.py` | 31,175 | `997e94c6d6fb9acac74bcb6bcc52ae093361e85a57daf7e9dedc60c913677571` |
| `source/supervise.py` | 1,715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |

These identities were read from source bytes, not from executing the files. Any later edit requires a new identity and static reconciliation before the freeze.

## Evidence and admission

The only scientific inputs are the pinned paired-support comparison (3,793,293 bytes, SHA-256 `b253b7199df24e8a2d5ff3000bed1f73937cd898ada8449256c91f0172962be3`) and the original saved airflow comparison (1,112,834 bytes, SHA-256 `dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3`). They supply already exposed retained stride-four samples. The reviewer has not inspected their values or metadata gates in this preparation.

The producer checks the copied nested original records against the original airflow cases with recursive type and binary64-word equality. It uses all nested original X/Z/u/v values for the six coordinate-only windows, ignoring predecessor core-inclusion and pairing flags. The auditor independently verifies those original records against both fixed inputs and exactly preserves originalCases, fullFieldSubsets and upstreamCounts, including float sign bits, keys, list order, integers, booleans and nulls.

Window membership is fixed by side, |X| in [1,3] and Z in [12,16), [16,20), [20,24]. The auditor independently uses Decimal coordinates for these integer-bound comparisons and packed binary64 words for exact grid identities. No tolerance, rounding, response-based rejection, mirror pairing, interpolation or changed model domain is applied.

All six windows must have at least five distinct nodes on both axes, unique cells and a full tensor product, with finite components at every selected node. The upstream nonfinite-coordinate and missing-u counts must both be zero; this gate addresses support losses that a tensor census of retained values alone cannot reveal. This is deliberately a gate on inherited saved support, not proof of complete raw PIV coverage.

The producer and auditor save/check selected and unique coordinate counts, expected tensor size, exact missing count, duplicate/nonfinite original indices and one first missing-coordinate preview ordered by increasing Z then |X|. They do not expand a potentially large missing tensor product. nodeIndices is empty when the product is incomplete or duplicated; a unique complete product is retained even if it separately fails the minimum-level or component gate. The original-index membership ledger and six region traces retain every case's selection reason.

Admission failure is a terminal, auditable outcome: status `admission-failed`, empty projectedNodes, and six null full/coarse/coarseMinusFull records. The auditor rebuilds the failed predicate and trace, then takes a branch that calls no projection or quadrature function. It does not evaluate favorable windows independently, retry, shrink, repair or replace support. Malformed input, wrong pins, failed controls, execution failure and deadline/output failures do not become admitted evidence; the auditor refuses them.

## Independent numerical construction after admission

For Y=1, the producer uses R=sqrt(X²+1) and Vr=R*v/X with signed X. Both sides are ordered by increasing |X|, so the left side is not accidentally integrated in decreasing R. The outward face signs are inner negative, outer positive, top/smaller-Z negative and bottom/larger-Z positive.

The auditor independently computes Decimal60 R and Vr from immutable original values. Its radial integrand is the algebraically equivalent `(X²+1)*v/X`; its axial integrand is `R*u`. This avoids using the producer's rounded projected values as the numerical reference. It implements native-R and native-Z trapezoids through nodal weights (half the adjacent interval lengths), independently of the producer's segment sum. It checks every projected node, original copied component, face-node identity, integrand, oriented face integral, coordinate and index list, total defect, absolute-face scale, signed/absolute fraction and coarse-minus-full difference with the declared absolute numerical tolerance 2e-12. Exact structure, membership, copied words and null branches do not receive that tolerance.

The denominator is the sum of absolute values of the four **integrated** signed face terms. The auditor checks that exact zero/nonzero classification against both its reconstructed terms and the saved face terms. Four zero integrated faces require null fractions; this can occur through within-face cancellation and does not assert zero airflow. No integrated absolute nodal-flux alternative is substituted.

The coarse selector independently takes even zero-based positions plus the last position on each axis. Thus full and coarse calculations share the same boundary endpoints. Difference orientation is always coarse minus full, including signed fractions, with null when either fraction is undefined. All six regions are reported, with no pooled score or numerical acceptance threshold.

## Fixed controls and execution mechanics

The source contains twelve fixed control outcomes: both-side irregular-grid divergence-free fields with individual analytic face checks and total balance; reflected projection/orientation; a known nonzero source integral; common positive and negative scaling of a mixed axial/radial field, checking every face and scale/fractions; constant axial flow; zero-integrated-face null fractions; coarse endpoint retention; and missing-node, duplicate-node, nonfinite-component and insufficient-axis rejection. The audit checks the exact saved twelve-item receipt under the frozen producer and successful supervisor, rather than running another control allocation. No control has been run during this source review.

The evaluator/auditor have permanent exclusive locks and separate failure files. The external supervisor starts a new child process session, monitors wall time and cumulative results/UI output, reserves 16 KiB for closure, and stops only that child session on a limit breach. The scientific cap is 60 seconds and 16 MiB cumulatively monitored output; it is not an OS memory limit or an assurance against transient output overshoot between polls. The auditor verifies the evaluator's successful receipt and byte count, and verifies both predecessors' evaluator/auditor receipts. It rechecks all source pins and retained evidence before writing its exclusive report. No old scientific code is imported or executed; no model, fit, calibration or gain is evaluated.

## Required source-manifest pins

The new manifest must include at least these six current-package files:

- `PROTOCOL.md`
- `source/evaluate.py`
- `source/audit.py`
- `source/supervise.py`
- `review/SOURCE-AUDIT.md`
- `review/PROTOCOL-REVIEW.md`

For **each** of `research/m31-airflow-test-2026-10-19/` and `research/m31-lateral-symmetry-2026-10-19/`, it must include all nine predecessor files:

- `PROTOCOL.md`
- `source-manifest.json`
- `source-publication.json`
- `result-manifest.json`
- `results/comparison.json`
- `results/execution.json`
- `results/evaluate-supervisor.json`
- `results/audit.json`
- `results/audit-supervisor.json`

It must additionally include `research/publication-receipts/m31-airflow-result-2026-10-19.json` and `research/publication-receipts/m31-lateral-symmetry-result-2026-10-19.json`. These are 26 mandatory entries; presentation, literature and other reviewed source files may add more. The current source manifest and its later publication receipt are bound by the public freeze gate, not self-listed recursively. The auditor checks original input size/hash, predecessor source/result manifests, source and public-result receipts, execution result hash, successful independent audit result pin and both predecessor supervisor receipts. This reuses established provenance helpers without rerunning any predecessor.

## Scientific boundary

The annular boundary calculation excludes the unseen core by using two measured radial boundaries under the declared reconstruction. It still assumes axisymmetry and no mean swirl; it does not measure a three-dimensional annulus. Left/right are separate conditional reconstructions of one exposed experiment, not independent trials. A nonzero defect cannot identify which flow assumption, sampling effect or measurement/preprocessing issue caused it; a small defect cannot validate the unseen core, global continuity, momentum, wake model, receiving forces or swarm behavior. The common nominal Ui convention is documented, while actual component preprocessing remains unverified. Coarse differences are descriptive sampling sensitivity, not uncertainty bounds or convergence evidence.
