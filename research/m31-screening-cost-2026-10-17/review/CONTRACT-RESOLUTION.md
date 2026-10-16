# Contract resolution before source freeze

The parent accepted the source-only review and then authorized implementation of the independent streaming checker. `source/result-contract.json` is authoritative. `review/CONTRACT-DRAFT-REVIEW.md` and `review/RESULT-CONTRACT-DRAFT.json` preserve the earlier proposals; prefreeze copies preserve subsequent corrections. No scientific execution was used to settle these choices.

Accepted decisions:

- Six paired scene shards in frozen spec order; a small index and a durable event journal; first **measured** representative per method. Both warmups and all four measured pairs bind to those representatives.
- Full independent classification of every logical pair, including every implicit zero and every zero-node member; one live scene/oracle plus one method-local control copy; streamed reference evidence and explicit cache release.
- Warmup `AB`, measured `AB, BA, BA, AB`; monotonic global trial intervals and `prepared/spatial/assembled/completed` offsets; exact stage partition; separately scoped harness cost.
- Printable-ASCII canonical JSON. Scientific digest envelopes use canonical bytes **without** newline. Saved runner index, scientific/anomaly shards and each journal event use canonical JSON **plus exactly one newline**; raw file pins include it. The saved checker enforces this encoding for the successful index/shards/journal. Independent checker output uses canonical JSON bytes and raw pins.
- Domain/context keys fixed in the final contract; whole method hashes include proof/work/status/branch. The common positive projection is exactly `{i,r,j,coefficient}` in canonical order with stable IDs.
- Exactly 15 new controls with deterministic first witnesses and intended semantic failures. No old fixtures or controls run. Exact candidate-load identity preflight prevents the candidate-bit control from being hidden by a downstream row check.
- 8 MiB index and journal, 64 MiB each scientific/anomaly file, 128 MiB all science plus the single `results/anomalies/first-mismatch.json`, 96 MiB checker corpus, 16 MiB metadata/all private/public logs, 384 MiB aggregate. The stated static output envelopes depend on the frozen rounding/support and field-accounting proof; they do not prove RSS/time feasibility.
- 256-character limits apply only to enumerated exact fraction evidence, with no rounding or truncation. Candidate load records are limited to 12 KiB. Full root/load/error checks remain unchanged.
- If the full first-mismatch record cannot fit, emit an explicit `anomaly-retention-resource` failure with bounded digest and required/available byte evidence; claim neither full anomaly retention nor success. No retry.
- Successful cost qualification requires all four normalized load tolerances for every method/scene. All paired ratios, duration medians, median paired ratio and ratio of medians are exact reduced rationals.

Implemented files, source lineage, review changes and syntax-only checks are recorded in `CHECKER-IMPLEMENTATION-NOTE.md`; exact reading is in `PROTOCOL-READING.json`. Source freeze/publication/exact remote verification and the separately authorized single kernel/checker allocations remain parent responsibilities.
