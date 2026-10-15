# Static saved-review preparation

This directory prepares future checker source only. No browser, GPU, network, operational producer or full checker has been invoked. The original overnight cutoff is closed and unchanged. No execution is allocated.

The independent `byte_primitives.py` is copied byte-for-byte from the published static GPU-readback preparation, `research/m31-gpu-readback-preparation-2026-10-16/review/byte_primitives.py`, at source commit `1241213790d94fb0e99efa0804d4affcf1446b24`. Its expected fixture is 128 bytes with SHA-256 `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951`. The primitive computes expected output independently; it does not import shader/page/host source.

The full checker entry point is source preparation only. Inert tests may import pure predicates and exercise bounded reads on fresh scratch fixtures; they must never call the checker main, the host, the page or any browser/GPU operation. Actual file bytes, page self-reports and external lifecycle evidence remain separate conclusions.
