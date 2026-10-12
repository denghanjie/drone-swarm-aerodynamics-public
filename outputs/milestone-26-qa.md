# Milestone 26 QA — completed

Final status: completed. Earlier notes below retain the live audit history; the final acceptance section supersedes their pending status.

Numerical implementation checks pass through 5,000 bodies: exact final states, scientific metrics, samples and sparse replay frames agree with the earlier fixed two-second runs. Geometry variants and progress callback regression also pass. Streaming uses Float64LE with a declared layout. Full-mission numerical comparisons remain pending.

An initial factory-wrapper syntax error prevented the first study launch from starting numerical jobs. The error and startup protocol were retained in `milestone-26-development/`. The wrapper was corrected, both variants checked, and the final protocol frozen before any mission outcomes. No controller gains were changed after outcomes.

An incremental artifact audit passed74 checks across9 completed runs; the two5,000 jobs remain outstanding. Available full comparisons:200/narrow misses the1cm endpoint threshold (5.445cm), while1,000/wide repeats the contact and agrees to1.067mm. These are distinct numerical outcomes.

Browser QA on the current research page verified the1,000 primary contact at16.020s, drone296 and partition-0-above, a timeline ending at the actual stop, and an unobscured red marker. Earlier50-drone interpolation and geometry switching were also checked. At390×844, document scroll width is390px and the3D canvas fits358×420px. No browser error/warning entries were observed during the latest check. Desktop and mobile screenshots are saved. Final5,000 loading and all-case checks remain pending. This is an in-progress record, not a completed QA claim.

The completed5,000 primary replay was loaded and inspected in Three.js: stop11.9525s, drone4215, partition-0-above,0/5,000 finished, entire sampled flock still connected. The contact camera was corrected to center the affected drone rather than the centroid of the very long flock; the red marker is now visible at the wall. Screenshot `milestone-26-contact-5000.png` preserves the verified view. No browser errors/warnings were observed. The final5,000 refinement is still running.

## Final audit — 12 October 2026

All 11 frozen runs are complete. The final artifact audit passes 85 checks, including unchanged numerical sources, exact Float64 endpoints, checkpoints and geometry. Both 5,000 runs stop against the same wall with drone4215; the endpoint difference is1.084mm and stop-time difference1.25ms. This descriptive early-stop supplement does not replace the failed/missing20s-checkpoint criterion. The200/narrow5.445cm discrepancy remains a failure.

All11 cases were loaded through the Three.js selector and advanced to Outcome. Visible completion, stop identity and actual terminal timelines were saved in `milestone-26-browser-cases.json`. The5,000 finer-step contact view is saved in `milestone-26-refinement-5000.png`. Earlier desktop/mobile screenshots and measured390px no-overflow check remain applicable because the page layout has not changed.
