# Adopted cost-checkpoint contract

The finalized source/result-contract.json is the machine-readable prospective contract. It inherits the semantic method/prepared/input/tree/load interfaces from the closed exact-screening checkpoint, while replacing its run packaging, allocation, timing schedule and negative controls. Its schema and exact source bytes will be frozen before execution. The original review/RESULT-CONTRACT-DRAFT.json remains the first concrete proposal; subsequent choices are retained in review/CONTRACT-RESOLUTION.md and prefreeze history.

Raw input, method and cross-method common digests use the three distinct versioned domains in the contract. Canonical JSON is recursively ASCII-key-sorted, printable ASCII strings, exact safe integers, no floats/negative zero/undefined; arrays retain order. All duration fields are nonnegative canonical nanosecond strings. Raw-file pins hash exact file bytes, including their trailing newline; semantic digests hash canonical envelopes without an added newline. Source-manifest identity hashes its exact bytes; the manifest excludes itself.

The first measured representatives are global sceneOffset+2for complete and +3for hierarchy. The complete scientific objects are retained in one paired shard per scene. All60trial digests and independently reconstructed work bind to those representatives, including warmups. The independent checker validates scientific semantics before cross-method/digest binding so metadata cannot mask a targeted control failure.

The allowed anomaly is results/anomalies/first-mismatch.json, at most one globally. If a full anomaly exceeds64MiB or the remaining128MiB science+anomaly budget, close as explicit anomaly-retention-resource with bounded required/available/digest metadata. Do not truncate an alleged complete scientific artifact or retry.

Summaries are ordered by scene and have exact fields sceneId,pairs,completeMedianNs,hierarchyMedianNs,medianPairedRatio,ratioOfMedians. Every pair has repetition,pairOrder,completeNs,hierarchyNs,ratio. Fractions are reduced {n,d}canonical integer strings with positive denominator. Four-run medians are the exact arithmetic mean of the middle two sorted observations. Median paired ratio and ratio of medians are distinct quantities.

No numerical qualification is inferred from these source declarations. PROTOCOL.md defines allocation and interpretive boundaries; the independent semantic checker and targeted controls determine qualification after source publication.
