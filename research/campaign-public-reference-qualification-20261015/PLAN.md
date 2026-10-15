> Public edition of the preserved original, SHA256 `170a53fccc8ea0962f7d829135805b5ffffd62c4f4d9b89320481cc131faf4fd`. Public dependency links replace local working-document paths; private storage-admission/release details are omitted. Its original prospective NOT RELEASED status is historical: one later released qualification stopped, as recorded in results/summary.json. No new execution release follows from this export.

# Public numerical reference: frozen prospective protocol

Status: implemented for static review, NOT RELEASED. Root must create a hash-bound release and launch the supervisor once. This campaign is new; no old R8/reference failure is overwritten or retroactively qualified.

## Scientific scope

Test numerical consistency of the pinned public finite-support sum-rotor model under genuine own-state local-3D Boids. No parameter, cutoff, source strength, near-field rule, controller, derivative or integrator physics changes. The 2026 amplitude screen found all six published true-axis markers below fixed-nominal predictions by 0.629–0.760 m/s, including its self-similar stratum. Unknown measurement/parameter error and mean-speed versus axial-velocity mismatch remain. Numerical agreement here is never physical truth or validation; no refit or physical safety claim follows. See the primary 2026 source and scope caveat in SOURCE-LEDGER.md.

Public commit: 1336f5c416875a9651f92b58b2ed06649f25b04e. The original closure, represented here by SOURCE-MAP.json, pins the 15 functional files and already-retained compatibility tensor. The driver loads original source strings through an in-memory CommonJS path map with their original relative-path semantics; only fs/path/crypto built-ins are allowed. No duplicate source tree, custom arithmetic, private archive or external dependency. Explicit factory variant=wide. All source bytes are verified before import and after execution. A published initializer/controller is used, never a scripted replacement.

## Fixed design and ordering

config.json is authoritative for exact numerical constants. N=16; seeds840131/840137; Q=1/51200 s; controls every512ticks; common accepted-state observations every128ticks. Qualification horizon5120ticks=0.1s; extension51200ticks=1s requires a separate release after review. No automatic retry, extra seed or refinement.

First, public compatibility: B.initial(4301,16) and four held steps h128/air512 must match all first five saved public s4301 states byte-for-byte. Only public saved bytes are used. Stop on mismatch.

Gate A: joint physical steps128/64/32ticks, both seeds, before any held arm. All stages use a synchronized whole-swarm trial, normalized geometry for the unchanged field, raw state for derivative, then normalized accepted endpoint. Controls are fixed within a control interval. All arms deep-copy one initial state per seed and use their own evolving state at identical controller clocks; command values are allowed to diverge.

Gate B: airflow hold periods128/64/32ticks, each at physical steps16/8ticks. h-halving is checked separately for every fixed airflow period; temporal-hold convergence compares h8 arms. At shared event ticks, refresh field, update controls, then integrate. Held winds are fixed throughout all RK stages until the next refresh. No terminal production refresh/control update. Joint stage4 geometry is not an accepted endpoint.

The two gates use nine arms per seed. Compatibility is additional. Before proceeding, all source/config/event/work counts must match. Compare the first production lean field per seed against A.fields(sum-rotor) on identical geometry. Assert accepted-state and command inputs were not mutated. No heavy historical audit replay.

## Observations and acceptance

Compare all vehicles at every common tick: max position/velocity/attitude/angular-rate norm and nominal-rotor difference, location, paired17-state witness, and terminal metric values. Attitude uses normalized relative-quaternion 2atan2(vectorNorm,abs(scalar)), sign-invariant. Also retain command differences/signature mismatch counts and per-rotor inflow, force, roll/pitch load differences at controller ticks.

IMPORTANT: diagnostic incoming held winds are sampled on arrival at a controller tick BEFORE scheduled refresh, versus a fresh endpoint field. Initial sampling follows initialization; terminal sampling adds no production refresh. Record field age. Post-refresh sampling would erase lag because every airflow period divides the control period. Fresh joint endpoint fields are auxiliary, never aliases for stage4. These diagnostic comparisons are sampled, not full-time maxima.

Exposure includes nonzero production fields, max inflow, contributions, all-pair signed guard/support margin extrema, controller neighbor/constraint/clip/repair counts, and control-grid clearance minima. Show zero exposure explicitly. Changed-pair-signature counts are sample visitation changes, not individual-bit or physical-event counts; equal-time RK trial states are not ordered physical times. Short flights may miss obstacles, boundaries, substantial airflow variation and long-horizon instability. No general reference qualification follows.

Numerical caps for position(m), velocity(m/s), attitude(rad), angular-rate(rad/s): small=(1e-4,1e-4,1e-4,1e-3), outer=(1e-3,1e-3,1e-3,1e-2), floors=(1e-8,1e-8,1e-7,1e-7). These are approximation goals, not physical tolerances. Coarser proposed steps do not loosen caps or qualify historical runs.

Per seed/family: joint fine-pair <=small and <=max(floor,0.6*coarse-pair). Every held h-pair <=small. Cross-family errors at air64 and air32 <=outer and <=max(floor,0.7*preceding-cadence error); finest cross-family also <=outer. For resolved temporal attribution at each cadence, max(joint fine h-difference, held h-difference) <=10% of held-vs-joint32 error. When error<=floor, both numerical differences must also be<=floor and no lag-order attribution is made. These observed differences are self-consistency evidence, not certified error bounds. Nonzero airflow exposure is required. Any gate failure stops and preserves its evidence.

## Domains, failure and retention

Unchanged model guards and endpoint contact tests remain. Compact monitoring retains the old near-wake throw only for center distance<neighborRadius and down>0, down<farStart, radial<nearRadius. Finite-jump screen includes ALL ordered rotor/source pairs: stop when minDown<=farStart<=maxDown, minRadial<outerAtFar and maxRadial>=nearRadius over step samples. Joint samples include normalized stage geometry and accepted endpoints; held samples are endpoint-only. This is conservative sampled risk, not continuous regularity/contact proof. Controller repair failure also stops.

Common-grid state arrays remain in RAM. Persist only finest-joint controller-grid full17 states (47,872B both seeds at0.1s;439,552B at1s), all metric maxima/terminal values and bounded paired-vehicle witnesses, source/config hashes, coverage, run/exposure summaries and first failure. Other complete trajectories/command tapes are not retained. Worst witnesses can be independently checked; all dense maxima cannot be recomputed without rerunning. Completed references survive later failure. Hard-kill progress is a last durable tick, not exact failed state. Held integrator errors retain exact input when available, never claim inaccessible internal stage state.

Stopped attempts retain bounded state matrices (<=28KB) plus failure metadata and terminal summary. No hidden retries or post-result tuning. Failure statuses distinguish GATE_STOP, STOPPED and SOURCE_CHANGED. The original failed public reference, denied private-R8 recovery and measured-screen gate failures stay separate and unchanged.

## Resource and release contract

Full qualification matrix:6320physical steps,3360production fields,180controls; extension core counts10x. Compatibility adds4steps/1field/1control. Fresh diagnostics add198/1818fields; baseline comparisons add2fields. Single serial times are resource observations, not speedups.

Hard outer wall limit20/60s, child termination begins18/58s. Driver cooperatively stops at17.5/57.5s wall or CPU, including serialization checks. RLIMIT_CPU child hard18/58s plus supervisor hard2s (soft1s) bounds the two processes' allotted CPU to20/60s; driver creates no descendants. Actual CPU and wall are reported separately. RSS is observed, not hard-limited. No paid compute.

