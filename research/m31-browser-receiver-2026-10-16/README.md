# Browser GPU rotor arithmetic: a limited component pass

The independent saved-data review confirmed that the browser GPU returned all **24,032 valid rotor forces within the frozen 1e-7 N error allocation**, and rejected all five invalid controls. The largest force error was **8.564453909953862e-9 N**, about 8.56% of that allocation. This is encouraging for a GPU implementation of this one equation. It is not a speed result, physical validation or evidence of novelty.

The older **1e-12 N comparison failed for 24,022 of 24,032 inputs**. Both outcomes are retained. Choosing a separate engineering budget does not make this implementation interchangeable with the binary64 reference at the old precision.

[Open the Three.js evidence view](viewer/) · [Original Boids flock replay](../../outputs/milestone-31-lab.html) · [Frozen protocol](PROTOCOL.md) · [Claims](claims.md) · [Independent review](INDEPENDENT-SAVED-REVIEW.md) · [Reproduce](REPRODUCE.md)

## What we did

The existing simulation computes rotor thrust from incoming air speed. We translated that scalar calculation literally to WebGPU binary32 arithmetic and ran it in the installed Chrome browser. There were 32 fixed scalar probes, five invalid bit-pattern controls, and 24,000 rotor inflows from two already published numerical inputs. Those old inputs were openly reused; they are not new holdouts or new drone flights.

Three independent reference paths distinguish original-input force, the force after rounding the inputs, and the force at the GPU's returned division result. Saved operands then separate input/constant packing, division, root arithmetic and final multiplication. The references used bracketed binary64 bisection. Numerical brackets are not rigorous directed-rounding interval proofs. The new allocation is a chosen engineering target, not an experimentally established flight tolerance.

## What happened

| Batch | Valid inputs | Maximum force error, N | New gate failures | Old precision failures | 12-update records |
|---|---:|---:|---:|---:|---:|
| scalar32 | 32 | 7.8532464698e-09 | 0 | 32 | 30 |
| fresh1000 | 4000 | 7.2060424849e-09 | 0 | 3998 | 3600 |
| fresh5000 | 20000 | 8.5644539100e-09 | 0 | 19992 | 18000 |

All three batches also passed their separate root-isolation, independently evaluated polynomial-residual and represented-power checks. Five invalid inputs produced the specified rejection sentinel. Complete raw input, GPU word and reference arrays are retained under `raw/`; checksums and source identities are in the manifest and run records.

Of 21,631 positive-input records, **21,630 reached the 12-update cap**. One met the strict step threshold. The other 2,401 records had zero inflow and used the identity path without Newton updates. A stopping label alone is not an accuracy certificate. We did not save intermediate iterates, so these records do not establish oscillation, stagnation or the effect of compiler reassociation. The criterion was not changed after observing this result, and its performance cost was not measured.

## What this means for the research

The result supports continuing to the next numerical component: pair geometry and wake terms, followed by accumulation. That next test must separate original geometry from its packed representation and separate errors in individual terms from errors in adding those same terms. It must be frozen and reviewed before execution. This checkpoint computes no wake field, source sum, body/world GPU assembly, controller or moving flock.

The Three.js update reads exact saved poses and GPU forces, with checksum validation, drone selection, all four rotor values and scalar error attribution. It is a static evidence view. The linked historical M31 replay supplies the actual local 3D Boids behavior; those missions had airflow off, and their original trajectory-refinement failures remain unresolved.

The original [eight-step roadmap](../../outputs/research-roadmap.md) remains intact. This work checks a small part of Step 6 (acceleration) while Steps 7–8 (large coupled simulations and a defensible contribution) remain open. Physical receiver/wake validation also remains open; the model's ideal actuator-disk power is not measured shaft or electrical power.

## Provenance and resource accounting

Source commit: [`4f2ead30ce48e4845ceefc105f9796ce468d907e`](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/4f2ead30ce48e4845ceefc105f9796ce468d907e). Freeze SHA256: `ad64a3f092d08045e1233fa9e05a4db72cda3ae8b5db039dec329f7628f8e7ae`. Independent GitHub retrieval matched the exact freeze bytes and all 51 local pins before execution.

One scientific invocation: 2.982534083 s external wall time, 820,902 runtime checks, four dispatches, 48,096 new host bisections and 2,121,357 actual host iterations. The run retained 36 raw files / 5,028,952 bytes. These are resource-accounting observations, **not a timing comparison or throughput benchmark**. Chrome reported version 155.0.8059.40 and a nonfallback Apple / metal-3 adapter; device/description strings were empty. This single environment does not establish portability.

Both Node and browser groups were confirmed absent after normal closure; no supervisor kill was needed. The dormant identity-check/kill branch was statically reviewed, not failure-injected. Ordinary process supervision has the non-atomic limitations disclosed in the protocol.

Independent saved-only review and final publication status are recorded separately in [INDEPENDENT-SAVED-REVIEW.md](INDEPENDENT-SAVED-REVIEW.md) and [POSTRUN-RESTART.md](POSTRUN-RESTART.md). Frozen prospective documents retain their original wording as historical records.
