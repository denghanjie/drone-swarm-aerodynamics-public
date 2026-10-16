# Can we safely skip whole groups?

The latest experiment found a faster way to reject far-away drone pairs while keeping the tested numerical answers unchanged. Even so, a 5,000-drone interaction query still took roughly 366–396 ms in the recorded Chrome cases. That is far too slow to establish a responsive live simulation.

This checkpoint examines a bigger step: instead of calculating every weak interaction separately, put sources into groups and calculate a guaranteed range for each group's total effect. If the range is too wide, divide the group and inspect it more closely. This could reduce work; it could also become slower if most groups need splitting.

Three independent reviews examined the mathematics, software contract and published antecedents. The mathematical chain is defensible under explicit exact-arithmetic and admission assumptions. We have not implemented those guarantees, measured their tightness or shown that the idea saves time.

An important distinction is now explicit: a guarantee for a mathematical formula is not automatically a guarantee for the existing JavaScript program, which rounds numbers and makes cutoff decisions. We adopted a separately named mathematical-model track for developing certified load estimates. Comparing it with the old program and validating the underlying aerodynamics remain open tasks.

We also corrected a planning ambiguity: the old timed queries already excluded dense classification tensors. Their removal cannot explain any future speedup. Future comparisons must ask every method to return the same loads, error bounds and status, and must include all work needed to produce them.

The visible 3D page reuses the unchanged, verified recorded Boids flights. It labels this update as design only: airflow was off during those flights, and this checkpoint generated no new trajectory or performance result. The research goal remains incomplete.

Next gate: specify and verify the numerical arithmetic and shared query contract, then freeze a bounded experiment before scoring it. Published hierarchy ideas are antecedents; novelty and practical value still require evidence.
