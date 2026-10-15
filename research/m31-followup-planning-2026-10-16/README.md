# M31 follow-up: what we can test next

This is supporting desk work after the [published transport checkpoint](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/98880952397aedbc99bdd11794ad6085d883328a). It contains no new drone simulation, transport trial, model fit or benchmark. All earlier experimental outcomes and closed budgets remain unchanged.

**We have two practical next directions: repair the evidence-transfer path with a small engineering test, and inspect a promising physical dataset before using it to judge our model. Neither direction has yet produced a validated result.**

The completed synthetic experiment found a browser-reported local-network permission boundary before the local HTTP handler was entered. That explains the failure observed in that particular trial; it does not establish the cause of the older GPU failure. Its [Three.js view](http://127.0.0.1:8876/research/m31-transport-diagnostic-2026-10-16/viewer/) is an evidence diagram, clearly labeled as such, and links the historical local 3D Boids replay with airflow disabled. The viewer and its backing records remain unchanged and hash-bound to the published result.

## What the literature/data review adds

| Candidate | What it could help answer | What it cannot yet establish |
|---|---|---|
| MODERA / UPV | How four motor commands relate to measured forces and moments | A calibrated wake field; internal archive schema and uncertainty remain unchecked |
| NanoBench | Actuator, battery and flight-telemetry questions | Independent measured thrust or spatial airflow; its instrumented mass is 40.85 g, versus our assumed 27 g |
| Air-duct measurements | How confinement changes aerodynamic loads | Free-air behavior of our smaller nanoquad or swarm interactions |

The [compatibility matrix](datasets/COMPATIBILITY-MATRIX.md) links the verified sources, versions and licenses. These candidates offer complementary partial evidence. None currently meets the joint thrust-and-spatial-flow requirements; that is not a claim that suitable data do not exist.

An independent metadata audit found 107 CSV filenames but 87 distinct CSV blob IDs in NanoBench's specified data directory. Equal content must be reconciled before choosing repetitions or evaluation splits. This does not establish how many independent flights were acquired. The [audit](m31-nanobench-independent-metadata-review.md) and [coordinator reproduction](metadata-verification.json) preserve the scope of that finding.

## Read or reproduce

- [Plain-language overnight summary](MORNING-SUMMARY.md)
- [Next decision and restart limits](NEXT-DECISION.md)
- [Claim–evidence ledger](claims.json)
- [Literature–experiment ledger](literature-experiment-ledger.json)
- [Machine-readable bibliography](bibliography.json)
- [Control-channel API rationale](CONTROL-CHANNEL-API.md)
- [Privacy and publication scope](PRIVACY-REVIEW.md)

From this directory, `python3 verify-metadata.py` checks the saved public projections and four small text-file bindings. It reads no CSV payloads and runs no external repository code, numerical model or historical campaign reviewer. `manifest.json` binds this static package's bytes; it is an integrity inventory, not a scientific source freeze or launch allocation.
