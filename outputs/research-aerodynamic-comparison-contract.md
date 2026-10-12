# Aerodynamic comparison contract — next research block

The active goal requests explicitly labeled approximations. It permits an exploratory sensitivity comparison before independent measurements are accessible. This is distinct from the physical-validation gate in the earlier plan: only validation claims require that gate to pass. The gate is not silently waived, and simulated agreement will not be called physical accuracy.

## Keep the questions separate

1. How do assumed aerodynamic loads change navigation, contact, connectivity and control effort on the same mission?
2. How much computation does each approximation add?
3. Does either approximation predict independent measured forces, moments and wake velocities under matched experimental conditions?

The first two questions are executable simulation studies. The third still needs measurement and geometry/actuation matching.

## Candidate comparison to freeze before execution

Use airflow-off as the regression baseline. A quasi-steady mean-wake field can supply rotor inflow; an explicitly assumed constant ideal induced-power response can translate inflow into reduced effective rotor thrust. Compare total-force-only and rotor-resolved force-plus-moment variants under the same field, then separately test an alternative rule for combining overlapping wakes. Do not imply that a velocity profile alone supplies a thrust response or validates superposition.

Keep source strength, receiver response, multiple-wake combination, spatial truncation, near-field treatment, tilt/motion assumptions and coupling cadence explicit. Check dimensions, zero-flow regression, symmetry, force/moment accounting, monotonic response and numerical refinement before whole-flock trials. Preserve model-domain exits as distinct from body-envelope contacts. Avoid silently filling an unmodeled near field with a clipped far-field value.

The existing vehicle stays 27 g with motors at (±28,±28) mm. An independently measured vehicle gets a separate configuration, not silently substituted dimensions. Free-air hover wake equations extended to moving vehicles inside a factory omit wall interaction, wake transport history and turbulent fluctuations. Comparisons are sensitivity evidence until those approximations are tested.

## Independent-source check, 12 October 2026

The [RSS 2025 study](https://arxiv.org/html/2507.09463v1) was rechecked. It uses fixed supply/PWM, not fixed rotational speed. Its force section reports 65% *remaining* thrust for a close stacked case, while the conclusion uses conflicting reduction wording. Resolve that ambiguity against the figure/raw observations before calibration. Its characteristic arm length also differs from our vehicle. A focused search for the dataset DOI found the paper again, but no accessible raw observations. No dataset was acquired, and no physical-validation claim follows.

This note is preparation, not a frozen numerical protocol or completed aerodynamic result. The final model choices and test cases must be frozen before inspecting their mission outcomes.
