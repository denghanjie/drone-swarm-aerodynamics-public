# Remembering which drones are far apart

The new rule passed a limited test: it proposed excluding **273,280 of 7,741,440 directed pair checks (3.53%)**, with **zero incorrect exclusions in the tested saved states**. An independently written audit checked all records and the arithmetic used to build the exclusion lists.

Imagine keeping a short note: “These two drones are far enough apart that this part of our model will ignore their interaction.” We allow each drone a small box to move inside. While the drones remain in their boxes, we reuse that note. If a drone leaves, the rule must rebuild the note. This checkpoint asks whether the notes were correct in our existing recordings.

We used all **1,920 saved stages of a 64-drone swarm**, grouped into twelve clips, plus ten deliberately chosen checks of the rule's boundaries and bookkeeping. In the saved clips the rule built twelve lists and reused them 1,908 times. No sampled stage triggered a box-exit rebuild; the separate fixed controls exercised leaving a box, changed identities/counts and falling back to keeping all pairs. These controls are limited examples, not complete coverage.

The underlying model already rejects many distant pairs after calculating their distance. The proposed rule would let us know some of those answers earlier. Crucially, **this test still calculated every baseline distance needed for validation**. The 273,280 figure therefore describes potential exclusions, not operations actually saved or a measured speedup. The cost of constructing and checking the notes may outweigh their benefit. The earlier performance test remains a failure; this checkpoint does not reverse it.

There are three different levels of evidence. First, we have a mathematical argument that works under explicitly stated arithmetic assumptions. Second, the recorded test found no incorrect proposed exclusions. Third, we have **not proved that every execution path of the installed runtime meets those assumptions**. Passing this finite test cannot fill that gap or establish correctness on every possible swarm arrangement.

No new flight, force calculation or physical experiment was performed. The 3D view replays earlier recorded positions with the new exclusion counts and list-reuse annotations. It preserves the earlier trial the model refused because drones were too close; that refusal has not been solved by this distance rule.

The next useful research step is to design a separately reviewed integration study: preserve the model's accepted/refused decisions and scientific outputs, keep real work counters visible, and measure the complete cost of using the rule. Resolve the arithmetic-contract question before claiming general correctness. If the complete cost does not improve, retire this optimization rather than treating fewer proposed checks as success.

The original display test passed every saved position and annotation check but failed at the camera-drag assertion. Its evidence is preserved. A separately reviewed and publicly frozen display-only recovery passed all checks, including camera controls, desktop/mobile rendering and altered-evidence rejection. Both screenshots were visually inspected; the first failed attempt remains preserved. Research remains computational-only and unfinished. No physical accuracy, flight safety, novelty or large-swarm speed claim is established.

Evidence: [raw summary](results/summary.json), [independent audit](audit/audit.json), [fixed protocol](EXECUTION-PROTOCOL.md), [claim ledger](RESULT-CLAIMS.md), [verified sources and limitations](LITERATURE.md), [Three.js replay](viewer/).
