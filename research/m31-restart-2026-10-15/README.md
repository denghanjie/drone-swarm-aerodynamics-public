# Milestone 31 restart — first research checkpoint

**Decision:** retain M31 as an airflow-off engineering baseline, preserve its failed trajectory-accuracy tests, and investigate one bounded numerical question before optimizing aerodynamic calculations. No breakthrough or physical-validation result is claimed.

The eventual question remains: **which shortcuts let a genuinely local 3D flock of up to 5,000 drones run efficiently in a browser without changing the physical predictions we care about?** This checkpoint checks whether the existing evidence is a trustworthy starting point.

## What we learned

- The four prescribed primary candidate missions finished. Three matched fresh baseline missions stopped at walls. These are observations in the saved model, not general flight-safety evidence.
- **All three original 1 cm path-agreement tests failed.** Halving the physics integration step produced maximum same-drone position differences of **5.17 m**, **32.77 m**, and **7.98 m**. The 5,000-drone comparison covers only the first 60 seconds.
- A new descriptive calculation found that individual finishing times can change substantially while the total finishing pattern changes little. In the narrow 1,000-drone case, the largest individual difference is **53.55 seconds**, yet the largest difference in the fraction finished is **0.6 percentage points**. These measure different things; neither replaces the failed path test.
- An exploratory calculation at the same saved state found that reversing neighbor-processing order changes some requested velocities by about **0.17 m/s**. It changed two calculation orders together. It supplies a lead to test, not an established cause of the historical divergence or a better controller.
- **M31 has no aerodynamic interaction.** It uses local 3D Boids, shared map-informed route guidance, rigid-body dynamics and ideal observations. Physical airflow fidelity, WebGPU throughput and novelty remain unresolved.

Every quantitative statement above is traced in the [claim–evidence ledger](claims.md), [evidence audit](evidence/audit.md) and its saved calculations. The [3D evidence viewer](viewer/index.html) overlays exact historical poses at selected saved times. It is a recorded-state comparison, not a live physics simulation. Cyan is the 2.5 ms calculation; amber is 1.25 ms. Use **Largest gap** to inspect the highlighted same-drone disagreement.

## Next experiment, in ordinary language

First ask whether the controller's answer changes because we add neighbors' motion in a different order, or because we handle collision constraints in a different order. Change only one at a time, while holding the drone states fixed. Then compare a small, fixed set of ten-second restarts to separate inherited-state differences from time-step and feedback effects.

The [bounded plan](protocol/bounded-restart-plan.md) permits at most ten study trajectories plus four 0.05-second verification traces, all within 20 minutes of computation in the next tranche. It specifies exact negative controls, stop conditions, and what each comparison can and cannot explain. No new full-swarm trajectory campaign was launched in this checkpoint. Six single-drone integration steps checked three saved contacts; the other new calculations reanalyzed records or evaluated the controller at fixed states.

After this one diagnostic tranche, return to a small aerodynamic model comparison. Independent measurements of force and moment are still needed before a physical-accuracy claim. A [verified map of eight publications](literature/annotated-ledger.md) guides that work; it is not an exhaustive novelty search. Seven sources were inspected in relevant full-text sections; Reynolds is explicitly limited to primary author pages and the original abstract/citation.

## Records and reproducibility

| Record | Purpose |
|---|---|
| [Evidence audit](evidence/audit.md) | Checked outcomes, failures, model assumptions and limits |
| [Claim–evidence ledger](claims.md) | Exact claim, status, source, uncertainty and next challenge |
| [Experimental plan](protocol/bounded-restart-plan.md) | Bounded development diagnosis and later aerodynamic proposal |
| [Independent challenge](protocol/challenging-review.md) | Competing explanations and reasons not to overclaim |
| [Literature ledger](literature/annotated-ledger.md) / [experiment mapping](literature/experiment-map.md) / [BibTeX](literature/sources.bib) | Verified sources, their use and untested adaptations |
| [Reproduction and restart](REPRODUCE.md) | Commands, dependencies, inputs and next action |
| [Provenance](provenance.json) / [payload manifest](manifest.json) | Source version, prior exposure and file integrity |
| [Viewer QA](viewer/qa.md) | Browser checks and visible evidence |

## Position in the original eight steps

The [original roadmap](../../outputs/research-roadmap.md) is retained unchanged. This checkpoint revisits Step 1 (measurements and references), checks the limits of Steps 2–5 (vehicle, interactions, local flock), and specifies gates for Steps 6–8 (acceleration, scale, contribution). It does not restart or erase later milestones.

This additive research branch begins at public commit `c591ce2b195fa01b895d4ba881a44a4b92fdd703`. Existing M32 findings and the later DOT work at remote main `1336f5c416875a9651f92b58b2ed06649f25b04e` are prior context. That later work is preserved on main, not overwritten or relabeled as our discovery. All inspected historical cases are development evidence.
