# Public edition of the frozen prospective plan

Original plan SHA256: `432df20958f03ff66e20f4b9590a1924f92a3822ea2c14a2fb7beb1e81741d75`. The original was adopted before the single attempt. Its prospective wording is retained below; only the stale local storage-headroom sentence is omitted. See [the result](results/REPORT.md) and [retention erratum](results/RETENTION-ERRATUM.md). This edition grants no execution permission.

# Predictor event-stress protocol
2026-10-15 UTC. FINAL PROPOSAL awaiting hash-bound root adoption; code review and execution release remain separate. No model preview occurred. Earlier campaigns remain unchanged.

## Question and fixed case
Test whether the unchanged linear-plus-clamp predictor retains its fourfold numerical advantage over ZOH during longer own-state Boids obstacle/support interactions. No novelty, order, speedup, physical safety or wall-induced airflow claim.

Use public commit1336f5c416875a9651f92b58b2ed06649f25b04e, factory=wide,N16,airflow=sum-rotor,field=lean. Initialize seed840163 once; verify its17-component initial state block against saved SHA2568968fc73e80f604e1dee302f4feed81620dadcaf420ec0c6800db13e32a84cb7. Add exactly4.5m to every x position, leaving every other component unchanged. Copy this state into all arms, then use the existing own-state controller. No scripted formation, trajectory or obstacle modification.

The fixed+4.5m offset moves the front from about-6m to-1.5m, inside1.6m wall-filter range, preserving relative wake geometry analytically but not necessarily bitwise. No alternative offset was searched. Seed840163 was selected after its short screen showed neighbor changes and smaller position improvement: developmental selection.

## Static geometry
GEOMETRY-READINESS.json SHA2560143887fd175b1eca88471d7632dda073a2a73468edc2f61fa2637cc8d9a92ad uses the saved initial2176bytes and all34 public AABBs, without JS evaluation. Translated x bounds[-2.329613,-1.437776]m. Minimum body clearance1.219225m to partition-0-right; ground3.682229m; pair-body0.495559m. Rotor-center offset plus radius=sqrt(2)*0.028+0.023=0.06259798m, inside the0.075m body sphere: initial rotor disks clear every box by at least1.231627m. Eight agent/box combinations, six agents, are within1.6m. Descriptive margins are not interval-certified future safety; range exposure does not prove binding avoidance.

Initial farStart=0.197989899m. Nearest absolute downstream margin0.0618284m has simultaneous radial distance1.07505m. Minimum radial clearance from forbidden0<down<farStart,r<0.15 is0.460922m. Among positive-downstream pairs with r<outerAtFar=0.15152109m, nearest farStart margin is0.468933m. Translation preserves these relative margins analytically initially; future proximity is unknown.

## Seven arms
Q=1/51200s,endTick25600=0.5s; controls every512ticks; comparisons every128ticks. First run joint128/64/32 with normalized trial geometry, raw derivative state and accepted quaternion projection. Qualify references before approximations. Then ZOH and predictor each h16/h8, air64ticks. No substitute seed, offset, cadence or horizon. An early reference/domain stop is informative.

Keep source bytes, receiver closure, amplitude, controller arithmetic/clocks, predictor and componentwise max(0,raw) unchanged. Initial64ticks use ZOH; later actual RK-stage alpha includes old-interval alpha1. History spans controls. No slope tuning, reset, adaptive refresh, geometry fallback or refit. Both approximation methods share the wrapper/guards.

Repeat inherited compatibility/scalar fixtures within this attempt; count every call. Tick0 diagnostics follow U0 acquisition; later controller-grid diagnostics precede refresh; no terminal production refresh/control. Auxiliary fields never enter history/evolution. Each arm uses its own Boids commands.

## Numerical decisions
Reuse metric definitions and small caps(position,velocity,attitude,angular-rate)=(1e-4,1e-4,1e-4,1e-3), outer=(1e-3,1e-3,1e-3,1e-2), floors=(1e-8,1e-8,1e-7,1e-7). These are numerical goals.

Reference: J64-J32<=small and <=max(floor,0.6*(J128-J64)) per metric; nonzero production wind required. Failure stops before approximations. If qualified, collect all four approximate arms unless source/domain/resource checks stop. Baseline absolute-cap failure does not abort paired scoring.

Each method's h16-h8 difference must meet small caps. For h8 error E against J32, require U=max(joint-fine difference,method h-difference)<=0.1E; when E<=floor require U<=floor and label floor-limited, with no relative-resolution claim. Predictor must meet all outer caps and E_P<=0.25E_Z where baseline>floor; otherwise E_P<=floor, uninformative for fourfold improvement. Require at least one resolved baseline metric. Report every failed/unresolved cell, maxima, terminal metrics and branch differences.

## Exposure and joint evidence
Read-only observers use geometry/state snapshots, never wake evaluations or modified field/source arithmetic. Apply identical instrumentation to every arm and count observer work.
Preserve near-wake, tilt, motor/ground/contact and conservative sampled finite-jump stops. Do not smooth farStart or continue through unmodeled wake. No sampled failure does not prove continuous safety.

For each arm retain nearest abs(down-farStart) WITH simultaneous radial distance, half-width, neighbor-center distance, receiver/rotor/source IDs, tick/stage and normalized receiver/source states. Also retain minimum distance in (down,r) coordinates to the finite-jump annulus: hypot(down-farStart,max(0,0.15-r,r-outerAtFar)), with the same tuple. Do not combine unrelated minima to infer a safe joint condition. This distance uses the closed annulus[0.15,outerAtFar]; it is not a signed safety certificate. Preserve exact first-failure evidence.

Count all exposure events; archive only bounded first/worst paired witnesses, not dense wall rows. Log listed wall rows separately from repair. A conservative wall-response witness requires beforeWallResidual>1e-8, repair iterations>0, final wallResidual<=1e-9. The pre-repair velocity already passed the speed limiter, so significant residual identifies wall violation requiring repair. This misses corrections resolved in earlier projection passes: absence is not proof of no obstacle influence. Preserve controller tick, vehicle, wall rows and residuals.

Count accepted-endpoint C1 support entry/exit for the SAME ordered rotor/source pair:
- radial-cut membership r-3b changes(<0 versus>=0), while down>=farStart,down<2.5,center distance<3 hold at both endpoints;
- or axial-cut membership down-2.5 changes, while down>=farStart,r<3b,center distance<3 hold at both endpoints.
Preserve paired endpoint tuples/states for the first witness of each type. Exclude near/far jumps, inactive far-away pairs and RK trial backtracking. These are sampled transitions, not located continuous events.

Reference/domain/source/resource failures take precedence; preserve their original status. After numerical qualification, full event-stress evidence requires a wall-response witness AND a C1 support transition in J32,H8,P8 individually. Missing exposure then means EVENT_EXPOSURE_INSUFFICIENT. Numerical failure keeps its failure/unresolved status. No extension/placement change. Report arm exposure differences, clamps, saturation and neighbor events.

## Work and retention
Outer wall30s, cooperative27.5s, childCPU28s, supervisorCPU2s require explicit root adoption/admission before execution. One serial attempt; no descendants/paid compute. Scientific totals:11000steps,704000vehicle derivatives,7200production fields,357diagnostic fields,350controls,1baseline comparison. Compatibility adds8steps,512derivatives,1field,1controller,12scalar checks. Separate attempts/returns and count observer work. Equal fields do not imply equal total cost.

Campaign<=500000bytes including code/plans/reviews/receipts/results; results<=300000 with40000 failure reserve,20000 supervisor reserve. Save only J32 controller-grid states:51x16x17 doubles=110976bytes, compact summaries and bounded witnesses. Reference existing source/fixtures by hash without copying. No automatic retry, extension or publication.
