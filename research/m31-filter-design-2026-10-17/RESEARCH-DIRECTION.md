# Why this test, and what would make us change direction

The original goal remains a browser simulation of 5000 interacting drones, with genuine local 3D Boids, flight dynamics, and mutual aerodynamic effects. The recent static timing checkpoint is a prerequisite result, not a substitute for that goal.

This candidate avoids computing an interaction exactly only when a cheap interval proves that the same model returns exactly zero. It sacrifices neither a positive wake term nor the declared error tolerances; it may sacrifice time on uncertain cases because both the filter and the exact calculation run. Its first weakness to expose is a wrong zero near a boundary. Its second is overhead: a correct filter can still make the complete calculation slower.

The next evidence sequence is deliberately short:

1. Verify finite primitive enclosures and branch preservation on a fresh fixed set of ordinary, boundary, tilted, invalid and extreme raw inputs. Require independent checks and corruption controls. Report fallback coverage, with no timing claim.
2. If that gate passes, test the unchanged candidate on a new matched total-cost suite, including its preparation and fallback overhead. Include a filter-off ablation under identical hierarchy and load solving. Do not retune the first verification or the closed six-scene timing set.
3. If total costs improve meaningfully, restore the moving-swarm integration as the next performance boundary. Measure steering, dynamics, interaction calculation and rendering separately; include transfer/synchronization if GPU work is used. Preserve closed baselines and real 3D group behavior.

Do not add successive optimizations merely because a local count improves. A false zero rejects this candidate for its claimed scope. Missing required witnesses or an oracle failure leaves the gate unqualified. A correct but slower candidate is a negative computational finding; consider exact shared-work reuse or batching, then assess a fresh design. Four repeated times alone will not justify a broad statistical performance claim.

Published filtering methods make this an adaptation of prior numerical practice. A zero filter by itself is not an established novel contribution. The project would need a more specific accuracy-cost result, fair comparisons to the closest published approaches, fresh confirmation, failure boundaries, and a credible explanation of applicability to drone swarms before a publication claim. Physical-model validity still requires compatible independent experimental evidence; numerical agreement cannot supply it.
