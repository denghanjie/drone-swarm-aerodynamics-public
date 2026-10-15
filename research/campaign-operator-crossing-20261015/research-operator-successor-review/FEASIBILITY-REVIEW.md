# Independent pre-execution review
2026-10-15. Static review only; no model imports or numerical runs. Consolidates prior record c8ec3383596379af006b2e780edf6c43454a3a50c308f7d483828240b0b0b5ea pre-execution.

## Identity and verdict
Protocol SHA256: 32545f3d96b85ab86353732fe876442cae87e6c24e91c00f99a77fa803ad8d37.
Reviewed code-set SHA256: 06eb30c45cd6f31d21f99adfe2b021dc0cd532ba1f5c3698af963e9ce56ecd59.
Code-set order: driver.cjs (15113 B), supervise.py (1150 B), SOURCE-MANIFEST.json (1204 B). Hash uint32LE(name/content byte lengths), UTF-8 name, contents per file.
Six sources total 20,997 B; size/blob/SHA256 match manifest and public source reads. Node syntax/Python AST checks passed.

PASS for prospective implementation, conditional on final admission and hash-bound release. Independent physics review also passed. No executed result or publication approval.

## Checked
- All four methods use scheduled samples only; integer alpha, hold/linear startup, raw quadratic shadows, per-rotor delayed cliff gates, degeneracy/ties and terminal diagnostics match protocol.
- Incoming scoring precedes sample acceptance; outgoing checks have zero integration weight. Original force closure and W/Wa norms retain all four rotors. Fine/coarse fixed-variant decisions are consistent.
- Checked analytic event brackets, packed labels and symmetry. Header bytes 40..47 retain maximum normalized roll.
- Binary layout: 64+10752+7040+2560+5584=26000 B. Absent rows and partial status/progress are marked. Witnesses cannot certify every dense maximum; rerun needed.
- Separate field/kernel/source-zero/crosscheck counts; 3,968 shadows, 3,952 decisions, 16 terminal diagnostics; 528,016 load calls plus 2 identity calls. Newton work is a bound, not measured FLOPs.
- Verified fixes: no oversized-local-source storage credit; field calls counted before invocation; short writes rejected; release argument validated; partial evidence periodically fsynced; no-retry files and bounded supervision.

## Admission and limits
Admission SHA256: 52fa2d836ed86ca39e5d725f6ddf6972a8981df771969f958d6aa862f954eccd. It supersedes nominal slots: other primary 57,000+evidence 30,000+viewer 3,000=90,000 B; ZIP 75,000/receipts 15,000/growth 180,000 B. Historical 199,751,910 B remains charged.
ZIP omits only six unchanged public sources, still retained locally: 69,003+4,954+up to 1,000 receipt bytes=74,957 B, within declared entry/name limits. Rerun needs pinned source; viewer needs existing Three.js. Fail closed on missing/mismatched source. Not standalone.

Driver clocks omit admission/final-write work; supervisor clock omits its receipt. Root's independent 20 s outer wrapper must capture whole-launch wall/child CPU. No speedup claim.
Acceptance requires RUN.status=completed AND evidence.status=2 with checked counts/hashes; supervisor exit 0 alone is insufficient. Failure logs retain first 2,500 bytes and record full length.
C23 counts clamp applications; active primary clips are fine.neg. A zero-leak witness may be initial in-core masked zero, not an outside-support positive sample.
Failure paths were not executed. Viewer/results verification remain separate gates. No flight, full-CHOPtrey, physical-validity or novelty claim follows.

