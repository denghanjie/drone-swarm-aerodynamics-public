# Smaller saved evidence, with exact reconstruction

The fixed saved-data experiment passed. All **156 selected records** preserved the original tree's absence/null/object state and reconstructed every saved tree value exactly. Both retained 5,000-drone H trees used about **78% fewer encoded bytes**, exceeding the preregistered target of at least 50% savings.

This resolves one demonstrated storage problem on the exposed records. It does not complete the earlier browser flight experiment, establish that a whole future run fits, or establish aerodynamic validity or speed.

## What we did

The tree records are an audit trail of which drone interactions the spatial search kept or skipped. Smaller records let us retain more evidence. This experiment does not measure whether the force calculation itself becomes faster.

The previous browser probe stopped while saving its evidence. We retained that failure and used only already saved data to test a smaller representation. Repeated labels became columns; source-index lists used whichever of literal lists, runs or bitmaps had the lowest fixed encoded cost. Every numerical word, list order, cull and tree property remained reconstructable. These are established storage techniques, with no novelty claim.

A JavaScript encoder wrote the representation. An independent Python checker compared reconstructed values with all selected original trees. It also passed one positive and sixteen specific rejection controls. The encoder's eight fixed controls passed. Neither program ran new flight, native aerodynamic queries or reference calculations. Non-tree fields stayed in the unchanged input records.

| Saved tree | Original encoded bytes | New encoded bytes | Reduction |
| --- | ---: | ---: | ---: |
| 5,000 drones, first stage (journal 60) | 43,030,681 | 9,498,259 | 77.927% |
| 5,000 drones, second stage (journal 63) | 43,040,079 | 9,499,571 | 77.929% |
| All 156 selected tree fields | 101,342,629 | 23,162,035 | 77.145% |

The 156 selections contain 52 absent, eight null and 96 object-valued tree fields. The total is logical encoded tree size, not whole-run disk use, RAM or timing. New distinct shards use 23,159,547 bytes and 104 descriptors use 50,420 bytes, giving 23,209,967 bytes of new evidence. Final result files total 23,389,312 bytes; the two private logs are empty. Existing 122,408,637 bytes of immutable selected inputs remain retained and are excluded from the new-write budget. No old data was deleted to realize these savings.

The single supervised attempt completed in about 41 seconds before final report/exit; the external process exit was observed as code 0. It stayed inside its 300-second and 64 MiB allocations, and source/input/output preservation passed. The supervisor's pre-final byte count is 553 bytes smaller than the final results because its own final ledger grew; both figures are retained.

## What you can see

The [updated Three.js inspector](viewer/index.html) shows the original three recorded scenes and five available states, now with checked storage figures. The 5,000-drone scene remains an initial captured state, not a new evolved flock. Its five receiver choices reveal the actual saved retained candidates and omitted groups. No new trajectory or interpolation was added.

The corrected UI check passed 55 checks and 25 receiver selections on desktop/mobile, including exact saved positions, source-bound byte figures and missing/corrupt-data handling. The first UI test failed because its pin comparator incorrectly depended on JSON field order; that failure is preserved alongside the corrected test. Scientific evidence and viewer geometry were unchanged.

## Research implication

A more economical audit record is now qualified on these development inputs. The next meaningful checkpoint should complete an independently checked fresh browser computation under an admitted whole-run storage/time budget. It should then test useful multi-step coupled flock motion and complete cost, with held-out scenes reserved before tuning. Physical validation requires suitable measured force/flow data and remains a separate unresolved gate.

The original failed browser experiment remains failed. No 5,000-drone numerical qualification, real-time performance, physical accuracy or publishable novelty follows from this storage result. See [claims](CLAIMS.md), [independent evidence review](review/RESULT-EVIDENCE-REVIEW.md), [operational review](review/OPERATIONAL-RESULT-REVIEW.md) and [next experiment](review/NEXT-EXPERIMENT.md).

Source commit: `b19aadc9a4157ad7c2bcba67856baf1d0c9096c6`. Source manifest: `eb7d1fda53791a919d64b06590299276f91f67afbaf9d444c219ffff829b368f`. Exact-public verification preceded execution. The overall goal remains active and incomplete.
