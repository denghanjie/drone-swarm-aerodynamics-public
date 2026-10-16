**Renewal checker delta review — source only**

Decision: accept the inspected delta for separate prospective source publication of the renewed harmless qualification. This is a source decision, not a harness result or execution authorization supplied by the reviewer. The parent allocated the renewal after rechecking standing authorization. The expired package remains immutable and unexecuted; its cutoff has not been retrospectively extended.

Exactly ten source files were examined across the old and renewal packages, within the ten-file allowance. Work consisted of text diffs, targeted gate reading, byte comparisons, byte counts, SHA256 hashing and directory-existence checks. No interpreter, checker, runner, guardian, inert fixture, live process sample or scientific code was imported or invoked. No syntax-test execution is claimed for this delta review. Only this new review document was written.

**Exact delta.** The checker differs from the previously accepted 22,458-byte checker at exactly two lines:

* `CUTOFF` changes from `2026-10-16T23:00:00Z` to `2026-10-17T01:00:00Z`.
* The required package basename changes from `m31-launch-qualification-2026-10-17` to `m31-launch-qualification-renewal-2026-10-17`.

The config differs only in `cutoffUtc`, with the same new deadline. Complete byte comparisons establish that `run.py`, `guard.py` and `inert.py` are each identical between packages. The original checker/config and three copied files still have their previously accepted hashes. Both packages' results paths were absent when inspected.

The unchanged runner resolves its package and result paths from its own file location and reads its own config cutoff. The unchanged guardian/inert scripts are located relative to that package. The changed checker accepts only its own resolved package directory and the renewed basename, reads that package's config/manifest/publication receipt, and requires manifest members to lie under that exact package prefix. Thus the renewal uses a distinct package and source/publication identity; retaining the same format schema does not substitute an old allocation's identity.

**Gate consistency.** The checker compares the new config cutoff with its new `CUTOFF`. Its own launch gate, publication-verification deadline and recorded run-attempt chronology all use the corresponding new epoch. There is no residual old-cutoff comparison in the reviewed checker. Publication commit/manifest SHA, byte count, path, member count and verification flags remain required; current source pins, active Python binary pin and required source closure remain checked. Saved run/check artifacts stay bound to the new source commit, manifest and config SHA, runtime and declared execution context. Source, manifest, receipt, runtime and saved input pins are rechecked after validation. Exclusive checker attempt/report files and the 15-second alarm through ordinary report writing are unchanged.

The renewed package still needs its own final source manifest and exact publication receipt before any launch. This review did not fabricate or verify a not-yet-supplied receipt, repeat remote verification, or reread a separate renewal protocol. Final prospective protocol/publication completeness remains with the parent source freeze. The old late-publication receipt cannot satisfy a manifest path and source-pin prefix for this renewal.

**Finite operational contract preserved.** The exact diff leaves all eight fixed cases, expected first failures, separate secondary missing-output facts, strict output sets, case/report/index pins and execution order unchanged. Positive leader observations and release observations retain supervisor-PPID binding and RSS consistency checks. Ready/sample/authorization/child-start order, delayed readiness, timeout threshold and actual timeout child exit, normal release versus forced cleanup, and two post-event absence probes retain their accepted validation. Limits remain one 60-second run, one 15-second checker, bounded cases/watchdogs, 128 MiB sampled RSS and 1 MiB results, with unchanged per-file caps.

No finite-case check or failure gate was removed to enable the new window. The checker still writes `scientificQualification:false`, `historicalRootCauseEstablished:false` and `scientificRerunAuthorized:false`. Execution context remains a saved caller attestation, not a sandbox detector. A later operational pass would not establish the earlier normalizer failure's cause, qualify the old supervisor, transfer to another environment or authorize a scientific rerun. No pass or measurement is asserted here.

**Ten-file pin inventory.** `old` expands to `research/m31-launch-qualification-2026-10-17`; `renewal` expands to `research/m31-launch-qualification-renewal-2026-10-17`. Each table entry identifies a distinct file. Both checkers/configs were compared by complete text diff; renewed checker identity/deadline/provenance gates were also read directly. Runner/guardian/inert pairs were compared as complete opaque bytes, relying on their previously accepted source review rather than reopening their execution semantics.

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `old/source/check.py` | 22458 | `ab70f93c4a00d69611ea5e2f4355b323accf8593ea1a1c3ef8f5d0f3a34b4bf7` |
| `renewal/source/check.py` | 22466 | `6f99d76bb374b8b397f40bdc2c08f950549fcbaadcb736eba7c6de279b7365a4` |
| `old/source/config.json` | 536 | `ae4eaeb165a1754cc4e81e8621f43d99290fe23f6c37a8f444fd29401fede6b7` |
| `renewal/source/config.json` | 536 | `d5ab7cd5f24885babcfc89a0d9f430162e2fd47a94b8f8340ebb67dc51c36d3e` |
| `old/source/run.py` | 12950 | `148de9f1da3f1ccf3a995f70b9f3b8158bd7b8927325483cdb970ef09de509dd` |
| `renewal/source/run.py` | 12950 | `148de9f1da3f1ccf3a995f70b9f3b8158bd7b8927325483cdb970ef09de509dd` |
| `old/source/guard.py` | 2862 | `18851920da041242f7df7f85f5782e7d0647a72e4d5831fdc7bad9c940e35e80` |
| `renewal/source/guard.py` | 2862 | `18851920da041242f7df7f85f5782e7d0647a72e4d5831fdc7bad9c940e35e80` |
| `old/source/inert.py` | 378 | `a48b286b39a3b3a80d703d842a7a3a3bec341da8c8f5c9ee8f76358af5324344` |
| `renewal/source/inert.py` | 378 | `a48b286b39a3b3a80d703d842a7a3a3bec341da8c8f5c9ee8f76358af5324344` |

The earlier package's **SOURCE ONLY — NOT RUN** status and the separate failed normalizer attempt remain unchanged. This renewal is a new bounded operational allocation with its own deadline and prospective evidence requirements.
