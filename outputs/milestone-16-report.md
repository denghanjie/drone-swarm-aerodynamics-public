# Checkpoint 16 — does stronger cohesion keep everyone together?

Within original research Step 5. Development seeds 801–802; not independent validation.

The primary candidate smooths the flocking and route-steering transitions while retaining the previous joint clearance filter. A second candidate also increases cohesion and slows a drone when its local neighbors fall behind. The latter's normalization was corrected after the checkpoint 15 threshold probe. Neither controller assigns individual paths or slots.

| Seed | Variant | Finished at 5 ms /2.5 ms | Maximum endpoint position difference | Smallest connected group at 5 ms |
|---|---|---|---|---|
|801|Smoothed steering|49 /49|0.00000373 m|49/50|
|802|Smoothed steering|49 /49|0.00000638 m|49/50|
|801|Stronger retention|50 /49|12.1339 m|32/50|
|802|Stronger retention|50 /50|0.002410 m|50/50|

All eight runs reached 60 seconds without a contact-envelope stop. Connectivity is the largest component under a 1.8 m neighbor radius, sampled every 0.1 s; it is distinct from heading alignment. A group can move in the same direction while splitting into separate pieces.

**Decision:** retain smoothed steering as the primary candidate for fresh evaluation. Retention's apparent all-drone completion is not reliable: one development case fails refinement and fragments. Carry it into the fresh comparison as a diagnostic variant, not an accepted solution. One drone remains behind in each smoothed-steering development case, so narrow passage is still incomplete.

This checks agreement of two physics integration steps with the same 10 ms control period. It does not demonstrate controller-rate independence, physical accuracy, safety, aerodynamic fidelity or novelty.

[3D comparison](milestone-16-retention.html) · [Protocol](milestone-16-protocol.json) · [Full runs](milestone-16-study.json) · [Refinement records](milestone-16-comparisons.json) · [Previous diagnosis](milestone-15-report.md)
