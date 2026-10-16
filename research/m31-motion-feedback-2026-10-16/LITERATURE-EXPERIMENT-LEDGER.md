# Sources and assumptions

No new acquisition, search or version/retraction check was made for this numerical adapter. These entries inherit the explicitly verified access scope in m31-restart-2026-10-15/literature/annotated-ledger.md and source-access-log.md, and the source-accounting receipt. Machine-readable citations are in bibliography.bib.

| Source | Specific use | Limits / adaptation |
|---|---|---|
| Bauersfeld et al., *Robotics meets Fluid Dynamics: A Characterization of the Induced Airflow below a Quadrotor as a Turbulent Jet*, arXiv2403.13321v3,12Dec2024 accepted RA-L manuscript; §§III-D/IV,Eq8. | Motivation of the inherited fitted jet shape, as pinned in the existing coefficient kernel. | Local27g scaling, distance definition, fades/cutoffs, source-total force scaling, instantaneous moving-pose use and ideal-power receiver are our unvalidated assumptions. No reproduction of measured apparatus. |
| Reynolds (1987), *Flocks, Herds, and Schools: A Distributed Behavioral Model*, SIGGRAPH,pp25–34; author's abstract/citation and Boids explanatory page. | Local separation, alignment, cohesion/neighborhood as embodied in the original M31 steering. | Original full paper was not read successfully; author's explanatory three-rule/neighborhood discussion was read. Our shared route, avoidance, controller and physics are separate additions; no novel flocking claim. |

Rigid-body force balance, rotor lever-arm moments and explicit RK4 are conventional mathematics implemented locally. Equations and limitations are stated in PROTOCOL.md and adapter.cjs; no external experimental support is attributed to these implementations. The source-total/ideal-power closure is the same provisional contract previously reviewed in m31-coupled-solve-2026-10-16/review/CONTRACT-CHALLENGE.md. Keeping nominal yaw torque while altering axial thrust is an explicit modeling assumption, not a result of either cited paper.

The immediately preceding Simmons–Hatke access attempt did not provide measurements; it informs only the decision to keep this checkpoint numerical. See the separately published m31-fixed-command-presentation-2026-10-16 result and bibliography. No new physical score, novelty search or publication claim is made here. The result ledger will associate actual observations with this frozen source commit, including failures and skipped exploratory paths.
