# Milestone 24 verification record

## Numerical and artifact checks

The frozen experiment contains 16 prescribed runs: 12 primary cases and four physics-step refinements. See the report and numerical-comparison JSON for scientific acceptance, separately from software QA. `milestone-24-source/check.cjs` checks analytic geometry, exact grid/brute neighbor equivalence, short trajectory equivalence, swept-contact broadphase, route-center clearance and valid initial clouds. Its six checks passed; larger initial clouds alone are not mission evidence.

`milestone-24-source/audit.py` checks frozen source hashes, every prescribed configuration, matched initial states, replay indexes, exact final replay positions/quaternions, displayed metrics and local links. Output is saved in `milestone-24-artifact-checks.json`.

## Browser checks

Tested in the Codex in-app browser at 1440×1200 and 390×844. Temporary viewport override reset afterward.

- All 12 trial selections loaded. Outcome displays matched 50/50 or 200/200 saved completions; contact buttons were disabled for these no-stop trials. Exact observed UI values are in `milestone-24-ui-outcomes.json`.
- Play advanced recorded time; pause, restart, outcome and timeline worked.
- Whole-factory, close-up and top cameras operated; shell, route and trail toggles changed their checked state and corresponding view.
- The 200-drone case at 48 s displayed a connected group of 200, 92% direction agreement and 3.9 m vertical spread. The visible drones form a volumetric group around the factory geometry.
- Mobile document width was 390 px at a 390 px viewport, with a 358×420 px canvas and no horizontal overflow. Screenshot inspected.
- No browser warnings/errors were captured.

Fixed two viewer issues during QA: set the canvas CSS width/height explicitly to prevent high-DPI backing dimensions overflowing the panel; request replay indexes/data without cache so completed trials appear on reload. Neither change affects the frozen numerical source.

Screenshots: `milestone-24-preview.png`, `milestone-24-mobile.png`. These are UI evidence, not physics validation or browser performance measurements. Three.js displays saved offline positions and quaternions; interpolation is visual only.
