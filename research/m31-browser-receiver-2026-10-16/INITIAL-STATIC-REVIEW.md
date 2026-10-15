# Static review of the unexecuted browser receiver draft

Date: 2026-10-16 Shanghai. Reviewer: m31_evidence_audit. Campaign: research/m31-browser-receiver-2026-10-16 under <REPOSITORY_ROOT>.

This review inspected source/config/design text and the dated WGSL specification. It did not import a scientific module, compile or parse the shader, create a browser/GPU context, dispatch work, solve a root, generate scientific inputs, or run a checker. No repository source was edited. The new driver and protocol were not yet available in this snapshot; no final launch clearance is given.

## Inspected source snapshot

| File | Bytes | SHA256 |
| --- | ---: | --- |
| source/receiver.wgsl | 3124 | 27f41f25076d65142d8d1a73855b32c2a9b1d509aa27a78e87ab22e44ba21b8f |
| source/browser.js | 3865 | fde4f5920a4a5a6a200b9ffe41898bd5f29e2702efb5479bf6edb4e8858e1767 |
| source/reference.cjs | 796 | 4628e2a3a4d843868810bea070153fe22798cfe3e73fd483492ca329558d497d |
| config.json | 1742 | 1b93c0616228efe0e3c1923e9a35cb96c9cb0980d39a5f16f1ecff3e9d35cddf |

The zero-screen predecessor remains closed at the coordinator-supplied published commit cefe6c7bb47362e90135179d22a9721b6f03bb88. Its reused inflows are exposed reference evidence, not new full-flock holdouts. Its prior precision and cost outcomes must not be reinterpreted by this experiment.

## Findings requiring resolution

**1. Inspect invalid uploaded bits as integers before floating-point interpretation.** The current ReceiverInput fields are f32, and finiteBits takes a floating value before bitcasting it to u32. That is a weaker contract than the planned explicit quiet-NaN/positive-infinity guards: exceptional values have already entered the floating-point expression domain. Use a u32 storage input structure with the same four-word/16-byte layout, inspect original exponent masks as integers, and bitcast only finite admitted words to f32. Reject invalid records with the full status-3 record before any floating arithmetic. The padding word's required value should also be frozen, even if it is semantically ignored.

This recommendation follows the dated [WGSL specification, §15.7.2](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#floating-point-evaluation), which permits finite-math assumptions, read together with [§17.2.1, bitcast](https://www.w3.org/TR/2026/CRD-WGSL-20260921/#bitcast-builtin). Integer inspection avoids depending on preservation of exceptional floating values. The source change is a static prevention of that dependence, not evidence of an observed adapter failure. Host validation of actual returned raw output words remains necessary; intermediate finiteBits checks are not a portable physical/numerical certificate.

**2. Enforce deadlines outside the mapAsync race.** The browser's timeout currently races only read.mapAsync. After that race resolves, a still-pending popErrorScope is outside its rejection effect: a later timer can destroy the device but cannot reject an already-resolved race. Initialization also awaits adapter/device/compilation/pipeline promises without a local deadline. The final driver must enforce a complete-operation deadline around initialization and each entire dispatch/readback/error-check operation, plus an independent external process/browser watchdog within 180 seconds. An asynchronous Promise race is not enough if the page/browser becomes unresponsive; the external supervisor must terminate the owned process group. A timeout or lost device is terminal, with no adapter/kernel/backend fallback or retry.

**3. Complete the host contract before freezing.** Browser input validation currently checks only nonempty length divisible by four; Uint32Array otherwise coerces values. The driver must supply and retain validated uint32 words, exactly four per record, with fixed byte order and declared invalid bit patterns. It must retain every raw returned word before comparison, require count=n and exactly eight output words per record, and distinguish unavailable/unsupported hardware, shader compile error, validation error, device loss, timeout, numerical rejection and successful qualification. The browser returns shader text on a successful initialization; the driver must reconcile the actual shader with the frozen source before dispatch. Browser/API/build/OS/adapter metadata and diagnostic messages must be saved even when initialization fails.

Items 2 and 3 are requirements for the pending driver/protocol, rather than a claim that those currently absent files are defective. Item 1 is a specific source change needed in the inspected shader.

## Numerical expressions and required interpretation

The shader spells the M28 receiver update as x=min(1,1/alpha), followed by at most 12 updates with numerator x*x*x+alpha*x-1 and denominator 3*x*x+alpha. It retains the source-level multiplication/addition grouping, zero-inflow identity and final f0*x multiplication. It introduces no pow, clamp, alternate root formula or explicit fma intrinsic. This source match is not a guarantee that a WGSL compiler preserves identical rounding or avoids fusion/reassociation; the dated language permits behavior different from a sequence of JS Math.fround operations.

The output contains alpha, x, f, reported residual, iteration count, stop code, final step magnitude and reserved word. Every in-range invocation first writes the complete invalid record, and every completed valid path replaces it with a complete record. Extra workgroup lanes return before writes. This supports explicit coverage/status checks, but the host must check them.

The 1e-15f step threshold is inherited source logic, not an f32 accuracy certificate. Stop code 1 can indicate floating-point stagnation. Stop code 2 means the 12-iteration limit was reached. Neither label alone qualifies accuracy. The protocol must specify whether a limit result may pass only when all independently evaluated numerical gates pass, consistent with the unchanged capped solver. Require code 0 only for the direct zero case with zero iterations and exact uploaded nominal force; code 1 with 1..12 iterations and matching step semantics; code 2 with 12 iterations; code 3 for each designated invalid record and no valid records. Finite/range/root-error/residual/power gates remain independent of shader residual and stop reporting. Shader residual is a diagnostic, not an oracle.

reference.cjs contains a separate monotone bracketed solver with no production or GPU imports. For alpha=0 it returns the exact x=1 identity. For positive alpha it bisects [0,1] up to 96 iterations or width<=2e-15, using its own binary64 polynomial evaluation and returning alpha/x/lo/hi/iterations/residual. The comments correctly call these numerical brackets, not directed-rounding interval certificates. Caller checks must enforce finite values, ordering, width, iterations and residual; the helper alone does not throw when the final diagnostic tolerance is missed. powerRatio is the nondimensional closure x*(alpha/2+sqrt(alpha*alpha/4+x)); it is not a measured shaft/electrical-power model.

## Required error attribution in the pending driver

For each valid record, retain the original U/constants and R64 result; the uploaded uint32 bits and decoded Uq/f0q/viq; Q64 at the host binary64 quotient Uq/viq; actual shader alpha/x/f; and A64 at that actual returned shader alpha. Existing saved I rotor results can supply R for the reused inflows; only the 32 new scalar R roots are reserved. Do not rerun an old full field or receiver reference unnecessarily.

The signed force decomposition should retain:

- representation: fQ−fR;
- shader division: fA−fQ;
- iteration/root: f0q*xG−fA;
- final multiplication: fG−f0q*xG;
- delivered total: fG−fR.

These telescope algebraically; retain the small scalar reconstruction residual and worst-record witnesses. Do not compare G only to Q/A and omit total original-reference error. xG versus the independent A root isolates iteration error after actual shader division; alphaG versus Uq/viq measures division separately. A host residual evaluated at xG and alphaG checks the solved polynomial rather than trusting the shader's residual.

Freeze which alpha enters representedPowerRatio. A power check using only alphaG is a shader-alpha closure check and excludes division error. For the represented-input closure use decoded Uq/viq; an additional alphaG power diagnostic may be labeled separately. Separately rounded f0q and viq need not satisfy the original density/area derivation exactly, so a normalized represented closure must not be mislabeled as the old physical-constant power identity.

The new 1e-7 N rotor total budget is a distinct prospective engineering criterion for this receiver stage and these declared records. Preserve original 1e-12 N differences/counts as diagnostics; do not claim the new budget inherits or repairs binary64 precision qualification. A new-budget pass would not establish physical adequacy, wake-field accuracy, orientation/load-assembly accuracy, trajectory accuracy, speed or 5,000-drone browser simulation.

## Byte layout, adapter and reservation arithmetic

Four scalar input words have 4-byte alignment and 16-byte stride; eight scalar output words have 4-byte alignment and 32-byte stride. Replacing input fields by u32 preserves these sizes. The host allocates input STORAGE|COPY_DST, output STORAGE|COPY_SRC and readback COPY_DST|MAP_READ, submits the copy after compute, maps the readback, copies its uint32 words before unmapping, and destroys buffers in finally. This is a coherent raw-word transport path when the driver validates actual lengths and byte order. No evidence here establishes a device implementation's execution.

The browser requests one high-performance adapter and accepts only an explicit isFallbackAdapter===false, using adapter.info with the older property as fallback. An absent or fallback flag produces unsupported status; this is intentionally conservative and must not be silently replaced with software or another backend. Adapter limits/features are recorded. The driver should verify the actual device's resource support and preserve unavailable/unsupported outcomes. All current batch sizes are small relative to ordinary WebGPU limits, but that expectation is not permission to skip admission and validation diagnostics.

The declared records give:

| Batch | Valid roots | Invalid records | Input bytes | Output bytes | Workgroups at 64 |
| --- | ---: | ---: | ---: | ---: | ---: |
| scalar32 | 32 | 0 | 512 | 1,024 | 1 |
| invalid5 | 0 | 5 | 80 | 160 | 1 |
| fresh1000 rotor records | 4,000 | 0 | 64,000 | 128,000 | 63 |
| fresh5000 rotor records | 20,000 | 0 | 320,000 | 640,000 | 313 |
| Total | 24,032 | 5 | 384,592 | 769,184 | 378 |

There are 24,037 input records, 1,153,776 core input/output bytes and 24,192 dispatched lanes, of which 155 are out-of-range lanes that perform no root. The GPU root iteration reservation is 24,032*12=288,384. Host Q and A each reserve 24,032 roots, plus 32 scalar R roots: 48,096 total, with 48,096*96=4,617,216 bisection iteration slots. No field evaluation or integration step is reserved. No warmup, timing comparison, extra diagnostic dispatch or alternate solver is allowed by this matrix.

Raw total is capped at 32 MiB, including a 2 MiB failure reserve. Core bytes fit, but full per-record Q/A/R diagnostics and JSON framing must still be counted from the final schema. Unknown serialized size may terminate the campaign; it cannot justify dropping records or increasing caps after exposure. Exact attempted-call/record/iteration reservations, ordered batch completion and failure witnesses remain required in the pending driver.

## Disposition

Hold final freeze/launch until raw-u32 invalid inspection is resolved and the driver/protocol/schema/supervisor are reviewed for complete error attribution, raw byte retention, stopping certificates, exact reservations, adapter failure behavior, time/storage bounds and sole-invocation closure. This note is a static review artifact only. It authorizes no science, shader compilation, browser launch or checker execution. Earlier campaigns remain terminal.
