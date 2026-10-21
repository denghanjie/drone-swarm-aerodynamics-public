# Does switching off coupling change the recorded descent?

21 October 2026. Computational-only milestone. Overall research remains unfinished.

**All four prescribed nominal-load paths reached five seconds.** The previously saved coupled paths for the first starting configuration stopped at about 4.62 seconds; the second configuration reached 5 seconds at both time steps. The new runs retained the same starting states, flocking rules, controller, motor lag, geometry and stopping rules. Only the load selection changed.

For these particular simulated starting conditions, removing the implemented aerodynamic coupling changed the first configuration's stopping outcome. This is a controlled difference inside the simulation. It does not show that actual drones would lose this much thrust, that switching off physics is a practical remedy, or which controller modification would work.

Think of two copies of the same flock following the same rules: one experiences the model's mutual airflow effects, and the other uses nominal rotor loads. Each copy then reacts to its own motion. Their later neighbors and commands are allowed to differ—that is part of the total effect being compared.

| Configuration | Time step | Coupling off | Coupling on (existing record) |
| --- | ---: | --- | --- |
| 2026102001 | 0.005 s | completed at 5.0000 s | stopped at 4.6200 s |
| 2026102001 | 0.0025 s | completed at 5.0000 s | stopped at 4.6175 s |
| 2026102002 | 0.005 s | completed at 5.0000 s | completed at 5.0000 s |
| 2026102002 | 0.0025 s | completed at 5.0000 s | completed at 5.0000 s |

## Compare at the same saved endpoint

The following heights use the last discrete endpoint available in both arms. They do not compare an off endpoint at 5 seconds with a coupled endpoint at 4.62 seconds. The modeled body radius is 0.075 m; height refers to the drone center.

| Configuration | Step | Common nominal time | Drone 17 height, off | Drone 17 height, coupled | Mean-height difference, off minus coupled |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026102001 | 0.005 s | 4.6200 s | 3.136160 m | 0.074745 m | 1.746865 m |
| 2026102001 | 0.0025 s | 4.6175 s | 3.136096 m | 0.074935 m | 1.746210 m |
| 2026102002 | 0.005 s | 5.0000 s | 3.676985 m | 1.733773 m | 1.816600 m |
| 2026102002 | 0.0025 s | 5.0000 s | 3.676985 m | 1.733773 m | 1.816600 m |

Exact recorded timestamps, center separations, mean vertical displacements and terminal velocities are retained in the audit report. The coupled intermediate velocity is absent from the older replay export, so the comparison does not invent a velocity difference. After a coupled path stops, its missing suffix stays missing.

## What was verified

The independent checker verified 6,000 new completed steps, 24,000 nominal-load stages and 1,536,000 full derivative rows. All four original 64 × 17-word initial states and reached segment boundaries matched. Zero native aerodynamic queries and zero coupled reruns occurred. These are implementation checks, not independent flight experiments.

The independent Python audit reconstructed every consumed nominal load, quaternion projection, motor-lag/rigid-body derivative and projected-RK endpoint from saved evidence. It checked all journal identities, schedules, command bindings, safety-record linkage, comparisons and export. It did not regenerate the Boids/controller or contact geometry; those source implementations and previous baseline audits remain reused trust.

The two time steps are resolution checks on each exposed configuration, not four independent trials. Off coarse/fine sensitivity:

- Seed 2026102001: maximum common-endpoint center difference 6.99333122e-08 m.
- Seed 2026102002: maximum common-endpoint center difference 4.91581138e-08 m.

Small resolution differences do not establish physical accuracy or a rigorous trajectory error bound. These seeds were chosen in the earlier admission study and this diagnostic was motivated by already observed outcomes. It is not held-out confirmation or a population reliability estimate.

## Visible evidence and next question

The [Three.js comparison](viewer/) shows both saved flocks side by side, highlights drone 17, draws its path and the floor, and displays actual saved times. A pane becomes empty beyond its own last endpoint. Both arm buffers, missing suffixes, controls, camera reset, corrupted-evidence refusal and desktop/mobile rendering passed the sole display allocation. Other factory obstacles are omitted; the wire halo is a visibility aid.

The next useful question is whether a separately specified change to vertical tracking can prevent this coupled-model failure while retaining the aerodynamic loads. First inspect earlier controller/force-ablation work to avoid repeating it. Such a follow-up needs a new bounded, independently reviewed and publicly frozen protocol; no controller tuning or additional flight run is authorized by this completed allocation. Removing coupling is a diagnostic, not a proposed physical fix.

Earlier N16 off/full/force-only and short N64 current-adapter comparisons already exist. [Historical check](HISTORICAL-CHECK.md) and [literature scope](LITERATURE.md) preserve that context. No new flocking method, research novelty, physical airflow validation, real-flight safety, speedup or scalability claim is made.

[Independent audit](audit/audit.json) · [Result claims](RESULT-CLAIMS.md) · [Protocol](PROTOCOL.md) · [Audit contract](AUDIT-CONTRACT.md) · [Closure](ALLOCATION-CLOSURE.json) · [Restart](RESTART-RESULT.md). All raw records remain under results/ in ordered lossless parts. Final public identity is recorded separately in publication-receipts after verification.
