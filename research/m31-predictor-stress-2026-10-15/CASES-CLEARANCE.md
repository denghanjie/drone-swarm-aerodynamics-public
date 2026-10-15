# Predictor stress cases: independent static clearance

Reviewed `research/m31-predictor-stress-2026-10-15/source/cases.cjs`, `config.json`, `PROTOCOL.md`, and `DESIGN-REVIEW.md` before execution. The repository design memo is byte-for-byte identical to `/tmp/m31-predictor-design-review.md`.

**No implementation blocker found in the case definitions.**

- All six case IDs, ordering, positions and analytic translational velocities match the memo. In the stacked case S1 is fixed, while S2 and S3 move at their specified fixed heights.
- Source pitch is `(pi/12)*sin(4*pi*t)` with xyzw quaternion `[0,sin(theta/2),0,cos(theta/2)]` and body angular velocity `[0,(pi^2/3)*cos(4*pi*t),0]`. These are consistent derivatives and remain within 15 degrees.
- Receiver roll is `(pi/18)*sin(4*pi*t)` with xyzw quaternion `[sin(beta/2),0,0,cos(beta/2)]` and body angular velocity `[(2*pi^2/9)*cos(4*pi*t),0,0]`. These are consistent derivatives and remain within 10 degrees. Other orientations/angular velocities are identity/zero.
- State layout and all motor-state thrusts match the intended 17-component state and constant `mg/4` contract.
- At the frozen 0.25 ms tick, startup windows `[0,20]` and `[20,40]` represent 0–5 and 5–10 ms. Reversal centers 1000/2000/3000 represent 0.25/0.50/0.75 s; +/-40 ticks correctly gives +/-10 ms. Window-boundary treatment in the driver is outside this case-definition review.
- The all-pair domain proof remains applicable: every center separation is at least 0.4 m in the analytic definitions, whereas a near-wake exception would require center separation below 0.29 m after allowing the rotor arm radius. Rotation preserves rotor-arm length. The proof covers every ordered pair, tilted receiver rotors and source-source interactions. All tilts remain strictly within the model's 20-degree limit.
- The protocol correctly identifies the stored thrust/torques as body-frame quantities and states that held/predicted scalar inflow already contains its refresh-pose receiver-axis projection.

One documentation correction was reported separately: the protocol's Inputs paragraph says “a moving receiver with three moving sources.” The actual intended case has **three sources, two moving**, as both memo and implementation specify. Correct that wording before freeze; do not change the case to match the typo.

This clearance covers static agreement and analytic domain reasoning only. It does not establish oracle agreement, predictor accuracy, timing, physical validity, or complete driver correctness. No case function, solver, field evaluator, candidate trajectory or timing loop was executed, and no repository file was edited by this reviewer.
