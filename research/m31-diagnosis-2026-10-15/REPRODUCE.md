# Reproduction and evidence retrieval

Original executable environment: Node v24.19.0, Python 3.9.6, Darwin 25.5.0 arm64, Apple M4. Browser QA uses installed Chrome 155.0.8059.40 and Playwright 1.62.1. No paid resources. Timings are local diagnostics, not hardware comparisons.

The source freezes are `freeze-order.json` (commit `9e8fe14`) and `freeze-micro.json` (commit `e6680fe`). The latter hashes all original mission/checkpoint/command inputs and dependencies. Original public data are restored using the repository's `python3 scripts/fetch-research-data.py`. It verifies its own versioned archive. Never substitute private originals or different checkpoint bytes.

To download this checkpoint's raw micro evidence:

```sh
gh release download m31-diagnosis-2026-10-15-v1 --repo denghanjie/drone-swarm-aerodynamics-public --pattern m31-diagnosis-micro-evidence-v1.tar.gz --dir /tmp/m31-evidence
python3 research/m31-diagnosis-2026-10-15/verify.py --archive /tmp/m31-evidence/m31-diagnosis-micro-evidence-v1.tar.gz
```

The verifier reads and hashes every archive member without extracting it. Tar paths are relative, owner/timestamp metadata normalized, raw contents unchanged. Streams are Float64LE; each index records fields, frames and bytes. Time columns use integer ticks at 1,600 Hz. Four traces include six segments; split segments are not six independent traces. Final-context files preserve held actuators and full restart state.

To reproduce experiments, use an **independent disposable checkout at the source commit**, with restored original public evidence. The source commits precede their outcomes, so `results/order-probe.json`, `results/microchecks.json` and `raw/micro-started.json` must not exist there. Keep this completed result checkout unchanged. A new reproduction is a separately budgeted campaign, not a rerun in the closed original ledger.

Original executable sequence (from repository root):

```sh
python3 research/m31-diagnosis-2026-10-15/source/run-step.py --id order --timeout 240 -- node research/m31-diagnosis-2026-10-15/source/order-probe.cjs /path/to/restored-public-evidence
python3 research/m31-diagnosis-2026-10-15/source/run-step.py --id microchecks --timeout 240 -- node research/m31-diagnosis-2026-10-15/source/microchecks.cjs /path/to/restored-public-evidence
```

The supervisor rejects duplicate IDs, active or terminal campaigns, tracks wall time and raw size, and terminates/reaps children on interruption. The four 0.05 s microtraces consume the full 0.2 s allowance. Never automatically launch the full matrix after reproducing them: apply the frozen planning gate and subtract actual recorded elapsed time. No full matrix launcher is supplied in this checkpoint.

Viewer-only regeneration is safe data processing:

```sh
python3 research/m31-diagnosis-2026-10-15/source/build-order-viewer.py --evidence-root /path/to/restored-public-evidence
python3 -m http.server 8876 --bind 127.0.0.1
```

Open `/research/m31-diagnosis-2026-10-15/viewer/`. Regeneration was byte-identical: data SHA-256 `d552b2f591b2798585a2996c01a5f2286fed4de737a68fd0a9f3e66f4daa8ae8`. Viewer QA and screenshots are in `viewer/qa.md`. Viewer screenshot/camera interactions do not rerun the simulation.
