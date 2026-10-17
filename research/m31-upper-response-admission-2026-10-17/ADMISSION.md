# Upper-response admission audit

**Disposition: no retained textual statement establishes a matched, admitted-domain rejection of the current model's zero upper mean interaction response.** The paper does report an upper response. The missing step is associating that response with a complete configuration and actuation/measurement mapping that passes the whole-query contract. This is a narrow source review, not a claim that the model is physically validated or that the reported effect is absent.

## Sources and scope

Kiran, Ayanian and Breuer, *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, RSS 2025, DOI 10.15607/RSS.2025.XXI.102; retained body is arXiv **2507.09463v1**, 13 July 2025. Citations below refer to that retained version, not an assumed identical proceedings body. Body/text identities and implementation sources are pinned in READ-RECEIPT.json; third-party bodies remain private.

No network, acquisition, figure-number extraction, digitization, fitting, scoring, implementation execution, or scientific run was performed. Numerical values below are published prose values, source constants, or explicitly identified elementary deductions. No frozen package was modified.

## Explicit textual facts

1. **Geometry and actuation:** §II-A describes two Crazyflies on an x–z translation stage, upper A traversing and lower B fixed, 100 μm stage position accuracy, and ATI Nano-17 six-axis transducers. The introductory §II description says the mounting prevents roll and yaw; this does not supply complete raw attitudes and rotor geometry. Motors receive constant 4 V and hover PWM; speed is approximately 320 Hz. The authors explicitly distinguish constant voltage from constant rotational frequency. §III-A defines **l = 32.5 mm as body-center-to-motor distance** and W approximately 0.265 N.
2. **Closest upper mean thrust:** §III-A, discussion of Fig. 5(a), says the upper vehicle experiences a slight thrust reduction and retains 90% of original hover thrust at **Δz/l = 4**. That sentence does not separately identify its horizontal coordinate. Earlier discussion identifies the strongest lower loss with the stacked closest configuration. These are not sufficient grounds to silently attach every upper value to every horizontal coordinate.
3. **Upper pitch:** §III-A, discussion of Figs. 5(c), 6(c), reports a pitch moment on both vehicles with horizontal centerline displacement, growing to **Δx/l = 2**, where upper left and lower right rotors align. The upper moment is described as one-third of the lower moment. This paragraph does not specify the simultaneous vertical coordinate, signed moment, or an uncertainty interval excluding zero.
4. **Farther flow measurements:** §II-A2 explicitly includes stacked and offset PIV cases at **Δz/l = 12.5**, as well as 4. These are velocity measurement configurations; the prose does not attach a nonzero upper mean thrust or pitch measurement to the 12.5 case.
5. **Fluctuations:** §III-A, Figs. 5(b), 6(b), discusses standard deviation, persistence to approximately 17l vertically / 4.5l horizontally, and upper turbulence roughly two orders smaller than lower. Variance/unsteadiness is a different observable from a nonzero mean upper thrust or pitch increment.
6. **Coordinate association discrepancy:** §II-A1 gives a horizontal test range 0.1–0.6 m and vertical range 0.1–1.1 m. The horizontal lower bound does not directly reconcile with the separately described stacked Δx = 0 and offset 2l = 0.065 m cases. This review leaves that range/case association unresolved. It does not amend the paper or infer a hidden case table.

The preceding lower-vehicle discussion at Δz/l > 19 does not establish an upper mean response at that spacing merely because the next sentence contrasts upper and lower effects.

## Deductions from the exact source contract

The frozen spec uses arm = 0.028 m and corners (±1, ±1, 0). **arm is a corner coordinate component, not paper l.** `constants_from_graph` forms rounded R = sqrt(2) × arm and D = 2R (pair-reference.py:302–323). Thus the current model's center-to-motor distance is approximately 0.0396 m, D approximately 0.0792 m, and its near-height threshold 2.5D approximately 0.198 m. D is not the propeller diameter; the separate rotor radius constant is 0.023 m. Neither paper l = arm nor paper l = D is an admissible substitution.

For a conditional upright mapping, the published closest height 4l is nominally 0.13 m. Conservative source-scale bounds are 0.039 < R < 0.043 m and 0.195 < 2.5D < 0.215 m; binary64 rounding is far smaller than these margins. At stacked centers, the lower rotor points have radial distance R from the upper source axis, not zero. They nevertheless lie inside nearRad = 0.15 m, while down = 0.13 m is below 2.5D. Every lower-rotor ← upper-source pair therefore reaches **near refusal**. At a conditional horizontal offset 2l = 0.065 m at the same height, the triangle bound gives radial ≤ 0.065 + R < 0.108 m for any planar yaw; those pairs also refuse. This second deduction does **not** assert that the paper's upper-moment paragraph specifies height 4l.

The pair gate uses source center minus the **actual rounded receiver rotor point**, projected onto the source axis. It does not use just center height or center horizontal separation (pair-reference.py:345–357, 474–558). Under upright positive separation the reverse upper-receiver ← lower-source pairs are upstream zeros. That alone cannot admit the two-drone query: tree-reference.py:211–235 refuses the whole query if any relevant pair refuses. Consequently a conditional stacked 4l placement cannot supply an admitted full-query prediction for comparison.

For an otherwise admitted upright pair at fixed nominal rotor forces, all incoming upper interaction coefficients vanish; the cubic has alpha = 0 and root x = 1, so upper force and moment equal their isolated-input baselines (semantic-reference.py:158–216). This is a structural omission of upper mean interaction. It remains a valid qualitative limitation even though the retained prose does not establish a matched in-domain rejection.

## Gate and matching ledger

| Requirement | Status for a published upper mean-response case |
|---|---|
| Raw finite 17-component states, positive four nominal rotor forces; valid quaternion, prepared axis and offset geometry | No complete case-specific inputs supplied by the cited prose. Mounting description and hover setting do not fill them. |
| Center bounds (components ≤257 m; norm ≤512 m), receiver-point components ≤258 m, projected down ≤1024 m, radial norm ≤2048 m | Ordinary reported nominal meter-scale upright placements are far inside these guards, but exact raw/prepared states are not established. |
| Neighbor support: center distance <3 m for potentially active pairs | Reported nominal ranges are inside this support; the upper-response case association remains incomplete. Neighbor zero would not prove a measured mean response. |
| Upstream down≤0; down cutoff at 2.5 m | Conditional upright upper receiver is upstream zero; reported nominal positive lower gaps are below cutoff. Full attitudes remain unresolved. |
| Near: down<2.5D and radial<0.15 m refuses; otherwise near-outside gives zero | Conditional closest stacked and 2l-offset examples refuse as above. Larger unreported horizontal offsets could enter near-outside instead; do not extrapolate the closest upper measurement there. |
| Positive height/width; radial support radial<3×width; alignment projection>0; down/radial fades | Defined by height=down/D−origin, width=spread×height×D, origin=−5.817, spread=0.07668; fades start at down=2 m and radial/width=2. Need matched prepared geometry. A 12.5l PIV height alone verifies no mean-force case or complete support path. |
| K and K×beta ≤128; beta from source nominal total; positive receiver force normalizer | No case-specific force/actuation mapping or cap certification. No coefficient computation was run. |
| Whole-query preparation, descending-center-z/stable-ID ordering, no positive backward edge, ≤180 drones, positive-term cap 2,000,000 | Two vehicles easily satisfy count limits; geometry/forces must still establish all pair statuses and ordering. Near refusal already blocks the conditional closest placement. |
| Physical geometry match | Paper l=0.0325 m differs from frozen R≈0.0396 m. Rotor radius/propeller equivalence, rotor ordering, yaw/pitch and center/reference locations are unresolved; changing constants would define another model. |
| Actuation and comparison baseline | Need mapping from constant-voltage/PWM operation to the model's nominal per-rotor forces, including any RPM/load change, tare, isolated hover baseline and signed axis conventions. Approximate speed and total weight do not establish these. |
| Upper measurement uncertainty | Sampling at 20 kHz for 30 s with three repetitions (§II-A1) is stated. No matched upper-channel calibration/tare uncertainty and interval for a mean increment has been established. Repetition SD is not a sensor accuracy bound. |

## Narrow admission decision

**No published prose statement reviewed here suffices for a matched in-domain mean-response rejection.** The only explicitly height-linked upper mean-thrust value is at the closest gap; the natural upright stacked interpretation is refused, and its horizontal association is not separately explicit. The upper moment statement lacks a simultaneous height. Farther PIV cases and unsteadiness prose cannot replace a mean-load observation. A future source-level resolution would need a jointly identified geometry and mean upper observable, exact mapping to frozen inputs, and uncertainty/baseline evidence. No such extraction, new experiment, or scoring is authorized or performed by this note.
