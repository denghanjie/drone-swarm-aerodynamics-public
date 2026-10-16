# Physical evidence checkpoint: measurements unavailable in this view

We tried to identify a published, matched propeller experiment before testing our airflow-to-thrust law. The selected comparison was one CW propulsion unit at PWM1475, with a static baseline and two axial inflow settings. The source is Simmons and Hatke (2021), *Investigation of High Incidence Angle Propeller Aerodynamics for Subscale eVTOL Aircraft*, NASA/TM-20210014010; see the frozen bibliography and SOURCE-REVIEW.md.

The public text view identified the report and relevant figure captions, but it did not expose readable load plots or a numerical observation table. **The presentation was not admitted.** One initial open and one same-document follow-up were used. No load values were transcribed, no model was scored, and no download or alternate access route was attempted. This says nothing about whether the dataset exists elsewhere or whether the model is correct.

A recording error was caught before publication. The original elapsed-time value subtracted clocks from different processes and is invalid. We preserved it in ACCESS-RESULT.original-invalid-timing.json. Saved UTC timestamps differ by 41.744003 seconds; this is consistent with the 900-second limit, but no independent monotonic wall-time supervision was established. TIMING-CORRECTION.json documents the correction and its limits.

What improved: the exact evidence gap is now explicit. What failed: this representation cannot support reproducible extraction of the selected three loads. Physical validation remains unresolved. The earlier typed-storage experiment also remains negative on its practical speed criterion; neither result is a novelty claim.

The updated Three.js page reuses an exact earlier 5,000-drone recording to keep the model visible, and clearly states that no new flight or measured loads were obtained here. It is a two-second, airflow-off replay with local 3D Boids and rigid-body dynamics, not a physically validated coupled simulation.

Next: preserve this closed access allocation. Investigate a different dependency: whether the declared provisional coupled-load law can be fed back into motion at a small interpretable scale, with domain failures and integration error exposed. That would be a numerical diagnostic only. It would not fill this physical-validation gap.
