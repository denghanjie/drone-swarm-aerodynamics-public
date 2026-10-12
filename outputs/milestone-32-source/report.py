"""Independent binary comparisons and provenance checks. Python standard library only."""
from pathlib import Path
import array,sys,json,math,hashlib
S=Path(__file__).resolve().parent; R=S.parent
def read(p): return json.loads(p.read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2))
def binary(p):
 a=array.array('d');a.frombytes(p.read_bytes())
 if sys.byteorder!='little':a.byteswap()
 return a
def positions(name):
 d=read(S/(name+'.json'));a=binary(S/(name+'-positions.f64'));stride=1+3*d['count']
 assert len(a)==d['frames']*stride
 return {round(a[k],6):[a[k+1+i*3:k+4+i*3] for i in range(d['count'])] for k in range(0,len(a),stride)}
def historical(name):
 d=read(R/'milestone-31-source'/(name+'.json'));a=binary(R/'milestone-31-source'/d['replay']['file']);stride=d['replay']['valuesPerFrame']
 return {round(a[k],6):[a[k+1+i*7:k+4+i*7] for i in range(1000)] for k in range(0,len(a),stride) if 20<=a[k]<=30}
def compare(a,b):
 rows=[]
 for t in sorted(a.keys()&b.keys()):
  errors=sorted(math.dist(x,y) for x,y in zip(a[t],b[t]));rows.append({'t':t,'maximum':max(errors),'median':(errors[499]+errors[500])/2,'p95NearestRank':errors[949]})
 return {'maximum':max(x['maximum'] for x in rows),'firstExceedance1cm':next((x['t'] for x in rows if x['maximum']>.01),None),'profile':rows}
checks=[]
def check(name,condition):
 checks.append({'name':name,'pass':bool(condition)})
 if not condition:raise AssertionError(name)
for n in ['milestone-32-protocol.json','milestone-32-checkpoint-protocol.json']:
 p=read(R/n)
 for rel,h in p['sourceHashes'].items():check(n+' source '+rel,hashlib.sha256((S/rel).read_bytes()).hexdigest()==h)
 for rel,h in p['inputHashes'].items():check(n+' input '+rel,hashlib.sha256((R/rel).read_bytes()).hexdigest()==h)
saved=read(R/'archive-before-visible-airflow/research-manifest.json');old=[e for e in saved['files'] if '-source/' in e['path'] and not e['path'].startswith('archive-')]
for e in old:check('Preserved '+e['path'],hashlib.sha256((R/e['path']).read_bytes()).hexdigest()==e['sha256'])
jobs=read(R/'milestone-32-protocol.json')['diagnostic']['jobs']+read(R/'milestone-32-checkpoint-protocol.json')['diagnostic']['jobs']
for j in jobs:
 d=read(S/(j['id']+'.json'));check(j['id']+' finite final',all(math.isfinite(v) for s in d['final'] for v in s));check(j['id']+' full window',d['frames']==101 and d['stop'] is None)
coarse=positions('closed-0.0025');fine=positions('closed-0.00125');quarter=positions('closed-0.000625');shift=positions('fine-start-0.0025')
hc=historical('heldout-2002-1000-narrow-wall-priority-0.0025');hf=historical('refinement-2002-1000-narrow-wall-priority-0.00125')
historicalCheck=compare(coarse,hc);check('Coarse checkpoint continuation exactly matches original coarse positions at all eleven integer seconds',historicalCheck['maximum']==0)
independent=[]
for row in read(R/'milestone-32-comparisons.json'):
 c=compare(positions(row['a']),positions(row['b']));check('Independent comparison '+row['a']+' / '+row['b'],abs(c['maximum']-row['maximum'])<1e-12);independent.append({'a':row['a'],'b':row['b'],**c})
initialA=read(R/'milestone-31-source/checkpoint-heldout-2002-1000-narrow-wall-priority-0.0025-20.json')['states'];initialB=read(R/'milestone-31-source/checkpoint-refinement-2002-1000-narrow-wall-priority-0.00125-20.json')['states']
componentErrors={name:max(math.dist(a[lo:hi],b[lo:hi]) for a,b in zip(initialA,initialB)) for name,lo,hi in [('position_m',0,3),('velocity_m_s',3,6),('quaternion_components_not_angle',6,10),('angularVelocity_rad_s',10,13),('rotorThrust_N',13,17)]}
followup={'sameStepDifferentStartingStates':compare(coarse,shift),'sameFineStartingStateDifferentSteps':compare(shift,hf),'historicalDifferentStatesAndSteps':compare(hc,hf),'initialComponentErrors':componentErrors,'coarseContinuationMaximumError':historicalCheck['maximum']}
save(R/'milestone-32-checkpoint-comparisons.json',followup);save(R/'milestone-32-independent-comparisons.json',independent)
save(R/'milestone-32-artifact-checks.json',{'checks':checks,'passed':len(checks),'historicalSourceFilesPreserved':len(old),'note':'Software/provenance checks, not physical validation. Primary JS trace p95 uses floor(.95*N) zero-based order statistic; this independent file uses nearest-rank p95 and conventional even-N median. Maximum errors are unaffected.'})
labels=['Same starting state, feedback: 2.5 vs1.25ms','Same starting state, feedback: 1.25 vs0.625ms','Identical motor commands: 2.5 vs1.25ms','Identical motor commands: 1.25 vs0.625ms']
table='\n'.join(f'|{label}|{row["maximum"]:.9g} m|' for label,row in zip(labels,independent))
same=followup['sameStepDifferentStartingStates']['maximum'];local=followup['sameFineStartingStateDifferentSteps']['maximum'];history=followup['historicalDifferentStatesAndSteps']['maximum']
summary=f'''# Milestone 32 — visible airflow and a better accuracy diagnosis

**We can now see the modeled interaction between drones. We have not validated it against real flight.**

Open the [Three.js wake lab](milestone-32-lab.html). Start with “Understand two drones”: the upper drone pushes air down, and the lower drone receives less predicted inflow when moved sideways. Return to the flock to see which neighbors influence each other. The moving dots are direction cues, not a fluid simulation.

The flock recordings come from milestone28, where airflow really did affect the equations of motion. The matched airflow-off flock finishes; the three coupled examples stop at contact or a model limit. They use the earlier controller. The successful5,000-drone missions still have airflow off.

**The new accuracy test points toward sensitivity to earlier state differences.** Starting all three step sizes from exactly the same saved flock at20s produces a maximum difference of {independent[0]['maximum']*1e6:.3g} micrometres for2.5vs1.25ms through30s. Starting from the two slightly different historical states, but using the same2.5ms step, instead produces {same*1000:.3g}mm. Their initial position difference was only {componentErrors['position_m']*1e6:.3g} micrometres, although velocity, attitude, angular rates and motor states also differed.

This is a diagnosis in one selected interval, not a fix or a proof of chaos. The three earlier full-trajectory checks remain failed. The next task is to identify which feedback decisions amplify the inherited differences, then evaluate a proposed correction on fresh cases. Physical measurements remain separately necessary.

All six prescribed diagnostic continuations are saved, with commands, position traces, full endpoints and controller summaries. [Detailed report](milestone-32-report.md) · [Frozen first plan](milestone-32-protocol.json) · [Separate follow-up plan](milestone-32-checkpoint-protocol.json).
'''
report=f'''# Milestone32 — airflow visualization and checkpoint diagnosis

## Goal and method

Make mutual aerodynamic influence inspectable, and distinguish fresh local integration differences from errors inherited before20s. This extends original steps3–5 and8; it does not close the eight-step research programme.

The first protocol was frozen before execution: restart the historical narrow seed2002 1,000-drone coarse state at20s; integrate through30s at2.5,1.25 and0.625ms with100Hz feedback. Replay the coarse run's exact four-motor targets on both finer grids. Keep the same swept contacts and floor checks. Store positions every0.1s, full endpoints, and all closed-loop motor targets and controller summaries. Airflow remains off in these numerical diagnostic runs.

A separately frozen post-hoc follow-up integrates the historical fine checkpoint at2.5ms. Its comparison to the existing historical fine-step trajectory is explicitly reused evidence. The two initial states differ in all dynamic components, not only position. These are development cases chosen after milestone31; there are no new acceptance thresholds or confidence claims.

## Results

|Comparison over20–30s|Maximum matched-drone position difference|
|---|---:|
{table}
|Same2.5ms step, different historical starting states|{same:.9g} m|
|Same fine starting state,2.5ms vs historical1.25ms|{local:.9g} m|
|Historical runs, both starting state and step differ|{history:.9g} m|

The first four rows use0.1s samples; rows involving historical recordings use their common1s grid. Same-step different-state comparisons use0.1s. All six new continuations reach30s without contact. The coarse-state/coarse-step continuation reproduces the historical coarse recording **exactly** at all11 common saved times, validating restart alignment. Maximum initial position difference is {componentErrors['position_m']:.9g}m; the complete component comparison is retained in [checkpoint comparisons](milestone-32-checkpoint-comparisons.json).

Interpretation: local integration changes from a common state are much smaller than the divergence reproduced by changing the inherited state while keeping the integration step fixed. Feedback-sensitive evolution matters in this selected window. No individual neighbor threshold, yaw rule, constraint projection, or mathematical chaos mechanism has yet been isolated. Smaller RK4 steps alone do not establish long-mission accuracy. The original1cm full-trajectory criteria remain failed. No numerical tuning or controller change is presented as a solution.

## What the airflow graphics mean

The four displayed recordings reuse corrected milestone28 seed1601,50 drones, wide factory, baseline controller. “Off” completes50/50 at the180s horizon. Linear-force coupling stops at13.2375s by obstacle contact; rotor-aware linear coupling stops at7.770s and RSS coupling at8.915s by vehicle model limits. These are historical outcomes, not new wall-priority trials. Every view includes original local Boids dynamics.

For every exact Float64 saved pose, the builder calls the existing corrected `aero.fields` implementation. This is possible without saved motor states because source amplitude is prescribed isolated-hover thrust. It yields a **reconstructed snapshot field**, not the field held during the original10ms coupling updates and not actual rotor loads. No interpolation is used for the numeric field. Course counts come from recorded crossing times. 1,708 static two-drone configurations expose unsupported near-wake geometry instead of inventing a continuation.

Teal envelopes follow the published normalized far-wake half-speed width, with the existing2.5m cutoff; bodies are enlarged2×, envelopes are to scale. Receiver rotor colors show scalar axial inflow, saturated at4m/s. Amber arrows show the strongest two individual source contributions above0.03m/s per receiver; their lengths are source–receiver distance, not force. In RSS mode they identify component magnitudes, not additive shares. Decorative moving dots indicate downward direction only: there is no advected fluid, vortex computation or wall-resolved flow. The displayed nearby factory walls are context; they do not redirect the modeled wakes. Playback advances exact snapshots every0.75 wall-clock seconds, unrelated to solver speed.

The static receiver estimate solves the constant ideal induced-power thrust hypothesis already used by milestone28. At0.8m directly below, predicted mean rotor inflow is about2.24m/s and lift loss18.3%. At0.6m sideways the existing radial cutoff gives zero. This zero is a truncated-model result, not a claim of zero physical air movement. The lower source's wake is omitted from the explanatory pair view because it does not affect the upper receiver in this downward-only model.

Omissions: calibrated motor/electrical response, source thrust feedback, wake transport, turbulence, moving-source relative flow, near wake, walls and ground. The [Bauersfeld et al. mean far-wake model](https://arxiv.org/abs/2403.13321v3) supplies the normalized profile. Its geometry mapping is corrected; physical measurement agreement is still unestablished. This is not CFD or a new aerodynamic law.

## Verification and reproduction

13 airflow checks pass, including self-exclusion, upstream behavior, cutoff, unsupported near wake, constant-power identity, half-width convention, binary frame lengths and decomposition of every valid reconstructed field into individual pair contributions. {len(checks)} numerical/provenance checks pass, including preservation of {len(old)} historical source-tree files. Six new diagnostic runs complete. None of these checks establish real-world safety.

From the project root, verify the final manifest with `python3 outputs/research-reproduce.py`. To rerun the diagnostics and regenerate fields in a copied tree, use `python3 outputs/research-reproduce.py --stage32 --node /path/to/node` with a space between `--stage` and `32`. No external packages are needed. The checkpoint follow-up uses its own source-directory metadata; all protocol sources and inputs are pinned.

Files ending `-positions.f64` contain little-endian Float64 rows `[time, x0,y0,z0, …]`,3,001 values per row;101 rows per new run. Closed-run `-commands.f64` files contain1,000 consecutive100Hz updates of1,000 drones×4 motor targets, held constant for10ms. JSON files contain final17-component states, control diagnostics and stopping outcomes. The independent Python comparisons use nearest-rank P95 and conventional median; the original JS comparison trace used zero-based floor indices. Maxima and all conclusions are identical.

Previous delivery pages and manifest are preserved in `archive-before-visible-airflow`. [Browser QA](milestone-32-qa.md) and [artifact checks](milestone-32-artifact-checks.json) document the delivered view. [Summary](milestone-32-summary.md) · [Original eight-step roadmap](research-roadmap.md).
'''
# Normalize prose spacing without touching linked paths or identifiers.
import re
for name,text in [('summary',summary),('report',report)]:
 for word in ['milestone','Milestone','step','steps','seed','successful','at','for','through','same','before','below','by','of','all','existing','and','with','every','over','vs','Same','historical','common','use','reach','original','completes','the','enlarged','above','At','about','loss','contain','consecutive','final']:
  text=re.sub(r'\b'+word+r'(?=\d)',word+' ',text)
 text=re.sub(r'(?<=\d)vs(?=\d)', ' vs ', text)
 text=re.sub(r'(?<=\d)(ms|mm|m|s|Hz)(?=[ .,;:()\n|/]|$)',r' \1',text)
 text=text.replace('2.5,1.25','2.5, 1.25').replace('1601,50','1601, 50').replace(';101','; 101').replace('`,3,001','`, 3,001')
 text=text.replace('1,000-drone','1,000-drone').replace('all11','all 11').replace('four-motor','four-motor').replace('at0.','at 0.').replace('at2.','at 2.').replace('width, with the existing2.','width, with the existing 2.')
 (R/f'milestone-32-{name}.md').write_text(text.replace('--stage32','--stage 32').replace('with a space between `--stage` and `32`.','as shown.'))
print(json.dumps({'checks':len(checks),'historicalFiles':len(old),'followupMaxima':[same,local,history],'comparisons':[r['maximum'] for r in independent]}))
