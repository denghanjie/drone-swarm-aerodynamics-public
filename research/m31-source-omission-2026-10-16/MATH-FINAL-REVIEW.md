# Final static mathematics and candidate review

Date: 2026-10-16. Reviewer scope: exact symbolic reasoning plus read-only inspection of candidate, fixtures, protocol, configuration and their unchanged model dependencies. No module was imported or executed; no syntax test, case generation, geometry/field/root evaluation, benchmark or integration was performed. No repository file was edited.

## Disposition

**No mathematical or candidate-source blocker remains for the declared finite numerical experiment.** This is qualified static clearance of the mathematics and candidate, not experimental acceptance, driver/evidence clearance or launch permission. The separate evidence reviewer owns driver completeness and preservation. All required cases, frozen tolerances and runtime/evidence limits still have to pass their own prospective gates.

The full symbolic derivation and caveats are in `/tmp/m31-omission-math-review.md`. In particular:

- For the fixed positive nominal thrust and nonnegative inflow, the unique positive cubic response has sharp global Lipschitz constant `L=f0/(3vi0)`.
- Uniform omitted inflow bound B yields exact one-sided thrust error `[0,4LB]` and each signed body roll/pitch error at most `2aLB`. The two-sided per-rotor numerical reserve eta requires `4eta` in total thrust and `4a eta` in each moment; the inspected capacity uses both correctly.
- Computing actual rotor-offset radii and source-axis norms addresses the nonunit-quaternion issue in real arithmetic. The radial map `I−nnᵀ` has operator norm `max(1,|1−||n||²|)`, as implemented.
- The product of separately maximized decreasing decay/fade/profile factors provides a valid source envelope. No monotonicity of the complete wake versus downstream distance is assumed.
- Strict zero branches, equality at the far-domain lower boundary, near-domain fallback before radial/projection pruning, and source-center neighborhood selection match the stated model contract. Domain-reject agreement is the claimed behavior; first-offender tuple equivalence is explicitly excluded.
- Every query rebuilds geometry, neighbors and omission decisions. The matched M control avoids bound-only preprocessing, while C pays for it. The remaining source-order/control difference from B is subject to full-output precision checks, not presumed bitwise equality.

## Repaired positive-source fixture

`multipleWeak` now has four sources at `(±0.31,±0.12,1)` and a receiver at the origin with identity orientations. For each source, the nearest receiving rotor lies at matching signed arm coordinates. Its radial distance is `sqrt((0.31−0.028)^2+(0.12−0.028)^2)<0.3m`, whereas `3H(1)>0.3m`; downstream1m lies strictly in the far branch, and the axis projection equals1. Hence each source contributes positively to at least one central receiving rotor in the real construction. The same-height source pairs have downstream0, so they do not introduce an unmodeled near-wake case. This is a symbolic inspection of declared coordinates, not a generated or evaluated fixture.

The repair resolves the earlier accidental all-zero-support construction. It does not establish that these sources are omitted, that their combined accepted bounds approach capacity, or that a physical fixture exhausts the budget. Those outcomes remain observations of the frozen invocation.

## Scope dispositions before freeze

The actual protocol/configuration governs the24fixture/152attempted-call/700000receiver-reservation matrix. The earlier DESIGN-REVIEW contains proposed16fixture/120call/650000receiver figures; it also suggested stronger fixture goals. The inspected PREFLIGHT-RESOLUTIONS.md explicitly supersedes those proposal details and records the intended640832full-matrix receiver shape. Scalar nextUp/capacity checks cover acceptance arithmetic; the fixed physical fixtures do not guarantee budget exhaustion or proximity to the omission threshold. This scope disposition is resolved. No additional test matrix is requested here.

The24fixtures have no huge common-translation case, as expressly disclosed in PREFLIGHT-RESOLUTIONS.md. Consequently they do not challenge loss of rotor-offset detail or changes in branch arithmetic caused by very large world coordinates. The center-offset real proof alone does not enclose all rounded world-point addition/subtraction operations. This absence is a declared coverage limitation, not a universal-failure claim.

The positive source inflation and nextUp operations do not make every preceding norm, dot product, division, fade or product outward-rounded. The eta reserve is an engineering assumption about the total two-path error, not a proven consequence of one solver's residual tolerance. The protocol correctly calls the margins empirically checked and declines a universal binary64 certificate. Rounded-fade nonnegativity, finite terms, domain fidelity and actual source/aggregate bounds therefore remain empirical gates for this experiment.

Only the fresh and fixture cases retain direct per-source magnitude evidence. Historical cases supply aggregate independent fields/loads and zero/support classifications, so no omitted-magnitude per-source certificate is claimed there. World vectors are descriptive; the fixed body quantities govern acceptance. Two fixed synthetic lattice configurations and technical timing repetitions do not establish distributional coverage, physical validation, novelty, flight accuracy or real-time performance.

## Inspected fingerprints

Workspace: `<REPOSITORY_ROOT>`.

- `research/m31-source-omission-2026-10-16/source/candidate.cjs`: SHA256 `c88eef4e67b29ba133dd24965db7cf831cb4337853a5e42f282cca4ceed9317e`.
- `research/m31-source-omission-2026-10-16/source/cases.cjs`: SHA256 `f9432791bc90385c7ade62b81c4b66a7a0053c083569707a9bb7556b346f63d9`.
- `research/m31-source-omission-2026-10-16/PROTOCOL.md`: SHA256 `f014c68a8c5c33b21e81782c9524457a3a2232c224af7e1c2335bee75a3aa972`.
- `research/m31-source-omission-2026-10-16/PREFLIGHT-RESOLUTIONS.md`: SHA256 `375e6b22314c4126944ac2950dded529481a48e29a76b2298f904c65a0eb91fc`.

Clearance refers to those inspected bytes. The scope clarifications are present and require no further mathematical change. The final freeze still requires independent verification. This review does not claim a completed freeze manifest or science result.
