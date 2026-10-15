# Receiver-only f32 kernel: static draft contract

2026-10-16. Companion source: `m31-receiver-f32.wgsl`. This is an uncompiled, unexecuted source draft. It contains no wake field, source summation, geometry, neighbor search, integration, benchmark or timing measurement. The intended finite inputs are the 24,000 already saved independent-I rotor inflows from the exposed fresh1000/fresh5000 zero-screen cases plus 32 fixed U probes in [0,128]. Five proposed invalid-control records are separate: U=-1, U=NaN, U=+infinity, vi=0 and f0=-1, with other fields using the frozen valid constants. Final config must freeze all original and uploaded bit patterns, row ordering and expected classifications before execution.

## Bindings and exact layout

The input is a storage array of four raw u32 members; the output is a storage array of eight f32 members. Member alignment is 4 bytes. Input structure size/array stride is 16 bytes; output size/stride is 32 bytes. No implicit vec3 padding is used.

| Binding | Access | Record offsets in bytes |
|---|---|---|
| group0/binding0 | read | uBits:u32 at0, f0Bits:u32 at4, viBits:u32 at8, padBits:u32 at12 |
| group0/binding1 | read_write | alpha:0, x:4, f:8, reportedResidual:12, iterations:16, stopCode:20, finalAbsStep:24, reserved:28 |

Input padBits and output reserved are zero. The kernel rejects nonzero padBits. Field aliases after raw validation are `u=bitcast<f32>(uBits)`, `f0=bitcast<f32>(f0Bits)` and `vi=bitcast<f32>(viBits)`; these are bit reinterpretations, not integer-to-float numeric conversions. The host must bind exactly the intended input record byte range and allocate/bind an output record for every input. `arrayLength(&inputs)` supplies the count; the workgroup size is 64 and the host dispatch is `ceil(count/64),1,1`. Out-of-range invocations return before accessing a record. A mismatched output size is a host-contract failure, not a scientific result. For the proposed 24,037 records, the exact unpadded array payloads would be 384,592 input bytes and 769,184 output bytes; extra dispatch lanes are bounded by `arrayLength`.

Every in-range invocation first writes a complete invalid sentinel: all eight floats are zero except stopCode=3. Successful completion overwrites that record. Thus any local guard return preserves the documented invalid result rather than an unwritten record. A device/dispatch/readback failure cannot be inferred from these records alone; the host must separately require API success, complete readback and complete record coverage. In particular an untouched zero-initialized output buffer is not evidence of zero-input identities.

## Frozen input requirements and guards

The host must verify every valid record's f0 and vi are bitwise equal to the two selected uploaded f32 constants. This is a fixed-constant experiment. The kernel additionally requires U in [0,128], f0 in [0.01,0.1] and vi in [1,10]. These are arithmetic protection ranges, not a claim of numerical qualification throughout those intervals. Their positive lower bounds protect the first division; after that, alpha and each Newton denominator are checked before use as divisors.

The first guard loads only u32 values, checks raw exponent masks and padBits, and rejects an all-ones exponent before creating any f32 value from U/f0/vi. This covers the proposed NaN/infinity input controls without first loading them as floating-point data. The host should write their explicitly frozen uint32 encodings, not rely on a language's chosen NaN payload. Only after those integer checks pass are the three finite fields reinterpreted as f32; negative/range controls then reject before division.

Subsequent checks reject nonfinite alpha/intermediates and roots outside [0,1]; no value is clipped back into range. These checks are diagnostics on the bounded experiment. WGSL's finite-math and subnormal rules still apply; they are not a portable exception mechanism for arbitrary inputs. A tiny positive subnormal U can have zero-like or invalid behavior under permitted flush-to-zero rules. A positive alpha check alone also does not establish that the written reciprocal `1/alpha` cannot overflow before `min` selects its result. The actual selected positive inputs need a frozen host admission bound that excludes this case; the draft does not silently replace the original initialization or claim coverage of every positive representable U in [0,128].

## Source correspondence

The inspected source is M28 `outputs/milestone-28-source/aero.cjs`, `effectiveThrust` (retained in public base `c591ce2b195fa01b895d4ba881a44a4b92fdd703`), 4,259 bytes, SHA256 `710b0a8f0df62208e3385ac9b8288240b379fe9248a1a645251a77c533f24a62`. The initial uncompiled draft used an f32 input struct; its 3,124-byte source is retained as `m31-receiver-f32-v0-float-input.wgsl.txt`, SHA256 `27f41f25076d65142d8d1a73855b32c2a9b1d509aa27a78e87ab22e44ba21b8f`. Static review required raw-u32 input so invalid NaN/infinity controls are checked before any float reinterpretation. This revision changes only input guards/aliases and pad validation; valid Newton math is unchanged. The port retains:

- `alpha=U/vi`, initial `min(1,1/alpha)`;
- `next=x-(x*x*x+alpha*x-1)/(3*x*x+alpha)` with the same written multiplication/addition grouping;
- at most 12 Newton steps, testing `abs(next-x)<1e-15` before break and assigning `x=next` in either branch;
- `f=f0*x`, with no `pow`, explicit `fma`, clamp or replacement solver.

The selected scope intentionally uploads vi rounded from the original fixed binary64 vi0 instead of calculating `sqrt(f0/(2*rho*area))` in the shader. It therefore excludes the square-root/constant-construction port. Q64 must use the exact decoded uploaded f0/vi, while R64 retains the original constants; comparing both separates this representation choice from shader Newton arithmetic. General nominal=0 behavior is outside the selected scope and rejects because f0 must be positive in the declared range.

U=0 bypasses all division and returns x=1, f=the uploaded f0, alpha/residual/iterations/step=0 and stopCode=0. Exact identity is relative to the uploaded f32 f0, not an assertion that it equals the original binary64 nominal thrust. No signed-zero preservation claim is made.

WGSL may reassociate or fuse operations despite the source grouping, and the literal `1e-15f` is evaluated under WGSL's f32 rules. This is source-expression correspondence, not bitwise CPU emulation or a guarantee of IEEE round-to-nearest execution. See W3C WGSL, dated 2026-09-21, §§15.7.2–15.7.5 and 17.5.32, [specification](https://www.w3.org/TR/2026/CRD-WGSL-20260921/).

## Output interpretation

| stopCode | Meaning | iterations / finalAbsStep |
|---:|---|---|
| 0 | Zero-U identity | Both zero |
| 1 | The written strict threshold test succeeded | 1–12; saved final absolute step may be zero or nonzero |
| 2 | All 12 updates completed without that test succeeding | 12; saved final absolute step |
| 3 | Input or intermediate guard rejection; no root result | Both zero; all other fields zero |

Iteration counts and codes are integers exactly represented in f32. Code1 means threshold termination; it must not be labeled exact stagnation unless the saved finalAbsStep equals zero. Even zero step may reflect rounding/flush behavior. Code2 is an outcome, not automatic numerical failure: acceptance depends on independently frozen root, rotor-thrust and residual checks. Code3's x=0 is a sentinel, not a root or a replacement estimate.

`reportedResidual` is the signed f32 result `x*x*x+alpha*x-1` at the final saved x and alpha. It is not an independent residual or interval certificate. Readback review must recompute a binary64 residual at those exact saved values and compare the root against independently bracketed bisection at the same alpha, then separately compare the delivered force against the original-input reference. The host must retain input identity and all output bytes, not merely aggregate errors. The compact layout loses which intermediate guard rejected; if that becomes necessary, a separately frozen integer diagnostic binding would be clearer than reinterpreting slot7 after exposure.

Static source reading and text-file creation only. No import of scientific modules, shader compilation, GPU execution, browser launch, scientific numerical evaluation or new permission/budget opening occurred.
