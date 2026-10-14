# Append-only pre-evaluation amendments

## A1 — owned output and whole-pipeline comparison (2026-10-13, before implementation)

Independent review requested a drop-in lifetime contract and end-to-end attribution. The reuse variant will reuse internal geometry and pair flags only. Every fields/evaluator result owns fresh winds arrays that remain unchanged by later calls. No borrowed-output speed result is part of the five-variant primary comparison; no copying cost is hidden.

After gates pass, time the fixed-work genuine Boids simulation with recording disabled, exactly the same initial state and number of steps, including field preparation, controller, RK4 and safety checks. Use development seed4301,N16,1second, legacy/previous-zero/selected, three serial balanced-order repetitions after one warmup each. Retain total/field/controller/physics/safety times; no end-to-end speed claim if intervals or absolute times do not support it. Held-out replay runs remain separate evidence. All timing counts toward the30-minute ceiling and requires the same exclusive lease.

## A2 — pre-timing repetition count and numeric input domain (2026-10-13)

The preregistered protocol requires seven, rather than three, balanced paired repetitions of the fixed-work whole-pipeline benchmark (one warmup per variant). All members must complete identical simulated work. This change precedes timing.

Independent tiny audit identified a pre-existing nontermination hazard at huge finite grid coordinates (1e20), where integer-loop increments no longer advance. New variants explicitly reject any position component with absolute value above1e6m. This is numerical API hardening outside the flight fixtures, not an assertion that legacy has equivalent malformed-input behavior. The accepted coordinate scope is now finite17-element states, unit quaternion tolerance1e-10, abs(position)<=1e6m. Conservative exact-zero envelopes add128*Number.EPSILON*1e6m to cover coordinate addition/subtraction roundoff at this declared limit; unit-quaternion envelope inflation remains. Original pre-amendment source retained as source-versions/exact-aero-v0.cjs.txt. No held-out or timing results existed when this changed.

## A3 — retained v0 failure and timing integrity (2026-10-13, before timing)

Independent audit preserved a concrete v0 false cull: receiver at(0,3e14,1), yaw45degrees; source at(0,3e14+0.5,1+d), where d=.45/(3*spread)+origin*motorDistance=1.4954986372761618. Legacy/lean rotor0 inflow was0.001587065203100887m/s, while v0 support/reuse returned0. Position rounding enlarged the actual rotated-rotor offset beyond the nominal envelope. A2's explicit position bound rejects that input and its conservative coordinate margin protects accepted coordinates; this is a retained implementation failure, not a physical finding.

Independent pre-timing harness review requires complete four-rotor/load output checksums against untimed deterministic results, incremental raw-row persistence and retained exceptions, source/input hashes before and after evaluation, plus memory/process observations. Output checksum calculation occurs after timed batches; outputs are retained temporarily for checking. The receiver-only measurement invokes identical load code and saved fields under every label; it is a repeated noise/negative control, never variant-specific acceleration. Runtime/memory observations are retained privately and redacted for public checkpoints with a disclosed editorial manifest.

## A4 — Boids schedule validation (2026-10-13, before Boids or timing)

Independent harness inspection requested explicit allowed-step checks. The Boids runner now rejects physics steps outside{2.5,1.25}ms, airflow steps outside{10,5}ms, nonfinite duration and non-integral field/control/frame/duration schedules. Planned cadences are unchanged. Benchmark setupMs means empty evaluator/scratch construction only; first geometry storage allocation occurs during documented warmup and is not presented as a full one-shot setup cost.

## A5 — timed whole-pipeline terminal-state integrity (2026-10-13, before primary pipeline timing)

Independent review requested deterministic terminal-state verification while recording remains disabled. Every primary timed Boids member now saves SHA256 of all final17-entry states and last held four-rotor winds, calculated after its measured total interval, and compares against a completed legacy warmup. Config, completed step count, field updates and end time are retained. This changes the harness only; airflow method6111d7a7 and frozen timing work/cadences are unchanged. Earlier independent whole-pipeline completion checks are not retroactively claimed as bitwise terminal-state verification.

## A6 — independent pipeline integrity clarification (2026-10-13, report audit)

A5's final sentence was too broad. Independent raw pipeline records already retained matching final full-state hashes and zero final-state difference for all27timed members. They lacked terminal held-wind hashes only. The primary A5 addition verifies both final states and held winds. This reporting correction does not change any method, timing or outcome.
