# Independent geometry classifier: static rationale

Artifact: `m31-domain-independent.cjs`. Prepared without importing or executing the module, constructing any poses, evaluating any cases/fields/forces, integrating dynamics, or running a benchmark. Only source text was read and files were written. The forthcoming frozen audit owns execution and comparisons.

The classifier imports nothing from the production physics, wake, grid, or aerodynamic modules. It contains no flow-amplitude formula, receiver thrust solver, rotor wrench, state advancement, timers, random inputs, or file I/O. Constants are frozen at arm coordinate a=0.028 m, motor separation D=2√2 a, normalized minimum downstream=2.5, near radius=0.15 m, downstream cutoff=2.5 m, radial cutoff=3 half-widths, half-width spread=0.07668, virtual origin=−5.817, and strict source-center radius<3 m.

## Public contract

`prepare(poses)` accepts an array whose rows are seven finite numbers `[x,y,z,qx,qy,qz,qw]`. It returns copied positions, body +z axes in world coordinates, and the four world rotor centers for every pose. An explicit 3×3 quaternion matrix replaces the production double-cross rotation. Rotor order is (+a,+a), (−a,+a), (−a,−a), (+a,−a). Quaternions are never normalized or repaired. The module applies no tilt gate; the caller must independently report the original global tilt gate and mark all classifications hypothetical whenever that gate fails. For nonunit quaternions, the unnormalized algebra is retained rather than represented as a valid rigid rotation.

`classifyReceiver(prepared,i)` loops directly over **every** j≠i. Its result contains:

- `receiver`: i.
- `codes`: `Uint8Array(4*N)`, with entry `4*j+k` identifying source j and receiving rotor k.
- `counts`: plain eight-element array counting every code in `codes`. The total is 4*N. This includes four self entries as code 0, plus four code-0 entries per outside-center source.
- `centerChecks`: N−1, one center-distance test per nonself source.
- `eligible`: number of source centers with strict distance<3 m. Exactly four entries are classified for each eligible source, so `4*eligible == sum(counts[1:])`.
- `nearEvents`: every code-3 or code-4 event in ascending source index and then ascending rotor index, as `{source,rotor,down,radial,code}`. A code-3 event is retained and does not stop hypothetical classification of subsequent source/rotor combinations.

## Exact branch order

1. Self and outside-center entries remain code 0. The center check is on vehicle centers, not rotor points, using `Math.hypot` and strict `<3`, matching the original grid's neighbor predicate while independently enumerating all sources.
2. Project the vector from the receiver rotor point to the source center onto the source axis. Downstream≤0 is code 1; downstream≥2.5 m is code 2. Radial position is not evaluated for these branches.
3. For 0<downstream<2.5 m, subtract the downstream projection and measure radial norm. If downstream<2.5D, radial<0.15 m gives code 3, and radial≥0.15 m gives code 4. This near-wake test precedes the far radial cutoff and receiver/source projection.
4. At downstream≥2.5D, calculate only the geometric half-width `spread*(downstream/D-origin)*D`. Radial≥3 half-widths is code 5.
5. Remaining geometry has code 6 if the nonnegative receiver/source axis dot product is zero, and code 7 otherwise. No inflow amplitude, fade amplitude, rotor load, or force is calculated. Code 7 means retained positive geometric support within the prescribed algebra, not a physical validation or certified force bound.

Boundary equality therefore belongs to code 0 at center distance 3; code 1 at downstream 0; code 2 at downstream 2.5 m; the far branch at downstream 2.5D; code 4 at near radial 0.15 m; code 5 at far radial 3 half-widths; and code 6 at zero axis projection.

## Comparison limits and static checks

The independent matrix and the production double-cross rotation are algebraically equivalent under the intended normalized input quaternions, but last-bit rounding can differ. A bitset disagreement near an exact branch boundary must be retained with its poses and diagnostics; it must not be hidden by changing a tolerance after exposure. Counts alone do not prove classifier equality: compare the complete per-source/per-rotor byte array. The near-event numbers support diagnosis of codes 3/4. Optional nearest-boundary diagnostics were omitted to keep the classifier small and its work accounting clear.

Source inspection establishes that each eligible source classifies each of its four receiving-rotor entries exactly once; every such branch has a code from 1 through 7; initialized zeros cover self/outside-center entries; the counters track each written byte; all near events are emitted before subsequent sources are considered; and no global tilt error short-circuits the hypothetical classification. No runtime validation or scientific result is claimed here.
