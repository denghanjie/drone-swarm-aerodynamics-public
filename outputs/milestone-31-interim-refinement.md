# Milestone 31 — first long-horizon numerical check

Seven of ten trials are saved. The remaining trials must still finish; this is an interim diagnostic.

**The wide-door 1,000-drone flock completes the course at both physics steps, but its individual paths fail the declared numerical agreement test.**

The primary step is 2.5 ms; the finer step is 1.25 ms. Both runs use identical initial states and controller settings. Both finish all drones and remain contact-free through 180 seconds. Last finish is 109.75000 versus 109.72125 seconds. These are completion times, not the terminal run times, which are both 180 seconds.

At 20 seconds, the maximum matched-drone position difference is only 1.77 micrometres. It first exceeds the frozen 1 cm criterion at the saved 35-second frame, reaches 0.501 m at 60 seconds, and reaches 5.167 m at 180 seconds. At 180 seconds, the median difference is 0.398 m and the nearest-rank 95th percentile is 1.109 m. This compares the same drone at the same recorded physical time; it does not compare unequal-time endpoints or substitute flock centers for individual positions.

The plain interpretation is that the simulated group gets through in both versions, while its precise member-by-member motion is sensitive to numerical resolution. We cannot promote short-window agreement into a full-mission accuracy claim. The result alone does not establish the cause of the sensitivity, mathematical chaos, or which trajectory is closer to physical flight.

The 1 cm threshold remains unchanged. No controller tuning or new simulation is introduced in response to this outcome. The complete report will repeat the comparison for all three prescribed refinements and retain any other failures.

[Saved comparison](milestone-31-interim-wide-refinement.json) · [Frozen method](milestone-31-source/method.md) · [Final report, pending](milestone-31-report.md).
