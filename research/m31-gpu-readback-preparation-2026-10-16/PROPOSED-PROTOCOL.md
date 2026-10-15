# Proposed actual-GPU readback boundary test

**Static preparation only. No execution allocation, launch-ready freeze or GPU result exists.** Independent source preparation began around the end of the overnight window. Finishing source work afterward does not extend the 2026-10-15 23:00 UTC diagnostic/saved-review launch window. Every previous terminal campaign stays immutable.

## Why this question comes next

Published result `468b980b94ad406257207767099ad06874ecfa73` supports one 3,840-byte ordinary-heap transfer and exact persistence. It never exercised GPU-mapped memory. Earlier numerical campaigns with missing saved output cannot establish what their GPU values were. A new, deliberately small integer fixture can isolate a prerequisite for collecting future numerical evidence without supplying missing old output.

Hypothesis: actual GPU-written bytes can be copied to independently owned ordinary memory while a staging buffer is mapped, then survive unmap and buffer destruction, one automation return and exact closed-file persistence. This hypothesis is untested. Success would support only this tiny fixture and admitted environment, not realistic aerodynamic transfer cost, general reliability, driver portability or physical validity.

## Fixed proposed fixture

32 unsigned 32-bit words, 128 bytes. Four prefix words, 17 active words and 11 suffix words. Initial word j is `0xD15EA5E5 XOR ((j * 0x01010101) modulo 2^32)`. Encode initialization explicitly in little-endian byte order. Dispatch three workgroups of eight invocations. An invocation with i >= 17 returns without writing; otherwise write storage word 4+i as:

`((((0x9E3779B9 * (i + 1)) modulo 2^32) XOR 0xA5A5A5A5) + 0x7F4A7C15) modulo 2^32`.

All 17 active values must differ from their original sentinel. All 15 padding words must retain their corresponding sentinel. The independent reference derives every expected word using integer arithmetic and explicitly packs little-endian bytes; it does not import producer shader code. This is a fixed public engineering fixture, not a fresh scientific holdout or a numerical aerodynamics reference.

## Proposed lifecycle and retained evidence

One admitted browser/device lifecycle, one compute dispatch, one staging copy and one payload-bearing automation call. No alternative extraction, HTTP sink, permission change, extra device or retry. Before requesting a device, record the bounded API-reported `adapter.info.isFallbackAdapter` as true, false or unavailable; admit only explicit false. No identifying adapter strings are needed. This is an API admission rule, not hardware attestation. Actual storage is initialized, GPU-computed and copied to a MAP_READ staging buffer. Await mapping, obtain the actual mapped range, copy its 128 bytes into a newly allocated ordinary Uint8Array while mapped, unmap, destroy both buffers, then convert only the owned copy to the return representation.

The returned bounded envelope reports page stages, mapped and owned lengths, GPU error observations and actual byte values. Page stage records are producer self-reports. External source inspection establishes intended ordering; independent returned/file byte equality establishes observed content. Neither independently observes every GPU API transition. A rejected or missing automation return cannot reveal an unreturned page stage. Map/device/error-scope failures must never be relabeled as byte equality or recovered through a second extraction.

Host validation rejects malformed envelopes before byte conversion. Validly encoded wrong bytes must remain available as the actual result; expected bytes must never replace them. Persist actual returned bytes exclusively, preserve partial writes, record close separately, and compare the closed file with the actual returned bytes and the independent fixture as distinct predicates. The previous host and process-ownership design is a reference only; no old worker may be imported or executed.

## Decisions that must precede execution

Resolve static review findings; verify exact API specification passages and the new source contract; integrate a new host driver and independent saved-evidence reviewer; define fresh execution/review windows and bounded budgets without reopening old allocations; pin runtime/source and fixture; privacy-review, publish and independently retrieve the exact source commit/freeze. In particular, verify the normative WGSL unsigned-arithmetic and memory-layout passages: the explicit modular/little-endian fixture is presently an adopted representation contract, not a newly verified specification claim. The future host evaluation allowance must exceed the page's full cleanup allowance with room for serialization and receipt; validation/persistence and independent external closure require their own remaining margin. Do not copy the old 10-second host race unchanged. The prior 60-second diagnostic/30-second review limits are design references, not adopted allocations for this package.

Predetermine failure classification for unavailable WebGPU/adapter, device creation/loss, compilation/validation error, map failure, detached-memory misuse, host timeout, malformed return, valid wrong bytes, persistence error and incomplete lifecycle evidence. Distinguish planned cleanup, reported page cleanup and externally observed process closure. A record-integrity pass must remain possible for a faithfully recorded failure; it cannot turn the failure into a successful readback.

Source parsing and pure reference/validator tests are preparation only. No shader compiler, browser, adapter request, GPU queue, operational worker or saved-evidence checker is invoked by this package during preparation.

## Connection to the research goal

This is one prerequisite for trustworthy numerical measurement, not the desired contribution. After engineering admission, realistic output sizes and matched cost accounting remain untested. Aerodynamic numerical-reference failures, physical-data compatibility and a useful approximation with fresh confirmatory evidence remain separate open requirements. The target remains genuine 3D local Boids, meaningful flight dynamics and mutual aerodynamics at 5,000 drones with a defensible accuracy–computation trade-off.
