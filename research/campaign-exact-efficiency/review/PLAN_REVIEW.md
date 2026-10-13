# Independent pre-run physics and numerical review

Reviewed 2026-10-13. Baseline checkpoint `c024dfc27b9e6b7cd5b39132164d1339cb95b12f`; underlying model `c591ce2b195fa01b895d4ba881a44a4b92fdd703`. This review concerns the pre-run numerical methodology. Source, original eight-step roadmap, prior campaign plan/amendments/results, original wake/receiver/mechanics/grid implementations, and new frozen plan were inspected independently.

## Decision

The bounded plan is appropriate for a same-equation CPU implementation experiment, conditionally on the output-ownership amendment below. Proceed only to tiny correctness checks and independent code review; broader correctness and serial timing require the declared review gates. Physical validity, safe flight, long-horizon convergence, GPU and 5,000-agent feasibility are not established.

## Required clarifications before measurements

1. Preserve the existing caller-owned result contract. Returned winds and metadata from one call must remain unchanged after later evaluations, state mutations, and swarm-size changes. Reuse internal scratch only. If any borrowed-output path remains, count its necessary copy in a separate fair API comparator and verify every caller; do not pool its timing with owned-output methods.
2. Preserve ascending source summation order per receiver rotor, all four sample locations, near-field and tilt rejection, force/roll/pitch response, and nominal yaw convention. For multiple unsupported pairs, preserve the original receiver-major, rotor-major, ascending-source first near-domain failure; global tilt checks continue before pair traversal. No support cull may hide an invalid pair.
3. Finite 17-component and unit-quaternion checks are field-input hardening. Negative stored motor thrust is rejected by load conversion, not necessarily the geometry-only field function. Do not claim universal legacy input equivalence.
4. Publish comparisons against legacy, previous bound-paying zero, lean, support, and reuse separately. A win against previous-zero alone is not proof that support culling or scratch reuse helps; isolate those increments versus the new lean exact control. Select on development data only and freeze identity/source before held-out timing. Report every measured regression and failed gate.
5. Preserve complete paired sample order and batch calls, state hashes, source hashes, and actual durations. Bootstrap intervals describe this experiment/host; they do not supply hardware-generalization or formal multiple-comparison guarantees. Any identifying machine metadata stays out of portable/public artifacts.

## Geometry proof obligations

The frozen source support is downstream `[farStart, 2.5)` with radial distance below three local half-widths. The half-width is increasing with downstream. At the axial endpoint its maximum is `0.22702516449366392 m`. For an exactly unit source axis, any positive sampled point is within `hypot(2.5, 3*halfMax)` of its source, and its receiver center is within that distance plus the receiver rotor-offset norm `0.03959797974644667 m`. Their sum is `2.630710448903349 m`, strictly within the unchanged 3 m neighbor search. The near-domain center envelope is `hypot(farStart, 0.15) + rotorOffset = 0.28799282671393106 m`.

A center-envelope support cull must overestimate all four actual point locations, retain equality/roundoff margins, and account for the accepted quaternion-norm tolerance. The dot/projection formula uses the unrenormalized rotated source axis; accepted near-unit states must not be silently normalized or treated as perfectly unit when that can understate an envelope. A lower bound on radial distance must use the operator norm of `I - axis*axis^T`, or a demonstrably conservative inflation. Tests complement this argument; they do not prove arbitrary floating-point geometry.

The source strength remains isolated-hover scale independent of stored nominal motor thrust. Changing that relationship would change the model. Existing support truncation is itself a model assumption; retaining it exactly is not an infinite-domain or physical-accuracy guarantee.

## Independent coverage division

An independent all-pairs implementation and broad fixture matrix cover support/fade/near-field/tilt/search boundaries, asymmetry, overlapping sources, density and size, permutation/translation/yaw transformations, malformed-input handling, and immutable-output reuse. This physics review additionally inspects cull algebra, operation and guard order, stale scratch risks, frozen raw statistics, and portable artifact privacy/license/data identity. No expensive benchmark was run for this review.
