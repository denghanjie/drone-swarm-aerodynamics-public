# Static source review: force/moment ablation

2026-10-16. **No remaining blocking discrepancy found in the inspected candidate/config/protocol.** One conditional-gate ordering issue was identified and corrected before freeze. The separately prepared independent reviewer and final source/reference manifest still require their own completed freeze checks. This review authorizes no execution and reopens no completed allocation.

Read the new package's config, protocol, disposition, adapter, experiment, controls, supervisor and restart/reproduction notes; compared the supervisor with the completed motion-feedback predecessor. Performed parser-only Node `--check` on the three JavaScript files and Python `ast.parse` on the supervisor; all passed using available local runtimes. No scientific source import, controls execution, model evaluation, integration, new input/scenario, external acquisition or repository modification occurred. The review file was written only in the requested temporary directory.

## Intervention and numerical contract

`adapter.cjs` sends each non-off arm's own simultaneous normalized stage state to the same lean builder/ordered solve/residual check. The `force-only` branch creates an applied correction with the modeled world force and torque `[0,0,0]`, while retaining the separately saved modeled correction and solved loads. It first obtains `F.derivative(state,command)` and adds the applied correction afterward. Thus nominal roll/pitch/yaw torque, gyroscopic dynamics and nominal motor lag remain present. No previous-arm state/force history is substituted, and unknown modes reject.

Global RK4 stage inputs, held commands, quaternion projection, endpoint reevaluation and first/planned-terminal step capture retain the prior scheme. Captured steps include actual starts/finals and four saved slopes, modeled/applied corrections and forces. Stage rejection and final-projection failure retain context. Finite inputs/forces/derivatives and the unchanged coupled admission/order/residual gates are checked. Modeled and applied load semantics are documented accurately as a synthetic wrench intervention.

The new body-rate discrepancy is the Euclidean difference of the three saved body-rate components and participates in the same refinement test with0.001rad/s tolerance. The both-errors-small exemption remains explicit. Body-axis contrast is computed separately from full quaternion orientation using axis chord length; recorded stage tilt remains a separate descriptive quantity. No effect magnitude, direction, percentage share or physical-relevance label is used as a validity gate.

## Schedule, references and gate correction

The candidate runs three force-only offset controls, six Boids off/full repeats, then at most three force-only Boids paths. Initialization is cached and copied; controller calls retain the10ms schedule and endpoint observations100ms. The protocol's12-path maximum and40MiB budget match config/source. A complete12-path campaign implies36,400 RK-stage attempt records,207 accepted endpoint arrays and96 captured stage witnesses; these are static schedule counts, not observed results.

Each historical reference is read against its frozen byte length and SHA256. Repeat comparisons require exact JSON equality for sample time, full state, command, solved loads, applied corrections, derivative, coefficient witness and group summary, plus equal sample count and complete paths. The new metadata does not alter the comparison fields. This establishes deterministic agreement with the stored numbers if it passes; it is not independent replication. Runtime/accounting metadata are excluded intentionally.

**Corrected finding:** the first draft computed `forceOnlyMask` only after the conditional three Boids paths. A pair-stage mask failure could therefore have been detected after the dependent launch. The final source defines `maskChecks()`, assigns the first three pair mask records before `primaryPass`, includes them in that gate, and only then enters the conditional arm. It recomputes the mask list afterward for `allocationPass`. The updated lines were reread. Pair endpoint invariants, completion, all first-nine sampled refinement gates and all six reference agreements also precede conditional launch.

After conditional execution, `allocationPass` additionally requires every path complete, every arm's refinement gates, all force-only stage/endpoint masks, and full/force-only initial state/command/load/modeled-correction/coefficient equality with equal applied force and zero force-only applied torque. Incomplete comparisons return null values. A no-effect result can pass; a negative or large mechanism contrast cannot bypass these gates. `complete` denotes recording finished; downstream interpretation must use `allocationPass` and the independent review as well.

## Resource/failure contract and disposition

The supervisor validates committed source bytes against the exact manifest/commit, creates exclusive candidate/review invocation locks and uses fixed300s/120s wall ceilings,768MiB sampled RSS,40MiB scientific-directory aggregate and4MiB log caps. Candidate cooperative guard is280s. Normal candidate writes reserve8MiB and increment accounting only after successful writes. Resource failure writes compact partial analysis first, then the full active trial if it fits, otherwise a compact summary containing the actual failure state and an explicit retention limitation. Supervisor launch/monitor/cleanup failures remain recorded. Sampled monitoring is execution accounting; it does not prove zero transient cap overshoot or constitute a speed benchmark.

The disposition explicitly declines the suggested1cm effect label and percentage-share summaries. Raw pairwise contrasts with observed refinement context satisfy the narrower question and avoid invented physical relevance. It also substitutes independently checked actual Boids states for an additional asymmetric synthetic mask fixture. That is acceptable provided the independent reviewer reports whether recorded data actually exercise unequal nominal rotor states and nonzero angular rates, as the disposition requires. The simple pair control alone would not establish preservation of nonzero nominal torque/gyroscopic terms.

For initial failures with no completed stages, descriptive maxima must remain unavailable/null, never evidence of a zero maximum. Other unsaved stages retain candidate scalar diagnostics only. The separate independent reviewer author reports implementing the same first-three-mask conditional gate and null treatment; this statement is not a completed static or execution audit of that separate reviewer file.

Before dispatch, freeze all executable dependencies, the independent reviewer and six old reference recordings in the source manifest and verify publication. None of those prospective publication checks is replaced by this source report. The fixed seed is exposed; physical validity, additive force/moment attribution, continuous safety, stability, novelty, performance and5,000-drone claims remain unsupported.

## Inspected final pins

Paths are relative to `research/m31-force-ablation-2026-10-16/`. Later changes require review of their delta.

| File | SHA256 |
|---|---|
| `config.json` | `ffa05916d909e1a003ce93ced9b67fc1409124aa142a89b03eb38cec5b061f67` |
| `PROTOCOL.md` | `e2e54a794ba0591c0eac1f0e3d03f90a1fa2230ae699aaecced7fef81cc059f3` |
| `review/DISPOSITION.md` | `73cbaaf8c050d74500342fdc2815acc5108af12be62068b303adc54fb426612f` |
| `source/adapter.cjs` | `3389613bb855361b5ec41768eafee60bc7c9bb85868697cf391d5689eea60469` |
| `source/experiment.cjs` | `fbbf32b677802915ad1a402ad739fd04e99a6b82d65fcc260ab865d0ece98c0d` |
| `source/controls.cjs` | `f0e69bbdda7f85cad295341ac9ffa125265c310eabe3721f6a6454b39506cbff` |
| `source/run.py` | `fad518b405fa42b1de9d8366b0d6a9563d6f336bd4746cb2dfd3630260ce11b0` |
