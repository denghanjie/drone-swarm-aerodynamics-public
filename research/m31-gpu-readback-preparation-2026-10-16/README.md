# Preparing the GPU-to-file evidence path

We have tested saving a small payload from ordinary browser memory. The next question is whether actual GPU output can be copied safely before the GPU mapping is released, and then saved exactly.

This directory contains preparation, not a completed experiment. A tiny integer pattern makes missing computation, wrong byte order and overwritten padding detectable. It does not simulate drones or validate physics. The existing [recorded Three.js evidence viewer](http://127.0.0.1:8876/research/m31-control-channel-2026-10-16/viewer/) continues to show the completed earlier test; it is not evidence for this proposed GPU test.

The page, shader and strict validator are saved in `source/`; the independently derived fixture and byte predicates are in `review/`. Seventy page/validator preparation checks and 33 independent byte-predicate cases passed. Both implementations produced exactly the same expected 128 bytes. These are expected values, not GPU observations. The coordinator checked delivery hashes and compared the two fixture files directly without rerunning unchanged tests.

Read PROPOSED-PROTOCOL.md, STATIC-REVIEW.md and NEXT.md. No operational execution is allocated; the overnight launch cutoff remains unchanged. Previous source freezes, failures and skipped stages are preserved. The new host, external process supervision and full saved-file reviewer are unfinished; normative WGSL arithmetic/layout verification remains a prelaunch gate. The package manifest inventories static artifacts and is not a launch-ready source freeze.
