# QA — checkpoints 15–18

The flow under test is: load the research viewer → choose a recorded case → play or jump to an outcome → display the saved completion, stopping and connectivity results with the corresponding 3D trajectories.

## Summary

The viewers and research records passed the software checks below. Several controller/numerical acceptance tests failed; those scientific failures are preserved and explicitly reported. A software QA pass does not override them.

## Environment and changes

- Local loopback server: `http://127.0.0.1:8875/outputs/research-results.html`.
- Unified computer-use in-app browser, using its supported Playwright locators and native accessibility snapshots. A separate Browser skill was not listed; no browser dependencies were installed.
- Desktop 1440×1100; mobile 390×844. Main dashboard and checkpoint 15–18 pages inspected.
- Saved Three.js replays added for every checkpoint. Whole-course framing now includes drones beyond the finish plane. Controls stay disabled until records load. Long scenario names originally caused mobile overflow (498 px on a 390 px viewport); CSS sizing reduced document width to 390 px.

## Checks

|Check|Result|Evidence|
|---|---|---|
|Page identity|PASS|Main dashboard URL and title matched the new checkpoint 18 viewer.|
|Nonblank 3D rendering|PASS|Two canvas panes rendered actual drone models, obstacles and trails.|
|Framework/runtime overlay|PASS|None in inspected screenshots or DOM.|
|Console health|PASS|No relevant errors or warnings on checked pages.|
|Interaction proof|PASS|Scenario changes, outcome jumps, playback, close-up camera and neighbor-link toggle updated visible state.|
|Responsive layout|PASS after fix|Mobile document width equals 390 px; no horizontal overflow.|
|Saved failure visible|PASS|Checkpoint 17 retention seed 901 stops at 21.78 s with 0/50 completions.|
|Saved regression visible|PASS|Checkpoint 18 seed 1004: both finish 50/50; connected group 50/50 vs 41/50.|
|Development improvement visible|PASS|Seed 801: reference 49/50 versus inward offset 50/50.|
|Numerical comparison visible|PASS|Checkpoint 15 steering-only:49/50 in both integration-step panes.|
|Syntax and local links|PASS|22 JS/CJS files checked; no broken links in checked checkpoint pages/reports.|
|Frozen controller sources|PASS|Checkpoint 17/18 controller hashes match their pre-run protocols.|
|Physics dependencies|PASS|Physics and swept-contact dependency hashes match the pre-block archive.|
|Reproduction spot checks|PASS|Two diagnostic replays match saved states/metrics exactly; three 2.5 ms audit reruns reproduce earlier metrics exactly.|

## Interaction loops

- Checkpoint 16 → seed 801 → Outcome:49/50 vs 50/50, but the retention connected group is 32/50. Switch to 802 → Outcome:49/50 vs 50/50, retention connected group 50/50.
- Checkpoint 17 → tight course → retention → Outcome: collision stop is preserved. Switch to sphere course and smoothed steering →25 s → Play: clock and recorded statistics advance.
- Main dashboard → development 801 → Outcome: recovered straggler. Switch to fresh 1001 wide → Outcome: both 50/50. Switch to fresh 1004 → Outcome: candidate fragmentation remains visible. Fresh 1001 tight →25 s → close-up + local links:3D passage view and local-neighbor visualization are present.
- Mobile 390 px → reload → Outcome: controls enable after load and the document remains 390 px wide.

## Commands and APIs

Used `node --check`, saved artifact/link validation, source SHA-256 comparisons, and the isolated-reproduction manifest check. Browser checks used `reload`, supported locator `selectOption`/`click`/`check`, accessibility state, read-only DOM layout measurements, console logs, and screenshots. The initial exact-label selector for Scenario did not match; a documented locator using its observed `scenario` ID worked. No application defect was inferred from that locator mismatch.

## Remaining risk

Only the in-app browser and these two viewport sizes were inspected. The views replay fixed saved trajectories; this QA does not benchmark an integrated live physics loop. Airflow, uncertain sensing and real-flight validity are not covered. The smaller-step audit preserves a seed 905 failure changing 50 to 49 finishers; the report does not mark the research complete.

## Screenshots

[Desktop passage view](research-block-passage-preview.png) · [Retention failure](milestone-17-retention-failure.png) · [Development outcome](milestone-16-preview.png) · [Mobile after correction](milestone-18-mobile.png) · [Mobile before correction](milestone-18-mobile-before.png)
