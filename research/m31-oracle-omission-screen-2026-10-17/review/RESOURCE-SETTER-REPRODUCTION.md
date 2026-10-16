# Harmless resource-setter diagnostic

This was exploratory operational diagnosis after the failed launch, not a preregistered scientific result. The three exact requested setter calls were each run once in a fresh pinned Python subprocess with a5second parent timeout, isolated mode and bytecode disabled. No project module or research input was imported. Output is RESOURCE-SETTER-DIAGNOSTIC.json; all subprocesses exited0 because the diagnostic caught and recorded setter exceptions. No stderr was emitted.

For each named constant below, the child read `resource.getrlimit`, attempted `resource.setrlimit`, and either read back the accepted pair or recorded exception type/message:

| Constant | Requested soft/hard | Observation |
|---|---|---|
| RLIMIT_CPU |60,61seconds|Accepted; readback60,61|
| RLIMIT_DATA |536870912,536870912bytes|ValueError: current limit exceeds maximum limit|
| RLIMIT_FSIZE |16777216,16777216bytes|Accepted; readback matched|

Immediately preceding read-only inspection reported soft/hard9223372036854775807for all three and RLIMIT_AS. `sysctl kern.maxdsiz kern.maxssiz` returned unknown oid for both; those queries provide no maximum-size estimate. No attempt was made to search for an accepted data-limit value. These observations localize the failed setter on this host; they do not characterize all macOS systems or the research algorithm.

The actual dispatch used tool `require_escalated`, which was authorized under the standing research brief. This label is an attestation, not an OS detector. The separately allocated renewal omits the unsupported data setter and states its weaker, observational memory acceptance policy explicitly. The old failed launch remains closed.
