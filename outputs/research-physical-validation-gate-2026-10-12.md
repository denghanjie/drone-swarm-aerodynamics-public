# Physical validation gate — 12 October 2026

## Retrieval outcome

The [published dataset DOI](https://doi.org/10.26300/64d4-wa17) redirects to the Brown repository. A direct HTTP retrieval now succeeds, but returns a **human-verification page**, not dataset metadata or observations. The web reader could not access the DOI or DataCite metadata. No challenge was solved or bypassed. No raw data, schema or dataset license was obtained. The saved response is `research-physical-reference-retrieval.txt`; its HTTP 200 status must not be counted as data acquisition.

## What the paper establishes

The [RSS 2025 paper, arXiv version 1](https://arxiv.org/html/2507.09463v1), reports force/torque measurements and PIV, using a tethered 4 V supply and hover PWM; this is not constant rotor speed. It specifies weight≈0.265 N and a 32.5 mm center-to-motor length. At stacked separation 4 lengths, lower-vehicle thrust is reported at 65% of nominal. At separations above 19 lengths it is 95–98%. These are paper-reported observations, not downloaded validation samples. The paper's PIV cut passes through two rotor centers; it is not automatically a center-axis radial cut.

Our model has 27 g mass and motors at(±28,±28)mm, giving 39.6 mm radial arms. Its motor states track commanded thrust directly. Agreement in mass does not establish agreement in geometry, actuation, or inflow response. The newer 32 g/46 mm-arm source has yet another configuration. These three configurations must stay separate.

## Experiment contract before comparing models

1. Acquire versioned observations and reuse terms. Save checksums, units, geometry, coordinate conventions, supply/PWM settings, calibration and repeated-trial identifiers. Keep force/moment and mean-velocity observations distinct.
2. Reproduce the measurement setup in a dedicated vehicle configuration. First predict the measured force under fixed supply/PWM conditions. A flight controller that restores hover thrust would answer a different question.
3. Implement an explicit receiver inflow-to-thrust-and-moment response. The existing far-wake equation predicts mean air velocity; it is not that response law. Do not turn downwash speed into an arbitrary body force and call it validated.
4. Freeze complete held-out separation/configuration groups before fitting. Compare no-interaction, mean-wake plus receiver response, and a richer interaction model. Report errors inN,N·m,m/s with repeat variability, then normalize using documented scales.
5. Validate pair interaction before claiming a superposition rule for several vehicles. A two-vehicle dataset alone cannot validate arbitrary overlapping wakes or turbulent fluctuations.
6. Only then repeat fixed flock missions with airflow enabled and benchmark the actual coupled Boids/physics/wake computation. Keep model error, controller success and execution cost as separate outcomes.

## Current decision

Navigation checkpoints 22–23 remain useful controller experiments with airflow off. They cannot establish aerodynamic accuracy or original scientific novelty. Further controller tuning should not indefinitely replace this measurement gate. Without accessible observations, the next executable physical task is preparation of a clearly labeled measurement-matched receiver model, not a claimed validation result.
