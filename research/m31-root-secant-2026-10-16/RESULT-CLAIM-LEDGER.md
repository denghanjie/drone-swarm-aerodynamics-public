# Saved-root secant: evidence and exact claim limits

Source commit `5a555210fa6012a9df334ecfc4ae0c9a666b0e82`, source-manifest SHA256 `06d8a81dfba014349b48c649d30bf4ed06479632a7a34f4bcd45026b7f49eaf3`. The exact remote source manifest and all24 local/committed pins were verified before the sole candidate invocation. Both candidate and saved-only reviewer are now closed. Frozen sources and raw results are unchanged.

## What was measured

All200 positive refresh endpoints of the exposed16-drone reuse path, including startup and terminal audit. Current nominal motor thrust and current attitude were identical for the held, predicted and saved fresh-root load calculations. The candidate is a fixed causal secant of previously solved roots, with mandatory first-event hold. No current/future root enters prediction; current oracle enters only after a flushed trace. This is a same-state endpoint diagnostic on the old hold-driven path, not a predictor-driven trajectory.

Every endpoint was scored. There were4 invalid finite roots, all drone3/rotor0 at0.31,0.32,0.33,0.34s, with predicted values1.0000050076817075,1.0000280867081577,1.000025529595089,1.0000047468478048. The frozen admissible domain is0<x<=1. No clipping or replacement occurred. Finite invalid-domain load diagnostics are retained in the complete-set maxima; they do not establish an admissible approximation. Zero unscored targets and no nonfinite scientific outputs were reported.

Primary predicted maxima: rotor0.018768458299923737 at event1/t0.01/drone12/rotor0; force0.00993811376408624 at event45/t0.45/drone15; moment0.004127670070010363 at event43/t0.43/drone15. All three exceed0.001. All three are below the corresponding held maxima0.034641310306829855,0.022282031285058564,0.010175726666147102. The resulting scientific decision is `rejected-fixed-secant`.

Full paired event-maximum comparisons are retained: rotor199 lower/1equal/0higher; force196lower/1equal/3higher; moment197lower/1equal/2higher. These are comparisons of event maxima, not a claim that every rotor or vector component improved. Time-correlated points on one exposed deterministic path are not200 independent flight trials; no statistical population claim is made.

The secondary199-target set excludes only mandatory startup and carries no qualification flag. Its predicted rotor maximum is0.016180553419591532 at event45/t0.45/drone15/rotor1; force and moment maxima are unchanged. All three remain above0.001, and all four invalid roots remain. Thus changing or deleting only the first record under the unchanged saved-root history does not repair this diagnostic. A different startup policy in an integrated flight could change later states and was not tested.

Rotor units are mg/4, force units mg, moment units mgR, with m=.027kg, g=9.81m/s², R=sqrt(2)*.028m. Moment is the full roll/pitch correction norm in this model; its aerodynamic yaw correction is zero and nominal yaw is common. These provisional engineering screens are not experimentally justified physical tolerances.

## Integrity and resource observations

Independent reviewer:1,098,131 checks, complete/pass=true, zero failed checks. It reconstructs every new prediction/load/error, inherited identities, invalidity and coverage; it separately recomputes strict primary gates from its own NumPy error arrays. Exact saved argmax/tie reductions use independently validated retained scalar arrays. Geometry and root-solver correctness are inherited from pinned prior audits; no new geometry or root equation was solved. See review/INDEPENDENT-METHOD and results/independent-review.json.

Candidate supervisor elapsed0.6268164999783039s, sampled child RSS108,511,232B over3samples. Reviewer elapsed3.4619541242718697s, sampled child RSS150,454,272B over29samples. Both returncode0, closed/supervisorSuccess=true, child groups absent, zero monitor errors/races/signals. Protected source/input pins and candidate outputs remained unchanged. Scientific result files after both closures:4,285,176B. These are operational observations of instrumented saved-data jobs, not solver timing comparisons or speedup evidence. Final result manifest includes later visualization/report bytes within the separate16MiB package allowance.

## Interpretation, literature and remaining work

The recorded evidence rejects this exact10ms secant candidate for this screen. It supports smaller sampled endpoint maxima relative to holding values, with the domain and coverage qualifications above. It cannot establish intermediate-time accuracy, a predictor-controlled trajectory, current-domain preservation between endpoints, useful adaptive triggers, actual saved solves, performance gains, stability, physical validity or fresh generalization.

Attribution and original-source limits remain in CLAIM-AND-LITERATURE-LEDGER and the closed two-paper desk review. Linear extrapolation and earlier inflow prediction are prior work; this is not a novelty result or a reproduction of Ahmad–Cohen or RESPA. Physical calibration/validation, application tolerances, independent conditions and complete5000-drone cost remain unresolved. No original paper was redistributed and no additional literature retrieval occurred.
