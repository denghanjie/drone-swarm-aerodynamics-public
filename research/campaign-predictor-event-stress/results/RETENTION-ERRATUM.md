# Post-run retention-schema limitation

Experiment: PREDICTOR-EVENT-STRESS-20261015. The frozen source and every original result remain unchanged. No corrective execution occurred.

Saved-output inspection found that the original public `geometry.boxDistance` maps its full input state. For these outside-box states its returned wall normal has 17 entries: the three spatial components followed by 14 zeros. All 14 retained normal arrays have that shape. The completed run stored those native JSON arrays correctly. The controller uses the spatial components as before; the research observer did not change its arithmetic.

The unused failure writer packs `[...normal, lower]`. Such a row would contain 18 entries, while its declared columns and prelaunch structural check assumed four. Therefore the prelaunch failure-schema/envelope guarantee is **unqualified**. The fact that the launched run completed without entering this path does not validate it.

A post-run shape-only calculation substituted 18-column rows, without model evaluation: mandatory matrices can occupy 19,408 bytes rather than 11,792. Under the same stated serialization assumptions, the maximum JSON bound was 15,520 bytes, still within the allocated caps. This arithmetic does not repair the incorrect column label, qualify all failure cases, or retroactively validate the launch review.

The completed-run native JSON, reference tensor, paired witnesses, numerical comparisons and `EVENT_EXPOSURE_INSUFFICIENT` decision are reviewed separately. They do not depend on this unused writer. Any future use must fix and independently review the failure schema first. Raw failing NaN/Infinity must continue to be preserved, rather than silently sanitized.
