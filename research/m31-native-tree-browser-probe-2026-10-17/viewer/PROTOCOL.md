# Prospective saved-record display plan

The flow under test is: open the milestone page, select a recorded case and one of the fixed displayed receivers, inspect the actual initial-query positions and recorded omitted groups, then switch to the accepted endpoint if it exists.

This viewer must not import a numerical producer or initialize a fresh swarm. It renders only a lossless-word projection of closed, hashed experiment records. Every public display file must identify its originating record pins, source commit and run status. A failed or incomplete attempt remains visibly failed/incomplete; an unavailable state cannot be filled with a synthetic replacement.

For each attempted case, preserve all actual drone positions and orientations from the first projected query state and, if available, its accepted endpoint. These are at most two accepted-time displays spanning 0.0025 seconds; internal RK trial states are not presented as a physical trajectory. Do not interpolate or claim a visibly evolved flock from such a short interval. Link the preceding recorded flight continuation for context.

To keep the display small, expose five fixed receiver indices: 0, floor(N/4), floor(N/2), floor(3N/4), N−1, deduplicated if necessary. For these receivers display the actual saved first-stage H gathered indices and recorded culled-node boxes. This is a display selection only; the scientific checker must still certify every receiver. Default to the first 5000 case if its record exists, otherwise the first available case. Selection is fixed before new results.

Full timing, native equivalence and coverage decisions come from saved checked results. Show correctness and the separate engineering cost gate distinctly. If the checker did not complete, label all timings as unqualified observations and withhold pass claims. A replay or static inspector establishes no simulation throughput.

UI QA uses the installed Playwright fallback because the Browser plugin/skill is not available. Preserve server8876. Check desktop and mobile, all available case/state/receiver choices, camera reset/orbit, missing/corrupt-display data, console health, exact displayed counts and positions against saved projection values. Record screenshots and review them visually. QA must call no scientific code and must verify source/result inventories remain unchanged.
