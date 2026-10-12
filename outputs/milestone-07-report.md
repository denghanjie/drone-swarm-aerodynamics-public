# Milestone 7 — extra clearance under uncertainty

The frozen candidate avoided measured navigation failures in all 60 holdout cases, with a substantial passage cost. This finishes the planned local navigation robustness comparison within original Step 5; it does not validate airflow or guarantee real-flight safety.

| Profile | Faster / extra-clearance total passages | Faster / extra-clearance invalid-crossing runs | Faster / extra-clearance sub-20 cm runs | Faster / extra-clearance stops |
|---|---:|---:|---:|---:|
| ±2 cm bias + 0.10 s delay | 870 / 610 | 0 / 0 | 0 / 0 | 0 / 0 |
| ±5 cm bias + 0.25 s delay | 786 / 514 | 14 / 0 | 5 / 0 | 1 / 0 |

Each row contains 30 paired runs; passage totals sum drones across runs, with a maximum of 1,500 per controller. The candidate reduced stress-profile passage by 34.6%. Its minimum separation was 0.346 m across all cases. These descriptive outcomes do not provide a validated failure probability. Counts at 60 s do not imply all drones eventually pass.

The test uses three widths, two error profiles and seeds 101–110. The candidate was designed using the earlier failure evidence, then frozen before these new seeds. It changes lane capacity/spacing, gate-edge clearance, position gain and group-release timing together, so no single-change causal claim is supported. Both controllers use paired initial states and navigation errors; exact low-level feedback and exact initial maps remain favorable assumptions. Aerodynamics is off.

All three verification checks passed: paired inputs/errors, finite records, and numerical refinement of the closest candidate case at each width. The old controller’s contact failure is retained. Every replay uses seed 101; its displayed outcome is not substituted for the whole study.

Reproduce with `node outputs/milestone-07-source/study.cjs` from the workspace root. This will regenerate milestone-7 numerical outputs, so copy them or use a separate output directory before a new research revision. Milestones 1–6 remain untouched.

[3D comparison](milestone-07-clearance.html) · [Protocol](milestone-07-protocol.json) · [Raw results](milestone-07-study.json) · [CSV](milestone-07-study.csv) · [Verification](milestone-07-verification.json)
