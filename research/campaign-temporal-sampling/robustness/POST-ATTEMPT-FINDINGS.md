# Findings after the first passing unit attempt

No numerical compatibility or fresh campaign case had run. Static review identified these additional gaps after the first 23-group check:

1. CommonJS exports were assigned after invoking campaign main. Importing the real reconstruction module from main could therefore capture undefined helpers. The first gate fixture had explicitly mocked reconstruction, so it did not detect this. Fix: assign exports before main. Added check: real campaign/evaluate source loaded through a shared CommonJS cache with entry-point ordering, while dynamics and data are synthetic.
2. The supervisor needed to recheck its wall deadline after its last execution-validity write. Extended deterministic watchdog fixture injects the deadline crossing exactly during that write, and requires unqualified invalidation plus retained emergency evidence.
3. Display traces previously summarized only a subset of each display bin. Extended endpoint-peak fixture puts a spike strictly inside a 64-tick bin and requires that bin to retain it.
4. Viewer qualification now requires a present, successful execution-validity record. This reporting-only guard was statically reviewed by the reference reviewer before the second attempt; it was not an additional numerical fixture.
5. Freeze wording now accurately distinguishes already-recorded analytic unit checks from not-yet-run compatibility/fresh cases.

All prior tested bytes, first-attempt outputs and its result index remain retained. The second 24-group attempt passed without changing source during execution. None of the above was represented as a failed real swarm experiment.
