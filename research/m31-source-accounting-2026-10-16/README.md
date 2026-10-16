# What does our source wake actually represent?

This checkpoint audits the source model before further optimization. It asks whether changing the source motors changes the computed field, how much of a stated profile its cutoffs remove, and what a small published asymmetric-rotor comparison can legitimately tell us.

The [protocol](PROTOCOL.md) separates a numerical implementation witness, mathematical profile accounting and descriptive reproduction of published numbers. None is a physical validation of our 27 g vehicle. The [derivation](literature/DERIVATION.md) and [source ledger](literature/LEDGER.md) explain why a squared-speed integral must not automatically be called measured thrust. We will not tune the model to force that integral to equal vehicle weight.

The scientific sources are frozen before the single new CPU invocation. Previous GPU/browser campaigns remain terminal and unchanged. The original eight-step research structure is retained: this is work on the physical-model/reference requirements that must support later approximation and scaling claims.

Source-level derivation is already available; execution status and results will be recorded in `results/` and an additive result summary. The eventual Three.js view will display saved numerical profiles and source-state outputs, with a separate link to the historical local 3D Boids replay.
