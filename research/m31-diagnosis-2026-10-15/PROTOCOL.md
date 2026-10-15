# M31 bounded numerical diagnosis

Status at creation: before new diagnostic outcomes. This implements the [published bounded plan](../m31-restart-2026-10-15/protocol/bounded-restart-plan.md) at audit commit `07e5165fa56f2f23bab24562b278dda1c82ed05e`. All inspected M31/M32 cases are development evidence. No fresh confirmatory population claim or new controller is being tested.

## Fixed-state decomposition (first executable phase)

Hypothesis: the large artificial neighbor-reversal effect reported in the audit arises mainly from the sequential pair projections rather than from summation order in the social rule. This is a hypothesis about the controller at two fixed states; it does not identify the cause of the historical trajectory divergence.

At the original 20 s primary states for 1,000-wide seed 2001 and 1,000-narrow seed 2002, evaluate every drone with (a) the unchanged natural order; (b) only pair constraints reversed, with wall order and all social calculations unchanged; (c) only social accumulation reversed, with all constraint order unchanged. Freeze the original six projection sweeps, speed limit, wall repair, gains, route and states. Require natural outputs and every original diagnostic field to match the frozen function exactly for all 2,000 drones. Check input states for mutation.

Save all neighbor IDs, requested/preferred/before-wall velocities, residuals, iterations and per-drone differences for all three modes. Report maximum, median, nearest-rank p95, identity of the maximum and counts above the previously exposed 0.01 m/s descriptive scale. No new pass threshold is fitted. Compare the separated effects with the previously exposed joint reversal, retaining uncertainty about subsequent dynamics. A small social-only difference does not prove it can never amplify over time.

The implementation is `source/controller.cjs`, a minimal adaptation of frozen M31 steering with separate social/pair ID arrays and extra passive diagnostics. A one-directed-pair override is implemented for the later local intervention, but is not exercised by the order probe. Its inclusion/exclusion fixtures must pass before that later intervention.

## Budget and subsequent phases

The whole diagnostic tranche retains the original cumulative **1,200-second executable wall-time**, **240-second per study trajectory**, **2 GiB raw-data**, **one solver process**, **ten study trajectories + four 0.05 s verification traces** limits. `source/run-step.py` records every executable phase, enforces in-flight wall/storage limits, and refuses duplicate job IDs. Failed harness execution requires explicit review and consumes its budget; no recorded result is silently overwritten. Fixed-state analysis is given a 120-second per-process limit. No paid resources.

The detailed microchecks, D1/D5/D2/D6/D3/D4 ordering, local L1–L4 conditions, exact scheduler, gates and stop rules remain those in the published plan. Their executable sources and hashes will be frozen in a separate pre-run commit before temporal outcomes. This staged implementation does not authorize relaxing any criterion or extending the cap after seeing order-probe results.

## Interpretation and provenance

Normal grid output remains ascending by drone ID. These artificial permutations are a controlled design-sensitivity test; they do not mean that normal execution randomly changes order. Neither permutation is accepted as a better or more physical controller. M31's three 1 cm failures remain failures. No aerodynamic load is introduced here. The prior checkpoint's verified bibliography continues to apply; no external method is newly attributed in this phase.

`freeze-order.json` pins the original scientific dependencies, the two input checkpoint files, and these executable sources before launch. The Git commit containing it pins the protocol. Results, milestone summary, next decision, visible 3D evidence and a verified public push will follow the execution.
