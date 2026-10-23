# Display evidence and failure history

Original UI attempt: CLOSED FAILED. It verified all 1,920 historical positions/status/count labels and all 1,920 diagnostic annotations before the unchanged-camera assertion failed. No screenshot or changed-evidence test was reached. Its source, lock, QA and supervisor records remain unchanged.

Separately reviewed display recovery: CLOSED PASSED. Frozen at f3101031a85b09e080214ebe4b838495d7017e83 and independently publicly verified (82 pins) before launch. One150s/16MiBallocation, no retries. All original record checks repeated and passed; playback, selectors, slider, focus, threshold toggles, orbit/reset, desktop/mobile screenshots/overflow, changed-evidence rejection and no unexpected browser errors passed. Evidence: ui-recovery/qa.json and ui-recovery-supervisor.json.

The new check scrolled the actual canvas into view, verified pointer start/end hit the visible canvas, saved geometry and camera before/after/reset, then executed one fixed drag. This establishes that this corrected interaction sequence works. The old failure's cause remains unconfirmed because its target geometry was not recorded. Do not describe the old attempt as passed or claim a renderer bug was fixed; the viewer source was unchanged.

Parent visually inspected ui-recovery/desktop.png and mobile.png. The Three.js swarm, cutoff sphere, controls, finite-result text, proposed exclusions and inherited near-field refused trial are visible. Desktop/table and mobile stacked layout are readable without page overflow. Mobile is a long scrolling evidence page. Screenshots contain only the local evidence page; no unrelated application or personal data is visible.

The replay uses earlier recorded positions and new saved annotations. It does not show new flights or new physical validation. Threshold illustrations are not certified cache bounds, airflow or safety zones. All display allocations are closed; do not rerun for prettier screenshots.
