# Browser wake arithmetic: a preserved accuracy failure

**The GPU computed all requested contributions, but one of 16 rotor cases exceeded the predeclared error allowance.** The experiment stopped before its final addition stage. The independent saved-data review confirmed the same failure, with zero evidence-integrity errors.

We asked whether a browser GPU could calculate the incoming airflow from 5,000 source IDs at four selected receiving drones. We kept the individual contributions so a good-looking total could not hide opposing errors. The first check rounded the inputs only; the second included the GPU's arithmetic. Both used the same declared numerical wake model.

The original binary64 reference reproduced the previous saved reference. Input rounding and all 16 control records passed. All 80,000 GPU records were finite, complete and matched the reference's policy classes. Only 388 records were positive; most source/rotor pairs contribute exactly zero under this model. All four rotors of receiver 4500 remained zero, as the fixed selection required.

At receiver 988, rotor 3, the sum of absolute contribution errors plus the reference allowance was **0.000026080175808988906 m/s**, above the preset **0.000018270441835956964 m/s**. The other 15 rotors passed that term check. The failed case's signed total contribution error was0.000025468264261715474 m/s, so cancellation did not hide this particular failure. This signed quantity uses exact sums of stored terms; it is not an executed GPU reduction.

The rule required term accuracy before addition. Consequently the serial addition dispatch, its 16 sums and the combined error gate were **not executed**. No threshold was relaxed and no run was repeated. Passing a numerical reference check would still not establish that the wake model predicts real drones accurately.

The separate review completed 326,768 integrity checks and 4,677,795 scientific checks in 2.15213425 seconds, reproducing the single failed gate. Review success means the evidence is faithful; the scientific acceptance test remains failed.

## What this changes

The preceding receiver component passed its separate force-conversion budget. This wake component failed its own chosen budget. The composed pipeline is therefore unqualified. A next experiment should investigate the source of this numerical discrepancy; changing only the final summation cannot retroactively satisfy the failed term gate. The reports separate input packing from GPU arithmetic, but do not isolate coordinates, axis rounding, constants or individual arithmetic operations as the cause.

This remains Step 6 implementation verification within the original eight-step roadmap. Genuine local 3D Boids behavior is preserved in the [historical M31 replay](../../outputs/milestone-31-lab.html), whose airflow was off. The [new Three.js evidence view](viewer/) shows saved synthetic geometry and this run's contributions. It is static inspection, not a new flock flight or a speed benchmark.

## Evidence and scope

- [Frozen protocol](PROTOCOL.md), [source freeze](freeze.json), [source commit4767787](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/4767787487fc7f8c3a8e8189523b1299c9c7f190).
- [Raw driver report](results/result.json), [term assessment](raw/terms-assessment.json), [external budget](results/budget.json), [schema](schema.json) and [reproduction notes](REPRODUCE.md).
- [Claim ledger](claims.md), [literature ledger](RESULT-LITERATURE-LEDGER.md), [independent review](INDEPENDENT-SAVED-REVIEW.md) and [restart](POSTRUN-RESTART.md).

The single attempt took 1.882813459 seconds externally, including references, setup, transfers, persistence and cleanup. This is resource bookkeeping, not a matched performance measurement. There were two dispatches,80,064 launched lanes including 48 padding lanes,51 raw files totaling 29,738,085 bytes, no timeout and no surviving registered process groups. Reduction was never launched. Chrome 155.0.8059.40 used a nonfallback Apple metal-3 adapter; exact GPU model was unavailable.

These 16 deterministic rotor cases were deliberately selected from exposed records. They are not independent population samples, held-out confirmation or full-fleet qualification. No uncertainty interval would justify population inference here. This test supplies no physical validation, end-to-end speedup, real-time result, portability result, novelty finding or publication-ready contribution. The chosen allowance is an engineering allocation within the model, not a measured physical tolerance.

## Every retained rotor case

Values below are rounded display summaries of exact integer certificates in the raw assessment. The acceptance gate adds the frozen 1e-12 m/s reference allowance and compares exact dyadic integers. Display rounding does not determine pass/fail.

|Receiver|Rotor|Positive terms|Input packing L1 m/s|GPU vs packed L1 m/s|GPU vs original L1 m/s|Preset term gate|
|---|---|---|---|---|---|---|
|27|0|30|4.1734622e-06|7.95264661e-06|1.11107154e-05|PASS|
|27|1|30|4.29998362e-06|4.59949879e-06|7.51047012e-06|PASS|
|27|2|31|4.83333769e-06|7.27391275e-06|4.69249683e-06|PASS|
|27|3|29|3.88116521e-06|4.20543269e-06|3.29619721e-06|PASS|
|445|0|44|6.64719925e-06|1.09858316e-05|1.24229966e-05|PASS|
|445|1|41|9.52105082e-06|1.27282616e-05|1.52102206e-05|PASS|
|445|2|39|6.83579504e-06|1.34158254e-05|1.34242847e-05|PASS|
|445|3|44|7.20189646e-06|9.4154073e-06|1.28496881e-05|PASS|
|4500|0|0|0|0|0|PASS|
|4500|1|0|0|0|0|PASS|
|4500|2|0|0|0|0|PASS|
|4500|3|0|0|0|0|PASS|
|988|0|25|6.29730066e-06|7.99315631e-06|7.58709158e-06|PASS|
|988|1|27|7.9575679e-06|1.25081185e-05|8.61103003e-06|PASS|
|988|2|25|9.32744554e-06|9.82455853e-06|1.73844075e-05|PASS|
|988|3|23|1.23970873e-05|1.52592897e-05|2.60801748e-05|FAIL|
