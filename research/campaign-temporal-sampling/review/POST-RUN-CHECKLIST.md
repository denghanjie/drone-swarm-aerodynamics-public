# Independent post-run review checklist

Prepared 2026-10-13T12:17:03Z before the single supervised campaign. This checklist requires saved-record inspection only. Do not launch a simulation, aerodynamic replay, new numerical reconstruction, alternative seed/cadence, or timing measurement after the original budget expires. The campaign's built-in reconstruction must supply the numerical reproducibility evidence inside that budget. Source/hash inspection and reading saved outputs afterward do not restart it.

## 1. Establish the authoritative outcome first

- Read results/execution-validity.json and results/supervisor.json before any numerical qualification table. Missing, false or interrupted execution validity overrides earlier complete/qualified labels.
- Read results/campaign.json plus every file in results/failures/. Distinguish reference-not-established, hard numerical/model-domain stop, resource stop, compatibility failure, and completed screened campaign.
- Check the final supervisor start/deadline identity against its retained initial lease. Confirm no restart, second campaign window, overlapping numerical worker or standalone evaluation occurred. Check per-job identities, monotonic deadline handling and finalization corrections, including any post-interruption cleanup records.
- Treat the exact frozen plan/configuration/source hashes as the experiment identity. Verify source freeze happened after the retained final synthetic checks and before compatibility/fresh cases. Note separately which synthetic attempt covered which source snapshot.

## 2. Check the compatibility preflight

- Seed 4301, N16, T=1 s, physics 16 ticks (2.5 ms), airflow 64 ticks (10 ms), unchanged lean source.
- Exactly 400 completed physics steps, 100 airflow updates, 100 controller updates, no stop, final tick 6400, final held tick 6336.
- Final full-state/held-inflow SHA256 equals fabdd3452577cfdc3cb948ecd12b90c93fc74ee8673129a9737ca2d3e1265ef7.
- On failure, preserve the attempted result and reject all fresh results; no undocumented retry.

## 3. Verify executed matrix and gate ordering

- Fresh seeds are exactly 840131 and 840137; count 16, duration 1 s, control 64 ticks, no seed substitution.
- First stage: physics steps 4,2,1 ticks at airflow 4 ticks for each seed. Inspect both seeds' four-metric physics gate rows separately.
- Physics finest caps: position 1e-4 m, velocity 1e-4 m/s, attitude 1e-4 rad, body angular velocity 1e-3 rad/s. Finest must also be <= max(coarser, floor), with floors 1e-8,1e-8,1e-7,1e-7 in those units.
- Only after both physics gates pass: airflow 8 and 16 ticks at physics 1 tick for each seed. Airflow finest caps: 1e-3 m, 1e-3 m/s, 1e-3 rad, 1e-2 rad/s. Finest must also be <= max(0.6*coarser, floor).
- Only after both airflow gates pass: airflow 32 and 64 ticks at physics 1 tick for each seed.
- Expected maximum completed run counts including compatibility: 7 if physics gates fail, 11 if airflow gates fail, 15 if the full matrix runs. Earlier hard stops may yield fewer; never mistake them for a matched complete comparison.
- Every completed fresh run has 100 controller updates, 6400/physicsStepTicks integration steps, 6400/airflowTicks field updates, and final held tick 6400-airflowTicks. No terminal refresh.
- Review saved all-cadence coupled comparisons and descriptive four-metric screens separately from reference qualification and fixed-path load qualification. Preserve nonmonotone comparisons and all seeds/cadences.

## 4. Inspect physical/numerical validity and failures

- Every used driver is complete, full17 states at all 6401 dense endpoints, with valid endpoint quaternions and nonnegative nominal rotor thrusts. Retained field arrays have shape [6401,16,4], distinct from production held inflows.
- Dense instantaneous field evaluation includes T and every point between production refreshes. Any rejection invalidates the driver; do not skip, clamp or substitute a zero field.
- Failure evidence must identify run, phase, exact tick/time, full affected swarm state, prior held timestamp, attempted field inputs and source guard/error. A watchdog's last checkpoint is older evidence, not an exact stopped state.
- Reference-screen failure permits only conditional replay of already-complete valid drivers. Reference qualification and cadence qualification remain false. A hard safety/domain/nonfinite/checksum/resource failure permits no later numerical job.
- Distinguish endpoint obstacle clearance from swept-linear pair clearance. Neither proves continuous curved-path clearance or safe flight.

## 5. Inspect replay and quadrature evidence

- Each hold cadence uses the same saved row-3 driver and current full state; differences arise only from ages of four already-projected scalar inflows. Current endpoint nominal thrust and attitude are used for loads; nominal yaw remains unchanged.
- Read one-sided worst indices and trace descriptions. Terminal and refresh left limits must remain represented, including hold age equal to h at the final left endpoint. No terminal zero reset may replace them.
- Force impulses are world vectors; torque error impulses integrate world-rotated body [roll,pitch,0]. Reference world torque includes nominal yaw; reference torque peak uses body roll/pitch.
- Per cadence and seed, quadrature must pass reference and error vector-prefix differences at every common coarse tick, plus accumulated error-norm prefix differences <=1e-4 after fixed-scale normalization. Sampled force/roll-pitch torque peak differences must be <=1e-3. Inspect actual differences and offending tick/drone, not only passed flags.
- All six load screens must pass separately: peak force and torque <=0.01; maximum per-drone prefix force and world-torque impulse norms <=0.001; force and torque error-norm integrals <=0.001. No swarm-wide signed cancellation is an accuracy metric.
- On failed quadrature, retain observed values but report classification unresolved. Both seeds' reference and quadrature gates are required before a cadence can be screen-qualified.
- Review absolute units, per-drone RMS/prefix maxima, rotor inflow errors, contribution counts and complete 10 ms display-bin traces. Saved maxima are sampled endpoints/one-sided limits, not continuous-time suprema.

## 6. Check excitation and scope of interpretation

- Read all four raw excitation measures and their frozen labels: loaded fraction <0.05; normalized rotor temporal range <1e-3; force wake amplitude <1e-3; torque wake amplitude <1e-4. Overall field-low is loaded fraction OR temporal range low; force/torque low labels remain separate.
- A numerical threshold pass on low-excitation cases stays visible but cannot support a general cadence recommendation. Do not tune disturbances, remove a seed, loosen screens, or replace a failed driver.
- If fixed-path loads pass but coupled state screens do not, describe feedback sensitivity or insufficient load-screen strength as possible explanations; do not assert chaos, physical inaccuracy or physical safety.
- Distinguish projected arm a, radial arm sqrt(2)*a, and opposite-motor distance 2*sqrt(2)*a. This study does not rehabilitate the withdrawn figure comparison or validate the implemented length normalization.

## 7. Retention, resource and reconstruction checks

- Both compressed and uncompressed hashes, shape, ordering, tick spacing and run identity must be present for raw arrays. Inspect artifact existence and sidecar identities; rely on the already supervised numerical reconstruction rather than rerunning it.
- Read results/recomputed/verification.json and reference-gates.json. Reconstruction must have completed inside the same lease and match all retained original gate rows exactly. A failed reconstruction blocks completion/qualification.
- All retained campaign artifacts count toward 150,000,000 logical uncompressed bytes, including compressed duplicates, copied sources, logs and reports. Normal writes reserve 2,000,000 bytes for failure evidence. Unknown accounting is a failure, not proof of staying within the cap.
- The 300-second lease includes compatibility, all fresh cases, replay, numerical reconstruction, checksums and serialization; each job remains <=45 seconds. Inspect explicit stop/finalization records before accepting resource compliance. Post-kill emergency logging is cleanup only and cannot create a qualified result.
- Viewer/report labels must honor execution validity as well as scientific gates. Do not publish a stale qualification from an interrupted run.

## Review deliverable

Return a concise verdict: qualified bounded numerical screen, reference not established, quadrature unresolved, or exact blocker. List actual work completed, the controlling failed/passed gates, excitation limitations, resource outcome and retained evidence paths. State explicitly that the frozen model remains physically unvalidated. Preserve every failed/stopped attempt and do not imply independent aerodynamic/physical validation from a reconstruction that shares the frozen equations.
