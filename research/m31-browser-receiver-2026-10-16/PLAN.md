# Can the browser GPU compute this rotor equation accurately?

This checkpoint is **prepared but unexecuted**. The source must be frozen, published and independently verified before its single scientific invocation.

A drone simulation repeatedly converts incoming air speed into rotor thrust. We will test that one calculation on the actual browser GPU. Its arithmetic keeps fewer digits than the existing CPU reference, which may make it cheaper but also introduces rounding error. This experiment measures accuracy only; it does not measure a speed advantage.

The test uses 32 fixed air-speed probes, five intentionally invalid inputs, and the 24,000 rotor inputs already saved for the 1,000- and 5,000-drone cases. These old inputs are openly reused. The GPU will not compute their wakes or move the drones. Any later 3D view will show saved poses and measured rotor results, clearly labeled as recorded evidence.

We separately check the loss caused by packing inputs into fewer digits, dividing them, solving the equation and multiplying the final force. The chosen force-error limit is 0.0000001 N per rotor, about 1.51 parts per million of nominal thrust. That is an engineering allocation for this component, not a measured flight requirement. We will also report whether it meets the much stricter earlier 0.000000000001 N comparison.

There is one capped attempt, with four GPU dispatches and no repeats. Unsupported hardware, compilation problems and numerical failures are retained as outcomes. A passing result would justify considering the next component of a GPU implementation. It would not validate the physical model, prove a speedup, establish novelty or qualify a complete 5,000-drone simulation.

Detailed contracts are in [PROTOCOL.md](PROTOCOL.md), [config.json](config.json) and [schema.json](schema.json). Verified arithmetic/API references are in [literature.md](literature.md) and [bibliography.bib](bibliography.bib). Earlier static reviews are preserved; [PREFLIGHT-RESOLUTIONS.md](PREFLIGHT-RESOLUTIONS.md) explains which draft choices were superseded.
