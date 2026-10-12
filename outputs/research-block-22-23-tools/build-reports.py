from pathlib import Path
import json,csv
root=Path(__file__).resolve().parents[1]
rows=[]
for stage in [22,23]:
 p=root/f'milestone-{stage}-summary.json'
 if not p.exists():continue
 data=json.loads(p.read_text());checks=json.loads((root/f'milestone-{stage}-comparisons.json').read_text());primary=[r for r in data if r['config']['dt']==.0025]
 lines=[f'# Milestone {stage} — '+('Local prediction development' if stage==22 else 'Frozen prediction evaluation on fresh flocks'),'','## Research question','',('Can position extrapolation recover the retained100ms delay failure, and what happens at200ms?' if stage==22 else 'How does the unchanged local predictor behave on six previously unused flocks in two known courses at100ms delay?'),'','## Method','', 'Each drone selects neighbors inside1.8m using the delayed measurement, then estimates positions as measured position + measured velocity × measurement age. No unseen drone is added by prediction. Velocities are held constant. Both self and neighbor positions are predicted; only low-level stabilization receives current self state. The original local Boids, inward guidance, sequential velocity filter and rigid-body physics remain unchanged. Airflow, noise and dropped observations are off. The map and route preferences are given. No central passage schedule is used.','',f'{len(data)} runs: '+('three development seeds, with an additional200ms stress on1103; every case at2.5 and1.25ms.' if stage==22 else '24 primary runs at2.5ms, plus14 predefined1.25ms refinements (all12 predicted cases and both raw1201 courses). No tuning after development; the candidate was not promoted because of the retained development failures.'),'','## Results','', '|Seed|Course|Delay ms|Observer|Finished|Stop time/reason|Minimum pair distance m|Minimum obstacle clearance m|Minimum connected /50|Final connected /50|','|---|---|---:|---|---:|---|---:|---:|---:|---:|']
 for r in primary:
  c,m=r['config'],r['metrics'];stop=f'{m["end"]:.4f}: {m["stopReason"]}' if m['stopReason'] else 'none'
  lines.append(f'|{c["seed"]}|{c["scenario"]}|{1000*c["observationDelay"]:.0f}|{c["estimator"]}|{m["passed"]}/50|{stop}|{m["minimum"]:.5f}|{m["obstacleMinimum"]:.5f}|{r["minimumConnected"]:.0f}|{m["final"]["largestFraction"]*50:.0f}|')
 for r in data:
  c,m=r['config'],r['metrics'];rows.append({'stage':stage,**c,'passed':m['passed'],'stop':m['stopReason'],'end':m['end'],'min_pair_m':m['minimum'],'min_obstacle_m':m['obstacleMinimum'],'min_connected':r['minimumConnected'],'final_connected':m['final']['largestFraction']*50})
 lines+=['','One whole run stops when any contact/model limit is reached. Unfinished drones are not independent collisions. Pair distance uses a conservative15cm center envelope, not resolved rotor geometry. Connectivity is sampled every0.1s using actual positions and a1.8m link distance. Completion and connectedness are separate outcomes.','','## Numerical checks','',f'{sum(c["passed"] for c in checks)}/{len(checks)} planned2.5→1.25ms comparisons pass. Acceptance requires identical finish count and stop reason, end-time difference below0.01s, and maximum final position difference below0.01m.','', '|Seed|Course|Observer|Delay ms|Maximum final difference m|Counts|Pass|','|---|---|---|---:|---:|---|---|']
 for c in checks:lines.append(f'|{c["seed"]}|{c["scenario"]}|{c["estimator"]}|{c["observationDelay"]*1000:.0f}|{c["difference"]:.8g}|{c["counts"]}|{c["passed"]}|')
 if stage==22:
  lines+=['','## Conclusion','', 'Prediction recovers completion for the saved100ms failure at both steps, but the recovered trajectory fails our numerical criterion (0.548546m final difference). At200ms, prediction causes contact while the original finishes at both steps. Delay effects are not monotonic in this nonlinear flock controller. Constant-velocity prediction is therefore not a validated replacement.','', 'The six observer implementation checks pass, including local visibility, immutability, zero-delay equivalence and exact raw-command/trajectory regressions. Those checks establish implementation behavior, not safe flocking.']
  ap=root/'milestone-22-refinement-audit.json'
  if ap.exists():
   a=json.loads(ap.read_text());q=a['comparison'];lines+=['','## Separate post-hoc finer-step audit','',f'The1.25→0.625ms comparison for1103/predict/100ms has maximum final position difference {q["difference"]:.8g}m; finish counts{q["counts"]}; pass={q["passed"]}. This extra run was specified after inspecting the failed planned comparison. It does not replace or erase that failure. See the separate audit protocol and saved trajectory.']
 else:
  lines+=['','## Conclusion','']
  for est in ['raw','predict']:
   g=[r for r in primary if r['config']['estimator']==est];n=sum(r['metrics']['passed']==50 and not r['metrics']['stopReason'] for r in g);fail=sum(bool(r['metrics']['stopReason']) for r in g)
   lines.append(f'{est}: {n}/{len(g)} complete50-drone runs; {fail} stopped runs. Minimum sampled connected group across these runs: {min(r["minimumConnected"] for r in g):.0f}/50.')
  lines+=['','These six seeds and two related courses are a small, deliberately specified evaluation. Drones within a flock are coupled;600 drone passages are not600 independent safety trials. The earlier200ms counterexample and100ms numerical failure remain relevant even if fresh primary cases succeed. No broad superiority, real-flight safety or calibrated latency tolerance is established.']
 lines+=['','## Records and reproduction','',f'[Three.js replay](milestone-{stage}-lab.html) · [Protocol](milestone-{stage}-protocol.json) · [All metrics](milestone-{stage}-summary.json) · [Full study states](milestone-{stage}-study.json) · [Numerical checks](milestone-{stage}-comparisons.json). Each individual run and its failure snapshot is saved in`milestone-{stage}-source/`. The viewer replays2.5ms trajectories, not live browser physics.','',f'Run `python3 research-reproduce.py --stage {stage} --node /path/to/node` from the outputs directory to verify hashes and rerun in an isolated copy.','']
 (root/f'milestone-{stage}-report.md').write_text('\n'.join(lines))
if rows:
 with (root/'research-block-22-23-trials.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
