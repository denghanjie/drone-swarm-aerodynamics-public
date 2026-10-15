# Claim ledger

| Claim | Evidence | Status and boundary |
|---|---|---|
| Independent static implementations agree for all 12 saved poses | Frozen gates; raw binary/receiver records; saved-data review | Supported for 112,000 rotor and 28,000 vehicle evaluations with prescribed equal nominal motors |
| Body thrust, roll/pitch and world vectors agree numerically | All 13 discrepancy max/RMS summaries independently recovered | Supported for these static inputs; yaw remains nominal zero, not modeled effective rotor drag |
| Ordinary summation is close to compensated summation here | Same contribution stream, Neumaier1974 method | Supported finite observation; no correct-rounding or universal error-bound claim |
| 5,000-drone model reference is physically accurate | No compatible calibrated force/moment dataset used | Unestablished |
| Predicted load losses occurred in the original flights | Historical motors absent; airflow was off in original paths | Unsupported; these are newly prescribed static calculations |
| Earlier 60-second trajectory screens are repaired | No integration here | False; earlier failures remain |
| Efficient approximation, speedup or new method established | No approximation or benchmark here | Unestablished |
| Generic source omission would be novel | Literature review pending separately | Unestablished; numerical source pruning has substantial prior art |

All 12 snapshots were already exposed during development; they are not an independent held-out dataset. Drone count grows with cloud extent, not fixed-volume density. Near-field policy skips omit physical effects of unknown size. The finite 20-degree model tilt domain, isolated-hover source strength, superposition, rotor point samples, missing walls/ground/unsteady wakes and constant ideal induced-power receiver response remain modeling limitations.

The saved-only review verifies hash coverage, record dimensions, arithmetic summaries, residual/power identities, wrench components and classifications. It does not regenerate field geometry or rotate moments independently from quaternions, and does not certify floating-point intervals. See the complete independent memo for precise limits.
