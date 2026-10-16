# Source checkpoint: one calculation per drone, reused safely

We identified a small, testable optimization: source strength and receiver-rotor normalization repeat across many pair calculations. The draft keeps successful results only within one complete method call, using the same arithmetic and checks. Three independent desk reviews support this narrowly defined design under its closed-call ownership assumptions.

Nothing here measures speed or adds a new flight. Ordinary memoization is not a novelty claim. The current certified implementation still admits at most180drones; the5000-drone objective and physical validation remain unresolved.

A separate ablation is being prepared on two fresh64-drone Boids flights. It must preserve complete results, pass independent checks and meet a fixed complete-cost threshold. Its source must be publicly verified before any run. The latest completed3D evidence remains the validator qualification replay at ../m31-validator-qualification-2026-10-17/viewer/.
