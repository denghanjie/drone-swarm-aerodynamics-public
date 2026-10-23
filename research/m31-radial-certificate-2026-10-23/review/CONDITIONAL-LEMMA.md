# Conditional three-argument norm lemma

Static review by the protocol challenger, 23 October 2026. No numerical case, runtime probe, model import, benchmark, or saved-state aggregate was executed for this note. The inequalities below are an analytical derivation, not empirical evidence.

## Status and scope

This is a theorem about a specified floating-point expression under stated arithmetic assumptions. It is **not yet a theorem about every actual call to the installed Node executable's `Math.hypot`**. Source-to-executable binding and all relevant interpreter/JIT/optimized paths remain unresolved. Those conditions cannot be discharged by successful numerical tests.

The parent supplied the already-inspected tagged source at:

<https://raw.githubusercontent.com/nodejs/node/v24.19.0/deps/v8/src/builtins/math.tq>

The supplied three-argument expression, following absolute values, maximum selection and the zero-maximum special case, is:

```text
powerA = (a / max) * (a / max)
powerB = (b / max) * (b / max)
compensation = (powerA + powerB) - powerA - powerB
powerC = (c / max) * (c / max) - compensation
return Float64Sqrt(powerA + powerB + powerC) * max
```

This reviewer used that source observation as relayed by the parent and did not perform an additional primary-source acquisition. The parent reports tagged V8 version 13.6.233.17. A tag/version observation is not itself an installed-executable or all-path proof.

## Explicit assumptions

1. Inputs are three finite binary64 values `dx`, `dy`, `dz`, each with absolute value strictly less than 4. These are the **already rounded coordinate subtractions consumed by F**, not ideal real-coordinate differences.
2. `a`, `b`, `c` are their exact absolute values and `m = max(a,b,c)` is selected exactly. For the main lemma `m > 0`; the source zero case is handled separately.
3. Every addition, subtraction, multiplication and division in the displayed expression rounds individually to binary64, round-to-nearest/ties-to-even, with gradual underflow. Parenthesization is as displayed and additive expressions associate left to right. There is no unanalysed contraction, reassociation, extra-precision retention or alternative implementation.
4. Repeated evaluation of the same division or `powerA + powerB` yields the same rounded result. Ordinary deterministic binary64 evaluation provides this property.
5. `Float64Sqrt` returns the correctly rounded binary64 square root of its argument.
6. To apply the conclusion to F, the actual three-number call must follow this expression or another path for which an equally sufficient theorem has been proved. The intrinsic and execution environment must have the stated behavior.

Assumptions 3–5 define the abstract program being proved. Establishing assumption 6 for the installed runtime requires a separately documented provenance/path argument. Official release archive checksums and a local executable checksum describe different objects; they alone do not establish that binding.

## Absolute rounding bound used below

Write `RN(x)` for binary64 round-to-nearest/ties-to-even and set `ε = 2^-52`. For any finite exact real result with magnitude at most 4, `|RN(x)-x| ≤ ε`. For magnitude strictly less than 8, the weaker bound `|RN(x)-x| ≤ 4ε` is sufficient here.

These are deliberately loose absolute bounds. They also cover subnormal results and rounding to zero, so the derivation does not use a relative-error formula where underflow would invalidate it. Exact binary64 zero, one and the supplied positive maximum are available throughout. The bounded operations below cannot overflow.

## Derivation

Let `r_i = a_i/m` denote the exact real ratios and `q_i = RN(r_i)`. Since `0 ≤ a_i ≤ m`, both `r_i` and `q_i` lie in `[0,1]`, and at least one ratio and its rounded value equal 1 exactly. Thus

```text
|q_i - r_i| ≤ ε.
```

Let `p_i = RN(q_i*q_i)`. Each `p_i` is in `[0,1]`; at least one is exactly 1. Because both factors in the difference of squares are bounded,

```text
|p_i - r_i^2|
  ≤ |RN(q_i^2) - q_i^2| + |q_i-r_i|*(q_i+r_i)
  ≤ ε + 2ε = 3ε.
```

Define the exact normalized squared norm `Q = r_A^2 + r_B^2 + r_C^2`, so `1 ≤ Q ≤ 3`. Let `t = RN(p_A+p_B)`. Then

```text
0 ≤ t ≤ 2,
|t - (p_A+p_B)| ≤ ε.
```

The compensation is `k = RN(RN(t-p_A)-p_B)`. The exact inner subtraction is bounded in magnitude by 2. Write the three relevant rounding errors as `e_0`, `e_1`, `e_2`, each with magnitude at most `ε`. The cancellation is a real-algebra identity used for analysis, not a proposed code rewrite:

```text
t = p_A + p_B + e_0,
RN(t-p_A) = p_B + e_0 + e_1,
k = e_0 + e_1 + e_2,
|k| ≤ 3ε.
```

The exact input to the last compensation subtraction has magnitude at most `2ε`, so the bound on `e_2` is valid including underflow.

Let `v = RN(p_C-k)`, matching `powerC`. Its exact pre-rounding value lies between `-3ε` and `1+3ε`, hence its rounding error is at most `ε` and

```text
|v-p_C| ≤ 4ε.
```

The radicand is `z = RN(t+v)`. Its exact pre-rounding value lies between `-4ε` and `3+4ε`, strictly inside `(-4,4)`. Therefore

```text
|z-(p_A+p_B+p_C)| ≤ ε + 4ε + ε = 6ε,
|z-Q| ≤ 6ε + 3*(3ε) = 15ε.
```

Since `Q ≥ 1` and `15ε < 1`, the radicand is strictly positive. Since `Q ≤ 3` and `15ε < 1`, it is strictly below 4. The actual square-root call is consequently finite and in range. For real square roots,

```text
|sqrt(z)-sqrt(Q)|
  = |z-Q|/(sqrt(z)+sqrt(Q))
  ≤ 15ε,
```

because the denominator is at least 1. Let `s = RN(sqrt(z))`; the assumed correctly rounded square root contributes at most `ε`, giving `|s-sqrt(Q)| ≤ 16ε`. Also `0 ≤ s ≤ 2`.

Finally let `H = RN(s*m)` be the returned value. Because `0 < m < 4`, its exact pre-rounding product is in `[0,8)`, and

```text
|H - m*sqrt(Q)|
  ≤ |RN(s*m)-s*m| + m*|s-sqrt(Q)|
  ≤ 4ε + 4*(16ε)
  = 68ε.
```

The real number `m*sqrt(Q)` equals `R = sqrt(dx^2+dy^2+dz^2)` for the supplied rounded differences. Every intermediate is finite, and the returned `H` is nonnegative and at most 8, hence no greater than F's center-guard limit 512.

It follows, more conservatively, that

```text
|H-R| ≤ 128ε = 2^-45.
```

No empirical tuning enters either constant. The loose bound is chosen to simplify the proof, not to estimate observed error. The zero-maximum case gives zero under the supplied source special case and cannot satisfy the positive separation condition below.

## Conditional exclusion consequence

If a sound lower bound `L` for `R` satisfies `L ≥ 3+128ε`, the displayed program returns a finite `H` with `3 ≤ H ≤ 512`. Therefore F takes its ordinary center-distance rejection branch after its center guard. This is exactly the branch needed to leave the four rotor symbols at their initial value 1; an invalid center must not be silently treated as an ordinary rejection.

The parent proposes the more generous, prospectively fixed margin `δ = 2^-20`. Since `δ > 128ε`, a sound certificate `L ≥ 3+δ` implies the same conditional result. Increasing the margin does **not** resolve missing runtime/path assumptions; it only strengthens a theorem conditional on them.

This proof does not require a general monotonicity theorem for the approximate `Math.hypot` implementation. It uses monotone basic subtraction for the input enclosure, a real-norm lower bound on the enclosed rounded differences, and a derived absolute error bound on the specified floating-point program.

## Sound moving-box geometric lower bound

For each axis, let source and receiver coordinates remain within inclusive stored endpoint intervals. With ordinary correctly rounded subtraction,

```text
l = RN(sourceLo - receiverHi),
h = RN(sourceHi - receiverLo)
```

enclose every current rounded source-minus-receiver difference on that axis. Define `a = max(l, 0, -h)`. Then `a` is a nonnegative lower bound on the absolute current difference. This follows from the three cases where the interval is positive, negative, or crosses zero; it does not assume the current subtraction is an exact real subtraction.

The ideal squared lower bound is `S = a_x^2+a_y^2+a_z^2`. An implementation must not compare an accidentally rounded-up estimate of `S` with the radius threshold. One sound prospective construction is:

- Round each nonnegative square, move once to the next lower binary64 value, then clamp to zero.
- Accumulate with the same downward-enclosing operation after each addition, again clamping to zero if necessary.
- Compare that lower enclosure with an upper enclosure of `(3+δ)^2`, obtained by rounding the square and moving once to the next higher binary64 value. `3+2^-20` itself is exactly representable.
- Require finite endpoints and intermediates; retain/fall back whenever a prerequisite or enclosure check fails.

For correctly rounded finite basic arithmetic, one adjacent representable step encloses the exact operation. Clamping a negative lower bound to zero is sound only because the exact squared quantities and sums are nonnegative. Ordinary unadjusted multiplication/addition would not provide this guarantee. Concrete source still needs review, including the `nextUp`/`nextDown` edge cases and the actual operand order.

## Remaining gap and permitted wording

Permitted: “Under the displayed floating-point program and stated arithmetic assumptions, the derived bound implies F's ordinary radius rejection.”

Not established: “The installed executable universally implements that program on every relevant call,” “the moving cache is now an exact portable replacement,” or “a finite test proves all positions inside its boxes.”

A separately frozen finite diagnostic may record the actual intrinsic's results for every selected query and check every proposed omission. Those recorded calls establish finite observations on those exact argument words. They cannot by themselves prove the engine assumptions, unseen queries, or a universal moving-box certificate.
