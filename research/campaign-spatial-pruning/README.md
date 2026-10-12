# Spatial wake omission: bounded numerical campaign

This local research campaign tests controlled omission of geometrically weak wake interactions against a pinned, finite-support, unvalidated mean-field model. It preserves four receiver rotors and force/moment response. Passing tests establishes software/model-relative bounds, not aerodynamic validity, flight safety or real-time performance.

Status: the bounded campaign is complete. Numerical error bounds passed, but the weak-wake pruning speed-benefit gate failed. The failed v0 development candidate, all timings, compact accuracy cases and eight one-second genuine local Boids records are retained. Read REPORT.md for the result and limitations.

## Layout and reproduction

Place this directory at `research/campaign-spatial-pruning/` in the repository containing commit `c591ce2b195fa01b895d4ba881a44a4b92fdd703`. The development archive alternatively includes a `snapshot/` child with that commit. The source loader supports both layouts without network access or installing packages. Node.js runs the numerical code; Python can serve the eventual local viewer.

From this directory, run:

```
node src/verify-source.cjs
node src/checks.cjs
timeout 180s node src/experiment.cjs accuracy
python src/summarize-accuracy.py
timeout 285s node src/experiment.cjs timing
timeout 90s node src/boids-diagnostic.cjs
```

The verification command checks SHA-256 of the imported historical source files. The tiny check command regenerates `results/tiny-checks.json`. Read `PLAN.md` and `AMENDMENTS.md` before running additional experiments. All measured work is bounded and serial. No large historical evidence archive is needed. Full new per-rotor accuracy evidence is about 194 MiB compressed and retained separately, with its exact hash/bytes in results/accuracy-cases.json.

Open wake-pruning-evidence.html directly in a browser for the self-contained offline Three.js replay. Alternatively run `python3 -m http.server 8876 --bind 127.0.0.1` here and open `http://127.0.0.1:8876/demo/index.html`. The viewer displays actual saved states and held fields; it performs no physics simulation. The source-based build requires esbuild only if regenerating the standalone HTML; all numerical scripts need only Node's built-in modules.

Viewer verification is limited to source/data identity and syntax checks. Browser launch was blocked by a socket permission restriction, so rendered appearance, interactions and mobile layout remain unverified.

## Records and limitations

- `PLAN.md`, its original hash, and append-only `AMENDMENTS.md`: frozen assumptions, tolerances and changes.
- `configs/campaign.json`: prescribed seeds, scenarios, budgets and caps.
- `source-versions/`: failed pre-freeze candidate v0, retained rather than erased.
- `results/`: actual test and experiment records, including failures.
- `provenance.json`: pinned upstream reference hashes and scientific source links.

The original eight-step roadmap remains at `outputs/research-roadmap.md` in the pinned repository. The new code does not alter it or claim those steps complete. Nominal rotor thrust remains the state variable used by the existing receiver response, while source wake strength remains prescribed isolated-hover strength. Mean-wake fading, finite support, uncalibrated receiver response and neglected flow effects limit all conclusions. The prior cadence and long-trajectory-refinement failures are not repaired by this campaign.

Original project material has no selected open-source license. Existing third-party files retain their original notices; no new licensing rights are implied by this checkpoint.
