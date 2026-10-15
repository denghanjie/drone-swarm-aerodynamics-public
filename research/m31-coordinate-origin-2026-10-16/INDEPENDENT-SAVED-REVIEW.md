# Independent saved-review discrepancy disposition

The sole saved-evidence review finished its full check sequence but failed its
aggregate evidence-integrity gate. Its two recorded discrepancies arise from one
incorrect lifecycle assumption in the checker: the API snapshot after the third
control was checked before the checker modeled the release of the control buffers.
The saved control-C API record is consistent with the frozen browser source.

This is a post-terminal interpretation of saved JSON and source text. It is not a
replacement review, successful review certificate, waiver, numerical recomputation,
or authorization to retry. The checker, launcher, input index, arguments, locks,
report and runtime closure remain unchanged. No raw scientific binary arithmetic,
scientific execution or checker execution was performed for this disposition.

## Immutable terminal result

The report retains `completed: true`, `evidenceIntegrityPass: false`, `fatal: null`
and `scientificQualification.decisionVerified: false`. It lists exactly:

| Failure category | Count | Witness |
|---|---:|---|
| `API-cost-snapshot` | 1 | `controls-C` |
| `API-stage` | 1 | `controls-C` |

The external closure retains `reviewCompleted: true`, `completed: false`,
`evidenceIntegrityPass: false`, exit code 1, one attempt and no retry permission.
The checker elapsed time is 7.278362959 seconds; subprocess time is 7.316123042
seconds; external recorded time is 7.343124625000001 seconds. No timeout or output
cap excess occurred. The child process group was confirmed absent without a kill
signal. Prepared artifacts were unchanged. Its immutable accounting is 68 files
and 682,224 bytes within the 32 MiB ceiling, with a 2 MiB failure reserve.

## Exact discrepancy and source sequence

The source references below are in campaign
`research/m31-coordinate-origin-2026-10-16` at source commit
`ccafbd9b9fd3a3cdd7ffacb5fb360ee5f3dc1abc`.

| Comparison | Checker's expectation for C | Saved C API value |
|---|---|---|
| `costs.liveBufferBytes` | 5,344 | 64 |
| `stage` | `controls-ready` | `controls-complete` |

All other fields of the C API cost snapshot match the checker's constructed
snapshot. The saved API record also has `validation: null`, `loss: null` and
`uncaptured: null`.

The frozen source establishes this order:

1. `source/browser.js:4` declares the control input as 3,200 bytes and control
   output as 2,080 bytes. Lines 38–40 create those buffers and the common 64-byte
   constant buffer. `destroy` at line 10 subtracts the buffer's size from the live
   byte counter before calling its destruction method.
2. `dispatchCoordinate` records the control arm in `seenControls` at line 55.
   Its return expression at line 70 captures a cost snapshot while the 2,080-byte
   readback buffer still exists. The `finally` block at line 71 then destroys that
   readback buffer. The saved `raw/controls-C-readback.json` therefore records
   `liveBufferBytes: 7424`; the live count immediately after that destruction is
   5,344.
3. `finishCoordinateBatch` at lines 73–78 waits for validation, then handles the
   `control-read` stage. At line 76, `seenControls.size === 3` causes it to destroy
   `common.controls` and `common.controlOutputs`, clear their references and set
   `stage = 'controls-complete'`. The return at line 78 takes its API snapshot
   **after** those releases. The remaining live storage is the 64-byte constant
   buffer. The saved `raw/controls-C-api.json` records exactly that stage and count.
4. `source/experiment.cjs:29` awaits `dispatchCoordinate`; line 30 saves its returned
   readback snapshot. Line 31 then calls `finishCoordinateBatch` and saves the
   returned API snapshot. Thus the two JSON snapshots intentionally describe
   different points in the release sequence.
5. The next cell preparation requires `controls-complete` or `idle` and all three
   controls to have been seen (`source/browser.js:45`). Its saved
   `raw/o0-A-buffer-contract.json` is consistent with only the common constant
   buffer being retained before the first cell allocation.

The preserved checker has a different placement for the same release:

- `checker.py:477` subtracts only the temporary readback buffer.
- Line 478 compares the API cost snapshot immediately afterward, so it expects
  5,344 live bytes for C.
- Line 479 maps every control API stage to `controls-ready`, including C.
- Lines 482–483 release the 3,200-byte input and 2,080-byte output only **after**
  all three API snapshots have already been checked.

The A and B API records actually are `controls-ready` with 5,344 live bytes, so the
assumption fits those two records. It fails at the third-control transition.
Releasing the control buffers later in the checker explains why its subsequent
cell snapshots and final cumulative/live resource reconciliations recorded no
additional discrepancies. The checker author's assumption was wrong; these two
witnesses do not identify a contradictory saved source/API sequence.

## Scope retained from the completed failed review

The immutable report records no other integrity failure categories. This statement
describes the report's completed checks; it does not turn the failed aggregate gate
into an overall pass. Those checks included:

- All 250 indexed inputs, including 185 raw files, 53 frozen source pins, their 53
  preserved archives, the freeze, five original science outputs, two separately
  tracked postrun provenance files and four private receipts; raw/result inventory
  and manifest coverage; exact invocation, source and served-byte receipts.
- All 60 literal controls; six saved references with 480,000 rows and 8,640,000
  scalar fields; four GPU term streams with 320,000 rows and 5,760,000 fields; three
  serial streams with 48 total rows. Identity, status, code, mask, reached fields,
  zero placeholders, bounds, exact certificates, term sums and conservative gates
  were checked from saved data.
- Seed/integer provenance, coordinate representation/translation certificates,
  high/low reconstruction, dependent origin copies, usefulness and stimulus flags;
  three saved-reference contrasts and two saved-vector contrasts; typed skips,
  assessor/driver counters, caps, remaining resource snapshots and historical
  process-closure reconciliation.

The immutable numerical findings remain separate from the two checker-integrity
discrepancies: `o1-Q0` has 12 numerical failures and `o1-C-terms` has 12 numerical
failures. The origin-0 reference, term and serial stages retain their recorded
passes. At origin 1, R and Q1 retain their recorded passes, A and B remain skipped
at the Q0 interface gate, and C retains its failed term gate with no serial stage.
All 60 controls retain their recorded passes. Both usefulness assessments and all
four stimulus flags retain their recorded positive outcomes.

The source/result decision remains `candidate: null`, `decision: 'no-candidate'`,
`pass: false`, with A, B and C all unqualified across the paired origins. The
checker compared that decision logic without a corresponding mismatch category,
but its top-level `decisionVerified` remains false because the aggregate review
failed. No candidate, favorable confirmation, physical validation, causal account
of a historical failure, speed claim or deployment qualification follows from this
disposition. Exact saved-term consistency and dependent origin copies have the
limited meaning stated in the frozen review contract.

## Publication qualification

A candid public description is:

> The single saved-evidence review completed but did not earn its aggregate
> evidence-integrity pass. It reported two control-C lifecycle-snapshot mismatches.
> Inspection of the frozen source and saved API JSON shows that the checker
> incorrectly delayed modeling the final control-buffer release; the saved C API
> snapshot follows the source sequence. The original failed review, exit code and
> hashes are preserved, without rerun or waiver. Its other completed comparisons
> recorded no additional integrity mismatches and retained the numerical negatives
> at translated-origin Q0 and C terms. The campaign remains no-candidate; this
> diagnosis supplies no favorable confirmation.

This narrative is outside the immutable executed-review directory and has its own
size/hash for post-review publication accounting. It must be labeled as a later
source/JSON interpretation, rather than inserted into or presented as part of the
original 68-file terminal runtime inventory.

## Identity anchors

| Artifact | Bytes | SHA256 |
|---|---:|---|
| Original checker | 49013 | `82c22b704ca1ace26caa73d636b58375c4f3bbb9bbca77c507f143e3d76b20b6` |
| Original launcher | 10792 | `aafa39073f65ca76d2cbbe7cd996928b957693ac6f6036d34c928f6ce7ada014` |
| Immutable checker report | 8012 | `577272a4cfd22b1e283f2e5cbcea0978561b96c3fbdd3ee876d729083ed63276` |
| Immutable external runtime | 10167 | `581490dbd2a000be0a6917bdd41b295513150e721886801576666e6ca56edce8` |
| Frozen `source/browser.js` | 10286 | `b9bf4622d5d8706d45a5439370406243f3248eaebd7d35939cd011c12a720a5e` |
| Frozen `source/experiment.cjs` | 21736 | `95351d9329221f2299e0a5a292920aefaa4b6a08db2f04c9a74e791b68e75a51` |
| Saved `raw/controls-C-readback.json` | 545 | `caf3c011ba89c7368c853e800d94f858f6af59dcca1515ebe35ec0c707133b9a` |
| Saved `raw/controls-C-api.json` | 417 | `30d06a63484194e2129f2bfe9fd9c601aab26cbc6fe0c4a8555f0dae1b0fcc6f` |
| Saved `raw/o0-A-buffer-contract.json` | 527 | `fef596b255ae3a5173fe9e34ed4636a5ef20e91211a741c5b79be9ad4a767a89` |

The source freeze SHA256 is
`ccfeac8a7b6386f647d00899933757004146f4e01f8b135eaf73389190f9efaa`.
The immutable runtime binds the original input indices, exact arguments,
prepared manifest, report and terminal science result/budget pins. The separate
private receipt contents and absolute input/process paths are not reproduced here.
