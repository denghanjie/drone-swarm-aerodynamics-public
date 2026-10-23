# Numerical contract for a radius-3 certificate

23 October 2026. **The sources acquired here do not prove a lower bound for the installed executable's three-argument `Math.hypot`.** The language specification supplies no quantitative error bound, while the Node-tagged source exposes a particular algorithm whose relationship to the recorded executable has not been established by this acquisition. A proof about that algorithm would be conditional until its arithmetic and executable mapping were justified. No numerical or model code was executed.

## ECMAScript contract

TC39, *ECMAScript Language Specification*, [§21.3.2.19 Math.hypot](https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-math.hypot), accessed 23 October 2026. The live page was titled *ECMAScript® 2027 Language Specification*; this is a rolling draft reference, not a claim that a final 2027 edition was consulted. The retrieved primary search excerpt for [the 2025 edition's same clause](https://tc39.es/ecma262/2025/multipage/numbers-and-dates.html#sec-math.hypot) used the same finite-result description; the full 2025 page was not separately opened.

The inspected clause specifies argument conversion and special cases, then calls the general finite result implementation-approximated. It recommends avoiding overflow/underflow precision loss but states no ULP limit, relative-error constant, correct-rounding requirement, monotonicity guarantee or one-sided bound. Our inference is that this clause alone cannot justify replacing the actual branch `Math.hypot(dx,dy,dz) >= 3` by a real-norm comparison with an assumed numerical margin. This is an absence of the required guarantee, not evidence that a particular engine is inaccurate.

An attempt to inspect the linked implementation-approximated definition did not expose its substantive text within this allocation. No additional assertion is attributed to that definition; see [the acquisition ledger](RESEARCH-ACQUISITION.md).

## Node-tagged V8 source

V8 project authors, [`deps/v8/src/builtins/math.tq` at Node.js tag `v24.19.0`](https://raw.githubusercontent.com/nodejs/node/v24.19.0/deps/v8/src/builtins/math.tq), accessed 23 October 2026. The inspected source has a specialized `FastMathHypot` path for up to three arguments. The three-argument branch takes absolute values, obtains their maximum, handles exceptional values and zero, scales each argument, forms squares with a compensation term, then applies `Float64Sqrt` and rescales. The `MathHypot` builtin first dispatches to this fast path. Its general loop is therefore not the three-argument algorithm to analyze merely because that loop mentions Kahan summation.

Two exact source lines from the three-argument branch are:

```text
    const powerA: float64 = (a / max) * (a / max);
    return Convert<Number>(Float64Sqrt(powerA + powerB + powerC) * max);
```

The source does not attach a formal lower-error bound to this branch. This inspection did not follow Torque compilation, `Float64Sqrt` lowering, optimizing compiler substitutions, generated builtins or platform instructions. An operation-level bound remains work to prove, not a property established by the presence of scaling or compensation.

The associated [`deps/v8/include/v8-version.h`](https://raw.githubusercontent.com/nodejs/node/v24.19.0/deps/v8/include/v8-version.h) identifies major 13, minor 6, build 233 and patch 17, with the candidate-version flag zero. This is a property of the source served under the Node tag. It does not identify the engine bytes embedded in the local executable. The tag was not resolved to an immutable commit, and browser extraction did not preserve raw source bytes for hashing.

## Source claim versus executable claim

The retained [runtime record](../m31-buffered-motion-2026-10-22/runtime.json), SHA-256 `74c139dd6fb007cc20fbdec1615ceec8695174b654cd8498d0d73122eec71243`, records Node `v24.19.0`, executable size 121,304,480 bytes, and executable SHA-256 `d0c6c74401e6a544bb4d4b2a9ded9c43298d4e6dcd5ebac4dd010c4c81774105`. These are retained metadata, not a new executable inspection. A version label and binary hash identify an artifact; they do not, by themselves, show which exact source, build configuration or generated numerical path produced it.

The following are proof obligations inferred for this project, rather than guarantees supplied by the citations:

1. State a precise input domain and derive a bound for the operation sequence actually used, including rounded coordinate subtraction, division, squaring, compensation, summation, square root and rescaling. Handle the relevant exceptional, subnormal and boundary cases explicitly.
2. Establish why that sequence and its arithmetic assumptions apply to the identified executable and platform, including applicable compilation/optimization paths. A verified executable-level argument could serve instead of a source/build map, but none was acquired here.
3. Connect the resulting one-sided bound to every center difference allowed by a stored moving box, then to the original center guards, threshold-3 branch and full evidence/status contract.

A real geometric distance certificate by itself is not an exact certificate of the original software branch. Nor does one outward rounding step or an arbitrarily chosen epsilon establish the missing `Math.hypot` error bound. Finite regression or boundary tests could find mistakes, but could not turn an unproved assumption into a portable theorem. Replacing F's norm with a newly specified norm would change the reference semantics and requires a separate contract; this source review does not authorize that substitution.

Accordingly, **no useful radius-3 moving omission certificate for the pinned executable is proved by this literature acquisition alone**. This does not assert that such a certificate is impossible. The present gap is a justified operation-level bound connected to the executable, not a need for more empirical agreement before making a universal claim.

## Established neighbor-list precedent

No new acquisition was made for these antecedents. The [20 October verified ledger](../m31-buffered-candidates-2026-10-20/LITERATURE.md), SHA-256 `9a514f8e340a5d4146c08d21603c4ef1a29c512e5b44dae78496309a9db52076`, retains the access evidence and limits:

- Loup Verlet (1967), *Computer “Experiments” on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules*, *Physical Review* 159, 98, [DOI 10.1103/PhysRev.159.98](https://journals.aps.org/pr/abstract/10.1103/PhysRev.159.98). Printed page 99/PDF page 2/section II supplies the neighbor-table antecedent. Imperfect OCR and the exclusion of molecular velocity estimates as drone guarantees remain explicit.
- LAMMPS developers, [4.4.3. Neighbor lists](https://docs.lammps.org/stable/Developer_par_neigh.html), official developer documentation displaying git info 30Sep2026 at the 20 October access. Cutoff-plus-skin, reuse and rebuilding are established implementation ideas. The rolling page was not revisited and is documentation, not a second research paper.

These sources motivate conservative motion buffers; neither proves JavaScript numerical behavior, this radial certificate, a useful cost saving or drone physics. The new radius is the software's Euclidean drone-center cutoff, not the later rotor-to-wake-axis lateral quantity. There is no new-method, physical, speed or broad novelty claim.
