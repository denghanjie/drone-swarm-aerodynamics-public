# Result claims and literature

| Claim | Status | Evidence and limits |
|---|---|---|
| The adapter replaces nominal axial force/roll-pitch contribution without double counting, retaining nominal yaw torque. | Supported within tested numerical states. |6synthetic controls; independent complete body derivatives at234endpoints and192captured stages; source equations. Unsaved stages were not independently reintegrated. |
| All24 short trajectories completed and passed declared sampled timestep gates. | Observed. |results/analysis.json and independent-review.json; all32gates use the below-comparison-floor branch. This is not a proof of order, continuous-time convergence, safety or stability. |
| Load feedback changes this16-drone simulated trajectory materially relative to timestep differences. | Supported within this provisional model and seed. |Fine on/off max sampled position1.102444m; medium/fine coupled position gap5.353805e-8m. Different interventions and correlated resolutions; these are not statistical error bars or physical confidence intervals. |
| The16-drone swarm tilts84degrees. | Not supported. |84.13degrees is on/off full orientation distance including yaw. Recorded maximum coupled tilt is19.56degrees. |
| The unstabilized offset pair rotates past90degrees. | Observed model output, outside hover evidence. |Fine stage maximum92.972768degrees; no physical validation. Torque need not remain positive at terminal time; angular inertia carries rotation forward. |
| A physically accurate5,000-drone browser solution or novel method is established. | Unresolved. |No fresh physical data, browser solve benchmark, scale trial or novelty comparison in this checkpoint. |

Source commit ee1c888d1e10fd712750c8a80150b13abb32eb19; source manifest4cffb621a5925441fd0c4fcea5a55e7d1fa70d7bd931496fd74b45d9bcb6b63d. Raw trial JSON stores all fixed paths, stage summaries, actual endpoint inputs/loads, selected stage/step witnesses and applied commands. DESCRIPTIVE-STATS.json is a saved-only reduction; no additional model evaluation.

External research use is unchanged from LITERATURE-EXPERIMENT-LEDGER.md and bibliography.bib: Bauersfeld et al. arXiv2403.13321v3 motivates the inherited jet profile within its original hover scope; Reynolds's verified author pages motivate local neighborhood rules. Neither validates this scale/control/moving-state adaptation. No new citations, source access, physical scoring, version/retraction search or novelty claim was added during result interpretation. The failed Simmons–Hatke presentation attempt remains a separate closed record.
