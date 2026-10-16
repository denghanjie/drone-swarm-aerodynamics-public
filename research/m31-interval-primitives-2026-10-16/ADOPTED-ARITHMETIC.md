# Adopted primitive argument and limits

The independently reviewed interval.cjs endpoint formulas are adopted for prospective qualification. No numerical run has occurred at this adoption. The immutable draft and complete review/MATHEMATICS.md retain the argument and its scrutiny. This is not a formal proof of the JavaScript engine or a complete M-current implementation.

The arithmetic represents [l/2^96,u/2^96], with validated BigInt endpoints bounded by 2^352. Integer directed quotients, corner extrema, the one-variable square range and checked integer square roots provide outward enclosures. Successful outputs are the exact tight lattice endpoints for the independent operand intervals, not a claim of tightness after repeated dependent computations. Tiny positive values can enclose zero, and resource/range/domain failures remain explicit.

The independent square-root termination proof strengthens the draft: write x=m+d with m=floor(sqrt(n)). Iterates stay at least m; while d>=1, the next error is at most floor(d/2). The allowed radicand is at most 2^448 and initial estimate at most 2^225, so 225 descending iterations and one detection suffice conservatively. The 512 cap and exact postcondition x*x<=n<(x+1)^2 are retained. No native sqrt/hypot premise is used.

Three source-review clarifications are adopted without changing the kernel:

- encode assumes a validated ordinary interval; it is not a general hostile-object serialization boundary. decode checks bounded decimal grammar then interval range. The fixed empirical suite does not test malformed inputs.
- Unqualified is a named exception. The runner must preserve its code; unexpected errors remain failed attempts. No failure is a physical-domain conclusion.
- Multiplication intermediates may occupy about 705 bits, while binary64 conversion has a separate bounded pre-range intermediate of up to 1120 bits. Resource arguments concern validated ordinary operands and bounded bit strings, not arbitrary proxies/getters or caller-created unbounded BigInts.

This source uses exact standard BigInt semantics as a premise. Independent Python Fraction/isqrt checks will supply finite empirical evidence for the frozen cases. They cannot establish all-engine portability, hardware correctness, downstream model precision or browser speed. No scientific result is available until the source-publication gate, sole runner/checker allocation and saved evidence review complete.

This layer is intended as a rigorous reference/certificate foundation. Its cost may make it unsuitable as a production per-interaction path. The full research still requires a current-geometry model adapter, guards, a hierarchy, a candidate solve, complete-contraction/load bounds, matched F/H/B comparisons and physical evidence. It remains the original 5,000-drone local-Boids/meaningful-dynamics goal, not a primitive microbenchmark goal.
