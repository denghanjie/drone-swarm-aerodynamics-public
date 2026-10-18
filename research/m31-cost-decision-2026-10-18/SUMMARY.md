# The current tree shortcut is slower — stop using it as an acceleration candidate for this workload

We now have a clear decision. For the same saved arrangement of 1,000 drones, the current tree shortcut was slower in **all 24 measured comparisons**, even with detailed tree records switched off. Its median paired runtime was **2.282 times** the direct method. All 116queries preserved the complete checked numerical outputs exactly.

Imagine checking a guest list. Looking through a well-organized list is already cheap. Our shortcut builds groups, searches them, and sorts the names again. It avoids some easy checks, but still has to do the same detailed work afterward. Here, that extra organization costs more than it saves.

| Method | Median complete query | Middle 50% |
|---|---:|---:|
| F: direct scan with cheap screening |36.85ms|35.88–45.92ms|
| H: tree shortcut, records off |85.15ms|84.22–85.95ms|
| HC: tree shortcut, records on |90.10ms|89.50–90.92ms|
| H0: tree machinery, skipping off |106.35ms|104.87–107.55ms|

There are 24 measured queries per method, following 16 warm-up calls; four final diagnostic queries are separate. The 2.282 ratio is the median of paired ratios, not the quotient of the table's two medians. Execution order was balanced, and no slow observations were removed.

## What explains the slowdown

H reduces candidate pair visits from 999,000 to 627,164, as before. However, both methods still perform 487,242 center-distance tests,599,336 rotor-interaction checks and produce 9,012 positive rotor terms. F already rejects the omitted interactions with a cheap component test. The reduction in candidate count is **not a reduction in the counted detailed rotor work**.

The measured build/admission phase has medians 27.10 ms for F and 75.90 ms for H. A separate instrumented H query spent about 0.60 ms constructing the tree and 49.70 ms gathering candidates across all 1,000 receivers. Gathering includes traversal, collecting and sorting. That single diagnostic cannot tell us how much belongs to each subtask or provide an exact causal decomposition.

Turning detailed tree capture on increased the median paired full-query cost by about 5.78%. It does not explain the much larger H/F slowdown. External evidence encoding, comparison, transfer and disk persistence are outside the primary timing and separately recorded. Transfer includes persistence; do not add them twice.

## Decision

The preregistered keep gate required a median paired H/F ratio no greater than 0.90 and at least 20 strict wins. Actual: 2.282 and 0 wins. **Stop pursuing this unchanged H implementation for this workload; keep F as the current computational baseline.** Do not spend another cycle merely removing its logging. A substantially different method would need a new hypothesis and separately bounded test.

This is a useful negative engineering result, not a breakthrough or a peer-reviewed publication. It rules out a proposed explanation and prevents further investment in this unchanged version. It does not rule out every tree algorithm or benefits at other swarm sizes.

## What is verified and what remains open

The actual full semantic output from every query was transferred, byte-compared with the independently exported earlier F result, saved through exact content-addressed deduplication, and reread by the independent analysis. All scientific diagnostics were compared except the four explicitly registered implementation/timing paths. Complete inputs, coefficients, solutions, loads, IDs and consumption agree exactly. Source pins remained unchanged. Two independent reviewers inspected the source and later saved results; they did not rerun the experiment or checker.

This is one projected state in one browser process. There was no new initialization, controller update, derivative, integration, high-precision reference, sustained flock flight or 5,000-drone result. Matching our own model does not establish agreement with real drones. Physical validation and genuine novelty remain unresolved.

## Visible evidence and preserved failures

[Updated Three.js view](viewer-v2/) shows the exact saved 1,000-drone arrangement alongside the measured costs. It is an interactive snapshot, not a flight animation. Seven saved-display QA groups passed, including all 1,000 positions, camera movement, mobile layout and corrupt-data rejection. Desktop and mobile screenshots were visually inspected.

The first viewer QA failed mobile width, and its screenshots did not show a useful rendered scene. That failure remains in ui/ and UI-EXIT.json. A separately registered saved-display repair passed in ui-repair/. The original frozen viewer/source, scientific allocation and analysis were not rerun or overwritten.

[Protocol](PROTOCOL.md) · [Raw analysis and every pair](results/analysis.json) · [Claim ledger](CLAIMS.md) · [Restart record](RESTART-RESULT.md).
