from pathlib import Path
import json,math,struct,hashlib
root=Path(__file__).resolve().parent.parent;d=root/'milestone-30-source';protocol=json.loads((root/'milestone-30-protocol.json').read_text());runs=[];checks=[]
def check(ok,label):
 checks.append(dict(passed=bool(ok),check=label))
 if not ok:raise AssertionError(label)
def frames(r,folder):
 raw=(folder/r['replay']['file']).read_bytes();w=r['replay']['valuesPerFrame'];v=struct.unpack('<'+'d'*(len(raw)//8),raw);return [v[i:i+w] for i in range(0,len(v),w)]
for rel,h in protocol['sourceHashes'].items():check(hashlib.sha256((d/rel).read_bytes()).hexdigest()==h,'frozen '+rel)
for job in protocol['jobs']:
 r=json.loads((d/(job['id']+'.json')).read_text());runs.append(r);f=frames(r,d);n=job['count'];check(all(r['config'][key]==job[key] for key in ['seed','filter','count','dt','duration']) and r['config']['mode']=='boids' and r['config']['airflow']=='off' and r['config']['observation']=='ideal','configuration '+job['id']);check(r['replay']['valuesPerFrame']==1+7*n,'frame layout '+job['id']);check(r['diagnostics']['updates']==n*math.ceil(r['metrics']['end']/.01-1e-8),'control update accounting '+job['id']);check(len(f)==r['replay']['frames'],'frame count '+job['id']);check(all(math.isfinite(x) for row in r['initial']+r['final'] for x in row),'finite states '+job['id']);check(all(math.isfinite(x) for row in f for x in row),'finite replay '+job['id']);check(all(math.isfinite(v) for v in r['diagnostics'].values()),'finite diagnostics '+job['id']);check(f[0][0]==0 and f[-1][0]==r['metrics']['end'],'replay endpoints '+job['id'])
 for rows,frame in [(r['initial'],f[0]),(r['final'],f[-1])]:check(all(list(frame[1+7*i:8+7*i])==s[:3]+s[6:10] for i,s in enumerate(rows)),'exact poses '+job['id'])
 check(all(abs(sum(s[k]*s[k] for k in range(6,10))-1)<1e-10 for s in r['final']),'unit quaternions '+job['id'])
 check(all(f[i][0]<f[i+1][0] for i in range(len(f)-1)),'increasing frame times '+job['id'])
 check(r['metrics']['end']<=job['duration'] and (r['metrics']['stopReason'] is not None or r['metrics']['end']==job['duration']),'terminal accounting '+job['id'])
 check(r['metrics']['passed']==sum(t is not None for t in r['crossings']),'crossings '+job['id'])
 if r['metrics']['stopReason']:
  check(r['lastControl']['t']<r['metrics']['end'] and r['metrics']['end']-r['lastControl']['t']<=.01000001,'actual preceding control '+job['id'])
for seed in [1901,1902]:
 for count in [50,1000]:
  pair=[r for r in runs if r['job']['seed']==seed and r['job']['count']==count and r['job']['kind']=='heldout']
  if len(pair)==2:check(pair[0]['initial']==pair[1]['initial'],'matched initial '+str((seed,count)))
comparisons=[]
for b in runs:
 if b['job']['kind']!='refinement':continue
 a=next(r for r in runs if r['job']['kind']=='heldout' and all(r['job'][k]==b['job'][k] for k in ['count','seed','filter']))
 check(a['initial']==b['initial'],'refinement initial '+b['job']['id'])
 fa={round(f[0],8):f for f in frames(a,d)};fb={round(f[0],8):f for f in frames(b,d)};times=sorted(set(fa)&set(fb));maximum=max(math.dist(fa[t][1+7*i:4+7*i],fb[t][1+7*i:4+7*i]) for t in times for i in range(a['config']['count']))
 def identity(r):
  f=r['metrics']['failure'];return None if not f else (f.get('drone'),f.get('pair'),[x['id'] for x in f.get('hits',[])])
 comparisons.append(dict(coarse=a['job']['id'],fine=b['job']['id'],commonSavedTimes=times,maximumSynchronizedPositionDifference=maximum,withinOneCentimeter=maximum<.01,terminalTimes=[a['metrics']['end'],b['metrics']['end']],sameEventIdentity=identity(a)==identity(b) and a['metrics']['stopReason']==b['metrics']['stopReason'],samePassageCount=a['metrics']['passed']==b['metrics']['passed'],scope='Only exact common saved frames, not a bound between frames or physical validation'))
(root/'milestone-30-comparisons.json').write_text(json.dumps(comparisons,indent=2));(root/'milestone-30-artifact-checks.json').write_text(json.dumps(dict(checks=len(checks),passed=all(c['passed'] for c in checks),details=checks),indent=2))
index=[dict(config=r['config'],metrics=r['metrics'],job=r['job'],file=r['job']['id']+'.json',geometry='factory-wide.json') for r in runs]
for n in [1000,5000]:
 name=f'primary-1501-{n}-wide-0.0025.json';r=json.loads((root/'milestone-26-source'/name).read_text());index.append(dict(config={**r['config'],'filter':'baseline'},metrics=r['metrics'],job={**r['job'],'kind':'historical baseline'},file='../milestone-26-source/'+name,geometry='factory-wide.json',replayDir='../milestone-26-source/'))
(d/'index.json').write_text(json.dumps(index))
import csv
with (root/'milestone-30-trials.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['role','seed','count','filter','dt_s','planned_horizon_s','actual_end_s','passed','stop_reason','failure','wall_residual_max_mps','pair_residual_max_mps','unconverged_solves','minimum_sampled_obstacle_clearance_m','minimum_sampled_drone_spacing_m','minimum_connected_fraction'])
 for r in runs:
  j=r['job'];m=r['metrics'];v=r['diagnostics'];writer.writerow([j['kind'],j['seed'],j['count'],j['filter'],j['dt'],j['duration'],m['end'],m['passed'],m['stopReason'] or '',json.dumps(m['failure']),v['maxWallAfter'],v['maxPairAfter'],v['unconverged'],m['minimumSampledObstacleClearance'],m['minimumSampledSeparation'],m['minimumConnectedFraction']])
rows=[]
for r in runs:
 j=r['job'];m=r['metrics'];rows.append(f"|{j['kind']}|{j['seed']}|{j['count']}|{j['filter']}|{j['dt']*1000:g}|{m['end']:.4f}|{m['passed']}|{m['stopReason'] or 'horizon reached'}|")
text='''# Milestone 30 — wall-priority avoidance

This experiment asks whether repairing wall-clearance commands after the old pair filter prevents the saved large-flock wall contacts. All runs keep local 3D Boids, shared route guidance and rigid-body dynamics. Airflow is off and observations ideal.

## Every planned run

Large-flock tests cover the first 20 seconds only. The 50-drone tests cover 180 seconds. Reaching a short horizon is not completing a factory mission.

|Role|Seed|Drones|Filter|Step ms|End seconds|Finished|Outcome|
|---|---:|---:|---|---:|---:|---:|---|
'''+ '\n'.join(rows)+'\n\n## Command diagnostics\n\nWall priority can repair a wall request while violating requests to separate from other drones. Values below count drone-control updates, not independent trials or collisions. A finite-iteration nonconvergence flag does not prove infeasibility.\n\n|Trial|Wall violations before → after|Largest wall residual after m/s|Pair violations after|Nonconverged solves|\n|---|---:|---:|---:|---:|\n'
for r in runs:
 v=r['diagnostics'];text+=f"|{r['job']['id']}|{v['wallViolationsBefore']} → {v['wallViolationsAfter']}|{v['maxWallAfter']:.6g}|{v['pairViolationsAfter']}|{v['unconverged']}|\n"
geometry=json.loads((d/'factory-wide.json').read_text());plane=max(b['max'][0] for b in geometry['boxes'] if b['id'].startswith('partition-0-'))+.075
exploration=[]
for r in runs:
 if r['config']['count']>=1000 and r['config']['filter']=='wall-priority' and r['job']['kind']!='refinement':
  exploration.append(dict(trial=r['job']['id'],end=r['metrics']['end'],threshold=plane,centersBeyondFirstPartitionWithBodyRadius=sum(s[0]>plane for s in r['final']),meanForwardDisplacement=r['metrics']['final']['center'][0]-sum(s[0] for s in r['initial'])/len(r['initial'])))
(root/'milestone-30-exploratory-progress.json').write_text(json.dumps(dict(scope='Post-hoc descriptive check, not a prespecified success criterion or first-passage counter; not full mission completion.',records=exploration),indent=2))
text+='\n## Does the flock still move?\n\nThis post-hoc descriptive check was added after the two fresh-seed candidate outcomes. It counts final centers beyond the first partition’s far face plus the body radius (x > 0.255 m). It does not count completed factory missions or establish freedom from later stalls.\n\n|Candidate trial|End s|Beyond first partition|Mean forward displacement m|\n|---|---:|---:|---:|\n'
for a in exploration:text+=f"|{a['trial']}|{a['end']:.4f}|{a['centersBeyondFirstPartitionWithBodyRadius']}|{a['meanForwardDisplacement']:.3f}|\n"
traces=[]
for r in runs:
 for a in r['lastControl']['affected']:
  for wall in a['walls']:
   n=wall['n'][:3];command=sum(x*y for x,y in zip(n,a['velocity']));actual=sum(x*y for x,y in zip(n,a['actual']));traces.append(dict(trial=r['job']['id'],drone=a['drone'],controlTime=r['lastControl']['t'],eventTime=r['metrics']['end'],normal=n,requiredAwayVelocity=wall['lower'],commandedAwayVelocity=command,actualAwayVelocity=actual,commandDeficit=max(0,wall['lower']-command)))
(root/'milestone-30-precontact-commands.json').write_text(json.dumps(traces,indent=2))
text+='\n## Actual commands before contact\n\nThese are saved at the preceding control update, not recomputed at the terminal state. Each row is one active wall constraint for a contact-involved drone; the normal alone does not uniquely identify the box. Negative away velocity means motion toward that surface.\n\n|Trial / drone|Command time s|Contact time s|Required away m/s|Commanded away m/s|Actual away m/s|\n|---|---:|---:|---:|---:|---:|\n'
for a in traces:text+=f"|{a['trial']} / {a['drone']}|{a['controlTime']:.5f}|{a['eventTime']:.5f}|{a['requiredAwayVelocity']:.5f}|{a['commandedAwayVelocity']:.5f}|{a['actualAwayVelocity']:.5f}|\n"
text+='\n## Numerical refinement\n\n'
for c in comparisons:text+=f"- {c['fine']}: maximum synchronized position difference **{c['maximumSynchronizedPositionDifference']:.8g} m**, 1 cm test **{c['withinOneCentimeter']}** across {len(c['commonSavedTimes'])} exact common saved frames through {c['commonSavedTimes'][-1]} s. Same terminal event identity: {c['sameEventIdentity']}; terminal times {c['terminalTimes']}.\n"
text+='\nNo candidate 5,000-drone refinement was prescribed here. Passing a 1,000-drone comparison cannot certify the 5,000-drone candidate.\n'
text+='\n## Records and limits\n\n[3D replay](milestone-30-lab.html) · [Protocol](milestone-30-protocol.json) · [Method](milestone-30-source/method.md) · [Checks](milestone-30-artifact-checks.json) · [Initial implementation-error record](milestone-30-error-record/README.md). Actual preceding commands for affected drones are in each run’s `lastControl`. The analytic solver and baseline equivalence checks are in [solver checks](milestone-30-checks.json). Larger flocks start in larger clouds at the same nominal 0.75 m lattice spacing; this is not fixed-volume density scaling. No dynamic safety guarantee, physical calibration, airflow validity, general navigation or novelty claim follows. Concurrent wall times are not a performance benchmark.\n'
text+='\n[All trials as CSV](milestone-30-trials.csv) · [Independent projection reference](milestone-30-reference-checks.json). The independent reference enumerates affine faces and intersects each with the speed ball; all 200 generated feasible problems agree within 1.41e-9 m/s.\n'
held=[r for r in runs if r['job']['kind']=='heldout' and r['config']['count']==1000]
base=[r for r in held if r['config']['filter']=='baseline'];candidate=[r for r in held if r['config']['filter']=='wall-priority'];big=next(r for r in runs if r['config']['count']==5000)
small=[r for r in runs if r['job']['kind']=='heldout' and r['config']['count']==50]
intro=f"## Plain-language result\n\nOn the two fresh 1,000-drone starting flocks, the old filter stopped for contact in {sum(r['metrics']['stopReason'] is not None for r in base)}/2 trials; the wall-priority filter stopped in {sum(r['metrics']['stopReason'] is not None for r in candidate)}/2. Each large-flock test covers 20 seconds only. The 5,000-drone development trial ends at {big['metrics']['end']:.4f} s with {big['metrics']['stopReason'] or 'no contact stop'}.\n\n"
intro+='The 50-drone full-mission comparison finishes '+', '.join(r['config']['filter']+': '+str(r['metrics']['passed'])+'/50' for r in small)+'.\n\n'
if len(small)==2 and small[0]['final']==small[1]['final'] and next(r for r in small if r['config']['filter']=='wall-priority')['diagnostics']['maxIterations']==0:
 intro+='The two 50-drone final states are exactly equal. Wall repair never activates in that candidate run; this is a regression check, not evidence that the repair improves small-flock navigation.\n\n'
if all(r['metrics']['stopReason'] is None for r in runs if r['config']['filter']=='wall-priority'):
 intro+='The correction is promising for the tested early wall failure. Advance it to full-duration large-flock testing; do not call it generally safe or a completed navigation solution. Wall requests can still conflict with requests to keep drones apart, and a later queue or contact remains possible.\n\n'
else:intro+='Wall priority alone is insufficient across these cases. Preserve the failures and investigate the actual pre-contact commands before another controller change.\n\n'
intro+='This changes how competing movement requests are resolved. It preserves local Boids and supplies no individual paths or crossing schedules. The underlying projection method is standard; no algorithmic novelty is claimed. [Next test gate](research-next-controller-gate.md).\n\n'
text=text.replace('## Every planned run',intro+'## Every planned run')
(root/'milestone-30-report.md').write_text(text)
print(json.dumps(dict(runs=len(runs),checks=len(checks),comparisons=comparisons),indent=2))
