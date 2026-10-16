# Viewer QA

The flow under test is: open the measured-query-cost page, choose each saved snapshot, see its matching timing bars and separate cached workload, resize/orbit/reset the swarm, and follow evidence links.

Browser plugin not available; installed Playwright with Chrome155.0.8059.80 was used. Existing server: http://127.0.0.1:8876/research/m31-coupled-cost-host-2026-10-16/viewer/ . Desktop1440×1000 and mobile390×844. No dependency installation or scientific execution occurred.

Attempt1 stopped on a test issue: it tried to read rendered cached text inside a closed details element. The page and scientific records were correct. Its report, desktop capture and exact test source remain in attempt-1/. The test was corrected to open the disclosure and assert visibility before reading. Attempt2 passed all48 checks, zero console errors/warnings/HTTP failures.

| Check | Result | Evidence |
|---|---|---|
| Correct page and nonblank first screen | Pass | Title, URL, heading, audited totals |
| Framework overlay / console / network | Pass | No overlays, errors, warnings or failed links |
| All4snapshots | Pass |1000/5000/5000/5000 instances; selected state and cost summaries update |
| Numerical display scope | Pass | Full versus cached costs, observed ranges, hypothetical loads and historical airflow-off poses disclosed |
| Controls | Pass |1×/8×/4× scale, visible camera orbit change, reset, cached disclosure |
| Responsive layout | Pass | No horizontal overflow at390px; mobile screenshot inspected |
| Screenshot review | Pass | Desktop5000scene and full mobile view inspected; all drones framed, text/bars readable, no overlap |

Sources: run.cjs (final), attempt-1/run.cjs (initial), attempt-1/report.json, attempt-2/report.json. Captures: attempt-2/desktop.png, swarm5000.png, mobile.png and mobile-scene.png. Browser closed after each attempt. No browser performance, simulation frame rate, Safari/Firefox behavior or other viewport is claimed.

The results display is an interactive Three.js view of fixed experiment states. It does not run an airflow solver or generate new trajectories.
