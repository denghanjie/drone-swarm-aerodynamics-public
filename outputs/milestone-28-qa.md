# Milestone 28 QA — completed

Final status: completed. Earlier notes below retain the live audit history; the final acceptance section supersedes their pending status.

The opposite-motor distance is independently checked against the rotor coordinates and a dimensional far-wake calculation. Seven aerodynamic checks, the exact airflow-off regression and all three two-second development smoke tests pass. Forced model-domain exits at0,0.1,0.13s retain exact terminal states and unique frame/sample timestamps. Seed1401 is development only.

The25-case paired protocol was frozen after these checks and before corrected mission outcomes. It preserves the original seeds, gains, geometry and thresholds, changing only the wake length mapping. It is a correction rerun rather than a fresh independent test set. Results, final artifact audit and browser QA are pending.

Incremental audit:73 checks passed for the first nine completed cases, including matched initial states, finite full endpoints, quaternion normalization and exact binary endpoints. Nine paired correction cases verify unchanged navigation sources; completed airflow-off outcomes agree exactly with the original. Browser QA of the corrected seed1601/wide force-only case verifies stop13.2375s, drone5, partition-0-below, exact terminal timeline and a marker centered by the camera. No errors/warnings were observed. Screenshot `milestone-28-force-contact.png` is saved. Remaining cases and numerical comparisons are pending.

## Final audit — 12 October 2026

All25 frozen runs are complete;202 artifact checks pass.20 correction pairs verify that only the intended numerical parameter changed and all five airflow-off outcomes match the originals exactly. The original five uncompleted refinements remain explicitly unpaired. All four physics-step comparisons pass with matching event identities; the separate airflow-refresh comparison fails, despite repeating the same vehicle-limit/drone4 identity.

All25 trials were loaded and advanced to Outcome in Three.js; visible states are saved in `milestone-28-browser-cases.json`. Corrected domain and cadence-stop screenshots are saved. The domain example names drone186 and the20-degree assumption boundary; its marker is amber. Browser error/warning inspection returned no entries.

Responsive check on the active browser tab confirms390px viewport and document width, with a358×420px canvas. Screenshot `milestone-28-mobile.png` preserves the narrow layout. The temporary viewport override was reset.
