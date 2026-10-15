# Independent disposition of the saved M31 wake-slice review

The sole saved-evidence review faithfully confirms a negative scientific result. The review reports `status: consistent-recorded-negative` and `reviewPass: true`, while `fullSuiteQualified: false` and `firstFailedStage: terms`. A successful evidence review establishes that the recorded result and stopping behavior are consistent; it does not convert the failed numerical gate into a pass.

This disposition is based on the saved review report, saved runtime record, and already recorded assessment values. No checker was executed and no additional raw scientific arithmetic was performed in preparing this disposition.

The scientific source commit is `4767787487fc7f8c3a8e8189523b1299c9c7f190`, with freeze SHA-256 `5862d96e2556d58852f7b1d3a65e00e5303c8061e137f27280041156191c282f`. The receiver-selection SHA-256 is `00bfae2e0d0cc8cfc811556ea549fe69399d45882693b760f612e15f8daa125f`. The prepared slice exposes receivers 27, 445, 4500, and 988, with 5,000 sources and four rotors per receiver: 80,000 term slots and 16 potential rotor sums. The recorded exposure status is `partial`.

| Stage | Present | Complete | Passed |
| --- | --- | --- | --- |
| R: original binary64 reference | Yes | Yes | Yes |
| Q: decoded prepared-interface binary64 reference | Yes | Yes | Yes |
| Controls | Yes | Yes | Yes |
| GPU materialized terms T | Yes | Yes | No |
| Prospective serial GPU sums S | No | No | Unexecuted |

All 80,000 term records passed the recorded structural, identity, class, finite-value, and coverage checks. The report's term-coverage qualification describes valid records, not passage of the numerical L1 gate. The saved report records 388 positive terms overall.

The sole failed numerical gate is rotor-array index 15: receiver 988, rotor 3, using zero-based rotor numbering. That row contains 5,000 valid terms and 23 positive terms. Its saved displayed `L1(T−R)` is `2.6080174808988907e-05` m/s. The saved displayed `L1(T−R) + 1e-12` is `2.6080175808988906e-05` m/s, against epsilon `1.8270441835956964e-05` m/s. The exact integer/dyadic comparison determined failure; these displayed values are descriptive. The failed test is the conservative sum-of-absolute-errors allocation for term generation on this rotor.

The independent implementation reports 326,768 integrity checks and 4,677,795 scientific checks, zero integrity failures, one scientific finding, and no fatal error. It verified the 82 frozen source/input pins, 56 terminal core evidence pins, and three private provenance pins. Its saved checks cover reference links and allowances, exact policy and L1 gates, typed GPU records and controls, exact dyadic error and term-sum evidence, recorded counters and byte coverage, launch/API evidence, resource-ledger consistency, and the absence of a stage after the first failed gate. It did not import or copy the host assessment functions and did not reconstruct geometry, profiles, roots, or shader values.

The serial reduction was never dispatched because the term gate failed. Consequently, this evidence contains no executed GPU summation-error result and no combined final-gate result. It supports no full-suite, full-fleet, physics, force-composition, speed, portability, or flight claim.

The sole scientific attempt recorded two dispatches, for controls and main terms, with 51 raw files and 29,738,085 raw bytes. It recorded zero roots and zero integration steps, no timeout, and Node exit 1 due to the term-gate failure. Its resource records show both known process groups absent, zero kill signals, zero active ownership checks, and no cleanup errors. The external wall time `1.8828134589999999` seconds and driver wall time `1.515547417` seconds are bookkeeping measurements only.

The saved-review runtime records one attempt, exit 0, no timeout, no output-cap excess, an unchanged checker, an unchanged input index, an absent process group, and `qualifiedReviewClosure: true`. Its external wall time is `2.15213425` seconds and checker elapsed time before output is `2.0995155` seconds. The recorded output count before the runtime record is 138,044 bytes. The review limits were 60 seconds external, 59 seconds subprocess, 55 seconds cooperative, and 16 MiB of outputs including a 2 MiB failure reserve. The archived-file output-accounting correction was made before the sole review invocation; it did not constitute a review retry.

The immutable review identities used for this disposition are:

| Artifact label | SHA-256 |
| --- | --- |
| Saved review report (`review.json`) | `2e2c62b883df1ecc15418c424e9c731521400b53d71ee307cf8024c224a5d95e` |
| Saved review runtime (`launch/runtime.json`) | `76df357b535ea3f2e9b283a188caee4bf4dae30d9baffc3b9daf226901536571` |
| Saved review input index (`input-index.json`) | `ba00b67474e5f4c7ae9025c9aed960193384433b286aba4d6ac04e6b9b59d53a` |
| Independent checker (`checker.py`) | `1d546f28965f40785b6bdc426a9163c126710e2e3f65cf96a5cc0727663c335b` |
| Review launcher (`launcher.py`) | `8f150f4c038d0c3c24a8789d29c4231283c32b5190bd36a6a798f4544e0f93dd` |
| Review invocation (`invocation.json`) | `daa47238ece6bec85e8281f5dc03072aad64629fee092d10f10aa36c60cd392e` |
| Prelaunch output-accounting correction | `5bdd3e278f35d8b3c40aeb14178ca9b57b8b8bf7b78e7232ad4d84a36927619d` |

Private provenance contents, machine paths, process identifiers, and browser profiles are excluded from this public-safe disposition. Mutable publication and viewer packaging documents outside the frozen scientific inputs are not part of the scientific immutability claim.

Both the science budget and the saved-review budget are terminal and closed. No retry, checker modification, additional scientific execution, or further raw arithmetic is authorized by this disposition. The defensible publication outcome is faithfully reviewed negative evidence, with the serial stage explicitly marked unexecuted.
