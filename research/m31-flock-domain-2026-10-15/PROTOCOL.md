# Prospective M31 flock-domain coverage audit

This is a new, bounded **geometry-only** analysis of retained, already exposed M31 flock poses. It follows six prescribed two-to-four-vehicle airflow tests, whose successes do not establish applicability to the large flock. The question is whether the unchanged M28 field's stated input restrictions cover the saved primary M31 configurations. No aerodynamic field or load calculation, integrator, new trajectory, controller, Boids or speed benchmark is allowed in this campaign.

## Fixed inputs and scope

Use the committed compact pose export from checkpoint07e5165fa56f2f23bab24562b278dda1c82ed05e: `research/m31-restart-2026-10-15/viewer/data.json` and `snapshots.bin`. Freeze expected metadata/binary hashes and byte length in config; validate both against those pinned values before decoding, independently of the hash contained in metadata. The binary contains Float64LE [position3,quaternionxyzw4] poses. Freeze primary variantIndex0 only, for wide1000seed2001, narrow1000seed2002 and wide5000seed2001, at exact saved times0,20,30,60s. Twelve snapshots,28,000 vehicle poses. The earlier suggestion of40s is replaced prospectively with the available30s record; never interpolate40s. Original large pose streams are referenced by hashes but need not be restored. Freeze the exact metadata offsets and provenance in the independent design review.

These are existing airflow-off local3D-Boids flights with map guidance. They are development evidence, not fresh held-out flights or acceptable trajectory references. The earlier same-drone time-step discrepancies remain failed. The compact export has no complete active/arrived mask. Treat **every saved vehicle** as a potential receiver and source, without reconstructing eligibility from positions. Do not claim the audit matches an operational active-drone subset. No velocity, motor-state or force values are invented.

Quaternions remain exactly as stored; never normalize or correct them silently. Nonfinite input stops the audit. Report norm defect per vehicle; mark the unit-quaternion assumption unresolved if abs(norm−1)>1e-10. The model's tilt criterion is axisZ<cos20°, after rotating body+z with the original quaternion. It is not max(|Euler roll|,|Euler pitch|). Compare the two implementations’ tilt predicates exactly as well as their numeric axes; a threshold disagreement fails the implementation check. All tilt violations are counted even though original M28 fields would throw on the first one.

## Pair classification

The production-style checker uses unchanged M26 Grid with1.5m cells and strict3m center radius, original physics double-cross rotation and M28 constants/branch order. The independent implementation imports none of those modules and uses explicit matrix rotation plus an all-source loop for every receiver. Both classify every receiver-rotor/source pair into an indexed byte code; self/outside-center entries remain zero. Compare exact code vectors, counts and ordered near-event identities for each receiver. Assert vector length4N, independent nonself centerChecks=N−1 per receiver and107,972,000 total at completion. Split code0 into4N self entries per snapshot and outside-center entries. Compare independent axes, rotor world points and all near-event coordinates to absolute1e-12 SI tolerance. Any disagreement stops the entire invocation with the first offending snapshot/receiver/source/rotor and its poses. Do not waive a mismatch as rounding after seeing it.

Codes follow the exact geometry predicates:

0. Self or source center outside strict3m radius.
1. Downstream coordinate d≤0.
2. d≥2.5m cutoff.
3. 0<d<2.5D and radial distance r<0.15m: **unmodeled near-wake exception**.
4. 0<d<2.5D and r≥0.15m: skipped by the existing near-field policy.
5. d≥2.5D but r≥3H(d): outside radial support.
6. Inside retained far-field geometry but receiver/source axis projection≤0.
7. Inside retained far-field geometry with positive axis projection.

D=2sqrt(2)×0.028m; H(d)=0.07668(d+5.817D). The geometry code performs no wake speed, receiver root or force calculation. Model finite cutoffs, near-field skip policy, rotor-point sampling and overlap assumptions remain implementation choices; classify them, do not validate them physically.

For tilt-invalid snapshots, pair classification continues **only as a diagnostic geometric census**. Original M28 would reject that full input before reaching the pair loop. Do not label code7 as a valid computed force, or label code4 as validated far-field behavior. Report per-receiver and per-snapshot counts, all tilt IDs, all near-invalid source/receiver/rotor events with geometry, all near-skipped identities through complete compressed code vectors, and source/receiver involvement separately. Several rotors and directions can refer to the same physical pair; code counts are not numbers of distinct collisions.

Report closest inspected predicate-boundary gap, its label, receiver/source/rotor and sign. The diagnostic covers eligible-center pairs and the predicates actually reached; it is not a global distance to every excluded boundary. Each gap uses the predicate's native units (metres for distances, dimensionless for projection); a common1e-10 numerical proximity flag is descriptive, not an uncertainty estimate or proof of classification robustness. Exact equality at a boundary is retained with its strict/non-strict branch rule.

A saved snapshot passes this **implemented-input-domain screen** only if it has no tilt violation, no near-wake exception and no unit-quaternion assumption violation. This is a finite saved-time condition, not a continuous flight claim, safety certificate, physical validation or numerical-reference acceptance. Do not evaluate aerodynamic loads afterward under this protocol even if all snapshots pass. Any later field comparison requires its own source freeze and precise eligibility/scope.

## Evidence and budget

One invocation,300 executable seconds,64MiB combined raw evidence with1MiB reserved for failure details. At most110,000,000 independent nonself center-pair checks and864,000,000 combined rotor classifications. Exact planned independent center checks are4×(1000×999+1000×999+5000×4999)=107,972,000. Eligible pairs receive four rotor classifications in each implementation; worst-case863,776,000 combined. Grid cost is not equated to direct-loop work and no timing ratio is a research result. Zero aerodynamic-field calls and zero integration steps by construction.

A cooperative guard and external supervisor stop the invocation on time/count/storage cap. Save every completed receiver row, per-row code hashes from both implementations, complete indexed primary code vectors compressed with zlib deflate/base64, full geometry for all code3 exceptions, summary/input hashes and budget ledger. Every code3/4 identity is recovered from the complete vector index4*source+rotor; only code4 geometry numbers are omitted from storage. Runtime compares all code3/4 coordinates from both implementations before writing the row. Independent saved-data review can inflate the exact vectors and check hashes/counts/identities without recomputing geometry. Reserve failure storage; set snapshot/offset context before decode, and structured production/independent event/count/tilt context before comparisons. Record first mismatch/current input before stopping. Hard external termination guarantees only already-written evidence. No rerun, extra snapshot, tolerance expansion or source patch after outcome. A completed model-domain failure is a finding and does not abort the census; implementation disagreements or resource caps do abort.

Obtain independent static source/protocol scrutiny, freeze/push all scientific files and input hashes before execution. Then independently verify saved arithmetic/event aggregation without reexecuting geometry, update a visible Three.js flock view using exact saved poses, record claims/limitations, privacy-review, commit/push and independently verify the manifest. No paid resources, data acquisition, author contact or submission. Stop new overnight launches at07:00Asia/Shanghai2026-10-16. Preserve all earlier campaigns and later main/DOT work.

Physics sources remain the [verified aerodynamic ledger](../m31-restart-2026-10-15/literature/annotated-ledger.md); current [physical-target limitations](../m31-predictor-stress-2026-10-15/physical-target-followup.md) explain why this domain check cannot establish experimental agreement. The audit adds a scoped input-coverage measurement; no novel method is assumed.
