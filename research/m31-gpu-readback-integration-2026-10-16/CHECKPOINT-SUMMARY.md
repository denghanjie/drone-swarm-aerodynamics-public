# Source checkpoint summary

**What changed:** we prepared a new GPU readback recorder and an independently written saved-file checker. A verified shader-language specification now supports the tiny fixture's expected arithmetic and byte layout. The fixture itself did not change.

**Why it matters:** earlier missing GPU output prevents us from judging the underlying numerical calculations. The new test is intended to show whether actual GPU bytes survive cleanup, transfer and saving. It can resolve this measurement uncertainty only if a future experiment succeeds.

**What was checked now:** 25 host pure cases, 37 independent checker pure/scratch cases, and four Python admission test methods passed. Six Node syntax checks and nine integrated Python parses passed. Independent source review caught and corrected configuration, parsing, file-inventory and deadline issues. No operational code, browser, GPU or complete saved-file review was invoked.

**What remains unresolved:** source checks are not experimental success. Actual GPU readback, realistic transfer cost, accurate coupled dynamics, physical calibration and the 5,000-drone accuracy–computation goal remain unestablished. There is no breakthrough or publication-ready result to claim.

**What is saved:** source, contracts, test receipts, independent review, verified references, claim and literature ledgers, checksums and restart instructions. Earlier experiments and all 30 pins in the previous preparation remain unchanged. The original eight-step framework and historical M31 are preserved.

**What comes next:** finish the remaining operational prerequisites and define a new bounded cycle before execution. Then test the 128-byte GPU transfer once and evaluate the actual saved evidence. Return to force/trajectory verification and measured-data compatibility promptly afterward. See NEXT.md and SOURCE-STATUS.md.

**Visible evidence:** the last completed Three.js view remains the [recorded control-channel engineering result](http://127.0.0.1:8876/research/m31-control-channel-2026-10-16/viewer/). It links historical local 3D Boids behavior. This source preparation supplies no new simulation record to animate.
