# Bounded physical-data admission audit

Prospective data-quality audit, 17 October 2026. This follows the published fresh numerical checkpoint `e42134d6184df2aa1fe7d1d11f919e57192c3cf3`. It does not fit, train or score an aerodynamic model and does not construct physical force labels.

## Question and prior exposure

Can the two complete small/small random-walk flight pairs in the fixed Neural-Swarm collection be admitted as candidate evidence for a later physical comparison? File availability alone is insufficient. Inspect all four files, without selecting favorable times. The first CF50/04 file has previously been inspected only for identity, header and line count; the other three have not been downloaded. Source-code reading before this protocol already revealed conflicting time-unit documentation, per-file time origin removal, a 32g small-vehicle mass in training code, PWM/voltage calibration and a first-order thrust lag. These are disclosed design inputs, not new confirmatory discoveries.

The four immutable data blobs are enumerated in `audit.py`, from data tree `6c1e0bcfbc55e5739307accbb68b6985adb11510`, directory `training/datacollection19_12_11_2019/random_walk_small_small`. Acquire CF50/04 by verified local copy and retrieve CF51/04, CF50/05 and CF51/05 once each over verified HTTPS. Keep complete source CSVs private. Verify Git blob identity and exact byte size before parsing. No third-party scripts, weights, binaries or serialized objects may be executed or loaded.

## Fixed measurements

Use an independently written standard-library parser. For each full file, report row/column counts, finite-value counts, strictly increasing time, interval minimum/median/maximum, duration under both header milliseconds and preprocessing microseconds, all-row quaternion norm range, PWM range, battery range, acceleration component ranges and firmware-force ranges. Do not label firmware-force fields measured external forces.

For both fixed candidate time scales, report root mean squared disagreement between interval position differences divided by elapsed time and the average logged endpoint velocity. Use every positive-time interval and all three coordinates; do not trim, interpolate, filter, tune a delay or select moving frames. This is an internal consistency diagnostic, not independent velocity/time calibration. Report both outcomes even if one looks clearly preferable.

For each named pair, report raw start-time difference, intersection length under both time scales, individual elapsed durations and overlap after independently subtracting first timestamps. Coinciding or overlapping clocks do not prove physical synchronization. No lag fitting, cross-correlation, trajectory association, separation calculation or inferred neighbor force is allocated.

## Decision and stopping rules

Structural eligibility requires the advertised 30-column schema, at least two rows, all finite fields, strictly increasing timestamps, PWM within [0,1] and quaternion norm error at most 0.01. These are file-integrity screening thresholds, not physical-accuracy tolerances. Report violations without fixing or dropping them. Matching schema and plausible units permit only continued provenance work. Physical-model scoring remains blocked until clock alignment, acceleration frame/gravity convention, actual mass, applicable calibration/lag uncertainty, relevant environments and reuse terms are resolved. No success claim may be based on the calibration training score. These exposed flights are development/admission data, never untouched confirmatory evaluation data.

The source review must link findings to immutable blobs and distinguish what code does from what the physical flight actually did. Any mass/time mismatch is an unresolved provenance discrepancy, not evidence that the authors' published result is wrong. No source/data copyright/license conclusion follows from public availability. Publish only our code, summaries and immutable source identities; retain third-party full source and CSVs privately.

Exactly one audit attempt after this source is committed and pushed; no automatic retries or replacement files. Launch before 03:00UTC 17 October 2026, finish or fail within 600 seconds via self alarm, with 30-second per-request timeouts and 7MiB response limits. Audit private output cap 32MiB, public outputs 1MiB. No browser launch, scientific simulation, heavy benchmark, fit or parameter search. Preserve started/failed outcomes. Verify the 547-pin fresh-result manifest before and after the attempt. Resource caps apply to this allocation, not the entire historical research checkout; no memory-cap enforcement is claimed.

Save aggregate outcomes, independent source challenge, plain-language interpretation and precise restart. Update the visible research navigation to the already reviewed fresh-flock replay and clearly identify its synthetic, airflow-off scope. The admission audit supplies no new flight simulation or real-measurement 3D reconstruction.
