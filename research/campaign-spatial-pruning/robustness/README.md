# Independent robustness evidence

Place this directory at `research/campaign-spatial-pruning/robustness/`, beside the campaign’s `src/`, within the pinned public repository. This package contains independent numerical checks, modest fixed-work CPU timing, support-assumption sensitivity, and a clearly labeled browser-QA blocker. Start with FINDINGS.md.

Reproduce functional checks with `node checks.cjs --full`, then `node accumulation_probe.cjs` and `node support_sensitivity.cjs`. These scripts resolve the original pinned source through `../src/source.cjs`. Only run `timeout 120s node timing.cjs --serial-slot` during an otherwise idle serial measurement window; no performance claim should be made from overlapping runs. The timing configuration and every ordered raw timing sample are retained.

The viewer’s static identity/syntax checks are reproducible with `python verify_offline.py`; that is not visual validation. `qa_viewer.py` is the attempted real-browser procedure, provided for an environment where sandboxed Chromium is permitted. No browser permission, network-security or sandbox changes are authorized by these files.

Scientific result: numerical omission budgets passed sampled tests, but the independent useful pruning-speed gate failed in all 14 comparisons. Same-equation improvements relative to the inherited legacy implementation must remain separate. The extended-support model is exploratory, not a validated reference.

## Reviewed distribution edits

Paths were made portable, internal execution-coordination wording replaced with serial-measurement instructions, and the timing opt-in CLI flag renamed to `--serial-slot`. Absolute runtime paths and detailed host CPU/load/memory diagnostics were removed from shared raw copies; mathematical inputs, numeric field/load errors, source hashes, all measured durations, and negative outcomes are unchanged. Preliminary changing-source records are excluded from frozen evidence; their scientific bound failure remains described in FINDINGS.md and in the main campaign archive. Complete original records remain retained locally.

Test-script bytes differ from original execution hashes only through these documented packaging edits. The candidate source hash remains `1d9e1afcf9983b900034b7b586c4ffd02ec4b3242c467f8e684fbdda1850d562`. Source repository: https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/c591ce2b195fa01b895d4ba881a44a4b92fdd703
