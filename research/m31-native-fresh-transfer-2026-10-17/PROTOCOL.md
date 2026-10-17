# Fresh-state native-load transfer protocol

Status: prospective source preparation. No numerical execution is allocated until final source review, freeze and exact public verification. ADOPTED-DESIGN.md is authoritative for adopted scope; review/PROPOSED-TRANSFER.md records the earlier proposal and its explicitly narrowed lifecycle recommendation.

## Scientific question

Do the unchanged native F/L calculations reproduce the independently computed numerical model on two prospectively chosen post-initial Boids states? This challenges transfer beyond the six exposed retained states that passed the saved audit. It is a numerical implementation test, not physical validation or algorithmic novelty.

Within the original eight-step roadmap, this supports Steps3–4 numerical interaction verification and Step6 baseline calculation, using the Step5 local-flock workload. It does not complete Step7 coupled scaling or Step8 contribution evaluation.

## Frozen cases and measurements

Use fresh-a-t5/seed26171711 and fresh-b-t5/seed26171712. Each is a separate deterministic64-drone run of the unchanged wide-factory M31 Boids simulator, duration5s, dt0.0025s, frameEvery0.2s, grid neighbors, wall-priority filtering, ideal observation and airflow off. Shared broad route guidance is inherited and disclosed. Store both raw initial states and actual returned terminal states, every17-word drone row and saved pose sequence before any aerodynamic query. Full snapshot t5 must agree exactly with the corresponding pose/terminal capture. No interpolation, substitution or seed search.

Both scheduled states must survive to5s without stop, change from their initial states and show a change in relative geometry. Initial aerodynamic references are not evaluated. A target must not reproduce any of the six retained raw state inputs. Exact references must show at least one positive rotor interaction per fresh state; a missing, rejected, unresolved, unsupported or uncoupled case stays in the denominator and prevents overall success.

The reference stage runs once on four unchanged moving-admission controls and the two fresh states. The copied exact pair/semantic helpers are independent of the native producer; their fixed192-bit coefficient/source bounds and128 cubic bisections remain unchanged. No extra precision or refinement retry. Enforce maxDrones180 and actual allowed control sizes2/3 or target64 explicitly. Serialize independent roots and load enclosures directly; never run the old rational candidate merely to obtain a reference field.

Named Chrome runs the inherited48screen controls,6ownership builds,56Buffer adapter assertions,24native microcontrols and the four moving controls once per F/L method. Then four fresh calls: fresh-a F,L; fresh-b L,F. Every call starts from independently decoded current raw state, with no oracle coefficients or cached roots. Record intents, actual returned words, statuses, input/ownership evidence and diagnostics. No warmup or repetitions; diagnostic durations are not a performance campaign.

The saved checker preserves14fixed arithmetic fixtures and four fixed corruption laws. Use fresh-a F for altered load word, squared-force law and ID association; fresh-b F for wrong body/world-frame force. No favourable-row search. Missing witnesses fail the assertion. Native success alone is insufficient: require every identity, exact support, actual delivered load arithmetic/consumption, F/L parity and exact-reference accuracy gate.

Primary numerical tolerance remains1e-8 in every category: rotor maximum/(mg/4), collective/mg, Euclidean world force/mg and Euclidean world moment/(mgR). Reference uncertainty is included. Upper bound<=threshold passes; lower>threshold fails; overlap is unresolved. No average or changed tolerance can replace these checks. All targets and admitted accuracy controls must pass. Force is rotor thrust excluding gravity; moment excludes rotor reaction torque. Neither output is a measured physical prediction.

## Stage and operational policy

Four single-use stages: generation, reference, browser, check. Freeze sources/configuration/controls/runtime before generation and bind later generated outputs through completed attempt hashes. Generation requires both scheduled captures. Reference may complete with qualified=false; that stops progression to browser. A completed checker may report unqualified. Preserve failures and partial files, then stop dependent work without retries.

Per-stage child wall/CPU soft caps are120/600/120/180s; CPU hard caps are each+1s. Every child-written file is capped at32MiB. Cumulative supervisor runtime is at most1500s, with at most10s cleanup per stage; interstage human/source work is not scientific execution time. Combined new results, private logs and private profile/scratch are counted against256MiB before completion, including finalization reserves. This is a completion-time disk accounting rule, not a continuously enforced whole-disk ceiling. There is no enforced memory ceiling. Supervisor RSS is only supervisor memory. Wall-time and accounting enforcement require a live supervisor and awake host.

All four stages use the same resolved private log/scratch directory; its path digest is bound in every attempt and checked against predecessors so cumulative disk accounting includes their logs.

For nonbrowser stages retain and reap a sole Python/Node child. For browser stage retain the guardian until the controller finishes and the specific spawned Chrome root's exit and close events are confirmed. Normal success releases guardianR and reaps it without group signaling. Timeout/failure cleanup remains limited to owned live handles/groups and any permission/ownership/cleanup uncertainty stays failed. Never signal a group after its guardian has been reaped. This establishes root/controller event evidence only, not all-helper exit or hard containment.

Source/run.py and frozen config implement those caps and publication/preservation gates. Launch cutoff03:00UTC17October2026, with no automatic extension. Original native/saved-audit stages remain closed and immutable. All dispatches require explicit tool escalation. No paid resource, external contact or physical flight is included.

## Result and next decision

Report numerical and operational outcomes separately. Success requires both fresh targets to meet every fixed numerical gate and each prerequisite stage to satisfy its own operational completion contract. A two-state pass licenses consideration of a separate matched browser timing campaign, not that timing itself. A failure may motivate a new source decision, evaluated prospectively; never overwrite this record.

After the allocation, preserve raw evidence, independent review, clear claims/uncertainty, a readable milestone summary, actual-record Three.js update, privacy review and verified GitHub checkpoint. Generalization beyond this pair, speed, real coupled flight, physical accuracy and5000-drone feasibility remain open.
