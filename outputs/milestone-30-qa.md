# Milestone 30 — replay and artifact verification

The tested flow was: select a saved trial → show its outcome → compare the displayed count, time, filter and stop reason with its numerical record. All twelve visible entries pass: ten corrected study runs and two historical baselines. No relevant browser warnings or errors were recorded. Restart, play and pause work; playback advanced to 0.2833 seconds during the interaction check. The main research page loads the same updated viewer.

The in-app browser was used at its existing 1280×720 viewport. The full-page screenshot shows the 5,000-drone outcome, flock connectivity, 20-second endpoint and explicit full-mission limitation. No mobile viewport or other browser was tested in this milestone. The existing responsive layout was retained.

Evidence:
- [All 12 browser checks](milestone-30-browser-cases.json)
- [5,000-drone view](milestone-30-5000.png)
- [Fresh baseline contact view](milestone-30-baseline-contact.png)
- [157 artifact checks](milestone-30-artifact-checks.json)
- [21 solver/interface/equivalence checks](milestone-30-checks.json)
- [200 independent projection-reference comparisons](milestone-30-reference-checks.json)

The numerical study process finished with exit 0 before synthesis. The artifact audit checks frozen source hashes, configurations, finite states/diagnostics, unit quaternions, exact replay endpoints, frame layout, monotonic times, control-update accounting, crossing counts, preceding control timing, matched starts and prescribed refinements. The two refinement comparisons pass at exact common saved frames. They are not continuous-time error bounds or physical validation.

Reproduce in an isolated copy with `python3 outputs/research-reproduce.py --stage 30 --node node`. This was added to the reproduction helper; a second full numerical campaign was not rerun during QA. Previously frozen numerical sources remain unchanged. The rejected first implementation and all ten original job statuses remain in the error record.
