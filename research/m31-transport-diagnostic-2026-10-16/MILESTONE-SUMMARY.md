# What we learned

**We found a specific browser-reported obstacle to saving results. We have not yet validated the full drone simulation.**

The previous GPU experiment stopped while sending its first output to a local file receiver. We tested that saving path with a small, known package of ordinary bytes so we could observe each stage clearly.

Chrome reported a local-network permission error. The receiver saw one connection but no HTTP request, so no payload reached a file. The new records passed their separate consistency review. This makes the new failure easier to locate, while the old experiment’s precise cause remains unknown.

What changed is our evidence: we now have the browser’s specific error, server observations, complete shutdown records and an independently checked public record. No browser security setting was changed. The failed runs remain saved.

The updated [Three.js view](viewer/) shows the five transfer stages and lets you inspect the 32 recorded events. It is a 3D diagram of this diagnostic, not drone flight. It links back to the genuine historical 3D Boids replay, which still has airflow off.

## What matters for the research goal

- A small GPU receiver calculation previously agreed with its numerical reference within its declared allowance. That is a component result.
- The full body-load GPU path remains unqualified. Several numerical and performance candidates failed their tests; those failures remain part of the evidence.
- Real aerodynamic accuracy still requires compatible measured flow, thrust and motor data. A newly verified wake preprint suggests checking average behavior separately from fluctuations, but supplies no located compatible raw dataset for our model.
- We have not established a new publishable method, a real-time 5,000-drone coupled simulation, low-end-device feasibility or real-world flight safety.

The next engineering option is to return saved values through the existing browser automation connection, with exact byte checks, rather than ask the page to make this cross-origin network transfer. That option is [planned only](NEXT-TRANSPORT-OPTION.md); it needs a fresh, separately reviewed test. Its success would still leave GPU memory handling, scaling cost and physics to establish.

[Full observations](OBSERVATIONS.md) · [Claims and limits](claims.md) · [Saved-review result](INDEPENDENT-SAVED-REVIEW.md) · [Physical evidence lead](PHYSICAL-DATA-FOLLOWUP.md) · [Restart record](POSTRUN-RESTART.md)
