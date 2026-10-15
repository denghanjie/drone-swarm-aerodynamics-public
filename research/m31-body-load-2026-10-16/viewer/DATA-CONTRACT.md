# Saved body-load viewer contract

At source preparation, this scaffold had not been bound, served or browser-tested. The current `viewer-artifact.json` states its binding status; later browser QA requires its own record. It is intended for `research/m31-body-load-2026-10-16/viewer/`. Its Three.js imports resolve to the repository's existing `outputs/step02b-source/vendor/` modules. No network dependency is installed or downloaded.

## Separate claims

1. **Byte binding:** a selected file matches a pinned byte count and SHA-256. The offline binder verifies every entry of the terminal result's immutable `files` list, including full policy arrays, using a streaming hash. The browser verifies reports and small files it fetches. It does not download policy arrays.
2. **Recorded execution:** `result.status`, `result.qualified`, each case disposition, and saved assessment reports retain their exact values. The viewer never recomputes gates or upgrades qualification.
3. **Independent review:** pinned JSON review artifacts remain visible even when failed, pending or unmapped. Their status/detail are read via explicit JSON pointers. No review artifact means pending and review-unqualified. An offline binding receipt is not a review.

The deployment's `viewer-artifact.json` is the trust anchor. Hash checks demonstrate internal byte consistency, not authenticity of a server or independent scientific correctness. Publish its hash with the final evidence record. There is deliberately no browser control for ignoring mismatches.

## Binding API (deferred)

`build-bindings.cjs` exports `async buildBindings(request, destination)`. Importing it is inert. The CLI takes a pinned-request JSON path and a destination viewer directory. Do not execute it before source publication and later authorization. It never imports campaign science, compiles shaders, evaluates geometry, profiles or roots, or generates inputs.

The request shape is:

```text
{
  schema: "m31-body-binding-request/1",
  campaignDir: <absolute campaign directory>,
  result: {path: "results/result.json", bytes: <actual>, sha256: <actual>},
  externalReports: [
    {label: "Execution closure", artifact: {path: "results/budget.json", bytes: <actual>, sha256: <actual>}}
  ],
  reviews: [
    {label: <actual review name>,
     artifact: {path: <confirmed review JSON path>, bytes: <actual>, sha256: <actual>},
     statusPointer: <actual JSON pointer>, detailPointer: <optional JSON pointer>}
  ]
}
```

All pins come from actual saved artifacts, never invented examples. The result must be terminal. The confirmed supervisor closure is `results/budget.json`; review paths/schema remain explicit inputs until the sole reviewer finishes. The result copy `results/result.json` has the same bytes as `raw/result.json`, which is not itself listed in `result.files`. A missing status pointer shows “No mapped status”; it does not imply a pass. Unspecified reviews are an empty list. The report cap is 16 MiB per browser-fetched file; the reserved raw cap is 805,306,368 bytes.

The builder verifies first, copies selected bytes into a temporary directory, hashes the copies, then installs `evidence/` and a bound `viewer-artifact.json`. It refuses to replace an existing bound artifact or evidence directory. If installation fails after the evidence directory moves, correct the destination explicitly before retrying; it does not silently replace existing evidence. The exact result file is copied as `campaign-result.json`; reviews and external reports use deterministic local aliases. The raw manifest names are retained for binaries. Paths are contained within the campaign directory and raw filenames must be flat safe names.

Public result/review/closure and selected JSON bytes are copied exactly. Before copying, the binder rejects JSON containing absolute local-system paths or private localhost evidence-sink URLs. It never redacts a pinned result or changes its scientific/review meaning. If that check fails, resolve it through a separately documented public report and explicit new pins before binding. The private binding request and absolute campaign directory are never emitted into public artifacts. `PUBLIC-SOURCE-LEDGER.json` records source packaging transformations separately from evidence byte binding.

## Browser fetch and record layout

At startup: bound terminal result, every pinned review, optional external reports, and the saved control assessment. On selection: only that family's original states, R output and GPU output; or the saved pair-control records. Switching family drops previous buffers. No full N² policy file is included among fetched assets. Policy entries remain in the offline receipt with their byte counts and hashes.

All binary reads use little-endian `DataView`. No binary is converted through JSON. Scalar values retain raw hex bits, saved validity flags, signed zero and nonfinite values in the inspector. Missing/invalid values display unavailable; they are not coerced to zero.

| File | Exact record layout | Display use |
|---|---|---|
| family-ID-originalStates.f64 | N × 17 × 8 bytes | position 0–2, quaternion xyzw 6–9 |
| family-ID-R-output.bin | N × 480 bytes | header 32 bytes; four 96-byte roots; eight f64 body values at byte 416 |
| family-ID-gpu-output.u32 | N × 256 bytes | header 32 bytes; four 48-byte roots; eight f32 body values at byte 224 |
| controls-pairs-original.f64 | 15 × 16 × 8 bytes | receiver position 0–2, receiver axis 3–5, source position 6–8, source axis 9–11, offset 12–14 |
| controls-pairs-gpu-output.u32 | 15 × 256 bytes | header; symbol word 8; term/down/radial/projection/center words 9–13; validity word 14 |
| controls-reference-pairs.json | saved R and Q arrays | exact saved term/policy values and validity |
| controls-reference-status.json | saved reference status and counters | exact recorded R/Q reference completion/status, not independent review |
| control-metadata.json | saved pair/root metadata | expected symbols and counts |

R roots: ten f64 fields `Uordinary,Ucompensated,nominal,vi,alpha,x,force,lower,upper,residual`; u32 status/iterations/flagsValidity/positiveTerms at offsets 80/84/88/92. Low ten validity bits map directly to the ten doubles. GPU roots: eight f32 fields `Uraw,nominalRaw,vi,coefficient,x,force,shaderResidual,signedLastUpdate`; meta/validity/positiveTerms/pad at words 8–11. Body validity uses header bits 3 and 4. R/GPU header identity mismatches are explicitly shown and do not generate comparison colors.

Q, H, root-control buffers, partial buffers, and full policy arrays remain preserved in the complete receipt; they are not all decoded by this focused viewer. Saved campaign/control reports carry their recorded assessment results. In particular, drawing a pair control does not imply that all 146 root controls succeeded.

## Display rules

- Four planned families are always listed, with planned N = 50, 500, 5000, 5000. Missing families say not executed; partial files remain distinguished from no evidence.
- Family 3 is the default if it has selectable saved files, otherwise the first available family, then actual saved pair controls. There are no generated sample values or poses.
- Saved vehicle positions/quaternions produce enlarged display glyphs only. Invalid/nonfinite drawable transforms are hidden, without creating replacement positions. Camera transforms do not change saved data. No wake mesh, trajectory, integration, or flight animation exists.
- Pair controls use saved point positions/axes/offset, without invented quaternions. Cyan marks the receiver; white marks the source; orange shows the saved offset.
- A control-only terminal stop with no GPU file defaults to **fixed pair inputs**, not a main family. The header states “Saved control inputs. No GPU observation.” The scene and inspector label the original saved geometry as expected fixed control/input; the table shows R/Q reference diagnostics and “GPU · not observed”. No GPU column is populated from a reference or an expected symbol. No field-to-body result is implied.
- Selecting an unexecuted main family produces one explicit empty state in each result table. It creates no synthetic receiver, rotor/root values or body-load records. Saved R/Q root-control buffers remain in the receipt; they are not decoded or used to fill missing GPU/H roots.
- **Force-error color:** per-receiver maximum absolute saved GPU minus saved R rotor force, only for valid query identities and four available force values.
- **Lift-reduction color:** `1 − GPU effective T / GPU nominal T`, only for available valid-query body values and nonzero nominal T. This is a display ratio, never a feasibility gate. Negative values are retained; the family-local color range is reported.
- Colors range from blue (lower) to orange (higher); gray means unavailable. A failed independent review does not hide byte-consistent records. A hash/length/layout mismatch disables the data view.

## Deferred verification

No binding, actual binary decoding, browser launch, visual QA, screenshot or science run occurred during the source-only stage. `QA-PLAN.md` lists the later checks. Parser/static checks alone do not establish numerical or browser correctness. The historical M31 link resolves to a separate saved 3D Boids replay whose page states that airflow was off; it is not evidence for this checkpoint's unexecuted field-to-body comparison.
