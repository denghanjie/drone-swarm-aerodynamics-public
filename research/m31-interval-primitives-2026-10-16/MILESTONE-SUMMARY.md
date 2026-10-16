# Arithmetic foundation: the frozen test passed

Before grouping aerodynamic interactions, we need arithmetic that never silently rounds an error bound in the wrong direction. This checkpoint built a small interval-arithmetic layer using exact integers and checked it with a separately written Python rational-arithmetic implementation.

The published, predeclared suite produced **1,488 matching records with zero mismatches**. Of these, 1,032 returned the expected enclosing intervals; 215 correctly refused a domain condition such as division by an interval containing zero; 236 correctly reported that the requested interval exceeded the representation's range; and 5 correctly rejected nonfinite inputs. The refusals were expected test outcomes, not failed runs.

The checker also rejected all six deliberately corrupted records: an interval that excludes the exact answer, a wrong status, a missing case, a duplicate, reordered cases and an altered input. The complete journal agrees with the final result. Source was frozen, pushed and independently downloaded from GitHub before the first numerical run. Both sole attempts finished successfully with closed process groups and unchanged source/executable identities.

This supplies finite experimental evidence for the primitive arithmetic on the recorded Node runtime. A separate mathematical review supports the general inclusion argument under exact BigInt semantics. Neither finding proves every runtime or hardware implementation correct.

It is a necessary foundation, not a swarm breakthrough. The complete geometric model, group bounds, coupled-load certificate, browser execution and speed comparison remain to be implemented and qualified. Real aerodynamic accuracy and novelty remain open. These tests do not measure 5,000-drone performance.

The 3D page keeps the unchanged historical Boids replay visible and clearly labels it. No new drone flight was generated. The next checkpoint should connect the arithmetic to the fully specified current-geometry and branch/admission model, with its own reviewed protocol and source-publication gate.
