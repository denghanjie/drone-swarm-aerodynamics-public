# A checked path from drone state to one airflow interaction

We connected the previous reliable arithmetic to actual drone geometry: positions, tilts, rotor points and unequal nominal forces. The experiment tested 322 predetermined synthetic cases. All 320 ordinary cases matched an independently implemented checker; two deliberately extreme force cases remained unqualified. No case was removed.

| Recorded outcome | Cases | Meaning |
|---|---:|---|
| Positive interaction with enclosing coefficient ranges |92|The independent reference ranges fit inside the returned ranges.|
| Exactly zero interaction |189|The declared model's exclusion/cutoff branch was verified.|
| Proved rejection |39|Invalid input, unsupported near-field geometry or a cap violation was identified.|
| Unresolved extreme-force case |2|The candidate could not certify a usable result; neither was called zero or admitted.|

There were no unexplained encoding, preparation, branch, containment or journal mismatches. All seven deliberately wrong records were rejected by the same numerical/coverage validator. This includes a positive coefficient falsely replaced with zero, a wrong branch, changed prepared/raw values, and missing, duplicated or reordered cases.

The distinction between verification and full qualification matters. `verificationPassed=true` means the frozen acceptance policy and evidence checks passed. `fullQualification=false` means two queries are still unusable. For a tiny receiver force, both the candidate and fixed-precision reference could not establish a positive normalizer lower bound. For enormous source forces, the reference proves a cap violation, but the candidate only reports its arithmetic range limit. That conservative refusal is preserved.

The adapter's emitted constants and prepared geometry bits matched the independent exact-rounding specification. The model uses those prepared values as exact dyadic operands. This does not prove ideal attitude reconstruction or equivalence to the old native JavaScript aerodynamic computation. The positions/forces are synthetic diagnostic inputs, not flight measurements.

For the 92 positive cases, the widest returned coefficient interval was approximately 3.03e-28 wide; the descriptive maximum relative-width bound was approximately 5.73e-27. These are finite numerical enclosure diagnostics, not physical-model error estimates or a full coupled-load accuracy claim. No accuracy/speed optimization or threshold was selected from these values.

Source was frozen/pushed as 6ed4471c2dc7e920a1a63d16eafb6bdb9616a9da and its exact-commit manifest independently fetched and verified before execution. The sole kernel and checker attempts both closed successfully. Their supervision wall times were approximately 0.55s and 0.53s; these include overhead and are not simulation-performance measurements. Raw results, journal, stage records, source reviews and every correction are retained.

The new Three.js page displays each saved two-drone geometry, axes, selected rotor and status. It also preserves the previous moving 5,000-drone Boids replay, explicitly unchanged and airflow-off. No new flight or browser scientific-kernel execution occurred.

The next meaningful research step is to combine complete rows of these interactions and certify the resulting coupled loads. Then the proposed exact-screening, exact-hierarchy and bounded-omission methods must be compared under the same complete current-state cost boundary. Browser scale, dynamics, physical validation and novelty remain open. This checkpoint is progress on a necessary numerical component; the overall research is not finished.

Here, “320 resolved” includes the 39 correct rejections. Only 281 pair outputs are admitted (92 positive and 189 zero); it does not mean 320 valid flight situations.
