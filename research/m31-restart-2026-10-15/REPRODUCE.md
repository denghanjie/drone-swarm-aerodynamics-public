# Reproduce this checkpoint

Use the public repository and a checkout containing this directory. Commands below run from the repository root with Python 3 (standard library) and Node.js. They perform analysis and small consistency probes, not a new mission campaign. Exact runtime versions are recorded in the output JSON. No Python or npm packages are needed for these analyses.

## View without downloading the large archive

```sh
python3 -m http.server 8876 --bind 127.0.0.1
```

Open `http://127.0.0.1:8876/research/m31-restart-2026-10-15/viewer/`. The committed compact binary contains all displayed poses. Three.js and OrbitControls come from the repository's existing vendor directory, with existing license notices. The viewer checks the binary SHA-256 before displaying it. It offers 14 exact saved case/time combinations, without interpolation or rerunning physics. These snapshots show position and attitude, not all 17 vehicle-state components.

## Restore and verify original evidence

The original large trajectories are versioned GitHub release assets, indexed by `data/research-data-manifest.json`. Restore them with the existing script:

```sh
python3 scripts/fetch-research-data.py
python3 scripts/fetch-research-data.py --verify-only
python3 outputs/research-reproduce.py
```

At this checkpoint the public evidence verification reported **306 files verified**, and the original manifest reproduction reported **1,581 verified files, no changed or missing entries**. These are archive integrity checks, not a new scientific campaign. The old manifest intentionally does not cover the new research directory; use its separate `manifest.json` below.

With restored data, the original full replay is available at `http://127.0.0.1:8876/outputs/milestone-31-lab.html`. It requires the large original trajectory assets; the new checkpoint viewer does not.

## Recompute the audit and selected poses

The main evidence scripts and viewer generator write their outputs beside themselves. To preserve the committed checkpoint byte-for-byte, run copies in a scratch directory or a separate worktree. The secondary M31/M32 audit instead requires an explicit output outside the evidence repository. Supply the evidence repository path explicitly. Different Python/Node version strings may change metadata hashes; compare scientific content and declared input hashes as well as file bytes.

```sh
python3 research/m31-restart-2026-10-15/evidence/audit_recompute.py .
node research/m31-restart-2026-10-15/evidence/audit_controls.cjs .
python3 research/m31-restart-2026-10-15/protocol/reproduce-evidence-audit.py --source-root . --output /tmp/m31-read-only-evidence-audit.json
python3 research/m31-restart-2026-10-15/build-viewer-data.py --evidence-root .
```

The first script independently reads original JSON and Float64 records and computes the evidence tables. The second reuses frozen dynamics for three two-step single-drone contact checks and evaluates normal/reversed neighbor lists at the two saved 20 s states. It saves all neighbor lists, velocity requests and residuals. The third independently recomputes the selected M31/M32 comparisons and input hashes. The final script extracts exact xyz/xyzw poses and verifies displayed maximum position differences against the historical comparison records.

Every per-drone statistic is descriptive within a scenario. Drones and time samples are dependent, and are not independent experimental replicates. Crossing times are recorded at integration-step endpoints. The novel summaries and order probes were developed after looking at the historical evidence; no retrospective preregistration is claimed.

The root researcher reran all three audit scripts from copies in an external scratch directory. All three output JSON files were **byte-identical** to the saved records; see [reproduction-check.json](reproduction-check.json). This is execution reproducibility of the analysis, not another independent dynamics model. The three two-step contact checks were repeated during that reproduction.

## Check new file integrity

```sh
python3 research/m31-restart-2026-10-15/verify-checkpoint.py
```

The manifest covers the new files except itself. It is a corruption/change check anchored by the Git commit, not proof of external authenticity. A deliberate revision needs a new manifest and commit; do not regenerate it to conceal an unexpected mismatch.

## Resume research

1. Read the summary, claim ledger and next-tranche proposal. Recheck the evidence hashes and any later work on main. All examined M31/M32 states are exposed development cases.
2. Implement only the fixed-state ordering decomposition and bounded restart harness specified in the plan. Freeze executable sources, inputs, schedules, budget enforcement and analysis before temporal runs. Exact natural-mode reproduction is a prerequisite.
3. Enforce the proposed 20-minute cap and retain incomplete/failed jobs. One solver process at a time; do not overlap benchmarks. No controller tuning or automatic expansion of the job matrix.
4. Save results against the exact implementation commit, update both ledgers and the 3D viewer, check the publication payload for private information, commit, push and verify the remote.
5. Return to the small aerodynamic comparison after this one diagnostic tranche. Obtain a compatible independent measurement reference before claiming physical validity. Do not call a numerical model or the finest step physical truth.

This branch is additive to historical public commit `c591ce2b195fa01b895d4ba881a44a4b92fdd703`. Remote main was observed at `1336f5c416875a9651f92b58b2ed06649f25b04e`, containing later DOT research. Do not reset or force-push main to this historical branch. If integration with newer main is desired, review the additive checkpoint separately.
