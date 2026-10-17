# Milestone: aerodynamic loads now checked throughout a coupled flight calculation

**The numerical qualification passed for the prescribed 64-drone, 0.02-second continuation.** This is a useful prerequisite for scaling, not a breakthrough or a physical validation result.

## What we tested

We connected the aerodynamic load calculation to the existing flight dynamics and local 3D Boids controller. At each intermediate integration stage, we checked that the correct drone received the correct force and moment in the correct coordinates. A matched branch used the same starting state with aerodynamic coupling off. Shared route guidance and the inherited wall-priority controller remain disclosed.

The experiment used one previously exposed starting state at original time 5 seconds. Its 32 stages are dependent parts of one short continuation, not 32 independent trials. The criteria were published before the run in source commit `25cfcee43b02f88a021fe0bae59d07cabf5fc163`.

## What the evidence supports

- All **32 consumed aerodynamic stages** passed the four prescribed error limits against the independent numerical reference, including reference uncertainty.
- The checker verified the force/moment consumption and integration chain for both branches, plus simple motions with known analytical answers.
- **34 drones** had a nonzero aerodynamic load change at the initial stage. Those differences propagated into the flight states; all **64 drones** had changed command words at the second controller update. This demonstrates a feedback path on this case, not a group-level aerodynamic phenomenon or a useful magnitude threshold.
- All 12 wiring controls, three analytical families and ten fixed corrupted-record tests passed their declared checks. The corrupted records were detected; this does not prove that every possible bug would be detected.
- The owned browser closed normally, all stages stayed within their budgets, and the frozen source/input bytes were preserved. There was one scientific attempt and no retry.

The first unprojected intermediate attitude failed the quaternion-norm prerequisite for 63 of 64 drones. The experiment had already specified quaternion normalization at every stage; all projected stages qualified. The raw diagnostic did not attempt full native admission, so it does not establish that a raw alternative would otherwise be admissible.

## What remains open

The aerodynamic model still lacks matched physical validation. This experiment does not establish continuous-time trajectory accuracy, long-duration stability, collision safety, 5,000-drone speed, or novelty. The short replay will show very little motion because only 20 milliseconds were simulated. That is intentional: this checkpoint checks the connection between calculations, rather than producing a long animation.

The next computational question is whether the browser can avoid enumerating distant drone pairs while preserving the accepted load calculation. The existing production full method still visits every pair; an earlier grid method was not automatically faster. A source-reviewed proposal is recorded separately in `review/NEXT-EXPERIMENT.md`; it is not a result of this qualification.

## Inspect and reproduce

- [Recorded Three.js viewer](viewer/index.html): actual endpoints, intermediate stages and consumed force arrows; no simulation runs in this page. Playback is 200× slower and has no invented intermediate motion.
- [Prospective protocol](PROTOCOL.md), [source review](SOURCE-REVIEW.md), [independent checker contract](review/CHECKER.md).
- [Supervisor record](results/run-attempt.json), [browser journal](results/browser-journal.jsonl), [reference index](results/reference.json), [checker result](results/check.json).
- [Saved-evidence review](review/INDEPENDENT-REVIEW.md), [claim ledger](claims.json), [literature ledger](LITERATURE.md), [viewer QA](viewer/QA.md), [restart instructions](RESTART.md).

The roughly 45.62-second supervised duration includes reference generation and auditing and excludes final report writing/process exit from its timestamp. It is **not** a simulation-speed or frame-rate result. Process-lifetime memory observations are not aggregate browser memory or OS containment measurements.
