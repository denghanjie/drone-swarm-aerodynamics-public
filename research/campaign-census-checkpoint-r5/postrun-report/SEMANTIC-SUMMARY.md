# R5: bounded checkpoint-census check passed

The single prescribed attempt completed all **21 expected decisions**: 10 accepts and 11 expected control rejections, with no unexpected failure or retry. Independent review verified receipt order, all 9 scheduled actions, occupancy records and all 54 retained fixture files against frozen literal declarations.

For these fixed interleavings, reserving two bounded checkpoint slots avoided the stale-name failure, covered every declared occupancy and did not double-count the pair. Unrelated missing files and injected enumeration/type/link anomalies produced their required rejections. The stopped-writer case counted actual bytes separately from the live reservation.

At the production boundary, the live charge was 131,088 bytes: 16 ordinary bytes plus two 65,536-byte slots. The valid small terminal case counted 64 actual bytes while reporting its 128-byte live reservation separately.

## Measured scope

- Launch to child reap: 0.066656105 seconds; child CPU: 0.068349 seconds
- Child RSS high-water: 12,320,768 bytes
- Conservative instrumented-payload bounds: 330,834 bytes read and 152,936 bytes written
- Retention through the parent observation: 251,584 bytes, below the 300,000-byte normal limit

The attempt met its stated limits. Payload accounting excludes interpreter/runtime library I/O; memory assurance uses a software guard and process high-water check. Unit-test timings are not speedup evidence. Later reporting files are additional retention outside these execution measurements.

## Limits

The accepted result is only census_checkpoint_coordination_satisfied_on_fixed_interleavings_only. It assumes a trusted single writer, exactly two registered bounded slots and fixed unrelated files. It is not a general atomic snapshot or arbitrary-concurrency proof. Crash durability, adversarial writers and earlier-harness integration remain untested.

R4 remains terminal and incomplete; R3's failure is unchanged. No selector, model, audit, physics or scale claim follows. This aggregate derivative omits raw fixtures, private release/census details, source inventories and runtime paths. Public reproduction is incomplete. No new test ran during review.
