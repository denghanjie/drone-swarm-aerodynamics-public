# Runtime replication saved-data contract

Status: source-only and unbound. No source freeze/result/review identities have been invented. All actual pins will be supplied after terminal execution and external closure/review. Do not invoke the binder, execute the adapter or open this page for QA until separately authorized.

## Future binding request

`build-bindings.cjs` is inert on import and exports `buildBindings(request,destination)`. The CLI accepts a private JSON request path and this replication's `viewer` directory. It refuses a prior bound artifact or existing evidence directory. Required request fields:

| Field | Meaning |
|---|---|
| schema | `m31-runtime-body-binding-request/1` |
| campaignDir | Operator-supplied local replication directory; never published |
| expectedSourceCommit | Actual published 40-character source commit |
| freeze | Actual `{path,bytes,sha256}` of the source freeze |
| result | Actual `{path,bytes,sha256}` of the terminal scientific result |
| reviews | Pinned records with label, role, statusPointer and optional detailPointer |
| externalReports | Pinned execution closure and other reports, each with label and artifact |

Each review has an `artifact` pin. Exactly one review must have `role: final-external-observation`; its statusPointer must point to the actual final observed integrity boolean, and detailPointer should preserve its scope. Other review records use `saved-review-report`. Candidate/completion records must not be designated final authority. The selected external boolean is not scientific qualification, which comes from the terminal scientific result. Actual report identities and mappings remain pending.

The binder verifies source freeze and result pins, requires the terminal result's sourceCommit to match, and checks the raw started record's source/freeze identities when present. It hashes every listed raw file and copies selected bytes exactly. No private local path or private evidence endpoint is permitted in selected public JSON; failure stops binding rather than redacting pinned evidence. The result, source freeze and reports use deterministic local aliases. The bound viewer artifact is the deployment trust anchor; its final hash must be recorded separately.

A source-freeze hash identifies the frozen contract. Fetching that manifest in the browser does not independently reverify every source file. Published source identity and external observation retain their separate authorities.

## Family records

All fields below are selected only when saved and exactly the expected layout. Every binary uses little-endian DataView, retaining raw scalar hex bits, signed zero and masks. No values pass through a JSON binary conversion.

| Record | Shape | Display |
|---|---|---|
| originalStates.f64 | N × 17 × 8 bytes | original position 0–2 and quaternion xyzw 6–9 |
| R-output.bin, Q-output.bin | N × 480 bytes | header32, four root96, eight body f64 at416 |
| gpu-output.u32 | N × 256 bytes | header32, four root48, eight body f32 at224 |
| H-output.bin | N × 288 bytes | header32 and four root64; **no body payload** |
| assessment.json / stimulus.json | saved JSON | exact completion, pass, integrity, counters and bounded failures |
| generator-audit.json / admission.json | saved JSON | recorded construction/admission metadata; no geometry regeneration |
| R/Q/H-status.json, gpu-api.json, disposition.json | saved JSON | actual path and API status |

Prefixes are `family-ID-`. R/Q/H exact-sized `-partial-output.bin` and their partial status JSON may substitute when canonical outputs are absent; names remain unchanged. A partial assessment's metadata may be shown as its recorded assessment, with the enclosing source JSON preserved in the family reports. Files with other partial names or truncated lengths remain receipt-only. Masked or identity-mismatched values are unavailable, never zero-filled. Unwritten headers remain visible in the record inspector.

R/Q root fields are ten f64 values: Uordinary, Ucompensated, nominal, vi, alpha, x, force, lower, upper, residual; u32 status/iterations/flagsValidity/positiveTerms at80/84/88/92. Low10 validity bits map to those doubles.

GPU root fields are eight f32 values: Uraw, nominalRaw, vi, coefficient, x, force, shaderResidual, signedLastUpdate. Meta/validity/positiveTerms/pad are words8–11. Header body flags3/4 gate effective/nominal body payloads.

H root fields are seven f64 values: vi, alpha, x, force, lower, upper, residual. Iterations is u32 at56; meta at60 encodes status bits0–3, termination bits4–6, validity bits8–14 and productZero bit15. H uses the actual GPU operands but does not duplicate its inflow/nominal fields. No H body or missing operand is reconstructed.

## Fixed controls

Pair count15: original positions/axes/offset use original16 f64 rows; pair GPU output uses256 bytes each with symbol at32, five f32 values at36–52 and validity at56. Pair R/Q values are exact saved JSON. Metadata supplies expected symbols, separately labeled as expected inputs.

Scalar count146: original nominal/inflow use two f64 values; R/Q root records use96 bytes each; GPU uses256-byte controls with a root at32 and header N=1; H uses64-byte roots. The scalar view has no invented scene or body output. Recognized full-layout reference/handoff partial files retain their saved values and masks. When pair references are embedded in a saved partial-status metadata object, that actual object is displayed without recomputation.

## Gate and geometry semantics

Only saved assessment decisions are gates. Per-row failures are shown only when a matching saved failure sample exists. A completed assessment with pass true may be labeled “Passed · complete saved assessment.” Otherwise, missing samples say “No individual pass recorded,” because failure lists are capped at64. No threshold test, polynomial, root, policy reconstruction, body composition or exposure calculation is run by the viewer.

Displayed differences and local color ratios are presentation arithmetic only. Force-error colors use saved valid GPU−R rotor values; lift-reduction colors use saved GPU effective/nominal T. Missing or invalid data is gray. Colors cannot qualify a family or review.

All saved family poses are selectable by receiver input or scene click. World positions and xyzw attitudes remain unchanged; RGB coordinate axes at world zero are display guides. Glyph enlargement and camera fitting affect only display. No trajectory, Boids step, world-force rotation, field mesh or interpolation is provided.

## Limits and later verification

Browser-selected files are capped at16 MiB each; full raw manifest accounting is capped at805,306,368 bytes. No N² policy is copied to browser assets. Family switching releases old buffers/scenes and aborts obsolete requests. A failed length, hash or layout check disables the view, with no bypass.

Actual saved-file decoding, numeric display agreement, full receiver/control interactions, responsive screenshots, corruption/recovery and final authority mapping await terminal evidence and authorized browser QA. Source checks cannot establish those outcomes.

## Actual terminal stop now known

The saved result is terminal failed / qualified false. The first pair dispatch was submitted; no GPU binary was persisted. Source adaptation adds optional `executionEvidence` descriptors for the saved pair dispatch API, browser failure snapshot, capability, runtime before/after inventory and host-control results. These descriptors must match the same terminal raw manifest and each fetched JSON receives the same SHA/length check. They are observation records, not a new dispatch or diagnosis.

The pair API's `dispatch.submitted`, `dispatch.completed`, count and after-costs supply the submission display. The terminal result's output reservation supplies started/complete persistence fields. The saved `TypeError: Failed to fetch` is quoted without attributing a cause. No missing binary is fabricated from expected output length, constants, CPU references, a browser failure snapshot or a dispatch-submitted flag.

The final external saved-review authority is still pending. The pinned scientific capture observation and closure may be external execution reports, but may not be silently mapped as final saved-review integrity authority. The artifact remains unbound until those actual identities and authorization arrive.
