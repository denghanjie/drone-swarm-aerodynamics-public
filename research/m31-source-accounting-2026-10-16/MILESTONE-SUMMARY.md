# Source wake: a limitation made explicit

**The current wake does not respond directly to source motor strength.** In the new fixed-position test, all four receiving rotors saw exactly **2.524178 m/s** for every source setting: off, quarter-hover, hover, twice-hover and unequal motors with the hover total. The exact extracted field function produced all 20 values. This is a property of our numerical model, not an observation of a real drone shutting down.

That matters because our goal is mutual aerodynamics: the air a drone produces should depend on its operating state. A prescribed hover wake can still be a useful numerical benchmark, but it cannot yet supply that response. Changing the total amplitude alone would also leave the question of unequal-rotor wake shape unresolved.

We also measured what the model's cutoffs remove. For a specified squared-speed cross-section proxy, the radial fade retains **97.1366%** of the untruncated profile. The downstream fade reduces that further between 2 and 2.5 m and sets it to zero at 2.5 m. The numerical integral agrees with its available closed form, and refinement differences are below the prespecified threshold. These percentages describe this mathematical proxy, not the percentage of a real drone's thrust preserved.

The untruncated proxy equals 0.71677 times the model's nominal weight. We deliberately do not call the remaining difference “missing thrust”: the underlying fit concerns mean speed magnitude, and a full force balance needs more flow information. No coefficient was adjusted to force agreement.

As a small physical reference, we reproduced one already-published Mavic 2 Pro front/back comparison from [Wolf et al. (2024), §3.2](https://doi.org/10.1007/s00348-024-03880-3). The squared-frequency ratio is 1.34675; the ratio of the printed flow-derived loads is 1.36410, a 1.27% relative difference. The input rounding and authors' separately reported ratios are preserved. This provides context for unequal source weights; it is neither a new finding nor validation of our 27 g model.

**Decision:** return to the source/receiver contract before pursuing another speedup for the final coupled-swarm claim. Keep a prescribed-source benchmark explicitly labeled. Test a future motor-responsive source against compatible measurements; do not silently promote a square-root amplitude rule or force-normalized profile to validated physics. The current two-article data search did not supply the required raw reference.

The independent saved-result review passed **46 checks**, using separate arithmetic and a different integration method. The new **Three.js profile view** passed 99 display checks, including desktop/mobile layout and refusal of corrupted evidence. It renders the saved profiles; it is not a newly validated fluid simulation. Both failed display-check attempts remain saved with their corrections.

This checkpoint revisits original Steps 2–4: credible dynamics and two/multiple-drone interactions. Steps 5–7 retain the genuine local 3D Boids and scaling objective, but the final physical and publication gates remain open. Read the [claim ledger](CLAIM-EVIDENCE-LEDGER.md), [raw numerical result](results/result.json), [source witness](results/witness-stdout.json), [protocol](PROTOCOL.md), [literature](literature/LEDGER.md), [QA record](QA-REPORT.md) and [3D numerical view](viewer/).
