# Independent mathematical review: fixed-lattice interval primitives

2026-10-16. Package: research/m31-interval-primitives-2026-10-16.

## Disposition and review boundary

The inspected endpoint formulas give conservative enclosures of their declared exact-real interval operations, conditional on correct standard JavaScript BigInt semantics and successful completion. I found no mathematical inclusion defect in binary64 conversion, addition, subtraction, multiplication, division, square, or square root. The integer square-root iteration has a bounded-domain termination proof stronger than merely relying on its hard cap.

This is source reasoning, not an observed qualification result or a machine-checked proof of JavaScript execution. It does not establish the finite runner/checker coverage, supervision, runtime portability, useful model precision, performance, native coefficient compatibility, or complete M-current certification. Those objects were not inspected or run here.

Only the three requested new files were read, in full, and hashed. No inherited content files were read in this checkpoint. No code was imported, compiled, executed, or tested; no fixtures, target arrays, external source, or earlier campaign was accessed; no source was changed. The exact reading inventory appears below.

## Representation and validation

The kernel uses S = 2^96 and endpoint bound MAX = 2^352. A valid pair of BigInts l <= u represents the closed interval [l/S,u/S]. The inclusive endpoint bound therefore corresponds to a real magnitude bound 2^256. It is an implementation range, not an assumed physical bound.

The interval constructor first checks BigInt types and ordering, then checks l >= -MAX and u <= MAX. Those two range comparisons suffice: with l <= u, an upper endpoint below -MAX also forces l below -MAX, and a lower endpoint above MAX also forces u above MAX. There is no unchecked opposite-side range escape.

Each arithmetic operation obtains a fresh validated frozen endpoint object through check. It does not modify the supplied interval. Successful final endpoints pass through the same constructor, so a computed range excess is rejected rather than clipped. This proof concerns ordinary data objects with stable endpoint fields. Arbitrary JavaScript getters/proxies or already constructed unbounded hostile BigInts are not a resource-controlled serialized interface; they should not be covered by an unrestricted public-API safety claim.

The decimal decode helper bounds grammar before BigInt construction: an optional minus sign and either zero or a nonzero leading digit followed by at most 106 more digits. The resulting integer is then range-checked. Negative zero is accepted and becomes ordinary integer zero; leading positive zeros, plus signs, exponent syntax, and nondecimal strings are not accepted. The permitted grammar is bounded even though it allows some numbers outside MAX, which then receive unresolved-range.

The encode helper does not call check. It is safe for the validated successful intervals used in this design, but it does not itself promise input validation or bounded serialization of arbitrary supplied objects. Clarify that precondition or harden it before claiming a general serialization boundary. This is not an error in the arithmetic endpoint formulas.

## Binary64 conversion

The input grammar requires exactly sixteen lowercase hexadecimal characters before constructing its BigInt. This gives one bounded 64-bit word. The sign, 11-bit exponent, and 52-bit fraction extraction is correct.

For exponent zero, the decoded real value is sign * fraction * 2^-1074. For a normal exponent E, it is sign * (2^52 + fraction) * 2^(E-1075). The source adds 96 to that exponent to convert the exact represented real value to lattice units. A nonnegative shift gives an exact integer endpoint. A negative shift gives an exact integer numerator divided by a power of two, to which the directed integer floor and ceiling are applied.

Both signed zero bit patterns therefore produce [0,0]. All exponent-2047 inputs are invalid-nonfinite, including both infinities and all NaN payloads. Finite values may legitimately exceed the lattice range and produce unresolved-range. A positive tiny finite value may enclose as an interval with a zero lower endpoint; a negative tiny value may have a zero upper endpoint. No sign or strict-positivity conclusion may be recovered from the original bit pattern after treating the returned interval alone as an operand.

No native floating conversion, decimal approximation, Math.sqrt, or Math.hypot participates in this conversion argument. The proof does not preserve the IEEE signed-zero distinction, because that distinction is intentionally absent from real interval semantics.

## Directed quotient and elementary endpoint formulas

After normalizing a negative denominator, BigInt division truncates toward zero. For a negative numerator with nonzero remainder, subtracting one produces the exact floor. Otherwise the truncated quotient is already the floor. Consequently ceilDiv(n,d) = -floorDiv(-n,d) gives the exact ceiling for either denominator sign. Zero divisors generate the named domain failure.

Addition and subtraction are exact endpoint sums on the lattice. Subtraction correctly reverses the second operand's endpoints.

For multiplication, the range over the rectangle of independent operand intervals has minimum and maximum among the four endpoint products. In lattice units the product is an endpoint product divided by S. Flooring the minimum and ceiling the maximum therefore encloses every exact product. Dependencies between two supplied operands can widen this independent-rectangle enclosure but cannot invalidate inclusion.

For division, excluding every denominator interval containing zero guarantees a sign-definite denominator. The quotient extrema then occur at rectangle corners. Each scaled corner is n*S/d. Taking the minimum of all corner floors and maximum of all corner ceilings is the directed enclosure of the full quotient range, including wholly negative denominator intervals. A numerator that crosses zero does not invalidate this argument. A denominator with zero as even one endpoint must remain unresolved-domain because the represented closed interval includes zero.

For square, the minimum is zero when the interval contains zero and otherwise the smaller endpoint square. The maximum is always the larger endpoint square. Division by S with directed rounding gives the correct lattice enclosure. Treating the same variable twice through the generic multiplication operation would also be conservative but could be wider; the specialized square formula uses the actual one-variable range without an independence assumption.

For these operations, the returned endpoints are the exact directed lattice endpoints of the indicated interval range, provided that they fit MAX. Thus a later checker can require exact canonical endpoints, rather than merely accepting an arbitrarily wider enclosing result. That finite-checker requirement still needs inspection of the checker implementation; this review does not assert that it is implemented.

## Square-root inclusion and bounded termination

The square-root operation first rejects a valid interval with a negative lower endpoint. It does not silently intersect a partially negative interval with the nonnegative half-line. This matches the declared whole-input domain rule.

For a nonnegative endpoint l, scaling the exact square root gives

    S * sqrt(l/S) = sqrt(l*S).

Thus the lower endpoint must be floor(sqrt(l*S)), and the upper endpoint must be ceil(sqrt(u*S)). The code obtains the upper ceiling by increasing its integer floor unless the exact squared floor equals u*S. This perfect-square test has the correct direction and treats zero correctly.

Here is an independent termination argument for the inspected isqrt routine. For integer n >= 2, let m = floor(sqrt(n)), so m >= 1. The bit-length seed is a power of two strictly above sqrt(n), hence at least m. If an iterate is x = m+d with d >= 0, then

    floor(n/x) >= m-d,

because n >= m^2 and m^2 >= (m-d)*(m+d). Therefore its integer Newton update y is at least m. The iteration never crosses below the integer root or reaches a zero divisor.

If d >= 1, then x >= m+1 and n < (m+1)^2, so floor(n/x) <= m. Hence

    0 <= y-m <= floor(d/2).

Above the integer root, the error therefore at least halves at every update. When x=m, floor(n/x) >= m, so y>=x and the return condition is reached. Its exact verification x*x <= n < (x+1)*(x+1) proves that the returned value is precisely the integer floor. The verification is retained even though the iteration argument already establishes it.

For this public sqrt operation, each radicand is at most MAX*S = 2^448. Its bit length is at most 449, and the initial power of two is at most 2^225. The initial integer error is strictly below 2^225. After at most 225 descending updates it is zero, and one further iteration detects completion. This conservative bound of 226 loop iterations is below the declared 512 cap. The n<2 early returns are also exact. This is a source-level worst-case argument, not a measured iteration count.

Math.ceil is applied only to half of a bounded integer bit length. Those small integers and half-integers are exactly representable as Numbers. This use does not assume any native square-root accuracy. The positive BigInt right shift implements floor division by two, as required by the iteration.

The named unresolved-sqrt-check and unresolved-iteration outcomes remain defensive failure paths. On validated operands under the proved algorithm and correct exact integer semantics, neither is needed to obtain a successful root. This does not imply that runtime interruption or resource failure is impossible. A checked arithmetic postcondition is also not protection against every possible engine or hardware fault.

## Range, resource, and status limits

Validated endpoint magnitudes bound multiplication and square intermediates by 2^704, and division/sqrt radicands use endpoint times S, bounded by 2^448. Addition/subtraction can temporarily reach twice MAX before being range-checked. Finite binary64 conversion has a separate bounded pre-range intermediate: its largest shift is 1067 on a significand of at most 53 bits, so an intermediate can occupy up to 1120 bits before rejection. The draft correctly mentions the independently bounded exponent; its approximately 705-bit product bound should not be read as a bound on every conversion intermediate.

These are bounded operand-size arguments, not a latency or resident-memory measurement. They do not prove that a whole future hierarchy or load certificate can complete within any budget. A fixed lattice also cannot resolve all positive scales usefully: enclosure may include zero, divisions can become unresolved, and polynomial lower bounds can lose positivity. A mathematically valid wide interval is not evidence that downstream tolerances can be certified.

The source returns an interval on success and throws Unqualified with a code on invalid or unresolved operations. It does not directly return a status record. The runner must faithfully preserve that distinction and map the intended exceptions into the declared per-case records. Unexpected exceptions, process interruption, and resource failures must not be relabeled as legitimate arithmetic successes or silently omitted. The runner and supervisor were outside this requested read.

A range/domain failure reports inability of this representation or operation contract to supply the requested successful enclosure. It is not a statement that the physical input is invalid or that a downstream model is false. In particular, a negative sqrt lower endpoint may arise because an earlier conservative interval includes negative values even if an unknown actual value is nonnegative; the failure still correctly refuses the whole represented interval.

## Scope and adoption recommendations

The protocol appropriately separates a general algorithmic argument from the proposed finite qualification. Its 1,488-record declaration is not treated here as observed coverage. No empirical record or executed fault control was inspected. Invalid grammar/malformed object behavior is explicitly outside that finite suite and remains a source/interface obligation.

No mathematical repair to the inspected arithmetic formulas is required by this review. Preserve the following clarifications when adopting the source: encode expects a validated interval unless explicitly hardened; the primitive status mechanism is a named exception that the runner must record; bounded intermediate sizes apply to validated ordinary operands and separately bounded conversion/serialization inputs; and the square-root termination argument above depends on that declared range.

The current scope does not overclaim full model correctness or performance. Complete preparation, geometric guards, coefficients, weights/source construction, candidate/row consistency, load propagation, and native compatibility still need their own implementation and proof. Primitive qualification is a necessary foundation for those later obligations, not completion of them. Any finite numerical execution remains subject to the separately frozen source gate and allocation.

## Actual reading inventory

All paths are repository-relative; all three files were read in full. No inherited content reads were used.

| Path | SHA-256 |
| --- | --- |
| research/m31-interval-primitives-2026-10-16/PROTOCOL-DRAFT.md | 15f86c9e11f7b69386b073219946539cbd66c59fe92b10b25936fdb53150a891 |
| research/m31-interval-primitives-2026-10-16/ARITHMETIC-ARGUMENT-DRAFT.md | 12363b18045043f5d550850a1f9d329f698ff96b0a71914d08ea4c0e77b4aecb |
| research/m31-interval-primitives-2026-10-16/source/interval.cjs | 73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3 |
