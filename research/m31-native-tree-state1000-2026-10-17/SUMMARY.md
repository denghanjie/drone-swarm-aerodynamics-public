# A complete 1,000-drone state passed its planned checks

**We now have a fully saved and checked aerodynamic calculation for one new state containing 1,000 drones.** This closes the previous evidence-storage obstacle for this particular test. It advances numerical correctness and scale; it does not yet establish faster simulation, sustained flight or physical accuracy.

[Open the actual-record Three.js view](result-viewer/). Every displayed drone comes from the new saved state. Select a receiver to see which other drones the tree retained and which groups it excluded. This is a single instant at t=0, with no motion interpolation.

## What we did

We initialized one fixed, previously planned seed and applied the unchanged local Boids controller once. Three methods then calculated the same aerodynamic interaction: the full method F, a tree with exclusions disabled H0, and a tree with conservative exclusions H. H's delivered forces were used in the motion derivative—the instantaneous rate at which each drone's state would change. No integration step followed.

The independently written checker compared all three scientific outputs, verified the omission evidence for every receiver, and checked all 17,000 primary derivative values. All 12 wiring controls and 14 arithmetic fixtures passed. A separate saved-result review checked source identities, evidence completeness, accounting and interpretation without repeating the scientific calculation.

## What happened

| Observation | Result |
| --- | ---: |
| Drones / checked projected states | 1,000 / 1 |
| Required journal records retained | 22 / 22 |
| Full directed candidate pairs | 999,000 |
| Tree candidates retained | 627,164 |
| Tree candidates omitted | 371,836 (37.22%) |
| Complete native outputs agree | Yes, for all three methods |
| Primary motion derivative values checked | 17,000 / 17,000 |
| Unique saved evidence | 4,204,482 bytes |
| Evidence without sharing repeated chunks | 7,045,914 bytes |

The full attempt completed within its six-minute limit, with about 12.36 seconds reported before the final ledger write; external supervisor exit 0 was separately observed. The new browser calculation, independent checker and retained-prerequisite metadata stage all completed. Private logs were empty. The earlier 5,000-drone browser failure is preserved and has not become a successful flight.

## The speed result needs care

The single recorded query times were F **62.9 ms**, H0 **141.4 ms** and H **114.6 ms**, in that fixed order. H skipped many candidate pairs but took longer than F in this observation. These times include native query/capture work and exclude separately recorded evidence processing. They are neither browser frame times nor a controlled speed benchmark. Persistence time overlaps transfer time and must not be added twice.

The supported conclusion is that the tested exclusions preserved the native calculation on this state. A speedup has not been demonstrated. The result gives a reason to examine the cost of tree construction/traversal and evidence capture before promoting the method for faster simulation.

## What remains open

The three methods share numerical/model components. Their agreement does not replace a fresh high-precision reference at 1,000 drones, which was not run. The checker binds saved controller inputs/commands and selected target arithmetic, but does not independently reconstruct the full Boids neighbor search or controller law. One derivative is not an integrated trajectory, sustained flock behavior, collision safety or a 5,000-drone simulation. No measured aerodynamic validation or publication-level novelty follows.

The next scientific decision should be a separately preregistered comparison of complete computation cost with an explicit correctness bridge, or a bounded coupled continuation if trajectory correctness is the priority. It must preserve the present negative speed observation and all evidence overheads. Neither experiment is automatically allocated by this successful single attempt.

[Claim ledger](CLAIMS.md) · [Executed allocation](EXECUTION-PROTOCOL.md) · [Raw result/check](results/check.json) · [Independent evidence review](review/RESULT-EVIDENCE-REVIEW.md) · [Protocol/accounting review](review/RESULT-PROTOCOL-REVIEW.md) · [Precise restart](RESTART-RESULT.md)
