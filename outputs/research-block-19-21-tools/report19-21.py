from pathlib import Path
import json,math,hashlib
O=Path('outputs')
def table(rows):
 h=['|Seed|Controller|Step(ms)|Finished|Contact stop|Smallest connected group|Final connected group|','|---|---|---:|---:|---|---:|---:|']
 for r in rows:
  c,m=r['config'],r['metrics'];h.append(f"|{c['seed']}|{c['mode']}|{c['dt']*1000:g}|{m['passed']}/50|{m['stopReason'] or 'None'}|{round(r['minimumConnected'])}/50|{round(50*m['final']['largestFraction'])}/50|")
 return '\n'.join(h)
def numerical(stage):
 r=json.loads((O/f'milestone-{stage}-comparisons.json').read_text());h=['|Seed|Controller / scenario|Step pair(ms)|Maximum final position difference(m)|Finish counts|Pass1cm test|','|---|---|---|---:|---|---|']
 for q in r:
  label=q.get('mode',q.get('scenario',''))+(f" / delay{q['observationDelay']*1000:g}ms" if 'observationDelay' in q else '')
  h.append(f"|{q['seed']}|{label}|{q['dt']*1000:g}→{q['finerDt']*1000:g}|{q['difference']:.8g}|{q['counts']}|{'Yes' if q['passed'] else 'No'}|")
 return '\n'.join(h)
def integrity(stage,expected):
 records=json.loads((O/f'milestone-{stage}-study.json').read_text());p=json.loads((O/f'milestone-{stage}-protocol.json').read_text());d=O/f'milestone-{stage}-source';checks=[]
 checks.append({'name':'Expected unique trial count','passed':len(records)==expected and len({json.dumps(r['config'],sort_keys=True) for r in records})==expected})
 checks.append({'name':'Frozen source hashes unchanged','passed':all(hashlib.sha256((d/f).read_bytes()).hexdigest()==h for f,h in p['hashes'].items())})
 checks.append({'name':'All final values finite and crossing counts reconcile','passed':all(all(math.isfinite(v) for s in r['final'] for v in s) and sum(x is not None for x in r['crossings'])==r['metrics']['passed'] for r in records)})
 checks.append({'name':'Matched starting conditions identical','passed':all(r['initial']==next(q['initial'] for q in records if q['config']['seed']==r['config']['seed']) for r in records)})
 demo=json.loads((d/'demo.json').read_text());checks.append({'name':'All recorded replay endpoints match final states exactly','passed':all(r['frames'][-1][1:]==[v for s in r['final'] for v in (s[:3]+s[6:10])] and abs(r['frames'][-1][0]-r['metrics']['end'])<1e-7 for r in demo)})
 refs=json.loads((O/f'milestone-{stage}-comparisons.json').read_text());out={'softwareChecks':checks,'scientificNumericalAcceptance':{'passed':sum(q['passed'] for q in refs),'total':len(refs),'note':'Failures retained; software integrity is not scientific acceptance.'}}
 (O/f'milestone-{stage}-artifact-checks.json').write_text(json.dumps(out,indent=2));assert all(c['passed'] for c in checks),checks
 print(stage,out['scientificNumericalAcceptance'])
if (O/'milestone-19-study.json').exists():
 r=json.loads((O/'milestone-19-summary.json').read_text())
 s='''# Checkpoint19 — reject the simultaneous soft filter

The proposed smoother command filter is mathematically well behaved in isolated tests, but it worsens this flock-passage task. Do not promote it.

## What we tested

Three previously troublesome starting flocks, two controllers, three physics steps:18 runs. Both controllers use identical checkpoint18 inward map guidance and the same local3D Boids, rigid-body dynamics and contact detection. This is development evidence, not new holdout evidence. The fixed controller period is10ms. See the [frozen protocol](milestone-19-protocol.json) and [filter method](milestone-19-source/method.md).

## What happened

At5ms the previous controller completed150/150 passages; the new soft filter completed84/150. None of the18 runs stopped for contact. The new filter failed all6 adjacent time-step comparisons; seed1002 changed33→27→25 completions. The old controller passed5/6 comparisons, including all three2.5→1.25ms comparisons. Its1002 coarse comparison still fails and remains in the record. Seed905 here uses inward guidance; do not conflate it with the earlier steering-only seed905 counterexample.

'''+table(r)+'''

## Numerical evidence

'''+numerical('19')+'''

The solver test suite covers analytic half-space solutions, finite-difference gradients, linear solves, reversed constraint ordering and conflicting random constraints. These checks pass. The largest gradient residual during the nine soft-filter runs is below1e-6. This verifies the local soft-objective solution, not the safety or convergence of an entire trajectory. A speed cap applied after optimization can further violate constraints. Long-horizon divergence may involve nonlinear amplification as well as controller transitions; these experiments do not identify a single root cause.

## Decision and records

Retain the previous controller as a provisional reference. Preserve this unsuccessful replacement for diagnosis; do not claim smoothing solved numerical sensitivity. [3D comparison](milestone-19-lab.html), [full final states and samples](milestone-19-study.json), [all numerical comparisons](milestone-19-comparisons.json), [solver checks](milestone-19-solver-checks.json). Individual files in the source directory retain complete runs and recorded trajectories.
'''
 (O/'milestone-19-report.md').write_text(s);integrity('19',18)
if (O/'milestone-20-study.json').exists():
 r=json.loads((O/'milestone-20-summary.json').read_text());refs=json.loads((O/'milestone-20-comparisons.json').read_text());coarse=[q for q in r if q['config']['dt']==.005]
 s='''# Checkpoint20 — stronger guidance and fixed heading do not solve passage

We tested two specific explanations for the failed soft filter: weak sideways guidance within an opening, and large heading changes near zero speed. A2×2 comparison includes the unchanged soft reference from19 plus three new combinations. The new27 runs cover the same three development seeds at5,2.5,1.25ms. No new seed was used for tuning.

Center guidance replaces the zero lateral preference inside the target aperture with a preference toward its center, capped at the same lateral speed. The same centering error also feeds the existing forward-speed reduction, so this treatment changes lateral attraction and forward slowing together; it is not a pure lateral-gain ablation. Fixed heading holds the world yaw target at0 while retaining3D translation. Each drone still uses local separation, alignment and cohesion. No passage slots, global flock center or global connectivity constraint were added. The comparison changes known-map guidance, not route discovery.

## Results

'''
 for mode in ['soft-fixedyaw','soft-center','soft-center-fixedyaw']:
  a=[q for q in coarse if q['config']['mode']==mode];s+=f"- {mode}: {sum(q['metrics']['passed'] for q in a)}/150 completed at5ms.\n"
 s+=f"\nThe old soft reference completed84/150, and the prior interior controller completed150/150 in19. {sum(q['passed'] for q in refs)}/{len(refs)} new adjacent-step comparisons passed the1cm criterion. Contact stops across the27 new runs: {sum(q['metrics']['stopReason'] is not None for q in r)}.\n\n"+table(r)+'\n\n## Numerical checks\n\n'+numerical('20')+'''

## Decision

Do not promote any of these variants. Stronger map centering improves completion relative to the unsuccessful soft reference, but does not restore all-drone passage or consistent trajectories. Fixed heading does not resolve the sensitivity. This does not prove heading has no effect; it rules out treating this particular heading change as a sufficient fix.

The software checks verify exact reproduction of the unmodified soft controller, invariance to agent ordering within numerical precision, and no response to a far-away invisible drone. These are implementation checks, not successful research outcomes. The frozen optimization parameters and physical plant were unchanged. Timings in parallel execution are not a controlled speed benchmark.

[3D comparison](milestone-20-lab.html) · [Protocol](milestone-20-protocol.json) · [Full trial records](milestone-20-study.json) · [Software checks](milestone-20-control-checks.json). The viewer includes three exact reference replays from19 plus nine new5ms replays. Run `build-replay.cjs` after the study to assemble them without rerunning simulations.
'''
 (O/'milestone-20-report.md').write_text(s);integrity('20',27)
if (O/'milestone-21-study.json').exists() and (O/'milestone-21-failure-audit.json').exists():
 r=json.loads((O/'milestone-21-summary.json').read_text());primary=[q for q in r if q['config']['dt']==.0025];refs=json.loads((O/'milestone-21-comparisons.json').read_text());audit=json.loads((O/'milestone-21-failure-audit.json').read_text())
 s='''# Checkpoint21 — a100ms observation delay exposes a contact failure

The unchanged reference controller can pass the tested courses under ideal observation, but a new starting flock reaches the drone-to-drone contact limit when high-level observations are100ms old. This is evidence against treating the controller as robust to that delay.

## Experiment

Four fresh seeds(1101–1104), two courses(tight staggered openings and a three-obstacle slalom), three observation delays(0/50/100ms):24 primary runs at2.5ms. Eight refinements at1.25ms were selected before outcomes were known. After the first contact stop we added a separately documented four-run audit: exact replays and refinements of the failed case and its ideal counterpart. Total36 numerical executions; two are exact replay regenerations, not additional independent cases.

The controller is the frozen checkpoint18 inward-guidance/local Boids controller. High-level steering sees a coherent delayed snapshot of self and neighbors. At startup it holds the initial snapshot until delayed data is available. Low-level stabilization still uses exact current own state. Contact detection always uses true current geometry. This models high-level observation lag, not a calibrated radio system: no noise, packet loss, asynchronous clocks, wake forces or uncertain onboard stabilization are included.

## Fresh primary outcomes

|Course|Delay(ms)|Runs finishing50/50|Contact-stop runs|Total individual passages|Worst sampled largest group|Final disconnected runs|
|---|---:|---:|---:|---:|---:|---:|
'''
 for course in ['tight','slalom']:
  for delay in [0,.05,.1]:
   a=[q for q in primary if q['config']['scenario']==course and q['config']['observationDelay']==delay]
   s+=f"|{course}|{delay*1000:g}|{sum(q['metrics']['passed']==50 for q in a)}/{len(a)}|{sum(q['metrics']['stopReason'] is not None for q in a)}|{sum(q['metrics']['passed'] for q in a)}/{50*len(a)}|{min(q['minimumConnected'] for q in a):g}/50|{sum(q['metrics']['final']['largestFraction']<1 for q in a)}|\n"
 s+='''
These are small matched deterministic samples. Drones within one flock are not independent trials. A stopped run is terminated for all drones; unfinished counts after a stop are not50 individually observed collisions. Connectivity is measured at the unchanged1.8m radius; a connected group can still reach the contact limit.

|Seed|Course|0ms outcome|50ms outcome|100ms outcome|
|---|---|---|---|---|
'''
 for seed in [1101,1102,1103,1104]:
  for course in ['tight','slalom']:
   row=[str(seed),course]
   for delay in [0,.05,.1]:
    q=next(q for q in primary if q['config']['seed']==seed and q['config']['scenario']==course and q['config']['observationDelay']==delay);m=q['metrics'];row.append(f"{m['passed']}/50"+(f"; stop{m['end']:g}s" if m['stopReason'] else '; no stop'))
   s+='|'+'|'.join(row)+'|\n'
 s+='\n## Numerical checks\n\n'+numerical('21')
 s+=f"\n{sum(q['passed'] for q in refs)}/{len(refs)} preregistered refinements pass the1cm endpoint, same-count/same-stop test. Failed comparisons remain failures; matching completion alone does not override them.\n"
 s+='\n### Post-hoc contact audit\n\n|Delay(ms)|Stop times at2.5/1.25ms|Finish counts|Final-position difference(m)|Numerical acceptance|Exact replay|\n|---|---|---|---:|---|---|\n'
 for q in audit:s+=f"|{q['observationDelay']*1000:g}|{q['end']}|{q['counts']}|{q['difference']:.8g}|{q['passed']}|{q['exactReplay']}|\n"
 s+='''
At the original stop(10.1725s), drones20 and47(zero-based IDs) are approximately0.14974m apart and closing at0.222m/s. This crosses the model's0.15m center-distance envelope. It is a conservative proximity failure, not a resolved rotor-contact simulation. The separate [diagnostic](milestone-21-contact-diagnostic.json) retains positions, actual velocities and last requested velocities. The replay marks the closest pair in red.

## Decision

Keep the reference as an experimental baseline, not a demonstrated delay-robust controller. Study a local delay-compensated avoidance/arrival rule next, retaining this failure and checking on new seeds before adoption. Do not use additional integration refinement to conceal an observation-model failure. Physical validation, airflow coupling, actual flock GPU scaling and scientific novelty remain open.

[3D replay](milestone-21-lab.html) · [Frozen protocol](milestone-21-protocol.json) · [Full records](milestone-21-study.json) · [Post-hoc audit protocol](milestone-21-failure-audit-protocol.json) · [Audit final states](milestone-21-failure-audit-runs.json) · [Delay implementation checks](milestone-21-delay-checks.json).
'''
 (O/'milestone-21-report.md').write_text(s);integrity('21',32)
