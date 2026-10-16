# Result claims and limitations

| Claim | Saved evidence | Assessment |
|---|---|---|
| Both prescribed flights completed and all six snapshots were captured | results/index.json; generation/run-a.json and run-b.json | Observed on two seeds, 64 drones each, ten seconds |
| Every snapshot passed its individual four-tolerance load check | results/check.json counts and outcomes; ten independent reference files | 6/6; conditional on checker qualification, which failed globally |
| Moving geometry and coupling are nontrivial under the registered witnesses | results/check.json nontriviality | Both runs informative; positive directed source edges A:103/76/55, B:99/63/53 at0/5/10seconds |
| Validator qualification succeeded | results/check.json corruptionControls | FALSE:20/20 rejected,19/20 reached intended failure families |
| Overall advancement justified | results/check.json passed/advancement | FALSE; both fields false |
| Replay preserves saved centers | qa/attempt-02/output/report.json |19,584center components checked; Float32 rendering conversion explicitly accounted for |
| Physical validity, aerodynamic feedback, real-time browser scale or novelty | No such experiment in this allocation | Not established |

Containment: sole kernel20.455s and sole checker42.783s; both child groups closed. Checker exit1 is the failed scientific qualification, not timeout or containment failure. These whole-stage durations are descriptive and not a performance comparison. The full frozen tolerances and normalization are specified in source/spec.json and independent helper references; this report does not convert them into physical accuracy.

Numerical filtering background, reused from previously verified primary sources (no new retrieval this cycle): Jonathan Richard Shewchuk, “Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates,” Discrete & Computational Geometry18 (1997),305–363, https://doi.org/10.1007/PL00009321; Hervé Brönnimann, Christoph Burnikel and Sylvain Pion, “Interval arithmetic yields efficient dynamic filters for computational geometry,” Discrete Applied Mathematics109 (2001),25–47, https://doi.org/10.1016/S0166-218X(00)00231-6; Guillaume Melquiond and Sylvain Pion, “Formally certified floating-point filters for homogeneous geometric predicates,” RAIRO–Theoretical Informatics and Applications41 (2007),57–69, https://doi.org/10.1051/ita:2007005. The provenance record is ../m31-filter-design-2026-10-17/review/literature/bibliography.json. These works support numerical-filter design principles, not this aerodynamic law, physical validity, moving-state outcome or novelty. Citation facts follow that retained verification; no fresh correction-status search is claimed.
