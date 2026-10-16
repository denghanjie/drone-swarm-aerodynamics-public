# Result claims, evidence and limits

Source commit a3705740e586941855a71a320d48e7374ccd5224; source-manifest SHA256 5864adc22bbbf9d27afca25bb2ccb6f8da3c234997bf2a7e8c55bdafd750917d. Exact remote manifest and all 63 local/committed pins verified before target execution. One candidate and one saved-only independent reviewer invocation; no retries.

| Claim | Saved support | Scope |
|---|---|---|
| 12 paths complete; all declared gates pass | results/analysis.json; independent-review.json | 3 pair controls, 6 prior-seed repeats, 3 conditional new force-only paths |
| Full/force-only sampled position discrepancy 0.510847004 m | Finest trial JSONs; analysis.comparisons; independent recomputation | One deterministic exposed seed, 2 s; no physical accuracy threshold |
| Force-only/off discrepancy 1.331128103 m; full/off 1.102444041 m | Same | Separate maxima on different drone IDs; no additive attribution |
| Full/force-only stage tilt maxima 19.555806443° / 8.904407282° | Candidate stage records; independently checked sampled tilts and selected stages | All-stage maximum is recorded candidate diagnostic, not complete independent reintegration |
| Final mean heights full 3.655363984 m; force-only 3.654584264 m | Final states and independently recomputed centroid | Similar means do not imply per-drone or trajectory agreement |
| 360,829 checks pass | Frozen independent-review.json | Numerical implementation assertions; not physical observations or independent experiments |
| 207 endpoints / 96 captured RK stages | Reviewer/trial records; SAVED-DESCRIPTIVE.json | Other 36,304 stages retain candidate scalar diagnostics only |
| Original nominal angular dynamics retained in nontrivial states | Reviewer savedStateCoverage, independently derived body equations | Force-only has 960 endpoint and 288 captured-stage vehicle-state occurrences with both nonzero rates and unequal nominal rotor states; repeated samples, not independent trials |
| Numerical-resolution context | 20 observable refinement gates; 19 bothTiny; coupled bodyRate standard reduction | No formal order or rigorous continuous-time bound; body-rate error 2.3337e-5 → 1.8189e-6 rad/s |
| No recorded model/contact failure; zero saturation counts in Boids | Candidate records and summary | Not general flight stability/safety; collision logic not independently replayed |

The candidate supervisor reports 4.446899291 s, sampled RSS 285,296 KiB, zero monitor errors/races; reviewer 2.107516210 s, 145,472 KiB, zero monitor errors/races. Output fits the prospectively enlarged 40 MiB cap. These timings are not benchmarks.

No new external research was acquired. The verified-scope literature remains Reynolds (1987), SIGGRAPH, pp. 25–34, DOI 10.1145/37401.37406 (local flocking motivation; author's explanation read), and Bauersfeld et al., arXiv:2403.13321v3 (hover jet-shape motivation; stated sections previously read). See bibliography.bib, CLAIM-LITERATURE-LEDGER.md, and the pinned inherited literature/access ledgers. Neither supports our source-total closure, ideal-power receiver, moving-pose extension, retained nominal yaw model or synthetic moment mask as experimentally validated physics. No measurement was admitted by the closed Simmons–Hatke access attempt. Current novelty and physical validity remain unresolved.
