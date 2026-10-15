# Can the browser preserve each wake contribution before adding it?

We have checked the equation that converts incoming air into rotor force. This checkpoint asks where that incoming-air number comes from. For four fixed receiving drones, the browser will calculate a separate contribution from every source ID and then add the saved contributions in a fixed order.

The purpose is to distinguish two possible errors: calculating a contribution inaccurately, and losing accuracy when adding contributions. Rounding the positions and prepared axes is checked separately before either GPU stage. A small final difference is insufficient if positive and negative term errors cancel: the acceptance gate charges the sum of their absolute differences.

The four receivers were selected from already exposed records by fixed rules. The weakest row is allowed to have exactly zero inflow; it will not be replaced. Five thousand source IDs does not mean five thousand nonzero terms. This is sixteen rotor sums, not a complete 5,000-drone GPU flight.

The result will be a numerical component test against the declared reference equations. The force-related tolerance is a chosen engineering allocation derived through those equations, not a measured physical tolerance. No flight, performance or novelty result is promised. A separate Three.js view will show the actual saved geometry and contributions, with failed or unexecuted stages identified.

The original eight-step roadmap remains intact. This advances Step 6's implementation checks while the physical-validation, coupled-flight and publication requirements remain open. The original Milestone 31 Boids replay remains available and retains its airflow-off limitation.

Every source and input must be frozen, independently reviewed, published and independently verified before the sole bounded invocation. The result and sole saved-data review will preserve every failure. No new launch is permitted after 07:00 Asia/Shanghai on 16 October 2026.
