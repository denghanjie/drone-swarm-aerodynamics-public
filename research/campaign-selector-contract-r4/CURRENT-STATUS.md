# SELECTOR-CONTRACT-R4: terminally incomplete

**Eight nominal cases completed; the one-shot attempt then stopped.** The wrapper records `incomplete_or_blocked`. The ninth case, `json-4-initial`, has a last-durable checkpoint at `before-case-receipt`, but no completed case receipt. Count **8 completed, 1 interrupted, and 91 unreached** out of 100 planned cases. None of the 73 negative controls or four positive controls was reached.

A checkpoint temporary filename disappeared during storage accounting. Static inspection supports an enumeration-to-stat race with the checkpoint's atomic rename; the receipt contains no traceback proving which census call encountered it. The child was killed, and the attempt is terminal with zero retries.

[Milestone](postrun-report/MILESTONE.md) · [Sanitized actual-record evidence](postrun-report/EVIDENCE.json) · [Independent aggregate review](postrun-report/SEMANTIC-SUMMARY.md) · [Historical Three.js display with R4 outcome](postrun-demo/index.html)

The completed prefix does not establish a full selector-contract pass, negative-control coverage, audit equivalence, speedup, numerical accuracy, or physical validity. Read accounting and final full-input hashes remain incomplete. No simulation or new flight was produced.

These are new local presentation derivatives. Original R4 records are preserved. Detailed inventory publication is still awaiting approval; raw checkpoints, state arrays, private paths, and detailed input/runtime inventories are excluded. At preparation, no R4 publication had been made. The currently verified repository commit remains `5293fba9093179096963784aa8fe765238259eb4`.

The earlier R3 standalone HTML was built and delivered. Its historical replay remains separate from this R4 result. [Published R3 milestone at the verified commit](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/5293fba9093179096963784aa8fe765238259eb4/research/campaign-audit-successor-r3/postrun-report/MILESTONE.narrow.md).
