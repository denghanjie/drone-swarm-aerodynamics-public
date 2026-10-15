# Prospective wall-activity replay
Public edition of the prospective plan frozen before the completed replay. Original SHA256 a8d87399a5bc88e92fa3246553313050f2591ba30d064e56d1ca2d6fe0e4583e. Archive paths are replaced by artifact identities; authorization wording is editorially shortened. The scientific selection, parity gates and limits are unchanged.

## Question and fixed evidence
Did listed walls cause corrections in the six early controller passes on saved J32 states? Final wall-repair activity was zero. This new observable cannot retroactively qualify event-stress or establish physical wall aerodynamics.

Input: the archived J32 reference tensor (not distributed in this addendum), 110976 bytes, SHA256 57c41683a78b3b467b64ab00109fb92bb78118dfd7c3ff8e87f03803d24c9298. Shape 51x16x17 little-endian binary64, cadence 512 ticks. Use exactly rows 0..49 at ticks 0..25088: the 50 pre-control states. Exclude terminal row 50; never regenerate/interpolate. Prior summary SHA256 6efb79738c4c05e7eef033cae817ff5da5151ea01bb76d43bb21eb407fcf0d90 stays EVENT_EXPOSURE_INSUFFICIENT.

Pin the original public-source closure (see [source identities](SOURCE-IDENTITIES.json)), SHA256 8bdf344f726d55ab8f1a8c2324e7fe56b3514fa05c8641902d3bdf53f55e7896 and its 15 original source hashes. Reference existing files without copying.

## Matched evaluations
At each state, call original C.controller once and a diagnostic-only instrumented copy once, using separate bit-identical input copies. Completion means 100 swarm-controller calls and 1600 vehicle steering/control calls; zero initializer, wake, load or dynamics calls. No extra model fixtures/retries. Count attempts and returns separately; stop on first failure.

Instrumentation copies diagnostics after original branch arithmetic. Preserve operation order, branches, speed limiting, repair, route, neighbor order and actuator mapping. Review an exact source patch; no new controller rule. Side-channel logging never feeds back; original source bytes remain unchanged.

Compare ALL original returned data after excluding only the added side channel: commands, controls, branch signatures and existing event diagnostics. Compare every number as binary64 bits, including signed zero; other types, keys, array lengths/order and strings exactly. Check input bytes before/after and retain per-state output hashes. Any mismatch or nonfinite diagnostic means IMPLEMENTATION_MISMATCH and prevents scientific interpretation. No tolerance.

## Activity and bounded witnesses
For each of six passes, classify every tested row as wall(obstacle ID) or pair(neighbor ID). Record whether the ORIGINAL radial<lower branch fired, incoming/outgoing three-velocity and the Euclidean norm of their difference. Preserve pass 0..5, tick, vehicle, row index, ID, lower bound and full normal. Normals may have 17 entries with trailing zeros: label actual shapes and identify the first 3 spatial entries.

Per pass/type, aggregate tests, branch fires, correction-norm sum/max, and counts exceeding 1e-12 and 1e-8 m/s. These fixed descriptive thresholds are not physical tolerances. Keep first nonzero wall/pair witnesses and maximum-norm witness per pass/type; ties select earliest tick, vehicle, row. Witnesses include before/after vectors and signed constraint slack. Count speed-limit changes separately. No dense per-row tape; retain all aggregates even when zero.

Only after parity passes: positive wall correction establishes early-pass activity on these states; zero establishes absence in these sampled early passes. Later operations can undo corrections, so this does not establish net trajectory causality. No wall-deleted counterfactual, new event qualification or support-crossing claim.

## Resource limits and stops
One future serial attempt; proposed outer 5 s, CPU 4 s, cooperative 3.5 s require adoption. The subsequent release specified child-only CPU 4 s and whole-process-group outer 5 s. Folder<=50000 bytes including plan/source/reviews/results; outputs<=25000 with 5000 reserved for failure. Check retention headroom before release. Verify identities before imports. Stop on source/hash/parity/resource failure, retaining first witness and counts; no retry. Do not repair the unrelated old failure writer. This historical plan is not a new execution authorization.
