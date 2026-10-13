# Exact-equation airflow efficiency campaign

Editorial correction (2026-10-13): the independent previous-zero pass count is 3/12. See [the correction record](CORRECTIONS.md); numerical records and simulation code are unchanged.

## Result
Lean bound-free exact evaluation passed the preregistered field-time gate in 8/12 held-out N=100/200 cases. Scaling stopped before N=500.

The frozen lean implementation removes positive omission-budget bounds and allocation-heavy geometry operations while keeping all four rotors and every positive in-model contribution. Conservative support culling and reusable geometry scratch were tested separately; their added work did not consistently beat lean. This is software-equivalence evidence for an unvalidated finite-support model, not physical validation or a new accuracy–cost frontier.

## Frozen methods and controls

- Legacy: unchanged milestone-28 sum-rotor field.
- Previous-zero: unchanged prior campaign zero-budget module, including omission-bound calculation.
- Lean: scalar geometry/kernel with no pair bounds.
- Support: lean plus conservative exact-zero pair support checks.
- Reuse: support with refreshed internal geometry scratch; caller-owned returned winds.

Original source checkpoint: `c024dfc27b9e6b7cd5b39132164d1339cb95b12f`. Mechanics/wake baseline: `c591ce2b195fa01b895d4ba881a44a4b92fdd703`. New module SHA256: `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`. Selection used development seeds 4301/4302 only; held-out seeds were 4391/4392. [Selection record](results/selection.json).

The original eight-step roadmap remains in force: define the experiment, preserve mechanics, verify pair interaction, verify overlapping sums, run genuine local 3D Boids, measure CPU efficiency, scale conditionally, and evaluate limitations. This campaign makes no claim that physical-validation steps are complete.

## Correctness and retained failures

151 primary tiny/development/held-out prescribed-state cases passed. Maximum error versus legacy: inflow 0 m/s; force 0 N; moment 0 N m. These tolerances are model-relative, not measured aerodynamic accuracy.

Independent checks test boundaries, permutation/translation behavior, changing swarm sizes, mutated states and stable ownership of returned wind arrays. Raw independent reports accompany the checkpoint.

A retained v0 error at a huge coordinate translation rounded a receiver-rotor offset beyond the nominal support envelope: legacy/lean produced 0.001587065203100887 m/s while support/reuse produced 0. The fixed numeric API rejects position components with absolute magnitude above 1e6 m and adds conservative roundoff margin within that range. A pre-existing legacy/previous-grid hang at 1e20 m is also retained. These are implementation/input-domain findings. No positive interaction is intentionally dropped on the accepted domain. See [amendments](AMENDMENTS.md), [retained v0](source-versions/exact-aero-v0.cjs.txt), [exact v0 counterexample](review/large-translation-v0.json), [fixed-domain regression](review/large-translation-v1.json), [guard checks](review/targeted-guards-v1.json) and [independent code review](review/CODE_REVIEW.md).

## Held-out CPU field measurements

All five variants ran serially, in paired rotated orders, with nine repeats per held-out case. Field timing includes finite/unit/range validation, refreshed geometry, grid search, kernel evaluation and caller-owned output. Every complete output is checksum-verified outside the timed interval. Field+receiver evaluation is separate. Receiver-only repeated measurements run identical code and are a noise control. Reuse construction timing covers empty evaluator construction; first geometry allocation occurs during warmup. Small warmup/sample budgets, shared-host interference and timing outliers limit hardware-generalization.

| N | Family | Seed | Lean / previous-zero (95% paired bootstrap) | Gate | Legacy / lean speed | Raw |
|---:|---|---:|---|---|---:|---|
| 100 | dense | 4391 | 0.869 [0.605, 0.959] | pass | 1.95× | [record](results/timing/heldout-4391-100-dense.json) |
| 100 | sparse | 4391 | 0.890 [0.628, 0.983] | pass | 1.74× | [record](results/timing/heldout-4391-100-sparse.json) |
| 100 | tilted | 4391 | 0.935 [0.854, 1.004] | fail | 1.70× | [record](results/timing/heldout-4391-100-tilted.json) |
| 200 | dense | 4391 | 0.925 [0.857, 1.030] | fail | 1.96× | [record](results/timing/heldout-4391-200-dense.json) |
| 200 | sparse | 4391 | 0.863 [0.747, 0.928] | pass | 1.76× | [record](results/timing/heldout-4391-200-sparse.json) |
| 200 | tilted | 4391 | 0.958 [0.734, 0.995] | fail | 1.61× | [record](results/timing/heldout-4391-200-tilted.json) |
| 50 | dense | 4391 | 0.876 [0.822, 0.907] | pass | 1.75× | [record](results/timing/heldout-4391-50-dense.json) |
| 50 | sparse | 4391 | 0.886 [0.852, 0.916] | pass | 1.71× | [record](results/timing/heldout-4391-50-sparse.json) |
| 50 | tilted | 4391 | 0.894 [0.882, 1.036] | fail | 1.59× | [record](results/timing/heldout-4391-50-tilted.json) |
| 100 | dense | 4392 | 0.881 [0.619, 0.962] | pass | 2.07× | [record](results/timing/heldout-4392-100-dense.json) |
| 100 | sparse | 4392 | 0.895 [0.791, 0.937] | pass | 1.84× | [record](results/timing/heldout-4392-100-sparse.json) |
| 100 | tilted | 4392 | 0.879 [0.783, 0.909] | pass | 1.73× | [record](results/timing/heldout-4392-100-tilted.json) |
| 200 | dense | 4392 | 0.923 [0.815, 0.972] | fail | 1.96× | [record](results/timing/heldout-4392-200-dense.json) |
| 200 | sparse | 4392 | 0.885 [0.719, 0.984] | pass | 1.67× | [record](results/timing/heldout-4392-200-sparse.json) |
| 200 | tilted | 4392 | 0.899 [0.818, 0.974] | pass | 1.61× | [record](results/timing/heldout-4392-200-tilted.json) |
| 50 | dense | 4392 | 0.882 [0.837, 0.917] | pass | 1.72× | [record](results/timing/heldout-4392-50-dense.json) |
| 50 | sparse | 4392 | 0.847 [0.811, 0.908] | pass | 1.71× | [record](results/timing/heldout-4392-50-sparse.json) |
| 50 | tilted | 4392 | 0.928 [0.825, 1.277] | fail | 1.64× | [record](results/timing/heldout-4392-50-tilted.json) |

At N=100, sparse and dense pass on both primary held-out seeds; tilted passes only one. At N=200, sparse passes both, dense neither, and tilted only one. Therefore N=500 was not run. A favorable result for one seed does not stand in for family-wide replication.

## Genuine Boids replay and whole pipeline

All 14 planned actual Boids recordings completed: two seeds, N=16 for 1 second and N=50 for 3 seconds, each legacy/previous-zero/lean, plus two separate N=16 cadence refinements. All 8 matched implementation comparisons had identical SHA256 streams over every integrated full state and held rotor field, with zero saved-pose differences. [Replay index](results/boids/index.json) · [repository demo](demo/index.html). The offline HTML bundle is delivered separately and can be regenerated with `python src/build-standalone.py`; it is not duplicated in Git. These short starting-cloud windows do not establish obstacle-course or full-mission success.

Primary fixed-work N=16/1s pipeline timing used seven paired repetitions, one warmup per method,400 physics steps and100 field updates. All terminal full-state/held-field hashes matched. Lean/legacy total-time ratio was 0.847, paired 95% interval [0.797,0.918]; lean/previous-zero was 0.911,[0.901,0.960]. The latter 8.9% median saving is below 10%, and this tiny development workload does not establish general end-to-end gains. [Raw primary pipeline](results/pipeline.json).

Separate N=16/1s numerical checks gave maximum saved-position differences 7.21 nm for halved physics step and 7.01 mm for halved airflow interval. Both are below the predeclared 1 cm short-window screen, but the much larger refresh sensitivity and prior long-horizon failures remain unresolved.

## Independent robustness replication

Independent fresh lattice-based fixtures and seeds passed their own preregistered primary field gate versus legacy in 12/12 nonzero cases: lean/legacy ratios 0.498–0.708. Against previous-zero, ratios 0.856–0.965 passed both parts of the individual field-time gate in 3/12 cases: median ratio at most 0.9 and paired-bootstrap 95% upper ratio below 1. Four cases met the median-only threshold; the 628791/N=100/tilted case failed the upper-bound condition (1.0105362). No family/count passed on both independent seeds; this is an additional robustness observation, not a retrospective failure of the independent primary comparator. The independent protocol times checksum accumulation inside its field interval, unlike the primary protocol; results are not pooled.

An independent 9-repetition N=16 whole-pipeline workload gave lean/legacy0.917,[0.885,0.967], and lean/previous-zero0.960,[0.936,1.018]. These smaller gains reinforce the workload-specific interpretation. All independent final full-state hashes matched, with zero final-state difference across its 27 timed members. Terminal held-wind hashes were not retained in that independent run; the primary A5 pipeline additionally verifies those winds. See [independent findings](robustness/FINDINGS.md), [independent correctness checks](robustness/raw/independent-checks.json), [primary timing arithmetic audit](robustness/raw/primary-timing-audit.json), [independent pipeline record](robustness/raw/independent-pipeline-628791-16-boids-lean.json) and [replay audit](robustness/raw/replay-audit.json). The independent field records are linked from its findings.

Overall: cumulative field acceleration over allocation-heavy legacy is robust. The extra gain over the previous optimized zero-budget implementation is modest and workload-sensitive. No N=500 promotion, retuning on held-out data, or browser/GPU claim followed the mixed results.

## Reproduction and limitations

See [README](README.md), [frozen plan](PLAN.md), [configuration](configs/campaign.json) and [provenance](provenance.json). Each raw timing record links its deterministic fixture input and retains full paired measurements; incomplete/failing records are not pooled as successful measurements. Public copies omit private machine/process observations with a disclosed editorial manifest.

The source has fixed isolated-hover strength, finite support 2.5 m downstream/three half-widths radially and 3 m center search. It does not model general rotor-speed-dependent emission, rotor-resolved source flow, wake deformation, turbulence, or validated multi-vehicle interference. Receiver force response and multi-wake superposition are unvalidated. Existing airflow-refresh and long-horizon trajectory sensitivity are not resolved by exact-code acceleration. This campaign does not establish browser/WebGPU throughput, full-mission safety or 5,000-drone feasibility.

## Viewer verification

The standalone HTML bundles local Three.js modules, the full MIT license and actual saved Boids records. Static syntax, data, link and integrity checks are separate from rendered visual QA. One cloud Chromium launch was attempted and blocked by a socket-permission denial; no screenshot or interactive rendered verification was obtained, and no workaround or retry was attempted. See [browser check](results/viewer-qa/browser-check.json).
