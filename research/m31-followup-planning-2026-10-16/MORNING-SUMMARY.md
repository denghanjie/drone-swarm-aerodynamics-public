# Overnight checkpoint — October 16

**We made progress on finding why evidence was not being saved and on identifying useful physical measurements. We have not demonstrated a validated 5,000-drone simulation or a publishable accuracy–speed result.**

1. **A small engineering test isolated an observed browser boundary.** The browser reported a local-network permission failure while trying to send a 3,840-byte test payload. The receiving server recorded no HTTP request. This is evidence about that one transfer, not proof of the older GPU failure's cause. The unsuccessful attempt, raw public records and independent consistency review are preserved.
2. **A different transfer route is now a concrete proposal.** Playwright supports returning values through its existing automation connection. We checked both official documentation and the installed version's source. The proposal still needs its own bounded trial; it has not been shown to work here or to handle large GPU output efficiently.
3. **Three real measurement resources may help separate the physics questions.** MODERA offers command-to-load data, NanoBench offers flight telemetry, and the air-duct work offers confinement loads. Their licenses and provenance were inspected. Large archives and flight CSV payloads were not downloaded, so their actual data quality remains untested.
4. **We found compatibility details that matter.** NanoBench's instrumented drone weighs 40.85 g rather than our model's 27 g. Motor commands are not force measurements, and repeated file content must be reconciled before deciding which records are independent.

The next useful work is a small transfer test plus a bounded inspection of MODERA's force-file schema. A physically credible wake model still needs suitable measured thrust and spatial airflow, with uncertainty and compatible operating conditions. Numerical agreement alone cannot supply that evidence.

The [visible Three.js checkpoint](http://127.0.0.1:8876/research/m31-transport-diagnostic-2026-10-16/viewer/) displays saved engineering evidence and links the earlier genuine 3D Boids replay. No new coupled swarm flight is implied. [Published experimental checkpoint](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/98880952397aedbc99bdd11794ad6085d883328a).

All detailed records, unsuccessful attempts and restart instructions are retained. The overnight launch window ends at 07:00 Shanghai on October 16. This checkpoint does not promise execution while the environment is suspended.
