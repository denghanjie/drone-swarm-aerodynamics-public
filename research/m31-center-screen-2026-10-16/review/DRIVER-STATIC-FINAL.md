# Final static delta review: center-screen driver, closure and seal

2026-10-16. This supplements `m31-center-screen-driver-static.md`. No scientific module was imported or executed, no fixture/control/state/target was evaluated, and no repository file was edited. Inspection was limited to source text and identities. This reviewer authored the kernel/controls but is independent of the driver/supervisor/seal authors. The separate reviewer-source audit by the other existing agent remains a distinct review.

**Disposition: the previously reported final-serialization blocker is resolved. No remaining launch blocker was found in this delta/interface review.** This does not waive the pending complete source manifest, independent reviewer-source review, publication, remote/local/committed-byte verification, source-HEAD condition or the parent's final launch decision. No numerical qualification is implied.

## Corrected terminal payload checks

In `source/run.py:185–201`, elapsed/final-wall fields are set before the serialization loop. Each iteration encodes the current record, checks that exact payload against both closure reserve and aggregate directory allowance, and either writes those same immutable bytes or first marks the record explicitly unsuccessful and encodes/checks again. A previously exhausted cap can still receive truthful failure evidence, but cannot retain `supervisorSuccess:true`. The unchecked second-payload problem in the earlier hash is gone.

`source/seal.py:111–128` now follows the same pattern. It totals the existing directory, records elapsed time after that accounting, includes the seal lock in its administrative allowance, serializes and checks the exact output bytes, and reserializes after any failure status change. The final stored payload is the payload whose fit was checked. If existing overshoot prevents fitting, the stable failure record remains explicitly unqualified. These are truthful administrative cap outcomes, not hard real-time/no-overshoot guarantees.

The prior runtime-before-import, actual child-group closure, append-only raw timing, schedule coverage and intended-counter findings remain unchanged by this correction. The previously inspected driver remains the reference for those findings.

## Reviewer/seal compatibility

The now-integrated `source/review.py` and `review/REVIEW-DESIGN.md` match the seal's terminal handoff:

- `analysis(audit)` creates `independentAuditPass`, nullable `performanceRulePass`, `practicalRulePass:null` and `requiresReviewSupervisorClosure:true`. An incomplete/failed audit retains unavailable performance instead of manufacturing a false measured performance outcome.
- The output report contains strict Boolean `pass`, separate reviewer `complete` and candidate completion, and the exact `analysis.json` artifact pin. It writes the analysis and report exclusively and leaves the final supervisor gate to the external seal.
- `seal.py:93–104` accepts only Boolean-or-null internal performance, requires reviewer report `pass:true` and `complete:true`, requires analysis `independentAuditPass:true`, and requires a Boolean performance result before evidence can qualify. Both independently checked supervisor closure gates remain necessary.
- Final `practicalRulePass` stays Boolean: unavailable performance makes `performanceRuleAvailable` false, which makes evidence unqualified and short-circuits the final result to false. A completed audit with a false performance Boolean produces the distinct negative practical-rule decision; an incomplete/failed audit remains unqualified evidence.
- Timing review checks the exact 42-call raw/validated schedule, required phase keys including fallback-only `screenPreflight`, and qualified method-specific screen/work metadata. The prospective fallback phase and historical skipped-counter scope match the candidate interface.

The reviewer's top-level NumPy/reference imports are reached only after the authorized supervisor has checked runtime metadata/executable identities and pinned source bytes. The reviewer rechecks its actual NumPy version/distribution metadata and Python identity before controls/fresh numerical reconstruction; it pins the independent reference before importing that reference. This review did not import any of them. The NumPy RECORD hash remains distribution-metadata identity, not a new claim to hash every installed package byte.

The copied `source/numeric-reference.py` hash matches the declared unchanged reference. Its numerical implementation was not re-audited in this delta review; the other existing agent is reviewing the independent checker, and earlier inherited-reference qualification is not reopened here.

One nonblocking documentation nuance was sent to that reviewer: if an F fresh case falls back, `review.py:828–831` uses absent phase value zero in aggregate summaries, including an L `screenPreflight` series. Raw L records correctly omit that phase. Any public display should label that value as absent-phase accounting rather than an observed L preflight duration, consistent with the schema's raw-phase statement. This does not change timing totals or the practical gate.

## Remaining prelaunch gates

The final manifest was still the parent's next preparation step. It must pin the final source/config/runtime/protocol, inherited helpers, reviewer/reference, seal and full imported simulation/scientific dependency closure. The supervisor's critical-name subset is not a substitute for that review. Final source publication/independent byte verification and receipt field compatibility remain required. Preserve Git HEAD at the published source commit for both supervised scientific launches, as required by `run.py`; the administrative receipt must not accidentally advance HEAD before those checks.

No target access, dry run, replacement seed, threshold adjustment or budget extension is recommended. This delta disposition resolves source issues only.

## Reviewed identities

All paths are relative to `research/m31-center-screen-2026-10-16/`.

| File | SHA256 |
|---|---|
| `source/run.py` | `1a61172d84163e56e4ecbbfab37a467e8b424604e35cfe279ab106ad614394b5` |
| `source/seal.py` | `52d74642dfd5186cc09db751cb9f9c8c7059c0305a4fcd85c4b9b7b89b89a159` |
| `source/review.py` | `09660f29649d2e33da4a87d051936f10e612d28bf4001f98380e5a3d79a97279` |
| `source/numeric-reference.py` | `4b21e84674d0007e23641622aec52724bced4791fcca3c1b97d48189c21f6aeb` |
| `review/REVIEW-DESIGN.md` | `1d062b14cdcb1c25c428061b1c80d928b65901da01e8a1cb2aa9b0fcde6a4295` |

Content inspection: revised supervisor tail, complete revised seal, reviewer design note, and targeted reviewer import/runtime/provenance/timing/analysis/output sections. The numeric reference received an identity check only. No result artifact was opened. Subsequent changes require matching final pins and a relevant static delta review.
