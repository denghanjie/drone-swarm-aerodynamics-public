# Exact-lattice primitive inclusion argument

Draft for independent source challenge. No numerical evaluation has occurred. Finite evidence will be additional control evidence, not a proof covering all real inputs.

Let S=2^96. Each interval stores integers l<=u and represents all reals l/S<=x<=u/S. Endpoint range |l|,|u|<=2^352 bounds implementation resources. Failure to fit yields unresolved-range, never a clipped successful interval.

Binary64 is decoded by sign/exponent/fraction bits. Subnormals are sign*fraction*2^-1074; normals are sign*(2^52+fraction)*2^(exponent-1075). Multiplying by S and taking exact integer floor/ceiling encloses the exact represented value. Both signed zeros map to [0,0]. Exponent 2047 is invalid-nonfinite. Large finite input is allowed to be unresolved-range. Finite tiny input may have a zero endpoint; later code must not infer strict positivity.

floorDiv corrects BigInt's toward-zero integer quotient downward exactly when a negative numerator has nonzero remainder (after normalizing denominator sign). ceilDiv(n,d)=-floorDiv(-n,d). For addition/subtraction, integer endpoint sums already lie on the lattice. Multiplication takes the extrema of four endpoint products, then floor/ceil division by S. Division excludes any denominator interval containing zero; on the remaining sign-definite rectangle, quotient extrema occur at corners, so floor/ceil of n*S/d at all corners encloses the range. This includes wholly negative denominators.

Square uses lower zero when the interval crosses zero; otherwise the smaller endpoint square. The larger endpoint square is the upper bound. This is tighter than multiplication of two independent copies, without assuming independent occurrences of the same unknown value.

For square root of a nonnegative interval, lattice endpoints satisfy sqrt(l/S)*S=sqrt(l*S). Integer isqrt returns floor(sqrt(n)); the upper endpoint increments unless the upper radicand is a perfect square. The initial Newton estimate is a power of two at or above sqrt(n). The integer iteration y=floor((x+floor(n/x))/2) descends until y>=x. Before returning, exact comparisons require x*x<=n<(x+1)*(x+1), so even an iteration error cannot return an unchecked root. A 512-iteration cap returns unresolved-iteration. Native Math.ceil is used only on a small integer bit-length divided by two; no native root/norm accuracy is assumed.

Every public arithmetic operation validates its input interval and final endpoint range. Internal integer magnitudes are bounded by validated endpoint magnitudes (products at most about 705 bits; binary64 conversion shifts remain bounded by its 11-bit exponent). No arbitrary input integer string is constructed without a length/grammar limit in decode. The runner supplies valid constructed intervals, so malformed interval/bits grammar is not part of the declared 1,488-case empirical coverage. Those checks remain source-review obligations and a future interface boundary must validate serialized inputs.

This lattice may be wasteful or too coarse in extreme cases. Named unsuccessful outcomes are part of its contract. It is a candidate rigorous arithmetic/reference layer, not evidence that BigInt can meet a 5,000-drone browser latency target. It provides no guarantee for legacy native coefficients and no complete M-current coefficient or load certificate yet.
