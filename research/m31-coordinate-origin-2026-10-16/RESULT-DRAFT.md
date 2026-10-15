# Coordinate-origin diagnostic — result awaiting independent evidence review

The complete planned comparison selected **no candidate**. All three implementations passed near the origin. On the exactly translated copy, ordinaryf32 input positions failed their interface gate; high/low positions reconstructed the original input exactly, but their GPU terms still exceeded the unchanged error allowance. No failed cell was retried and no omitted reduction was run.

These are driver observations pending the one independent saved-evidence review. They do not establish a compiler root cause, physical validity, speed or novelty.

|Origin|Arm|Observed outcome|Largest recorded conservative error(m/s)|
|---|---|---|---|
|0|A|qualified|1.57718106801e-05|
|0|B|qualified|1.03063276052e-05|
|0|C|qualified|1.03063276052e-05|
|1|A|skipped-interface-gate|GPUcell unexecuted|
|1|B|skipped-interface-gate|GPUcell unexecuted|
|1|C|failed-term-gate|0.000234548798282|

Epsilon is1.8270441835956964e-5m/s. Passing rows above include term plus serial-addition error; the translated C row is its failed pre-reduction term gate. Do not compare a missing A/B result as though it were a measured GPU error. Both origins and all required cells must qualify for selection; none did.

The same synthetic scene contains5,000source positions and four receiving vehicles, with all four rotors per receiver. It is not a5,000receiver simulation or a Boids flight. First three receivers had substantive positive exposure; the top receiver remained a visible zero control. Origin copies and receiver/arm observations are dependent.

The run ended in3.8447863329999996s externally supervised, retaining185raw files and129695212bytes. Node/browser groups were confirmed absent with no cleanup signals/errors. These times are bookkeeping, not benchmark measurements. The source remains immutable.

Next: independent saved-only review, tested Three.js evidence view, final readable claims/literature/disposition/restart and verified result publication. The failed diagnostic does not earn the planned broader confirmation.
